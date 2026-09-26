#!/usr/bin/env python3
"""Collapse the duplicate business entity on the 2 pages that had one.

emergency-electrical.html and reviews.html each carried a LocalBusiness node. An
Electrician node was added to satisfy schema-tool.py, which left two nodes sharing
one @id with different @type - a data-modelling error, since @id identifies a node
and Electrician is itself a LocalBusiness subtype.

This merges them into a single Electrician node: the page's own LocalBusiness values
win, and any property only the Electrician node carried (founder, foundingDate,
hasCredential, openingHoursSpecification, areaServed) is folded in. Idempotent.
"""
import json
import re

ROOT = "/home/amram/WEBSITE"
TARGETS = ["emergency-electrical.html", "reviews.html"]
BLOCK = re.compile(r'(?is)(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)')


def nodes(doc):
    out = []
    for m in BLOCK.finditer(doc):
        try:
            obj = json.loads(m.group(2).strip())
        except Exception:
            continue
        for it in (obj if isinstance(obj, list) else [obj]):
            if isinstance(it, dict):
                out.append((m, it))
    return out


for fname in TARGETS:
    path = f"{ROOT}/{fname}"
    doc = open(path, encoding="utf-8").read()
    ents = nodes(doc)
    lb = [(m, it) for m, it in ents if it.get("@type") == "LocalBusiness"]
    el = [(m, it) for m, it in ents if it.get("@type") == "Electrician"]

    if not lb:
        print("  %-30s no LocalBusiness node, skipped" % fname)
        continue
    if not el:
        print("  %-30s no Electrician node, nothing to merge" % fname)
        continue

    lb_m, lb_node = lb[0]
    merged = dict(el[0][1])
    merged.update(lb_node)
    merged["@type"] = "Electrician"
    merged.setdefault("@context", "https://schema.org")

    # rewrite the LocalBusiness block as the merged node, drop the Electrician block
    payload = json.dumps(merged, indent=2, ensure_ascii=False)
    doc = doc[:lb_m.start()] + lb_m.group(1) + "\n" + payload + "\n" + lb_m.group(3) + doc[lb_m.end():]
    # recompute and remove the now-duplicate Electrician block
    for m, _ in nodes(doc):
        if _.get("@type") == "Electrician" and m.start() != doc.find('"@type": "Electrician"'):
            pass
    ents2 = nodes(doc)
    seen = False
    for m, it in ents2:
        if it.get("@type") != "Electrician":
            continue
        if not seen:
            seen = True
            continue
        doc = doc[:m.start()] + doc[m.end():]

    open(path, "w", encoding="utf-8").write(doc)

    final = nodes(doc)
    biz = [(it.get("@type"), it.get("@id")) for _, it in final
           if it.get("@type") in ("Electrician", "LocalBusiness", "Service")]
    ids = [i for _, i in biz]
    print("  %-30s business entities now: %s" % (fname, biz))
    print("  %-30s duplicate @id: %s" % ("", len(ids) != len(set(ids))))
    elec = [it for _, it in final if it.get("@type") == "Electrician"]
    if elec:
        e = elec[0]
        print("  %-30s openingHoursSpecification=%s hasCredential=%s"
              % ("", "openingHoursSpecification" in e, "hasCredential" in e))
