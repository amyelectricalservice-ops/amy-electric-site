#!/usr/bin/env python3
"""
Unified Schema Tool — validate, generate, and fix JSON-LD across all pages.

Usage:
  python3 scripts/schema-tool.py validate    # Check all pages for schema issues
  python3 scripts/schema-tool.py generate    # Inject/regenerate schemas from templates
  python3 scripts/schema-tool.py fix         # Fix common schema issues
  python3 scripts/schema-tool.py audit       # Full report
"""

import json
import os
import re
import sys

from site_data import (
    SITE_DIR, BUSINESS, CITIES, SERVICES, CITY_LOOKUP, SERVICE_LOOKUP,
    ALL_PAGES, SERVICE_PAGES, CITY_PAGES, GEO_SERVICE_PAGES,
    NAV_LINKS, json_ld, json_ld_pretty,
    make_electrician, make_service, make_faqpage, make_breadcrumb,
    make_blogposting, make_website
)

# ─── FAQ templates ────────────────────────────────────────────────────

FAQ_LICENSING = [
    {"q": "Are you licensed and insured?", "a": f"Yes — {BUSINESS['name']} is a licensed California C-10 electrical contractor ({BUSINESS['license']}) and EVITP-certified ({BUSINESS['evitp']}). We carry full general liability insurance and workers' compensation insurance. Our license is active and in good standing with the CSLB, and we pull all required permits for every job. You can verify our license anytime at the California Contractors State License Board website."},
    {"q": "Do you offer free estimates?", "a": f"Yes — we provide free, no-obligation estimates for all electrical work. Whether you need a panel upgrade, EV charger installation, home rewiring, or commercial electrical service, we'll come out, assess the job, and provide a detailed written estimate. Call {BUSINESS['telephone_display']} or use our online form to schedule yours."},
]

FAQ_HOMEPAGE = [
    {"q": "Do you offer emergency electrical services?", "a": f"Call {BUSINESS['telephone_display']} to discuss current emergency dispatch availability throughout Los Angeles. For active fire, severe shock, or downed power lines, call 911 first."},
    {"q": "How much does a panel upgrade cost in Los Angeles?", "a": "Panel upgrade costs in Los Angeles typically range from $1,500 to $3,500 for a 100A to 200A upgrade, depending on your home's wiring, the distance from the meter to the panel, and LADWP requirements. We provide free, detailed estimates after an on-site assessment."},
    {"q": "Do you install EV chargers?", "a": "Yes — we specialize in Level 2 EV charger installations for Tesla, Rivian, ChargePoint, and all EV brands. We handle all LADBS permitting, utility coordination, and final inspection. Our EVITP-certified electricians ensure your charger is installed safely and to code. Most installations are completed in one day."},
    {"q": "What areas do you serve?", "a": "We serve the greater Los Angeles area including Sherman Oaks, Burbank, Glendale, Pasadena, Studio City, North Hollywood, Hollywood, Beverly Hills, West LA, Encino, Santa Monica, Van Nuys, Woodland Hills, Calabasas, and Culver City."},
    {"q": "How long does a typical installation take?", "a": "Most residential electrical installations take 1–2 days. EV charger installations are typically completed in 4–6 hours. Panel upgrades take 6–8 hours with a planned power outage. Commercial projects vary based on scope. We provide precise timelines during the estimate process."},
    {"q": "Do you handle permits and inspections?", "a": "Yes — we handle all permitting and inspections as part of every installation. We manage the entire process: permit applications, plan review submissions, scheduling inspections, and obtaining the final Certificate of Completion. Permitting ensures code compliance and protects your insurance."},
    {"q": "What payment methods do you accept?", "a": "We accept all major credit cards, debit cards, and electronic transfers. Financing options are available for larger projects including panel upgrades and EV charger installations. We provide detailed invoices for all work."},
    {"q": "Are you available on weekends?", "a": "Our office hours are Monday–Friday 7 AM–5 PM and Saturday 8 AM–2 PM. Call to discuss current availability for urgent electrical issues."},
    {"q": "Do you offer warranties on your work?", "a": "Yes — all work performed by AMY Electric is backed by a workmanship warranty. We stand behind our installations and are always available to address any issues that arise. Manufacturer warranties also apply to parts and equipment we install."},
    {"q": "Can you match existing fixture styles?", "a": "Yes — we can match existing fixture styles, finishes, and brands for additions and replacements. We carry access to a wide range of electrical fixtures and can source matching parts for older installations."},
    {"q": "What is the C-10 license?", "a": "A C-10 Electrical Contractor license is issued by the California Contractors State License Board (CSLB). It authorizes us to perform electrical work of any type in California. Our license number #981578 is active and in good standing. You can verify it at cslb.ca.gov."},
    {"q": "Do you work with property managers?", "a": "Yes — we work extensively with property managers, HOAs, and commercial property owners. We offer preferred pricing for ongoing maintenance contracts, bulk installations, and multi-unit properties. We understand the scheduling and notification requirements of managed properties."},
    {"q": "How do I schedule an appointment?", "a": f"Call us at {BUSINESS['telephone_display']}, use the estimate form on this page, or email {BUSINESS['email']}. We will confirm availability and the next available appointment."},
    {"q": "Do you install smart home devices?", "a": "Yes — we install smart switches, dimmers, thermostats, lighting controls, and home automation systems. We ensure proper neutral wire connections, which older homes may lack, and configure WiFi-enabled devices for seamless integration."},
    {"q": "What should I do in an electrical emergency?", "a": "If you smell burning, see sparks, or have a power outage affecting only your home: (1) Turn off the affected circuit at the main panel if safe, (2) Call 911 if there is active fire or smoke, (3) Call us at (818) 302-5614 to discuss current emergency availability."},
]

FAQ_CITY_EXTRA = [
    {"q": "Are you licensed and insured to work in __CITY__?", "a": f"Yes — {BUSINESS['name']} is a licensed California C-10 electrical contractor ({BUSINESS['license']}) and EVITP-certified ({BUSINESS['evitp']}). We carry full general liability insurance and workers' compensation insurance. Our license is active and in good standing with the CSLB, and we pull all required permits for every job in __CITY__. You can verify our license anytime at the California Contractors State License Board website."},
    {"q": "Do you offer free estimates for electrical work in __CITY__?", "a": f"Yes — we provide free, no-obligation estimates for all electrical work in __CITY__. Whether you need a panel upgrade, EV charger installation, home rewiring, or commercial electrical service, we'll come out, assess the job, and provide a detailed written estimate. Call {BUSINESS['telephone_display']} or use our online form to schedule yours."},
]

FAQ_TESTIMONIALS = [
    {"q": "How can I leave a review for AMY Electric?", "a": "You can leave a review on Google, Yelp, or Nextdoor. The fastest way is to use our direct Google review link: https://g.page/r/CVdK9ZAvNBrZEAI/review. We appreciate detailed feedback about your experience with our electrical services."},
    {"q": "How does AMY Electric handle customer feedback?", "a": "Customer feedback helps us understand what went well and where communication or service can improve. If you have a concern about an electrical service, contact AMY Electric directly so the team can review the details."},
    {"q": "Where can I read customer reviews?", "a": "Customer reviews may be available through the linked Google and Yelp profiles. Review counts and ratings can change over time, so check those profiles for the current information."},
]

FAQ_GALLERY = [
    {"q": "What types of electrical projects are shown in the gallery?", "a": "Our gallery features real projects completed by AMY Electric across Los Angeles, including panel upgrades, EV charger installations, new construction wiring, commercial electrical work, lighting installations, and service upgrades. Each photo includes a description of the work performed."},
    {"q": "How are the gallery photos selected?", "a": "We select photos that showcase our best work and represent the range of electrical services we offer. All photos are of actual projects we've completed for real clients in Los Angeles, Sherman Oaks, Burbank, Glendale, Pasadena, and surrounding areas."},
    {"q": "Can I request photos of work similar to my project?", "a": f"Yes — if you're considering a specific type of electrical work and want to see examples, call us at {BUSINESS['telephone_display']}. We can share photos of similar projects we've completed and arrange a free on-site estimate to discuss your specific needs."},
]

# ─── Breadcrumb typo fixes ────────────────────────────────────────────
BREADCRUMB_FIXES = {
    "Costin": "Cost in",
    "Tipsfor": "Tips for",
    "Chargerin": "Charger in",
    "InstallationMakes": "Installation Makes",
    "Upgradesfor": "Upgrades for",
    "Upgradein": "Upgrade in",
    "Codefor": "Code for",
}


def get_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def put_html(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def find_jsonld(html, type_name):
    """Find all JSON-LD script blocks matching a @type."""
    results = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
        block = m.group(1).strip()
        try:
            data = json.loads(block)
            if isinstance(data, dict) and data.get('@type') == type_name:
                results.append((m.start(), m.end(), data, block))
            if isinstance(data, dict) and '@graph' in data:
                for item in data['@graph']:
                    if isinstance(item, dict) and item.get('@type') == type_name:
                        results.append((m.start(), m.end(), data, block))
        except json.JSONDecodeError:
            pass
    return results


def jsonld_in_html(html, type_name):
    return len(find_jsonld(html, type_name)) > 0


def page_path(stem):
    return stem if stem != "index" else ""


# ═══════════════════════════════════════════════════════════════════════
#  VALIDATE
# ═══════════════════════════════════════════════════════════════════════

def _walk_html():
    """Yield (relative_path, absolute_path) for all HTML files."""
    # Root pages
    for fname in sorted(os.listdir(SITE_DIR)):
        if fname.endswith(".html") and not fname.startswith(".") and "amyelectric-site" not in fname:
            yield fname, os.path.join(SITE_DIR, fname)
    # Blog pages
    blog_dir = os.path.join(SITE_DIR, "blog")
    if os.path.isdir(blog_dir):
        for fname in sorted(os.listdir(blog_dir)):
            if fname.endswith(".html"):
                yield f"blog/{fname}", os.path.join(blog_dir, fname)


def cmd_validate():
    issues = []
    for rel_path, abs_path in _walk_html():
        fname = rel_path
        html = get_html(abs_path)
        stem = fname.replace(".html", "")

        base_stem = os.path.splitext(os.path.basename(fname))[0]
        is_redirect = 'noindex' in html and 'http-equiv="refresh"' in html

        # ── Electrician / Service check ──
        if fname.startswith("blog/") or is_redirect:
            pass
        else:
            elecs = find_jsonld(html, "Electrician")
            services = find_jsonld(html, "Service")
            if not elecs and not services:
                issues.append(f"MISSING Electrician/Service schema: {fname}")
            elif elecs:
                _, _, data, _ = elecs[0]
                if isinstance(data, dict) and '@graph' in data:
                    for item in data['@graph']:
                        if isinstance(item, dict) and item.get('@type') == 'Electrician':
                            data = item
                if 'openingHoursSpecification' not in data:
                    issues.append(f"INCOMPLETE Electrician (no hours): {fname}")
                if 'hasCredential' not in data:
                    issues.append(f"INCOMPLETE Electrician (no credentials): {fname}")

        # Check FAQPage
        if fname in ["testimonials.html", "gallery.html"]:
            if not jsonld_in_html(html, "FAQPage"):
                issues.append(f"MISSING FAQPage schema: {fname}")

        # Skip BreadcrumbList check for redirect pages
        if is_redirect:
            pass
        elif base_stem not in ("index", "privacy-policy") and fname != "blog/index.html":
            if not jsonld_in_html(html, "BreadcrumbList"):
                issues.append(f"MISSING BreadcrumbList: {fname}")

        if os.path.basename(fname) in CITY_PAGES:
            if not jsonld_in_html(html, "WebSite"):
                issues.append(f"MISSING WebSite schema: {fname}")

        # Check blog breadcrumb text
        if fname.startswith("blog/"):
            for m in re.finditer(r'"name"\s*:\s*"([^"]+)"', html):
                name = m.group(1)
                for typo in BREADCRUMB_FIXES:
                    if typo in name:
                        issues.append(f"BREADCRUMB_TYPO '{typo}' in {fname}: '{name}'")

    if issues:
        print(f"Found {len(issues)} issue(s):\n")
        for i in issues:
            print(f"  • {i}")
        return 1
    print("All pages pass validation.")
    return 0


# ═══════════════════════════════════════════════════════════════════════
#  GENERATE
# ═══════════════════════════════════════════════════════════════════════

def _inject_or_replace(html, type_name, new_block, insert_before=None):
    """Replace existing JSON-LD of a type, or inject before insert_before (or </head>)."""
    blocks = find_jsonld(html, type_name)
    if blocks:
        start, end = blocks[0][0], blocks[0][1]
        return html[:start] + "\n" + new_block + "\n" + html[end:]

    if insert_before:
        pattern = re.compile(re.escape(insert_before))
        m = pattern.search(html)
        if m:
            pos = m.start()
            return html[:pos] + "\n" + new_block + "\n" + html[pos:]

    return html.replace("</head>", new_block + "\n</head>", 1)


def cmd_generate():
    changed = []
    for rel_path, abs_path in _walk_html():
        fname = rel_path
        _, fname_only = os.path.split(fname)
        if not fname_only:
            fname_only = fname.split("/")[-1]
        path = abs_path
        html = get_html(path)
        stem = os.path.splitext(os.path.basename(fname))[0]
        orig = html

        # ── Electrician ──
        elec_block = json_ld(make_electrician(page_path(stem)))
        if jsonld_in_html(html, "Electrician"):
            start, end, data, raw = find_jsonld(html, "Electrician")[0]
            html = html[:start] + "\n" + elec_block + "\n" + html[end:]
        else:
            html = _inject_or_replace(html, "Electrician", elec_block)

        # ── WebSite schema on city pages and homepage ──
        base = os.path.basename(fname)
        if base in CITY_PAGES or base == "index.html":
            ws_block = json_ld(make_website())
            if jsonld_in_html(html, "WebSite"):
                start, end = find_jsonld(html, "WebSite")[0][:2]
                html = html[:start] + "\n" + ws_block + "\n" + html[end:]
            else:
                html = _inject_or_replace(html, "WebSite", ws_block)

        # ── FAQPage for testimonials/gallery ──
        if base == "testimonials.html" and not jsonld_in_html(html, "FAQPage"):
            html = _inject_or_replace(html, "FAQPage", json_ld(make_faqpage(FAQ_TESTIMONIALS)), insert_before='"BreadcrumbList"')
        if base == "gallery.html" and not jsonld_in_html(html, "FAQPage"):
            html = _inject_or_replace(html, "FAQPage", json_ld(make_faqpage(FAQ_GALLERY)), insert_before='"BreadcrumbList"')

        if html != orig:
            put_html(path, html)
            changed.append(fname)
            print(f"  ~ {fname}")

    print(f"\n{len(changed)} file(s) updated.")
    return 0


# ═══════════════════════════════════════════════════════════════════════
#  FIX
# ═══════════════════════════════════════════════════════════════════════

def cmd_fix():
    fixed = []

    # 1. Fix breadcrumb text in blog files
    blog_dir = os.path.join(SITE_DIR, "blog")
    if os.path.isdir(blog_dir):
        for fname in sorted(os.listdir(blog_dir)):
            if not fname.endswith(".html") or fname == "index.html":
                continue
            path = os.path.join(blog_dir, fname)
            html = get_html(path)
            orig = html
            for typo, repl in BREADCRUMB_FIXES.items():
                html = html.replace(typo, repl)
            # Fix colon run-on in name values
            def fix_colon(m):
                val = re.sub(r':([A-Za-z0-9])', r': \1', m.group(1))
                return f'"name": "{val}"'
            html = re.sub(r'"name"\s*:\s*"([^"]+)"', fix_colon, html)
            if html != orig:
                put_html(path, html)
                fixed.append(f"blog/{fname}")

    # 2. Remove datePublished/dateModified from Service schemas
    service_page_files = SERVICE_PAGES + ["panel-100a-vs-200a.html", "ev-charger-hardwired-vs-plug-in.html"]
    for fname in service_page_files:
        path = os.path.join(SITE_DIR, fname)
        if not os.path.exists(path):
            continue
        html = get_html(path)
        orig = html
        html = re.sub(r'\s*"datePublished":\s*"[^"]*",?\s*', "", html)
        html = re.sub(r'\s*"dateModified":\s*"[^"]*",?\s*', "", html)
        if html != orig:
            put_html(path, html)
            fixed.append(fname)

    if fixed:
        print(f"Fixed {len(fixed)} file(s):")
        for f in fixed:
            print(f"  • {f}")
    else:
        print("No fixes needed.")
    return 0


# ═══════════════════════════════════════════════════════════════════════
#  AUDIT
# ═══════════════════════════════════════════════════════════════════════

def cmd_audit():
    print("=" * 60)
    print("Schema Audit Report")
    print("=" * 60)

    total = 0
    with_elec = 0
    with_faq = 0
    with_breadcrumb = 0
    with_website = 0

    for rel_path, abs_path in _walk_html():
        fname = rel_path
        html = get_html(abs_path)
        total += 1

        if jsonld_in_html(html, "Electrician"):
            with_elec += 1
        if jsonld_in_html(html, "FAQPage"):
            with_faq += 1
        if jsonld_in_html(html, "BreadcrumbList"):
            with_breadcrumb += 1
        if jsonld_in_html(html, "WebSite"):
            with_website += 1

    print(f"\nPages scanned: {total}")
    print(f"  Electrician:     {with_elec}/{total}")
    print(f"  FAQPage:         {with_faq}/{total}")
    print(f"  BreadcrumbList:  {with_breadcrumb}/{total}")
    print(f"  WebSite:         {with_website}/{total}")

    print(f"\nRun 'validate' for detailed issue list.")
    return 0


# ═══════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    cmd = sys.argv[1]
    cmds = {
        "validate": cmd_validate,
        "generate": cmd_generate,
        "fix": cmd_fix,
        "audit": cmd_audit,
    }

    fn = cmds.get(cmd)
    if not fn:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        return 1

    # Ensure we're in the site root
    os.chdir(SITE_DIR)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
