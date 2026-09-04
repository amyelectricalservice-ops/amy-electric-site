import glob
import os
import re
import json
from xml.etree import ElementTree as ET

def seo_audit():
    html_files = glob.glob('**/*.html', recursive=True)
    ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/')
    html_files = [f for f in sorted(html_files) if not any(f.startswith(p) for p in ignore_prefixes)]

    print(f"=== DEEP SEO AUDIT ON {len(html_files)} PRODUCTION PAGES ===")

    # 1. Sitemap check
    sitemap_urls = set()
    if os.path.exists('sitemap.xml'):
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_node in root.findall('.//ns:url', ns):
            loc = url_node.find('ns:loc', ns).text
            clean_loc = loc.replace('https://amyelectric.com/', '').strip('/')
            if clean_loc == '':
                clean_loc = 'index'
            sitemap_urls.add(clean_loc)
            sitemap_urls.add(clean_loc + '/')
            sitemap_urls.add(loc)

    canonical_issues = []
    og_issues = []
    twitter_issues = []
    schema_issues = []
    h1_issues = []
    img_alt_issues = []
    internal_link_html_ext = []
    sitemap_missing = []

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()

        clean_path = f[:-5] if f.endswith('.html') else f
        if clean_path.endswith('/index'):
            clean_dir = clean_path[:-5] # e.g. blog/
        else:
            clean_dir = clean_path

        # 1. Sitemap check
        if f != '404.html':
            in_sitemap = (
                clean_path in sitemap_urls or
                clean_dir in sitemap_urls or
                (clean_dir.rstrip('/') + '/') in sitemap_urls or
                f'https://amyelectric.com/{clean_dir.rstrip("/")}/' in sitemap_urls
            )
            if not in_sitemap:
                sitemap_missing.append((f, clean_dir))

        # 2. Canonical URL check
        c_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', c, re.IGNORECASE)
        if not c_match:
            canonical_issues.append((f, 'Missing canonical tag'))
        else:
            href = c_match.group(1)
            if not href.startswith('https://amyelectric.com/'):
                canonical_issues.append((f, f'Non-absolute canonical: {href}'))
            elif href.endswith('.html'):
                canonical_issues.append((f, f'Canonical contains .html: {href}'))

        # 3. OpenGraph check
        og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']*)["\']', c, re.IGNORECASE)
        og_desc = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']*)["\']', c, re.IGNORECASE)
        og_url = re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']*)["\']', c, re.IGNORECASE)
        og_img = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']*)["\']', c, re.IGNORECASE)

        if not og_title:
            og_issues.append((f, 'Missing og:title'))
        if not og_desc:
            og_issues.append((f, 'Missing og:description'))
        if not og_url:
            og_issues.append((f, 'Missing og:url'))
        elif og_url and og_url.group(1).endswith('.html'):
            og_issues.append((f, f'og:url contains .html: {og_url.group(1)}'))
        if not og_img:
            og_issues.append((f, 'Missing og:image'))

        # 4. Twitter card check
        tw_card = re.search(r'<meta\s+name=["\']twitter:card["\']\s+content=["\']([^"\']*)["\']', c, re.IGNORECASE)
        if not tw_card:
            twitter_issues.append((f, 'Missing twitter:card'))

        # 5. H1 check
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', c, re.IGNORECASE | re.DOTALL)
        if len(h1s) == 0:
            h1_issues.append((f, 'Missing <h1>'))
        elif len(h1s) > 1:
            h1_issues.append((f, f'Multiple <h1> tags ({len(h1s)})'))

        # 6. Image alt check
        imgs = re.findall(r'<img\s+[^>]*\bsrc=["\'](?![\'"]\s*\+)[^"\']+["\'][^>]*>', c, re.IGNORECASE)
        for img in imgs:
            if 'alt=' not in img:
                img_alt_issues.append((f, f'Missing alt attribute in {img[:60]}'))
                break
            alt_m = re.search(r'alt=["\'](.*?)["\']', img)
            if alt_m and alt_m.group(1).strip() == '':
                img_alt_issues.append((f, f'Empty alt attribute in {img[:60]}'))
                break

        # 7. Schema JSON-LD validation
        json_ld_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
        if not json_ld_blocks and f != '404.html':
            schema_issues.append((f, 'Missing JSON-LD schema'))
        else:
            for i, block in enumerate(json_ld_blocks):
                try:
                    json.loads(block)
                except Exception as e:
                    schema_issues.append((f, f'JSON-LD Parse error in block {i+1}: {e}'))

        # 8. Internal links pointing to .html
        hrefs = re.findall(r'href=["\']([^"\']*)["\']', c, re.IGNORECASE)
        for href in hrefs:
            if href.startswith('http://') or href.startswith('https://') or href.startswith('#') or href.startswith('tel:') or href.startswith('mailto:') or href.startswith('sms:'):
                continue
            clean_h = href.split('?')[0].split('#')[0]
            if clean_h.endswith('.html') and clean_h != 'privacy-policy.html':
                internal_link_html_ext.append((f, href))

    print(f"\n--- DEEP SEO AUDIT RESULTS ---")
    print(f"Missing from sitemap: {len(sitemap_missing)}")
    print(f"Canonical URL issues: {len(canonical_issues)}")
    print(f"OpenGraph meta issues: {len(og_issues)}")
    print(f"Twitter card issues: {len(twitter_issues)}")
    print(f"H1 tag issues: {len(h1_issues)}")
    print(f"Image alt issues: {len(img_alt_issues)}")
    print(f"JSON-LD Schema issues: {len(schema_issues)}")
    print(f"Internal links with .html extension (triggering 301 redirects): {len(internal_link_html_ext)}")

if __name__ == '__main__':
    seo_audit()
