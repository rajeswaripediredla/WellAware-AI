# 🌿 WellAware AI: Patient Wellness Campaign Visual Generator

> **"Creating Visuals for a Healthier Tomorrow"**  
> An enterprise-grade Generative AI application for synthesizing publication-ready public health awareness posters, educational banners, and wellness campaign visuals.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Technology Stack](#-technology-stack)
5. [Local Installation & Setup (VS Code)](#-local-installation--setup-vs-code)
6. [Alternative Execution: Google Colab GPU](#-alternative-execution-google-colab-gpu)
7. [Automated Verification & Test Suites](#-automated-verification--test-suites)
8. [Production Deployment Guide](#-production-deployment-guide)
9. [Ethical Standards & Non-Clinical Disclaimer](#-ethical-standards--non-clinical-disclaimer)
10. [License](#-license)

---

## 🎯 Project Overview

Healthcare foundations, pharmaceutical communication teams, and non-profit advocacy organizations frequently require custom, high-impact campaign imagery for awareness drives such as:
- **Cardiovascular Health:** Heart health, hypertension, active lifestyle
- **Chronic Care Awareness:** Diabetes prevention, balanced nutrition
- **Mental Wellness:** Mindfulness, stress reduction, meditation
- **Preventative Health:** Routine checkups, early screening, vaccination
- **Infection Prevention:** Pristine hygiene, handwashing advocacy
- **Nutrition & Fitness:** Whole-food diets, daily mobility, hydration

Instead of relying on repetitive stock photography or long design turnaround cycles, **WellAware AI** synthesizes bespoke, high-contrast, culturally sensitive campaign visuals from brief text themes using fine-tuned prompt engineering and latent diffusion models.

---

## ✨ Key Features

1. **Front-Loaded CLIP Prompt Engineering:**
   - Automatically expands high-level themes into structured, high-density prompts.
   - Strictly bounded within CLIP's **77-token ceiling** to ensure 100% keyword attention and eliminate image muddiness.
2. **6 Specialized Artistic Styles:**
   - 🎨 **3D Illustration:** Modern isometric clay renders (Pixar/ArtStation aesthetic).
   - 📐 **Minimalist:** Modern Scandinavian graphic design with clean negative space.
   - 📸 **Photorealistic:** Commercial 85mm studio healthcare photography.
   - 📊 **Flat Design:** Swiss-style corporate infographic vectors.
   - 🧸 **Cartoon Illustration:** Friendly storybook patient education graphics.
   - 🏥 **Professional Healthcare Illustration:** Scientific editorial watercolor clarity (Mayo Clinic style).
3. **Curated Healthcare Taxonomies:**
   - Pre-engineered color palettes, visual motifs, and symbolic elements for 10 public health domains.
4. **Multi-Variation Generation:**
   - Generate up to 4 distinct variations per run using systematic latent noise seeding.
5. **DPM-Solver++ (Karras) Sampling:**
   - Achieves sharp, crisp convergence in just **20 steps** (70% faster than legacy 50-step samplers).
6. **Editorial Polish Engine:**
   - Built-in post-processing that optimizes micro-contrast, edge sharpness, and color vibrance.
7. **Session Archive & One-Click PNG Export:**
   - Direct high-resolution PNG download with sanitized timestamps and persistent session gallery.

---

## 🏗️ System Architecture

```
WellAware-AI/
│
├── app.py                      # Multi-Page Streamlit Studio (UI & Session Controller)
├── prompt_generator.py         # 77-Token Front-Loaded Healthcare Prompt Synthesizer
├── image_generator.py          # Singleton Diffusers Engine (DPM-Solver++ Karras)
├── config.py                   # Central Settings, Hardware Offload & Aspect Ratios
├── requirements.txt            # Validated Dependency Manifest
│
├── check_env.py                # Environment Diagnostic & Package Verifier
├── test_prompt_generator.py    # Prompt Module Unit Test
├── test_image_generator.py     # Image Generation Integration Test
├── test_suite.py               # Comprehensive 23-Point Quality & Security Suite
│
├── generated_images/           # Session Archive for Saved Campaign PNGs
└── assets/                     # Visual Branding & Design Artifacts
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.11+ | Core runtime |
| **Generative AI** | Hugging Face Diffusers | 0.43.0+ | Latent diffusion pipeline & schedulers |
| **Foundation Model**| Stable Diffusion v1.5 | `runwayml/stable-diffusion-v1-5` | Pretrained text-to-image weights |
| **Deep Learning** | PyTorch & Transformers | 2.15+ / 5.24+ | Tensor operations & CLIP ViT-L/14 text encoder |
| **Inference Scheduler**| DPM-Solver++ (Karras) | Multistep | Fast 20-step high-fidelity ODE solver |
| **Web UI** | Streamlit | 1.67+ | Reactive multi-page web application |
| **Image Processing**| Pillow (PIL) | 13.0+ | Image enhancement & PNG stream serialization |

---

## 💻 Local Installation & Setup (VS Code)

### Step 1: Clone or Open Project
```powershell
cd c:\Users\HP\OneDrive\Desktop\WellAware-AI
```

### Step 2: Initialize Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Environment
```powershell
python check_env.py
```

### Step 5: Launch Streamlit Studio
```powershell
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🚀 Alternative Execution: Google Colab GPU

If you wish to execute generations in under **5 seconds** using a free **NVIDIA T4 GPU**:
1. Open [Google Colab](https://colab.research.google.com/).
2. Upload `WellAware_AI_Colab_Phase2.ipynb` from this repository.
3. Switch runtime to **T4 GPU** (*Runtime $\rightarrow$ Change runtime type $\rightarrow$ T4 GPU*).
4. Run the notebook cells to execute cloud inference.

---

## 🧪 Automated Verification & Test Suites

The repository includes a 23-point automated test suite:

```powershell
# Run Comprehensive Phase 6 Test Suite
python test_suite.py
```

### Test Coverage Highlights:
- ✅ **Theme Coverage (10/10):** Validates prompt generation and token counts across all healthcare topics.
- ✅ **Style Coverage (6/6):** Validates style-specific positive directives and negative filters.
- ✅ **Boundary & Edge Cases:** Verified against empty inputs, 1500+ char strings, and code injection.
- ✅ **Filesystem Security:** Path sanitization prevents directory traversal attacks.
- ✅ **Download Integrity:** In-memory PNG byte serialization confirmed for browser exports.

---

## 🌐 Production Deployment Guide

### Option A: Streamlit Community Cloud (Recommended for Demos)
1. Push the `WellAware-AI` repository to GitHub.
2. Log in to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, set the main file to `app.py`, and deploy.
4. *Note:* Streamlit Cloud runs on CPU; generation takes ~90s per visual. For sub-5s performance, use Option B or C.

### Option B: Hugging Face Spaces (GPU Enabled)
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Select **Streamlit** as the SDK.
3. Choose a **T4 Small (16GB VRAM)** hardware tier.
4. Push the project files. Hugging Face caches the `runwayml/stable-diffusion-v1-5` model automatically within its internal hub network.

### Option C: Containerized Deployment (Docker + NVIDIA GPU)
Create a `Dockerfile`:
```dockerfile
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Build and run:
```bash
docker build -t wellaware-ai .
docker run --gpus all -p 8501:8501 wellaware-ai
```

---

## 🛡️ Ethical Standards & Non-Clinical Disclaimer

> **IMPORTANT NOTICE:**  
> **WellAware AI** is developed solely for **non-clinical public health communication, patient education, and wellness advocacy**.  
> It is **not** an FDA/CE-cleared medical device and must **never** be used for clinical diagnosis, prescribing, treatment decisions, or personalized medical triage.
>
> All generated visual assets adhere to the **CreativeML OpenRAIL-M** ethical license, strictly prohibiting the synthesis of defamatory, harmful, or discriminatory health depictions.

---

## 📄 License
This project is open-source and distributed under the terms of the **CreativeML OpenRAIL-M License**.
