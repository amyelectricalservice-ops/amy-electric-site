#!/usr/bin/env python3
"""LADBS permit monitor — turn submitted electrical permits into prospects.

AE-037: pulls Electrical permits submitted in the last N days from the City of
Los Angeles open-data API, keeps the ones inside the service-area ZIPs, scores
them, writes a CSV, and (optionally) pushes them into the CRM prospect table
via POST /api/admin/prospects.

Dataset: https://data.lacity.org/resource/9k3p-zrda (submitted 2020-present)
No API key is required. Public records only — no personal contact details are
scraped; the record is the property/permit, and outreach is to the listed
address or the contractor of record.

Usage:
  python3 scripts/permit-monitor.py --days 14
  python3 scripts/permit-monitor.py --days 14 --push \
      --url https://amy-electric-site.a-m-y-electricalservice.workers.dev \
      --token "$ADMIN_TOKEN"

Never commit the token. The script refuses to run --push without one.
"""
import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = "https://data.lacity.org/resource/9k3p-zrda.json"


def service_zips():
    """ZIPs listed on service-areas.html, with a conservative fallback."""
    fallback = {
        "90001", "90002", "90003", "90004", "90005", "90006", "90007", "90008",
        "90010", "90011", "90012", "90013", "90014", "90015", "90016", "90017",
        "90018", "90019", "90020", "90021", "90024", "90025", "90026", "90027",
        "90028", "90029", "90034", "90035", "90036", "90038", "90039", "90041",
        "90042", "90045", "90046", "90048", "90049", "90064", "90065", "90066",
        "90068", "90210", "90211", "90212", "90230", "90232", "90248", "90291",
        "90292", "90401", "90402", "90403", "90404", "90405", "91001", "91006",
        "91007", "91011", "91020", "91024", "91030", "91040", "91042", "91101",
        "91103", "91104", "91105", "91106", "91107", "91108", "91201", "91202",
        "91203", "91204", "91205", "91206", "91207", "91208", "91214", "91301",
        "91302", "91303", "91304", "91305", "91306", "91307", "91311", "91316",
        "91320", "91324", "91325", "91326", "91330", "91331", "91335", "91340",
        "91342", "91343", "91344", "91345", "91352", "91356", "91360", "91361",
        "91362", "91364", "91367", "91371", "91377", "91380", "91401", "91402",
        "91403", "91405", "91406", "91411", "91423", "91436", "91501", "91502",
        "91504", "91505", "91506", "91601", "91602", "91604", "91605", "91606",
        "91607", "91608", "91610",
    }
    page = ROOT / "service-areas.html"
    if page.exists():
        found = set(re.findall(r"\b9\d{4}\b", page.read_text(encoding="utf-8", errors="ignore")))
        if len(found) > 30:
            return found
    return fallback


def fetch(where, limit=2000):
    params = {
        "$where": where,
        "$limit": str(limit),
        "$order": "submitted_date DESC",
    }
    url = DATASET + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "AMY-Electric-permit-monitor/1.0"})
    with urllib.request.urlopen(req, timeout=45) as res:
        return json.loads(res.read().decode("utf-8"))


def score(row, zips):
    text = f"{row.get('permit_sub_type','')} {row.get('work_desc','')}".lower()
    score = 30
    reasons = ["electrical permit +30"]
    if "commercial" in text:
        score += 30
        reasons.append("commercial +30")
    if re.search(r"multi[- ]?family|apartment|3 or more|condo", text):
        score += 15
        reasons.append("multi-family +15")
    if row.get("ev") in ("Y", "y", "Yes", "yes") or re.search(r"\bev\b|charger|wall connector", text):
        score += 20
        reasons.append("EV charging +20")
    if row.get("solar") in ("Y", "y", "Yes", "yes"):
        score += 5
        reasons.append("solar-adjacent +5")
    if re.search(r"panel|service upgrade|rewire|new circuits|switchgear", text):
        score += 15
        reasons.append("panel/rewire +15")
    if str(row.get("zip_code", "")) in zips:
        score += 10
        reasons.append("in service area +10")
    return min(100, score), reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--min-score", type=int, default=45)
    ap.add_argument("--out", default="seo-workspace/ads/permit-opportunities.csv")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--url", default="")
    ap.add_argument("--token", default=os.environ.get("ADMIN_TOKEN", ""))
    args = ap.parse_args()

    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%dT00:00:00")
    where = f"permit_type='Electrical' AND submitted_date > '{since}'"
    print(f"querying LADBS electrical permits since {since} …")
    try:
        rows = fetch(where)
    except (urllib.error.URLError, TimeoutError) as err:
        sys.exit(f"permit API unavailable: {err}")
    print(f"{len(rows)} raw permits")

    zips = service_zips()
    seen = set()
    out = []
    for row in rows:
        permit = str(row.get("permit_nbr") or "").strip()
        if not permit or permit in seen:
            continue
        seen.add(permit)
        s, reasons = score(row, zips)
        if s < args.min_score:
            continue
        out.append({
            "permit_ref": permit,
            "project_address": (row.get("primary_address") or "").strip(),
            "zip": str(row.get("zip_code") or ""),
            "project_type": (row.get("permit_sub_type") or "Electrical").strip(),
            "submitted_date": str(row.get("submitted_date") or "")[:10],
            "status": str(row.get("status_desc") or ""),
            "work_desc": re.sub(r"\s+", " ", str(row.get("work_desc") or ""))[:400],
            "score": s,
            "score_reasons": "; ".join(reasons),
            "segment": "commercial" if "commercial" in f"{row.get('permit_sub_type','')}".lower() else "residential",
        })
    out.sort(key=lambda r: (-r["score"], r["submitted_date"]))

    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()) if out else ["permit_ref"])
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} opportunities → {path}")

    if not args.push:
        return
    if not args.url or not args.token:
        sys.exit("--push needs --url and --token (or ADMIN_TOKEN in the environment)")
    payload = json.dumps({
        "prospects": [{
            "source": "permit-monitor",
            "permit_ref": r["permit_ref"],
            "project_address": r["project_address"],
            "zip": r["zip"],
            "project_type": r["project_type"],
            "segment": "general-contractor",
            "score": r["score"],
            "notes": f"{r['status']} · submitted {r['submitted_date']} · {r['work_desc']}",
            "city": "",
            "company": "",
        } for r in out]
    }).encode()
    req = urllib.request.Request(
        args.url.rstrip("/") + "/api/admin/prospects",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {args.token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            print("push:", res.read().decode())
    except urllib.error.HTTPError as err:
        sys.exit(f"push failed: {err.code} {err.read().decode()[:200]}")


if __name__ == "__main__":
    main()
