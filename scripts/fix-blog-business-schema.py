#!/usr/bin/env python3
"""Close the business-schema gaps on blog pages.

scripts/schema-tool.py skips blog/ for the Electrician/Service check, so these
drifted unnoticed:
  - is-your-home-ev-ready-los-angeles.html declares an Electrician with no
    openingHoursSpecification, failing the project's own standard for that type
  - 6 posts carry no business schema at all, while 55 of 61 do

Adds a compliant Electrician node to the 6, and backfills the hours on the 7th.
Cloned from a page that already passes, so the data is identical to the rest of
the site rather than newly invented. Idempotent.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
BLOCK = re.compile(r'(?is)(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)')

HOURS = [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
     "opens": "07:00", "closes": "17:00", "description": "Office hours"},
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00",
     "description": "Office hours"},
]


def load(p):
    h = open(os.path.join(ROOT, p), encoding="utf-8").read()
    nodes = []
    for m in BLOCK.finditer(h):
        try:
            nodes.append((m, json.loads(m.group(2).strip())))
        except Exception:
            pass
    return h, nodes


template = None
for _, obj in load("emergency-electrician.html")[1]:
    for it in (obj if isinstance(obj, list) else [obj]):
        if isinstance(it, dict) and it.get("@type") == "Electrician":
            template = it
if template is None:
    raise SystemExit("no Electrician template found")

BLOG = "blog"
added, hours_added = [], []

for f in sorted(os.listdir(os.path.join(ROOT, BLOG))):
    if not f.endswith(".html"):
        continue
    rel = BLOG + "/" + f
    doc, blocks = load(rel)
    biz = [it for _, o in blocks for it in (o if isinstance(o, list) else [o])
           if isinstance(it, dict) and it.get("@type") in ("Electrician", "LocalBusiness")]
    canon = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', doc, re.I)
    url = canon.group(1) if canon else "https://amyelectric.com/" + rel[:-5]

    if not biz:
        elec = copy.deepcopy(template)
        elec["@id"] = url
        elec["url"] = url
        payload = ('<script type="application/ld+json">\n'
                   + json.dumps(elec, indent=2, ensure_ascii=False)
                   + "\n</script>\n")
        if APPLY:
            i = doc.find("</head>")
            if i == -1:
                i = doc.find("<body")
            open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(doc[:i] + payload + doc[i:])
        added.append(rel)
        continue

    for m, obj in blocks:
        items = obj if isinstance(obj, list) else [obj]
        for it in items:
            if isinstance(it, dict) and it.get("@type") == "Electrician" \
                    and "openingHoursSpecification" not in it:
                it["openingHoursSpecification"] = copy.deepcopy(HOURS)
                if APPLY:
                    new = json.dumps(obj, indent=2, ensure_ascii=False)
                    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(
                        doc[:m.start(2)] + "\n" + new + "\n" + doc[m.end(2):])
                hours_added.append(rel)

print("mode:                 %s" % ("APPLY" if APPLY else "DRY RUN"))
print("Electrician added:    %d %s" % (len(added), added))
print("hours backfilled:     %d %s" % (len(hours_added), hours_added))
