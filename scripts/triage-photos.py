#!/usr/bin/env python3
"""Bulk triage for the photo backlog: dedupe + score + stage candidates.

The gallery bar is high (finished work, upright, no PII). Most of the
1,200+ file backlog is burst-mode duplicates and near-identical framings,
so this script collapses same-day near-duplicates into groups, scores each
group's best shot (sharpness + exposure + resolution), and stages the top
candidates for human review.

Usage:
  python3 scripts/triage-photos.py stage --n 36   # stage top candidates
  python3 scripts/triage-photos.py skip IMG_a.jpg IMG_b.jpg "reason"
  python3 scripts/triage-photos.py pending         # how many remain

Review state lives in scripts/photo-review-log.csv (one row per staged
file, verdict=skip/pick) so batches survive across sessions: `stage` never
re-stages a file that already has a verdict. Picks graduate to
scripts/photo-manifest.csv (use the source_file basename).
"""
import argparse
import csv
import json
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image
import numpy as np

ROOT = Path(__file__).parent.parent
PHOTOS = Path(os.environ.get("PHOTOS_SRC", "/home/amram/Pictures/Electric Work"))
STAGE = Path(os.environ.get("TRIAGE_STAGE", "/tmp/opencode/review-all"))
LOG = ROOT / "scripts" / "photo-review-log.csv"
MANIFEST = ROOT / "scripts" / "photo-manifest.csv"
GROUPS_JSON = Path(os.environ.get("TRIAGE_JSON", "/tmp/opencode/triage.json"))
HASH_MAX = 10  # dHash hamming distance treated as near-duplicate


def load_used():
    used = set()
    with open(MANIFEST) as f:
        for row in csv.DictReader(f):
            used.add(os.path.basename(row["source_file"].strip()))
    return used


def load_verdicts():
    if not LOG.exists():
        return {}
    with open(LOG) as f:
        return {row["file"]: row["verdict"] for row in csv.DictReader(f) if row.get("file")}


def walk_unused():
    used = load_used()
    files = []
    for dp, _, fns in os.walk(PHOTOS):
        for fn in fns:
            if fn.lower().endswith((".jpg", ".jpeg", ".png")):
                p = os.path.join(dp, fn)
                if fn not in used:
                    files.append(p)
    return sorted(files)


def daykey(path):
    bn = os.path.basename(path)
    for pre in ("IMG_", "PXL_", "MVIMG_"):
        if bn.startswith(pre) and len(bn) > len(pre) + 8:
            return bn[len(pre):len(pre) + 8]
    if len(bn) >= 8 and bn[:8].isdigit():
        return bn[:8]
    return "other"


def dhash(im):
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    px = np.asarray(g, dtype=np.int16)
    diff = px[:, 1:] > px[:, :-1]
    h = 0
    for b in diff.flat:
        h = (h << 1) | int(b)
    return h


def quality(im):
    g = im.convert("L").resize((256, 256), Image.BILINEAR)
    a = np.asarray(g, dtype=np.float32)
    lap = (a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:] - 4 * a[1:-1, 1:-1])
    w, h = im.size
    return float(lap.var()), float(a.mean()), w * h / 1e6


def build_groups():
    recs = []
    for p in walk_unused():
        try:
            with Image.open(p) as im:
                im.load()
                recs.append({"p": p, "day": daykey(p), "hash": dhash(im),
                             "sharp": quality(im)[0], "bright": quality(im)[1],
                             "mp": quality(im)[2]})
        except Exception as e:
            recs.append({"p": p, "day": daykey(p), "hash": None, "err": str(e)[:60]})

    groups, byday = [], defaultdict(list)
    for r in recs:
        byday[r["day"]].append(r)
    for day, items in byday.items():
        hashed = [r for r in items if r.get("hash") is not None]
        seen = set()
        for i, r in enumerate(hashed):
            if i in seen:
                continue
            g = [r]
            seen.add(i)
            for j in range(i + 1, len(hashed)):
                if j in seen:
                    continue
                if bin(r["hash"] ^ hashed[j]["hash"]).count("1") <= HASH_MAX:
                    g.append(hashed[j])
                    seen.add(j)
            groups.append({"day": day, "items": g})
        for r in items:
            if r.get("hash") is None:
                groups.append({"day": day, "items": [r]})
    return groups


def score_groups(groups, recs):
    sharp_sorted = sorted(r["sharp"] for r in recs if "err" not in r)
    import bisect

    def sharp_pct(v):
        return bisect.bisect_left(sharp_sorted, v) / len(sharp_sorted)

    kept = []
    auto = Counter()
    for g in groups:
        best = g["items"][0]
        if "err" in best:
            auto["unreadable"] += len(g["items"])
            continue
        if best["mp"] < 2.0:
            auto["tiny<2MP"] += len(g["items"])
            continue
        if best["bright"] < 35:
            auto["near-black"] += len(g["items"])
            continue
        if best["bright"] > 225:
            auto["blown-out"] += len(g["items"])
            continue
        bexp = 1.0 - min(1.0, abs(best["bright"] - 110) / 110)
        sc = 0.55 * sharp_pct(best["sharp"]) + 0.3 * bexp + 0.15 * min(1.0, best["mp"] / 12.0)
        kept.append((round(sc, 3), g))
    kept.sort(key=lambda x: -x[0])
    return kept, auto


def cmd_stage(args):
    STAGE.mkdir(parents=True, exist_ok=True)
    verdicts = load_verdicts()
    groups = build_groups()
    kept, auto = score_groups(groups, [r for g in groups for r in g["items"]])
    print(f"groups={len(groups)} candidates={len(kept)} auto-skipped={dict(auto)}")
    perday, staged = Counter(), 0
    for sc, g in kept:
        if staged >= args.n:
            break
        best = g["items"][0]
        bn = os.path.basename(best["p"])
        if bn in verdicts or perday[g["day"]] >= 3:
            continue
        perday[g["day"]] += 1
        shutil.copy(best["p"], STAGE / f"{g['day']}__{bn}")
        staged += 1
        print(f"  {sc:.2f} {g['day']} x{len(g['items'])} {bn}")
    print(f"staged {staged} -> {STAGE}")
    json.dump({"groups": groups, "kept": [[sc, g["day"], os.path.basename(g["items"][0]["p"])]
                                          for sc, g in kept]},
              open(GROUPS_JSON, "w"))


def log_rows():
    if not LOG.exists():
        return []
    with open(LOG) as f:
        return list(csv.DictReader(f))


def cmd_skip(args):
    rows = log_rows()
    have = {r["file"] for r in rows}
    with open(LOG, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "verdict", "note"])
        if not have:
            w.writeheader()
        for bn in args.files:
            if bn not in have:
                w.writerow({"file": bn, "verdict": "skip", "note": args.note})
                print("logged skip:", bn)
            else:
                print("already logged:", bn)


def cmd_pending(args):
    verdicts = load_verdicts()
    groups = build_groups()
    kept, _ = score_groups(groups, [r for g in groups for r in g["items"]])
    pend = [g for sc, g in kept if os.path.basename(g["items"][0]["p"]) not in verdicts]
    print(f"pending candidate groups: {len(pend)} (of {len(kept)} scored; "
          f"{len(verdicts)} verdicts logged; {len(groups)} total groups)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stage", help="stage top unreviewed candidates for review")
    s.add_argument("--n", type=int, default=36)
    s.set_defaults(fn=cmd_stage)
    k = sub.add_parser("skip", help="log reviewed files as skipped")
    k.add_argument("files", nargs="+")
    k.add_argument("--note", default="")
    k.set_defaults(fn=cmd_skip)
    p = sub.add_parser("pending", help="count unreviewed candidate groups")
    p.set_defaults(fn=cmd_pending)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
