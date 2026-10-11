#!/usr/bin/env python3
"""Published EV price <-> estimate-engine drift inventory (report-only).

Usage:
  python3 scripts/audit-price-drift.py            # inventory, exit 0 always
  python3 scripts/audit-price-drift.py --strict   # exit 1 if any flagged range exists

The estimate engine (js/src/05-estimate-data.js) is the single source of truth
for what a lead is told. Published pages are hand-written and accumulate their
own numbers, so the two drift. This script reads the canonical EV charger
ranges out of the JS table and lists every price published next to a charger
phrase, grouped, so a maintainer can decide which copy to correct.

It never edits pages. A range is only *flagged* when it is neither the
canonical range nor a documented alternative scope (see ALT_SCOPES): several
services are legitimately published at two scopes, e.g. a NEMA 14-50 outlet
alone ($350-$550) versus the same outlet as part of a charger circuit
($350-$900). Flagging those as errors would just cry wolf.

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

# Ranges that differ from canonical on purpose, per service. Keys are
# (low, high) as published. Documented so the diff stays legible. The LADBS
# permit line ($150-$400) is legitimately printed right after each service
# phrase, so it is an accepted alternative for every EV service.
ALT_SCOPES = {
    # Outlet on its own vs. outlet as part of a whole charger circuit.
    "ev-nema-1450": {(350, 900): "outlet inside a full charger circuit, not the outlet alone"},
    "ev-tesla-wall": {},
    "ev-hardwired": {},
}
PERMIT_ALT = (150, 400)
PERMIT_NOTE = "LADBS permit line printed beside the service"

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


def scan():
    """{(service id, published low, published high): set(page names)}, plus glued prices."""
    found = {}
    glued = {}
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
                        found.setdefault((sid, lo, hi), set()).add(rel)
    return found, glued


def main():
    strict = "--strict" in sys.argv[1:]
    can = canonical()
    found, glued = scan()
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
            pages_hit = sorted(found[(sid, plo, phi)])
            same = (plo, phi) == (lo, hi)
            alt = ALT_SCOPES.get(sid, {}).get((plo, phi))
            if not alt and (plo, phi) == PERMIT_ALT:
                # Only services that itemize their permit may print the permit
                # line; "included"/"unpublished" services must not.
                alt = PERMIT_NOTE if can[sid]["handling"] == "separate" else None
            mark = "  ok  " if same else ("  alt " if alt else "  DRIFT")
            note = f"  ({alt})" if alt else ("" if same else "  <-- differs from the engine")
            print(f"    {mark} ${plo:,}-${phi:,}{note}")
            for pg in pages_hit[:4]:
                print(f"            {pg}")
            if len(pages_hit) > 4:
                print(f"            ... +{len(pages_hit) - 4} more")
            if not same and not alt:
                flagged += len(pages_hit)

        for pg, prices in sorted(glued.get(sid, {}).items()):
            glued_total += len(prices)
            print(f"    BROKEN {', '.join(prices)}  (no separator; shown verbatim to visitors)")
            print(f"            {pg}")
        print()

    print(f"Flagged page/range pairs: {flagged}")
    print(f"Glued prices (missing separator): {glued_total}")
    if strict and (flagged or glued_total):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
