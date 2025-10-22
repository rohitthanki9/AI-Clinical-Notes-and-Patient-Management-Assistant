#!/usr/bin/env python3
"""
Create a simple medical cross icon for the application
Run this to generate assets/icon.png
"""

from PIL import Image, ImageDraw

def create_medical_icon():
    """Create a simple medical cross icon"""
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle - Medical blue
    margin = 10
    draw.ellipse(
        [margin, margin, size-margin, size-margin],
        fill=(41, 128, 185, 255),  # Medical blue
        outline=(52, 152, 219, 255),
        width=3
    )

    # White medical cross
    cross_color = (255, 255, 255, 255)
    cross_width = 40
    cross_length = 140

    # Vertical bar of cross
    x_center = size // 2
    y_center = size // 2
    draw.rectangle(
        [
            x_center - cross_width // 2,
            y_center - cross_length // 2,
            x_center + cross_width // 2,
            y_center + cross_length // 2
        ],
        fill=cross_color
    )

    # Horizontal bar of cross
    draw.rectangle(
        [
            x_center - cross_length // 2,
            y_center - cross_width // 2,
            x_center + cross_length // 2,
            y_center + cross_width // 2
        ],
        fill=cross_color
    )

    # Save the icon
    import os
    os.makedirs('assets', exist_ok=True)
    img.save('assets/icon.png', 'PNG')
    print("✓ Created: assets/icon.png (256x256)")

    # Also create smaller versions
    for size in [128, 64, 32, 16]:
        small = img.resize((size, size), Image.Resampling.LANCZOS)
        small.save(f'assets/icon_{size}.png', 'PNG')
        print(f"✓ Created: assets/icon_{size}.png")

    print("\nIcon created successfully!")
    print("You can replace assets/icon.png with your own logo.")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw
        create_medical_icon()
    except ImportError:
        print("Installing Pillow...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageDraw
        create_medical_icon()
