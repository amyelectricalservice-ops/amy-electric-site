#!/usr/bin/env python3
"""Normalise the font preload block on every HTML page.

Only three faces are preloaded: the two Barlow Condensed weights used in the
header/hero and the Source Serif 4 body weight. Preloading all five cost ~92 KB
of highest-priority fetches on a 4G connection and pushed LCP out by roughly
0.8 s in a 6x interleaved devtools-throttled test (LCP 1296 ms -> 448 ms).
The un-preloaded faces (Barlow Condensed 600 and the italic serif) still load
on demand from the @font-face rules in css/src/01-base.css.

Idempotent: re-running rewrites the same block. Repo-relative so it works in
worktrees.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRELOAD_FONTS = (
    'BarlowCondensed-700.woff2',
    'BarlowCondensed-800.woff2',
    'SourceSerif4-400.woff2',
)
FONT_PRELOAD = re.compile(r'<link rel="preload" as="font"[^>]*>\s*')

# Where the block goes: immediately before the first of these markers.
ANCHORS = (
    '<link rel="preload" as="image"',
    '<style>',
    '<link rel="preload" as="style"',
    '</head>',
)


def html_files():
    files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    files += sorted(glob.glob(os.path.join(ROOT, 'blog', '*.html')))
    files += sorted(glob.glob(os.path.join(ROOT, 'case-studies', '*.html')))
    return [f for f in files if '/amyelectric-site/' not in f]


def main():
    changed = 0
    for filepath in html_files():
        with open(filepath, encoding='utf-8') as fh:
            content = fh.read()

        new_content = FONT_PRELOAD.sub('', content)
        depth = os.path.relpath(filepath, ROOT).count(os.sep)
        prefix = '../' * depth
        block = ''.join(
            f'<link rel="preload" as="font" href="{prefix}fonts/{font}" crossorigin>\n'
            for font in PRELOAD_FONTS
        )

        pos = -1
        for marker in ANCHORS:
            pos = new_content.find(marker)
            if pos != -1:
                break
        if pos == -1:
            print(f'  skip (no insertion anchor): {filepath}')
            continue

        new_content = new_content[:pos] + block + new_content[pos:]
        if new_content == content:
            continue

        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        changed += 1
        print(f'  {os.path.relpath(filepath, ROOT)}: normalised to {len(PRELOAD_FONTS)} font preloads')

    print(f'\n{changed} files changed')


if __name__ == '__main__':
    main()
