#!/usr/bin/env python3
"""Add idempotent 'Related guides' cross-link blocks (<!-- related-guides -->).

- Blog post  -> top-2 related posts by title-token overlap.
- Thin service page (<=2 inbound, curated list) -> top-3 related posts.
- Inserts before </main> (fallback: before <footer). Reruns replace in place.
"""
import glob
import os
import re

STOP = set("""a an the and or of to in on for with is are was were be by at from
as it its this that these those you your we our they their he she his her
how what when where which who why vs via do does did can will your my our
los angeles la california ca cost guide complete best top new""".split())

def tokens(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}

def title_of(fn):
    t = open(fn, encoding="utf-8", errors="replace").read()
    m = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
    title = (m.group(1).strip() if m else fn)
    return re.sub(r"\s*[|\-–—]\s*AMY.*$", "", title).strip()

def page_url(fn):
    fn = fn.replace(os.sep, "/")
    if fn == "index.html":
        return "/"
    if fn.endswith("/index.html"):
        return "/" + fn[:-11].rstrip("/")
    if fn.endswith(".html"):
        return "/" + fn[:-5]
    return "/" + fn

def href_for(src, target_fn):
    # extensionless relative href from src's directory
    rel = os.path.relpath(target_fn, os.path.dirname(src) or ".").replace(os.sep, "/")
    if rel.endswith(".html"):
        rel = rel[:-5]
    if rel.endswith("/index"):
        rel = rel[:-5] or "./"
    return rel

def block(links):
    items = "\n".join(f'    <li><a href="{h}">{t}</a></li>' for h, t in links)
    return (f'<!-- related-guides -->\n<section class="related-guides" aria-label="Related guides">\n'
            f'  <div class="wrap">\n    <h2>Related guides</h2>\n    <ul>\n{items}\n    </ul>\n  </div>\n</section>\n')

def inject(fn, section):
    p = open(fn, encoding="utf-8", errors="replace").read()
    p = re.sub(r"<!-- related-guides -->\s*<section class=\"related-guides\".*?</section>\n?", "", p, flags=re.S)
    if "</main>" in p:
        p = p.replace("</main>", section + "</main>", 1)
    else:
        p = p.replace("<footer", section + "<footer", 1)
    open(fn, "w", encoding="utf-8").write(p)

posts = sorted(glob.glob("blog/*.html"))
toks = {f: tokens(title_of(f)) for f in posts}

# blog -> blog
for f in posts:
    scored = []
    for g in posts:
        if g == f:
            continue
        s = len(toks[f] & toks[g])
        if s >= 1:
            scored.append((s, g))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = [(href_for(f, g), title_of(g)) for _, g in scored[:2]]
    if top:
        inject(f, block(top))
        print(f"blog+2 {f} <- {[t for _, t in top]}")

# service -> blog (thin money pages)
thin_services = [
    "commercial-ev-fleet-charging.html", "electrical-permit-cost-los-angeles.html",
    "home-automation-electrical.html", "ladwp-electrical-guide.html",
    "portable-vs-standby-generator.html", "recessed-lighting-installation.html",
    "200-amp-panel-upgrade.html", "adu-electrical.html", "electrical-repair.html",
    "commercial-electrical.html", "tesla-charger-installation.html",
    "lighting-installation.html", "subpanel-installation.html",
    "smoke-co-detector-installation.html", "ceiling-fan-installation.html",
    "generator-transfer-switch.html", "surge-protection.html",
    "outlet-switch-installation.html", "dedicated-circuits.html",
    "smart-home-electrical.html",
]
for f in thin_services:
    if not os.path.exists(f):
        continue
    ft = tokens(title_of(f))
    scored = []
    for g in posts:
        s = len(ft & toks[g])
        if s >= 1:
            scored.append((s, g))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = [(href_for(f, g), title_of(g)) for _, g in scored[:3]]
    if top:
        inject(f, block(top))
        print(f"svc+{len(top)} {f}")
