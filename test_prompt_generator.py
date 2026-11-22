"""
WellAware AI - Prompt Engineering Verification Script
Validates prompt synthesis, theme presets, style mappings, and negative prompts.
"""

import sys
from prompt_generator import (
    build_prompt,
    get_negative_prompt,
    get_available_themes,
    get_available_styles
)

def run_prompt_tests():
    print("=" * 70)
    print("  WellAware AI - Prompt Engineering Module Verification")
    print("=" * 70)

    # 1. Check supported themes and styles
    themes = get_available_themes()
    styles = get_available_styles()
    print(f"\n[1/3] Supported Themes ({len(themes)}):")
    for t in themes:
        print(f"      - {t}")
        
    print(f"\n      Supported Styles ({len(styles)}):")
    for s in styles:
        print(f"      - {s}")

    assert len(themes) >= 10, "Should support at least 10 health themes"
    assert len(styles) >= 6, "Should support at least 6 artistic styles"

    # 2. Test Case 1: Custom Description + Heart Health + 3D Illustration
    print("\n[2/3] Test Case 1: Custom User Input (Heart Health, 3D Illustration)")
    pos_1, neg_1 = build_prompt(
        campaign_title="Beats of Joy",
        health_theme="Heart Health",
        user_description="an active grandmother smiling while holding a fresh green apple",
        style="3D Illustration",
        aspect_ratio="Portrait (2:3) - Campaign Poster"
    )
    print("\n  >> POSITIVE PROMPT:")
    print(f"  {pos_1}\n")
    print("  >> NEGATIVE PROMPT:")
    print(f"  {neg_1}\n")

    assert "Beats of Joy" in pos_1
    assert "grandmother" in pos_1
    assert "Blender" in pos_1 or "3D" in pos_1
    assert "flat 2d" in neg_1

    # 3. Test Case 2: Minimal/Empty Description (Fallback to Domain Knowledge)
    print("\n[3/3] Test Case 2: Minimal Input / Diabetes Awareness / Minimalist")
    pos_2, neg_2 = build_prompt(
        campaign_title="",
        health_theme="Diabetes Awareness",
        user_description="",
        style="Minimalist",
        aspect_ratio="Landscape (3:2) - Website Banner"
    )
    print("\n  >> POSITIVE PROMPT (Enriched from Domain Taxonomy):")
    print(f"  {pos_2}\n")
    print("  >> NEGATIVE PROMPT:")
    print(f"  {neg_2}\n")

    assert "diabetes" in pos_2.lower()
    assert "minimalist" in pos_2.lower() or "scandinavian" in pos_2.lower()
    assert "cluttered" in neg_2

    print("=" * 70)
    print("ALL PROMPT ENGINEERING TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_prompt_tests()
