#!/usr/bin/env python3
"""Ensure all HTML files have CSS preload links."""
import glob, re, os

html_files = sorted(
    glob.glob('/home/amram/WEBSITE/*.html') +
    glob.glob('/home/amram/WEBSITE/blog/*.html')
)

fixed = 0
for path in html_files:
    rel = os.path.relpath(path, '/home/amram/WEBSITE')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = '../' if path.startswith('/home/amram/WEBSITE/blog/') else ''
    css_path = f"{prefix}css/style.min.css"
    preload_tag = f'<link rel="preload" as="style" href="{css_path}">'
    stylesheet_tag = f'<link rel="stylesheet" href="{css_path}">'

    if stylesheet_tag in content and preload_tag not in content:
        new_content = content.replace(stylesheet_tag, f'{preload_tag}\n{stylesheet_tag}')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"Fixed CSS preload in {rel}")

print(f"Total files updated with CSS preload: {fixed}")
