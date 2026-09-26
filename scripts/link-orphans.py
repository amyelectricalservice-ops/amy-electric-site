#!/usr/bin/env python3
"""Extend the existing "by City" sections so every city variant is reachable.

panel-upgrade.html listed 10 of its 24 city pages and ev-charger-installation.html
listed 6 of 24, leaving 32 geo pages orphaned. Appends only the missing cards,
reusing each section's own markup and sub-text. Idempotent.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPECIAL = {"la": "LA", "west-la": "West LA", "la-crescenta": "La Crescenta"}


def pretty(slug):
    return SPECIAL.get(slug) or " ".join(w.capitalize() for w in slug.split("-"))


def existing_variants(prefix):
    out = []
    for f in os.listdir(ROOT):
        m = re.fullmatch(re.escape(prefix) + r"-(.+)\.html", f)
        if m:
            out.append(m.group(1))
    return sorted(out)


for page, heading in [("panel-upgrade.html", "Panel Upgrades by City"),
                      ("ev-charger-installation.html", "EV Charger Installation by City")]:
    path = os.path.join(ROOT, page)
    doc = open(path, encoding="utf-8").read()
    stem = page[:-5]

    hm = re.search(
        r'(?is)<section[^>]*>\s*<div class="wrap[^"]*">\s*'
        r'<div class="section-label">Service Areas</div>\s*<h2>%s</h2>' % re.escape(heading),
        doc)
    if not hm:
        print("  %-32s by-city section not found" % page)
        continue

    # The two hubs use different wrappers (flex-center-wrap vs inline flex), so
    # anchor on the last existing card in the section instead of a class name.
    sec_end = doc.find("</section>", hm.end())
    section = doc[hm.start():sec_end]
    cards = list(re.finditer(r'<a\s+href="%s-[^"]+"' % re.escape(stem), section))
    if not cards:
        print("  %-32s no city cards in section" % page)
        continue
    last = cards[-1]
    close = section.find("</a>", last.end())
    if close == -1:
        print("  %-32s could not locate card boundary" % page)
        continue

    have = set(re.findall(r'href="%s-([^"]+)"' % re.escape(stem), section))
    allv = existing_variants(stem)
    missing = [c for c in allv if c not in have]
    if not missing:
        print("  %-32s already complete (%d/%d cities)" % (page, len(have & set(allv)), len(allv)))
        continue

    tail_txt = re.search(r'(?is)<a\s+href="%s-[^"]+"[^>]*>(.*?)</a>' % re.escape(stem), section, re.S)
    proto = tail_txt.group(0)
    span = re.search(r'(?is)(<span[^>]*>)(.*?)(</span>)', proto)
    span_open, sub, span_close = (span.group(1), span.group(2), span.group(3)) if span else ("", "Service details", "")

    attrs = re.match(r'(?is)<a\s+href="[^"]+"([^>]*)>', proto)
    extra = attrs.group(1) if attrs else ' class="related-card flex-card"'

    cards_html = []
    for c in missing:
        cards_html.append('\n      <a href="%s-%s"%s><strong>%s</strong>%s%s%s</a>'
                          % (stem, c, extra, pretty(c), span_open, sub, span_close))

    at = hm.start() + close + len("</a>")
    open(path, "w", encoding="utf-8").write(doc[:at] + "".join(cards_html) + doc[at:])
    print("  %-32s +%d cities (now %d/%d)" % (page, len(missing), len(have & set(allv)) + len(missing), len(allv)))
