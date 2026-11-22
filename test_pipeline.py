"""
WellAware AI - Phase 2 Pipeline Verification Script
Tests loading of the model checkpoint and executes a minimal generation cycle.
Can run on both CUDA GPU and CPU fallback.
"""

import os
import sys
import torch
from PIL import Image

try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
except ImportError:
    print("[ERROR] Hugging Face 'diffusers' is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

import config

def run_phase2_test():
    print("=" * 65)
    print("  WellAware AI - Phase 2 Pipeline & Model Verification")
    print("=" * 65)

    device = config.DEVICE
    dtype = config.TORCH_DTYPE
    print(f"Target Compute Device : {device.upper()}")
    print(f"Floating-Point Type   : {dtype}")
    print(f"Model Identifier      : {config.MODEL_ID}")

    print("\n[Step 1/3] Loading Pretrained Stable Diffusion Pipeline...")
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            config.MODEL_ID,
            torch_dtype=dtype,
            safety_checker=None
        )
        
        # Accelerate with DPM-Solver++
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to(device)

        if device == "cuda":
            pipe.enable_attention_slicing()
            print("  -> Enabled attention slicing for GPU VRAM optimization.")
        else:
            print("  -> Running on CPU. (Note: CPU generation requires more time).")

        print("  -> [SUCCESS] Pretrained model loaded into memory.")
    except Exception as e:
        print(f"  -> [FAILED] Could not load model: {e}")
        return False

    print("\n[Step 2/3] Generating Baseline Wellness Awareness Visual...")
    sample_prompt = (
        "A clean healthcare wellness campaign poster for heart health awareness, "
        "a stylized healthy heart symbol surrounded by fresh organic fruits and running shoes, "
        "minimalist 3D vector illustration, soft morning light, soothing teal and coral palette, 8k"
    )
    
    # On CPU, 12-15 steps with DPMSolver is optimal for fast convergence
    steps = 15 if device == "cpu" else config.DEFAULT_NUM_INFERENCE_STEPS
    print(f"  -> Prompt       : {sample_prompt[:70]}...")
    print(f"  -> Steps        : {steps} steps (DPM-Solver++ Multistep)")
    print(f"  -> Dimensions   : 512x512")
    print(f"  -> Guidance     : {config.DEFAULT_GUIDANCE_SCALE}")
    print(f"  -> Starting inference... (Please wait while diffusion denoises latents)")

    import time
    start_time = time.time()
    generator = torch.Generator(device=device).manual_seed(config.DEFAULT_SEED)

    try:
        output = pipe(
            prompt=sample_prompt,
            negative_prompt=config.DEFAULT_NEGATIVE_PROMPT,
            num_inference_steps=steps,
            guidance_scale=config.DEFAULT_GUIDANCE_SCALE,
            width=512,
            height=512,
            generator=generator
        )
        elapsed = time.time() - start_time
        img = output.images[0]
        print(f"  -> [SUCCESS] Image generated in {elapsed:.1f}s! Resolution: {img.size}")
    except Exception as e:
        print(f"  -> [FAILED] Generation error: {e}")
        return False

    print("\n[Step 3/3] Saving Output Image...")
    output_path = os.path.join(config.OUTPUT_DIR, "heart_health_sample.png")
    img.save(output_path)
    print(f"  -> [SUCCESS] Saved test visual to: {output_path}")

    print("=" * 65)
    print("Phase 2 pipeline verification complete!")
    print("=" * 65)
    return True

if __name__ == "__main__":
    run_phase2_test()
