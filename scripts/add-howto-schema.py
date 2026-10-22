#!/usr/bin/env python3
"""Add HowTo JSON-LD to service pages whose visible step sections lack it.

Extraction mirrors the visible markup exactly (Google validates consistency
between structured data and page content), so the step names/texts come
straight from the DOM:

  - pattern A: `<h2>` process heading followed by a `<div class="steps">`
    container of `<div class="step"><div class="step-num">N</div>
    <div class="step-body"><strong>Name</strong><p>Text</p></div></div>`
  - pattern B: `<h2>` process heading followed by an inline-styled grid of
    blocks, each `<div style="text-align:center"><div>0N</div><h3>Name</h3>
    <p>Text</p></div>`

What is emitted follows the existing HowTo blocks (ev-charger-installation
et al.): one dedicated `<script type="application/ld+json">` block in <head>.
Only required fields are set (name + step) — no costs/times we do not state.

Idempotent: pages that already carry a HowTo block are skipped. Run
`python3 scripts/schema-tool.py validate` afterwards.
"""
import html
import json
import re
import sys

# Page -> (process H2 exactly as in the file, HowTo @name).
PAGES = {
    "tesla-charger-installation.html": (
        "Your Tesla Charger Installation Process",
        "How Tesla Charger Installation Works in Los Angeles"),
    "ceiling-fan-installation.html": (
        "How Does the Ceiling Fan Installation Process Work?",
        "How Ceiling Fan Installation Works in Los Angeles"),
    "dedicated-circuits.html": (
        "Dedicated Circuit Installation Process",
        "How Dedicated Circuit Installation Works in Los Angeles"),
    "electrical-safety-inspections.html": (
        "Electrical Safety Inspection Process",
        "How an Electrical Safety Inspection Works in Los Angeles"),
    "outlet-switch-installation.html": (
        "How Does Outlet and Switch Installation Work?",
        "How Outlet & Switch Installation Works in Los Angeles"),
    "smart-home-electrical.html": (
        "Smart Home Electrical Installation Process",
        "How Smart Home Electrical Installation Works in Los Angeles"),
    "smoke-co-detector-installation.html": (
        "Smoke & CO Detector Installation Process",
        "How Smoke & CO Detector Installation Works in Los Angeles"),
    "200-amp-panel-upgrade.html": (
        "How We Upgrade Your Panel",
        "How a 200 Amp Panel Upgrade Works in Los Angeles"),
    "subpanel-installation.html": (
        "How We Install Your Subpanel",
        "How Subpanel Installation Works in Los Angeles"),
}

STEP_A = re.compile(
    r'<div class="step"><div class="step-num">\d+</div>'
    r'<div class="step-body"><strong>(.*?)</strong><p>(.*?)</p></div></div>',
    re.S)
STEP_B = re.compile(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', re.S)


def clean(text):
    """Strip stray tags/whitespace and resolve entities to visible text."""
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def section_after_h2(doc, h2):
    m = re.search(r"<h2[^>]*>%s</h2>(.*?)(</section>|</div></section>)" % re.escape(h2), doc, re.S)
    if not m:
        raise SystemExit("process heading not found: %r" % h2)
    return m.group(1)


def extract(doc, h2):
    region = section_after_h2(doc, h2)
    if 'class="steps"' in region:
        steps = STEP_A.findall(region)
    else:
        steps = STEP_B.findall(region)
    if not steps:
        raise SystemExit("no steps found under heading %r" % h2)
    out = []
    for name, text in steps:
        name, text = clean(name), clean(text)
        if not name or not text:
            raise SystemExit("empty step under heading %r" % h2)
        out.append((name, text))
    return out


def main():
    added = skipped = 0
    for fname, (h2, howto_name) in PAGES.items():
        doc = open(fname, encoding="utf-8").read()
        if '"@type": "HowTo"' in doc:
            print("  %-38s already has HowTo" % fname)
            skipped += 1
            continue
        steps = extract(doc, h2)
        howto = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": howto_name,
            "step": [
                {"@type": "HowToStep", "position": i, "name": name, "text": text}
                for i, (name, text) in enumerate(steps, 1)
            ],
        }
        block = '<script type="application/ld+json">\n' \
            + json.dumps(howto, indent=2, ensure_ascii=False) + "\n</script>\n"
        i = doc.find("</head>")
        doc = doc[:i] + block + doc[i:]
        open(fname, "w", encoding="utf-8").write(doc)
        added += 1
        print("  %-38s +HowTo (%d steps: %s)" % (fname, len(steps), ", ".join(n for n, _ in steps)))
    print("added %d, skipped %d" % (added, skipped))
    sys.exit(0)


if __name__ == "__main__":
    main()
