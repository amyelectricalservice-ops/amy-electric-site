#!/usr/bin/env python3
"""Redact or blur privacy-sensitive content from published gallery photos.

Usage: python3 scripts/redact-photos.py
Outputs: overwrites img/gallery/{slug}-1200w.webp, -1200w.jpg, -400w.webp in place.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).parent.parent / "img" / "gallery"
QUALITY = 82
QUALITY_THUMB = 75
FACE_BLUR_RADIUS = 12

REDACTIONS_PATH = Path(__file__).parent / "photo-redactions.json"


def blur_box(im, box):
    """Apply Gaussian blur to a region."""
    x1, y1, x2, y2 = box
    region = im.crop(box)
    blurred = region.filter(ImageFilter.GaussianBlur(FACE_BLUR_RADIUS))
    im.paste(blurred, box)


def blackout_box(im, box):
    """Draw a black rectangle."""
    draw = ImageDraw.Draw(im)
    draw.rectangle(box, fill="black")


def main():
    import json
    with open(REDACTIONS_PATH) as f:
        raw = json.load(f)
    redactions = {slug: [tuple(b) for b in boxes] for slug, boxes in raw.items()}

    for slug, boxes in redactions.items():
        src_1200 = OUT / f"{slug}-1200w.jpg"
        if not src_1200.exists():
            print(f"SKIP: {src_1200} not found")
            continue

        is_text = "steel-stud" in slug
        action = "Redacting text" if is_text else "Blurring faces"
        print(f"{action}: {slug}")

        with Image.open(src_1200) as im:
            im = im.convert("RGB")

            for box in boxes:
                x1, y1, x2, y2 = box
                w, h = im.size
                x1 = max(0, min(w, x1))
                y1 = max(0, min(h, y1))
                x2 = max(0, min(w, x2))
                y2 = max(0, min(h, y2))
                if is_text:
                    blackout_box(im, (x1, y1, x2, y2))
                else:
                    blur_box(im, (x1, y1, x2, y2))

            # Save 1200w variants
            im.save(OUT / f"{slug}-1200w.webp", "WEBP", quality=QUALITY, method=6)
            im.save(OUT / f"{slug}-1200w.jpg", "JPEG", quality=QUALITY, optimize=True)

            # 400w thumbnail
            ratio = 400.0 / w
            thumb = im.resize((400, int(h * ratio)), Image.LANCZOS)
            thumb.save(OUT / f"{slug}-400w.webp", "WEBP", quality=QUALITY_THUMB, method=6)

            print(f"  OK ({w}x{h})")

    print("Done.")


if __name__ == "__main__":
    main()
