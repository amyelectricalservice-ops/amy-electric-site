#!/usr/bin/env python3
"""Add new blog posts to nav and sitemap across all HTML files."""

import re
from pathlib import Path

WEBSITE_DIR = Path("/home/amram/WEBSITE")

# New blog posts to add
NEW_BLOG_POSTS = [
    ("panel-upgrade-cost-los-angeles", "Panel Upgrade Cost"),
    ("ev-charger-installation-cost-los-angeles", "EV Charger Cost"),
    ("whole-home-rewiring-cost-los-angeles", "Rewiring Cost"),
    ("is-your-home-ev-ready-los-angeles", "Is Your Home EV Ready?"),
]

# Insert after the last blog post in nav (find the blog/ links)
BLOG_NAV_MARKER = '      <a href="blog/">Blog</a>\n'

def update_nav(content: str) -> str:
    """Add new blog post links to nav after Blog link."""
    for slug, label in NEW_BLOG_POSTS:
        link = f'      <a href="blog/{slug}">{label}</a>\n'
        if f'href="blog/{slug}"' not in content and BLOG_NAV_MARKER in content:
            content = content.replace(BLOG_NAV_MARKER, BLOG_NAV_MARKER + link)
    return content

def update_sitemap(sitemap_path: Path) -> None:
    """Add new blog posts to sitemap.xml."""
    content = sitemap_path.read_text(encoding="utf-8")
    
    # Find the last blog entry to insert after
    last_blog_pattern = r'(<loc>https://amyelectric\.com/blog/[^<]+</loc>\s*<lastmod>[^<]+</lastmod>\s*<priority>[^<]+</priority>\s*</url>)\s*(?=<url>|</urlset>)'
    matches = list(re.finditer(last_blog_pattern, content, re.DOTALL))
    
    if matches:
        last_match = matches[-1]
        insert_after = last_match.group(0)
        
        new_entries = ""
        for slug, label in NEW_BLOG_POSTS:
            new_entries += f"""  <url>
    <loc>https://amyelectric.com/blog/{slug}</loc>
    <lastmod>2026-09-12</lastmod>
    <priority>0.7</priority>
  </url>
"""
        
        # Insert after the last blog entry
        content = content.replace(insert_after, insert_after + "\n" + new_entries.strip())
        sitemap_path.write_text(content, encoding="utf-8")
        print(f"Added {len(NEW_BLOG_POSTS)} entries to sitemap.xml")
    else:
        print("WARNING: Could not find last blog entry in sitemap")

def main():
    files_updated = 0
    for html_file in WEBSITE_DIR.glob("*.html"):
        if html_file.name in [f"{slug}.html" for slug, _ in NEW_BLOG_POSTS]:
            continue
        if html_file.name.startswith("blog/"):
            continue
            
        content = html_file.read_text(encoding="utf-8")
        original = content
        content = update_nav(content)
        
        if content != original:
            html_file.write_text(content, encoding="utf-8")
            files_updated += 1
            print(f"Updated nav: {html_file.name}")
    
    # Update sitemap
    sitemap = WEBSITE_DIR / "sitemap.xml"
    update_sitemap(sitemap)
    
    print(f"\nTotal files updated: {files_updated}")

if __name__ == "__main__":
    main()
