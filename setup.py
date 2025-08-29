#!/usr/bin/env python3
"""
Lookalike Setup Verification Script
Checks system requirements and guides through installation
"""

import sys
import os
import subprocess
import platform

def print_header():
    """Print the application header."""
    print("🎭 Lookalike - Celebrity Face Recognition App")
    print("=" * 50)
    print("Setup Verification and Installation Guide")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    print("\n🐍 Checking Python version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"   Current version: Python {version_str}")
    
    if version.major == 3 and version.minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.8 or higher is required")
        print("   💡 Please install Python 3.8+ from https://python.org")
        return False

def check_system_info():
    """Display system information."""
    print("\n💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        print("   🍎 Apple Silicon (M1/M2) detected")
        print("   💡 Special installation steps may be needed for dlib")
        return "apple_silicon"
    elif platform.system() == "Darwin":
        print("   🍎 Intel Mac detected")
        return "intel_mac"
    elif platform.system() == "Windows":
        print("   🪟 Windows detected")
        return "windows"
    else:
        print("   🐧 Linux detected")
        return "linux"

def check_dependencies():
    """Check if virtual environment and dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    # Check if venv exists
    if os.path.exists("venv"):
        print("   ✅ Virtual environment found")
        
        # Check if Flask is installed in venv
        try:
            if os.path.exists("venv/lib/python3.*/site-packages/flask") or \
               os.path.exists("venv/Lib/site-packages/flask"):
                print("   ✅ Flask appears to be installed")
                return True
            else:
                print("   ⚠️  Flask not found in virtual environment")
                return False
        except:
            print("   ⚠️  Unable to verify Flask installation")
            return False
    else:
        print("   ⚠️  Virtual environment not found")
        return False

def provide_installation_guide(system_type):
    """Provide installation instructions based on system type."""
    print("\n🚀 Installation Guide:")
    print("-" * 30)
    
    print("\n1️⃣  Create and activate virtual environment:")
    print("   python3 -m venv venv")
    if system_type == "windows":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2️⃣  Install dependencies:")
    
    if system_type == "apple_silicon":
        print("   🍎 For Apple Silicon (M1/M2), try one of these options:")
        print("\n   Option A - Using Homebrew (Recommended):")
        print("   brew install cmake dlib")
        print("   pip install -r requirements.txt")
        print("\n   Option B - Using Conda:")
        print("   conda create -n lookalike python=3.9")
        print("   conda activate lookalike")
        print("   conda install -c conda-forge dlib")
        print("   pip install Flask face-recognition opencv-python Pillow numpy")
    else:
        print("   pip install -r requirements.txt")
    
    print("\n3️⃣  Run the application:")
    print("   python app.py")
    print("   # Or use the convenience script:")
    print("   ./run.sh")
    
    print("\n4️⃣  Open your browser:")
    print("   http://localhost:5000")

def main():
    """Main setup verification function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup cannot continue with incompatible Python version")
        sys.exit(1)
    
    # Check system info
    system_type = check_system_info()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 50)
    
    if deps_ok:
        print("🎉 Setup appears to be complete!")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   # Or:")
        print("   ./run.sh")
        print("\n📍 Then open: http://localhost:5000")
    else:
        print("⚠️  Setup needs to be completed")
        provide_installation_guide(system_type)
    
    print("\n📚 For detailed instructions, see README.md")
    print("🐛 For issues, check the troubleshooting section in README.md")

if __name__ == "__main__":
    main()
