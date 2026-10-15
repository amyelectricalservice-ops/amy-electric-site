#!/usr/bin/env python3
"""Apply logged privacy redactions (Gaussian blur boxes) to gallery outputs.

Usage: python3 scripts/apply-redactions.py

Reads data/privacy-redactions.json: {slug: [[x0,y0,x1,y1], ...]} with boxes in
1200x900 output coordinates. Applies matching scaled boxes to all four variants
(-1200w.webp, -1200w.jpg, -800w.webp, -400w.webp).

These run AFTER scripts/process-photos.py. A process-photos re-run overwrites
redacted files with clean renders, so always re-run this script afterwards.
"""
import json
from pathlib import Path
from PIL import Image, ImageFilter

WEBSITE = Path(__file__).parent.parent
GALLERY = WEBSITE / "img/gallery"
LOG = WEBSITE / "data" / "privacy-redactions.json"

VARIANTS = [
    ("1200w.webp", 1200, 12),
    ("1200w.jpg", 1200, 12),
    ("800w.webp", 800, 8),
    ("400w.webp", 400, 4),
]


def main():
    redactions = json.loads(LOG.read_text())
    for slug, boxes in redactions.items():
        for suffix, width, radius in VARIANTS:
            path = GALLERY / f"{slug}-{suffix}"
            if not path.exists():
                print(f"  SKIP {slug}-{suffix}: not found")
                continue
            im = Image.open(path).convert("RGB")
            scale = im.width / 1200.0
            for x0, y0, x1, y1 in boxes:
                box = tuple(int(v * scale) for v in (x0, y0, x1, y1))
                region = im.crop(box).filter(ImageFilter.GaussianBlur(max(2, int(radius * scale))))
                im.paste(region, (box[0], box[1]))
            if suffix.endswith(".webp"):
                im.save(path, "WEBP", quality=75, method=6)
            else:
                im.save(path, "JPEG", quality=75, optimize=True)
            print(f"  OK {slug}-{suffix}: {len(boxes)} box(es)")


if __name__ == "__main__":
    main()
