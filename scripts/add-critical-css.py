#!/usr/bin/env python3
"""Give every async-CSS page an inline critical stylesheet.

Pages load css/style.min.css non-render-blocking via
    <link rel="preload" as="style" ... onload="this.onload=null;this.rel='stylesheet'">
That pattern is only safe when the above-the-fold layout is already styled by an
inline <style> block in <head>. 118 pages have one; 43 were generated without
it, so they can paint unstyled before the stylesheet applies (CLS + worse LCP).

This copies the canonical critical block from a known-good page into those
pages, inserted immediately before the preload tag — the same structure the
existing pages use.

    python3 scripts/add-critical-css.py            # apply
    python3 scripts/add-critical-css.py --dry-run  # report only
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = "panel-upgrade.html"  # shares its critical block with 6 other pages
PRELOAD = re.compile(
    r'[ \t]*<link rel="preload" as="style" href="([^"]*style\.min\.css)"[^>]*>'
)
BLOCKING = re.compile(r'<link[^>]*rel="stylesheet"')
STYLE_TAG = re.compile(r"<style[^>]*>", re.I)


def head_of(html: str) -> str:
    lower = html.lower()
    idx = lower.find("</head>")
    return html[:idx] if idx != -1 else html


def critical_block(path: str) -> str | None:
    """Return the inline critical CSS body from a known-good page."""
    html = open(path, encoding="utf-8").read()
    head = head_of(html)
    head_without_noscript = re.sub(r"<noscript.*?</noscript>", "", head, flags=re.S | re.I)
    match = re.search(r"<style[^>]*>(.*?)</style>", head_without_noscript, re.S)
    return match.group(1) if match else None


def main() -> int:
    dry = "--dry-run" in sys.argv
    canonical = critical_block(os.path.join(ROOT, TEMPLATE))
    if not canonical:
        print(f"ERROR: no critical <style> block found in {TEMPLATE}")
        return 1
    print(f"canonical critical block: {len(canonical)} chars (from {TEMPLATE})\n")

    files = sorted(
        glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "blog", "*.html"))
    )

    fixed, already, no_preload, has_blocking = [], [], [], []
    for path in files:
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding="utf-8").read()
        head = head_of(html)
        head_no_ns = re.sub(r"<noscript.*?</noscript>", "", head, flags=re.S | re.I)

        if STYLE_TAG.search(head_no_ns):
            already.append(rel)
            continue

        # A render-blocking <link rel="stylesheet"> means the page cannot paint
        # unstyled, so it doesn't need the inline block.
        if BLOCKING.search(head_no_ns):
            has_blocking.append(rel)
            continue

        preload = PRELOAD.search(head)
        if not preload:
            no_preload.append(rel)
            continue

        block = f"<style>{canonical}</style>\n"
        new_head = head[: preload.start()] + block + head[preload.start() :]
        new_html = html.replace(head, new_head, 1)

        if not dry:
            open(path, "w", encoding="utf-8").write(new_html)
        fixed.append(rel)

    print(f"critical CSS inserted : {len(fixed)}")
    for p in fixed:
        print("   +", p)
    print(f"already had one       : {len(already)}")
    print(f"render-blocking CSS   : {len(has_blocking)} (cannot paint unstyled)")
    print(f"no async-preload tag  : {len(no_preload)}")
    for p in no_preload[:8]:
        print("   -", p)
    if dry:
        print("\n(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
