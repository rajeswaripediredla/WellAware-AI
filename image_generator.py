"""
WellAware AI - Image Generation Module (image_generator.py)
Encapsulates Hugging Face Diffusers pipeline loading, memory management,
deterministic and variation-based latent diffusion inference, and file persistence.
"""

import os
import gc
import time
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from PIL import Image
import torch

try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
except ImportError:
    raise ImportError(
        "Hugging Face 'diffusers' is not installed. Please run: pip install -r requirements.txt"
    )

import config


class CampaignImageGenerator:
    """
    Manages the lifecycle and inference execution of the Stable Diffusion pipeline
    for WellAware AI patient wellness visuals.
    """

    _instance: Optional["CampaignImageGenerator"] = None

    def __init__(self, model_id: Optional[str] = None):
        self.model_id = model_id or config.MODEL_ID
        self.device = config.DEVICE
        self.dtype = config.TORCH_DTYPE
        self.pipe: Optional[StableDiffusionPipeline] = None
        self.is_loaded: bool = False

    @classmethod
    def get_instance(cls, model_id: Optional[str] = None) -> "CampaignImageGenerator":
        """Singleton accessor to prevent reloading multi-gigabyte models into RAM."""
        if cls._instance is None:
            cls._instance = cls(model_id=model_id)
        return cls._instance

    def load_pipeline(self) -> None:
        """Loads and optimizes the Stable Diffusion pipeline in memory."""
        if self.is_loaded and self.pipe is not None:
            return

        print(f"[ImageGenerator] Loading model '{self.model_id}' on {self.device.upper()}...")
        start_time = time.time()

        # 1. Load pipeline from Hugging Face hub or local cache
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=self.dtype,
            safety_checker=None  # Can be enabled or kept none for health campaigns
        )

        # 2. Configure DPM-Solver++ Multistep Scheduler with Karras noise sigmas
        # Karras sigmas ensure sharper edges and anatomical fidelity at 20 steps
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config,
            use_karras_sigmas=True
        )

        # 3. Move pipeline to compute device (CUDA or CPU)
        self.pipe = self.pipe.to(self.device)

        # 4. Memory and throughput optimizations
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            if hasattr(self.pipe, "enable_vae_slicing"):
                self.pipe.enable_vae_slicing()
            print("  -> GPU optimizations enabled (attention slicing & VAE slicing).")
        else:
            # Enable attention slicing on CPU as well to minimize peak RAM spikes
            self.pipe.enable_attention_slicing()
            print("  -> CPU optimizations enabled.")

        load_time = time.time() - start_time
        self.is_loaded = True
        print(f"[ImageGenerator] Model successfully loaded in {load_time:.2f} seconds.")

    def load_lora_weights(self, lora_path: Optional[str] = None, weight_name: Optional[str] = None) -> bool:
        """Loads custom trained LoRA adapter weights into the active pipeline."""
        if not self.is_loaded or self.pipe is None:
            self.load_pipeline()

        target_path = lora_path or config.DEFAULT_LORA_PATH
        if os.path.exists(target_path):
            try:
                if os.path.isdir(target_path):
                    self.pipe.load_lora_weights(target_path, weight_name=weight_name)
                else:
                    folder = os.path.dirname(target_path)
                    fname = os.path.basename(target_path)
                    self.pipe.load_lora_weights(folder, weight_name=fname)
                print(f"[ImageGenerator] Successfully loaded LoRA weights from: {target_path}")
                return True
            except Exception as e:
                print(f"[ImageGenerator] Could not load LoRA weights: {e}")
                return False
        return False

    def unload_lora_weights(self) -> None:
        """Unloads LoRA adapters from the UNet."""
        if self.is_loaded and self.pipe is not None:
            try:
                self.pipe.unload_lora_weights()
                print("[ImageGenerator] LoRA weights unloaded.")
            except Exception:
                pass

    def generate_single_visual(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        seed: Optional[int] = None,
        step_callback: Optional[Callable[[int, int, Any], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes latent diffusion inference to generate a single wellness campaign visual.

        Returns a dictionary containing:
            - 'image': PIL Image
            - 'seed': Integer seed used
            - 'generation_time': Float duration in seconds
            - 'width': Integer width
            - 'height': Integer height
        """
        if not self.is_loaded or self.pipe is None:
            self.load_pipeline()

        # Default inference parameters
        if num_inference_steps is None:
            num_inference_steps = (
                20 if self.device == "cpu" else config.DEFAULT_NUM_INFERENCE_STEPS
            )
        if guidance_scale is None:
            guidance_scale = config.DEFAULT_GUIDANCE_SCALE
        if negative_prompt is None:
            negative_prompt = config.DEFAULT_NEGATIVE_PROMPT

        # Deterministic seed management
        active_seed = int(seed) if seed is not None else int(torch.randint(0, 2**32 - 1, (1,)).item())
        generator = torch.Generator(device=self.device).manual_seed(active_seed)

        start_time = time.time()

        # Callback adapter for step progress reporting
        diffusers_callback = None
        if step_callback is not None:
            def _cb(step: int, timestep: int, latents: Any):
                step_callback(step + 1, num_inference_steps, latents)
            diffusers_callback = _cb

        # Run diffusion inference
        pipe_kwargs: Dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "width": width,
            "height": height,
            "generator": generator,
        }
        if diffusers_callback is not None:
            pipe_kwargs["callback"] = diffusers_callback
            pipe_kwargs["callback_steps"] = 1

        output = self.pipe(**pipe_kwargs)
        image = output.images[0]
        gen_time = time.time() - start_time

        # Force garbage collection to prevent memory fragmentation
        if self.device == "cuda":
            torch.cuda.empty_cache()
        gc.collect()

        return {
            "image": image,
            "seed": active_seed,
            "generation_time": round(gen_time, 2),
            "width": width,
            "height": height,
            "steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "prompt": prompt,
            "negative_prompt": negative_prompt
        }

    def generate_variations(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_variations: int = 2,
        base_seed: Optional[int] = None,
        width: int = 512,
        height: int = 512,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        variation_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates multiple variations (1 to 4) of a campaign visual by systematically
        varying the latent noise seed.
        """
        num_variations = max(1, min(4, num_variations))
        if base_seed is None:
            base_seed = int(torch.randint(0, 1000000, (1,)).item())

        results: List[Dict[str, Any]] = []

        for idx in range(num_variations):
            variation_seed = base_seed + (idx * 17)
            if variation_callback:
                variation_callback(idx + 1, num_variations)

            result = self.generate_single_visual(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                seed=variation_seed
            )
            result["variation_index"] = idx + 1
            results.append(result)

        return results

    def save_visual_to_disk(
        self,
        image: Image.Image,
        campaign_title: str = "campaign",
        seed: Optional[int] = None
    ) -> str:
        """
        Persists a generated PIL image into the 'generated_images' folder with a
        sanitized, timestamped filename. Returns the absolute file path.
        """
        # Sanitize campaign title for filesystem
        safe_title = re.sub(r"[^\w\-_]", "_", campaign_title.strip().lower())
        safe_title = safe_title[:30] or "campaign"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        seed_str = f"_seed{seed}" if seed is not None else ""
        filename = f"{safe_title}_{timestamp}{seed_str}.png"
        filepath = os.path.join(config.OUTPUT_DIR, filename)

        image.save(filepath, format="PNG", optimize=True)
        return filepath

    @staticmethod
    def postprocess_image(
        image: Image.Image,
        sharpness: float = 1.15,
        contrast: float = 1.05,
        color: float = 1.05
    ) -> Image.Image:
        """
        Applies subtle editorial post-processing to enhance edge sharpness,
        color vibrance, and contrast for publication-grade wellness visuals.
        """
        from PIL import ImageEnhance
        enhanced = image
        if sharpness != 1.0:
            enhanced = ImageEnhance.Sharpness(enhanced).enhance(sharpness)
        if contrast != 1.0:
            enhanced = ImageEnhance.Contrast(enhanced).enhance(contrast)
        if color != 1.0:
            enhanced = ImageEnhance.Color(enhanced).enhance(color)
        return enhanced
