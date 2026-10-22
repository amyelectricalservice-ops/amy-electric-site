#!/usr/bin/env python3
"""Mirror the mobile touch-target rules into each page's inline critical CSS.

Above-the-fold elements (topbar phone, breadcrumb) only change height under
these rules, so the inlined critical block has to carry them too — otherwise a
phone would paint at the old size and then shift when css/style.min.css
applies (CLS).  The rules live in css/src/10-responsive.css; this script copies
that one block into the /*topbar-responsive-fix*/ inline block of every page
that has one, right before the /*nav-book*/ marker, and stays idempotent.

    python3 scripts/sync-mobile-touch-css.py            # apply
    python3 scripts/sync-mobile-touch-css.py --dry-run  # report only
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "css", "src", "10-responsive.css")
MARKER = "/*touch-targets*/"
ANCHOR = "/*nav-book*/"
START = "/* ── MOBILE TOUCH TARGETS"


def minify(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*{\s*", "{", css)
    css = re.sub(r"\s*}\s*", "}", css)
    css = re.sub(r"\s*;\s*", ";", css)
    css = re.sub(r"\s*:\s*", ":", css)
    return css.strip()


def touch_block() -> str:
    css = open(SOURCE, encoding="utf-8").read()
    idx = css.find(START)
    if idx == -1:
        raise SystemExit(f"ERROR: touch-target block not found in {SOURCE}")
    return MARKER + minify(css[idx:])


def main() -> int:
    dry = "--dry-run" in sys.argv
    block = touch_block()
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    added, already, absent = [], [], []
    for path in pages:
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if ANCHOR not in html:
            absent.append(os.path.relpath(path, ROOT))
            continue
        if MARKER in html:
            already.append(path)
            continue
        new = html.replace(ANCHOR, block + ANCHOR, 1)
        added.append(os.path.relpath(path, ROOT))
        if not dry:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)

    verb = "would add" if dry else "added"
    print(f"{verb} inline touch-target CSS to {len(added)} pages")
    if already:
        print(f"already present: {len(already)}")
    if absent:
        print(f"no inline critical block (skipped): {len(absent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
