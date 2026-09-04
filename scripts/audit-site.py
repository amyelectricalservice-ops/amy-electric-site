import glob
import os
import re
import json
from xml.etree import ElementTree as ET

def audit():
    html_files = glob.glob('**/*.html', recursive=True)
    ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/')
    html_files = [f for f in sorted(html_files) if not any(f.startswith(p) for p in ignore_prefixes)]
    
    file_map = {}
    for f in html_files:
        if f.endswith('.html'):
            clean = f[:-5]
            file_map[clean] = f
            if clean.endswith('/index'):
                file_map[clean[:-5]] = f
                file_map[clean[:-6] + '/'] = f

    # Read Sitemap
    sitemap_urls = set()
    if os.path.exists('sitemap.xml'):
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for loc in root.findall('.//ns:loc', ns):
            url = loc.text.replace('https://amyelectric.com/', '')
            if url == '':
                url = 'index'
            sitemap_urls.add(url)

    missing_from_sitemap = []
    for f in html_files:
        if f == '404.html':
            continue
        clean = f[:-5]
        if clean.endswith('/index'):
            clean_dir = clean[:-5] # e.g. blog/
        else:
            clean_dir = clean
            
        if clean not in sitemap_urls and clean_dir not in sitemap_urls and (clean_dir.rstrip('/') + '/') not in sitemap_urls:
            missing_from_sitemap.append((f, clean))

    issues_by_file = {}
    sticky_bar_missing = []
    js_missing = []
    meta_desc_issues = []
    title_issues = []

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()

        file_issues = []

        # 1. Title
        t_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if not t_match:
            file_issues.append('Missing <title>')
            title_issues.append((f, 'Missing <title>'))
        elif not t_match.group(1).strip():
            file_issues.append('Empty <title>')
            title_issues.append((f, 'Empty <title>'))
        elif len(t_match.group(1).strip()) > 70:
            file_issues.append(f'Title too long ({len(t_match.group(1).strip())} chars)')
            title_issues.append((f, f'Title too long ({len(t_match.group(1).strip())} chars)'))

        # 2. Meta description
        d_match = re.search(r'<meta\s+(?:name=["\']description["\']\s+content=["\']([^"\']*)["\']|content=["\']([^"\']*)["\']\s+name=["\']description["\'])', content, re.IGNORECASE)
        if not d_match:
            file_issues.append('Missing meta description')
            meta_desc_issues.append((f, 'Missing meta description'))
        else:
            desc = d_match.group(1) or d_match.group(2)
            if len(desc) > 165:
                file_issues.append(f'Meta description too long ({len(desc)} chars)')
                meta_desc_issues.append((f, f'Meta description too long ({len(desc)} chars)'))
            elif len(desc) < 50:
                file_issues.append(f'Meta description too short ({len(desc)} chars)')
                meta_desc_issues.append((f, f'Meta description too short ({len(desc)} chars)'))

        # 3. Asset references
        if 'js/site.min.js' not in content and 'gallery.html' not in f:
            file_issues.append('Missing site.min.js reference')
            js_missing.append(f)

        # 4. Sticky mobile call bar
        if 'sticky-bar' not in content and f != '404.html' and 'privacy-policy' not in f:
            file_issues.append('Missing sticky mobile bar')
            sticky_bar_missing.append(f)

        if file_issues:
            issues_by_file[f] = file_issues

    print(f"=== AUDIT REPORT ===")
    print(f"Total production HTML pages: {len(html_files)}")
    print(f"Pages missing from sitemap: {len(missing_from_sitemap)}")
    print(f"Pages missing site.min.js: {len(js_missing)}")
    print(f"Pages missing sticky mobile bar: {len(sticky_bar_missing)}")
    print(f"Pages with meta description issues: {len(meta_desc_issues)}")
    print(f"Pages with title tag issues: {len(title_issues)}")

    if missing_from_sitemap:
        print("\n[!] Missing from sitemap.xml:")
        for f, clean in missing_from_sitemap:
            print(f"  - {f} ({clean})")

    if js_missing:
        print(f"\n[!] Missing site.min.js ({len(js_missing)}):")
        for m in js_missing:
            print(f"  - {m}")

    if sticky_bar_missing:
        print(f"\n[!] Missing sticky mobile bar ({len(sticky_bar_missing)}):")
        for m in sticky_bar_missing:
            print(f"  - {m}")

    if meta_desc_issues:
        print(f"\n[!] Meta Description Issues ({len(meta_desc_issues)}):")
        for f, iss in meta_desc_issues:
            print(f"  - {f}: {iss}")

    if title_issues:
        print(f"\n[!] Title Tag Issues ({len(title_issues)}):")
        for f, iss in title_issues:
            print(f"  - {f}: {iss}")

if __name__ == '__main__':
    audit()
