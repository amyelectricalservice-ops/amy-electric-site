#!/usr/bin/env python3
"""
Inject canonical nav/footer partials into all HTML files.
Idempotent — skips files that already match.

Usage:
  python3 scripts/inject-layout.py           # Check + update
  python3 scripts/inject-layout.py --force   # Overwrite all
"""

import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS_DIR = os.path.join(SITE_DIR, "partials")


def read_partial(name):
    with open(os.path.join(PARTIALS_DIR, name), "r") as f:
        return f.read().strip()


NAV_CANONICAL = read_partial("nav.html")
NAV_BLOG = read_partial("nav-blog.html")
FOOTER_CANONICAL = read_partial("footer.html")


def find_region(html, tag):
    """Return (start, end) of <tag>...</tag> region."""
    start = html.find(f"<{tag}")
    if start < 0:
        return None
    tag_end = html.find(">", start)
    if tag_end < 0:
        return None
    end = html.find(f"</{tag}>", tag_end)
    if end < 0:
        return None
    return (start, end + len(tag) + 3)


def strip_whitespace(s):
    return re.sub(r'\s+', '', s)


def has_active(html_nav):
    return 'class="active"' in html_nav


def inject_nav(html, is_blog):
    """Replace nav content while preserving active state."""
    region = find_region(html, "nav")
    if not region:
        return html, False

    start, end = region
    old_nav = html[start:end]
    active = has_active(old_nav)
    new_nav = NAV_BLOG if is_blog else NAV_CANONICAL

    # If the old nav has an active class, add it to the matching link in new nav
    if active:
        active_match = re.search(r'href="([^"]*)"[^>]*class="active"', old_nav)
        if active_match:
            active_href = active_match.group(1)
            # Add active to the matching link in new nav
            new_nav = re.sub(
                rf'(href="{re.escape(active_href)}")',
                r'\1 class="active"',
                new_nav
            )

    if strip_whitespace(old_nav) == strip_whitespace(new_nav):
        return html, False  # Already matches

    return html[:start] + new_nav + html[end:], True


def inject_footer(html):
    """Replace footer content."""
    region = find_region(html, "footer")
    if not region:
        return html, False

    start, end = region
    old_footer = html[start:end]

    if strip_whitespace(old_footer) == strip_whitespace(FOOTER_CANONICAL):
        return html, False

    return html[:start] + FOOTER_CANONICAL + html[end:], True


def walk_html():
    for root, dirs, files in os.walk(SITE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".")
                   and d not in ("amyelectric-site", "partials", "__pycache__")]
        for fname in sorted(files):
            if fname.endswith(".html"):
                yield os.path.join(root, fname)


def main():
    force = "--force" in sys.argv
    changed = []

    for path in walk_html():
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        orig = html
        rel = os.path.relpath(path, SITE_DIR)
        is_blog = rel.startswith("blog/")

        html, nav_changed = inject_nav(html, is_blog)
        html, footer_changed = inject_footer(html)

        if force and not nav_changed and not footer_changed:
            # Force re-write
            pass

        if html != orig:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            changed.append(rel)

    if changed:
        print(f"Updated {len(changed)} file(s):")
        for f in changed:
            print(f"  ~ {f}")
    else:
        print("All pages already match canonical partials.")


if __name__ == "__main__":
    main()
