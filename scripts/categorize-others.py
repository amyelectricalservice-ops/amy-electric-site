#!/usr/bin/env python3
"""Recategorize 'other' photos to 'uncategorized' with batch captions."""

import csv
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "photo-manifest.csv")

# Batch captions keyed by source_file date prefix (YYYYMMDD)
# These are grouped by date - photos from same day = same project
BATCH_CAPTIONS = {
    "20260113": "Residential panel and meter work — 2026 project",
    "20260112": "New construction rough-in — 2026 project",
    "20251217": "Commercial electrical installation — 2025 project",
    "20251215": "Service upgrade equipment — 2025 project",
    "20251212": "Conduit and wiring rough-in — 2025 project",
    "20251211": "Panel and subpanel installation — 2025 project",
    "20250207": "Residential electrical work — 2025 project",
    "20241213": "Commercial tenant improvement — 2024 project",
    "20241211": "Electrical system upgrade — 2024 project",
    "20241210": "Wiring and conduit installation — 2024 project",
    "20240709": "Service panel and meter work — 2024 project",
    "20240205": "New construction rough-in — 2024 project",
    "20230706": "Residential rewiring — 2023 project",
    "20230215": "Panel upgrade installation — 2023 project",
    "20230130": "Commercial electrical — 2023 project",
    "20230104": "Electrical system work — 2023 project",
    "20230103": "Residential electrical — 2023 project",
    "20221227": "Electrical project — 2022 year-end",
    "20220809": "Residential panel upgrade — 2022 project",
    "20220808": "Conduit and wiring — 2022 project",
    "20220804": "Electrical rough-in — 2022 project",
    "20220709": "Service upgrade — 2022 project",
    "20220708": "Panel installation — 2022 project",
    "20220707": "Wiring and connections — 2022 project",
    "20220603": "Residential new construction — 2022 project",
    "20220602": "Electrical system — 2022 project",
    "20220201": "Residential electrical — early 2022",
    "20220127": "Panel and subpanel — early 2022",
    "20220118": "Wiring installation — early 2022",
    "20220106": "Electrical rough-in — early 2022",
}

def get_date_key(source_file):
    m = re.search(r'(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])', source_file)
    return m.group(1) + m.group(2) + m.group(3) if m else None

rows = []
with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if row["category"] == "other":
            date_key = get_date_key(row["source_file"])
            batch_cap = BATCH_CAPTIONS.get(date_key, f"Electrical project — {row['year']}")
            # Keep the one pipe threading photo as equipment with its real caption
            if "pipe-threader" in row["slug"] or "pipe-threading" in row["slug"]:
                row["category"] = "equipment"
                # Caption is already good
            else:
                row["category"] = "uncategorized"
                row["caption"] = batch_cap
        rows.append(row)

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Count results
cats = {}
for r in rows:
    cats[r["category"]] = cats.get(r["category"], 0) + 1
print("New category distribution:")
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}")
