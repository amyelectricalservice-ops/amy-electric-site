#!/usr/bin/env python3
"""Apply caption/category/cull updates from a vision-pass CSV.

Usage:
  python3 scripts/apply-photo-captions.py /path/to/captions.csv

Input CSV columns:
  slug (required)
  caption (required unless action=cull)
  action (optional): caption-only | recategorize | cull  (default caption-only)
  new_category (required if action=recategorize)

Rules:
  - Every slug must already exist in scripts/photo-manifest.csv.
  - Captions 10-125 chars (matches alt_text() cap in update-gallery.py).
  - action=cull removes the row AND deletes its 4 variants (irreversible).
  - After: python3 scripts/update-gallery.py, then the pre-push gate.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "scripts" / "photo-manifest.csv"
GALLERY = ROOT / "img" / "gallery"
FIELDS = ["source_file","slug","category","caption","city","year","custom_crop"]

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: apply-photo-captions.py <captions.csv>")
    inp = Path(sys.argv[1])
    if not inp.exists():
        sys.exit(f"input not found: {inp}")

    orig = list(csv.DictReader(open(MANIFEST)))
    by_slug = {r["slug"]: r for r in orig}
    updates = list(csv.DictReader(open(inp)))
    print(f"loaded {len(updates)} update rows against {len(orig)} manifest rows")

    errors = []
    culled = set()
    for u in updates:
        slug = (u.get("slug") or "").strip()
        action = (u.get("action") or "caption-only").strip()
        if not slug or slug not in by_slug:
            errors.append(f"unknown/empty slug: {slug!r}")
            continue
        if action == "cull":
            culled.add(slug)
            for v in [f"{slug}-1200w.webp", f"{slug}-1200w.jpg", f"{slug}-800w.webp", f"{slug}-400w.webp"]:
                p = GALLERY / v
                if p.exists():
                    p.unlink()
            print(f"  CULL {slug}")
            continue
        caption = (u.get("caption") or "").strip()
        if not (10 <= len(caption) <= 125):
            errors.append(f"{slug}: caption length {len(caption)} (need 10-125)")
            continue
        by_slug[slug]["caption"] = caption
        if action == "recategorize":
            nc = (u.get("new_category") or "").strip()
            if nc:
                by_slug[slug]["category"] = nc
        print(f"  OK   {slug}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print("  ", e)
        sys.exit(1)

    kept = [by_slug[r["slug"]] for r in orig if r["slug"] not in culled]
    with open(MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(kept)
    print(f"\napplied {len(updates)-len(culled)} captions, culled {len(culled)}, manifest now {len(kept)}")

if __name__ == "__main__":
    main()
