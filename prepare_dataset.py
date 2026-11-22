"""
WellAware AI - Dataset Preparation Module for LoRA Fine-Tuning (prepare_dataset.py)
Prepares, validates, and formats healthcare image-caption pairs for training.
"""

import os
import shutil
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "training_data")
GENERATED_DIR = os.path.join(BASE_DIR, "generated_images")

# Curated healthcare awareness sample templates (Trigger phrase: "wellaware style")
HEALTHCARE_SAMPLES = [
    {
        "filename": "heart_health_1.png",
        "caption": "wellaware style, 3d isometric illustration of a healthy glowing heart, fresh organic apples, stethoscope, teal and coral tones, clean background"
    },
    {
        "filename": "diabetes_care_1.png",
        "caption": "wellaware style, minimalist healthcare poster of balanced diabetes nutrition plate, blue circle ribbon, fresh vegetables, clean vector edges"
    },
    {
        "filename": "mental_wellness_1.png",
        "caption": "wellaware style, peaceful mindfulness meditation silhouette, blooming lavender, soft morning sunlight, serene lavender and gold tones"
    },
    {
        "filename": "hygiene_care_1.png",
        "caption": "wellaware style, clean hands washing with foaming soap bubbles, crystal water droplets, oceanic turquoise and white tones, crisp vector"
    },
    {
        "filename": "preventive_checkup_1.png",
        "caption": "wellaware style, friendly healthcare checkup, medical clipboard checklist, stethoscope, clinical blue and soft daylight tones"
    }
]


def prepare_starter_dataset():
    """
    Initializes the training_data folder. If existing visuals exist in generated_images,
    it automatically copies and captions them to bootstrap the training dataset.
    """
    os.makedirs(DATASET_DIR, exist_ok=True)
    print("=" * 65)
    print("  WellAware AI - LoRA Dataset Preparation")
    print("=" * 65)
    print(f"Dataset Target Directory: {DATASET_DIR}")

    # Check existing files in generated_images to populate training set
    existing_images = [
        f for f in os.listdir(GENERATED_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg")) and not f.startswith(".")
    ]

    copied_count = 0
    for idx, sample in enumerate(HEALTHCARE_SAMPLES):
        img_name = sample["filename"]
        img_path = os.path.join(DATASET_DIR, img_name)
        txt_path = os.path.join(DATASET_DIR, os.path.splitext(img_name)[0] + ".txt")

        # If source image exists in generated_images, use it
        src_img = None
        if idx < len(existing_images):
            src_img = os.path.join(GENERATED_DIR, existing_images[idx])

        if not os.path.exists(img_path):
            if src_img and os.path.exists(src_img):
                shutil.copy(src_img, img_path)
            else:
                # Create a standardized placeholder RGB 512x512 image if none exists
                dummy = Image.new("RGB", (512, 512), color=(14, 116, 144))
                dummy.save(img_path)

        # Write corresponding caption file
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(sample["caption"])

        copied_count += 1
        print(f"  [+] Prepared: {img_name} <-> {os.path.basename(txt_path)}")
        print(f"      Caption : '{sample['caption'][:60]}...'")

    print("\n" + "=" * 65)
    print(f"Dataset ready! Total training pairs in 'training_data/': {copied_count}")
    print("Trigger keyword to use during generation: 'wellaware style'")
    print("=" * 65)


def add_custom_image(image_path: str, caption: str):
    """
    Utility to add any custom image and caption to the training dataset.
    Resizes image to 512x512 and saves as PNG.
    """
    os.makedirs(DATASET_DIR, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    dest_img = os.path.join(DATASET_DIR, f"{base_name}.png")
    dest_txt = os.path.join(DATASET_DIR, f"{base_name}.txt")

    img = Image.open(image_path).convert("RGB")
    img = img.resize((512, 512), Image.Resampling.LANCZOS)
    img.save(dest_img, "PNG")

    # Ensure trigger token is present
    if "wellaware style" not in caption.lower():
        caption = f"wellaware style, {caption}"

    with open(dest_txt, "w", encoding="utf-8") as f:
        f.write(caption)

    print(f"[OK] Added custom training pair: {dest_img} with caption '{caption}'")


if __name__ == "__main__":
    prepare_starter_dataset()
