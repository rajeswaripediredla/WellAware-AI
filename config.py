"""
WellAware AI - Configuration Module
Central settings for model checkpoints, inference parameters, and hardware defaults.
"""

import os
import torch

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_images")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LORA_DIR = os.path.join(BASE_DIR, "lora_models")
TRAINING_DATA_DIR = os.path.join(BASE_DIR, "training_data")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(LORA_DIR, exist_ok=True)
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

DEFAULT_LORA_PATH = os.path.join(LORA_DIR, "wellaware_healthcare_lora.safetensors")

# ---------------------------------------------------------------------------
# Model Selection & Hugging Face Checkpoint
# ---------------------------------------------------------------------------
# Default Production Model: Stable Diffusion v1.5 (CreativeML OpenRAIL-M)
# High-fidelity, versatile styles, ~4GB download.
MODEL_SD_V15 = "runwayml/stable-diffusion-v1-5"

# Ultra-Fast Local CPU Option: Tiny-SD (Distilled Stable Diffusion, ~700MB)
# Generates 512x512 visuals 4-5x faster on standard laptop CPUs.
MODEL_TINY_SD = "segmind/tiny-sd"

# Active Model: Set to MODEL_SD_V15 for full quality, or MODEL_TINY_SD for rapid CPU testing
MODEL_ID = MODEL_SD_V15

# Hardware Acceleration & Precision
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

# CPU Performance Optimization (use all available physical CPU cores)
if DEVICE == "cpu":
    import os
    cpu_count = os.cpu_count() or 4
    torch.set_num_threads(max(1, cpu_count - 1))

# ---------------------------------------------------------------------------
# Default Inference Hyperparameters
# ---------------------------------------------------------------------------
# With DPMSolverMultistepScheduler, 25 steps provides photorealistic convergence
DEFAULT_NUM_INFERENCE_STEPS = 25
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_SEED = 42

# Aspect Ratio Dimensions (Multiples of 64 required by Latent Diffusion)
ASPECT_RATIOS = {
    "Square (1:1) - Social Media / Card": (512, 512),
    "Portrait (2:3) - Campaign Poster": (512, 768),
    "Landscape (3:2) - Website Banner": (768, 512),
}

# ---------------------------------------------------------------------------
# Negative Prompt Defaults (Strictly suppress in-image text, clutter, and distortions)
# ---------------------------------------------------------------------------
DEFAULT_NEGATIVE_PROMPT = (
    "text, words, letters, alphabet, typography, writing, script, font, "
    "headline, title, label, slogan, banner, logo, brand, watermark, signature, "
    "blurry text, garbled text, pseudotext, characters, quote, captions, numbers, "
    "messy doodles, scribbles, chaotic patterns, crowded background, clutter, "
    "ugly, deformed, disfigured, poor anatomy, bad hands, missing fingers, "
    "extra limbs, blurry, low quality, pixelated, cut off, "
    "hospital horror, gory, morbid, violent, distorted faces"
)
