#!/usr/bin/env python3
"""Refresh sitemap.xml <lastmod> for HTML files changed in a given diff.

Usage: python3 scripts/refresh-sitemap-lastmod.py [git-diff-arg...]
Defaults to HEAD~1..HEAD. Only bumps entries whose file actually changed,
never rewrites untouched dates. Skips 404/noindex pages (matching CI).
Surgical line replacement: no XML reformatting, minimal diff.
Prints changed URLs; exits 0 with no changes.
"""
import datetime
import re
import subprocess
import sys


def html_to_url(path):
    path = path.strip().lstrip("./")
    if not path.endswith(".html"):
        return None
    if path == "404.html":
        return None
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            if "noindex" in fh.read(4000):
                return None
    except OSError:
        return None
    clean = path.removesuffix(".html")
    if clean == "index":
        return "https://amyelectric.com/"
    if clean.endswith("/index"):
        return "https://amyelectric.com/" + clean[: -len("index")]
    return "https://amyelectric.com/" + clean


def main():
    diff_args = sys.argv[1:] or ["HEAD~1..HEAD"]
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only"] + diff_args + ["--", "*.html"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
    except subprocess.CalledProcessError:
        print("no git history for diff; skipping")
        return
    urls = {u for f in out if (u := html_to_url(f))}
    if not urls:
        print("no eligible pages changed")
        return
    text = open("sitemap.xml", encoding="utf-8").read()
    today = datetime.date.today().isoformat()
    changed = 0
    for url in sorted(urls):
        pat = re.compile(
            r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)"
        )
        text, n = pat.subn(r"\g<1>" + today + r"\g<2>", text, count=1)
        changed += n
    if changed:
        open("sitemap.xml", "w", encoding="utf-8").write(text)
    print(f"lastmod refreshed for {changed} urls")


if __name__ == "__main__":
    main()
