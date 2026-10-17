import glob
import os
import re
import json
import sys
from xml.etree import ElementTree as ET

def audit():
    html_files = glob.glob('**/*.html', recursive=True)
    ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/',
                       'accessibility-audit/', 'admin/', 'audit/',
                       'node_modules/', '.cloudflare/', '.wrangler/')
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

    def canon_path(f):
        """Canonical URL path of an HTML file (e.g. '/emergency-electrician-los-angeles'),
        or None when the page has no rel=canonical."""
        try:
            with open(f, encoding='utf-8', errors='replace') as fh:
                head = fh.read(8000)
        except OSError:
            return None
        m = re.search(r'<link rel="canonical" href="https://amyelectric\.com([^"]*)"', head)
        if not m:
            return None
        p = m.group(1) or '/'
        return p.rstrip('/') or '/'

    # 404.html and seo-audit-report.html are deliberate non-pages: 404 is never
    # indexed, and the report is an internal doc that .assetsignore blocks (live 404).
    # Flagging either as "missing from sitemap" is a false positive.
    not_pages = ('404.html', 'seo-audit-report.html')

    missing_from_sitemap = []
    for f in html_files:
        if f in not_pages:
            continue
        # A noindex page is deliberately kept out of the sitemap, so its absence is
        # correct. The deploy workflow skips these too; flagging them here contradicts CI.
        if 'noindex' in open(f, encoding='utf-8', errors='replace').read(4000):
            continue
        # A canonical-elsewhere page is an alias whose real canonical target is the
        # sitemap entry (e.g. /emergency-electrician -> /emergency-electrician-los-angeles);
        # it must not carry its own sitemap URL, so its absence is correct.
        clean = f[:-5]
        own_path = '/' if clean == 'index' else '/' + clean
        if canon_path(f) is not None and canon_path(f) != own_path:
            continue
        if clean.endswith('/index'):
            clean_dir = clean[:-5] # e.g. blog/
        else:
            clean_dir = clean
            
        if clean not in sitemap_urls and clean_dir not in sitemap_urls and (clean_dir.rstrip('/') + '/') not in sitemap_urls:
            missing_from_sitemap.append((f, clean))

    # Reverse assertion: every sitemap URL must point at a real, self-canonical HTML
    # file. A sitemap entry whose page canonicalizes elsewhere (or 301s, or is missing)
    # publishes a non-canonical URL and undermines consolidation.
    sitemap_not_self_canonical = []
    html_set = set(html_files)
    for url in sorted(sitemap_urls):
        if url == 'index':
            candidate = 'index.html'
        elif url.endswith('/'):
            candidate = url + 'index.html'
        else:
            candidate = url + '.html'
        if candidate not in html_set:
            sitemap_not_self_canonical.append((url, 'no HTML file'))
            continue
        cp = canon_path(candidate)
        expected = '/' if url == 'index' else '/' + url.rstrip('/')
        if cp is None or cp != expected:
            sitemap_not_self_canonical.append((url, 'canonical %s != %s' % (cp, expected)))

    issues_by_file = {}
    sticky_bar_missing = []
    js_missing = []
    meta_desc_issues = []
    title_issues = []
    head_close_missing = []

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

        # 4. Sticky mobile call bar. Two class names are in use across the site
        # (sticky-bar and sticky-call), so matching only one reported 66 false misses.
        if not re.search(r'class="[^"]*\bsticky-(?:bar|call)\b', content) and f != '404.html' and 'privacy-policy' not in f:
            file_issues.append('Missing sticky mobile bar')
            sticky_bar_missing.append(f)

        # 5. Missing </head> before <body> (malformed head breaks crawlers).
        if re.search(r'<body', content) and '</head>' not in content:
            file_issues.append('Missing </head> before <body>')
            head_close_missing.append(f)

        if file_issues:
            issues_by_file[f] = file_issues

    print(f"=== AUDIT REPORT ===")
    print(f"Total production HTML pages: {len(html_files)}")
    print(f"Pages missing from sitemap: {len(missing_from_sitemap)}")
    print(f"Sitemap URLs not self-canonical: {len(sitemap_not_self_canonical)}")
    print(f"Pages missing site.min.js: {len(js_missing)}")
    print(f"Pages missing sticky mobile bar: {len(sticky_bar_missing)}")
    print(f"Pages with meta description issues: {len(meta_desc_issues)}")
    print(f"Pages with title tag issues: {len(title_issues)}")
    print(f"Pages missing </head>: {len(head_close_missing)}")

    if missing_from_sitemap:
        print("\n[!] Missing from sitemap.xml:")
        for f, clean in missing_from_sitemap:
            print(f"  - {f} ({clean})")

    if sitemap_not_self_canonical:
        print("\n[!] Sitemap URLs not self-canonical (remove from sitemap.xml):")
        for url, why in sitemap_not_self_canonical:
            print(f"  - {url} ({why})")

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

    if head_close_missing:
        print(f"\n[!] Missing </head> ({len(head_close_missing)}):")
        for m in head_close_missing:
            print(f"  - {m}")

    any_issues = (missing_from_sitemap or sitemap_not_self_canonical or js_missing or
                  sticky_bar_missing or meta_desc_issues or title_issues or head_close_missing)
    if any_issues:
        print("\nAUDIT FAILED — fix the issues above before deploying.")
        sys.exit(1)
    print("\nAUDIT OK — 0 issues.")

if __name__ == '__main__':
    audit()
