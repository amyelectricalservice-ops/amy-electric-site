import glob
import os
import re
import json

def fix_seo():
    html_files = glob.glob('**/*.html', recursive=True)
    ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/')
    html_files = [f for f in sorted(html_files) if not any(f.startswith(p) for p in ignore_prefixes)]

    print(f"=== APPLYING SEO DEBUG & FIXES ACROSS {len(html_files)} PAGES ===")

    # 1. Replace internal .html links with clean URLs
    html_replacements = [
        ('href="/services.html"', 'href="/services"'),
        ('href="services.html"', 'href="services"'),
        ('href="../services.html"', 'href="../services"'),
        ('href="/privacy-policy.html"', 'href="/privacy-policy"'),
        ('href="privacy-policy.html"', 'href="privacy-policy"'),
        ('href="../privacy-policy.html"', 'href="../privacy-policy"'),
        ('href="service-areas.html"', 'href="service-areas"'),
        ('href="../service-areas.html"', 'href="../service-areas"'),
        ('href="/service-areas.html"', 'href="/service-areas"'),
        ('href="index.html"', 'href="index"'),
        ('href="blog/index.html"', 'href="blog/"'),
        ('href="../blog/index.html"', 'href="../blog/"'),
    ]

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
            
        orig = c

        for old_ref, new_ref in html_replacements:
            c = c.replace(old_ref, new_ref)

        # 2. Check and fix missing OpenGraph & Twitter tags
        # Extract title and description
        t_m = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE | re.DOTALL)
        d_m = re.search(r'<meta\s+(?:name=["\']description["\']\s+content=["\']([^"\']*)["\']|content=["\']([^"\']*)["\']\s+name=["\']description["\'])', c, re.IGNORECASE)
        
        title_val = t_m.group(1).strip() if t_m else "AMY Electric | Los Angeles Electrician"
        desc_val = (d_m.group(1) or d_m.group(2)).strip() if d_m else "Licensed C-10 electrician in Los Angeles."

        clean_path = f[:-5] if f.endswith('.html') else f
        if clean_path == 'index':
            canonical_url = "https://amyelectric.com/"
        elif clean_path.endswith('/index'):
            canonical_url = f"https://amyelectric.com/{clean_path[:-6]}/"
        else:
            canonical_url = f"https://amyelectric.com/{clean_path}"

        # Inject OpenGraph if missing
        if 'og:title' not in c:
            og_tags = f'''<meta property="og:title" content="{title_val}">
<meta property="og:description" content="{desc_val}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://amyelectric.com/img/hero-electrician.jpg">'''
            c = c.replace('</head>', f'{og_tags}\n</head>')
        elif 'og:url' not in c:
            og_url_tag = f'<meta property="og:url" content="{canonical_url}">'
            c = c.replace('</head>', f'{og_url_tag}\n</head>')

        # Inject Twitter Card if missing
        if 'twitter:card' not in c:
            tw_tags = f'''<meta name="twitter:card" content="summary_large_image">
<meta property="twitter:title" content="{title_val}">
<meta property="twitter:description" content="{desc_val}">
<meta property="twitter:image" content="https://amyelectric.com/img/hero-electrician.jpg">'''
            c = c.replace('</head>', f'{tw_tags}\n</head>')

        if c != orig:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(c)

    print("Successfully processed all production HTML pages for SEO optimization!")

if __name__ == '__main__':
    fix_seo()
