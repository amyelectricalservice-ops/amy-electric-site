#!/usr/bin/env python3
"""Scan local photo folders and report what's available for the website gallery.

Usage: python3 scripts/scan-local-photos.py [--src PATH] [--min-bytes N] [--min-year YYYY]

Scans the raw photo tree (default: /home/amram/Pictures/Electric Work) and reports:
  - Total image files found
  - Breakdown by subfolder, year, file type
  - Already-processed (in photo-manifest.csv) vs unprocessed
  - Junk/excluded files (bursts, panos, small files)
  - Candidate photos suitable for the gallery (large, non-junk, recent)
  - Top candidate list with paths

Does NOT modify any files. Outputs a human-readable report to stdout and
writes a JSON inventory to data/photo-scan.json.
"""
import argparse
import csv
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_SRC = "/home/amram/Pictures/Electric Work"
MANIFEST = Path(__file__).parent / "photo-manifest.csv"
DATA_DIR = Path(__file__).parent.parent / "data"

JUNK_RE = re.compile(r"\.MP\.|BURST|PANO|MVIMG|EFFECTS|ANIMATION|PORTRAIT\.|NIGHT\.|WA00\d", re.I)
DATE_RE = re.compile(r"(20\d{2})(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])")
IMG_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}


def parse_args():
    p = argparse.ArgumentParser(description="Scan local photos for website candidates")
    p.add_argument("--src", default=DEFAULT_SRC, help="Source photo folder")
    p.add_argument("--min-bytes", type=int, default=500000, help="Min file size for candidates")
    p.add_argument("--min-year", type=int, default=2022, help="Min year for candidates")
    p.add_argument("--json-out", default=None, help="JSON output path (default: data/photo-scan.json)")
    return p.parse_args()


def load_manifest():
    existing = set()
    if MANIFEST.exists():
        with open(MANIFEST) as f:
            for row in csv.DictReader(f):
                existing.add(row.get("source_file", "").strip().split("/")[-1])
    return existing


def extract_year(name, parent):
    m = DATE_RE.search(name)
    if m:
        return m.group(1)
    if re.match(r"^\d{8}$", parent):
        return parent[:4]
    return "unknown"


def scan(src, min_bytes, min_year):
    src = Path(src)
    if not src.is_dir():
        print(f"ERROR: source folder not found: {src}")
        return None

    existing = load_manifest()
    all_files = []
    for p in src.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            all_files.append(p)

    records = []
    for p in all_files:
        try:
            sz = p.stat().st_size
        except OSError:
            sz = 0
        junk = bool(JUNK_RE.search(p.name))
        processed = p.name in existing
        year = extract_year(p.name, p.parent.name)
        try:
            rel = p.relative_to(src)
            rel_str = str(rel)
        except ValueError:
            rel_str = str(p)
        candidate = (
            not processed
            and not junk
            and sz >= min_bytes
            and year != "unknown"
            and int(year) >= min_year
        )
        records.append({
            "name": p.name,
            "path": rel_str,
            "folder": p.parent.name,
            "year": year,
            "bytes": sz,
            "junk": junk,
            "processed": processed,
            "candidate": candidate,
        })

    return records, existing


def report(records, src, min_bytes, min_year):
    total = len(records)
    processed = sum(1 for r in records if r["processed"])
    junk = sum(1 for r in records if r["junk"])
    candidates = [r for r in records if r["candidate"]]
    by_year = Counter(r["year"] for r in records)
    by_folder = Counter(r["folder"] for r in records)
    by_ext = Counter(Path(r["name"]).suffix.lower() for r in records)

    print("=" * 70)
    print(f"PHOTO SCAN REPORT — {src}")
    print("=" * 70)
    print(f"Total image files:        {total}")
    print(f"Already processed:        {processed}  (in photo-manifest.csv)")
    print(f"Junk/excluded:            {junk}  (bursts, panos, small)")
    print(f"Candidates (>= {min_bytes//1000}KB, >= {min_year}, non-junk, unprocessed): {len(candidates)}")
    print()

    print("By year:")
    for y in sorted(by_year, reverse=True):
        c = sum(1 for r in records if r["year"] == y and r["candidate"])
        print(f"  {y}: {by_year[y]:>5} total  ({c} candidates)")
    print()

    print("By file type:")
    for ext, n in by_ext.most_common():
        print(f"  {ext}: {n}")
    print()

    print("Top folders by count:")
    for folder, n in by_folder.most_common(15):
        c = sum(1 for r in records if r["folder"] == folder and r["candidate"])
        print(f"  {folder}: {n} files ({c} candidates)")
    print()

    if candidates:
        print(f"Top {min(30, len(candidates))} candidates (largest first):")
        for r in sorted(candidates, key=lambda x: -x["bytes"])[:30]:
            print(f"  {r['bytes']//1024:>6}KB  {r['year']}  {r['path']}")
    else:
        print("No candidates found. Try lowering --min-bytes or --min-year.")
    print()
    print(f"Full inventory written to data/photo-scan.json")


def main():
    args = parse_args()
    result = scan(args.src, args.min_bytes, args.min_year)
    if result is None:
        return
    records, existing = result
    report(records, args.src, args.min_bytes, args.min_year)

    out = Path(args.json_out) if args.json_out else DATA_DIR / "photo-scan.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"source": args.src, "total": len(records),
                   "processed": sum(1 for r in records if r["processed"]),
                   "junk": sum(1 for r in records if r["junk"]),
                   "candidates": sum(1 for r in records if r["candidate"]),
                   "records": records}, f, indent=1)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()