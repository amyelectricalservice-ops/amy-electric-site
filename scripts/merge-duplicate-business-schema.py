#!/usr/bin/env python3
"""Collapse business entities that share an @id into a single Electrician node.

117 pages declare both a LocalBusiness and an Electrician node with an identical
@id (the page's own URL). Electrician is a LocalBusiness subtype and @id identifies
a single node, so this is a data-modelling error: a consumer merging by @id sees a
type conflict, and one that does not merge sees two competing businesses per page.

Merge rule, chosen so nothing is lost and the richer signal wins:
  - union of both nodes' properties. This matters: LocalBusiness is the sole
    carrier of `speakable` on 20 pages, and of logo/knowsAbout/review/
    hasOfferCatalog/openingHours on index.html, so keeping only the Electrician
    node would silently drop them.
  - on conflict the LocalBusiness value wins. areaServed is the only property
    where both nodes regularly differ, and only on 3 pages (index, service-areas,
    services) where LocalBusiness lists 16-17 cities against Electrician's single
    generic region. On the other 114 only Electrician has areaServed, so there is
    nothing to resolve.
  - the result is typed Electrician, the more specific type and the one
    scripts/schema-tool.py requires (with openingHoursSpecification + hasCredential)
  - null values never overwrite a real value

Service nodes and business groups with distinct @ids are left untouched.
Idempotent.
"""
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
BUSINESS = ("Electrician", "LocalBusiness", "Service")
BLOCK = re.compile(r'(?is)(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)')


def pages():
    out = [f for f in sorted(os.listdir(ROOT)) if f.endswith(".html")]
    for sub in ("blog", "case-studies"):
        sd = os.path.join(ROOT, sub)
        if os.path.isdir(sd):
            out += [sub + "/" + e for e in sorted(os.listdir(sd)) if e.endswith(".html")]
    return out


def parse(doc):
    out = []
    for m in BLOCK.finditer(doc):
        try:
            out.append((m, json.loads(m.group(2).strip())))
        except Exception:
            pass
    return out


def prune_nulls(d):
    return {k: v for k, v in d.items() if v is not None}


def build(lb, el, node_id):
    merged = dict(prune_nulls(el))
    merged.update(prune_nulls(lb))
    merged["@type"] = "Electrician"
    merged.setdefault("@context", "https://schema.org")
    merged["@id"] = node_id
    return merged


merged_pages = 0
merged_nodes = 0
detail = []

for rel in pages():
    path = os.path.join(ROOT, rel)
    doc = open(path, encoding="utf-8", errors="replace").read()
    if "LocalBusiness" not in doc:
        continue

    groups = defaultdict(lambda: defaultdict(list))
    for m, obj in parse(doc):
        for it in (obj if isinstance(obj, list) else [obj]):
            if isinstance(it, dict) and it.get("@type") in BUSINESS:
                groups[it.get("@id")][it["@type"]].append((m, it))

    targets = {i: g for i, g in groups.items()
               if i is not None and g.get("LocalBusiness") and g.get("Electrician")}
    if not targets:
        continue

    for node_id, g in targets.items():
        lb = g["LocalBusiness"][0][1]
        el = g["Electrician"][0][1]
        merged = build(lb, el, node_id)
        detail.append((rel, node_id, len(lb), len(el), len(merged)))
        merged_nodes += 1

    if APPLY:
        edits = []
        for node_id, g in targets.items():
            lb_m, lb = g["LocalBusiness"][0]
            el_m, el = g["Electrician"][0]
            first, second = (lb_m, el_m) if lb_m.start() < el_m.start() else (el_m, lb_m)
            edits.append((second.start(), second.end(), ""))
            edits.append((first.start(2), first.end(2),
                          "\n" + json.dumps(build(lb, el, node_id), indent=2, ensure_ascii=False) + "\n"))
        out = doc
        for s, e, payload in sorted(edits, key=lambda x: -x[0]):
            out = out[:s] + payload + out[e:]
        open(path, "w", encoding="utf-8").write(re.sub(r"\n{3,}", "\n\n", out))
        merged_pages += 1

print("mode:                       %s" % ("APPLY" if APPLY else "DRY RUN"))
print("pages merged:               %d" % merged_pages)
print("duplicate node pairs fixed: %d" % merged_nodes)
print()
print("sample (page, slug, lb_props + el_props -> merged):")
for rel, nid, a, b, c in detail[:10]:
    print("  %-36s %-26s %2d + %2d -> %2d" % (rel, (nid or "").replace("https://amyelectric.com", "") or "/", a, b, c))
if len(detail) > 10:
    print("  ... and %d more" % (len(detail) - 10))
