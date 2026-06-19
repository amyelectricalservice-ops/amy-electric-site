#!/usr/bin/env python3
"""
Build CSS from source modules.

Reads all numbered css/src/*.css files in order, concatenates them,
and writes the result to css/style.css (human-readable) and
css/style.min.css (minified for production).
"""

import os, re, glob

SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'css', 'src')
OUT_DEV = os.path.join(os.path.dirname(__file__), '..', 'css', 'style.css')
OUT_PROD = os.path.join(os.path.dirname(__file__), '..', 'css', 'style.min.css')

BANNER = (
    '/* AMY ELECTRIC — Stylesheet */\n'
    '/* Source: css/src/ — edit modules, not this file */\n'
    '/* Run: python3 scripts/build-css.py */\n'
)


def read_modules():
    files = sorted(glob.glob(os.path.join(SRC_DIR, '*.css')))
    if not files:
        raise SystemExit('No source modules found in css/src/')
    parts = []
    for f in files:
        with open(f) as fh:
            parts.append(fh.read())
    return BANNER + '\n'.join(parts)


def minify(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*{\s*', '{', css)
    css = re.sub(r'\s*}\s*', '}', css)
    css = re.sub(r'\s*;\s*', ';', css)
    css = re.sub(r'\s*:\s*', ':', css)
    css = re.sub(r'\s*,\s*', ',', css)
    css = re.sub(r'\s*>\s*', '>', css)
    css = re.sub(r'\s*\+\s*', '+', css)
    css = re.sub(r'\s*~\s*', '~', css)
    css = re.sub(r';}', '}', css)
    css = re.sub(r'@media\s*\(', '@media(', css)
    css = re.sub(r' !important', '!important', css)
    css = re.sub(r' 0px', ' 0', css)
    css = re.sub(r':0 ', ':0 ', css)
    return css.strip()


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
