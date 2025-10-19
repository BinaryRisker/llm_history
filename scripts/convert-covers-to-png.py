#!/usr/bin/env python3
"""
Convert SVG covers to PNG format for better compatibility
Run: python scripts/convert-covers-to-png.py
"""

import os
import sys

# Check if cairosvg is available
try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

def convert_svg_to_png(svg_path, png_path, width=1600):
    """Convert SVG to PNG with specified width (height auto)"""
    if HAS_CAIRO:
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            output_width=width
        )
        print(f"✓ Converted: {svg_path} -> {png_path}")
        return True
    else:
        print(f"⚠ cairosvg not installed. Please install with:")
        print("  pip install cairosvg")
        return False

def main():
    svg_dir = "assets/images"
    png_dir = "assets/images"

    svg_files = [
        "cover-1-minimal.svg",
        "cover-2-geometric.svg",
        "cover-3-tech.svg",
        "cover-4-brain.svg",
        "cover-5-complex.svg"
    ]

    print("Converting SVG covers to PNG...")
    print("=" * 50)

    if not HAS_CAIRO:
        print("\n⚠️  cairosvg is not installed!")
        print("\nTo install, run:")
        print("  pip install cairosvg")
        print("\nOr use online converter:")
        print("  https://cloudconvert.com/svg-to-png")
        print("\nRecommended PNG size: 1600x2400 pixels")
        return 1

    success_count = 0
    for svg_file in svg_files:
        svg_path = os.path.join(svg_dir, svg_file)
        png_file = svg_file.replace('.svg', '.png')
        png_path = os.path.join(png_dir, png_file)

        if os.path.exists(svg_path):
            if convert_svg_to_png(svg_path, png_path, width=1600):
                success_count += 1
        else:
            print(f"✗ Not found: {svg_path}")

    print("=" * 50)
    print(f"Converted {success_count}/{len(svg_files)} covers")

    if success_count > 0:
        print("\n✓ Now update cover.md to use PNG:")
        print('  <img src="assets/images/cover-5-complex.png" ...>')
        print("\n✓ And update epub-metadata.yaml:")
        print('  cover-image: "assets/images/cover-5-complex.png"')
        print("\nThen run: .\\scripts\\build-all.ps1")

    return 0

if __name__ == "__main__":
    sys.exit(main())
