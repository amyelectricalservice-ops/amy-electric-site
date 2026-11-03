#!/usr/bin/env python3
"""
Sync the header navigation to one canonical menu across every production page.

Before this script the site shipped 29 different header navs (4 to 31 links
each) — which menu a visitor saw depended on which page they landed on. This
rewrites the <nav> inside <header> on every page from a single source of truth,
computing the relative prefix from the file's depth (root = '', blog/ and
case-studies/ = '../').

Idempotent: running it twice produces no diff. `--check` exits 1 if any page is
out of sync (usable as a CI gate).

Usage:
    python3 scripts/sync-nav.py            # rewrite in place
    python3 scripts/sync-nav.py --check    # report drift, change nothing
"""

import glob
import os
import re
import sys

# Pages that are not part of the deployed site (mirrors scripts/audit-site.py).
IGNORE_PREFIXES = (
    'reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/',
    'accessibility-audit/', 'admin/', 'audit/',
    'node_modules/', '.cloudflare/', '.wrangler/',
)

# ── The menu ──────────────────────────────────────────────────────────────
# Seven top-level destinations. Everything else lives behind "More" so the
# header stops wrapping to three rows at 1140px.
PRIMARY = [
    ('services',                 'Services'),
    ('ev-charger-installation',  'EV Chargers'),
    ('panel-upgrade',            'Panel Upgrades'),
    ('electrical-repair',        'Repairs'),
    ('service-areas',            'Service Areas'),
    ('reviews',                  'Reviews'),
    ('blog/',                    'Blog'),
]

# Two columns inside the "More" panel. Each entry is (label, [(href, text), ...]).
MORE_COL_1 = [
    ('Services', [
        ('commercial-electrical',        'Commercial Electrical'),
        ('emergency-electrician-los-angeles', 'Emergency Electrician'),
        ('lighting-installation',        'Lighting'),
        ('whole-home-rewiring',          'Whole-Home Rewiring'),
        ('generator-transfer-switch',    'Generators &amp; Transfer Switches'),
        ('surge-protection',             'Surge Protection'),
        ('tesla-charger-installation',   'Tesla Charger'),
    ]),
]

MORE_COL_2 = [
    ('Areas & Company', [
        ('city-los-angeles', 'Los Angeles'),
        ('gallery',          'Project Gallery'),
        ('about',            'About Amram'),
        ('get-quote',        'Get a Quote'),
    ]),
    ('Popular Guides', [
        ('blog/is-your-home-ev-ready-los-angeles', 'Is Your Home EV Ready?'),
        ('blog/ev-charger-installation-cost-la',   'EV Charger Installation Cost'),
        ('blog/whole-home-rewiring-cost-la',       'Whole-Home Rewiring Cost'),
        ('blog/panel-upgrade-cost-los-angeles',    'Panel Upgrade Cost'),
    ]),
]

BOOK_LABEL = '\U0001F4C5 Book Online'  # 📅 Book Online — hamburger menu only
PHONE = 'tel:18183025614'


def render_nav(prefix):
    """Return the canonical <nav> block for a page at the given relative prefix."""
    out = [
        '    <nav class="main-nav" aria-label="Main navigation">',
    ]
    for href, text in PRIMARY:
        out.append(f'      <a href="{prefix}{href}">{text}</a>')

    out.append('      <details class="nav-more">')
    out.append('        <summary>More</summary>')
    out.append('        <div class="nav-more-panel">')

    for col in (MORE_COL_1, MORE_COL_2):
        out.append('          <div class="nav-more-col">')
        for label, links in col:
            out.append(f'            <div class="nav-more-label">{label}</div>')
            for href, text in links:
                out.append(f'            <a href="{prefix}{href}">{text}</a>')
        out.append('          </div>')

    out.append('        </div>')
    out.append('      </details>')
    out.append(f'      <a href="{prefix}book" class="nav-book">{BOOK_LABEL}</a>')
    out.append(f'      <a href="{PHONE}" class="nav-cta">Call Now</a>')
    out.append('    </nav>')
    return '\n'.join(out)


HEADER_RE = re.compile(r'(<header\b.*?</header>)', re.S)
NAV_RE = re.compile(r'[ \t]*<nav\b[^>]*>.*?</nav>', re.S)


def production_files():
    files = sorted(glob.glob('**/*.html', recursive=True))
    return [f for f in files if not any(f.startswith(p) for p in IGNORE_PREFIXES)]


def prefix_for(path):
    depth = path.count('/')
    return '../' * depth


def sync(path, apply=True):
    """Return True if the page was (or would be) changed."""
    src = open(path, encoding='utf-8').read()
    m = HEADER_RE.search(src)
    if not m:
        return False
    header = m.group(1)
    if not NAV_RE.search(header):
        return False

    new_header = NAV_RE.sub(render_nav(prefix_for(path)), header, count=1)
    if new_header == header:
        return False
    if apply:
        open(path, 'w', encoding='utf-8').write(src[:m.start(1)] + new_header + src[m.end(1):])
    return True


def main():
    check = '--check' in sys.argv[1:]
    files = production_files()
    changed = [f for f in files if sync(f, apply=not check)]

    if check:
        if changed:
            print(f'NAV DRIFT — {len(changed)} page(s) do not match the canonical nav:')
            for f in changed[:20]:
                print('  ', f)
            if len(changed) > 20:
                print(f'   ... +{len(changed) - 20} more')
            return 1
        print(f'NAV OK — all {len(files)} pages match the canonical nav.')
        return 0

    print(f'Synced {len(changed)} of {len(files)} pages to the canonical nav.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
