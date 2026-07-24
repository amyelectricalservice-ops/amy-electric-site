#!/usr/bin/env python3
"""Replace @type Electrician with LocalBusiness in all JSON-LD blocks."""
import re, glob, os

# Find all HTML files
html_files = sorted(
    glob.glob('/home/amram/WEBSITE/*.html') +
    glob.glob('/home/amram/WEBSITE/blog/*.html')
)

# Exclude amyelectric-site
html_files = [f for f in html_files if '/amyelectric-site/' not in f]

changed = 0
total_replacements = 0

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Count occurrences before
    before = content.count('"@type": "Electrician"')
    # Also handle compact format: "type":"Electrician" or @type: "Electrician"
    before += content.count('"@type":"Electrician"')
    
    if before == 0:
        continue
    
    # Replace only @type values
    new_content = re.sub(
        r'"@type"\s*:\s*"Electrician"',
        '"@type": "LocalBusiness"',
        content
    )
    
    after = new_content.count('"@type": "LocalBusiness"')
    replacements = before
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        changed += 1
        total_replacements += replacements
        rel = os.path.relpath(filepath, '/home/amram/WEBSITE')
        print(f"  {rel}: {replacements} replacements")

print(f"\nTotal: {changed} files changed, {total_replacements} replacements")
