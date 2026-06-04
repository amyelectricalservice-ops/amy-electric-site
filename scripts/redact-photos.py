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

# Each entry: slug, list of (x1, y1, x2, y2) boxes in 1200x900 coords
# faces → Gaussian blur, text → black box
REDACTIONS = {
    "gallery-commercial-parking-team": [
        # Worker 1 (orange hoodie, crouching, partial face)
        (340, 400, 470, 520),
        # Worker 2 (dark hoodie, back to camera, partial profile)
        (500, 340, 630, 470),
        # Worker 3 (black hoodie, full face profile)
        (645, 360, 795, 480),
    ],
    "gallery-lighting-commercial-install": [
        # Worker 1 (green shirt on ladder, face profile)
        (490, 100, 690, 260),
        # Worker 2 (orange shirt, full face with glasses)
        (480, 440, 690, 660),
    ],
    "gallery-team-utility-lines": [
        # Worker in dark blue jacket, full face with glasses
        (370, 320, 650, 680),
    ],
    "gallery-roughin-steel-stud": [
        # "302" handwritten on drywall
        (400, 250, 605, 360),
    ],
}


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
    for slug, boxes in REDACTIONS.items():
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
