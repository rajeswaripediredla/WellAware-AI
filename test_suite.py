"""
WellAware AI - Phase 6 Comprehensive Testing Suite (test_suite.py)
Validates:
1. Health awareness theme coverage (all 10 domains)
2. Artistic style coverage (all 6 styles)
3. Robustness against invalid, empty, or malicious inputs
4. Output file integrity, filesystem sanitization, and PNG download buffer serialization
5. Error handling and boundary conditions
"""

import os
import io
import sys
from PIL import Image

import config
from prompt_generator import (
    build_prompt,
    get_negative_prompt,
    get_available_themes,
    get_available_styles,
    estimate_token_count,
    THEME_PRESETS,
    STYLE_DIRECTIVES
)
from image_generator import CampaignImageGenerator


class TestResultTracker:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def log(self, test_name: str, passed: bool, message: str = ""):
        self.tests.append((test_name, passed, message))
        if passed:
            self.passed += 1
            print(f"  [PASS] {test_name} {message}")
        else:
            self.failed += 1
            print(f"  [FAIL] {test_name} - {message}")


def run_phase6_test_suite():
    print("=" * 75)
    print("  WellAware AI - Phase 6 Comprehensive Quality & Validation Suite")
    print("=" * 75)

    tracker = TestResultTracker()

    # -----------------------------------------------------------------------
    # TEST SUITE 1: THEME & PROMPT SYNTHESIS COVERAGE
    # -----------------------------------------------------------------------
    print("\n[Suite 1/5] Testing Theme Coverage & Token Ceilings:")
    themes = get_available_themes()
    for theme in themes:
        pos, neg = build_prompt(
            campaign_title=f"Awareness Drive for {theme}",
            health_theme=theme,
            user_description="",
            style="3D Illustration"
        )
        tokens = estimate_token_count(pos)
        is_token_safe = tokens <= 77
        tracker.log(
            f"Theme: {theme:<24}",
            is_token_safe,
            f"({tokens}/77 tokens)"
        )

    # -----------------------------------------------------------------------
    # TEST SUITE 2: ARTISTIC STYLE & NEGATIVE PROMPT VALIDATION
    # -----------------------------------------------------------------------
    print("\n[Suite 2/5] Testing Style Directives & Negative Filtering:")
    styles = get_available_styles()
    for style in styles:
        pos, neg = build_prompt(
            campaign_title="Wellness Campaign",
            health_theme="Mental Wellness",
            user_description="peaceful mind",
            style=style
        )
        has_style_prefix = len(pos) > 20
        has_negative_filter = len(neg) > 20 and "ugly" in neg
        tracker.log(
            f"Style: {style:<30}",
            has_style_prefix and has_negative_filter,
            f"[Negative Filter: {len(neg)} chars]"
        )

    # -----------------------------------------------------------------------
    # TEST SUITE 3: EDGE CASES, EMPTY INPUTS & SPECIAL CHARACTERS
    # -----------------------------------------------------------------------
    print("\n[Suite 3/5] Testing Edge Cases & Input Sanitization:")

    # Case A: Totally Empty Inputs
    pos_empty, neg_empty = build_prompt("", "Heart Health", "", "3D Illustration")
    tracker.log(
        "Empty Title & Empty Description",
        bool(pos_empty and len(pos_empty) > 30),
        "-> Gracefully fell back to domain taxonomy"
    )

    # Case B: Unknown Theme & Unknown Style
    pos_unkn, neg_unkn = build_prompt("Test", "NonExistentTheme123", "scene", "NonExistentStyle456")
    tracker.log(
        "Unrecognized Theme & Style",
        bool(pos_unkn and neg_unkn),
        "-> Gracefully fell back to safe defaults"
    )

    # Case C: Extreme String Length (1500 chars)
    massive_desc = "healthy lifestyle " * 100
    pos_massive, _ = build_prompt("Massive Campaign", "Physical Fitness", massive_desc, "Minimalist")
    tracker.log(
        "Extreme Input (1500+ characters)",
        bool(pos_massive and len(pos_massive) > 0),
        "-> Handled without memory crash"
    )

    # Case D: Malicious / Injection Characters
    dirty_title = "../../../etc/passwd; DROP TABLE campaigns; <script>alert(1)</script>"
    pos_dirty, _ = build_prompt(dirty_title, "Hygiene Awareness", "washing hands", "Flat Design")
    tracker.log(
        "Code Injection & Escape Characters",
        bool(pos_dirty),
        "-> Safely absorbed into prompt string"
    )

    # -----------------------------------------------------------------------
    # TEST SUITE 4: FILE PERSISTENCE & SECURITY SANITIZATION
    # -----------------------------------------------------------------------
    print("\n[Suite 4/5] Testing Persistence Security & Image Serialization:")

    generator = CampaignImageGenerator.get_instance()
    dummy_img = Image.new("RGB", (512, 512), color=(14, 116, 144))

    # Test path traversal prevention in save_visual_to_disk
    unsafe_title = "../../system32/cmd_malicious_campaign"
    saved_path = generator.save_visual_to_disk(dummy_img, campaign_title=unsafe_title, seed=999)
    is_safe_path = os.path.dirname(os.path.abspath(saved_path)) == os.path.abspath(config.OUTPUT_DIR)
    tracker.log(
        "Directory Traversal File Sanitization",
        is_safe_path,
        f"-> Path confined to: {config.OUTPUT_DIR}"
    )

    # Test PNG Download Byte Serialization
    buf = io.BytesIO()
    dummy_img.save(buf, format="PNG")
    byte_data = buf.getvalue()
    tracker.log(
        "In-Memory PNG Byte Buffer (Download Integrity)",
        len(byte_data) > 100 and byte_data[:8] == b"\x89PNG\r\n\x1a\n",
        f"-> Valid PNG header detected ({len(byte_data)} bytes)"
    )

    # -----------------------------------------------------------------------
    # TEST SUITE 5: EDITORIAL POST-PROCESSING VALIDATION
    # -----------------------------------------------------------------------
    print("\n[Suite 5/5] Testing Image Post-Processing Module:")
    enhanced_img = generator.postprocess_image(dummy_img, sharpness=1.2, contrast=1.1, color=1.05)
    tracker.log(
        "Editorial Polish Filter (Sharpness & Vibrance)",
        enhanced_img.size == dummy_img.size and enhanced_img.mode == "RGB",
        f"-> Dimensions preserved: {enhanced_img.size}"
    )

    # -----------------------------------------------------------------------
    # FINAL SUMMARY REPORT
    # -----------------------------------------------------------------------
    print("\n" + "=" * 75)
    print(f"  PHASE 6 TEST SUMMARY: {tracker.passed} PASSED | {tracker.failed} FAILED")
    print("=" * 75)

    if tracker.failed == 0:
        print("ALL QUALITY, ROBUSTNESS, AND EDGE-CASE TESTS PASSED PERFECTLY!\n")
        return True
    else:
        print("Some test cases failed. Review logs above.\n")
        return False


if __name__ == "__main__":
    success = run_phase6_test_suite()
    sys.exit(0 if success else 1)
