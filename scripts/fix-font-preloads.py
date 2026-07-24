#!/usr/bin/env python3
"""Reduce font preloads from 5 to 2 (BC-800 + SS4-400) across all pages."""
import glob, re

KEEP_FONTS = {'BarlowCondensed-800.woff2', 'SourceSerif4-400.woff2'}
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

    # Find all font preloads
    preloads = FONT_PRELOAD.findall(content)
    unique = list(dict.fromkeys(p.strip() for p in preloads))  # deduplicate, preserve order

    if not unique:
        continue

    # Filter to keep only critical fonts
    keep = [p for p in unique if any(k in p for k in KEEP_FONTS)]
    dropped = len(unique) - len(keep)

    if dropped == 0 and len(unique) < 6:
        continue  # no change needed

    # Remove ALL font preloads, then re-insert kept ones
    new_content = FONT_PRELOAD.sub('', content)

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
    block = '\n'.join(p.strip() for p in keep) + '\n'
    new_content = new_content[:pos] + block + new_content[pos:]

    with open(filepath, 'w') as f:
        f.write(new_content)

    changed += 1
    rel = '/'.join(filepath.split('/')[-2:])
    print(f'  {rel}: {len(unique)} preloads → {len(keep)} ({dropped} dropped)')

print(f'\n{changed} files changed')