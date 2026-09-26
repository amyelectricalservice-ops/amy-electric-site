#!/usr/bin/env python3
"""Rebuild FAQPage JSON-LD so it mirrors the FAQ items actually visible on the page.

Dry run with --apply to write. Extracts <details><summary>Q</summary>A</details>
where Q is question-shaped, then replaces mainEntity with that list. A summary
must contain "?" so non-FAQ disclosures (the homepage estimate-form toggle) are
skipped.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

DETAILS = re.compile(r"(?is)<details[^>]*>(.*?)</details>")
SUMMARY = re.compile(r"(?is)<summary[^>]*>(.*?)</summary>")
BLOCK = re.compile(r'(?is)(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)')
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def text(s):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    return WS.sub(" ", html.unescape(TAG.sub(" ", s))).strip()


def visible_faqs(body):
    out = []
    for d in DETAILS.findall(body):
        m = SUMMARY.search(d)
        if not m:
            continue
        q = text(m.group(1)).replace("▾", "").strip()
        if "?" not in q or len(q.split()) < 4:
            continue
        ans = text(d[m.end():])
        if not ans:
            continue
        out.append((q, ans))
    return out


def norm(s):
    return WS.sub(" ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


pages = []
for d in sorted(os.listdir(ROOT)):
    if d.endswith(".html"):
        pages.append(d)
for sub in ("blog", "case-studies"):
    sd = os.path.join(ROOT, sub)
    if os.path.isdir(sd):
        for e in sorted(os.listdir(sd)):
            if e.endswith(".html"):
                pages.append(sub + "/" + e)

tot_add = tot_del = 0
touched = []
no_block = []

for rel in pages:
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        doc = fh.read()
    body = BLOCK.sub(" ", doc)
    vis = visible_faqs(body)
    if not vis:
        continue
    vis_n = [norm(q) for q, _ in vis]

    found = False
    changed = False
    for m in list(BLOCK.finditer(doc)):
        raw = m.group(2).strip()
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        items = obj if isinstance(obj, list) else [obj]
        for it in items:
            if not (isinstance(it, dict) and it.get("@type") == "FAQPage"):
                continue
            found = True
            cur = it.get("mainEntity", []) or []
            cur_n = [norm(q.get("name", "")) for q in cur]
            add = [q for q, n in zip(vis, vis_n) if n not in cur_n]
            rem = [q.get("name", "") for q, n in zip(cur, cur_n) if n not in set(vis_n)]
            if not add and not rem:
                continue
            tot_add += len(add)
            tot_del += len(rem)
            touched.append((rel, len(add), len(rem), add[:1], rem[:1]))
            changed = True
            if APPLY:
                merged = []
                seen = set()
                for q, a in vis:
                    if norm(q) in seen:
                        continue
                    seen.add(norm(q))
                    merged.append({
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    })
                it["mainEntity"] = merged
                new_raw = json.dumps(obj, indent=2, ensure_ascii=False)
                doc = doc[:m.start(2)] + "\n" + new_raw + "\n" + doc[m.end(2):]

    added_block = False
    if not found and vis:
        added_block = True
        touched.append((rel, len(vis), 0, vis[:1], []))
        tot_add += len(vis)
        if APPLY:
            faq = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in vis
                ],
            }
            block = ('<script type="application/ld+json">\n'
                     + json.dumps(faq, indent=2, ensure_ascii=False)
                     + "\n</script>\n</head>")
            doc = doc.replace("</head>", block, 1)
    if not found:
        no_block.append((rel, len(vis)))

    if APPLY and (changed or added_block):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc)

print("mode:                     %s" % ("APPLY" if APPLY else "DRY RUN"))
print("pages scanned:            %d" % len(pages))
print("pages needing FAQ sync:   %d" % len(touched))
print("questions to ADD:         %d" % tot_add)
print("questions to REMOVE:      %d" % tot_del)
print("pages with visible FAQ but NO FAQPage block: %d" % len(no_block))
for r, n in no_block[:15]:
    print("    %-52s %d visible" % (r, n))
print()
print("sample changes:")
for r, a, d, ex_a, ex_r in sorted(touched, key=lambda x: -(x[1] + x[2]))[:20]:
    print("   %-50s +%-3d -%-3d" % (r, a, d))
    if ex_a:
        print("        + %s" % ex_a[0][0][:88])
    if ex_r:
        print("        - %s" % ex_r[0][:88])
