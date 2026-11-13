#!/usr/bin/env python3
"""Build js/estimator.min.js from js/estimator-widget.js.

Same regex pipeline as scripts/build-js.py so the bundle has no extra
toolchain. Never hand-edit js/estimator.min.js — edit the source and run this.

Run: python3 scripts/build-estimator.py [--check]
     --check exits 1 when the committed bundle is stale (used by CI).
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'js', 'estimator-widget.js')
OUT = os.path.join(ROOT, 'js', 'estimator.min.js')

BANNER = (
    '/* AMY ELECTRIC — homepage quote widget (built) */\n'
    '/* Source: js/estimator-widget.js — edit that, then run scripts/build-estimator.py */\n'
)


def minify(js):
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'//.*', '', js)
    js = re.sub(r'\s+', ' ', js)
    js = re.sub(r'\s*;\s*', ';', js)
    # NB: no whitespace compaction around , : { } — it also rewrites spaces
    # inside string literals ("2,000+ sq ft" became "2,000+sq ft" in the UI).
    return BANNER + js.strip() + '\n'


def main():
    with open(SRC, encoding='utf-8') as fh:
        source = fh.read()
    built = minify(source)
    check = '--check' in sys.argv
    with open(OUT, encoding='utf-8') as fh:
        current = fh.read()
    if check:
        if current != built:
            print('js/estimator.min.js is stale — run python3 scripts/build-estimator.py')
            sys.exit(1)
        print('js/estimator.min.js up to date')
        return
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(built)
    print(f'built js/estimator.min.js ({len(built)} bytes from {len(source)} source)')


if __name__ == '__main__':
    main()
