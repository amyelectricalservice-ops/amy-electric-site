#!/usr/bin/env python3
"""Ensure all self-hosted fonts are preloaded across all HTML pages."""
import glob, re

FONT_FILES = (
    'BarlowCondensed-600.woff2',
    'BarlowCondensed-700.woff2',
    'BarlowCondensed-800.woff2',
    'SourceSerif4-400.woff2',
    'SourceSerif4-400italic.woff2',
)
FONT_PRELOAD = re.compile(r'<link rel="preload" as="font"[^>]*>\s*')

html_files = sorted(
    glob.glob('/home/amram/WEBSITE/*.html') +
    glob.glob('/home/amram/WEBSITE/blog/*.html')
)
html_files = [f for f in html_files if '/amyelectric-site/' not in f]

changed = 0

for filepath in html_files:
    with open(filepath) as f:
        content = f.read()

    # Remove existing font preloads, then insert one canonical block.
    new_content = FONT_PRELOAD.sub('', content)
    prefix = '../' if '/blog/' in filepath else ''
    keep = [
        f'<link rel="preload" as="font" href="{prefix}fonts/{font}" crossorigin>'
        for font in FONT_FILES
    ]

    # Find insertion point: before the first non-font preload
    # Insert right before the first image preload, or before <style>, or before </head>
    insert_before = [
        '<link rel="preload" as="image"',
        '<style>',
        '<link rel="preload" as="style"',
        '</head>'
    ]
    for marker in insert_before:
        pos = new_content.find(marker)
        if pos != -1:
            break

    if pos == -1:
        continue

    # Insert the kept preloads
    block = '\n'.join(keep) + '\n'
    new_content = new_content[:pos] + block + new_content[pos:]

    if new_content == content:
        continue

    with open(filepath, 'w') as f:
        f.write(new_content)

    changed += 1
    rel = '/'.join(filepath.split('/')[-2:])
    print(f'  {rel}: normalized to {len(keep)} font preloads')

print(f'\n{changed} files changed')