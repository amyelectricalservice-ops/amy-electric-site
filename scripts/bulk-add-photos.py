#!/usr/bin/env python3
"""
Bulk-add new gallery photos from source folder.
Picks best frames per project day, generates manifest entries, processes photos.
"""
import csv
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

SRC = Path("/home/amram/Pictures/Electric Work")
MANIFEST = Path(__file__).parent / "photo-manifest.csv"

# Existing slugs to avoid duplicates
existing_sources = set()
existing_slugs = set()
rows = []
if MANIFEST.exists():
    with open(MANIFEST, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            existing_sources.add(row["source_file"].strip())
            existing_slugs.add(row["slug"].strip())

MIN_YEAR = 2022  # Skip older lower-quality photos
MAX_PER_DAY = 4   # Max photos per project day

def pick_best_per_day(files):
    """Pick the best frames from a day's photos."""
    scored = []
    for fname in files:
        src_path = SRC / fname
        try:
            with Image.open(src_path) as img:
                w, h = img.size
            if w < 1500 or h < 1500:
                continue
            # Score: prefer landscape, larger files, non-HDR for cleaner look
            aspect = w / h
            aspect_score = 1.0 if abs(aspect - 1.33) < 0.3 else 0.7  # prefer ~4:3
            size_score = min(1.0, (w * h) / (4000 * 3000))
            # Prefer non-HDR
            hdr_penalty = 0.85 if "_HDR" in fname.upper() else 1.0
            file_size = src_path.stat().st_size
            total_score = aspect_score * size_score * hdr_penalty * min(1.0, file_size / 2000000)
            scored.append((total_score, fname, w, h))
        except:
            pass
    scored.sort(reverse=True)
    return [(f, w, h) for _, f, w, h in scored[:MAX_PER_DAY]]


def categorize_for_date(fname, year, month, day):
    """Heuristic category based on date and filename. User can override later."""
    name = fname.upper()
    if "HDR" in name or any(x in name for x in ['PANEL', 'METER', 'SUB']):
        return "panel"
    y, m, d = int(year), int(month), int(day)
    
    # Rough seasonal/pattern heuristics - user will fix
    if m >= 6 and m <= 8 and d >= 10:
        return "new-construction"
    if m in (3, 4, 5):
        return "lighting"
    if m in (9, 10, 11):
        return "commercial"
    if m in (12, 1, 2):
        return "other"
    return "other"


def make_slug(fname, year, month, day, idx):
    """Generate unique slug."""
    base = f"photo-{year}{month}{day}-{idx+1:02d}"
    if base not in existing_slugs:
        return base
    for n in range(2, 100):
        alt = f"{base}-v{n}"
        if alt not in existing_slugs:
            return alt
    return base


def main():
    # Group new photos by date
    by_day = defaultdict(list)
    for f in SRC.glob("*"):
        if not f.name.lower().endswith(('.jpg','.jpeg')): continue
        if f.name in existing_sources: continue
        
        m = re.search(r'(20\d{2})(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])', f.name)
        if not m: continue
        year = int(m.group(1))
        if year < MIN_YEAR: continue
        
        name = f.name.upper()
        if any(x in name for x in ['BURST', '.MP.', '.MP.JPG', '-PANTO.', '-PANTO',
                                     'EFFECTS', 'MVIMG', 'PANO', 'ANIMATION',
                                     'PORTRAIT.', 'NIGHT.', 'WA000', 'WA001']):
            continue
        
        if f.stat().st_size < 500000:  # < 500KB, likely low quality
            continue
        
        by_day[f"{m.group(1)}-{m.group(2)}-{m.group(3)}"].append(f.name)

    print(f"Found {sum(len(v) for v in by_day.values())} candidate photos in {len(by_day)} days (2022+)")

    # Process from most recent to oldest
    new_count = 0
    for date_key in sorted(by_day, reverse=True):
        year, month, day = date_key.split("-")
        files = by_day[date_key]
        picks = pick_best_per_day(files)
        
        for idx, (fname, w, h) in enumerate(picks):
            src_path = SRC / fname
            cat = categorize_for_date(fname, year, month, day)
            slug = make_slug(fname, year, month, day, idx)
            
            rows.append({
                "source_file": fname,
                "slug": slug,
                "category": cat,
                "caption": f"Electrical project photo - {year}",
                "city": "",
                "year": year,
                "custom_crop": ""
            })
            existing_sources.add(fname)
            existing_slugs.add(slug)
            new_count += 1

    # Write updated manifest
    fieldnames = ["source_file", "slug", "category", "caption", "city", "year", "custom_crop"]
    with open(MANIFEST, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Added {new_count} new entries to {MANIFEST}")
    print(f"Total manifest entries: {len(rows)}")
    return new_count


if __name__ == "__main__":
    main()
