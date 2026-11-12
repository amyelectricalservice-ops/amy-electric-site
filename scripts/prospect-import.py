#!/usr/bin/env python3
"""Import commercial prospects (GCs, property managers, architects) into the CRM.

AE-036: the prospect table is the commercial outreach list. This script takes a
CSV and POSTs it to /api/admin/prospects in batches. It never invents contacts:
blank rows are skipped and duplicate permit refs are merged by the server.

CSV columns (header required):
  company,contact_name,email,phone,city,segment,source,notes

segment: general-contractor | property-manager | architect | owner | facility
source:  manual | referral | maps | permit-monitor | association

Usage:
  python3 scripts/prospect-import.py prospects.csv \
      --url https://amy-electric-site.a-m-y-electricalservice.workers.dev \
      --token "$ADMIN_TOKEN"
  python3 scripts/prospect-import.py prospects.csv --dry-run
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

FIELDS = ["company", "contact_name", "email", "phone", "city", "segment", "source", "notes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--url", default="")
    ap.add_argument("--token", default=os.environ.get("ADMIN_TOKEN", ""))
    ap.add_argument("--batch", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.csv)
    if not path.exists():
        sys.exit(f"no such file: {path}")

    rows = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [f for f in FIELDS if f not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"missing columns: {', '.join(missing)}")
        for raw in reader:
            row = {k: (raw.get(k) or "").strip() for k in FIELDS}
            if not (row["company"] or row["contact_name"]):
                continue
            if row["email"] and "@" not in row["email"]:
                print(f"skip bad email: {row['email']}", file=sys.stderr)
                row["email"] = ""
            row["segment"] = row["segment"] or "general-contractor"
            row["source"] = row["source"] or "manual"
            rows.append(row)

    print(f"{len(rows)} usable prospects")
    if args.dry_run:
        for r in rows[:10]:
            print(json.dumps(r, ensure_ascii=False))
        return
    if not args.url or not args.token:
        sys.exit("--url and --token are required (or set ADMIN_TOKEN)")

    saved = 0
    for i in range(0, len(rows), args.batch):
        chunk = rows[i:i + args.batch]
        req = urllib.request.Request(
            args.url.rstrip("/") + "/api/admin/prospects",
            data=json.dumps({"prospects": chunk}).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {args.token}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                body = json.loads(res.read().decode())
                saved += body.get("saved", 0)
                print(f"batch {i // args.batch + 1}: saved {body.get('saved', 0)}")
        except urllib.error.HTTPError as err:
            sys.exit(f"import failed: {err.code} {err.read().decode()[:300]}")
    print(f"done — {saved} prospects saved")


if __name__ == "__main__":
    main()
