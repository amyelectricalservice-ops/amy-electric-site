#!/usr/bin/env python3
"""Comprehensive SEO audit fixes — July 23, 2026.

Fixes:
1. Remove duplicate FAQ <details> from 16 city pages
2. Add Service schema to 5 service pages missing it
3. Add SpeakableSpecification to 15 service pages missing it
4. Add areaServed to service/city Electrician schemas
5. Standardize phone format to +1-818-302-5614
6. Add loading="lazy" to images missing it
7. Fix empty BreadcrumbList URLs on gallery/privacy-policy
"""

import re, json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fix_duplicate_faq(html):
    """Remove duplicate <details class="faq-item"> blocks."""
    # Split by <details class="faq-item"> and reconstruct
    parts = re.split(r'(<details class="faq-item">)', html)
    if len(parts) <= 3:
        return html, 0
    
    seen = set()
    result = [parts[0]]  # everything before first <details>
    removed = 0
    
    i = 1
    while i < len(parts):
        if parts[i] == '<details class="faq-item">':
            content = parts[i + 1] if i + 1 < len(parts) else ''
            # Extract summary text for dedup
            summary_match = re.search(r'<summary[^>]*>(.*?)</summary>', content, re.DOTALL)
            key = summary_match.group(1).strip() if summary_match else content[:100]
            
            if key in seen:
                removed += 1
                i += 2  # skip <details> tag and content
                continue
            seen.add(key)
            result.append(parts[i])
            result.append(content)
        i += 1
    
    if removed:
        return ''.join(result), removed
    return html, 0


def make_service_schema(info):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": info['name'],
        "description": info['description'],
        "serviceType": info['serviceType'],
        "provider": {
            "@type": "Electrician",
            "name": "AMY Electric",
            "url": "https://amyelectric.com"
        },
        "areaServed": {
            "@type": "City",
            "name": "Los Angeles"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "priceRange": "$$"
        },
        "url": info['url']
    }, indent=2)


SERVICE_SCHEMAS = {
    'breaker-tripping.html': {
        'name': 'Circuit Breaker Tripping Repair',
        'description': 'Diagnosis and repair of repeatedly tripping circuit breakers in Los Angeles homes and businesses. Same-day service by licensed C-10 electrician.',
        'serviceType': 'Electrical Repair',
        'url': 'https://amyelectric.com/breaker-tripping',
    },
    'burning-smell-panel.html': {
        'name': 'Burning Smell from Electrical Panel',
        'description': 'Emergency diagnosis of burning smells from electrical panels in Los Angeles. Licensed C-10 electrician. Same-day dispatch.',
        'serviceType': 'Emergency Electrical Service',
        'url': 'https://amyelectric.com/burning-smell-panel',
    },
    'emergency-electrician.html': {
        'name': '24/7 Emergency Electrician',
        'description': '24/7 emergency electrical service in Los Angeles. Power outages, sparking panels, downed wires. Same-day dispatch by licensed C-10 electrician.',
        'serviceType': 'Emergency Electrical Service',
        'url': 'https://amyelectric.com/emergency-electrician',
    },
    'power-outage-repair.html': {
        'name': 'Power Outage Repair',
        'description': 'Diagnosis and repair of residential power outages in Los Angeles. LADWP coordination, panel repair, and full electrical restoration.',
        'serviceType': 'Electrical Repair',
        'url': 'https://amyelectric.com/power-outage-repair',
    },
    'same-day-electrical-repair.html': {
        'name': 'Same-Day Electrical Repair',
        'description': 'Same-day electrical repair service in Los Angeles. Fast diagnostics and repairs by licensed C-10 electrician.',
        'serviceType': 'Electrical Repair',
        'url': 'https://amyelectric.com/same-day-electrical-repair',
    },
}


def add_area_served(html):
    """Add areaServed to Electrician schema if missing."""
    if '"areaServed"' in html:
        return html, False
    # Find priceRange in Electrician schema and add areaServed after it
    pattern = r'("priceRange":\s*"\$\$")(\s*\})'
    match = re.search(pattern, html)
    if match:
        insert = ',\n  "areaServed": {\n    "@type": "City",\n    "name": "Los Angeles"\n  }'
        new_html = html[:match.start(2)] + insert + html[match.start(2):]
        return new_html, True
    return html, False


def add_speakable(html):
    """Add SpeakableSpecification to Electrician schema if missing."""
    if '"SpeakableSpecification"' in html:
        return html, False
    # Add before hasCredential
    pattern = r'("hasCredential")'
    match = re.search(pattern, html)
    if match:
        speakable = '"speakable": {\n    "@type": "SpeakableSpecification",\n    "cssSelector": [".page-hero h1", ".page-hero p"]\n  },\n  '
        new_html = html[:match.start(1)] + speakable + html[match.start(1):]
        return new_html, True
    return html, False


def fix_phone_format(html):
    """Standardize phone format in JSON-LD."""
    old = '"telephone": "+18183025614"'
    new = '"telephone": "+1-818-302-5614"'
    if old in html:
        return html.replace(old, new), True
    return html, False


def fix_lazy_loading(html):
    """Add loading='lazy' to <img> tags missing it."""
    count = 0
    def add_lazy(match):
        nonlocal count
        tag = match.group(0)
        if 'loading=' in tag:
            return tag
        if 'hero-electrician' in tag or 'fetchpriority' in tag:
            return tag
        tag = tag[:-1] + ' loading="lazy" decoding="async">'
        count += 1
        return tag
    new_html = re.sub(r'<img [^>]+>', add_lazy, html)
    return new_html, count


def fix_breadcrumb_urls(html, filename):
    """Fix empty/null BreadcrumbList item URLs."""
    changed = False
    if filename == 'gallery.html':
        old = '"item": ""'
        new = '"item": "https://amyelectric.com/gallery"'
        if old in html:
            html = html.replace(old, new)
            changed = True
    elif filename == 'privacy-policy.html':
        old = '"item": ""'
        new = '"item": "https://amyelectric.com/privacy-policy"'
        if old in html:
            html = html.replace(old, new)
            changed = True
    if filename == 'city-los-angeles.html':
        old = '"item": null'
        new = '"item": "https://amyelectric.com/city-los-angeles"'
        if old in html:
            html = html.replace(old, new)
            changed = True
    return html, changed


def main():
    html_files = sorted(glob.glob(os.path.join(ROOT, '*.html')) + 
                        glob.glob(os.path.join(ROOT, 'blog', '*.html')))
    
    total_fixes = 0
    
    for filepath in html_files:
        filename = os.path.relpath(filepath, ROOT)
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        html = original
        file_fixes = []
        
        # Fix 1: Duplicate FAQ in city pages
        if filename.startswith('city-') and filename.endswith('.html'):
            html, removed = fix_duplicate_faq(html)
            if removed:
                file_fixes.append(f'removed {removed} duplicate FAQ items')
        
        # Fix 2: Add Service schema
        if filename in SERVICE_SCHEMAS:
            if '"@type": "Service"' not in html and '"@type":"Service"' not in html:
                schema = make_service_schema(SERVICE_SCHEMAS[filename])
                head_end = html.find('</head>')
                if head_end > 0:
                    last_script = html.rfind('</script>', 0, head_end)
                    if last_script > 0:
                        insert_pos = last_script + len('</script>')
                        html = html[:insert_pos] + '\n<script type="application/ld+json">\n' + schema + '\n</script>' + html[insert_pos:]
                        file_fixes.append('added Service schema')
        
        # Fix 3: areaServed on service/city pages (not index, blog, special)
        if (filename.endswith('.html') and 
            not filename.startswith('blog/') and 
            not filename.startswith('city-') and
            filename not in ['index.html', 'gallery.html', 'testimonials.html', 'privacy-policy.html']):
            html, added = add_area_served(html)
            if added:
                file_fixes.append('added areaServed')
        
        # Fix 3b: areaServed on city pages
        if filename.startswith('city-') and filename.endswith('.html'):
            html, added = add_area_served(html)
            if added:
                file_fixes.append('added areaServed')
        
        # Fix 4: SpeakableSpecification on service pages
        if (filename.endswith('.html') and 
            not filename.startswith('blog/') and
            filename not in ['index.html', 'gallery.html', 'testimonials.html', 'privacy-policy.html']):
            html, added = add_speakable(html)
            if added:
                file_fixes.append('added SpeakableSpecification')
        
        # Fix 5: Phone format
        html, fixed = fix_phone_format(html)
        if fixed:
            file_fixes.append('standardized phone format')
        
        # Fix 6: Lazy loading
        html, count = fix_lazy_loading(html)
        if count:
            file_fixes.append(f'added loading="lazy" to {count} images')
        
        # Fix 7: Breadcrumb URLs
        html, fixed = fix_breadcrumb_urls(html, filename)
        if fixed:
            file_fixes.append('fixed BreadcrumbList URL')
        
        if html != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            total_fixes += len(file_fixes)
            print(f'  FIXED: {filename}')
            for fix in file_fixes:
                print(f'    + {fix}')
    
    print(f'\n{"="*60}')
    print(f'Total fixes applied: {total_fixes}')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
