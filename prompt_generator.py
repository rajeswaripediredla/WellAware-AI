"""
WellAware AI - Prompt Engineering Module (prompt_generator.py)
Transforms user campaign concepts into concise, high-density diffusion prompts
strictly optimized for CLIP's 77-token limit and high-aesthetic healthcare design.
"""

from typing import Dict, List, Tuple
import config

# ---------------------------------------------------------------------------
# Healthcare Domain Taxonomies (High-Density Semantic Keywords)
# ---------------------------------------------------------------------------
THEME_PRESETS: Dict[str, Dict[str, str]] = {
    "Heart Health": {
        "icon": "🫀",
        "subject": "stylized glowing healthy heart, active pulse wave",
        "elements": "fresh fruits, running shoes, medical stethoscope",
        "palette": "coral red, teal, clean medical cyan, white",
        "default_desc": "vibrant healthy heart surrounded by fresh organic apples and stethoscope"
    },
    "Diabetes Awareness": {
        "icon": "🩸",
        "subject": "balanced blood sugar nutrition plate, blue circle ribbon",
        "elements": "glucometer, colorful fresh vegetables, pure water glass",
        "palette": "diabetes blue, crisp white, leafy green, warm earth tones",
        "default_desc": "healthy balanced meal plate with colorful vegetables and blue Diabetes awareness ribbon"
    },
    "Mental Wellness": {
        "icon": "🧠",
        "subject": "peaceful meditating human silhouette, blooming lotus flower",
        "elements": "serene soft breeze, glowing aura, gentle sunlight, green plants",
        "palette": "calming lavender, sky blue, sage green, soft gold",
        "default_desc": "peaceful mindfulness meditation with blooming lavender flowers and gentle morning sunlight"
    },
    "Healthy Eating": {
        "icon": "🥗",
        "subject": "vibrant Mediterranean nutrient bowl, rainbow fresh food",
        "elements": "sliced avocado, fresh berries, citrus, kale, olive oil, wooden bowl",
        "palette": "emerald green, ruby red, citrus orange, clean ivory",
        "default_desc": "delicious colorful wellness meal bowl with fresh berries, avocado slices, and greens"
    },
    "Physical Fitness": {
        "icon": "🏃",
        "subject": "cheerful people brisk walking and stretching in open nature",
        "elements": "sunlit park trail, running shoes, smartwatch, green trees",
        "palette": "morning amber, forest green, sky blue, bright white",
        "default_desc": "joyful active lifestyle in a sunlit green park with trees and running path"
    },
    "Cancer Awareness": {
        "icon": "🎗️",
        "subject": "supportive caring hands holding an awareness ribbon, gentle sunrise",
        "elements": "delicate flowers, soft dawn light, community solidarity",
        "palette": "hopeful pink, soft violet, warm morning gold, pure white",
        "default_desc": "gentle supportive hands holding an awareness ribbon at golden sunrise"
    },
    "Hygiene Awareness": {
        "icon": "🧼",
        "subject": "clean washing hands with foaming soap bubbles and flowing water",
        "elements": "crystal water droplets, clean white towel, sparkling surface",
        "palette": "aquamarine, oceanic turquoise, sparkling white, silver",
        "default_desc": "crisp clean hands washing with clear water droplets and rich foaming bubbles"
    },
    "Women's Health": {
        "icon": "🌸",
        "subject": "female wellness vitality, graceful botanical motifs",
        "elements": "gentle floral blossoms, stethoscope, nourishing self-care",
        "palette": "soft rose gold, warm terracotta, emerald, cream",
        "default_desc": "empowering women's health vitality surrounded by gentle blossoming flowers"
    },
    "Preventive Healthcare": {
        "icon": "🩺",
        "subject": "routine health checkup, friendly doctor clipboard, heart stethoscope",
        "elements": "modern bright clinic, medical checklist, reassuring smile",
        "palette": "clinical blue, mint green, daylight white, soft silver",
        "default_desc": "friendly preventive health checkup with medical clipboard and stethoscope"
    },
    "Patient Education": {
        "icon": "📖",
        "subject": "clear visual health infographic diagram, friendly healthcare guide",
        "elements": "digital health tablet, anatomical visual guide, medical icons",
        "palette": "instructional navy blue, vibrant teal, warm coral, clean white",
        "default_desc": "accessible healthcare education visual with clear health icons and friendly guide"
    }
}

# ---------------------------------------------------------------------------
# High-Impact Style Modifiers (Front-Loaded for Strong Diffusion Guidance)
# ---------------------------------------------------------------------------
STYLE_DIRECTIVES: Dict[str, Dict[str, str]] = {
    "3D Illustration": {
        "badge": "🎨 3D Isometric",
        "front": "3D clay illustration, isometric render, Pixar style",
        "details": "soft ambient occlusion, smooth matte finish",
        "finish": "trending on ArtStation, 8k, clean isolated background",
        "negative": "photo, ugly, deformed, flat 2d, sketch, dark, grainy, text, watermark"
    },
    "Minimalist": {
        "badge": "📐 Minimalist Vector",
        "front": "minimalist healthcare poster, modern graphic design",
        "details": "clean negative space, bold geometric shapes",
        "finish": "award-winning poster, crisp vector edges, high contrast",
        "negative": "cluttered, noisy, photographic, messy textures, text, watermark"
    },
    "Realistic": {
        "badge": "📸 Photorealistic",
        "front": "commercial healthcare photography, professional award-winning shot",
        "details": "85mm lens, natural studio lighting, authentic smile",
        "finish": "8k UHD, clean studio background, cinematic depth of field",
        "negative": "cartoon, 3d render, drawing, plastic skin, distorted face, text, watermark"
    },
    "Flat Design": {
        "badge": "📊 Modern Flat Art",
        "front": "modern flat vector healthcare graphic, clean corporate aesthetic",
        "details": "bold color blocking, sharp geometric silhouettes",
        "finish": "Dribbble trending vector, clean SVG lines, high visual clarity",
        "negative": "3d render, photo, glossy, complex shadows, noise, text, watermark"
    },
    "Cartoon Illustration": {
        "badge": "🧸 Friendly Cartoon",
        "front": "friendly healthcare storybook illustration, warm patient art",
        "details": "expressive whimsical characters, clean smooth linework",
        "finish": "delightful children health book quality, vibrant, charming",
        "negative": "photorealistic, terrifying, sterile gore, harsh 3d, dark shadows, text, watermark"
    },
    "Professional Healthcare Illustration": {
        "badge": "🏥 Medical Editorial",
        "front": "professional medical journal editorial illustration, clean healthcare graphic",
        "details": "scientific aesthetic, balanced digital watercolor",
        "finish": "Mayo Clinic journal editorial style, crisp, refined",
        "negative": "childish cartoon, surgery gore, morbid, sketch, text, watermark"
    }
}

COMPOSITION_DIRECTIVES: Dict[str, str] = {
    "Square (1:1) - Social Media / Card": "centered iconic composition",
    "Portrait (2:3) - Campaign Poster": "vertical poster layout",
    "Landscape (3:2) - Website Banner": "wide banner layout, rule of thirds"
}


# ---------------------------------------------------------------------------
# Core Generation & Prompt Optimization Functions
# ---------------------------------------------------------------------------
def get_available_themes() -> List[str]:
    """Returns the list of supported healthcare awareness themes."""
    return list(THEME_PRESETS.keys())


def get_available_styles() -> List[str]:
    """Returns the list of supported artistic and graphic styles."""
    return list(STYLE_DIRECTIVES.keys())


def estimate_token_count(text: str) -> int:
    """Estimates the CLIP token count of a given text (approx. 1.25 tokens per word)."""
    words = text.replace(",", " ").replace(".", " ").split()
    return int(len(words) * 1.25) + 2


def build_prompt(
    campaign_title: str = "",
    health_theme: str = "Heart Health",
    user_description: str = "",
    style: str = "3D Illustration",
    aspect_ratio: str = "Square (1:1) - Social Media / Card",
    custom_keywords: str = ""
) -> Tuple[str, str]:
    """
    Synthesizes a punchy, front-loaded diffusion prompt strictly bounded to
    fit within CLIP's 77-token ceiling (~45 to 65 tokens total).
    """
    style_cfg = STYLE_DIRECTIVES.get(style, STYLE_DIRECTIVES["3D Illustration"])
    theme_cfg = THEME_PRESETS.get(health_theme, THEME_PRESETS["Heart Health"])
    composition = COMPOSITION_DIRECTIVES.get(aspect_ratio, "centered composition")

    # Determine core subject
    if user_description.strip():
        core_subject = user_description.strip()
    else:
        core_subject = theme_cfg["default_desc"]

    # Assemble front-loaded, high-impact prompt
    # 1. Front: Style + Primary Subject + Optional Title context
    # 2. Mid: Details + Composition + Palette
    # 3. Tail: Finish & Quality
    style_and_subject = f"{style_cfg['front']} of {core_subject}"
    if campaign_title.strip():
        style_and_subject = f"{style_cfg['front']} for '{campaign_title.strip()}', of {core_subject}"

    prompt_parts = [
        style_and_subject,
        style_cfg["details"],
        f"{theme_cfg['palette']} tones",
        composition,
        style_cfg["finish"]
    ]

    if custom_keywords.strip():
        prompt_parts.append(custom_keywords.strip())

    positive_prompt = ", ".join(prompt_parts)

    # Clean, targeted negative prompt
    base_negative = config.DEFAULT_NEGATIVE_PROMPT
    negative_prompt = f"{style_cfg['negative']}, {base_negative}"

    return positive_prompt, negative_prompt


def get_negative_prompt(style: str = "3D Illustration") -> str:
    """Helper to return the complete negative prompt for a given style."""
    style_cfg = STYLE_DIRECTIVES.get(style, STYLE_DIRECTIVES["3D Illustration"])
    return f"{style_cfg['negative']}, {config.DEFAULT_NEGATIVE_PROMPT}"
