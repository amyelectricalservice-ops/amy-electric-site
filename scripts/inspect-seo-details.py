import glob
import json
import re

html_files = glob.glob('**/*.html', recursive=True)
ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/')
html_files = [f for f in sorted(html_files) if not any(f.startswith(p) for p in ignore_prefixes)]

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    
    # Check JSON-LD
    blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
        except Exception as e:
            print(f'JSON-LD Error in {f} block {i+1}: {e}')
            
    # Check img alt
    imgs = re.findall(r'<img\s+([^>]+)>', c, re.IGNORECASE)
    for img in imgs:
        if 'alt=' not in img:
            print(f'Missing alt in {f}: {img[:80]}')
        else:
            alt_match = re.search(r'alt=["\'](.*?)["\']', img)
            if alt_match and alt_match.group(1).strip() == '':
                print(f'Empty alt in {f}: {img[:80]}')
