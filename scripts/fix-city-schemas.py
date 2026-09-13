#!/usr/bin/env python3
"""Fix 87 city page schema issues: missing BreadcrumbList + missing Electrician credentials."""

import json
import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CREDENTIALS = [
    {"name": "C-10 Electrical Contractor License #981578"},
    {"name": "EVITP Certification #4051604"},
]

FOUNDER_CREDENTIALS = [
    {
        "@type": "EducationalOccupationalCredential",
        "name": "California C-10 Electrical Contractor License #981578",
        "url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578",
    },
    {
        "@type": "EducationalOccupationalCredential",
        "name": "EVITP Certification #4051604",
    },
]


def city_name_from_slug(slug):
    stem = slug.replace(".html", "").replace("city-", "")
    return stem.replace("-", " ").title()


def make_breadcrumb(city_name):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://amyelectric.com/"},
            {"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://amyelectric.com/city-los-angeles"},
            {"@type": "ListItem", "position": 3, "name": city_name, "item": f"https://amyelectric.com/city-{city_name.lower().replace(' ', '-')}"},
        ],
    }, ensure_ascii=False)


def find_all_jsonld(html):
    results = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
        block = m.group(1).strip()
        try:
            data = json.loads(block)
            results.append((m.start(), m.end(), data, block))
        except json.JSONDecodeError:
            pass
    return results


def fix_file(rel_path):
    abs_path = os.path.join(SITE_DIR, rel_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        html = f.read()

    city = city_name_from_slug(rel_path)
    changed = False
    blocks = find_all_jsonld(html)

    # Fix 1: Add hasCredential to Electrician if missing
    for start, end, data, raw in blocks:
        elec = None
        if isinstance(data, dict) and data.get("@type") == "Electrician":
            elec = data
        if isinstance(data, dict) and "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict) and item.get("@type") == "Electrician":
                    elec = item
        if elec and "hasCredential" not in elec:
            elec["hasCredential"] = CREDENTIALS
            if "founder" in elec and isinstance(elec["founder"], dict):
                elec["founder"]["hasCredential"] = FOUNDER_CREDENTIALS
            new_json = json.dumps(data, ensure_ascii=False, indent=2)
            old_tag = html[start:end]
            new_tag = re.sub(
                r'(<script type="application/ld\+json">).*?(</script>)',
                lambda m: m.group(1) + "\n" + new_json + "\n" + m.group(2),
                old_tag,
                count=1,
                flags=re.DOTALL,
            )
            html = html[:start] + new_tag + html[end:]
            changed = True
            print(f"  + Added hasCredential: {rel_path}")
            break

    # Fix 2: Add BreadcrumbList if missing
    blocks = find_all_jsonld(html)
    has_breadcrumb = False
    for _, _, data, _ in blocks:
        if isinstance(data, dict) and data.get("@type") == "BreadcrumbList":
            has_breadcrumb = True
        if isinstance(data, dict) and "@graph" in data:
            for item in data["@graph"]:
                if isinstance(item, dict) and item.get("@type") == "BreadcrumbList":
                    has_breadcrumb = True

    if not has_breadcrumb:
        breadcrumb_json = make_breadcrumb(city)
        breadcrumb_tag = f'\n<script type="application/ld+json">\n{breadcrumb_json}\n</script>\n'
        insert_point = re.search(r'</head>', html, re.IGNORECASE)
        if insert_point:
            html = html[: insert_point.start()] + breadcrumb_tag + html[insert_point.start() :]
            changed = True
            print(f"  + Added BreadcrumbList: {rel_path}")

    if changed:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(html)

    return changed


def main():
    issues = 0
    fixed = 0
    for fname in sorted(os.listdir(SITE_DIR)):
        if not fname.startswith("city-") or not fname.endswith(".html"):
            continue
        abs_path = os.path.join(SITE_DIR, fname)
        with open(abs_path, "r", encoding="utf-8") as f:
            html = f.read()

        blocks = find_all_jsonld(html)
        has_credential = False
        has_breadcrumb = False
        is_electrician = False

        for _, _, data, _ in blocks:
            types = set()
            if isinstance(data, dict):
                types.add(data.get("@type"))
                if "@graph" in data:
                    for item in data["@graph"]:
                        if isinstance(item, dict):
                            types.add(item.get("@type"))
            if "Electrician" in types:
                is_electrician = True
            if "BreadcrumbList" in types:
                has_breadcrumb = True

        if is_electrician:
            for _, _, data, _ in blocks:
                elec = None
                if isinstance(data, dict) and data.get("@type") == "Electrician":
                    elec = data
                if isinstance(data, dict) and "@graph" in data:
                    for item in data["@graph"]:
                        if isinstance(item, dict) and item.get("@type") == "Electrician":
                            elec = item
                if elec and "hasCredential" in elec:
                    has_credential = True

        needs_fix = (is_electrician and not has_credential) or not has_breadcrumb
        if needs_fix:
            issues += 1
            if fix_file(fname):
                fixed += 1

    print(f"\nScanned city pages: {issues} with issues, {fixed} fixed")
    return 0 if issues == fixed else 1


if __name__ == "__main__":
    sys.exit(main())
