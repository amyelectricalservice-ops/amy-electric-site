#!/usr/bin/env python3
"""Published EV price <-> estimate-engine drift inventory (report-only).

Usage:
  python3 scripts/audit-price-drift.py            # inventory, exit 0 always
  python3 scripts/audit-price-drift.py --detail   # also print the sentence each price sits in
  python3 scripts/audit-price-drift.py --strict   # exit 1 if any flagged range exists

The estimate engine (js/src/05-estimate-data.js) is the single source of truth
for what a lead is told. Published pages are hand-written and accumulate their
own numbers, so the two drift. This script reads the canonical EV charger
ranges out of the JS table and lists every price published next to a charger
phrase, grouped, so a maintainer can decide which copy to correct.

It never edits pages. A range is only *flagged* when it is neither the
canonical range nor a documented alternative scope (see ALT_SCOPES): several
services are legitimately published at two scopes, e.g. a NEMA 14-50 outlet
alone ($350-$600) versus the same outlet as part of a charger circuit
($350-$900). Flagging those as errors would just cry wolf.

Prices are found by two independent passes, because one alone left a hole
wide enough for ten below-canonical prices to ship while this script reported
zero drift. The proximity pass takes the first range within 160 chars of a
service phrase, stopping at a block or row boundary. The table pass reads the
structure instead: a charger named in a <th> claims its column, and a charger
named in a row's label cell claims that row's price — neither is reachable by
distance, since the name and the value are rows or columns apart. The table
pass matches a bare charger name (safe only inside a label cell, which cannot
mean "Tesla owners"), so "Hardwired" is required to sit beside an EV word or
it would price hardwired smoke/CO detectors as chargers.

Both passes still miss two shapes, deliberately rather than by accident: a
CSS-grid comparison table whose charger names are column headers with no
<table> around them, and prose that prices a charger without naming one
("a typical Level 2 installation costing $500-$900"). Those need a human
sweep — `grep -oE '\$[0-9,]+( to |–|-)\$[0-9,]+'` over the EV pages and a
glance at each, which is how the ten above were finally caught.

Two more near-matches are reported as `skip` rather than flagged, because the
figure next to the charger phrase is not that charger's own install price: a
combo row ("Wall Connector + NEMA 14-50 (dual)", priced for both) and a rebate
amount ("LADWP ChargeUp rebate paperwork ($1,000-$1,500 back)"). Both still
print, with the reason, so an exclusion can be audited instead of trusted.

Scope is deliberately limited to the three EV charger services. Panel and
permit prices are excluded: "panel upgrade" appears in meta descriptions and
in unrelated services (commercial panels, rewire comparisons), so proximity
matching there is noise rather than signal.

Also reports `sep_missing` — a price like "$350$550" with no separator, which
is published to users and to FAQ extraction exactly as shown.

Skips the mirror copy under amyelectric-site/ plus accessibility-audit/,
admin/ and node_modules/: those are not served pages.
"""
import glob
import html as htmlmod
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_PREFIX = ("amyelectric-site/", "accessibility-audit/", "admin/", "node_modules/")
SKIP_BASENAME = ("404.html", "seo-audit-report.html")

# service id -> phrases that introduce its published price
PHRASES = {
    "ev-nema-1450": ("NEMA 14-50",),
    "ev-tesla-wall": ("Tesla Wall Connector",),
    "ev-hardwired": ("Hardwired EVSE", "hardwired station", "Hardwired Installation"),
}

# Structure-based attribution, for prices no proximity window can reach. A
# feature table keeps a charger's name in a <th> or in a row's label cell and
# prints its price a column or several rows away, so the 160-char window
# around the phrase never sees it — which is how ten below-canonical prices
# shipped while the proximity pass reported zero drift. A bare name is safe
# here and only here: a cell that *is* the product label cannot mean "Tesla
# owners" or "a hardwired connection", the way it can in prose.
ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
CELL = re.compile(r"(t[hd])[^>]*>(.*?)</\1>", re.S)
LABEL_NAME = (
    ("ev-nema-1450", re.compile(r"NEMA\s*14-50", re.I)),
    ("ev-tesla-wall", re.compile(r"Tesla", re.I)),
    # Bare "Hardwired" also labels hardwired smoke/CO detectors and other
    # fixed devices, which are priced in the same tables — so it has to
    # sit beside an EV word to mean the charger.
    (
        "ev-hardwired",
        re.compile(
            r"Hardwired[^A-Za-z]{0,20}"
            r"(?:EVSE|EV\b|charger|station|installation|Wall Connector)",
            re.I,
        ),
    ),
)

# Ranges that differ from canonical on purpose, per service. Keys are
# (low, high) as published. Documented so the diff stays legible. The LADBS
# permit line ($150-$400) is legitimately printed right after each service
# phrase, so it is an accepted alternative for every EV service.
ALT_SCOPES = {
    # Outlet on its own vs. outlet as part of a whole charger circuit.
    "ev-nema-1450": {
        (350, 900): "outlet inside a full charger circuit, not the outlet alone",
        # blog/ev-charger-installation-cost-los-angeles.html itemises the
        # dedicated circuit and the permit on their own rows, so its charger
        # row is a component of the build, not the all-in install the engine
        # quotes. The same table's Tesla row is excluded for the same reason.
        (500, 1200): "cost-breakdown table that prices circuit and permit separately",
        # One sentence covers both charger types: "a NEMA 14-50 or hardwired
        # station in the standard $350 to $1,200 range" — the band spans both.
        (350, 1200): "shared NEMA-or-hardwired sentence spanning both subtypes",
    },
    "ev-tesla-wall": {
        # The cost-breakdown table above: its $1,200-$2,500 sits next to a
        # separate circuit row, so it is not the engine's all-in $500-$1,200.
        (1200, 2500): "cost-breakdown table that prices circuit and permit separately",
    },
    # The shared "NEMA 14-50 or hardwired station ... $350 to $1,200" sentence
    # is published under both charger types, so both may cite it.
    "ev-hardwired": {
        (350, 1200): "shared NEMA-or-hardwired range spanning both subtypes",
    },
}
PERMIT_ALT = (150, 400)
PERMIT_NOTE = "LADBS permit line printed beside the service"

# A label cell that names two chargers in one range is a combo price, not
# this service's own: "<td>Wall Connector + NEMA 14-50 (dual)</td>".
BUNDLE = re.compile(r"\+|\bdual\b", re.I)
# A rebate or incentive figure is money coming back, not an install price:
# "LADWP ChargeUp rebate paperwork ($1,000-$1,500 back)". Matched against the
# text ending at the price, so a permit or rebate line printed *after* a real
# service price can never swallow it.
REBATE = re.compile(r"(?:rebate|incentive|tax credit|chargeup)\b[^$]{0,40}$", re.I)

# A price with no separator at all: "$350$550". Published verbatim to users
# and to FAQ extraction, so it is reported rather than silently skipped.
GLUED = re.compile(r"\$\s?([0-9][0-9,]*)\$([0-9][0-9,]*)")
# Same defect with a bare space instead of no separator: "$350 $550" inside a
# <td class="price">. Whitespace only, so a correctly written
# "$350 &ndash; $550" or "$350 - $550" can never match.
GLUED_SPACED = re.compile(
    r"\$\s?([0-9]{1,3}(?:,[0-9]{3})*|[0-9]{3,9})[ \t]+\$([0-9]{1,3}(?:,[0-9]{3})*|[0-9]{3,9})"
)
# A price beyond one of these describes something else (next table row, next
# paragraph, next FAQ entry). Deliberately excludes </td>: within a single
# <tr> the label and its price sit in adjacent cells.
BLOCK_END = re.compile(r"</tr>|</p>|</li>|</h[1-6]>")

# Full thousands-groups only. The earlier "[0-9][0-9,]*" happily stopped at
# "$1" inside "$1,200", inventing ranges like $500-$1.
PRICE = re.compile(
    r"\$\s?([0-9]{1,3}(?:,[0-9]{3})*|[0-9]{3,9})\s?"
    r"(?:to|&#8211;|&ndash;|–|-|—)\s?\$?\s?"
    r"([0-9]{1,3}(?:,[0-9]{3})*|[0-9]{3,9})"
)
SVC = re.compile(
    r"\{\s*id:\s*'([^']+)'.*?baseLow:\s*([0-9]+).*?baseHigh:\s*([0-9]+)"
    r".*?permitHandling:\s*'([^']+)'",
    re.S,
)


def to_int(s):
    return int(s.replace(",", ""))


def canonical():
    """(service id) -> dict(low, high, handling) straight out of the JS data table."""
    with open(os.path.join(ROOT, "js", "src", "05-estimate-data.js"), encoding="utf-8") as fh:
        src = fh.read()
    out = {}
    for m in SVC.finditer(src):
        out[m.group(1)] = {
            "low": int(m.group(2)),
            "high": int(m.group(3)),
            "handling": m.group(4) or "unpublished",
        }
    return out


def pages():
    pats = ("*.html", "blog/*.html", "case-studies/*.html")
    out = []
    for p in pats:
        out.extend(glob.glob(os.path.join(ROOT, p)))
    return sorted(
        f
        for f in out
        if os.path.relpath(f, ROOT) not in SKIP_BASENAME
        and os.path.relpath(f, ROOT) not in SKIP_PREFIX
    )


def exclude_reason(label, pre):
    """Why a price printed beside a charger is not that charger's own — or None.

    Shared by the proximity pass and the table pass so the two can never
    disagree about a combo row or a rebate figure.
    """
    # Combo row: the label cell holds two charger names, so this range
    # prices both, not this one alone.
    if BUNDLE.search(label) and BUNDLE.search(label.split(">", 1)[-1]):
        return "combo row"
    # "$1,000-$1,500 back" beside a rebate word is the rebate, not what
    # the install costs.
    if REBATE.search(pre):
        return "rebate/incentive amount"
    return None


def table_prices(flat):
    """(service id, low, high, label, context) attributed by table structure.

    Two shapes, both invisible to the phrase pass:
      column  <th>Hardwired EVSE</th> ... <tr><td>Installation Cost</td>
                  <td>$500-$1,200</td>
              the header names the charger and the value sits in the same
              column further down the table.
      row     <td>Hardwired Charger Installation</td><td>$500-$1,200</td>
              the label cell is the product.
    """
    out = []
    for tbl in re.finditer(r"<table[^>]*>(.*?)</table>", flat, re.S):
        cols = {}  # column index -> service id, learned from the header row
        for row in ROW.finditer(tbl.group(1)):
            cells = [m.groups() for m in CELL.finditer(row.group(1))]
            if not cells:
                continue
            texts = [re.sub(r"<[^>]+>", "", t).strip() for _, t in cells]
            if any(tag == "th" for tag, _ in cells):
                # First name wins: "Tesla Wall Connector Gen 3 (hardwired)"
                # is a Tesla product, not a hardwired-generic one.
                for i, txt in enumerate(texts):
                    for sid, rx in LABEL_NAME:
                        if rx.search(txt):
                            cols.setdefault(i, sid)
                            break
                continue
            label = texts[0]
            row_sid = next((s for s, rx in LABEL_NAME if rx.search(label)), None)
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", row.group(1)))[:150]
            for i, txt in enumerate(texts):
                pm = PRICE.search(txt)
                if not pm:
                    continue
                # Column header wins when both name something, otherwise a
                # charger-named label cell prices every other cell in its row.
                sid = cols.get(i) or (row_sid if i > 0 else None)
                if not sid:
                    continue
                lo, hi = to_int(pm.group(1)), to_int(pm.group(2))
                if lo > hi:
                    lo, hi = hi, lo
                out.append((sid, lo, hi, label, ctx))
    return out


def scan():
    """Return (ranges, glued, excluded).

    ranges    {(service id, published low, published high): {page name: context}}
              — the sentence each price sits in, so a reviewer sees the scope
              rather than a bare number.
    glued     {service id: {page name: [verbatim broken prices]}}
    excluded  {(service id, low, high, why): {page name: context}} — prices near a
              charger phrase that are not that charger's own install price
              (combo rows, rebate amounts). Reported so the exclusions are
              auditable rather than silent.
    """
    found = {}
    glued = {}
    excluded = {}
    for path in pages():
        rel = os.path.relpath(path, ROOT)
        flat = htmlmod.unescape(re.sub(r"\s+", " ", open(path, encoding="utf-8", errors="replace").read()))
        for sid, phrases in PHRASES.items():
            for phrase in phrases:
                for m in re.finditer(re.escape(phrase), flat, re.I):
                    # Bounded-window search: slicing the string at 160 chars
                    # cuts numbers in half ("$500 to $1" from "$500 to $1,200").
                    # Search the whole document from the phrase and then reject
                    # matches that start too far away, so numbers stay intact.
                    p = g = None
                    limit = m.end() + 160
                    for cand in PRICE.finditer(flat, m.end()):
                        if cand.start() > limit:
                            break
                        # These tables print each charger's price in its own
                        # column/row, so a price past a block or row boundary
                        # describes a different charger (the NEMA phrase once
                        # picked up the hardwired column printed above it).
                        if BLOCK_END.search(flat, m.end(), cand.start()):
                            break
                        p = cand
                        break
                    for cand in GLUED.finditer(flat, m.end()):
                        if cand.start() > limit:
                            break
                        if BLOCK_END.search(flat, m.end(), cand.start()):
                            break
                        g = cand
                        break
                    for cand in GLUED_SPACED.finditer(flat, m.end()):
                        if cand.start() > limit:
                            break
                        if BLOCK_END.search(flat, m.end(), cand.start()):
                            break
                        if g is None or cand.start() < g.start():
                            g = cand
                        break
                    # A glued "$350$550" starts where a spaced one would, so
                    # whoever starts first is what the visitor reads.
                    if g is not None and (p is None or g.start() <= p.start()):
                        glued.setdefault(sid, {}).setdefault(rel, []).append(g.group(0).strip())
                        continue
                    if p:
                        lo, hi = to_int(p.group(1)), to_int(p.group(2))
                        if lo > hi:
                            lo, hi = hi, lo
                        ctx = re.sub(r"\s+", " ", flat[max(0, m.start() - 60) : p.end() + 70])
                        # Combo row: the label cell holds two charger names,
                        # so this range prices both, not this one alone.
                        cell = flat.rfind("<td", max(0, m.start() - 260), m.start())
                        label = flat[cell : p.start()] if cell != -1 else flat[m.start() : p.start()]
                        why = exclude_reason(label, flat[max(0, p.start() - 90) : p.start()])
                        if why:
                            excluded.setdefault((sid, lo, hi, why), {})[rel] = ctx
                            continue
                        found.setdefault((sid, lo, hi), {}).setdefault(rel, ctx)
        # Prices the proximity pass cannot see: attribute them from the
        # table's own structure instead.
        for sid, lo, hi, label, ctx in table_prices(flat):
            why = exclude_reason(label, label)
            if why:
                excluded.setdefault((sid, lo, hi, why), {})[rel] = ctx
                continue
            found.setdefault((sid, lo, hi), {}).setdefault(rel, ctx)
    return found, glued, excluded


def main():
    strict = "--strict" in sys.argv[1:]
    detail = "--detail" in sys.argv[1:]
    can = canonical()
    found, glued, excluded = scan()
    flagged = 0
    glued_total = 0

    print("=== Published EV charger pricing (canonical from 05-estimate-data.js) ===\n")
    for sid in PHRASES:
        if sid not in can:
            print(f"! {sid}: no canonical row found in the JS table")
            continue
        lo, hi = can[sid]["low"], can[sid]["high"]
        print(f"{sid}  canonical ${lo:,}-${hi:,}  (permit: {can[sid]['handling']})")
        rows = sorted(k for k in found if k[0] == sid)
        if not rows:
            print("    (no published price found next to its phrase)")
        for _, plo, phi in rows:
            pages_hit = found[(sid, plo, phi)]
            same = (plo, phi) == (lo, hi)
            alt = ALT_SCOPES.get(sid, {}).get((plo, phi))
            if not alt and (plo, phi) == PERMIT_ALT:
                # Only services that itemize their permit may print the permit
                # line; "included"/"unpublished" services must not.
                alt = PERMIT_NOTE if can[sid]["handling"] == "separate" else None
            mark = "  ok  " if same else ("  alt " if alt else "  DRIFT")
            note = f"  ({alt})" if alt else ("" if same else "  <-- differs from the engine")
            print(f"    {mark} ${plo:,}-${phi:,}{note}")
            for pg in sorted(pages_hit)[:4]:
                print(f"            {pg}")
                if detail:
                    print(f"                ...{pages_hit[pg]}...")
            if len(pages_hit) > 4:
                print(f"            ... +{len(pages_hit) - 4} more")
            if not same and not alt:
                flagged += len(pages_hit)

        for pg, prices in sorted(glued.get(sid, {}).items()):
            glued_total += len(prices)
            print(f"    BROKEN {', '.join(prices)}  (no separator; shown verbatim to visitors)")
            print(f"            {pg}")
        ex = sorted(k for k in excluded if k[0] == sid)
        for _, elo, ehi, why in ex:
            ex_pages = excluded[(sid, elo, ehi, why)]
            print(f"    skip ${elo:,}-${ehi:,}  ({why}; not this service's own price)")
            for pg in sorted(ex_pages)[:4]:
                print(f"            {pg}")
                if detail:
                    print(f"                ...{ex_pages[pg]}...")
        print()

    print(f"Flagged page/range pairs: {flagged}")
    print(f"Glued prices (missing separator): {glued_total}")
    print(f"Excluded near-matches (combo/rebate): {sum(len(v) for v in excluded.values())}")
    if strict and (flagged or glued_total):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
