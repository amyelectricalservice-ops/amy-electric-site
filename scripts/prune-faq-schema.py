#!/usr/bin/env python3
"""Drop FAQPage questions that have no visible counterpart on the page.

A FAQPage block is legitimate only if the questions it declares are actually
visible. Where a block is entirely fabricated the block is removed; where only
some questions are fabricated the block is rewritten with just the visible ones.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

BLOCK = re.compile(r'(?is)<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>')
SUMMARY = re.compile(r"(?is)<summary[^>]*>(.*?)</summary>")
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def text(s):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    return WS.sub(" ", html.unescape(TAG.sub(" ", s))).strip()


def norm(s):
    return WS.sub(" ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def visible_questions(doc):
    """Questions a visitor can actually see: <details><summary>, or a
    question-shaped <h2>/<h3>/<h4> section heading."""
    body = re.sub(r'(?is)<script[^>]*application/ld\+json.*?</script>', " ", doc)
    out = []
    for m in SUMMARY.finditer(body):
        q = text(m.group(1)).replace("▾", "").strip()
        if "?" in q and len(q.split()) >= 4:
            out.append(norm(q))
    if not out:
        for m in re.finditer(r"(?is)<h([234])[^>]*>(.*?)</h\1>", body):
            q = text(m.group(2)).strip()
            if q.endswith("?") and len(q.split()) >= 4:
                out.append(norm(q))
    return out


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

dropped_blocks = 0
pruned = 0
dropped_q = 0
changed_files = []

for rel in pages:
    path = os.path.join(ROOT, rel)
    doc = open(path, encoding="utf-8").read()
    vis = set(visible_questions(doc))

    spans = []
    for m in BLOCK.finditer(doc):
        raw = m.group(1).strip()
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        items = obj if isinstance(obj, list) else [obj]
        if len(items) != 1 or not isinstance(items[0], dict):
            continue
        if items[0].get("@type") != "FAQPage":
            continue
        me = items[0].get("mainEntity", []) or []
        keep = [q for q in me if norm(q.get("name", "")) in vis]
        if len(keep) == len(me):
            continue
        dropped_q += len(me) - len(keep)
        if not keep:
            spans.append((m.start(), m.end(), ""))
            dropped_blocks += 1
        else:
            payload = json.dumps(
                {"@context": items[0].get("@context", "https://schema.org"),
                 "@type": "FAQPage", "mainEntity": keep}, indent=2, ensure_ascii=False)
            spans.append((m.start(1), m.end(1), "\n" + payload + "\n"))
            pruned += 1

    if not spans:
        continue
    out = doc
    for start, end, payload in sorted(spans, reverse=True):
        out = out[:start] + payload + out[end:]
    out = re.sub(r"\n{3,}", "\n\n", out)
    changed_files.append(rel)
    if APPLY:
        open(path, "w", encoding="utf-8").write(out)

print("mode:                %s" % ("APPLY" if APPLY else "DRY RUN"))
print("pages changed:       %d" % len(changed_files))
print("blocks removed:      %d" % dropped_blocks)
print("blocks pruned:       %d" % pruned)
print("questions dropped:   %d" % dropped_q)
for r in changed_files:
    print("   ", r)
