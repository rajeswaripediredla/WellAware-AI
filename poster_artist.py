"""
WellAware AI - Pure Pillow Poster Artist (poster_artist.py)
============================================================
Draws complete healthcare awareness posters 100% programmatically using
Pillow — zero Stable Diffusion involvement.

Every element (illustration, shapes, icons, typography) is drawn with
Pillow's ImageDraw, so text is ALWAYS pixel-perfect with zero garbling.

This matches the reference poster style:
  • Top section  : Large bold campaign title on teal background
  • Middle section: Flat vector-style character illustration with icons
  • Bottom section: Dark navy panel with bullet action points
"""

import math
import os
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

FONT_PATHS_BOLD = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/verdanab.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]
FONT_PATHS_REGULAR = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/verdana.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = FONT_PATHS_BOLD if bold else FONT_PATHS_REGULAR
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    # Fallback: try to scale default
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font) -> Tuple[int, int]:
    """Return (width, height) of rendered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    center_x: int,
    y: int,
    fill,
    shadow_fill=None,
):
    """Draw horizontally-centred text with optional drop shadow."""
    w, _ = _text_size(draw, text, font)
    x = center_x - w // 2
    if shadow_fill:
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_fill)
    draw.text((x, y), text, font=font, fill=fill)
    return w


# ---------------------------------------------------------------------------
# Shape primitives
# ---------------------------------------------------------------------------

def _rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    radius: int,
    fill=None,
    outline=None,
    width: int = 1,
):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _draw_heart(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    size: int,
    fill,
):
    """Draw a simple heart shape using two ellipses + a polygon."""
    half = size // 2
    q = size // 4

    # Two top lobes
    draw.ellipse([cx - half, cy - q, cx, cy + q], fill=fill)
    draw.ellipse([cx, cy - q, cx + half, cy + q], fill=fill)

    # Bottom triangle
    draw.polygon(
        [(cx - half, cy + q // 2), (cx, cy + half + q // 2), (cx + half, cy + q // 2)],
        fill=fill,
    )


def _draw_ribbon(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    size: int,
    fill,
):
    """
    Draw an awareness ribbon (two angled teardrop loops + V-tail).
    Classic cancer/awareness ribbon shape.
    """
    # Loop dimensions
    lw = int(size * 0.38)   # loop half-width
    lh = int(size * 0.52)   # loop height
    gap = max(3, size // 14)

    # Left loop — tilted slightly inward at top
    draw.ellipse(
        [cx - lw * 2 - gap, cy - lh, cx - gap, cy + lh // 3],
        fill=fill,
    )
    # Right loop — mirror
    draw.ellipse(
        [cx + gap, cy - lh, cx + lw * 2 + gap, cy + lh // 3],
        fill=fill,
    )

    # Centre knot (small dark-shaded oval where loops cross)
    knot_r = max(4, size // 9)
    draw.ellipse(
        [cx - knot_r, cy - knot_r // 2, cx + knot_r, cy + knot_r + knot_r // 2],
        fill=fill,
    )

    # Tail — two angled strips forming a V
    tail_top = cy + lh // 4
    tail_tip_y = cy + lh + size // 3
    strip_w = max(3, size // 9)
    # Left tail strip
    draw.polygon(
        [
            (cx - strip_w, tail_top),
            (cx, tail_top),
            (cx - strip_w // 2, tail_tip_y),
            (cx - strip_w - strip_w // 2, tail_tip_y - strip_w),
        ],
        fill=fill,
    )
    # Right tail strip
    draw.polygon(
        [
            (cx, tail_top),
            (cx + strip_w, tail_top),
            (cx + strip_w + strip_w // 2, tail_tip_y - strip_w),
            (cx + strip_w // 2, tail_tip_y),
        ],
        fill=fill,
    )


def _draw_tangled_brain_cloud(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    cloud_fill,
    tangle_color,
):
    """
    Draw the iconic 'tangled mind' icon:
    - White organic cloud/thought-bubble shape
    - Dark tangled scribble lines inside (drawn deterministically)
    """
    r = radius

    # ── Cloud body: overlapping circles forming an organic blob ──────────
    # Main large centre ellipse (wider than tall, like a thought bubble)
    draw.ellipse(
        [cx - r, cy - int(r * 0.65), cx + r, cy + int(r * 0.65)],
        fill=cloud_fill,
    )
    # Top bumps
    for ox, oy, cr in [
        (-int(r * 0.45), -int(r * 0.50), int(r * 0.50)),
        (int(r * 0.45),  -int(r * 0.50), int(r * 0.50)),
        (0,              -int(r * 0.62), int(r * 0.42)),
    ]:
        draw.ellipse(
            [cx + ox - cr, cy + oy - cr, cx + ox + cr, cy + oy + cr],
            fill=cloud_fill,
        )
    # Side bumps
    draw.ellipse(
        [cx - r - int(r * 0.30), cy - int(r * 0.25), cx - r + int(r * 0.30), cy + int(r * 0.25)],
        fill=cloud_fill,
    )
    draw.ellipse(
        [cx + r - int(r * 0.30), cy - int(r * 0.25), cx + r + int(r * 0.30), cy + int(r * 0.25)],
        fill=cloud_fill,
    )

    # ── Tangled scribble lines inside cloud ───────────────────────────────
    # Draw overlapping wavy strokes — fewer, thinner, clearly separate
    line_w = max(2, radius // 20)
    inner_rx = int(r * 0.56)   # keep strokes inside main cloud ellipse
    inner_ry = int(r * 0.44)

    # 8 individual tangled strands with different phases & frequencies
    strand_configs = [
        (0.0,  2, 1.0, 0.7),
        (0.4,  3, 0.9, 0.6),
        (0.8,  2, 0.8, 0.8),
        (1.2,  3, 0.7, 0.5),
        (1.6,  2, 1.0, 0.6),
        (2.0,  3, 0.85, 0.75),
        (2.5,  2, 0.9, 0.55),
        (3.0,  3, 0.75, 0.65),
    ]
    for phase, freq, amp_x, amp_y in strand_configs:
        pts = []
        for j in range(60):
            t = phase + (j / 59) * 2 * math.pi * 1.5
            px = cx + int(inner_rx * amp_x * math.sin(t))
            py = cy + int(inner_ry * amp_y * math.cos(freq * t))
            pts.append((px, py))
        if len(pts) > 1:
            draw.line(pts, fill=tangle_color, width=line_w)


def _draw_person_mental_health(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    scale: float,
    skin: Tuple,
    shirt: Tuple,
    hair: Tuple,
    bg: Tuple,
):
    """
    Draw a flat-vector woman touching her forehead, looking sad/stressed.
    Matches the Mental Health Awareness reference illustration.
    All coordinates relative to (cx, cy) = centre of torso.
    """
    def sc(v):
        return int(v * scale)

    # ── HAIR (draw first so it's behind the head) ──────────────────────
    # Long dark hair: main mass behind head + side strands
    hair_hw = sc(52)   # half-width
    head_top_y = cy - sc(118)
    # Back of hair (wider ellipse behind head)
    draw.ellipse(
        [cx - hair_hw - sc(8), head_top_y - sc(10),
         cx + hair_hw + sc(8), cy + sc(60)],
        fill=hair,
    )

    # ── HEAD ──────────────────────────────────────────────────────────
    head_r_x = sc(40)
    head_r_y = sc(46)
    head_top = head_top_y
    head_bot = head_top + head_r_y * 2
    draw.ellipse(
        [cx - head_r_x, head_top, cx + head_r_x, head_bot],
        fill=skin,
    )

    # ── NECK ──────────────────────────────────────────────────────────
    neck_hw = sc(14)
    neck_top = head_bot - sc(8)
    neck_bot = cy - sc(18)
    draw.rectangle([cx - neck_hw, neck_top, cx + neck_hw, neck_bot], fill=skin)

    # ── TORSO / SHIRT (trapezoid) ──────────────────────────────────────
    torso_top = neck_bot
    torso_bot = cy + sc(100)
    hw_top = sc(58)
    hw_bot = sc(72)
    draw.polygon(
        [
            (cx - hw_top, torso_top),
            (cx + hw_top, torso_top),
            (cx + hw_bot, torso_bot),
            (cx - hw_bot, torso_bot),
        ],
        fill=shirt,
    )

    # ── LEFT ARM — raised to touch forehead ───────────────────────────
    # Upper arm: from left shoulder diagonally up-right
    shoulder_lx = cx - hw_top
    shoulder_ly = torso_top + sc(14)

    elbow_x = cx - sc(50)
    elbow_y = cy - sc(60)

    # Upper arm (thick line as a polygon strip)
    arm_w = sc(18)
    dx, dy = elbow_x - shoulder_lx, elbow_y - shoulder_ly
    length = max(1, math.sqrt(dx * dx + dy * dy))
    px, py = -dy / length * arm_w / 2, dx / length * arm_w / 2
    draw.polygon(
        [
            (shoulder_lx + px, shoulder_ly + py),
            (shoulder_lx - px, shoulder_ly - py),
            (elbow_x - px, elbow_y - py),
            (elbow_x + px, elbow_y + py),
        ],
        fill=shirt,
    )

    # Forearm: elbow up to forehead position
    forehead_x = cx + sc(5)
    forehead_y = head_top + sc(28)
    fa_w = sc(14)
    dx2, dy2 = forehead_x - elbow_x, forehead_y - elbow_y
    l2 = max(1, math.sqrt(dx2 * dx2 + dy2 * dy2))
    px2, py2 = -dy2 / l2 * fa_w / 2, dx2 / l2 * fa_w / 2
    draw.polygon(
        [
            (elbow_x + px2, elbow_y + py2),
            (elbow_x - px2, elbow_y - py2),
            (forehead_x - px2, forehead_y - py2),
            (forehead_x + px2, forehead_y + py2),
        ],
        fill=skin,
    )

    # Hand (small rounded oval at forehead)
    draw.ellipse(
        [forehead_x - sc(14), forehead_y - sc(10),
         forehead_x + sc(14), forehead_y + sc(12)],
        fill=skin,
    )

    # ── RIGHT ARM — hanging down at side ──────────────────────────────
    shoulder_rx = cx + hw_top
    shoulder_ry = torso_top + sc(14)
    r_elbow_x = cx + sc(68)
    r_elbow_y = cy + sc(40)
    r_hand_x = cx + sc(72)
    r_hand_y = cy + sc(90)
    arm_w2 = sc(17)

    # Upper right arm
    dx3, dy3 = r_elbow_x - shoulder_rx, r_elbow_y - shoulder_ry
    l3 = max(1, math.sqrt(dx3 * dx3 + dy3 * dy3))
    px3, py3 = -dy3 / l3 * arm_w2 / 2, dx3 / l3 * arm_w2 / 2
    draw.polygon(
        [
            (shoulder_rx + px3, shoulder_ry + py3),
            (shoulder_rx - px3, shoulder_ry - py3),
            (r_elbow_x - px3, r_elbow_y - py3),
            (r_elbow_x + px3, r_elbow_y + py3),
        ],
        fill=shirt,
    )
    # Lower right arm / hand stub
    draw.ellipse(
        [r_hand_x - sc(12), r_hand_y - sc(12),
         r_hand_x + sc(12), r_hand_y + sc(12)],
        fill=skin,
    )

    # ── FACE FEATURES ─────────────────────────────────────────────────
    face_cx = cx
    face_top = head_top

    # Eyes: closed drooping curves
    eye_y = face_top + sc(50)
    eye_hw = sc(13)
    for ex in [face_cx - sc(14), face_cx + sc(14)]:
        draw.arc(
            [ex - eye_hw, eye_y - sc(5), ex + eye_hw, eye_y + sc(7)],
            start=0, end=180, fill=hair, width=max(2, sc(3)),
        )

    # Eyebrows — furrowed inward (sad)
    brow_y = eye_y - sc(14)
    for ex, inner_dy in [(face_cx - sc(14), sc(4)), (face_cx + sc(14), sc(4))]:
        draw.line(
            [(ex - sc(12), brow_y + inner_dy), (ex + sc(12), brow_y - inner_dy)],
            fill=hair, width=max(2, sc(3)),
        )
    # Fix: left brow goes up-left, right brow up-right for sad look
    draw.line(
        [(face_cx - sc(26), brow_y + sc(2)), (face_cx - sc(2), brow_y - sc(4))],
        fill=hair, width=max(2, sc(3)),
    )
    draw.line(
        [(face_cx + sc(2), brow_y - sc(4)), (face_cx + sc(26), brow_y + sc(2))],
        fill=hair, width=max(2, sc(3)),
    )

    # Mouth — downward arc (sad)
    mouth_y = face_top + sc(76)
    draw.arc(
        [face_cx - sc(13), mouth_y - sc(4), face_cx + sc(13), mouth_y + sc(10)],
        start=200, end=340, fill=hair, width=max(2, sc(3)),
    )


# ---------------------------------------------------------------------------
# Theme poster builders
# ---------------------------------------------------------------------------

POSTER_THEMES = {
    "mental_health": {
        "title_line1": "MENTAL HEALTH",
        "title_line2": "AWARENESS",
        "bg_color": (22, 115, 128),         # Teal
        "footer_bg": (11, 33, 50),          # Deep navy
        "header_color": (248, 240, 220),    # Warm cream
        "bullet_color": (136, 192, 87),     # Lime green
        "accent1": (11, 33, 50),            # Dark heart color
        "accent2": (100, 160, 70),          # Green ribbon
        "bullets": ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"],
        "skin": (210, 140, 100),
        "shirt": (185, 85, 50),             # Rust/orange shirt
        "hair": (25, 35, 60),              # Dark navy hair
    },
    "diabetes": {
        "title_line1": "DIABETES",
        "title_line2": "AWARENESS",
        "bg_color": (30, 100, 170),
        "footer_bg": (10, 30, 60),
        "header_color": (255, 245, 220),
        "bullet_color": (90, 200, 250),
        "accent1": (200, 50, 50),
        "accent2": (90, 200, 250),
        "bullets": ["EAT SMART", "STAY ACTIVE", "CHECK REGULARLY"],
        "skin": (215, 155, 100),
        "shirt": (50, 100, 200),
        "hair": (60, 35, 20),
    },
    "heart_health": {
        "title_line1": "HEART HEALTH",
        "title_line2": "AWARENESS",
        "bg_color": (170, 30, 60),
        "footer_bg": (60, 10, 20),
        "header_color": (255, 240, 240),
        "bullet_color": (255, 160, 160),
        "accent1": (220, 60, 80),
        "accent2": (255, 180, 60),
        "bullets": ["EAT HEART-HEALTHY", "EXERCISE DAILY", "KNOW YOUR NUMBERS"],
        "skin": (220, 165, 115),
        "shirt": (180, 40, 70),
        "hair": (50, 30, 15),
    },
    "nutrition": {
        "title_line1": "HEALTHY",
        "title_line2": "NUTRITION",
        "bg_color": (45, 150, 90),
        "footer_bg": (15, 55, 30),
        "header_color": (240, 255, 230),
        "bullet_color": (160, 230, 100),
        "accent1": (200, 230, 60),
        "accent2": (255, 160, 40),
        "bullets": ["EAT MORE VEGGIES", "DRINK WATER", "LIMIT SUGAR"],
        "skin": (210, 155, 95),
        "shirt": (50, 170, 100),
        "hair": (40, 25, 15),
    },
}


def draw_mental_health_poster(
    width: int = 600,
    title_line1: str = "MENTAL HEALTH",
    title_line2: str = "AWARENESS",
    bullets: Optional[List[str]] = None,
    bg_color: Tuple = (22, 115, 128),
    footer_bg: Tuple = (11, 33, 50),
    header_color: Tuple = (248, 240, 220),
    bullet_color: Tuple = (136, 192, 87),
    accent1: Tuple = (11, 33, 50),
    accent2: Tuple = (100, 160, 70),
    skin: Tuple = (210, 140, 100),
    shirt: Tuple = (185, 85, 50),
    hair: Tuple = (25, 35, 60),
) -> Image.Image:
    """
    Draw a complete 3-section health awareness poster 100% with Pillow.

    Layout mirrors the reference image:
      ┌─────────────────────┐
      │   MENTAL HEALTH     │  ← Bold title (teal bg)
      │   AWARENESS         │
      ├─────────────────────┤
      │   [illustration]    │  ← Flat vector character + icons
      │  ♥  [person]  🎗️   │
      ├─────────────────────┤
      │  • UNDERSTAND       │  ← Dark navy footer bullets
      │  • TALK ABOUT IT    │
      │  • SEEK HELP        │
      └─────────────────────┘
    """
    if bullets is None:
        bullets = ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"]

    # Canvas proportions (2:3 portrait)
    h = int(width * 1.52)

    # Section heights
    top_h = int(h * 0.26)       # Title header
    mid_h = int(h * 0.52)       # Illustration
    bot_h = h - top_h - mid_h  # Footer bullets

    img = Image.new("RGB", (width, h), color=bg_color)
    draw = ImageDraw.Draw(img)

    # ── SECTION 1: Title header ───────────────────────────────────────────
    # Background already filled as bg_color
    # Font sizes scale with poster width
    title_size = max(28, int(width * 0.098))
    font_title = _load_font(title_size, bold=True)

    line1_text = title_line1.upper()
    line2_text = title_line2.upper()

    cx = width // 2
    total_title_h = title_size * 2 + int(title_size * 0.25)
    start_y = (top_h - total_title_h) // 2

    # Drop shadow then white/cream text
    _centered_text(draw, line1_text, font_title, cx, start_y, fill=header_color,
                   shadow_fill=(0, 0, 0, 80))
    _centered_text(draw, line2_text, font_title, cx, start_y + title_size + int(title_size * 0.25),
                   fill=header_color, shadow_fill=(0, 0, 0, 80))

    # ── SECTION 2: Illustration ──────────────────────────────────────────
    # Background strip (same teal, slightly lighter)
    mid_y = top_h
    mid_bottom = top_h + mid_h

    # Slightly lighten mid section
    mid_bg = tuple(min(255, c + 15) for c in bg_color)
    draw.rectangle([0, mid_y, width, mid_bottom], fill=mid_bg)

    # Character: torso centre sits at 65% down the mid section
    # scale tuned so figure spans ~75% of mid_h
    fig_scale = mid_h * 0.0038
    fig_cx = width // 2
    fig_cy = mid_y + int(mid_h * 0.72)   # torso centre pushed lower for more room above

    _draw_person_mental_health(
        draw, fig_cx, fig_cy, scale=fig_scale,
        skin=skin, shirt=shirt, hair=hair, bg=mid_bg
    )

    # Brain tangle cloud: sits on top of / touching head (like reference)
    head_top_approx = fig_cy - int(fig_scale * 118)
    brain_r = int(width * 0.148)        # large enough to show tangle clearly
    brain_cx = fig_cx
    brain_cy = head_top_approx - int(brain_r * 0.50)
    _draw_tangled_brain_cloud(
        draw, brain_cx, brain_cy, brain_r,
        cloud_fill=(238, 236, 222),
        tangle_color=(22, 30, 55),
    )

    # Heart icon (left side)
    heart_cx = int(width * 0.18)
    heart_cy = fig_cy - int(mid_h * 0.18)
    heart_size = int(width * 0.11)
    _draw_heart(draw, heart_cx, heart_cy, heart_size, fill=accent1)

    # Ribbon icon (right side)
    ribbon_cx = int(width * 0.82)
    ribbon_cy = fig_cy - int(mid_h * 0.18)
    ribbon_size = int(width * 0.10)
    _draw_ribbon(draw, ribbon_cx, ribbon_cy, ribbon_size, fill=accent2)

    # ── SECTION 3: Footer bullets ─────────────────────────────────────────
    draw.rectangle([0, mid_bottom, width, h], fill=footer_bg)

    bullet_size = max(16, int(width * 0.057))
    font_bullet = _load_font(bullet_size, bold=True)
    dot_r = max(5, bullet_size // 5)

    n = len(bullets)
    total_text_h = n * bullet_size + (n - 1) * int(bullet_size * 0.55)
    start_bullet_y = mid_bottom + (bot_h - total_text_h) // 2
    margin_x = int(width * 0.14)
    line_gap = bullet_size + int(bullet_size * 0.55)

    for i, item in enumerate(bullets):
        bx = margin_x + dot_r
        by_text = start_bullet_y + i * line_gap
        by_dot = by_text + bullet_size // 2

        # Bullet dot
        draw.ellipse(
            [bx - dot_r, by_dot - dot_r, bx + dot_r, by_dot + dot_r],
            fill=bullet_color
        )

        # Bullet text
        tx = bx + dot_r + int(width * 0.03)
        draw.text((tx, by_text), item.strip().upper(), font=font_bullet, fill=header_color)

    return img


def draw_poster_from_theme(theme: str = "mental_health", width: int = 600) -> Image.Image:
    """
    Convenience wrapper. theme must be one of:
      'mental_health', 'diabetes', 'heart_health', 'nutrition'
    """
    t = POSTER_THEMES.get(theme, POSTER_THEMES["mental_health"])
    return draw_mental_health_poster(
        width=width,
        title_line1=t["title_line1"],
        title_line2=t["title_line2"],
        bullets=t["bullets"],
        bg_color=t["bg_color"],
        footer_bg=t["footer_bg"],
        header_color=t["header_color"],
        bullet_color=t["bullet_color"],
        accent1=t["accent1"],
        accent2=t["accent2"],
        skin=t["skin"],
        shirt=t["shirt"],
        hair=t["hair"],
    )


def draw_custom_poster(
    title_line1: str,
    title_line2: str,
    bullets: List[str],
    bg_color: Tuple = (22, 115, 128),
    footer_bg: Tuple = (11, 33, 50),
    header_color: Tuple = (248, 240, 220),
    bullet_color: Tuple = (136, 192, 87),
    accent1: Tuple = (11, 33, 50),
    accent2: Tuple = (100, 160, 70),
    skin: Tuple = (210, 140, 100),
    shirt: Tuple = (185, 85, 50),
    hair: Tuple = (25, 35, 60),
    width: int = 600,
) -> Image.Image:
    """Full custom poster with all parameters exposed (for Streamlit UI)."""
    return draw_mental_health_poster(
        width=width,
        title_line1=title_line1,
        title_line2=title_line2,
        bullets=bullets,
        bg_color=bg_color,
        footer_bg=footer_bg,
        header_color=header_color,
        bullet_color=bullet_color,
        accent1=accent1,
        accent2=accent2,
        skin=skin,
        shirt=shirt,
        hair=hair,
    )


# ---------------------------------------------------------------------------
# CLI quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    out_dir = "generated_images"
    os.makedirs(out_dir, exist_ok=True)

    for theme_key in POSTER_THEMES:
        poster = draw_poster_from_theme(theme_key, width=600)
        out_path = os.path.join(out_dir, f"{theme_key}_pillow_poster.png")
        poster.save(out_path, "PNG")
        print(f"[OK] Saved {out_path}  ({poster.size[0]}×{poster.size[1]}px)")

    print("\nAll posters generated. Open generated_images/ to review.")
