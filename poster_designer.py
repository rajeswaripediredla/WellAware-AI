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


def render_infographic_action_poster(
    base_image: Image.Image,
    title_line1: str = "MENTAL HEALTH",
    title_line2: str = "AWARENESS",
    action_bullets: Optional[list] = None,
    bullet_color: Tuple[int, int, int] = (136, 192, 87),    # Lime green
    header_color: Tuple[int, int, int] = (253, 248, 238),    # Warm cream
    footer_bg: Tuple[int, int, int] = (11, 33, 45)           # Deep navy
) -> Image.Image:
    """
    Renders a complete 3-section Infographic Awareness Poster matching standard
    public health campaign designs:
    1. Top: Large, bold, centered 2-line campaign title
    2. Center: Flat vector artwork visual
    3. Bottom: Solid dark band with bulleted action points (e.g. • UNDERSTAND, • SEEK HELP)
    """
    if action_bullets is None:
        action_bullets = ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"]

    orig_w, orig_h = base_image.size
    
    # We create a standardized vertical poster canvas (ratio roughly 2:3)
    poster_w = orig_w
    # If square, extend canvas height to create vertical poster space
    top_bar_h = int(poster_w * 0.28)
    bot_bar_h = int(poster_w * 0.32)
    poster_h = orig_h + top_bar_h + bot_bar_h

    # Sample top pixel color to seamlessly extend the top header background
    top_sample = base_image.getpixel((poster_w // 2, 8))
    if len(top_sample) == 4:
        bg_rgb = top_sample[:3]
    else:
        bg_rgb = top_sample

    poster = Image.new("RGB", (poster_w, poster_h), color=bg_rgb)
    
    # Paste base image in the middle
    poster.paste(base_image.convert("RGB"), (0, top_bar_h))
    
    # Draw bottom solid footer block
    draw = ImageDraw.Draw(poster)
    draw.rectangle([0, poster_h - bot_bar_h, poster_w, poster_h], fill=footer_bg)

    # 1. RENDER TOP 2-LINE TITLE
    title_size = max(24, int(poster_w * 0.088))
    font_title = get_font(title_size, bold=True)

    # Line 1
    bbox1 = font_title.getbbox(title_line1.strip().upper())
    w1 = bbox1[2] - bbox1[0]
    x1 = (poster_w - w1) // 2
    y1 = int(top_bar_h * 0.16)
    draw.text((x1, y1), title_line1.strip().upper(), font=font_title, fill=header_color)

    # Line 2 (if present)
    if title_line2.strip():
        bbox2 = font_title.getbbox(title_line2.strip().upper())
        w2 = bbox2[2] - bbox2[0]
        x2 = (poster_w - w2) // 2
        y2 = y1 + title_size + 4
        draw.text((x2, y2), title_line2.strip().upper(), font=font_title, fill=header_color)

    # 2. RENDER BOTTOM ACTION BULLETS
    bullet_size = max(16, int(poster_w * 0.052))
    font_bullet = get_font(bullet_size, bold=True)

    bullet_spacing = int(bullet_size * 1.55)
    start_y = poster_h - bot_bar_h + int(bot_bar_h * 0.20)
    bullet_margin_x = int(poster_w * 0.14)

    for item in action_bullets:
        clean_item = item.strip().upper()
        if not clean_item:
            continue
        
        # Draw circular colored bullet dot
        dot_radius = max(4, bullet_size // 4)
        dot_center_x = bullet_margin_x + dot_radius
        dot_center_y = start_y + (bullet_size // 2) + 2
        
        draw.ellipse(
            [dot_center_x - dot_radius, dot_center_y - dot_radius, dot_center_x + dot_radius, dot_center_y + dot_radius],
            fill=bullet_color
        )
        
        # Draw bullet text
        text_x = bullet_margin_x + (dot_radius * 2) + 14
        draw.text((text_x, start_y), clean_item, font=font_bullet, fill=header_color)
        start_y += bullet_spacing

    return poster


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
