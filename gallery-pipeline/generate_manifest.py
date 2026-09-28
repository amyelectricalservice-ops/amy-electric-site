#!/usr/bin/env python3
"""Generate photo manifest CSV with descriptions and locations for all gallery images."""

import csv
import os
import random
import hashlib
from datetime import datetime
from collections import Counter

# Service descriptions keyed by category
SERVICE_DESCRIPTIONS = {
    "panel-upgrade": [
        "Main electrical panel upgrade with new 200-amp service",
        "Circuit breaker panel replacement",
        "Sub-panel installation for additional circuits",
        "Old fuse box to modern breaker panel conversion",
        "Panel grounding and bonding work",
        "New breaker installation for dedicated circuits",
        "Panel wiring and circuit organization",
        "200-amp panel upgrade for home addition",
        "Electrical panel relocation and upgrade",
        "Panel cover installation with labeled breakers",
    ],
    "ev-charger": [
        "Level 2 EV charger installation",
        "240V NEMA 14-50 outlet for EV charging",
        "Hardwired EV charging station installation",
        "Dedicated 50-amp circuit for EV charger",
        "Tesla Wall Connector installation",
        "EV charger circuit installation from panel",
        "Outdoor-rated EV charger installation",
        "Wall-mounted EV charger setup",
        "EV charging infrastructure for home",
        "EV charger with smart scheduling capability",
    ],
    "rewiring": [
        "Complete home rewiring from panel to outlets",
        "Aluminum to copper wire replacement",
        "New circuit installation for kitchen remodel",
        "Dedicated circuit for major appliances",
        "Electrical rough-in for new construction",
        "Wire routing through attic space",
        "Romex wire installation through walls",
        "Circuit extension for home office",
        "Wire management and organization",
        "Whole-home electrical wiring upgrade",
    ],
    "outlet": [
        "GFCI outlet installation in kitchen",
        "Dedicated outlet for major appliance",
        "Outdoor outlet with weatherproof cover",
        "USB outlet installation in bedroom",
        "Tamper-resistant outlet installation",
        "Outlet relocation during renovation",
        "Under-cabinet outlet installation",
        "Floor outlet installation in living room",
        "Double outlet installation in garage",
        "Outlet with integrated night light",
    ],
    "switch": [
        "Dimmer switch installation in living room",
        "Three-way switch setup for hallway",
        "Smart switch installation with app control",
        "Fan speed control switch installation",
        "Timer switch for outdoor lighting",
        "Motion sensor switch installation",
        "Master switch for whole-room lighting",
        "Double switch for separate circuits",
        "Low-voltage switch installation",
        "Switch with indicator light",
    ],
    "lighting": [
        "Recessed lighting installation in kitchen",
        "Ceiling fan with light installation",
        "Under-cabinet LED lighting setup",
        "Landscape lighting installation",
        "Pendant light installation over island",
        "Track lighting installation in workshop",
        "Wall sconce installation in hallway",
        "Chandelier installation in dining room",
        "LED strip lighting under stairs",
        "Outdoor security light installation",
    ],
    "safety": [
        "Smoke and carbon monoxide detector installation",
        "Whole-house surge protector installation",
        "GFCI protection for bathroom outlets",
        "Arc fault breaker installation for bedrooms",
        "Fire alarm system installation",
        "Emergency lighting installation",
        "Grounding system installation",
        "Lightning protection system",
        "Electrical safety inspection",
        "Code compliance upgrade",
    ],
    "generator": [
        "Whole-house generator installation",
        "Transfer switch installation for generator",
        "Portable generator hookup setup",
        "Standby generator wiring",
        "Manual transfer switch installation",
        "Generator circuit breaker installation",
        "Outdoor generator connection box",
        "Emergency power system installation",
        "Generator maintenance and testing",
        "Generator fuel line installation",
    ],
    "inspection": [
        "Electrical inspection for home sale",
        "Panel inspection and testing",
        "Code violation correction and reinspection",
        "Permit inspection preparation",
        "Electrical system assessment",
        "Safety compliance verification",
        "Insurance inspection preparation",
        "Load calculation and panel assessment",
        "Grounding and bonding verification",
        "Circuit labeling and documentation",
    ],
    "repair": [
        "Electrical troubleshooting and diagnosis",
        "Circuit breaker repair",
        "Loose connection repair in panel",
        "Flickering light repair",
        "Tripped breaker investigation",
        "Electrical outlet repair",
        "Switch malfunction repair",
        "Wire damage repair in wall",
        "Panel bus bar repair",
        "Ground fault repair",
    ],
    "residential": [
        "Residential electrical service installation",
        "Home electrical system upgrade",
        "Electrical maintenance and inspection",
        "New home electrical construction",
        "Home renovation electrical work",
        "Electrical system modernization",
        "Residential wiring for additions",
        "Home theater electrical setup",
        "Home office electrical installation",
        "General residential electrical work",
    ],
}

# LA area cities with zip codes
LA_CITIES = [
    ("Winnetka", "91306"),
    ("Encino", "91436"),
    ("Woodland Hills", "91367"),
    ("Tarzana", "91356"),
    ("Studio City", "91604"),
    ("Sherman Oaks", "91423"),
    ("Van Nuys", "91405"),
    ("North Hollywood", "91601"),
    ("Hollywood", "90028"),
    ("Beverly Hills", "90210"),
    ("West Hollywood", "90069"),
    ("Culver City", "90232"),
    ("Santa Monica", "90401"),
    ("Malibu", "90265"),
    ("Pasadena", "91101"),
    ("Glendale", "91201"),
    ("Burbank", "91502"),
    ("Northridge", "91324"),
    ("Reseda", "91335"),
    ("Canoga Park", "91303"),
    ("Chatsworth", "91311"),
    ("Granada Hills", "91344"),
    ("Mission Hills", "91345"),
    ("Sylmar", "91342"),
    ("Pacoima", "91331"),
    ("Sun Valley", "91352"),
    ("Tujunga", "91042"),
    ("La Canada Flintridge", "91011"),
    ("La Crescenta", "91214"),
    ("Altadena", "91001"),
    ("Sierra Madre", "91024"),
    ("Arcadia", "91006"),
    ("Monrovia", "91016"),
    ("Azusa", "91702"),
    ("Covina", "91722"),
    ("West Covina", "91790"),
    ("Upland", "91786"),
    ("Ontario", "91764"),
    ("Rancho Cucamonga", "91730"),
    ("Long Beach", "90802"),
    ("Torrance", "90501"),
    ("Redondo Beach", "90277"),
    ("Manhattan Beach", "90266"),
    ("Hermosa Beach", "90254"),
    ("Inglewood", "90301"),
    ("Hawthorne", "90250"),
    ("Gardena", "90247"),
    ("Carson", "90745"),
    ("Downey", "90241"),
    ("Norwalk", "90650"),
    ("Whittier", "90601"),
    ("Fullerton", "92831"),
    ("Anaheim", "92801"),
    ("Santa Ana", "92701"),
    ("Irvine", "92618"),
    ("Orange", "92866"),
    ("Costa Mesa", "92626"),
    ("Newport Beach", "92660"),
    ("Laguna Beach", "92651"),
    ("San Clemente", "92672"),
    ("Mission Viejo", "92691"),
    ("Lake Forest", "92630"),
]


def deterministic_choice(items, seed):
    """Pick from a list deterministically based on a seed string."""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return items[h % len(items)]


def extract_date(filename):
    """Try to extract a date string from the filename."""
    name = os.path.splitext(filename)[0]
    # YYYYMMDD_HHMMSS
    if len(name) >= 8 and name[:8].isdigit():
        try:
            return datetime.strptime(name[:8], "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    # IMG_YYYYMMDD...
    if name.startswith("IMG_") and len(name) >= 12 and name[4:12].isdigit():
        try:
            return datetime.strptime(name[4:12], "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    # PXL_YYYYMMDD...
    if name.startswith("PXL_") and len(name) >= 12 and name[4:12].isdigit():
        try:
            return datetime.strptime(name[4:12], "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def assign_location(filename, folder):
    """Deterministic location based on filename hash."""
    seed = filename + folder
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    city, zipcode = LA_CITIES[h % len(LA_CITIES)]
    return f"{city}, CA {zipcode}"


def assign_category_and_description(filename, folder):
    """Determine service category and description from folder + filename."""
    folder_lower = folder.lower()

    # Folder-based category
    if "panel" in folder_lower or "upgrade" in folder_lower:
        category = "panel-upgrade"
    elif "ev" in folder_lower or "charger" in folder_lower:
        category = "ev-charger"
    elif "rewire" in folder_lower:
        category = "rewiring"
    else:
        # Filename year → rotate through categories for variety
        name = os.path.splitext(filename)[0]
        year = None
        if name[:4].isdigit():
            year = name[:4]
        elif name.startswith("IMG_") and len(name) >= 8:
            year = name[4:8]
        elif name.startswith("PXL_") and len(name) >= 8:
            year = name[4:8]

        year_categories = {
            "2016": ["panel-upgrade", "rewiring"],
            "2017": ["panel-upgrade", "rewiring", "outlet", "switch", "lighting"],
            "2018": ["ev-charger", "lighting", "outlet", "safety"],
            "2019": ["rewiring", "panel-upgrade", "generator", "inspection"],
            "2020": ["ev-charger", "panel-upgrade", "lighting", "repair"],
            "2021": ["rewiring", "outlet", "switch", "safety"],
            "2022": ["panel-upgrade", "ev-charger", "lighting", "generator"],
            "2023": ["rewiring", "inspection", "repair", "safety"],
            "2024": ["ev-charger", "panel-upgrade", "lighting", "outlet"],
            "2025": ["rewiring", "generator", "inspection", "switch"],
            "2026": ["ev-charger", "panel-upgrade", "lighting", "safety"],
        }
        options = year_categories.get(year, ["residential"])
        category = deterministic_choice(options, filename)

    descriptions = SERVICE_DESCRIPTIONS.get(category, SERVICE_DESCRIPTIONS["residential"])
    description = deterministic_choice(descriptions, filename)
    return category, description


def main():
    photos = []
    base_dir = "/home/amram/Pictures/Photos-website"

    folders = [
        ("Electric Work", "residential"),
        ("Upgrade Electrical Panel Winnetka", "panel-upgrade"),
    ]

    for folder_name, default_cat in folders:
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            print(f"WARNING: {folder_path} not found, skipping")
            continue

        for fname in sorted(os.listdir(folder_path)):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            category, description = assign_category_and_description(fname, folder_name)
            location = assign_location(fname, folder_name)
            date = extract_date(fname)

            photos.append({
                "filename": fname,
                "folder": folder_name,
                "category": category,
                "description": description,
                "location": location,
                "date": date or "",
            })

    # Write CSV
    out = "/home/amram/WEBSITE/gallery-pipeline/photo_manifest.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "folder", "category", "description", "location", "date"])
        w.writeheader()
        w.writerows(photos)

    print(f"Manifest: {len(photos)} photos → {out}")

    # Stats
    cats = Counter(p["category"] for p in photos)
    print("\nCategories:")
    for c, n in cats.most_common():
        print(f"  {c}: {n}")

    locs = Counter(p["location"] for p in photos)
    print(f"\nUnique locations: {len(locs)}")
    print("\nTop 10 locations:")
    for loc, n in locs.most_common(10):
        print(f"  {loc}: {n}")

    dates = [p["date"] for p in photos if p["date"]]
    if dates:
        print(f"\nDate range: {min(dates)} to {max(dates)}")
        print(f"Photos with dates: {len(dates)}/{len(photos)}")

    # Show samples
    print("\nSample entries:")
    for p in photos[:5]:
        print(f"  {p['filename']}")
        print(f"    {p['category']} | {p['description']}")
        print(f"    {p['location']} | {p['date']}")


if __name__ == "__main__":
    main()
