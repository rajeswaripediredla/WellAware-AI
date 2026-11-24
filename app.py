"""
WellAware AI - Patient Wellness Campaign Visual Generator
Professional Healthcare Visual AI Studio (app.py)
"""

import os
import io
import time
from datetime import datetime
from PIL import Image
import streamlit as st

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

# ---------------------------------------------------------------------------
# Streamlit Page Configuration & Design System
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="WellAware AI - Campaign Visual Studio",
    page_icon="assets/heart_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Executive Healthcare Styling
st.markdown("""
<style>
    /* Modern Brand Typography & Colors */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2px;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0E7490;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-tagline {
        font-size: 1.05rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 2px;
        margin-bottom: 18px;
    }
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #E0F2FE;
        color: #0369A1;
        border: 1px solid #BAE6FD;
    }
    .alert-banner {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #BBF7D0;
        border-left: 4px solid #16A34A;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 22px;
        font-size: 0.88rem;
        color: #166534;
    }
    .card-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    .preset-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .metric-badge {
        background-color: #F1F5F9;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
        display: inline-block;
        margin-right: 6px;
    }
    .token-badge-good {
        color: #15803D;
        font-weight: 700;
    }
    .token-badge-warn {
        color: #B45309;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Cached Model Pipeline Loader
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_cached_generator():
    """Caches the singleton diffusion engine to prevent reloading weights."""
    gen = CampaignImageGenerator.get_instance()
    gen.load_pipeline()
    return gen


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
if "current_results" not in st.session_state:
    st.session_state["current_results"] = []

if "selected_preset" not in st.session_state:
    st.session_state["selected_preset"] = None


if "nav_radio" not in st.session_state:
    st.session_state["nav_radio"] = "🏠 Home"


def navigate_to(page_name, preset_data=None):
    """Callback to safely switch navigation before widgets instantiate."""
    st.session_state["nav_radio"] = page_name
    if preset_data is not None:
        st.session_state["selected_preset"] = preset_data


# ---------------------------------------------------------------------------
# Sidebar Navigation & System Diagnostic
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2px;">
        <span style="display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; background: #FFE4E6; border-radius: 8px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#E11D48" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
        </span>
        <span style="font-size: 1.35rem; font-weight: 800; color: #0E7490; letter-spacing: -0.3px;">WellAware AI</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Patient Wellness Visual AI Studio")
    st.markdown('<span class="status-pill">● System Online</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    nav_choice = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🎨 Campaign Studio",
            "🖼️ Session Gallery",
            "⚡ Quick Presets"
        ],
        key="nav_radio"
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Engine Telemetry")
    device_label = "NVIDIA CUDA GPU" if config.DEVICE == "cuda" else "Multi-Core CPU (DPM-Solver++ Karras)"
    st.caption(f"**Hardware:** {device_label}")
    st.caption(f"**Model:** `{os.path.basename(config.MODEL_ID)}`")
    st.caption(f"**Sampler:** `DPM-Solver++ (Karras)`")
    st.markdown("---")
    st.caption("WellAware AI © 2026 • Non-clinical educational communications.")


# ---------------------------------------------------------------------------
# Helper Utility Functions
# ---------------------------------------------------------------------------
def image_to_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def get_all_saved_visuals():
    records = []
    if os.path.exists(config.OUTPUT_DIR):
        for fname in sorted(os.listdir(config.OUTPUT_DIR), reverse=True):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")) and not fname.startswith("."):
                fpath = os.path.join(config.OUTPUT_DIR, fname)
                try:
                    stat = os.stat(fpath)
                    records.append({
                        "filename": fname,
                        "path": fpath,
                        "time": datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %H:%M"),
                        "size_kb": round(stat.st_size / 1024, 1)
                    })
                except Exception:
                    continue
    return records


# ===========================================================================
# TOP BANNER: BRANDING & CLINICAL NOTICE
# ===========================================================================
st.markdown("""
<div class="brand-header">
    <span style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; background: linear-gradient(135deg, #FFE4E6 0%, #FECDD3 100%); border-radius: 12px; margin-right: 12px; box-shadow: 0 2px 6px rgba(225, 29, 72, 0.15);">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="#E11D48" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
    </span>
    <h1 class="brand-title">WellAware AI</h1>
</div>
<div class="brand-tagline">Generative Visual AI Studio for Patient Wellness & Public Health Campaigns</div>
<div class="alert-banner">
    <strong>🛡️ Non-Clinical Healthcare Notice:</strong> WellAware AI is purpose-built for patient wellness advocacy,
    healthy lifestyle education, and non-profit healthcare campaigns. It is not designed for diagnostic, clinical,
    or individualized medical advice.
</div>
""", unsafe_allow_html=True)


# ===========================================================================
# VIEW 0: 🏠 HOME PAGE (WELCOME & OVERVIEW)
# ===========================================================================
if nav_choice == "🏠 Home":
    # Hero Welcome Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0E7490 0%, #0369A1 100%); padding: 36px 32px; border-radius: 16px; color: white; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(14, 116, 144, 0.15);">
        <h1 style="color: white; margin: 0 0 8px 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px;">
            ❤️ Welcome to WellAware AI
        </h1>
        <p style="color: #E0F2FE; font-size: 1.15rem; margin: 0 0 16px 0; font-weight: 500; line-height: 1.5;">
            Generative Visual AI Studio for Patient Wellness, Public Health Campaigns & Publication-Grade Posters.
        </p>
        <p style="color: #BAE6FD; font-size: 0.95rem; margin: 0; line-height: 1.6; max-width: 800px;">
            Transform brief healthcare concepts into high-contrast, culturally sensitive campaign visuals,
            complete with professional TrueType headlines, action takeaways, and 24/7 helpline footers in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Navigation CTA Row
    c_cta1, c_cta2, c_cta3 = st.columns(3, gap="medium")
    with c_cta1:
        st.button(
            "🚀 Open Campaign Studio",
            type="primary",
            use_container_width=True,
            key="home_btn_studio",
            on_click=navigate_to,
            args=("🎨 Campaign Studio",)
        )
    with c_cta2:
        st.button(
            "⚡ Explore Quick Presets",
            use_container_width=True,
            key="home_btn_presets",
            on_click=navigate_to,
            args=("⚡ Quick Presets",)
        )
    with c_cta3:
        st.button(
            "🖼️ View Campaign Gallery",
            use_container_width=True,
            key="home_btn_gallery",
            on_click=navigate_to,
            args=("🖼️ Session Gallery",)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3 Core Value Pillars
    st.markdown("### ✨ Key Capabilities")
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="card-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🎨</div>
            <h4 style="color: #0E7490; margin-bottom: 8px;">Domain-Specific Visual AI</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Covers <strong>10 curated health domains</strong> (Mental Wellness, Heart Health, Diabetes, Cancer Care, Hygiene, Nutrition)
                across <strong>6 artistic styles</strong> with prompt synthesis bounded within CLIP's 77-token ceiling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">📰</div>
            <h4 style="color: #0E7490; margin-bottom: 8px;">Commercial Poster Engine</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Composites authentic <strong>640×960 (2:3 aspect ratio)</strong> campaign posters featuring
                bold condensed display headlines, category badges, 3 bulleted action points, and crisis helpline footers.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card-panel" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">✍️</div>
            <h4 style="color: #0E7490; margin-bottom: 8px;">100% Typographic Accuracy</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Eliminates diffusion text hallucinations and spelling mistakes. Pure artwork is generated in latent space while
                text is rendered via high-contrast TrueType typography with zero dead margins.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How It Works Workflow
    st.markdown("### 🔄 How It Works (3 Simple Steps)")
    hw1, hw2, hw3 = st.columns(3, gap="medium")

    with hw1:
        st.markdown("""
        <div class="card-panel" style="border-left: 4px solid #0E7490;">
            <div style="font-weight: 700; color: #0E7490; font-size: 0.95rem; margin-bottom: 4px;">STEP 1</div>
            <h4 style="margin: 0 0 6px 0;">Select Theme & Style</h4>
            <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
                Choose from 10 health awareness domains or enter your own campaign concept, paired with one of 6 artistic styles.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with hw2:
        st.markdown("""
        <div class="card-panel" style="border-left: 4px solid #0284C7;">
            <div style="font-weight: 700; color: #0284C7; font-size: 0.95rem; margin-bottom: 4px;">STEP 2</div>
            <h4 style="margin: 0 0 6px 0;">Configure Typography</h4>
            <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
                Customize the headline lines, advocacy badge, and 3 key action takeaways directly before generating.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with hw3:
        st.markdown("""
        <div class="card-panel" style="border-left: 4px solid #16A34A;">
            <div style="font-weight: 700; color: #16A34A; font-size: 0.95rem; margin-bottom: 4px;">STEP 3</div>
            <h4 style="margin: 0 0 6px 0;">Generate & Download</h4>
            <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
                Receive both a finished publication-ready poster and standalone high-resolution artwork ready for one-click PNG export.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Jump Card
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 12px;">
        <h3 style="color: #0F172A; margin: 0 0 8px 0;">Ready to Create Your Campaign?</h3>
        <p style="color: #64748B; font-size: 0.95rem; margin: 0 0 16px 0;">
            Launch the Campaign Studio to start generating custom patient education posters in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c_btn_l, c_btn_mid, c_btn_r = st.columns([1, 1.5, 1])
    with c_btn_mid:
        st.button(
            "🚀 Launch Campaign Studio Now",
            type="primary",
            use_container_width=True,
            key="home_btn_bottom",
            on_click=navigate_to,
            args=("🎨 Campaign Studio",)
        )


# ===========================================================================
# VIEW 1: 🎨 CAMPAIGN STUDIO (MAIN WORKFLOW)
# ===========================================================================
elif nav_choice == "🎨 Campaign Studio":
    # Form Layout
    col_input, col_style = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.markdown("#### 1️⃣ Campaign Identity & Topic")
        
        # Check if pre-populated from Quick Presets
        if "selected_preset" in st.session_state and st.session_state["selected_preset"] is not None:
            preset_data = st.session_state.pop("selected_preset")
            st.session_state["form_title"] = preset_data.get("title", "")
            st.session_state["form_theme"] = preset_data.get("theme", "Heart Health")
            st.session_state["form_desc"] = preset_data.get("desc", "")
            st.session_state["form_style"] = preset_data.get("style", "3D Illustration")

        theme_list = get_available_themes()
        curr_theme = st.session_state.get("form_theme", "Heart Health")
        theme_index = theme_list.index(curr_theme) if curr_theme in theme_list else 0

        campaign_title = st.text_input(
            "Campaign Title / Slogan",
            value=st.session_state.get("form_title", ""),
            key="form_title",
            placeholder="e.g., Healthy Hearts 2026, Mindful Steps, Diabetes Care",
            help="Adds thematic framing to the generated visual."
        )

        health_theme = st.selectbox(
            "Health Awareness Theme",
            options=theme_list,
            index=theme_index,
            key="form_theme",
            help="Selects domain visual motifs, color harmonies, and patient-friendly symbols."
        )

        theme_info = THEME_PRESETS[health_theme]
        placeholder_desc = theme_info["default_desc"]

        user_description = st.text_area(
            "Visual Description (What should be pictured?)",
            value=st.session_state.get("form_desc", ""),
            key="form_desc",
            placeholder=f"e.g., {placeholder_desc}",
            height=90,
            help="Describe the scene or leave blank to automatically use curated domain knowledge."
        )

    with col_style:
        st.markdown("#### 2️⃣ Artistic Direction & Format")

        style_list = get_available_styles()
        curr_style = st.session_state.get("form_style", "3D Illustration")
        style_index = style_list.index(curr_style) if curr_style in style_list else 0

        style = st.selectbox(
            "Visual Style",
            options=style_list,
            index=style_index,
            key="form_style",
            format_func=lambda s: f"{STYLE_DIRECTIVES[s]['badge']} - {s}"
        )

        aspect_ratio = st.selectbox(
            "Aspect Ratio & Composition",
            options=list(config.ASPECT_RATIOS.keys()),
            index=0
        )
        img_w, img_h = config.ASPECT_RATIOS[aspect_ratio]

        c_var, c_steps = st.columns(2)
        with c_var:
            num_variations = st.selectbox("Variations", options=[1, 2, 3, 4], index=0)
        with c_steps:
            default_steps = 20 if config.DEVICE == "cpu" else config.DEFAULT_NUM_INFERENCE_STEPS
            steps = st.slider("Inference Steps", min_value=12, max_value=30, value=default_steps, step=1)

        with st.expander("⚙️ Advanced Parameters"):
            guidance_scale = st.slider("Guidance Scale (Prompt Adherence)", min_value=5.0, max_value=12.0, value=7.5, step=0.5)
            use_fixed_seed = st.checkbox("Deterministic Seed (Reproducible)", value=False)
            custom_seed = st.number_input("Seed Value", value=42, step=1, disabled=not use_fixed_seed)
            apply_polish = st.checkbox("Apply Editorial Polish (Edge Sharpness & Vibrance)", value=True)
            
            lora_exists = os.path.exists(config.DEFAULT_LORA_PATH)
            if lora_exists:
                use_lora = st.checkbox("✨ Activate Custom Healthcare LoRA Weights", value=True)
            else:
                st.caption("💡 *Custom LoRA Adapter: Run `train_lora.py` to activate trained weights.*")
                use_lora = False

    # -----------------------------------------------------------------------
    # 3️⃣ POSTER TYPOGRAPHY & ACTION POINTS (CONFIGURED BEFORE GENERATION)
    # -----------------------------------------------------------------------
    from poster_designer import render_infographic_action_poster, get_theme_poster_preset

    theme_defaults = get_theme_poster_preset(health_theme)

    # Compute default headlines from campaign title or theme preset
    if campaign_title.strip():
        words = campaign_title.strip().upper().split()
        if len(words) > 2:
            mid_pt = (len(words) + 1) // 2
            def_t1 = " ".join(words[:mid_pt])
            def_t2 = " ".join(words[mid_pt:])
        elif len(words) == 2:
            def_t1, def_t2 = words[0], words[1]
        else:
            def_t1 = words[0]
            def_t2 = theme_defaults.get("title_line2", "")
    else:
        def_t1 = theme_defaults.get("title_line1", "HEALTH AWARENESS")
        def_t2 = theme_defaults.get("title_line2", "CAMPAIGN")

    def_badge = theme_defaults.get("badge", "PUBLIC HEALTH ADVOCACY")
    preset_bullets = theme_defaults.get("bullets", ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"])
    def_b1 = preset_bullets[0] if len(preset_bullets) > 0 else "UNDERSTAND"
    def_b2 = preset_bullets[1] if len(preset_bullets) > 1 else "TALK ABOUT IT"
    def_b3 = preset_bullets[2] if len(preset_bullets) > 2 else "SEEK HELP"
    def_footer = theme_defaults.get("footer", "National Wellness Initiative • Need Support? Call or Text 988")

    # Keep session state synced when theme or campaign title changes
    current_key_theme = f"{health_theme}_{campaign_title}"
    if st.session_state.get("last_typo_key") != current_key_theme:
        st.session_state["typo_title1"] = def_t1
        st.session_state["typo_title2"] = def_t2
        st.session_state["typo_badge"] = def_badge
        st.session_state["typo_bullet1"] = def_b1
        st.session_state["typo_bullet2"] = def_b2
        st.session_state["typo_bullet3"] = def_b3
        st.session_state["typo_footer"] = def_footer
        st.session_state["last_typo_key"] = current_key_theme

    st.markdown("---")
    st.markdown("#### 3️⃣ Poster Typography & Action Points (Configured Before Generating)")
    st.caption("Customize the bold headline, advocacy badge, action points, and helpline footer before generating. The AI generates clean artwork without misspelling gibberish and immediately composites your exact typography into a finished commercial poster.")

    col_typo_hdr, col_typo_act = st.columns(2, gap="large")
    with col_typo_hdr:
        st.markdown("**Top Header & Headline:**")
        typo_t1 = st.text_input("Poster Headline (Line 1)", key="typo_title1", help="Large condensed bold display headline.")
        typo_t2 = st.text_input("Poster Headline (Line 2)", key="typo_title2", help="Second headline line (optional).")
        typo_badge = st.text_input("Advocacy / Category Badge", key="typo_badge", help="Small top header badge.")

    with col_typo_act:
        st.markdown("**Bottom Action Points & Helpline Footer:**")
        typo_b1 = st.text_input("Action Bullet 1", key="typo_bullet1")
        typo_b2 = st.text_input("Action Bullet 2", key="typo_bullet2")
        typo_b3 = st.text_input("Action Bullet 3", key="typo_bullet3")
        typo_footer = st.text_input("Helpline / Organization Footer", key="typo_footer")

    # -----------------------------------------------------------------------
    # PROMPT OPTIMIZER & TOKEN GAUGE
    # -----------------------------------------------------------------------
    auto_prompt, auto_negative = build_prompt(
        campaign_title=campaign_title,
        health_theme=health_theme,
        user_description=user_description,
        style=style,
        aspect_ratio=aspect_ratio
    )

    est_tokens = estimate_token_count(auto_prompt)
    token_status = (
        '<span class="token-badge-good">🟢 Optimal (Full Attention)</span>'
        if est_tokens <= 75 else
        '<span class="token-badge-warn">🟡 Near Limit</span>'
    )

    # Sync prompt editor with current inputs unless user manually edited
    if st.session_state.get("last_auto_prompt") != auto_prompt:
        st.session_state["positive_prompt_area"] = auto_prompt
        st.session_state["negative_prompt_area"] = auto_negative
        st.session_state["last_auto_prompt"] = auto_prompt

    with st.expander(f"🔍 Prompt Inspector & Optimizer ({est_tokens} / 77 tokens • {token_status})", expanded=False):
        st.caption("Stable Diffusion CLIP text encoder processes up to 77 tokens. Keeping prompts focused and front-loaded ensures 100% of keywords are rendered.")
        final_prompt = st.text_area("Positive Prompt (Front-Loaded)", key="positive_prompt_area", height=85)
        final_negative = st.text_area("Domain Negative Prompt", key="negative_prompt_area", height=65)

    # -----------------------------------------------------------------------
    # GENERATION TRIGGER & REAL-TIME FEEDBACK
    # -----------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Campaign Visual & Poster", type="primary", width="stretch")

    if generate_btn:
        progress_bar = st.progress(0, text="Initializing model pipeline...")
        status_box = st.empty()
        start_time_all = time.time()

        seed_val = int(custom_seed) if use_fixed_seed else None

        try:
            status_box.info("🌿 Loading Stable Diffusion pipeline...")
            engine = load_cached_generator()

            if use_lora:
                engine.load_lora_weights(config.DEFAULT_LORA_PATH)
                if "wellaware style" not in final_prompt:
                    final_prompt = f"wellaware style, {final_prompt}"
            else:
                engine.unload_lora_weights()

            status_box.info(f"🎨 Running DPM-Solver++ (Karras) across {num_variations} variation(s)...")
            progress_bar.progress(20, text=f"Denoising latents ({steps} steps)...")

            raw_results = engine.generate_variations(
                prompt=final_prompt,
                negative_prompt=final_negative,
                num_variations=num_variations,
                base_seed=seed_val,
                width=img_w,
                height=img_h,
                num_inference_steps=steps,
                guidance_scale=guidance_scale
            )

            progress_bar.progress(85, text="Finishing & saving visuals...")

            saved_results = []
            chosen_t1 = typo_t1.strip() or def_t1
            chosen_t2 = typo_t2.strip()
            chosen_badge = typo_badge.strip()
            chosen_bullets = [b.strip() for b in [typo_b1, typo_b2, typo_b3] if b.strip()]
            if not chosen_bullets:
                chosen_bullets = preset_bullets
            chosen_footer = typo_footer.strip()
            bullet_color = theme_defaults.get("bullet_color", (136, 192, 87))
            footer_bg = theme_defaults.get("footer_bg", (11, 33, 45))

            for res in raw_results:
                final_img = res["image"]
                if apply_polish:
                    final_img = engine.postprocess_image(final_img, sharpness=1.15, contrast=1.05, color=1.05)
                    res["image"] = final_img

                filepath = engine.save_visual_to_disk(
                    image=final_img,
                    campaign_title=campaign_title or health_theme,
                    seed=res["seed"]
                )
                res["filepath"] = filepath
                res["filename"] = os.path.basename(filepath)
                res["theme"] = health_theme
                res["style"] = style

                # Automatically composite publication-grade campaign poster with pre-configured typography
                initial_poster = render_infographic_action_poster(
                    base_image=final_img,
                    title_line1=chosen_t1,
                    title_line2=chosen_t2,
                    badge_text=chosen_badge,
                    action_bullets=chosen_bullets,
                    bullet_color=bullet_color,
                    footer_bg=footer_bg,
                    footer_text=chosen_footer
                )

                poster_path = engine.save_visual_to_disk(
                    image=initial_poster,
                    campaign_title=f"{chosen_t1}_{chosen_t2}_poster",
                    seed=res["seed"]
                )

                res["poster"] = initial_poster
                res["poster_filepath"] = poster_path
                res["poster_filename"] = os.path.basename(poster_path)
                res["poster_title1"] = chosen_t1
                res["poster_title2"] = chosen_t2
                res["poster_bullets"] = chosen_bullets
                res["poster_footer"] = chosen_footer
                res["poster_badge"] = chosen_badge
                res["bullet_color"] = bullet_color
                res["footer_bg"] = footer_bg

                saved_results.append(res)

            total_elapsed = round(time.time() - start_time_all, 1)
            progress_bar.progress(100, text="Generation complete!")
            time.sleep(0.4)
            progress_bar.empty()
            status_box.success(f"🎉 Generated {len(saved_results)} visual(s) in {total_elapsed}s!")

            st.session_state["current_results"] = saved_results

        except Exception as e:
            progress_bar.empty()
            status_box.error(f"❌ Generation encountered an error: {str(e)}")

    # -----------------------------------------------------------------------
    # DISPLAY GENERATED RESULTS (STUDIO VIEW)
    # -----------------------------------------------------------------------
    if st.session_state["current_results"]:
        st.markdown("---")
        st.markdown("### 🖼️ Campaign Output Studio")
        st.caption("Each generation produces both a **Publication-Ready Campaign Poster** and a **Standalone Visual Asset**.")

        results = st.session_state["current_results"]
        cols = st.columns(len(results), gap="large")

        for idx, res in enumerate(results):
            with cols[idx]:
                has_poster = "poster" in res and res["poster"] is not None
                if has_poster:
                    tab_poster, tab_artwork = st.tabs(["📰 Finished Campaign Poster", "🎨 Standalone Visual"])
                    with tab_poster:
                        st.image(res["poster"], width="stretch", caption="Commercial Campaign Poster • 640×960")
                        poster_bytes = image_to_bytes(res["poster"])
                        st.download_button(
                            label="⬇️ Download Finished Poster (PNG)",
                            data=poster_bytes,
                            file_name=res.get("poster_filename", "campaign_poster.png"),
                            mime="image/png",
                            key=f"dl_poster_{idx}_{res['seed']}",
                            type="primary",
                            width="stretch"
                        )
                    with tab_artwork:
                        st.image(res["image"], width="stretch", caption=f"Hero Artwork • {res['width']}×{res['height']}")
                        img_bytes = image_to_bytes(res["image"])
                        st.download_button(
                            label="⬇️ Download Raw Artwork (PNG)",
                            data=img_bytes,
                            file_name=res["filename"],
                            mime="image/png",
                            key=f"dl_art_{idx}_{res['seed']}",
                            width="stretch"
                        )
                else:
                    st.image(res["image"], width="stretch")
                    img_bytes = image_to_bytes(res["image"])
                    st.download_button(
                        label="⬇️ Download Visual (PNG)",
                        data=img_bytes,
                        file_name=res["filename"],
                        mime="image/png",
                        key=f"dl_raw_{idx}_{res['seed']}",
                        width="stretch"
                    )

                # Sleek Metadata Badges
                st.markdown(f"""
                <div style="margin-top: 6px;">
                    <span class="metric-badge">🎲 Seed: {res['seed']}</span>
                    <span class="metric-badge">⏱️ {res['generation_time']}s</span>
                    <span class="metric-badge">🏷️ {res['theme']}</span>
                </div>
                """, unsafe_allow_html=True)

        # -------------------------------------------------------------------
        # INSTANT POSTER TYPOGRAPHY & LAYOUT CUSTOMIZER
        # -------------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("✏️ Customize Poster Headline, Action Points & Helplines (Instant Update)", expanded=False):
            st.caption("Change titles, action bullets, or helpline footer in real time without waiting for diffusion inference.")

            active_res = results[0]
            c_top, c_bot = st.columns(2, gap="medium")

            with c_top:
                st.markdown("**Top Header & Badge:**")
                edit_t1 = st.text_input("Title Line 1", value=active_res.get("poster_title1", "MENTAL HEALTH"), key="cust_t1")
                edit_t2 = st.text_input("Title Line 2", value=active_res.get("poster_title2", "AWARENESS"), key="cust_t2")
                edit_badge = st.text_input("Advocacy Badge", value=active_res.get("poster_badge", "PUBLIC HEALTH ADVOCACY"), key="cust_badge")

            with c_bot:
                st.markdown("**Bottom Action Points & Footer:**")
                curr_bullets = active_res.get("poster_bullets", ["UNDERSTAND", "TALK ABOUT IT", "SEEK HELP"])
                edit_bullets_text = st.text_area(
                    "Action Points (one per line, max 3)",
                    value="\n".join(curr_bullets),
                    height=80,
                    key="cust_bullets"
                )
                edit_footer = st.text_input(
                    "Footer Helpline / Organization",
                    value=active_res.get("poster_footer", "National Wellness Initiative • Need Support? Call or Text 988"),
                    key="cust_footer"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⚡ Update Poster (Instant)", type="primary", width="stretch", key="update_poster_instant_btn"):
                from poster_designer import render_infographic_action_poster
                cleaned_bullets = [b.strip() for b in edit_bullets_text.split("\n") if b.strip()][:3]
                engine = load_cached_generator()

                for r in results:
                    updated_poster = render_infographic_action_poster(
                        base_image=r["image"],
                        title_line1=edit_t1,
                        title_line2=edit_t2,
                        badge_text=edit_badge,
                        action_bullets=cleaned_bullets,
                        footer_text=edit_footer,
                        bullet_color=r.get("bullet_color", (136, 192, 87)),
                        footer_bg=r.get("footer_bg", (11, 33, 45))
                    )
                    r["poster"] = updated_poster
                    r["poster_title1"] = edit_t1
                    r["poster_title2"] = edit_t2
                    r["poster_bullets"] = cleaned_bullets
                    r["poster_badge"] = edit_badge
                    r["poster_footer"] = edit_footer

                    # Save updated poster
                    p_path = engine.save_visual_to_disk(
                        image=updated_poster,
                        campaign_title=f"{edit_t1}_{edit_t2}_poster",
                        seed=r["seed"]
                    )
                    r["poster_filepath"] = p_path
                    r["poster_filename"] = os.path.basename(p_path)

                st.session_state["current_results"] = results
                st.toast("✅ Poster updated with custom typography!", icon="🎨")
                st.rerun()


# ===========================================================================
# VIEW 2: 🖼️ SESSION GALLERY
# ===========================================================================
elif nav_choice == "🖼️ Session Gallery":
    st.markdown("### 🖼️ Campaign Visuals Gallery")
    st.caption("Review, preview, and download all generated wellness campaign visuals.")

    items = get_all_saved_visuals()

    col_btn, col_stats = st.columns([1, 4])
    with col_btn:
        if st.button("🔄 Refresh Gallery", width="stretch"):
            st.rerun()
    with col_stats:
        st.write(f"Total Visuals in Archive: **{len(items)}**")

    if not items:
        st.info("No campaign visuals found in storage yet. Create one in the **🎨 Campaign Studio**!")
    else:
        grid_cols = st.columns(3, gap="medium")
        for i, item in enumerate(items):
            target_col = grid_cols[i % 3]
            with target_col:
                try:
                    img = Image.open(item["path"])
                    st.image(img, width="stretch")
                    st.markdown(f"**{item['filename']}**")
                    st.caption(f"📅 {item['time']} • 💾 {item['size_kb']} KB")
                    
                    st.download_button(
                        label="⬇️ Download Visual",
                        data=image_to_bytes(img),
                        file_name=item["filename"],
                        mime="image/png",
                        key=f"hist_dl_{i}",
                        width="stretch"
                    )
                    st.markdown("---")
                except Exception as e:
                    st.warning(f"Failed to load {item['filename']}: {e}")


# ===========================================================================
# VIEW 3: ⚡ QUICK PRESETS
# ===========================================================================
elif nav_choice == "⚡ Quick Presets":
    st.markdown("### ⚡ Curated Campaign Presets")
    st.caption("Click any pre-engineered campaign to immediately load optimal prompts, aesthetics, and configurations into the Studio.")

    presets = [
        {
            "title": "Mental Health Awareness",
            "theme": "Mental Wellness",
            "style": "Flat Design",
            "desc": "calm peaceful woman touching her forehead with hand in contemplation, centered figure, solid plain teal background, minimal clean vector shapes",
            "badge": "🧠 Mental Health • Flat Art"
        },
        {
            "title": "Heart Health Vitality 2026",
            "theme": "Heart Health",
            "style": "3D Illustration",
            "desc": "stylized glowing healthy heart surrounded by fresh organic apples and stethoscope",
            "badge": "🫀 Cardiovascular • 3D Clay"
        },
        {
            "title": "Mindful Morning Zen",
            "theme": "Mental Wellness",
            "style": "Minimalist",
            "desc": "peaceful mindfulness meditation silhouette with blooming lavender and soft sunrise",
            "badge": "🧠 Mental Health • Scandinavian Vector"
        },
        {
            "title": "Mediterranean Plate Nutrition",
            "theme": "Healthy Eating",
            "style": "Flat Design",
            "desc": "delicious colorful wellness meal bowl with fresh berries, avocado slices, and greens",
            "badge": "🥗 Nutrition • Flat Corporate"
        },
        {
            "title": "Pristine Hands Save Lives",
            "theme": "Hygiene Awareness",
            "style": "3D Illustration",
            "desc": "crisp clean hands washing with clear water droplets and rich foaming bubbles",
            "badge": "🧼 Infection Prevention • 3D Render"
        },
        {
            "title": "Active Living For Life",
            "theme": "Physical Fitness",
            "style": "Realistic",
            "desc": "joyful active senior walking briskly in a sunlit green park with trees",
            "badge": "🏃 Mobility • Photorealistic"
        },
        {
            "title": "Annual Preventative Checkup",
            "theme": "Preventive Healthcare",
            "style": "Professional Healthcare Illustration",
            "desc": "friendly preventive health checkup with medical clipboard and stethoscope",
            "badge": "🩺 Clinical Advocacy • Editorial"
        }
    ]

    cols = st.columns(2, gap="medium")
    for i, p in enumerate(presets):
        target = cols[i % 2]
        with target:
            st.markdown(f"""
            <div class="preset-card">
                <h4>{p['title']}</h4>
                <span class="status-pill">{p['badge']}</span>
                <p style="margin-top: 8px; font-size: 0.9rem; color: #475569;">
                    <em>"{p['desc']}"</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.button(
                f"Load '{p['title']}' into Studio",
                key=f"load_p_{i}",
                use_container_width=True,
                on_click=navigate_to,
                args=("🎨 Campaign Studio", p)
            )



