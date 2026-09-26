#!/usr/bin/env python3
"""Add the missing Electrician schema to 3 pages flagged by scripts/schema-tool.py.

emergency-electrical.html and reviews.html carry LocalBusiness but not Electrician,
and ev-charger-vs-panel-upgrade.html has no business schema at all. The block is
cloned from a compliant page and only @id/url are repointed, so the three pages
match the other 240+ exactly. Idempotent.
"""
import copy
import json
import re

REF = "emergency-electrician.html"
TARGETS = {
    "emergency-electrical.html": "https://amyelectric.com/emergency-electrical",
    "reviews.html": "https://amyelectric.com/reviews",
    "ev-charger-vs-panel-upgrade.html": "https://amyelectric.com/ev-charger-vs-panel-upgrade",
}
BLOCK = re.compile(r'(?is)<script[^>]*type="application/ld\+json"[^>]*>.*?</script>')


def blocks(doc):
    out = []
    for m in BLOCK.finditer(doc):
        try:
            out.append((m, json.loads(m.group(0).split(">", 1)[1].rsplit("</script>", 1)[0].strip())))
        except Exception:
            pass
    return out


ref_doc = open(REF, encoding="utf-8").read()
template = None
for _, obj in blocks(ref_doc):
    items = obj if isinstance(obj, list) else [obj]
    for it in items:
        if isinstance(it, dict) and it.get("@type") == "Electrician":
            template = it
if not template:
    raise SystemExit("no Electrician template found in " + REF)

for fname, url in TARGETS.items():
    doc = open(fname, encoding="utf-8").read()
    if any(isinstance(it, dict) and it.get("@type") == "Electrician"
           for _, o in blocks(doc) for it in (o if isinstance(o, list) else [o])):
        print("  %-34s already has Electrician" % fname)
        continue
    elec = copy.deepcopy(template)
    elec["@id"] = url
    elec["url"] = url
    payload = json.dumps(elec, indent=2, ensure_ascii=False)
    block = '<script type="application/ld+json">\n' + payload + "\n</script>\n"
    i = doc.find("</head>")
    if i == -1:
        i = doc.find("<body")
    doc = doc[:i] + block + doc[i:]
    open(fname, "w", encoding="utf-8").write(doc)
    print("  %-34s +Electrician (@id %s)" % (fname, url))
