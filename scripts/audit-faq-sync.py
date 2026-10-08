#!/usr/bin/env python3
"""FAQ schema <-> visible-content sync audit and fixer.

Usage:
  python3 scripts/audit-faq-sync.py --check   # report defects, exit 1 if any (writes baseline)
  python3 scripts/audit-faq-sync.py --fix     # apply fixes idempotently

Detects/fixes three classes:
  junk_name     FAQPage question names ending in accordion glyphs (" +" etc.) -> suffix stripped
  unmarked      visible <summary> question with no FAQPage entry -> appended to schema
  missing_head  <body> present with no preceding </head> -> </head> inserted

Reports (no auto-fix): missing_faqpage = page has visible faq-q disclosures but no FAQPage block.

All comparisons use normalize(): HTML-entity unescape + glyph strip + lowercase,
first 50 chars. Never compare raw text (the 2026-09-25 phantom-count bug came
from comparing "&#8217;" against "'").
"""
import glob
import json
import os
import re
import sys
import html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLYPHS = "+▾▶…"


def normalize(s):
    s = htmlmod.unescape(s)
    s = re.sub(r"[" + re.escape(GLYPHS) + r"]", "", s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def pages():
    pats = ("*.html", "blog/*.html", "case-studies/*.html")
    out = []
    for p in pats:
        out.extend(glob.glob(os.path.join(ROOT, p)))
    return sorted(f for f in out
                  if os.path.basename(f) not in ("404.html", "seo-audit-report.html"))


def jsonld_blocks(html):
    return list(re.finditer(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL))


def faq_block(html):
    """Return (match, parsed dict) for the page's FAQPage block, if any."""
    for m in jsonld_blocks(html):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get("@type") == "FAQPage":
            return m, d
    return None, None


def visible_faq_pairs(html):
    """Yield (question, answer) from <details> FAQ disclosures.

    Chunk by <details> first: a bare <summary>...</summary> regex spans across
    block boundaries and swallows the estimate-form <details id="detailed-form">
    up to the next FAQ summary (seen on 60 city pages + index).
    """
    for chunk in re.findall(r"<details[^>]*>(.*?)</details>", html, re.DOTALL):
        m = re.search(
            r'<summary[^>]*>(.*?)</summary>\s*<div class="faq-a">(.*?)</div>',
            chunk, re.DOTALL)
        if not m:
            continue
        q = normalize(re.sub(r"<[^>]+>", "", m.group(1)))
        if len(q) <= 10 or "?" not in q:
            continue
        a = re.sub(r"<[^>]+>", " ", m.group(2))
        a = re.sub(r"\s+", " ", htmlmod.unescape(a)).strip()
        yield q, a



def assert_all_parse(html, path):
    for m in re.finditer(
            r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.DOTALL):
        json.loads(m.group(1))


def scan(path):
    html = open(path, encoding="utf-8").read()
    defects = []

    # --- missing_head ---
    body = re.search(r"<body", html)
    head_end = re.search(r"</head>", html)
    if body and not head_end:
        defects.append(("missing_head", ["</head> before <body>"]))

    # --- junk_name ---
    _, faq = faq_block(html)
    if faq:
        junk = [q["name"] for q in faq.get("mainEntity", [])
                if re.search(r"[+▾▶]\s*$", q.get("name", ""))]
        if junk:
            defects.append(("junk_name", junk))

    # --- unmarked / missing_faqpage ---
    pairs = list(visible_faq_pairs(html))
    declared = ({normalize(q["name"])[:50] for q in faq.get("mainEntity", [])}
                if faq else set())
    if pairs and not faq:
        defects.append(("missing_faqpage", [q for q, _ in pairs]))
    else:
        un = [(q, a) for q, a in pairs if q[:50] not in declared]
        if un:
            defects.append(("unmarked", un))
    return html, defects



def fix(path, html, defects):
    kinds = {k for k, _ in defects}
    changed = False

    if "missing_head" in kinds:
        html = re.sub(r"(<body)", r"</head>\n\1", html, count=1)
        changed = True

    if "junk_name" in kinds or "unmarked" in kinds:
        m, faq = faq_block(html)
        assert faq, path
        for kind, items in defects:
            if kind == "junk_name":
                for q in faq["mainEntity"]:
                    q["name"] = re.sub(r"\s*[+▾▶]\s*$", "", q["name"]).strip()
            elif kind == "unmarked":
                have = {normalize(q["name"])[:50] for q in faq["mainEntity"]}
                for qtext, atext in items:
                    if qtext[:50] in have:
                        continue
                    faq["mainEntity"].append({
                        "@type": "Question",
                        "name": qtext[0].upper() + qtext[1:] if qtext[:1].islower() else qtext,
                        "acceptedAnswer": {"@type": "Answer", "text": atext},
                    })
        new_block = ('<script type="application/ld+json">\n'
                     + json.dumps(faq, ensure_ascii=False, indent=2)
                     + "\n</script>")
        html = html[:m.start()] + new_block + html[m.end():]
        changed = True

    if changed:
        assert_all_parse(html, path)
        open(path, "w", encoding="utf-8").write(html)
    return changed


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--check", "--fix"):
        print("usage: audit-faq-sync.py --check|--fix")
        return 2

    report = {}
    total = 0
    for path in pages():
        rel = os.path.relpath(path, ROOT)
        html, defects = scan(path)
        if not defects:
            continue
        report[rel] = [{"kind": k, "questions": [q if isinstance(q, str) else q[0]
                                                 for q in items]}
                       for k, items in defects]
        total += sum(len(items) for _, items in defects)
        label = "FIXED" if mode == "--fix" and fix(path, html, defects) else "FOUND"
        for kind, items in defects:
            print(f"[{label}] {kind} ({len(items)}): {rel}")

    if mode == "--check":
        baseline = os.path.join(ROOT, "audit", "faq-sync-baseline.json")
        os.makedirs(os.path.dirname(baseline), exist_ok=True)
        json.dump(report, open(baseline, "w"), indent=1, ensure_ascii=False)
        if report:
            print(f"\n{total} defect(s) across {len(report)} page(s). "
                  f"Baseline written to audit/faq-sync-baseline.json")
            return 1
        print("FAQ sync check passed: 0 defects.")
        return 0

    leftover = sum(1 for p in pages() if scan(p)[1])
    print("Post-fix rescan:", "PASS (0 defects)" if leftover == 0
          else f"FAIL ({leftover} page(s) still defective)")
    return 0 if leftover == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
