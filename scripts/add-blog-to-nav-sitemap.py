#!/usr/bin/env python3
"""Wire a new blog post into sitemap.xml, blog/index.html and llms.txt.

Replaces the stale September-2025 one-off (hardcoded NEW_BLOG_POSTS list,
`<priority>` regexes). Individual posts are NOT linked from the shared nav —
the shipped convention (verified against the 2026-10 posts) is:

  1. sitemap.xml      — alphabetical position, lastmod stamped today
  2. blog/index.html  — related card, inserted alphabetically by slug
  3. llms.txt         — the `> Last updated:` line bumped to today

Usage: python3 scripts/add-blog-to-nav-sitemap.py <slug> [--icon EMOJI] [--dry-run]

Title/card text are derived from the post itself (H1, then <title>; card
snippet = meta description truncated to 150 chars with an ellipsis, matching
existing cards). Idempotent: every step skips work that is already present.
"""
import argparse
import datetime
import html as htmllib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD_STYLE = ("background:var(--navy); color:white; padding:24px; "
              "border-radius:8px; text-decoration:none; transition:transform .2s;")


def read(p):
    return p.read_text(encoding="utf-8")


def write(p, text):
    p.write_text(text, encoding="utf-8")


def page_meta(path):
    """(card_title, snippet, meta_description) pulled from the post itself."""
    doc = read(path)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", doc, re.S)
    title = re.search(r"<title>(.*?)</title>", doc)
    desc = re.search(r'<meta name="description" content="([^"]+)"', doc)
    card_title = htmllib.unescape(re.sub(r"<[^>]+>", "", h1.group(1)).strip()) \
        if h1 else htmllib.unescape(title.group(1))
    meta_desc = htmllib.unescape(desc.group(1)) if desc else ""
    snippet = (meta_desc[:147] + "...") if len(meta_desc) > 150 else meta_desc
    return card_title, snippet, meta_desc


def wire_sitemap(root, slug, today, dry):
    sitemap = root / "sitemap.xml"
    text = read(sitemap)
    url = "https://amyelectric.com/blog/" + slug
    if "<loc>" + url + "</loc>" in text:
        print("  sitemap.xml    already wired (%s)" % slug)
        return
    entry = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n" % (url, today)
    # Alphabetical insert WITHIN the contiguous /blog/ block (the file's
    # sections are locale-grouped, never globally sorted — anchor elsewhere
    # would dump the entry into an unrelated section).
    best = None
    for m in re.finditer(r"<loc>(https://amyelectric\.com/blog/[^<]*)</loc>", text):
        if m.group(1) < url:
            best = m
    if best is None:  # firstalphabetical entry: right after the /blog/ index loc
        best = re.search(r"<loc>https://amyelectric\.com/blog/</loc>", text)
    insert_at = text.find("</url>", best.start()) + len("</url>")
    entry = "\n  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>" % (url, today)
    if text[insert_at:insert_at + 1] != "\n":
        entry += "\n"  # glued case: keep the following entry at line start
    if not dry:
        write(sitemap, text[:insert_at] + entry + text[insert_at:])
    print("  sitemap.xml    + %s (lastmod %s)" % (url, today))


def wire_blog_index(root, slug, card_title, snippet, icon, dry):
    index = root / "blog" / "index.html"
    text = read(index)
    if 'href="%s"' % slug in text:
        print("  blog/index.html already wired (%s)" % slug)
        return
    card = ('    <a href="%s" class="related-card" style="%s">'
            '<div class="rc-icon" style="font-size:36px; margin-bottom:12px;">%s</div>'
            '<strong style="color:white; display:block; margin-bottom:8px;">%s</strong>'
            '<div style="color:var(--gray); font-size:14px;">%s</div></a>\n'
            % (slug, CARD_STYLE, icon, htmllib.escape(card_title), htmllib.escape(snippet)))
    # Alphabetical insert: after the last card whose href slug sorts before ours.
    best = None
    for m in re.finditer(r'<a href="([^"]+)" class="related-card"', text):
        if m.group(1) < slug:
            best = m
    pos = text.find("\n", best.end()) + 1 if best else 0
    if not dry:
        write(index, text[:pos] + card + text[pos:])
    print("  blog/index.html + card (%s, icon %s)" % (slug, icon))


def wire_llms(root, today, dry):
    llms = root / "llms.txt"
    text = read(llms)
    new = re.sub(r"> Last updated: \d{4}-\d{2}-\d{2}",
                 "> Last updated: " + today, text, count=1)
    if new == text:
        print("  llms.txt       already current (%s)" % today)
        return
    if not dry:
        write(llms, new)
    print("  llms.txt       Last updated -> %s" % today)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--icon", default="\U0001f5e9")  # 🗒 fallback; pass a matching emoji
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    page = ROOT / "blog" / (args.slug + ".html")
    if not page.exists():
        raise SystemExit("no such post: %s" % page)
    card_title, snippet, _ = page_meta(page)
    today = datetime.date.today().isoformat()
    print("wiring %s (title %r)" % (args.slug, card_title[:60]))
    wire_sitemap(ROOT, args.slug, today, args.dry_run)
    wire_blog_index(ROOT, args.slug, card_title, snippet, args.icon, args.dry_run)
    wire_llms(ROOT, today, args.dry_run)
    print("done" + (" (dry run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
