#!/usr/bin/env python3
"""Fix duplicate FAQ questions in FAQPage JSON-LD schema across city pages."""

import re, json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

html_files = sorted(glob.glob(os.path.join(ROOT, 'city-*.html')))

for filepath in html_files:
    filename = os.path.relpath(filepath, ROOT)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # Find all JSON-LD scripts
    def dedup_faq_schema(match):
        try:
            data = json.loads(match.group(1))
            if data.get('@type') != 'FAQPage':
                return match.group(0)
            
            entities = data.get('mainEntity', [])
            seen = set()
            unique = []
            for e in entities:
                name = e.get('name', '')
                if name in seen:
                    continue
                seen.add(name)
                unique.append(e)
            
            if len(unique) == len(entities):
                return match.group(0)  # no duplicates
            
            data['mainEntity'] = unique
            return '<script type="application/ld+json">\n' + json.dumps(data, indent=2) + '\n</script>'
        except:
            return match.group(0)
    
    html = re.sub(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        dedup_faq_schema,
        html,
        flags=re.DOTALL
    )
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  FIXED: {filename} — deduplicated FAQPage schema')

print('Done.')
