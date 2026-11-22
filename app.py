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
    page_icon="🌿",
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


# ---------------------------------------------------------------------------
# Sidebar Navigation & System Diagnostic
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌿 **WellAware AI**")
    st.caption("Patient Wellness Visual AI Studio")
    st.markdown('<span class="status-pill">● System Online</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    nav_choice = st.radio(
        "Navigation",
        [
            "🎨 Campaign Studio",
            "🖼️ Session Gallery",
            "⚡ Quick Presets",
            "ℹ️ Architecture & Standards"
        ],
        index=0
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
# VIEW 1: 🎨 CAMPAIGN STUDIO (MAIN WORKFLOW)
# ===========================================================================
if nav_choice == "🎨 Campaign Studio":
    # Form Layout
    col_input, col_style = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.markdown("#### 1️⃣ Campaign Identity & Topic")
        
        # Check if pre-populated from Quick Presets
        preset_data = st.session_state.get("selected_preset")
        default_title = preset_data.get("title", "") if preset_data else ""
        default_theme = preset_data.get("theme", "Heart Health") if preset_data else "Heart Health"
        default_desc = preset_data.get("desc", "") if preset_data else ""
        default_style = preset_data.get("style", "3D Illustration") if preset_data else "3D Illustration"

        theme_list = get_available_themes()
        theme_index = theme_list.index(default_theme) if default_theme in theme_list else 0

        campaign_title = st.text_input(
            "Campaign Title / Slogan",
            value=default_title,
            placeholder="e.g., Healthy Hearts 2026, Mindful Steps, Diabetes Care",
            help="Adds thematic framing to the generated visual."
        )

        health_theme = st.selectbox(
            "Health Awareness Theme",
            options=theme_list,
            index=theme_index,
            help="Selects domain visual motifs, color harmonies, and patient-friendly symbols."
        )

        theme_info = THEME_PRESETS[health_theme]
        placeholder_desc = theme_info["default_desc"]

        user_description = st.text_area(
            "Visual Description (What should be pictured?)",
            value=default_desc,
            placeholder=f"e.g., {placeholder_desc}",
            height=90,
            help="Describe the scene or leave blank to automatically use curated domain knowledge."
        )

    with col_style:
        st.markdown("#### 2️⃣ Artistic Direction & Format")

        style_list = get_available_styles()
        style_index = style_list.index(default_style) if default_style in style_list else 0

        style = st.selectbox(
            "Visual Style",
            options=style_list,
            index=style_index,
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

    with st.expander(f"🔍 Prompt Inspector & Optimizer ({est_tokens} / 77 tokens • {token_status})", expanded=False):
        st.caption("Stable Diffusion CLIP text encoder processes up to 77 tokens. Keeping prompts focused and front-loaded ensures 100% of keywords are rendered.")
        final_prompt = st.text_area("Positive Prompt (Front-Loaded)", value=auto_prompt, height=85)
        final_negative = st.text_area("Domain Negative Prompt", value=auto_negative, height=65)

    # -----------------------------------------------------------------------
    # GENERATION TRIGGER & REAL-TIME FEEDBACK
    # -----------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate Campaign Visual(s)", type="primary", width="stretch")

    if generate_btn:
        progress_bar = st.progress(0, text="Initializing model pipeline...")
        status_box = st.empty()
        start_time_all = time.time()

        seed_val = int(custom_seed) if use_fixed_seed else None

        try:
            status_box.info("🌿 Loading Stable Diffusion pipeline...")
            engine = load_cached_generator()

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

        results = st.session_state["current_results"]
        cols = st.columns(len(results), gap="medium")

        for idx, res in enumerate(results):
            with cols[idx]:
                st.image(res["image"], width="stretch")

                # Sleek Metadata Badges
                st.markdown(f"""
                <div>
                    <span class="metric-badge">🎲 Seed: {res['seed']}</span>
                    <span class="metric-badge">⏱️ {res['generation_time']}s</span>
                    <span class="metric-badge">📐 {res['width']}×{res['height']}</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                img_bytes = image_to_bytes(res["image"])
                st.download_button(
                    label=f"⬇️ Download High-Res PNG",
                    data=img_bytes,
                    file_name=res["filename"],
                    mime="image/png",
                    key=f"dl_btn_{idx}_{res['seed']}",
                    width="stretch"
                )


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
            if st.button(f"Load '{p['title']}' into Studio", key=f"load_p_{i}", width="stretch"):
                st.session_state["selected_preset"] = p
                st.toast(f"✅ Loaded '{p['title']}'! Switching to Studio...", icon="🚀")
                st.rerun()


# ===========================================================================
# VIEW 4: ℹ️ ARCHITECTURE & STANDARDS
# ===========================================================================
elif nav_choice == "ℹ️ Architecture & Standards":
    st.markdown("### ℹ️ Architecture & Engineering Standards")
    
    st.markdown("""
    **WellAware AI** implements an enterprise Generative AI pipeline tailored for non-clinical health communication:
    
    1. **Front-Loaded CLIP Encoding:**
       - Traditional diffusion prompts often exceed CLIP's strict 77-token ceiling, discarding essential stylistic tokens.
       - WellAware AI prioritizes primary subject and aesthetic style tokens at positions $0-30$, ensuring 100% attention retention.
    
    2. **DPM-Solver++ (Karras) Sampling:**
       - Utilizes second-order differential equation solvers with Karras noise variance schedules.
       - Delivers photorealistic and clean vector convergence in **20 steps** (70% faster than legacy 50-step PNDM schedulers).
    
    3. **Domain Negative Prompting:**
       - Healthcare visuals require strict removal of clinical distress, morbid depictions, anatomical distortions, and garbled text.
       - Every generation automatically injects medical safety and style-specific negative embeddings.
    """)

    st.markdown("---")
    st.markdown("#### 🏗️ Modular Architecture Layout")
    st.code("""
WellAware-AI/
│
├── app.py                 # Multi-Page Studio UI & Session State Coordinator
├── prompt_generator.py    # Front-Loaded 77-Token CLIP Synthesizer
├── image_generator.py     # Singleton Diffusers Engine with DPM-Solver++ Karras
├── config.py              # Central Inference Settings & Hardware Offload
├── generated_images/      # Persisted Campaign PNG Repository
└── assets/                # Visual Branding & Design Artifacts
    """, language="text")
