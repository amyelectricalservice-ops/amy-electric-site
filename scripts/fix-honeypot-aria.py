#!/usr/bin/env python3
"""Move the honeypot decoy's aria-hidden from a CSS declaration to an attribute.

The spam trap on every form used to read:

    <div style="position:absolute;left:-9000px;aria-hidden:true">

`aria-hidden:true` inside a style attribute is not a CSS property, so browsers
drop it and the decoy "Website" label + input stay in the accessibility tree.
Screen-reader users hear a stray "Website" field on every form. The intent was
the attribute `aria-hidden="true"`, which removes the whole subtree from the
a11y tree (the input is already `tabindex="-1"`, so nothing tabbable is hidden).

Idempotent: files already carrying the attribute are left alone.

Run: python3 scripts/fix-honeypot-aria.py [--check]
"""
import glob
import re
import sys

IGNORE_PREFIXES = (
    'reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/',
    'accessibility-audit/', 'admin/', 'audit/', 'estimator-app/',
    'builder/', 'node_modules/', '.cloudflare/', '.wrangler/',
)

# Only the exact decoy wrapper is rewritten; anything else is reported, not guessed.
PATTERN = re.compile(
    r'style="(?P<pre>[^"]*?);?aria-hidden:true;?"',
)


def html_files():
    files = glob.glob('**/*.html', recursive=True)
    return [f for f in sorted(files) if not any(f.startswith(p) for p in IGNORE_PREFIXES)]


def fix(path, check_only=False):
    with open(path, encoding='utf-8') as fh:
        original = fh.read()
    if 'aria-hidden:true' not in original:
        return None

    count = original.count('aria-hidden:true')

    def repl(m):
        style = m.group('pre').rstrip(';')
        return f'style="{style}" aria-hidden="true"'

    fixed = PATTERN.sub(repl, original)
    leftover = fixed.count('aria-hidden:true')
    if leftover:
        raise SystemExit(
            f'{path}: {leftover} occurrence(s) did not match the known decoy pattern; '
            'fix them by hand rather than guessing'
        )
    if not check_only:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
    return count


def main():
    check_only = '--check' in sys.argv
    touched = 0
    total = 0
    for path in html_files():
        n = fix(path, check_only)
        if n:
            touched += 1
            total += n
    verb = 'would fix' if check_only else 'fixed'
    print(f'{verb} {total} occurrence(s) in {touched} file(s)')
    if check_only and total:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
