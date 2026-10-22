#!/usr/bin/env python3
"""Give the quote form's request-type radios a real group label.

The bulk pass on 2026-10-19 inserted

    <div class="radio-group"><label for="request_type">Request type</label>

into 238 pages.  No element in the site has id="request_type" (the radios are
grouped by name=), so that label was inert: it rendered a duplicate visible
"Request type" line inside the flex .radio-group and named nothing for screen
readers.  WCAG 4.1.2 / ARIA requires the group itself to be named.

This script replaces it with the correct pattern, reusing the heading label
that is already above every radio group:

    <label id="request-type-label">What can we help you with?</label>
    <div class="radio-group" role="radiogroup" aria-labelledby="request-type-label">

Idempotent: re-running makes no further changes.

    python3 scripts/fix-radiogroup-labels.py            # apply
    python3 scripts/fix-radiogroup-labels.py --dry-run  # report only
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADING = "<label>What can we help you with?</label>"
HEADING_LABELLED = '<label id="request-type-label">What can we help you with?</label>'
DANGLING = re.compile(r'(?:<label for="request_type">Request type</label>)+')
GROUP = '<div class="radio-group">'
GROUP_LABELLED = '<div class="radio-group" role="radiogroup" aria-labelledby="request-type-label">'


def fix(html: str):
    """Return (new_html, changes) where changes lists the edits applied."""
    changes = []
    if HEADING in html and HEADING_LABELLED not in html:
        html = html.replace(HEADING, HEADING_LABELLED, 1)
        changes.append("heading label id")

    if DANGLING.search(html):
        html, n = DANGLING.subn("", html)
        changes.append(f"dangling label removed (x{n})")

    if GROUP in html:
        html = html.replace(GROUP, GROUP_LABELLED)
        changes.append("radiogroup role")

    # Nothing to label -> leave the file alone rather than adding dead ARIA.
    if "request-type-label" in html and 'aria-labelledby="request-type-label"' not in html:
        html = html.replace(HEADING_LABELLED, HEADING, 1)
        changes.append("reverted (no radio group)")

    return html, changes


def main() -> int:
    dry = "--dry-run" in sys.argv
    pages = sorted(
        glob.glob(os.path.join(ROOT, "*.html"))
        + glob.glob(os.path.join(ROOT, "blog", "*.html"))
    )
    touched = 0
    for path in pages:
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if "request_type" not in html and HEADING not in html:
            continue
        new, changes = fix(html)
        if new == html:
            continue
        touched += 1
        print(f"{os.path.relpath(path, ROOT):55s} {', '.join(changes)}")
        if not dry:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)

    verb = "would update" if dry else "updated"
    print(f"\n{verb} {touched} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
