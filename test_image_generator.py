"""
WellAware AI - Phase 4 Verification Script (test_image_generator.py)
Validates image generation pipeline, singleton lifecycle, variations generation,
and file saving.
"""

import os
import sys
from PIL import Image

import config
from prompt_generator import build_prompt
from image_generator import CampaignImageGenerator

def run_phase4_verification():
    print("=" * 70)
    print("  WellAware AI - Phase 4 Image Generator Verification")
    print("=" * 70)

    # 1. Pipeline Singleton & Device
    generator = CampaignImageGenerator.get_instance()
    print(f"\n[1/3] Initializing Image Generator Singleton:")
    print(f"      - Target Device : {generator.device.upper()}")
    print(f"      - Model ID      : {generator.model_id}")
    print(f"      - Precision     : {generator.dtype}")

    # Load pipeline
    generator.load_pipeline()
    assert generator.is_loaded, "Pipeline failed to report is_loaded=True"
    print("      -> [OK] Pipeline loaded and ready.")

    # 2. Build prompt using prompt_generator
    print(f"\n[2/3] Generating Visual Variations using Synthesized Prompt:")
    theme = "Mental Wellness"
    style = "Minimalist"
    title = "Peace of Mind"
    description = "calm meditation silhouette with blooming lavender and soft sunlight"
    
    pos_prompt, neg_prompt = build_prompt(
        campaign_title=title,
        health_theme=theme,
        user_description=description,
        style=style,
        aspect_ratio="Square (1:1) - Social Media / Card"
    )
    print(f"      - Health Theme : {theme}")
    print(f"      - Style        : {style}")
    print(f"      - Positive     : {pos_prompt[:80]}...")

    # 3. Generate 2 variations with low steps for verification (e.g., 10 steps on CPU)
    steps = 10 if generator.device == "cpu" else 20
    print(f"      - Running 2 variations ({steps} steps each)...")

    variations = generator.generate_variations(
        prompt=pos_prompt,
        negative_prompt=neg_prompt,
        num_variations=2,
        base_seed=101,
        width=512,
        height=512,
        num_inference_steps=steps,
        guidance_scale=7.5
    )

    print(f"\n[3/3] Verifying and Saving Generated Variations:")
    for v in variations:
        idx = v["variation_index"]
        seed = v["seed"]
        img = v["image"]
        gen_time = v["generation_time"]
        
        saved_path = generator.save_visual_to_disk(
            image=img,
            campaign_title=title,
            seed=seed
        )
        assert os.path.exists(saved_path), f"File {saved_path} does not exist!"
        assert img.size == (512, 512), f"Expected 512x512, got {img.size}"
        
        file_size_kb = os.path.getsize(saved_path) / 1024
        print(f"      - Variation #{idx} (Seed {seed}): {gen_time}s | {file_size_kb:.1f} KB")
        print(f"        Saved to: {saved_path}")

    print("\n" + "=" * 70)
    print("PHASE 4 IMAGE GENERATOR ENGINE VERIFIED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_phase4_verification()
