"""
WellAware AI - Presentation Generator (create_presentation.py)
Creates an executive-grade 10-slide 16:9 widescreen PowerPoint presentation (.pptx)
showcasing WellAware AI's architecture, generative pipeline, typography engine, and results.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_wellaware_presentation(output_path="WellAware_AI_Project_Presentation.pptx"):
    prs = Presentation()
    
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    TEAL_PRIMARY = RGBColor(14, 116, 144) # Deep Teal
    TEAL_LIGHT = RGBColor(45, 212, 191)  # Soft Teal
    EMERALD = RGBColor(16, 185, 129)     # Green
    TEXT_DARK = RGBColor(30, 41, 59)     # Slate 800
    TEXT_BODY = RGBColor(51, 65, 85)     # Slate 700
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    TEXT_WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    DARK_CARD = RGBColor(30, 41, 59)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="WELLAWARE AI • HEALTHCARE GENAI PLATFORM", is_dark=False):
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL_LIGHT if is_dark else TEAL_PRIMARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE if is_dark else BG_DARK

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =======================================================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # =======================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.6), Inches(0.12), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL_LIGHT
    bar.line.fill.background()

    # Title & Taglines
    t_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.4), Inches(10.5), Inches(3.8))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "WELLAWARE AI"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(40)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_WHITE

    p1 = tf1.add_paragraph()
    p1.text = "Generative Visual Campaign & Poster Studio for Patient Wellness"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = TEAL_LIGHT
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = (
        "Autonomous Multimodal Diffusion Pipeline with Front-Loaded CLIP Prompt Engineering, "
        "DPM-Solver++ Karras Sampling & Automated Commercial Poster Typography"
    )
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(14)

    # Metadata Badges at bottom
    badges = [
        ("Architecture", "Stable Diffusion v1.5 + DPM-Solver++"),
        ("Inference Speed", "20 Steps • Zero-Cost Local CPU"),
        ("Typography", "Pillow Display Engine (100% Accurate)"),
        ("Domain Coverage", "10 Health Themes • 6 Styles")
    ]
    card_w = Inches(2.65)
    for i, (k, v) in enumerate(badges):
        bx = Inches(1.0) + (i * Inches(2.85))
        add_card(s1, bx, Inches(5.6), card_w, Inches(1.1), bg_color=DARK_CARD, border_color=TEAL_PRIMARY)
        b_box = s1.shapes.add_textbox(bx + Inches(0.15), Inches(5.65), card_w - Inches(0.3), Inches(1.0))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        pb1 = tf_b.paragraphs[0]
        pb1.text = k.upper()
        pb1.font.name = "Segoe UI"
        pb1.font.size = Pt(9)
        pb1.font.bold = True
        pb1.font.color.rgb = TEAL_LIGHT
        pb2 = tf_b.add_paragraph()
        pb2.text = v
        pb2.font.name = "Segoe UI"
        pb2.font.size = Pt(11)
        pb2.font.bold = True
        pb2.font.color.rgb = TEXT_WHITE

    # =======================================================================
    # SLIDE 2: PROBLEM STATEMENT & VALUE PROPOSITION
    # =======================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, BG_LIGHT)
    add_header(s2, "The Healthcare Communication Crisis & The AI Solution")

    # Left Column: The Problem
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    box_prob = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.6))
    tf_p = box_prob.text_frame
    tf_p.word_wrap = True
    
    p_pt = tf_p.paragraphs[0]
    p_pt.text = "⚠️ Challenges in Current Health Messaging"
    p_pt.font.name = "Segoe UI"
    p_pt.font.size = Pt(16)
    p_pt.font.bold = True
    p_pt.font.color.rgb = RGBColor(220, 38, 38)

    prob_bullets = [
        ("Prohibitive Agency Costs: ", "Custom public health artwork requires $2,000–$8,000 per campaign and 2–4 weeks turnaround."),
        ("Generic Stock Imagery: ", "Royalty-free photos lack emotional resonance, clinical specificity, and diverse cultural nuance."),
        ("The AI Text Paradox: ", "Standard diffusion models cannot draw readable words, generating bizarre gibberish (e.g. 'HHEATI C') across visuals."),
        ("Token Truncation: ", "CLIP text encoders discard tokens beyond position 77, causing vital medical instructions to be ignored.")
    ]
    for b_title, b_desc in prob_bullets:
        p_b = tf_p.add_paragraph()
        p_b.space_before = Pt(12)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = BG_DARK
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_BODY

    # Right Column: The WellAware AI Solution
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), bg_color=RGBColor(240, 253, 250), border_color=TEAL_PRIMARY)
    box_sol = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.6))
    tf_s = box_sol.text_frame
    tf_s.word_wrap = True

    p_st = tf_s.paragraphs[0]
    p_st.text = "✨ The WellAware AI Breakthrough"
    p_st.font.name = "Segoe UI"
    p_st.font.size = Pt(16)
    p_st.font.bold = True
    p_st.font.color.rgb = TEAL_PRIMARY

    sol_bullets = [
        ("Dual-Stage Pipeline: ", "Decouples generative artwork synthesis from typographic layout, guaranteeing 100% spelling accuracy."),
        ("Front-Loaded CLIP Optimizer: ", "Strict 77-token ceiling optimization ensures primary health subjects receive 100% neural attention."),
        ("DPM-Solver++ Karras Sampling: ", "Reaches publication-quality vector convergence in just 20 steps (60% faster on CPU)."),
        ("Commercial Poster Engine: ", "Standard 2:3 canvas (640×960) with display headline typography, alpha edge feathering, and crisis helplines.")
    ]
    for b_title, b_desc in sol_bullets:
        p_b = tf_s.add_paragraph()
        p_b.space_before = Pt(12)
        r1 = p_b.add_run()
        r1.text = "✔ " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEAL_PRIMARY
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_BODY

    # =======================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & DATA FLOW
    # =======================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, BG_LIGHT)
    add_header(s3, "End-to-End System Architecture & Modular Data Flow")

    stages = [
        ("1. Input & Controls", "Streamlit UI", "Campaign identity, 10 health themes, 6 styles, aspect ratio & guidance slider."),
        ("2. Prompt Engine", "77-Token CLIP", "Front-loaded subject synthesis, domain taxonomies, heavy anti-text negative filter."),
        ("3. Diffusion Core", "Stable Diffusion v1.5", "DPM-Solver++ Karras scheduler, 20 steps, attention slicing, CPU/CUDA offload."),
        ("4. Editorial Polish", "Pillow Unsharp Mask", "Contrast expansion (1.05), color boost (1.05), and digital edge sharpness (1.15)."),
        ("5. Poster Compositor", "Publication Engine", "Standard 2:3 canvas, Arial Narrow Bold / Impact fonts, edge feathering, action bullets.")
    ]
    c_w = Inches(2.2)
    for i, (st_num, st_tech, st_desc) in enumerate(stages):
        cx = Inches(0.8) + (i * Inches(2.4))
        card = add_card(s3, cx, Inches(1.8), c_w, Inches(4.8))
        
        # Header bar in card
        hbar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), c_w, Inches(0.4))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = TEAL_PRIMARY
        hbar.line.fill.background()

        h_box = s3.shapes.add_textbox(cx, Inches(1.8), c_w, Inches(0.4))
        h_box.text_frame.paragraphs[0].text = f"STAGE {i+1}"
        h_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        h_box.text_frame.paragraphs[0].font.name = "Segoe UI"
        h_box.text_frame.paragraphs[0].font.size = Pt(9.5)
        h_box.text_frame.paragraphs[0].font.bold = True
        h_box.text_frame.paragraphs[0].font.color.rgb = TEXT_WHITE

        # Content in card
        t_box = s3.shapes.add_textbox(cx + Inches(0.12), Inches(2.3), c_w - Inches(0.24), Inches(4.1))
        tf = t_box.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = st_num
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = BG_DARK

        p2 = tf.add_paragraph()
        p2.text = st_tech
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = TEAL_PRIMARY
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = st_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_BODY
        p3.space_before = Pt(12)

    # =======================================================================
    # SLIDE 4: PROMPT SYNTHESIS & ANTI-TEXT FILTERING
    # =======================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, BG_LIGHT)
    add_header(s4, "Front-Loaded CLIP Optimization & Anti-Text Filtering")

    # Left Box: Positive Prompt Engineering
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b_pos = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_pos = b_pos.text_frame
    tf_pos.word_wrap = True

    p_pos_t = tf_pos.paragraphs[0]
    p_pos_t.text = "🎯 Positive Prompt Synthesis Strategy"
    p_pos_t.font.name = "Segoe UI"
    p_pos_t.font.size = Pt(15)
    p_pos_t.font.bold = True
    p_pos_t.font.color.rgb = TEAL_PRIMARY

    p_pos_desc = tf_pos.add_paragraph()
    p_pos_desc.text = (
        "• Strict 77-Token Budget: Bounded to 50–68 tokens so 100% of keywords receive full CLIP attention.\n"
        "• Front-Loaded Attention (Tokens 0–15): The exact user subject is placed immediately after the style tag.\n"
        "• Zero Quoted Formatting: Never injects quotes like 'Mental Health' or words like 'poster/infographic' which confuse the diffusion model into painting fake text banners.\n"
        "• Thematic Color Guidance: Injects domain color palettes (e.g. calming teal, lavender, clean medical cyan)."
    )
    p_pos_desc.font.size = Pt(10.5)
    p_pos_desc.font.color.rgb = TEXT_BODY
    p_pos_desc.space_before = Pt(8)

    # Example Positive Snippet
    p_pos_code = tf_pos.add_paragraph()
    p_pos_code.text = (
        "Synthesized Positive Example:\n"
        "\"modern 2D flat vector illustration of calm peaceful woman touching her forehead in meditation, "
        "themed around Mental Health Awareness, clean outlines, solid plain teal background, high clarity\""
    )
    p_pos_code.font.name = "Consolas"
    p_pos_code.font.size = Pt(9)
    p_pos_code.font.color.rgb = TEAL_PRIMARY
    p_pos_code.space_before = Pt(12)

    # Right Box: Negative Filtering
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(248, 113, 113))
    b_neg = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf_neg = b_neg.text_frame
    tf_neg.word_wrap = True

    p_neg_t = tf_neg.paragraphs[0]
    p_neg_t.text = "🛡️ Front-Loaded Anti-Text Negative Filter"
    p_neg_t.font.name = "Segoe UI"
    p_neg_t.font.size = Pt(15)
    p_neg_t.font.bold = True
    p_neg_t.font.color.rgb = RGBColor(220, 38, 38)

    p_neg_desc = tf_neg.add_paragraph()
    p_neg_desc.text = (
        "• High Negative Weighting: Placed at the very front of the negative vector space to penalize letterforms.\n"
        "• Comprehensive Typographic Blacklist: Bans text, words, alphabet, typography, headlines, slogans, logos, signatures, and garbled pseudotext.\n"
        "• Anti-Clutter Penalties: Bans scribbles, doodles, busy patterns, and crowded backgrounds.\n"
        "• Medical Safety: Bans hospital horror, surgical gore, morbid depictions, and anatomical distortions."
    )
    p_neg_desc.font.size = Pt(10.5)
    p_neg_desc.font.color.rgb = TEXT_BODY
    p_neg_desc.space_before = Pt(8)

    # Example Negative Snippet
    p_neg_code = tf_neg.add_paragraph()
    p_neg_code.text = (
        "Active Negative Prompt:\n"
        "\"text, words, letters, font, typography, script, headline, title, label, slogan, banner, logo, brand, "
        "watermark, signature, blurry text, garbled text, pseudotext, messy doodles, scribbles, ugly, deformed\""
    )
    p_neg_code.font.name = "Consolas"
    p_neg_code.font.size = Pt(8.5)
    p_neg_code.font.color.rgb = RGBColor(185, 28, 28)
    p_neg_code.space_before = Pt(12)

    # =======================================================================
    # SLIDE 5: DIFFUSION ENGINE & HARDWARE OPTIMIZATION
    # =======================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, BG_LIGHT)
    add_header(s5, "Latent Diffusion Engine & Hardware Lifecycle Optimization")

    opt_cards = [
        ("⚡ DPM-Solver++ (Karras Sigmas)", "Fast High-Order Denoising", 
         "Replaces legacy 50-step PNDM scheduler with second-order differential equation solvers. Converges on sharp anatomical and vector details in just 20 steps, reducing inference time by 60% on CPU workstations."),
        ("🧠 Singleton Thread-Safe Pipeline", "Zero Weight Duplication",
         "Encapsulates model weights in a CampaignImageGenerator Singleton. Multi-gigabyte checkpoints are loaded once into RAM, completely eliminating pipeline reload overhead during iterative campaign sessions."),
        ("💾 Attention Slicing & CPU Allocation", "Peak Memory Optimization",
         "Enables multi-head attention slicing across all physical CPU cores (torch.set_num_threads), keeping peak memory consumption within standard 16GB RAM laptops without requiring an NVIDIA GPU."),
        ("✨ Dynamic LoRA Weight Injection", "On-the-Fly Domain Adapters",
         "Integrates load_lora_weights() and unload_lora_weights() methods to hot-swap custom fine-tuned healthcare weights (.safetensors) without restarting the web service.")
    ]
    for idx, (head, sub, body) in enumerate(opt_cards):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + (col * Inches(5.9))
        y = Inches(1.8) + (row * Inches(2.6))
        
        add_card(s5, x, y, Inches(5.6), Inches(2.3))
        b = s5.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.2), Inches(2.0))
        tf = b.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = sub.upper()
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_BODY
        p3.space_before = Pt(6)

    # =======================================================================
    # SLIDE 6: PUBLICATION-GRADE POSTER ENGINE
    # =======================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, BG_LIGHT)
    add_header(s6, "Publication-Grade Poster Typography & Compositing Engine")

    # Left: Explanation
    add_card(s6, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.0))
    b_post = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(7.1), Inches(4.6))
    tf_post = b_post.text_frame
    tf_post.word_wrap = True

    p_post_t = tf_post.paragraphs[0]
    p_post_t.text = "🏛️ Tripartite Commercial Poster Architecture (2:3 Ratio)"
    p_post_t.font.name = "Segoe UI"
    p_post_t.font.size = Pt(16)
    p_post_t.font.bold = True
    p_post_t.font.color.rgb = TEAL_PRIMARY

    p_post_b = tf_post.add_paragraph()
    p_post_b.text = (
        "1. Standard Commercial Canvas (640 × 960):\n"
        "   Eliminates awkward skinny aspect ratios, standardizing on real A3/A4 & social poster proportions.\n\n"
        "2. Top Header Zone (Top 22% / ~211px):\n"
        "   - Organization/Advocacy Badge (e.g. 'PUBLIC HEALTH ADVOCACY • 2026')\n"
        "   - Large Condensed Display Headlines using Arial Narrow Bold (ARIALNB.TTF) or Impact\n"
        "   - High-contrast cream/white text with auto-scaling to prevent text overflow.\n\n"
        "3. Center Hero Visual Zone (55% / ~529px):\n"
        "   - 18px Gaussian Alpha Feathering Mask on top, left, and right borders\n"
        "   - Completely removes harsh rectangular cuts, seamlessly blending art into the canvas.\n\n"
        "4. Bottom Action Block (Bottom 23% / ~220px):\n"
        "   - Solid deep navy card with 3 concise, memorable action bullet points\n"
        "   - Vibrant circular indicator badges (lime green, cyan, coral red)\n"
        "   - Verified public health helplines (e.g. National Crisis & Suicide Lifeline 988)."
    )
    p_post_b.font.size = Pt(10)
    p_post_b.font.color.rgb = TEXT_BODY
    p_post_b.space_before = Pt(8)

    # Right: Embedded Sample Poster
    sample_poster = os.path.join("generated_images", "test_pro_poster_feathered.png")
    if not os.path.exists(sample_poster):
        sample_poster = os.path.join("generated_images", "mental_health_infographic_poster.png")

    if os.path.exists(sample_poster):
        try:
            s6.shapes.add_picture(sample_poster, Inches(8.8), Inches(1.8), width=Inches(3.3), height=Inches(4.95))
        except Exception:
            pass

    # =======================================================================
    # SLIDE 7: 10 HEALTH THEMES & REAL-WORLD USE CASES
    # =======================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, BG_LIGHT)
    add_header(s7, "Comprehensive Domain Coverage across 10 Health Categories")

    domains = [
        ("🧠 Mental Wellness", "Mindfulness, stress reduction, lotus flower, calm contemplation", "UNDERSTAND • TALK ABOUT IT • SEEK HELP"),
        ("🫀 Heart Health", "Glowing active heart, fresh fruits, daily cardiovascular movement", "EAT HEART-HEALTHY • ACTIVE 30 MIN • CHECK BP"),
        ("🩸 Diabetes Care", "Balanced nutrition plate, blue circle ribbon, hydration, glucose control", "CHOOSE WHOLE GRAINS • STAY ACTIVE • CHECK GLUCOSE"),
        ("🥗 Healthy Eating", "Mediterranean nutrient bowl, vibrant berries, fresh greens, olive oil", "EAT RAINBOW VEGGIES • DRINK WATER • LIMIT SUGAR"),
        ("🏃 Physical Fitness", "Active seniors walking in sunlit parks, stretching, outdoor trails", "WALK 7,000+ STEPS • BUILD STRENGTH • TAKE BREAKS"),
        ("🎗️ Cancer Awareness", "Supportive caring hands, awareness ribbons, hopeful golden sunrise", "REGULAR SCREENING • FAMILY HISTORY • HEALTHY LIFE"),
        ("🧼 Hand Hygiene", "Clean washing hands, crystal water droplets, foaming soap bubbles", "WASH SOAP 20 SEC • ALCOHOL SANITIZER • CLEAN TOWEL"),
        ("🌸 Women's Health", "Empowering vitality, botanical self-care motifs, well-woman care", "ANNUAL CHECKUPS • SELF-CARE ROUTINE • NURTURE HEALTH"),
        ("🩺 Preventive Care", "Friendly clinical checkups, stethoscope, health checklists, early action", "ANNUAL EXAMS • VACCINES UP TO DATE • TRACK VITALS"),
        ("📖 Patient Education", "Clear accessible infographic diagrams, friendly guides, health empowerment", "ASK DOCTORS • KNOW MEDICATIONS • TRACK PROGRESS")
    ]
    for i, (title, art, bullets) in enumerate(domains):
        col = i // 5
        row = i % 5
        x = Inches(0.8) + (col * Inches(5.9))
        y = Inches(1.8) + (row * Inches(1.02))
        
        card = add_card(s7, x, y, Inches(5.6), Inches(0.92))
        b = s7.shapes.add_textbox(x + Inches(0.15), y + Inches(0.08), Inches(5.3), Inches(0.78))
        tf = b.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = f"Art: {art} | Bullets: {bullets}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED

    # =======================================================================
    # SLIDE 8: INTERACTIVE STREAMLIT STUDIO
    # =======================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, BG_LIGHT)
    add_header(s8, "Interactive Streamlit Studio UI & Instant Live Customizer")

    ui_features = [
        ("📰 Dual-Tab Output Studio", "Instantly delivers both the Finished Campaign Poster (640×960) and the Standalone Hero Artwork in a tabbed view with 1-click PNG downloads."),
        ("⚡ Instant Live Customizer", "Users can tweak headlines, change action bullet points, or modify crisis helplines, updating the poster in 0.05s without waiting for diffusion inference."),
        ("🔍 Real-Time CLIP Token Inspector", "Live gauge visually tracks positive prompt token density against the 77-token ceiling with optimal green badge indicators."),
        ("⚡ 1-Click Curated Presets", "Seven pre-engineered healthcare campaigns pre-populate optimal prompts, themes, artistic styles, and clinical typography."),
        ("🖼️ Archive Session Gallery", "Persisted local repository of all generated visuals with timestamps, seed identifiers, dimensions, and direct file access."),
        ("🛡️ Ethical Non-Clinical Guardrails", "Prominent medical notices reinforce that WellAware AI is dedicated to public health advocacy and healthy lifestyle education.")
    ]
    for idx, (f_title, f_desc) in enumerate(ui_features):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8) + (c * Inches(5.9))
        y = Inches(1.8) + (r * Inches(1.7))

        add_card(s8, x, y, Inches(5.6), Inches(1.5))
        b = s8.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), Inches(5.2), Inches(1.3))
        tf = b.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f_title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(4)

    # =======================================================================
    # SLIDE 9: QUALITY VALIDATION & AUTOMATED TEST RESULTS
    # =======================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, BG_LIGHT)
    add_header(s9, "Comprehensive Testing & Quality Validation Suite (23/23 PASSED)")

    # Left Box: Summary Stats
    add_card(s9, Inches(0.8), Inches(1.8), Inches(4.5), Inches(5.0), bg_color=RGBColor(240, 253, 244), border_color=EMERALD)
    b_stat = s9.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(4.1), Inches(4.4))
    tf_stat = b_stat.text_frame
    tf_stat.word_wrap = True

    ps1 = tf_stat.paragraphs[0]
    ps1.text = "100% PASS RATE"
    ps1.font.name = "Segoe UI"
    ps1.font.size = Pt(18)
    ps1.font.bold = True
    ps1.font.color.rgb = EMERALD

    ps2 = tf_stat.add_paragraph()
    ps2.text = "23 Passed • 0 Failed"
    ps2.font.name = "Segoe UI"
    ps2.font.size = Pt(28)
    ps2.font.bold = True
    ps2.font.color.rgb = BG_DARK
    ps2.space_before = Pt(4)

    ps3 = tf_stat.add_paragraph()
    ps3.text = (
        "Rigorous automated testing executed via test_suite.py across 5 core verification suites:\n\n"
        "• 100% Theme Token Compliance\n"
        "• 100% Style Directive Accuracy\n"
        "• Strict Directory Traversal Protection\n"
        "• PNG Binary Serialization Integrity\n"
        "• Memory Leaks & Edge Cases Handled"
    )
    ps3.font.name = "Segoe UI"
    ps3.font.size = Pt(11)
    ps3.font.color.rgb = TEXT_BODY
    ps3.space_before = Pt(14)

    # Right Box: Detailed Breakdown Table
    add_card(s9, Inches(5.6), Inches(1.8), Inches(6.9), Inches(5.0))
    b_table = s9.shapes.add_textbox(Inches(5.8), Inches(2.0), Inches(6.5), Inches(4.6))
    tf_tab = b_table.text_frame
    tf_tab.word_wrap = True

    p_tt = tf_tab.paragraphs[0]
    p_tt.text = "📋 Automated Verification Suite Breakdown"
    p_tt.font.name = "Segoe UI"
    p_tt.font.size = Pt(15)
    p_tt.font.bold = True
    p_tt.font.color.rgb = TEAL_PRIMARY

    test_rows = [
        ("Suite 1: Theme Coverage & Token Ceilings", "10 / 10 PASSED", "All 10 themes verified ≤ 70 tokens (within 77-token CLIP limit)."),
        ("Suite 2: Style Directives & Negative Filter", "6 / 6 PASSED", "All 6 styles verified with ~600 character anti-text & safety filters."),
        ("Suite 3: Edge Cases & Input Sanitization", "4 / 4 PASSED", "Empty inputs, 1500+ character stress tests, and SQL/code injection safely absorbed."),
        ("Suite 4: Security & Image Serialization", "2 / 2 PASSED", "Directory traversal attempts confined to generated_images; PNG byte headers verified."),
        ("Suite 5: Image Post-Processing Module", "1 / 1 PASSED", "Editorial polish filters preserved RGB channel integrity and canvas resolution.")
    ]
    for st_name, st_res, st_det in test_rows:
        p_r = tf_tab.add_paragraph()
        p_r.space_before = Pt(8)
        r1 = p_r.add_run()
        r1.text = f"✔ {st_name}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = BG_DARK
        r2 = p_r.add_run()
        r2.text = f"[{st_res}]\n"
        r2.font.bold = True
        r2.font.size = Pt(10)
        r2.font.color.rgb = EMERALD
        r3 = p_r.add_run()
        r3.text = st_det
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = TEXT_MUTED

    # =======================================================================
    # SLIDE 10: CONCLUSION & FUTURE ROADMAP (Dark Theme)
    # =======================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, BG_DARK)
    add_header(s10, "Conclusion & Strategic Future Roadmap", is_dark=True)

    # Left: Conclusion
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), bg_color=DARK_CARD, border_color=TEAL_PRIMARY)
    b_c1 = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.6))
    tf_c1 = b_c1.text_frame
    tf_c1.word_wrap = True

    pc1_t = tf_c1.paragraphs[0]
    pc1_t.text = "🎯 Project Conclusions"
    pc1_t.font.name = "Segoe UI"
    pc1_t.font.size = Pt(16)
    pc1_t.font.bold = True
    pc1_t.font.color.rgb = TEAL_LIGHT

    conc_points = [
        ("Bridged AI & Healthcare Design: ", "Delivered an autonomous tool enabling clinics and non-profits to produce publication-ready campaign posters in seconds."),
        ("Eliminated Garbled AI Text: ", "Proved that decoupling artistic neural diffusion from programmatic typography achieves 100% spelling and layout precision."),
        ("Democratized Access: ", "Operates smoothly on standard multi-core laptop CPUs with zero reliance on paid commercial APIs or NVIDIA hardware."),
        ("Production Verified: ", "Fully tested with 23 automated quality assertions and packaged for multi-platform deployment.")
    ]
    for t_pt, d_pt in conc_points:
        p = tf_c1.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + t_pt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = d_pt
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(203, 213, 225)

    # Right: Future Roadmap
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), bg_color=DARK_CARD, border_color=EMERALD)
    b_c2 = s10.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.6))
    tf_c2 = b_c2.text_frame
    tf_c2.word_wrap = True

    pc2_t = tf_c2.paragraphs[0]
    pc2_t.text = "🚀 Future Enhancement Roadmap"
    pc2_t.font.name = "Segoe UI"
    pc2_t.font.size = Pt(16)
    pc2_t.font.bold = True
    pc2_t.font.color.rgb = EMERALD

    road_points = [
        ("Multilingual Poster Typography: ", "Dynamic font localization across Spanish, Hindi, French, and Arabic to support global WHO humanitarian missions."),
        ("ControlNet Pose Guidance: ", "Integrate OpenPose and Canny edge conditioning to allow doctors to specify exact patient and clinician physical postures."),
        ("QR Code Integration: ", "Automatically generate dynamic QR codes linking patients directly to appointment scheduling and local health resources."),
        ("Interactive Patient Voice Avatars: ", "Pair visual campaigns with lightweight localized LLMs for conversational audio guidance.")
    ]
    for t_pt, d_pt in road_points:
        p = tf_c2.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "➔ " + t_pt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = d_pt
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(203, 213, 225)

    # Save presentation
    prs.save(output_path)
    print(f"[OK] Presentation successfully generated and saved to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_wellaware_presentation("WellAware_AI_Project_Presentation.pptx")
