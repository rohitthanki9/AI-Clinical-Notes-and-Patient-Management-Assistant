#!/usr/bin/env python3
"""
Build script for Clinical Notes AI
Converts icon and builds executable with PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_icon():
    """Convert PNG icon to ICO format"""
    print("Converting icon.png to icon.ico...")

    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow for icon conversion...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image

    icon_png = Path("assets/icon.png")
    icon_ico = Path("assets/icon.ico")

    if not icon_png.exists():
        print("WARNING: assets/icon.png not found!")
        print("Please add your icon.png file to the assets folder.")
        print("Continuing without icon...")
        return None

    try:
        img = Image.open(icon_png)
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Save as ICO with multiple sizes
        img.save(icon_ico, format='ICO', sizes=[
            (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
        ])
        print(f"✓ Icon converted: {icon_ico}")
        return str(icon_ico)
    except Exception as e:
        print(f"Error converting icon: {e}")
        return None

def build_executable(icon_path=None):
    """Build the executable using PyInstaller"""
    print("\nBuilding executable with PyInstaller...")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Clinical Notes AI",
    ]

    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])

    # Add data folders
    if sys.platform == "win32":
        separator = ";"
    else:
        separator = ":"

    cmd.extend([
        "--add-data", f"prompts{separator}prompts",
        "--add-data", f"assets{separator}assets",
    ])

    # Add hidden imports
    cmd.extend([
        "--hidden-import", "whisper",
        "--hidden-import", "ttkbootstrap",
        "--hidden-import", "sounddevice",
        "--hidden-import", "soundfile",
        "--hidden-import", "tkinter",
        "--hidden-import", "sqlite3",
    ])

    # Add main script
    cmd.append("main.py")

    print(f"Running: {' '.join(cmd)}")
    print("\nThis may take 5-10 minutes...")

    try:
        subprocess.check_call(cmd)
        print("\n" + "="*70)
        print("BUILD SUCCESSFUL!".center(70))
        print("="*70)
        print("\nYour executable is ready:")
        if sys.platform == "win32":
            print("  dist/Clinical Notes AI.exe")
        elif sys.platform == "darwin":
            print("  dist/Clinical Notes AI.app")
        else:
            print("  dist/Clinical Notes AI")
        print("\nYou can distribute this file to users.")
        print("Note: Users will still need to install Ollama separately for AI features.")
        print("="*70)
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)

def main():
    """Main build process"""
    print("="*70)
    print("Clinical Notes AI - Build Script".center(70))
    print("="*70)
    print()

    # Step 1: Convert icon
    icon_path = convert_icon()

    # Step 2: Build executable
    build_executable(icon_path)

if __name__ == "__main__":
    main()
