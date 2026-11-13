#!/usr/bin/env python3
"""Add the metric-matched 'Barlow Condensed Fallback' to the inlined --cond stack.

The critical CSS embedded in every page declares the condensed stack. Without
the fallback family there, the browser has nothing to swap *to* before the
woff2 lands, so `--cond` text reflows (desktop CLS 0.074 on the nav).

Idempotent: pages already carrying the fallback are skipped. Also updates the
city-page generator template so regenerated pages stay in sync.

Run: python3 scripts/sync-font-fallback-css.py [--check]
"""
import glob
import re
import sys

IGNORE_PREFIXES = (
    '.', 'reports/', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/',
    'accessibility-audit/', 'admin/', 'audit/', 'estimator-app/',
    'builder/', 'node_modules/', '.cloudflare/', '.wrangler/',
)

FALLBACK = 'Barlow Condensed Fallback'
# Matches "Barlow Condensed","Arial Narrow" with any spacing/quote style.
PATTERN = re.compile(
    r'(?P<q>["\'])(?P<fam>Barlow Condensed)(?P=q)(?P<sep>\s*,\s*)(?P<next>["\']Arial Narrow["\'])'
)


def patch(text):
    """Insert the fallback family after 'Barlow Condensed' when absent."""
    if FALLBACK in text:
        return text, 0

    count = 0

    def repl(m):
        nonlocal count
        count += 1
        q = m.group('q')
        return f'{q}{m.group("fam")}{q}{m.group("sep")}{q}{FALLBACK}{q}{m.group("sep")}{m.group("next")}'

    return PATTERN.sub(repl, text), count


def targets():
    files = [f for f in sorted(glob.glob('*.html'))]
    nested = [f for f in sorted(glob.glob('*/*.html'))
              if not any(f.startswith(p) for p in IGNORE_PREFIXES)]
    return files + nested


def main():
    check_only = '--check' in sys.argv
    touched = 0
    total = 0

    for path in targets():
        with open(path, encoding='utf-8') as fh:
            original = fh.read()
        if '--cond' not in original:
            continue
        fixed, n = patch(original)
        if not n:
            continue
        touched += 1
        total += n
        if not check_only:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(fixed)

    # Generator template + CSS source must stay in sync with the pages.
    for path in ('scripts/generate-city-pages.py', 'css/src/01-base.css'):
        with open(path, encoding='utf-8') as fh:
            original = fh.read()
        fixed, n = patch(original)
        if n:
            touched += 1
            total += n
            if not check_only:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(fixed)

    verb = 'would update' if check_only else 'updated'
    print(f'{verb} {total} --cond stack(s) across {touched} file(s)')
    if check_only and total:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
