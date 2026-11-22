"""
WellAware AI - Environment Verification Script
Validates Python version, installed dependencies, directory structure, and compute device (CUDA GPU vs CPU).
"""

import sys
import os
import platform

def verify_environment():
    print("=" * 60)
    print("  WellAware AI - Environment Diagnostic & Verification")
    print("=" * 60)
    
    # 1. Python Version Check
    py_ver = sys.version_info
    print(f"\n[1/4] Operating System: {platform.system()} {platform.release()}")
    print(f"      Python Version:   {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver.major == 3 and py_ver.minor >= 10:
        print("      Status:           [OK] Python version is compatible (>= 3.10).")
    else:
        print("      Status:           [WARNING] Python 3.10+ recommended.")

    # 2. Directory Structure Check
    print("\n[2/4] Verifying Project Directories:")
    required_dirs = ["generated_images", "assets"]
    for d in required_dirs:
        exists = os.path.exists(d)
        status = "[OK]" if exists else "[MISSING]"
        print(f"      - {d:<20} {status}")
        if not exists:
            os.makedirs(d, exist_ok=True)
            print(f"        -> Created directory: {d}")

    # 3. Dependency Check
    print("\n[3/4] Verifying Installed Packages:")
    packages = [
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("diffusers", "Hugging Face Diffusers"),
        ("transformers", "Hugging Face Transformers"),
        ("accelerate", "Hugging Face Accelerate"),
        ("safetensors", "SafeTensors"),
        ("streamlit", "Streamlit"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy")
    ]
    
    missing_packages = []
    for pkg_import, pkg_name in packages:
        try:
            mod = __import__(pkg_import)
            ver = getattr(mod, "__version__", "installed")
            print(f"      - {pkg_name:<26} [OK] (v{ver})")
        except ImportError:
            print(f"      - {pkg_name:<26} [NOT INSTALLED]")
            missing_packages.append(pkg_name)

    # 4. Device and Hardware Acceleration Check
    print("\n[4/4] Verifying Hardware Acceleration:")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"      - Compute Device:  CUDA (GPU)")
            print(f"      - GPU Model:       {gpu_name}")
            print(f"      - Total VRAM:      {vram_gb:.2f} GB")
            print("      Status:            [EXCELLENT] Hardware GPU acceleration is ready.")
        else:
            print("      - Compute Device:  CPU")
            print("      Status:            [NOTICE] No CUDA GPU detected locally.")
            print("                         For faster inference, use Google Colab T4 GPU runtime")
            print("                         or enable low-memory CPU settings in config.py.")
    except ImportError:
        print("      - PyTorch is not yet installed. Install requirements first.")

    print("\n" + "=" * 60)
    if missing_packages:
        print(f"Summary: Setup is pending {len(missing_packages)} package(s).")
        print("Run: pip install -r requirements.txt")
    else:
        print("Summary: All Phase 1 environment components are verified and ready!")
    print("=" * 60)

if __name__ == "__main__":
    verify_environment()
