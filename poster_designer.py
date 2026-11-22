"""
WellAware AI - Campaign Poster Typography & Overlay Engine (poster_designer.py)
Renders crisp, publication-grade healthcare campaign posters with authentic commercial
proportions, typography, and layout hierarchy matching real public health campaigns.
"""

import os
from typing import Optional, Tuple, List, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------------------
# Font Discovery & Typographic Hierarchy
# ---------------------------------------------------------------------------
DISPLAY_FONTS = [
    "C:/Windows/Fonts/ARIALNB.TTF",   # Arial Narrow Bold (Condensed headline - ideal for posters)
    "C:/Windows/Fonts/impact.ttf",    # Impact (High-impact display)
    "C:/Windows/Fonts/ariblk.ttf",    # Arial Black
    "C:/Windows/Fonts/framd.ttf",     # Franklin Gothic Medium
    "C:/Windows/Fonts/trebucbd.ttf",  # Trebuchet MS Bold
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]

BOLD_FONTS = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/trebucbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]

REGULAR_FONTS = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/trebuc.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]


def get_font(size: int = 24, bold: bool = False, display: bool = False) -> ImageFont.ImageFont:
    """Loads optimal TrueType fonts for display headlines, body, or badges."""
    candidates = []
    if display:
        candidates = DISPLAY_FONTS + BOLD_FONTS
    elif bold:
        candidates = BOLD_FONTS + REGULAR_FONTS
    else:
        candidates = REGULAR_FONTS + BOLD_FONTS

    for fpath in candidates:
        if os.path.exists(fpath):
            try:
                return ImageFont.truetype(fpath, size)
            except Exception:
                continue

    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Curated Domain Poster Presets (Authentic Real-World Campaign Standards)
# ---------------------------------------------------------------------------
CAMPAIGN_POSTER_PRESETS: Dict[str, Dict] = {
    "Mental Wellness": {
        "title_line1": "MENTAL HEALTH",
        "title_line2": "AWARENESS",
        "badge": "🧠 PUBLIC HEALTH ADVOCACY",
        "bullets": ["UNDERSTAND THE SIGNS", "TALK OPENLY ABOUT IT", "SEEK PROFESSIONAL HELP"],
        "footer": "National Crisis & Suicide Lifeline • Call or Text 988 (Available 24/7)",
        "bullet_color": (136, 192, 87),    # Lime green
        "footer_bg": (11, 33, 45)           # Deep navy
    },
    "Heart Health": {
        "title_line1": "HEART HEALTH",
        "title_line2": "VITALITY & CARE",
        "badge": "🫀 CARDIOVASCULAR HEALTH",
        "bullets": ["EAT HEART-HEALTHY FOODS", "STAY ACTIVE 30 MIN DAILY", "MONITOR BLOOD PRESSURE"],
        "footer": "American Heart Health Initiative • Know Your Numbers • www.heart.org",
        "bullet_color": (239, 68, 68),     # Coral red
        "footer_bg": (30, 15, 20)          # Deep maroon
    },
    "Diabetes Awareness": {
        "title_line1": "PREVENT & MANAGE",
        "title_line2": "DIABETES TODAY",
        "badge": "🩸 METABOLIC WELLNESS",
        "bullets": ["CHOOSE BALANCED NUTRITION", "MAINTAIN ACTIVE LIFESTYLE", "CHECK GLUCOSE REGULARLY"],
        "footer": "National Diabetes Education Program • Learn More at cdc.gov/diabetes",
        "bullet_color": (56, 189, 248),    # Diabetes cyan
        "footer_bg": (10, 25, 45)          # Deep blue
    },
    "Healthy Eating": {
        "title_line1": "FUEL YOUR BODY",
        "title_line2": "HEALTHY NUTRITION",
        "badge": "🥗 NUTRITION & WELLNESS",
        "bullets": ["EAT RAINBOW VEGETABLES", "DRINK PLENTY OF WATER", "LIMIT PROCESSED SUGARS"],
        "footer": "Community Nutrition Network • Eat Well, Live Well • www.nutrition.gov",
        "bullet_color": (74, 222, 128),    # Fresh green
        "footer_bg": (12, 35, 22)          # Deep forest
    },
    "Physical Fitness": {
        "title_line1": "ACTIVE LIVING",
        "title_line2": "FOR EVERY AGE",
        "badge": "🏃 LIFELONG MOBILITY",
        "bullets": ["WALK 7,000+ STEPS DAILY", "STRETCH & BUILD STRENGTH", "TAKE REGULAR ACTIVE BREAKS"],
        "footer": "Move Your Way Campaign • US Dept. of Health & Human Services",
        "bullet_color": (251, 146, 60),    # Energetic amber
        "footer_bg": (20, 25, 35)          # Deep slate
    },
    "Cancer Awareness": {
        "title_line1": "EARLY DETECTION",
        "title_line2": "SAVES LIVES",
        "badge": "🎗️ CANCER ADVOCACY",
        "bullets": ["SCHEDULE REGULAR SCREENINGS", "KNOW FAMILY HEALTH HISTORY", "ADOPT A HEALTHY LIFESTYLE"],
        "footer": "Cancer Information Center • Support & Guidance • 1-800-4-CANCER",
        "bullet_color": (244, 114, 182),   # Awareness pink
        "footer_bg": (35, 15, 25)          # Deep plum
    },
    "Hygiene Awareness": {
        "title_line1": "CLEAN HANDS",
        "title_line2": "SAVE LIVES",
        "badge": "🧼 INFECTION PREVENTION",
        "bullets": ["WASH WITH SOAP 20 SECONDS", "USE ALCOHOL-BASED SANITIZER", "COVER COUGHS AND SNEEZES"],
        "footer": "Clean Hands Protect Everyone • Clean Care is Safer Care • WHO",
        "bullet_color": (34, 211, 238),    # Pure aquamarine
        "footer_bg": (10, 30, 40)          # Oceanic navy
    },
    "Women's Health": {
        "title_line1": "WOMEN'S WELLNESS",
        "title_line2": "PRIORITIZE SELF-CARE",
        "badge": "🌸 EMPOWERED HEALTH",
        "bullets": ["ANNUAL WELL-WOMAN VISITS", "NOURISHING DAILY ROUTINE", "NURTURE MENTAL & BODY HEALTH"],
        "footer": "Office on Women's Health • Empowering Healthy Futures • womenshealth.gov",
        "bullet_color": (251, 113, 133),   # Rose coral
        "footer_bg": (35, 18, 28)          # Deep rose navy
    },
    "Preventive Healthcare": {
        "title_line1": "PREVENTATIVE CARE",
        "title_line2": "YOUR BEST DEFENSE",
        "badge": "🩺 CLINICAL ADVOCACY",
        "bullets": ["ANNUAL HEALTH CHECKUPS", "KEEP VACCINES UP TO DATE", "MONITOR KEY HEALTH VITALS"],
        "footer": "Public Health Advisory Board • Prevention is Protection • www.cdc.gov",
        "bullet_color": (52, 211, 153),    # Mint green
        "footer_bg": (12, 30, 42)          # Clinical navy
    },
    "Patient Education": {
        "title_line1": "KNOW YOUR HEALTH",
        "title_line2": "EMPOWERED CHOICES",
        "badge": "📖 HEALTH LITERACY",
        "bullets": ["ASK YOUR DOCTOR QUESTIONS", "UNDERSTAND YOUR MEDICATIONS", "TRACK YOUR HEALTH PROGRESS"],
        "footer": "Health Literacy Advocacy • Informed Patients, Better Outcomes",
        "bullet_color": (250, 204, 21),    # Warm gold
        "footer_bg": (15, 25, 40)          # Classic navy
    }
}


def get_theme_poster_preset(theme: str) -> Dict:
    """Returns curated poster typography defaults for a given healthcare theme."""
    return CAMPAIGN_POSTER_PRESETS.get(theme, CAMPAIGN_POSTER_PRESETS["Mental Wellness"])


def create_gradient_scrim(width: int, height: int, direction: str = "bottom") -> Image.Image:
    """Creates a smooth semi-transparent dark gradient scrim to guarantee text readability."""
    scrim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scrim)

    max_alpha = 220
    for y in range(height):
        ratio = (y / height) if direction == "bottom" else (1.0 - (y / height))
        alpha = int(max_alpha * (ratio ** 1.5))
        draw.line([(0, y), (width, y)], fill=(11, 23, 38, alpha))

    return scrim


# ---------------------------------------------------------------------------
# Core Poster Layout Engines
# ---------------------------------------------------------------------------

def render_infographic_action_poster(
    base_image: Image.Image,
    title_line1: str = "MENTAL HEALTH",
    title_line2: str = "AWARENESS",
    badge_text: str = "PUBLIC HEALTH ADVOCACY",
    action_bullets: Optional[List[str]] = None,
    bullet_color: Tuple[int, int, int] = (136, 192, 87),
    header_color: Tuple[int, int, int] = (253, 248, 238),
    footer_bg: Tuple[int, int, int] = (11, 33, 45),
    footer_text: str = "National Wellness Initiative • Need Support? Call or Text 988",
    target_width: int = 640,
    target_height: int = 960
) -> Image.Image:
    """
    Renders an authentic, commercial-grade 3-section Infographic Action Poster
    matching standard public health campaigns (2:3 aspect ratio):
      1. Top Header: Category badge + Large bold condensed display headline
      2. Center Hero: Seamlessly feathered AI visual asset
      3. Bottom Action Block: 3 bullet points with colored indicator badges + helpline footer
    """
    if action_bullets is None:
        action_bullets = ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"]

    W = target_width
    H = target_height

    top_h = int(H * 0.22)   # 22% top header (~211px)
    bot_h = int(H * 0.23)   # 23% bottom action block (~220px)
    mid_h = H - top_h - bot_h  # 55% hero artwork (~529px)

    # 1. Sample dominant background from base image edge pixels
    base_rgb = base_image.convert("RGB")
    sample_pt = (min(12, base_image.width - 1), min(12, base_image.height - 1))
    bg_color = base_rgb.getpixel(sample_pt)

    poster = Image.new("RGB", (W, H), color=bg_color)

    # 2. Proportionally scale base image to fit center hero zone
    img_w, img_h = base_image.size
    scale = min(W / img_w, mid_h / img_h)
    new_w, new_h = max(1, int(img_w * scale)), max(1, int(img_h * scale))
    scaled_art = base_image.resize((new_w, new_h), Image.Resampling.LANCZOS).convert("RGBA")

    # 3. Create feather mask for top, left, and right borders so art merges seamlessly
    feather = 18
    mask = Image.new("L", (new_w, new_h), 255)
    draw_mask = ImageDraw.Draw(mask)
    for i in range(feather):
        alpha = int(255 * (i / feather))
        draw_mask.line([(0, i), (new_w, i)], fill=alpha)
        draw_mask.line([(i, 0), (i, new_h)], fill=alpha)
        draw_mask.line([(new_w - 1 - i, 0), (new_w - 1 - i, new_h)], fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2))

    paste_x = (W - new_w) // 2
    paste_y = top_h + (mid_h - new_h) // 2
    poster.paste(scaled_art.convert("RGB"), (paste_x, paste_y), mask=mask)

    # 4. Draw bottom solid footer block
    draw = ImageDraw.Draw(poster)
    draw.rectangle([0, H - bot_h, W, H], fill=footer_bg)

    # 5. RENDER TOP HEADER & DISPLAY TITLE
    # Category badge
    if badge_text.strip():
        font_badge = get_font(size=12, bold=True)
        clean_badge = badge_text.strip().upper()
        bbox_b = font_badge.getbbox(clean_badge)
        bw = bbox_b[2] - bbox_b[0]
        bx = (W - bw) // 2
        draw.text((bx, 22), clean_badge, font=font_badge, fill=(200, 230, 235))

    # Display headline (Arial Narrow Bold / Impact / Arial Black)
    font_title = get_font(size=56, display=True)
    clean_l1 = title_line1.strip().upper()
    clean_l2 = title_line2.strip().upper()

    # Dynamic auto-scaling if title is long
    bbox1 = font_title.getbbox(clean_l1)
    w1 = bbox1[2] - bbox1[0]
    if w1 > W - 40:
        font_title = get_font(size=44, display=True)
        bbox1 = font_title.getbbox(clean_l1)
        w1 = bbox1[2] - bbox1[0]

    y_line1 = 50
    draw.text(((W - w1) // 2, y_line1), clean_l1, font=font_title, fill=header_color)

    if clean_l2:
        bbox2 = font_title.getbbox(clean_l2)
        w2 = bbox2[2] - bbox2[0]
        y_line2 = y_line1 + 62
        draw.text(((W - w2) // 2, y_line2), clean_l2, font=font_title, fill=header_color)

    # 6. RENDER BOTTOM ACTION BULLETS
    font_bullet = get_font(size=28, display=True)
    bullet_margin = max(40, int(W * 0.12))
    start_by = H - bot_h + 36
    line_step = 44

    for item in action_bullets[:3]:
        clean_item = item.strip().upper()
        if not clean_item:
            continue
        # Circular badge dot
        dot_r = 8
        dot_x = bullet_margin
        dot_y = start_by + 14
        draw.ellipse([dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r], fill=bullet_color)
        draw.text((bullet_margin + 28, start_by), clean_item, font=font_bullet, fill=header_color)
        start_by += line_step

    # 7. RENDER HELPLINE / ORGANIZATION FOOTER
    if footer_text.strip():
        font_foot = get_font(size=12, bold=False)
        clean_foot = footer_text.strip()
        bbox_f = font_foot.getbbox(clean_foot)
        fw = bbox_f[2] - bbox_f[0]
        draw.text(((W - fw) // 2, H - 28), clean_foot, font=font_foot, fill=(140, 165, 180))

    return poster


def render_campaign_poster(
    base_image: Image.Image,
    headline: str = "HEALTHY HEARTS, VIBRANT LIVES",
    slogan: str = "Balanced Nutrition • Daily Movement • Regular Checkups",
    badge_text: str = "🌿 WELLNESS AWARENESS",
    footer_text: str = "Non-Clinical Patient Education • WellAware AI",
    layout_style: str = "Bottom Card",
    theme_color: Tuple[int, int, int] = (14, 116, 144),
    target_width: int = 640,
    target_height: int = 960
) -> Image.Image:
    """
    Renders an editorial full-bleed campaign poster with a dark gradient scrim
    and modern typography over the visual (standard 2:3 aspect ratio).
    """
    W = target_width
    H = target_height

    # Scale base image to fill canvas nicely
    img_w, img_h = base_image.size
    scale = max(W / img_w, H / img_h)
    nw, nh = int(img_w * scale), int(img_h * scale)
    scaled_art = base_image.resize((nw, nh), Image.Resampling.LANCZOS).convert("RGBA")
    
    # Crop to exact canvas
    left = (nw - W) // 2
    top = (nh - H) // 2
    poster = scaled_art.crop((left, top, left + W, top + H))

    # Gradient scrim at bottom
    scrim_h = int(H * 0.40)
    scrim = create_gradient_scrim(W, scrim_h, direction="bottom")
    poster.paste(scrim, (0, H - scrim_h), scrim)

    draw = ImageDraw.Draw(poster)

    # Category Pill Badge at Top Left
    if badge_text.strip():
        font_badge = get_font(size=12, bold=True)
        badge_pad_x, badge_pad_y = 12, 6
        badge_x, badge_y = 28, 28
        b_clean = badge_text.strip().upper()
        bb = font_badge.getbbox(b_clean)
        bw = (bb[2] - bb[0]) + (badge_pad_x * 2)
        bh = (bb[3] - bb[1]) + (badge_pad_y * 2) + 2

        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + bw, badge_y + bh],
            radius=bh // 2,
            fill=(15, 23, 42, 210),
            outline=(255, 255, 255, 140),
            width=1
        )
        draw.text((badge_x + badge_pad_x, badge_y + badge_pad_y), b_clean, font=font_badge, fill=(255, 255, 255))

    # Bold Headline in Lower Third
    font_title = get_font(size=44, display=True)
    margin_x = 32
    curr_y = H - scrim_h + int(scrim_h * 0.22)

    if headline.strip():
        clean_head = headline.strip().upper()
        # Drop shadow for ultra clarity
        draw.text((margin_x + 2, curr_y + 2), clean_head, font=font_title, fill=(0, 0, 0, 200))
        draw.text((margin_x, curr_y), clean_head, font=font_title, fill=(255, 255, 255))
        curr_y += 54

    # Slogan
    if slogan.strip():
        font_slogan = get_font(size=18, bold=False)
        draw.text((margin_x + 1, curr_y + 1), slogan.strip(), font=font_slogan, fill=(0, 0, 0, 160))
        draw.text((margin_x, curr_y), slogan.strip(), font=font_slogan, fill=(224, 242, 254))
        curr_y += 32

    # Footer
    if footer_text.strip():
        font_foot = get_font(size=12, bold=False)
        draw.text((margin_x, H - 32), footer_text.strip(), font=font_foot, fill=(148, 163, 184))

    return poster.convert("RGB")
