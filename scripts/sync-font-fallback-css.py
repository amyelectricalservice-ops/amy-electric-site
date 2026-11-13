#!/usr/bin/env python3
"""Add the metric-matched fallback families to the inlined critical CSS stacks.

The critical CSS embedded in every page declares both font stacks. Without the
fallback families there, the browser has nothing to swap *to* before the woff2
lands, so text reflows: the nav (desktop CLS 0.074) and body paragraphs
(mobile CLS ~0.19 on /book and /tesla-charger-installation).

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

# (family as written in the stack, its declared fallback, the metric family)
FAMILIES = [
    ('Barlow Condensed', 'Arial Narrow', 'Barlow Condensed Fallback'),
    ('Source Serif 4', 'Georgia', 'Source Serif Fallback'),
]
PATTERNS = [
    (fam, fb, metric,
     re.compile(
         r'(?P<q>["\'])(?P<fam>' + re.escape(fam) + r')(?P=q)'
         # the fallback may be quoted ("Arial Narrow") or bare (Georgia)
         r'(?P<sep>\s*,\s*)(?P<next>["\']?' + re.escape(fb) + r'["\']?)'
     ))
    for fam, fb, metric in FAMILIES
]


def patch(text):
    """Insert each metric family directly after its webfont, when absent."""
    count = 0
    for _fam, _fb, metric, pattern in PATTERNS:
        if metric in text:
            continue

        def repl(m, metric=metric):
            nonlocal count
            count += 1
            q = m.group('q')
            return (f'{q}{m.group("fam")}{q}{m.group("sep")}'
                    f'{q}{metric}{q}{m.group("sep")}{m.group("next")}')

        text = pattern.sub(repl, text)
    return text, count


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
        if '--cond' not in original and '--serif' not in original:
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
    print(f'{verb} {total} font stack(s) across {touched} file(s)')
    if check_only and total:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
