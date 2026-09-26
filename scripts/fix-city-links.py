#!/usr/bin/env python3
"""Fix the broken-link template used by the 59 'neighborhood' city pages.

Three defects, all from the same generator:
  1. href="/contact"  -> 404. No contact page exists. /#estimate does (id="estimate" on index.html).
  2. href="/areas-served" -> 404. The real index is /service-areas. Appears in nav,
     breadcrumb, "View All Service Areas" CTA and footer, plus the BreadcrumbList JSON-LD.
  3. Byte-identical <p class="nearby-cities"> blocks emitted more than once.

Idempotent: re-running is a no-op.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_PREFIX = "city-"

CONTACT = 'href="/contact"'
ESTIMATE = 'href="/#estimate"'
AREAS = 'href="/areas-served"'
AREAS_FIXED = 'href="/service-areas"'
LD_AREAS = '"https://amyelectric.com/areas-served"'
LD_AREAS_FIXED = '"https://amyelectric.com/service-areas"'

counts = {"contact": 0, "areas": 0, "active": 0, "ld": 0, "dupe": 0, "files": 0}
changed = []

for name in sorted(os.listdir(ROOT)):
    if not name.startswith(TARGET_PREFIX) or not name.endswith(".html"):
        continue
    path = os.path.join(ROOT, name)
    with open(path, encoding="utf-8") as fh:
        orig = html = fh.read()

    # 1. dead contact links
    n = html.count(CONTACT)
    if n:
        html = html.replace(CONTACT, ESTIMATE)
        counts["contact"] += n

    # 2. dead service-areas links; drop the misleading active state since these
    #    pages are city pages, not the service-areas index.
    n = html.count(AREAS + ' class="active"')
    if n:
        html = html.replace(AREAS + ' class="active"', AREAS_FIXED)
        counts["active"] += n
    n = html.count(AREAS)
    if n:
        html = html.replace(AREAS, AREAS_FIXED)
        counts["areas"] += n

    # 3. same 404 inside BreadcrumbList
    n = html.count(LD_AREAS)
    if n:
        html = html.replace(LD_AREAS, LD_AREAS_FIXED)
        counts["ld"] += n

    # 4. collapse byte-identical nearby-cities paragraphs
    lines = html.split("\n")
    seen = set()
    kept = []
    for line in lines:
        s = line.strip()
        if s.startswith('<p class="nearby-cities">') and s in seen:
            counts["dupe"] += 1
            continue
        if s.startswith('<p class="nearby-cities">'):
            seen.add(s)
        kept.append(line)
    html = "\n".join(kept)

    if html != orig:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        changed.append(name)
        counts["files"] += 1

for k, v in counts.items():
    print("  %-9s %d" % (k, v))
print("  files changed: %d" % len(changed))

leftover = []
for name in changed:
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        t = fh.read()
    if CONTACT in t or AREAS in t or LD_AREAS in t:
        leftover.append(name)
print("  VERIFY leftover 404 refs: %d %s" % (len(leftover), leftover))
sys.exit(1 if leftover else 0)
