#!/usr/bin/env python3
"""Remove internal links that point at pages which do not exist.

The city template emits "Also serving" and "Electrician Services Near X" link
lists built from a full LA city inventory, but only cities that actually got a
page were created. Two failure modes:
  - slug never got a page                   -> drop the link
  - slug mangled during generation          -> repair the href when the page exists
    and is not already linked on the page
    ("city-echopark" -> city-echo-park, "city- Century-city" -> city-century-city)

Only the two nearby-cities containers are touched, and only when a dead link is
actually present, so the diff stays limited to real fixes. Idempotent.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANCHOR = re.compile(r'<a\s+href="([^"]+)"[^>]*>.*?</a>', re.S)
ONLY_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._~/-]*$")

stats = {"dropped": 0, "repaired": 0, "blocks_removed": 0, "files": 0}


def exists(slug):
    slug = slug.strip().split("#")[0].split("?")[0]
    if not slug or not ONLY_SLUG.match(slug):
        return False
    for cand in (slug, slug.rstrip("/") + ".html", os.path.join(slug, "index.html")):
        if os.path.isfile(os.path.join(ROOT, cand)):
            return True
    return False


def target_of(href):
    return href[1:] if href.startswith("/") else href


def alternate(slug, page_hrefs):
    fixed = slug.strip().replace(" ", "-")
    if fixed == slug or not exists(fixed):
        return None
    alt = "/" + fixed
    return None if alt in page_hrefs else alt


def scrub_inline(block, page_hrefs):
    """Rebuild an 'Also serving: a · b · c' paragraph without dead links."""
    m = re.match(r"^(\s*(?:Also\s+serving:\s*)?)", block)
    lead = m.group(1) if m else ""
    items = []
    for a in ANCHOR.finditer(block):
        href = a.group(1)
        slug = target_of(href)
        if exists(slug):
            items.append(a.group(0))
            continue
        alt = alternate(slug, page_hrefs)
        if alt:
            page_hrefs.add(alt)
            stats["repaired"] += 1
            items.append(a.group(0).replace('href="%s"' % href, 'href="%s"' % alt, 1))
            continue
        stats["dropped"] += 1
    return (lead + " · ".join(items)) if items else None


def scrub_section(section, page_hrefs):
    """Drop standalone anchor lines pointing at dead pages; keep everything else."""
    out = []
    for line in section.split("\n"):
        s = line.strip()
        found = ANCHOR.findall(s)
        if s.startswith("<a ") and s.endswith("</a>") and len(found) == 1:
            slug = target_of(found[0])
            if not exists(slug):
                alt = alternate(slug, page_hrefs)
                if alt:
                    page_hrefs.add(alt)
                    stats["repaired"] += 1
                    out.append(line.replace('href="%s"' % found[0], 'href="%s"' % alt, 1))
                    continue
                stats["dropped"] += 1
                continue
        out.append(line)
    return "\n".join(out)


PARA = re.compile(r'(?is)^[ \t]*<p class="nearby-cities">(.*?)</p>[ \t]*$', re.M)
SECTION = re.compile(r'(?is)^[ \t]*<section class="nearby-cities".*?</section>[ \t]*$', re.M)

touched = []
for name in sorted(os.listdir(ROOT)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(ROOT, name)
    with open(path, encoding="utf-8") as fh:
        orig = html = fh.read()
    if "nearby-cities" not in html:
        continue
    page_hrefs = set(re.findall(r'href="(/[^"]+)"', html))

    def do_para(m):
        rebuilt = scrub_inline(m.group(1), page_hrefs)
        if rebuilt is None:
            stats["blocks_removed"] += 1
            return ""
        return '    <p class="nearby-cities">' + rebuilt + "</p>"

    before = stats["dropped"] + stats["repaired"]
    html = PARA.sub(do_para, html)
    html = SECTION.sub(lambda m: scrub_section(m.group(0), page_hrefs), html)
    if stats["dropped"] + stats["repaired"] > before:
        html = re.sub(r"\n{3,}", "\n\n", html)

    if html != orig:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        touched.append(name)
        stats["files"] += 1

for k in ("dropped", "repaired", "blocks_removed", "files"):
    print("  %-14s %d" % (k, stats[k]))

dead = {}
for name in sorted(os.listdir(ROOT)):
    if not name.endswith(".html"):
        continue
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        h = fh.read()
    for href in re.findall(r'<a\s+href="([^"]+)"', h):
        if href.startswith(("http", "mailto:", "tel:", "sms:", "#", "/")):
            continue
        if not exists(href):
            dead.setdefault(href, []).append(name)
print("  VERIFY remaining dead relative hrefs: %d distinct" % len(dead))
for k, v in list(dead.items())[:15]:
    print("     %-30s x%d %s" % (k, len(v), v[:3]))
sys.exit(1 if dead else 0)
