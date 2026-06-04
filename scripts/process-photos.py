#!/usr/bin/env python3
"""Process raw project photos for website gallery.

Usage: python3 scripts/process-photos.py

Reads scripts/photo-manifest.csv with columns:
  source_file,slug,category,caption,city,year

For each entry:
  1. Opens source JPEG, fixes EXIF orientation
  2. Crops to 4:3 landscape (centered)
  3. Resizes to 1200w (gallery grid) and 400w (thumbnail)
  4. Saves as WebP (both sizes) and JPEG fallback (1200w only)
  5. Strips all EXIF metadata from outputs
"""

import csv
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps

SRC = Path("/home/amram/Pictures/Electric Work")
OUT = Path("/home/amram/WEBSITE/img/gallery")
MANIFEST = Path(__file__).parent / "photo-manifest.csv"
QUALITY = 82
QUALITY_THUMB = 75


def exif_transpose_fix(im):
    """Fix EXIF orientation and strip all EXIF."""
    im = ImageOps.exif_transpose(im)
    if im is None:
        return None
    return im.copy()


def center_crop_4_3(im):
    """Crop to 4:3 landscape ratio, centered."""
    w, h = im.size
    target = w / 4 * 3
    if h > target:
        top = (h - target) / 2
        im = im.crop((0, top, w, top + target))
    else:
        target_w = h / 3 * 4
        left = (w - target_w) / 2
        im = im.crop((left, 0, left + target_w, h))
    return im


def process_one(row):
    source = row["source_file"].strip()
    slug = row["slug"].strip()
    category = row["category"].strip()
    caption = row["caption"].strip()
    city = row.get("city", "").strip()
    year = row.get("year", "").strip()

    src_path = SRC / source
    if not src_path.exists():
        print(f"  SKIP: {source} not found")
        return

    print(f"  Processing: {source} → {slug}")
    with Image.open(src_path) as im:
        # Fix orientation
        im = exif_transpose_fix(im)
        if im is None:
            print(f"  ERROR: exif_transpose returned None for {source}")
            return

        # Ensure RGB
        if im.mode != "RGB":
            im = im.convert("RGB")

        # Crop to 4:3
        im = center_crop_4_3(im)

        w, h = im.size

        # Resize variants
        if w > 1200:
            ratio = 1200.0 / w
            im_1200 = im.resize((1200, int(h * ratio)), Image.LANCZOS)
        else:
            im_1200 = im.copy()

        if w > 400:
            ratio = 400.0 / w
            im_400 = im.resize((400, int(h * ratio)), Image.LANCZOS)
        else:
            im_400 = im.copy()

        # WebP (1200w)
        im_1200.save(OUT / f"{slug}-1200w.webp", "WEBP", quality=QUALITY, method=6)
        # JPEG fallback (1200w)
        im_1200.save(OUT / f"{slug}-1200w.jpg", "JPEG", quality=QUALITY, optimize=True)
        # WebP thumbnail (400w)
        im_400.save(OUT / f"{slug}-400w.webp", "WEBP", quality=QUALITY_THUMB, method=6)

    print(f"    OK: {slug}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Processing {len(rows)} photos...")
    for row in rows:
        process_one(row)
    print("Done.")


if __name__ == "__main__":
    main()
