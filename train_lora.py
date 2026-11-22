"""
WellAware AI - LoRA Fine-Tuning Module (train_lora.py)
Fine-tunes Stable Diffusion v1.5 cross-attention layers using Low-Rank Adaptation (LoRA)
on custom healthcare campaign visuals.

Outputs: lora_models/wellaware_healthcare_lora.safetensors
"""

import os
import sys
import time
import argparse
from typing import List, Tuple
from PIL import Image

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

try:
    from diffusers import (
        AutoencoderKL,
        UNet2DConditionModel,
        DDPMScheduler
    )
    from diffusers.models.attention_processor import LoRAAttnProcessor
    from transformers import CLIPTokenizer, CLIPTextModel
except ImportError:
    print("[ERROR] Hugging Face 'diffusers' and 'transformers' are required.")
    sys.exit(1)

import config

# ---------------------------------------------------------------------------
# Dataset Definition
# ---------------------------------------------------------------------------
class HealthcareLoRADataset(Dataset):
    """Pairs image files with corresponding .txt caption files in a directory."""

    def __init__(self, data_dir: str, tokenizer: CLIPTokenizer, size: int = 512):
        self.data_dir = data_dir
        self.tokenizer = tokenizer
        self.size = size

        self.image_paths: List[str] = []
        self.captions: List[str] = []

        valid_exts = (".png", ".jpg", ".jpeg", ".webp")
        for fname in sorted(os.listdir(data_dir)):
            if fname.lower().endswith(valid_exts) and not fname.startswith("."):
                img_path = os.path.join(data_dir, fname)
                txt_path = os.path.join(data_dir, os.path.splitext(fname)[0] + ".txt")

                caption = "wellaware style, healthcare wellness campaign visual"
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        caption = f.read().strip() or caption

                self.image_paths.append(img_path)
                self.captions.append(caption)

        if not self.image_paths:
            raise ValueError(f"No valid image files found in '{data_dir}'!")

        self.transforms = transforms.Compose([
            transforms.Resize((size, size), interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])  # Scale to [-1, 1]
        ])

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        img = Image.open(self.image_paths[idx]).convert("RGB")
        pixel_values = self.transforms(img)

        # Tokenize caption (77 max length)
        tokens = self.tokenizer(
            self.captions[idx],
            truncation=True,
            padding="max_length",
            max_length=self.tokenizer.model_max_length,
            return_tensors="pt"
        ).input_ids.squeeze(0)

        return pixel_values, tokens


# ---------------------------------------------------------------------------
# LoRA UNet Configuration
# ---------------------------------------------------------------------------
def setup_lora_unet(unet: UNet2DConditionModel, rank: int = 8) -> Tuple[UNet2DConditionModel, torch.nn.ModuleList]:
    """
    Replaces cross-attention processors in the UNet with trainable LoRAAttnProcessors.
    Freezes all other UNet parameters.
    """
    # Freeze all existing UNet weights
    unet.requires_grad_(False)

    lora_attn_procs = {}
    for name in unet.attn_processors.keys():
        cross_attention_dim = None if name.endswith("attn1.processor") else unet.config.cross_attention_dim
        if name.startswith("mid_block"):
            hidden_size = unet.config.block_out_channels[-1]
        elif name.startswith("up_blocks"):
            block_id = int(name[len("up_blocks.")])
            hidden_size = list(reversed(unet.config.block_out_channels))[block_id]
        elif name.startswith("down_blocks"):
            block_id = int(name[len("down_blocks.")])
            hidden_size = unet.config.block_out_channels[block_id]

        lora_attn_procs[name] = LoRAAttnProcessor(
            hidden_size=hidden_size,
            cross_attention_dim=cross_attention_dim,
            rank=rank
        )

    unet.set_attn_processor(lora_attn_procs)
    lora_layers = torch.nn.ModuleList(unet.attn_processors.values())
    return unet, lora_layers


# ---------------------------------------------------------------------------
# Training Loop
# ---------------------------------------------------------------------------
def train_lora(
    dataset_dir: str = "training_data",
    output_dir: str = "lora_models",
    model_id: str = "runwayml/stable-diffusion-v1-5",
    num_train_steps: int = 100,
    learning_rate: float = 1e-4,
    rank: int = 8,
    batch_size: int = 1,
    gradient_accumulation_steps: int = 2
):
    print("=" * 70)
    print("  WellAware AI - Healthcare LoRA Fine-Tuning Engine")
    print("=" * 70)

    device = config.DEVICE
    dtype = torch.float32 if device == "cpu" else torch.float16
    print(f"Device               : {device.upper()}")
    print(f"Precision            : {dtype}")
    print(f"Base Foundation Model: {model_id}")
    print(f"Dataset Directory    : {dataset_dir}")
    print(f"Target Output Folder : {output_dir}")
    print(f"LoRA Rank (r)        : {rank}")
    print(f"Total Steps          : {num_train_steps}")

    os.makedirs(output_dir, exist_ok=True)

    # 1. Load Tokenizer, VAE, Text Encoder, and UNet
    print("\n[Step 1/4] Loading Pretrained Components...")
    tokenizer = CLIPTokenizer.from_pretrained(model_id, subfolder="tokenizer")
    text_encoder = CLIPTextModel.from_pretrained(model_id, subfolder="text_encoder").to(device, dtype=dtype)
    vae = AutoencoderKL.from_pretrained(model_id, subfolder="vae").to(device, dtype=dtype)
    unet = UNet2DConditionModel.from_pretrained(model_id, subfolder="unet").to(device, dtype=dtype)
    noise_scheduler = DDPMScheduler.from_pretrained(model_id, subfolder="scheduler")

    # Freeze VAE and Text Encoder
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)

    # 2. Setup LoRA Layers on UNet
    print("\n[Step 2/4] Injecting Trainable LoRA Attention Processors...")
    unet, lora_layers = setup_lora_unet(unet, rank=rank)
    lora_layers.to(device)

    trainable_params = sum(p.numel() for p in lora_layers.parameters() if p.requires_grad)
    print(f"  -> Total Trainable LoRA Parameters: {trainable_params:,} (~{trainable_params*4 / (1024**2):.2f} MB)")

    optimizer = torch.optim.AdamW(lora_layers.parameters(), lr=learning_rate)

    # 3. Create DataLoader
    print("\n[Step 3/4] Preparing Dataset Loader...")
    dataset = HealthcareLoRADataset(dataset_dir, tokenizer=tokenizer, size=512)
    train_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    print(f"  -> Loaded {len(dataset)} image-caption pairs.")

    # 4. Training Loop
    print("\n[Step 4/4] Starting LoRA Fine-Tuning...")
    start_time = time.time()
    step = 0
    data_iter = iter(train_dataloader)

    while step < num_train_steps:
        try:
            batch = next(data_iter)
        except StopIteration:
            data_iter = iter(train_dataloader)
            batch = next(data_iter)

        pixel_values, input_ids = batch
        pixel_values = pixel_values.to(device, dtype=dtype)
        input_ids = input_ids.to(device)

        # Convert images to latent space: z = vae.encode(x)
        with torch.no_grad():
            latents = vae.encode(pixel_values).latent_dist.sample()
            latents = latents * vae.config.scaling_factor

        # Sample random noise
        noise = torch.randn_like(latents)
        bsz = latents.shape[0]

        # Sample random timesteps
        timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=device).long()

        # Add noise to latents (Forward diffusion process)
        noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

        # Encode text captions
        with torch.no_grad():
            encoder_hidden_states = text_encoder(input_ids)[0]

        # Predict the noise residual
        model_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample

        # Calculate MSE loss
        loss = F.mse_loss(model_pred.float(), noise.float(), reduction="mean")
        loss = loss / gradient_accumulation_steps
        loss.backward()

        if (step + 1) % gradient_accumulation_steps == 0 or (step + 1) == num_train_steps:
            optimizer.step()
            optimizer.zero_grad()

        step += 1
        if step % 10 == 0 or step == num_train_steps:
            elapsed = time.time() - start_time
            print(f"  [Step {step:03d}/{num_train_steps}] Loss: {loss.item() * gradient_accumulation_steps:.4f} | Elapsed: {elapsed:.1f}s")

    # 5. Save the Trained LoRA Weights
    print("\nSaving Trained Healthcare LoRA Weights...")
    final_output_path = os.path.join(output_dir, "wellaware_healthcare_lora.safetensors")
    
    # Save UNet LoRA attention processor weights in standard safetensors format
    try:
        from safetensors.torch import save_file
        state_dict = {}
        for name, proc in unet.attn_processors.items():
            if isinstance(proc, LoRAAttnProcessor):
                for k, v in proc.state_dict().items():
                    state_dict[f"unet.{name}.{k}"] = v.cpu()
        save_file(state_dict, final_output_path)
        file_size_mb = os.path.getsize(final_output_path) / (1024**2)
        print(f"[SUCCESS] Trained LoRA saved to: {final_output_path} ({file_size_mb:.2f} MB)")
    except Exception as e:
        # Fallback to diffusers save_attn_procs
        unet.save_attn_procs(output_dir)
        print(f"[SUCCESS] Trained LoRA saved to directory: {output_dir}")

    total_time = time.time() - start_time
    print("=" * 70)
    print(f"LoRA Fine-Tuning Completed in {total_time:.1f} seconds!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WellAware AI - LoRA Fine-Tuner")
    parser.add_argument("--dataset_dir", type=str, default="training_data")
    parser.add_argument("--output_dir", type=str, default="lora_models")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--rank", type=int, default=8)
    args = parser.parse_args()

    train_lora(
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        num_train_steps=args.steps,
        learning_rate=args.lr,
        rank=args.rank
    )
