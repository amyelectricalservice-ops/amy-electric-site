#!/usr/bin/env python3
"""
Auto-caption all 309 gallery photos using PIL + numpy image analysis.
Generates descriptive captions based on brightness, color, edges, and texture.
"""

import csv
import os
import re
import numpy as np
from PIL import Image, ImageFilter, ImageStat

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(SCRIPT_DIR, "photo-manifest.csv")
GALLERY_DIR = os.path.join(BASE_DIR, "img", "gallery")


def analyze_image(filepath):
    """Analyze an image and return descriptive features."""
    img = Image.open(filepath).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    h, w, _ = arr.shape

    # Basic stats
    gray = np.mean(arr, axis=2)
    brightness = np.mean(gray)
    brightness_std = np.std(gray)

    # Edge density (using PIL FIND_EDGES)
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_arr = np.array(edges, dtype=np.float32)
    edge_density = np.mean(edge_arr) / 255.0

    # Color analysis
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # White/beige/light wall detection (R>200, G>200, B>200)
    is_white = (r > 200) & (g > 200) & (b > 200)
    white_pct = np.mean(is_white)

    # Gray/metal detection (R,G,B close together, medium range)
    diff_rg = np.abs(r - g)
    diff_rb = np.abs(r - b)
    diff_gb = np.abs(g - b)
    max_diff = np.maximum(np.maximum(diff_rg, diff_rb), diff_gb)
    is_gray = (max_diff < 30) & (r > 60) & (r < 220)
    gray_pct = np.mean(is_gray)

    # Blue (sky) detection
    is_blue = (b > 1.2 * r) & (b > 1.2 * g) & (b > 80)
    blue_pct = np.mean(is_blue)

    # Green (trees/plants) detection
    is_green = (g > 1.15 * r) & (g > 1.1 * b) & (g > 60)
    green_pct = np.mean(is_green)

    # Brown/wood detection
    is_brown = (r > g) & (g > b) & (r > 80) & (r < 200)
    brown_pct = np.mean(is_brown)

    # Yellow/brass (copper, wire, brass fittings)
    is_yellow = (r > g * 1.1) & (g > b * 1.1) & (r > 100)
    yellow_pct = np.mean(is_yellow)

    # Dark area detection (shadows, dark equipment)
    is_dark = gray < 50
    dark_pct = np.mean(is_dark)

    # Blue sky in top portion (outdoor indicator)
    top_third = arr[:h//3, :, :]
    top_b = top_third[:, :, 2]
    top_r = top_third[:, :, 0]
    top_g = top_third[:, :, 1]
    is_top_blue = (top_b > 1.3 * top_r) & (top_b > 1.3 * top_g) & (top_b > 80)
    top_blue_pct = np.mean(is_top_blue)

    # Warmth index (red vs blue balance)
    warmth = np.mean(r) / (np.mean(b) + 1)

    # Color variance (how many distinct colors)
    color_var = np.mean(np.std(arr, axis=(0, 1)))

    # Saturation
    max_rgb = np.maximum(np.maximum(r, g), b)
    min_rgb = np.minimum(np.minimum(r, g), b)
    saturation = np.mean((max_rgb - min_rgb) / (max_rgb + 1))

    # Aspect ratio
    aspect = w / h

    return {
        "brightness": float(brightness),
        "brightness_std": float(brightness_std),
        "edge_density": float(edge_density),
        "white_pct": float(white_pct),
        "gray_pct": float(gray_pct),
        "blue_pct": float(blue_pct),
        "green_pct": float(green_pct),
        "brown_pct": float(brown_pct),
        "yellow_pct": float(yellow_pct),
        "dark_pct": float(dark_pct),
        "top_blue_pct": float(top_blue_pct),
        "warmth": float(warmth),
        "color_var": float(color_var),
        "saturation": float(saturation),
        "aspect": float(aspect),
        "height": h,
        "width": w,
    }


def classify_scene(f):
    """Classify scene type from image features."""
    # Outdoor detection
    is_outdoor = f["top_blue_pct"] > 0.05 or (f["brightness"] > 180 and f["blue_pct"] > 0.02 and f["saturation"] > 0.12)
    is_very_bright = f["brightness"] > 200

    # Texture complexity
    is_complex = f["edge_density"] > 0.06
    is_simple = f["edge_density"] < 0.025

    # Panel-like: lots of gray, high edges, medium brightness
    is_panel_like = f["gray_pct"] > 0.25 and f["edge_density"] > 0.04

    # Wiring-like: complex edges, warm tones (copper), some brown/yellow
    is_wiring_like = f["edge_density"] > 0.05 and (f["yellow_pct"] > 0.02 or f["brown_pct"] > 0.03)

    # Close-up
    is_closeup = f["aspect"] < 1.3 and f["edge_density"] > 0.05

    # Dark/indoor
    is_indoor = f["brightness"] < 140 and f["top_blue_pct"] < 0.01

    # Conduit/commercial: lots of gray, complex edges, medium-high brightness
    is_conduit = f["gray_pct"] > 0.20 and f["edge_density"] > 0.05 and f["brightness"] > 100

    return {
        "outdoor": is_outdoor,
        "indoor": is_indoor,
        "bright": is_very_bright,
        "complex": is_complex,
        "simple": is_simple,
        "panel_like": is_panel_like,
        "wiring_like": is_wiring_like,
        "closeup": is_closeup,
        "conduit": is_conduit,
    }


def generate_caption(f, scene, slug, category, year):
    """Generate a descriptive caption from image features."""
    # Detect scene elements
    elements = []

    # Background type
    if scene["outdoor"]:
        if f["blue_pct"] > 0.15 and f["green_pct"] > 0.05:
            elements.append("Outdoor electrical work against sky and landscaping")
        elif f["top_blue_pct"] > 0.05:
            elements.append("Exterior electrical installation with blue sky backdrop")
        else:
            elements.append("Outdoor electrical service equipment")
    elif scene["indoor"]:
        if f["white_pct"] > 0.35:
            if scene["panel_like"]:
                elements.append("Electrical panel against white wall")
            elif f["brown_pct"] > 0.05:
                elements.append("Wiring work in interior wall cavity")
            else:
                elements.append("Interior electrical work on light-colored wall")
        elif f["dark_pct"] > 0.30:
            elements.append("Electrical equipment in dimly lit area")
        elif f["brown_pct"] > 0.10:
            elements.append("Electrical work in unfinished wood-framed space")
        elif f["gray_pct"] > 0.20:
            elements.append("Indoor electrical installation with metal components")
        else:
            elements.append("Interior electrical work")
    else:
        # Mixed/transitional
        if f["brightness"] > 180:
            elements.append("Brightly lit electrical installation")
        elif f["gray_pct"] > 0.20:
            elements.append("Electrical system with metal enclosures")
        else:
            elements.append("Electrical project work")

    # Specific feature detection
    if scene["panel_like"] and scene["complex"]:
        elements.append("with panel and wiring detail")
    elif scene["wiring_like"] and scene["complex"]:
        elements.append("showing color-coded wiring and connections")
    elif scene["panel_like"]:
        elements.append("featuring electrical panel enclosure")
    elif scene["conduit"] and scene["complex"]:
        elements.append("with conduit and raceway runs")
    elif scene["simple"] and f["white_pct"] > 0.40:
        elements.append("on finished wall surface")
    elif scene["closeup"]:
        elements.append("close-up of electrical components")
    elif f["yellow_pct"] > 0.03:
        elements.append("with copper wiring and terminals visible")
    elif f["green_pct"] > 0.10 and scene["outdoor"]:
        elements.append("with landscaping around equipment")

    # Quality indicator
    if f["brightness_std"] > 60 and scene["complex"]:
        quality = "detailed installation view"
    elif f["brightness_std"] < 30 and f["brightness"] > 150:
        quality = "evenly lit workspace"
    else:
        quality = "work in progress"

    # Build caption
    base = " — ".join(elements) if elements else f"Electrical project — {year}"
    caption = f"{base} ({quality})"

    # Trim if too long
    if len(caption) > 140:
        caption = caption[:137] + "..."

    return caption


def main():
    rows = []
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    total = len(rows)
    # Find the 1200w JPEG for best analysis (full color, largest)
    updated = 0
    for i, row in enumerate(rows):
        # Try 1200w JPEG first, fallback to 1200w WebP, then to 400w
        candidates = [
            os.path.join(GALLERY_DIR, f"{row['slug']}-1200w.jpg"),
            os.path.join(GALLERY_DIR, f"{row['slug']}-1200w.webp"),
        ]
        img_path = None
        for c in candidates:
            if os.path.exists(c):
                img_path = c
                break

        if img_path is None:
            print(f"  SKIP {i+2}: {row['slug']} — no image found")
            continue

        try:
            feat = analyze_image(img_path)
            scene = classify_scene(feat)
            caption = generate_caption(feat, scene, row["slug"], row["category"], row["year"])
            row["caption"] = caption
            updated += 1

            if i < 5 or (i+1) % 50 == 0 or i == total - 1:
                print(f"  [{i+2}/{total+1}] {row['slug']}: {caption}")
        except Exception as e:
            print(f"  ERROR {i+2}: {row['slug']} — {e}")

    # Write back
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone — {updated}/{total} photos captioned.")


if __name__ == "__main__":
    main()
