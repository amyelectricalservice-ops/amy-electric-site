#!/usr/bin/env python3
"""Process images using Pillow: resize to max width, save JPEG + WebP."""

import os
import sys
from PIL import Image

MAX_WIDTH = 1200
JPEG_QUALITY = 85
WEBP_QUALITY = 80


def process_image(src_path, dst_dir, new_name):
    """Resize and save as JPEG + WebP."""
    os.makedirs(dst_dir, exist_ok=True)

    img = Image.open(src_path)

    # Fix orientation from EXIF
    try:
        from PIL import ExifTags
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == "Orientation":
                    if value == 3:
                        img = img.rotate(180, expand=True)
                    elif value == 6:
                        img = img.rotate(270, expand=True)
                    elif value == 8:
                        img = img.rotate(90, expand=True)
                    break
    except Exception:
        pass

    # Resize if wider than MAX_WIDTH
    w, h = img.size
    if w > MAX_WIDTH:
        ratio = MAX_WIDTH / w
        new_h = int(h * ratio)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    base = os.path.splitext(new_name)[0]

    # Save JPEG
    jpeg_path = os.path.join(dst_dir, base + ".jpg")
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(jpeg_path, "JPEG", quality=JPEG_QUALITY)

    # Save WebP
    webp_path = os.path.join(dst_dir, base + ".webp")
    img.save(webp_path, "WEBP", quality=WEBP_QUALITY)

    return img.size


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: process_image.py <src> <dst_dir> <new_name>")
        sys.exit(1)

    src = sys.argv[1]
    dst_dir = sys.argv[2]
    new_name = sys.argv[3]

    w, h = process_image(src, dst_dir, new_name)
    print(f"{w} {h}")
