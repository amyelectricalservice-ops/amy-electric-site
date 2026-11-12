#!/usr/bin/env python3
import os
import re
import sys

# --- Configuration ---
# Adjust paths if your layout differs
NAV_FILE = "index.html"  
SITEMAP_FILE = "sitemap.xml"
BLOG_DIR = "blog"

# --- Robust Regex Patterns ---
# Matches navigation lists like <ul id="nav">, <ul class="navigation">, etc. regardless of whitespace/attribute order
NAV_CONTAINER_PATTERN = re.compile(
    r'(<ul\s+[^>]*?(?:id|class)=["\'](?:nav|navigation|menu)["\'][^>]*?>)', 
    re.IGNORECASE
)
# Identifies existing blog items inside the nav list to prevent duplicate injections
EXISTING_BLOG_LINK_PATTERN = re.compile(
    r'<li[^>]*?>\s*<a\s+[^>]*?href=["\']/blog[^"\']*?["\'][^>]*?>', 
    re.IGNORECASE
)
# Matches the closing tag where new list items can safely be injected
NAV_CLOSING_PATTERN = re.compile(r'(</ul>)', re.IGNORECASE)

# Matches the closing urlset tag in standard sitemap XML structures
SITEMAP_CLOSING_PATTERN = re.compile(r'(</urlset>)', re.IGNORECASE)


def get_blog_posts():
    """Scans the blog directory for valid HTML files to build dynamic links."""
    if not os.path.exists(BLOG_DIR):
        print(f"[-] Blog directory '{BLOG_DIR}' not found.", file=sys.stderr)
        return []
    
    posts = []
    for file in os.listdir(BLOG_DIR):
        if file.endswith(".html") and file != "index.html":
            posts.append(f"{BLOG_DIR}/{file}")
    return sorted(posts)


def update_navigation_menu(posts):
    """Injects new blog entries into your HTML layout menu."""
    if not os.path.exists(NAV_FILE):
        print(f"[-] Navigation file '{NAV_FILE}' not found.", file=sys.stderr)
        return

    with open(NAV_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if not NAV_CONTAINER_PATTERN.search(content):
        print("[-] Target navigation container block not matched. Check attributes.", file=sys.stderr)
        return

    # Build up-to-date link elements
    new_links = []
    for post in posts:
        title = os.path.basename(post).replace("-", " ").replace(".html", "").title()
        # Ensure path format matches local preferences
        link_html = f'  <li><a href="/{post}">{title}</a></li>\n'
        
        # Avoid duplicating an existing item
        clean_url = f"/{post}"
        if clean_url not in content:
            new_links.append(link_html)

    if not new_links:
        print("[+] Navigation menu is already clean and up to date.")
        return

    # Inject the missing links right before the closing tag of the matched container
    updated_content = NAV_CLOSING_PATTERN.sub(f"{''.join(new_links)}\\1", content, count=1)
    
    with open(NAV_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"[+] Successfully injected {len(new_links)} new links into {NAV_FILE}.")


def update_xml_sitemap(posts, domain="https://amyelectric.com"):
    """Dynamically appends new links to your production sitemap format."""
    if not os.path.exists(SITEMAP_FILE):
        print(f"[-] Sitemap file '{SITEMAP_FILE}' not found.", file=sys.stderr)
        return

    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    new_entries = []
    for post in posts:
        full_url = f"{domain}/{post}"
        if full_url not in content:
            entry = f"  <url>\n    <loc>{full_url}</loc>\n  </url>\n"
            new_entries.append(entry)

    if not new_entries:
        print("[+] XML Sitemap is already clean and up to date.")
        return

    updated_content = SITEMAP_CLOSING_PATTERN.sub(f"{''.join(new_entries)}\\1", content, count=1)
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"[+] Successfully appended {len(new_entries)} urls to {SITEMAP_FILE}.")


if __name__ == "__main__":
    print("[*] Starting repository automation cleanup...")
    blog_posts = get_blog_posts()
    
    if blog_posts:
        update_navigation_menu(blog_posts)
        update_xml_sitemap(blog_posts)
        print("[+] Cleanup operations completed successfully.")
    else:
        print("[-] No active blog articles found to process.")
