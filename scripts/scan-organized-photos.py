#!/usr/bin/env python3
"""Scan organized/ photo tree, build inventory DB, draft manifest entries.

Usage: python3 scripts/scan-organized-photos.py

Outputs (all in data/):
  photo-inventory.json  - full file-level inventory (processed/junk/size/date)
  photo-db.sqlite       - same data as SQLite, table `photos`
  new-photos-draft.csv  - manifest-ready rows for best unprocessed 2022+ photos
                          (max 4/day by file size, junk + <500KB skipped)

Draft rows have caption "Electrical project photo - YEAR (REVIEW)": review each
image, fix category/caption/city, then append to scripts/photo-manifest.csv and run:
  python3 scripts/process-photos.py   (note: SRC must contain organized/ tree;
    either copy sources to SRC root or symlink them there by basename)
  python3 scripts/auto-caption.py     (optional: regenerate captions from pixels)
  python3 scripts/update-gallery.py
"""
from pathlib import Path
import re, csv, json, sqlite3
from collections import defaultdict, Counter

ORG = Path("/home/amram/Pictures/Electric Work/organized")
EXTRA_SOURCES = [
    Path("/home/amram/Pictures/Photos-website/Electric Work"),
    Path("/home/amram/Pictures/Photos-website/Upgrade Electrical Panel Winnetka"),
]
MANIFEST = Path(__file__).parent / "photo-manifest.csv"
DATA = Path(__file__).parent.parent / "data"

JUNK = re.compile(r"\.MP\.|BURST|PANO|MVIMG|EFFECTS|ANIMATION|PORTRAIT\.|NIGHT\.|WA00\d", re.I)
DATEP = re.compile(r"(20\d{2})(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])")
MIN_BYTES = 500000
MIN_YEAR = 2022
MAX_PER_DAY = 4


def cat_for(name, mo):
    n = name.upper()
    if any(x in n for x in ("PANEL", "METER", "SUB", "BREAKER", "ZINSCO", "FEDERAL", "SYLVANIA")):
        return "panel"
    m = int(mo)
    if m in (6, 7):
        return "new-construction"
    if m in (3, 4, 5):
        return "lighting"
    if m in (9, 10, 11):
        return "commercial"
    return "other"


def main():
    DATA.mkdir(exist_ok=True)
    with open(MANIFEST) as f:
        mrows = list(csv.DictReader(f))
    existing = set(r["source_file"].strip() for r in mrows)
    eslugs = set(r["slug"].strip() for r in mrows)

    files = [p for p in ORG.rglob("*") if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg")]
    extras = []
    for src in EXTRA_SOURCES:
        if src.is_dir():
            extras += [p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg")]
    all_seen = {p.name for p in files}
    new_extra = [p for p in extras if p.name not in all_seen]
    files += new_extra
    recs, byday = [], defaultdict(list)
    for p in files:
        try:
            sz = p.stat().st_size
        except OSError:
            sz = 0
        junk = bool(JUNK.search(p.name))
        proc = p.name in existing
        try:
            rel = p.relative_to(ORG)
            store = f"organized/{rel}"
        except ValueError:
            store = str(p)
        m = DATEP.search(p.name)
        if m:
            y, mo, d = m.group(1), m.group(2), m.group(3)
        elif re.match(r"^\d{8}$", p.parent.name):
            y, mo, d = p.parent.name[:4], p.parent.name[4:6], p.parent.name[6:8]
        else:
            y, mo, d = "unknown", "00", "00"
        recs.append({"path": store, "name": p.name,
                     "folder": p.parent.name, "date": f"{y}-{mo}-{d}" if y != "unknown" else "unknown",
                     "year": y, "bytes": sz, "processed": proc, "junk": junk})
        if not proc and not junk and sz >= MIN_BYTES and y != "unknown" and int(y) >= MIN_YEAR:
            byday[f"{y}-{mo}-{d}"].append(p)

    with open(DATA / "photo-inventory.json", "w") as f:
        json.dump({"total": len(recs), "manifest_entries": len(mrows), "records": recs}, f, indent=1)

    db = DATA / "photo-db.sqlite"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE photos(id INTEGER PRIMARY KEY, file TEXT, folder TEXT,
        date TEXT, year TEXT, bytes INTEGER, processed INTEGER, junk INTEGER,
        category TEXT, caption TEXT, city TEXT, slug TEXT)""")
    by_name = {r["source_file"].strip(): r for r in mrows}
    for r in recs:
        m = by_name.get(r["name"])
        con.execute("INSERT INTO photos VALUES (NULL,?,?,?,?,?,?,?, ?,?,?,?)",
                    (r["name"], r["folder"], r["date"], r["year"], r["bytes"],
                     int(r["processed"]), int(r["junk"]),
                     m["category"] if m else "", m["caption"] if m else "",
                     m.get("city", "") if m else "", m["slug"] if m else ""))
    con.commit()
    con.close()

    draft = []
    for dk in sorted(byday, reverse=True):
        y, mo, d = dk.split("-")
        for i, p in enumerate(sorted(byday[dk], key=lambda q: q.stat().st_size, reverse=True)[:MAX_PER_DAY]):
            base, slug, n = f"photo-{y}{mo}{d}-{i+1:02d}", f"photo-{y}{mo}{d}-{i+1:02d}", 2
            while slug in eslugs:
                slug, n = f"{base}-v{n}", n + 1
            eslugs.add(slug)
            try:
                src_ref = f"organized/{p.relative_to(ORG)}"
            except ValueError:
                src_ref = str(p)
            draft.append({"source_file": src_ref, "slug": slug,
                          "category": cat_for(p.name, mo),
                          "caption": f"Electrical project photo - {y} (REVIEW)",
                          "city": "", "year": y, "custom_crop": ""})
    with open(DATA / "new-photos-draft.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_file", "slug", "category", "caption", "city", "year", "custom_crop"])
        w.writeheader()
        w.writerows(draft)

    print(f"files={len(recs)} processed={sum(r['processed'] for r in recs)} "
          f"draft={len(draft)} days={len(byday)}")
    print(Counter(r["category"] for r in draft))
    print("wrote data/photo-inventory.json data/photo-db.sqlite data/new-photos-draft.csv")


if __name__ == "__main__":
    main()
