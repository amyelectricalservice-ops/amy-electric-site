#!/usr/bin/env python3
"""
Batch updates for AMY Electric site:
1. City FAQ: 3→5 questions (add 2 new Qs) on all 16 city pages
2. Fix blog title duplicate with service page
3. Remove datePublished/dateModified from Service schema (17 pages)
"""

import json
import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─── City name mappings ───────────────────────────────────────────────
# file_stem -> (city_name_for_questions, utility_office_name)
CITY_MAP = {
    "city-los-angeles":       ("Los Angeles",       "LADWP"),
    "city-sherman-oaks":      ("Sherman Oaks",      "LADWP"),
    "city-burbank":           ("Burbank",           "Burbank Water and Power"),
    "city-glendale":          ("Glendale",          "Glendale Water & Power"),
    "city-pasadena":          ("Pasadena",          "Pasadena Water and Power"),
    "city-studio-city":       ("Studio City",       "LADWP"),
    "city-north-hollywood":   ("North Hollywood",   "LADWP"),
    "city-hollywood":         ("Hollywood",         "LADWP"),
    "city-beverly-hills":     ("Beverly Hills",     "Southern California Edison"),
    "city-west-la":           ("West Los Angeles",  "LADWP"),
    "city-encino":            ("Encino",            "LADWP"),
    "city-santa-monica":      ("Santa Monica",      "Southern California Edison"),
    "city-van-nuys":          ("Van Nuys",          "LADWP"),
    "city-woodland-hills":    ("Woodland Hills",    "LADWP"),
    "city-calabasas":         ("Calabasas",         "LADWP"),
    "city-culver-city":       ("Culver City",       "Southern California Edison"),
}

# ─── Services affected by datePublished/dateModified cleanup ─────────
SERVICE_PAGES = [
    "ceiling-fan-installation.html",
    "dedicated-circuits.html",
    "electrical-repair.html",
    "electrical-safety-inspections.html",
    "generator-transfer-switch.html",
    "lighting-installation.html",
    "outlet-switch-installation.html",
    "smart-home-electrical.html",
    "smoke-co-detector-installation.html",
    "surge-protection.html",
    "tesla-charger-installation.html",
    "whole-home-rewiring.html",
    "panel-upgrade.html",
    "ev-charger-installation.html",
    "commercial-electrical.html",
    "panel-100a-vs-200a.html",
    "ev-charger-hardwired-vs-plug-in.html",
]

# ─── New FAQ questions ────────────────────────────────────────────────
def get_new_faqs(city):
    return [
        {
            "q": f"Are you licensed and insured to work in {city}?",
            "a": f"Yes — AMY Electric is a licensed California C-10 electrical contractor (#981578) and EVITP-certified (#4051604). We carry full general liability insurance and workers' compensation insurance. Our license is active and in good standing with the CSLB, and we pull all required permits for every job in {city}. You can verify our license anytime at the California Contractors State License Board website."
        },
        {
            "q": f"Do you offer free estimates for electrical work in {city}?",
            "a": f"Yes — we provide free, no-obligation estimates for all electrical work in {city}. Whether you need a panel upgrade, EV charger installation, home rewiring, or commercial electrical service, we'll come out, assess the job, and provide a detailed written estimate. Call (818) 302-5614 or use our online form to schedule yours."
        },
    ]


def expand_city_faqs():
    """Add 2 new FAQ Qs to each city page (HTML + JSON-LD)."""
    for stem, (city, utility) in sorted(CITY_MAP.items()):
        path = os.path.join(SITE_DIR, f"{stem}.html")
        if not os.path.exists(path):
            print(f"  SKIP {stem}.html (not found)")
            continue

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        new_faqs = get_new_faqs(city)

        # ── 1. HTML FAQ section ──
        # Find the last </details> in the faq-list, insert before </div> that closes it
        html_faq_blocks = ""
        for faq in new_faqs:
            html_faq_blocks += f'\n    <details class="faq-item"><summary class="faq-q">{faq["q"]} <span class="faq-chevron">▾</span></summary><div class="faq-a">{faq["a"]}</div></details>'

        # Insert before the closing </div> of faq-list
        pattern_html = r'(</details>\s*</div>\s*<div style="margin-top:40px;">)'
        replacement_html = f'</details>{html_faq_blocks}\n  </div>\n  <div style="margin-top:40px;">'
        
        # Simpler approach: replace the first </details> that's followed by </div> then margin
        old = '</details>\n  </div>\n  <div style="margin-top:40px;">'
        new = f'</details>{html_faq_blocks}\n  </div>\n  <div style="margin-top:40px;">'
        
        if old not in html:
            # Try with different whitespace patterns
            import re
            match = re.search(r'(</details>)\s*(</div>\s*<div style="margin-top:40px;">)', html)
            if match:
                old_raw = match.group(0)
                new_raw = f'</details>{html_faq_blocks}\n  {match.group(2)}'
                html = html.replace(old_raw, new_raw, 1)
                print(f"  {stem}.html: HTML FAQ regex-matched")
            else:
                print(f"  FAIL {stem}.html: could not find HTML FAQ insertion point")
                continue
        else:
            html = html.replace(old, new, 1)
            print(f"  {stem}.html: HTML FAQ inserted")

        # ── 2. JSON-LD FAQPage ──
        # Find the FAQPage JSON-LD block and add entries
        # Pattern: ...}]}</script> at end of FAQPage
        jsonld_blocks = []
        for faq in new_faqs:
            entry = json.dumps({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}}, ensure_ascii=False)
            jsonld_blocks.append(entry)

        new_entries = ", " + ", ".join(jsonld_blocks)
        
        # Insert before ]} in FAQPage JSON-LD
        # The FAQPage ends with: ...}]}</script>
        old_json = '}]}</script>'
        new_json = f'{new_entries}]}}</script>'
        
        if old_json in html:
            html = html.replace(old_json, new_json, 1)
            print(f"  {stem}.html: JSON-LD FAQ inserted")
        else:
            print(f"  FAIL {stem}.html: could not find JSON-LD FAQ insertion point")
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    print("City FAQ expansion complete.")


def fix_blog_title():
    """Fix duplicate blog title to differentiate from service page."""
    path = os.path.join(SITE_DIR, "blog", "smoke-co-detector-installation-la.html")
    if not os.path.exists(path):
        print("  SKIP blog/smoke-co-detector-installation-la.html (not found)")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Fix title
    old_title = '<title>Smoke & CO Detector Installation Los Angeles | AMY</title>'
    new_title = '<title>Smoke & CO Detector Installation Guide — LA Code & Costs | AMY</title>'
    if old_title in html:
        html = html.replace(old_title, new_title)
        print("  blog: title fixed")
    else:
        print("  FAIL blog: title not found")
        # Try escaped
        old_title_esc = '<title>Smoke &amp; CO Detector Installation Los Angeles | AMY</title>'
        if old_title_esc in html:
            html = html.replace(old_title_esc, new_title)
            print("  blog: title fixed (escaped)")

    # Fix OG title
    old_og = '<meta property="og:title" content="Smoke &amp; CO Detector Installation Los Angeles | AMY Electric">'
    new_og = '<meta property="og:title" content="Smoke &amp; CO Detector Installation Guide &amp; Costs | AMY Electric">'
    if old_og in html:
        html = html.replace(old_og, new_og)
        print("  blog: OG title fixed")

    # Fix description (add "costs")
    old_desc = '<meta name="description" content="Complete guide to smoke and carbon monoxide detector installation in Los Angeles. California code requirements & what homeowners. Call (818) 302-5614.">'
    new_desc = '<meta name="description" content="Complete guide to smoke and carbon monoxide detector installation in Los Angeles. California code requirements, costs, and what every homeowner should know. Call (818) 302-5614.">'
    if old_desc in html:
        html = html.replace(old_desc, new_desc)
        print("  blog: description fixed")
    else:
        # Try without HTML entity
        old_desc2 = '<meta name="description" content="Complete guide to smoke and carbon monoxide detector installation in Los Angeles. California code requirements &amp; what homeowners. Call (818) 302-5614.">'
        if old_desc2 in html:
            html = html.replace(old_desc2, new_desc)
            print("  blog: description fixed (entity)")

    # Fix OG description
    old_og_desc = '<meta property="og:description" content="Complete guide to smoke and carbon monoxide detector installation in Los Angeles. California code requirements.">'
    new_og_desc = '<meta property="og:description" content="Complete guide to smoke and CO detector installation in Los Angeles. California code requirements, costs, and what homeowners should know.">'
    if old_og_desc in html:
        html = html.replace(old_og_desc, new_og_desc)
        print("  blog: OG description fixed")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Blog title/description fix complete.")


def cleanup_service_schema():
    """Remove datePublished/dateModified from @type: Service JSON-LD schemas."""
    count = 0
    for page in SERVICE_PAGES:
        path = os.path.join(SITE_DIR, page)
        if not os.path.exists(path):
            print(f"  SKIP {page} (not found)")
            continue

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        original = html

        # Pattern 1: inline JSON-LD (single line) - remove datePublished, dateModified
        # e.g. "datePublished": "2024-01-15", "dateModified": "2026-06-08",
        html = re.sub(
            r'\s*"datePublished":\s*"[^"]*",\s*"dateModified":\s*"[^"]*",\s*',
            "",
            html,
        )
        # Alternative order
        html = re.sub(
            r'\s*"dateModified":\s*"[^"]*",\s*"datePublished":\s*"[^"]*",\s*',
            "",
            html,
        )

        # Pattern 2: multi-line JSON-LD
        html = re.sub(
            r'\s*"datePublished":\s*"[^"]*",\n\s*"dateModified":\s*"[^"]*",\n\s*',
            "\n  ",
            html,
        )
        html = re.sub(
            r'\s*"dateModified":\s*"[^"]*",\n\s*"datePublished":\s*"[^"]*",\n\s*',
            "\n  ",
            html,
        )

        if html != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
            print(f"  {page}: cleaned")
        else:
            print(f"  {page}: no changes")

    print(f"Service schema cleanup complete ({count} pages modified).")


def main():
    print("=" * 60)
    print("Batch Updates for AMY Electric Site")
    print("=" * 60)

    print("\n--- Step 1: Expand City FAQ 3→5 ---")
    expand_city_faqs()

    print("\n--- Step 2: Fix Blog Title ---")
    fix_blog_title()

    print("\n--- Step 3: Cleanup Service Schema ---")
    cleanup_service_schema()

    print("\n" + "=" * 60)
    print("All updates complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
