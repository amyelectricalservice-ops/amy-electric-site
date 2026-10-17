#!/usr/bin/env python3
"""Build a labeled contact sheet of pending photo candidates for fast review.

One image read of a 6x4 grid = 24 candidate groups triaged at once, instead of
24 separate reads. Cell label = index into the returned manifest printed on
stdout; log verdicts with triage-photos.py skip / pick.

Usage:
  python3 scripts/contact-sheet.py --day 20220708            # one shoot day
  python3 scripts/contact-sheet.py --n 24                    # next N pending
  python3 scripts/contact-sheet.py --day 20220708 --cols 6 --cell 320
"""
import argparse
import csv
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent.parent
GROUPS_JSON = Path(os.environ.get("TRIAGE_JSON", "/tmp/opencode/triage.json"))
LOG = ROOT / "scripts" / "photo-review-log.csv"
OUT = Path(os.environ.get("SHEET_DIR", "/tmp/opencode/sheets"))


def load_verdicts():
    if not LOG.exists():
        return set()
    with open(LOG) as f:
        return {r["file"] for r in csv.DictReader(f) if r.get("file")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", help="only this shoot day (YYYYMMDD)")
    ap.add_argument("--n", type=int, default=24, help="max groups on the sheet")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--cell", type=int, default=300)
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()

    groups = json.load(open(GROUPS_JSON))["groups"]
    verd = load_verdicts()
    sel = [g for g in groups
           if os.path.basename(g["items"][0]["p"]) not in verd
           and (not args.day or g["day"] == args.day)]
    sel = sel[args.offset:args.offset + args.n]
    if not sel:
        print("no pending groups match")
        return

    cols, cell = args.cols, args.cell
    rows = (len(sel) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 20)), "white")
    dr = ImageDraw.Draw(sheet)
    manifest = []
    for i, g in enumerate(sel):
        p = g["items"][0]["p"]
        r, c = divmod(i, cols)
        x, y = c * cell, r * (cell + 20)
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((cell, cell))
            sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        except Exception:
            dr.rectangle([x, y, x + cell, y + cell], fill="#eee")
        bn = os.path.basename(p)
        dr.rectangle([x, y + cell, x + cell, y + cell + 20], fill="black")
        dr.text((x + 4, y + cell + 5), f"[{i}] {bn[:26]}", fill="white")
        manifest.append((i, bn, g["day"]))

    OUT.mkdir(parents=True, exist_ok=True)
    tag = args.day or f"n{len(sel)}"
    out = OUT / f"sheet-{tag}-{args.offset}.jpg"
    sheet.save(out, quality=82)
    print(f"sheet: {out}  ({len(sel)} groups, {sheet.size[0]}x{sheet.size[1]})")
    for i, bn, day in manifest:
        print(f"  [{i}] {day} {bn}")


if __name__ == "__main__":
    main()
