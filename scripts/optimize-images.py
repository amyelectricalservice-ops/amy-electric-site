#!/usr/bin/env python3
"""One-time image optimization: add 800w WebP variants and recompress existing 1200w images."""
from pathlib import Path
from PIL import Image

GALLERY = Path(__file__).parent.parent / "img" / "gallery"
QUALITY = 75
QUALITY_MID = 72
QUALITY_THUMB = 70


def main():
    files = sorted(GALLERY.glob("*-1200w.webp"))
    print(f"Found {len(files)} 1200w WebP images")

    for f in files:
        slug = f.name.replace("-1200w.webp", "")

        # Generate 800w variant if missing
        f_800 = GALLERY / f"{slug}-800w.webp"
        if not f_800.exists():
            with Image.open(f) as im:
                w, h = im.size
                target = 800
                if w > target:
                    ratio = target / w
                    im_800 = im.resize((800, int(h * ratio)), Image.LANCZOS)
                    im_800.save(f_800, "WEBP", quality=QUALITY_MID, method=6)
                    kb = f_800.stat().st_size // 1024
                    print(f"  + {slug}-800w.webp ({kb} KiB)")
        else:
            # Already exists, check if it needs recompression at new quality
            pass

        # Recompress 400w thumbnail at new quality
        f_400 = GALLERY / f"{slug}-400w.webp"
        if f_400.exists():
            old_kb = f_400.stat().st_size // 1024
            with Image.open(f_400) as im:
                im.save(f_400, "WEBP", quality=QUALITY_THUMB, method=6)
            new_kb = f_400.stat().st_size // 1024
            if new_kb != old_kb:
                print(f"  ~ {slug}-400w.webp ({old_kb} -> {new_kb} KiB)")

        # Recompress 1200w at new quality
        old_kb = f.stat().st_size // 1024
        with Image.open(f) as im:
            im.save(f, "WEBP", quality=QUALITY, method=6)
        new_kb = f.stat().st_size // 1024
        if new_kb != old_kb:
            print(f"  ~ {slug}-1200w.webp ({old_kb} -> {new_kb} KiB)")

        # Recompress JPEG fallback
        f_jpg = GALLERY / f"{slug}-1200w.jpg"
        if f_jpg.exists():
            old_kb = f_jpg.stat().st_size // 1024
            with Image.open(f_jpg) as im:
                im.save(f_jpg, "JPEG", quality=QUALITY, optimize=True)
            new_kb = f_jpg.stat().st_size // 1024
            if new_kb != old_kb:
                print(f"  ~ {slug}-1200w.jpg ({old_kb} -> {new_kb} KiB)")

    # Summary
    print()

    # 800w
    count_800 = len(list(GALLERY.glob("*-800w.webp")))
    size_800 = sum(f.stat().st_size for f in GALLERY.glob("*-800w.webp"))
    # 1200w WebP
    size_1200 = sum(f.stat().st_size for f in GALLERY.glob("*-1200w.webp"))
    # 400w WebP
    size_400 = sum(f.stat().st_size for f in GALLERY.glob("*-400w.webp"))

    print(f"Summary:")
    print(f"  400w WebP: {size_400//1024} KiB ({count_800} files, avg {size_400//count_800//1024 if count_800 else 0} KiB)")
    print(f"  800w WebP: {size_800//1024} KiB ({count_800} files, avg {size_800//count_800//1024 if count_800 else 0} KiB)")
    print(f"  1200w WebP: {size_1200//1024} KiB ({len(files)} files, avg {size_1200//len(files)//1024 if files else 0} KiB)")
    print(f"  Total WebP: {(size_800+size_1200+size_400)//1024} KiB")


if __name__ == "__main__":
    main()
