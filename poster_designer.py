"""
WellAware AI - Campaign Poster Typography & Overlay Engine (poster_designer.py)
Renders crisp, publication-grade healthcare campaign headlines, slogans, and
awareness badges directly onto generated visual assets.
"""

import os
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

# Font search paths
FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]


def get_font(size: int = 24, bold: bool = False) -> ImageFont.ImageFont:
    """Attempts to load a modern system TrueType font, falling back gracefully."""
    font_files = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ] + FONT_CANDIDATES

    for fpath in font_files:
        if os.path.exists(fpath):
            try:
                return ImageFont.truetype(fpath, size)
            except Exception:
                continue

    return ImageFont.load_default()


def create_gradient_scrim(width: int, height: int, direction: str = "bottom") -> Image.Image:
    """Creates a smooth semi-transparent dark gradient scrim to guarantee text readability."""
    scrim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scrim)

    max_alpha = 210  # 82% opacity at deepest edge

    for y in range(height):
        if direction == "bottom":
            ratio = y / height
        else:
            ratio = 1.0 - (y / height)
        alpha = int(max_alpha * (ratio ** 1.6))
        draw.line([(0, y), (width, y)], fill=(15, 23, 42, alpha))

    return scrim


def render_campaign_poster(
    base_image: Image.Image,
    headline: str = "HEALTHY HEARTS, VIBRANT LIVES",
    slogan: str = "Balanced Nutrition • Daily Movement • Regular Checkups",
    badge_text: str = "🌿 WELLNESS AWARENESS",
    footer_text: str = "Non-Clinical Patient Education • WellAware AI",
    layout_style: str = "Bottom Card",
    theme_color: Tuple[int, int, int] = (14, 116, 144)  # Teal
) -> Image.Image:
    """
    Renders professional, publication-ready healthcare typography onto the visual.
    
    Layout Options:
        - 'Bottom Card': Gradient scrim at bottom with bold headline, slogan & footer
        - 'Top & Bottom Banner': Top title banner with lower subtitle
        - 'Minimalist Clean': Subtle sleek lower-third typography
    """
    poster = base_image.convert("RGBA").copy()
    w, h = poster.size

    # Dynamic font scaling based on image resolution
    title_size = max(20, int(w * 0.052))
    slogan_size = max(13, int(w * 0.032))
    badge_size = max(10, int(w * 0.024))
    footer_size = max(9, int(w * 0.020))

    font_title = get_font(title_size, bold=True)
    font_slogan = get_font(slogan_size, bold=False)
    font_badge = get_font(badge_size, bold=True)
    font_footer = get_font(footer_size, bold=False)

    # 1. Render Scrim / Backdrop
    scrim_height = int(h * 0.38)
    scrim = create_gradient_scrim(w, scrim_height, direction="bottom")
    poster.paste(scrim, (0, h - scrim_height), scrim)

    draw = ImageDraw.Draw(poster)

    # 2. Render Top Category Badge (if provided)
    if badge_text.strip():
        badge_pad_x, badge_pad_y = 12, 6
        badge_x, badge_y = 24, 24
        
        # Draw badge pill container
        badge_w = int(len(badge_text.strip()) * (badge_size * 0.62)) + 20
        badge_h = badge_size + 14
        
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=badge_h // 2,
            fill=(15, 23, 42, 190),
            outline=(255, 255, 255, 120),
            width=1
        )
        draw.text(
            (badge_x + badge_pad_x, badge_y + badge_pad_y),
            badge_text.strip().upper(),
            font=font_badge,
            fill=(255, 255, 255, 240)
        )

    # 3. Render Headline (All Caps, High Contrast White)
    margin_x = 26
    current_y = h - scrim_height + int(scrim_height * 0.22)

    if headline.strip():
        # Text shadow for extra contrast
        draw.text((margin_x + 1, current_y + 1), headline.strip().upper(), font=font_title, fill=(0, 0, 0, 180))
        draw.text((margin_x, current_y), headline.strip().upper(), font=font_title, fill=(255, 255, 255, 255))
        current_y += title_size + 10

    # 4. Render Slogan / Sub-bullet text
    if slogan.strip():
        draw.text((margin_x + 1, current_y + 1), slogan.strip(), font=font_slogan, fill=(0, 0, 0, 160))
        draw.text((margin_x, current_y), slogan.strip(), font=font_slogan, fill=(224, 242, 254, 245))  # Soft cyan-white
        current_y += slogan_size + 12

    # 5. Render Footer / Medical Disclaimer
    if footer_text.strip():
        footer_y = h - footer_size - 14
        draw.text((margin_x, footer_y), footer_text.strip(), font=font_footer, fill=(148, 163, 184, 210))

    return poster.convert("RGB")
