#!/usr/bin/env python3
"""
Build JS from source modules.

Reads all numbered js/src/*.js files in order, concatenates them,
and writes the result to js/site.js (human-readable) and
js/site.min.js (minified for production).
"""

import os, re, glob

SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'js', 'src')
OUT_DEV = os.path.join(os.path.dirname(__file__), '..', 'js', 'site.js')
OUT_PROD = os.path.join(os.path.dirname(__file__), '..', 'js', 'site.min.js')

BANNER = (
    '/* AMY ELECTRIC — Site Scripts */\n'
    '/* Source: js/src/ — edit modules, not this file */\n'
    '/* Run: python3 scripts/build-js.py */\n'
)


def read_modules():
    files = sorted(glob.glob(os.path.join(SRC_DIR, '*.js')))
    if not files:
        raise SystemExit('No source modules found in js/src/')
    parts = []
    for f in files:
        with open(f) as fh:
            parts.append(fh.read())
    return BANNER + '\n'.join(parts)


def minify(js):
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'//.*', '', js)
    js = re.sub(r'\s+', ' ', js)
    js = re.sub(r'\s*;\s*', ';', js)
    js = re.sub(r'\s*{\s*', '{', js)
    js = re.sub(r'\s*}\s*', '}', js)
    js = re.sub(r'\s*\(\s*', '(', js)
    js = re.sub(r'\s*\)\s*', ')', js)
    js = re.sub(r'\s*=\s*', '=', js)
    js = re.sub(r'\s*===\s*', '===', js)
    js = re.sub(r'\s*!==\s*', '!==', js)
    js = re.sub(r'\s*[+-]\s*', lambda m: m.group(0), js)
    return js.strip()


def main():
    full = read_modules()
    with open(OUT_DEV, 'w') as f:
        f.write(full)
    with open(OUT_PROD, 'w') as f:
        f.write(minify(full))
    dev_size = len(full)
    prod_size = len(open(OUT_PROD).read())
    print(f'Wrote {OUT_DEV} ({dev_size} bytes)')
    print(f'Wrote {OUT_PROD} ({prod_size} bytes, {100 - (prod_size/dev_size*100):.0f}% smaller)')


if __name__ == '__main__':
    main()
