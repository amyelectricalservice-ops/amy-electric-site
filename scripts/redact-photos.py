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
    redactions = {}
    for slug, entry in raw.items():
        # New form: {"action": "blackout"|"blur", "boxes": [[x1,y1,x2,y2], ...]}.
        # Legacy form: bare [[...], ...] list — action inferred as before.
        if isinstance(entry, dict):
            redactions[slug] = (entry.get('action', 'blur'),
                                [tuple(b) for b in entry.get('boxes', [])])
        else:
            legacy_text = "steel-stud" in slug
            redactions[slug] = ('blackout' if legacy_text else 'blur',
                                [tuple(b) for b in entry])

    for slug, (action, boxes) in redactions.items():
        src_1200 = OUT / f"{slug}-1200w.jpg"
        if not src_1200.exists():
            print(f"SKIP: {src_1200} not found")
            continue

        is_text = action == 'blackout'
        print(f"{'Redacting text' if is_text else 'Blurring faces'}: {slug}")

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

            # 800w intermediate (same settings as scripts/process-photos.py
            # QUALITY_MID). Without this the 800w srcset candidate keeps the
            # pre-redaction pixels.
            if w > 800:
                ratio800 = 800.0 / w
                im_800 = im.resize((800, int(h * ratio800)), Image.LANCZOS)
            else:
                im_800 = im.copy()
            im_800.save(OUT / f"{slug}-800w.webp", "WEBP", quality=72, method=6)

            # 400w thumbnail
            ratio = 400.0 / w
            thumb = im.resize((400, int(h * ratio)), Image.LANCZOS)
            thumb.save(OUT / f"{slug}-400w.webp", "WEBP", quality=QUALITY_THUMB, method=6)

            print(f"  OK ({w}x{h})")

    print("Done.")


if __name__ == "__main__":
    main()
