#!/usr/bin/env python3
"""
DEPRECATED — do not run. Use `python3 scripts/sync-nav.py` instead.

This script injected root-relative nav/footer partials into every page, so it
was only ever correct for pages at the repo root. Measured 2026-11-19, running
it would have regressed 367 pages: it replaces the first `<nav>` it finds
(which on some pages is the breadcrumb), strips `class="main-nav"`, drops the
whole "More" panel and the Book CTA, and reverts the menu to a 15-link list
that no longer matches the site. It also rewrote the first `<footer>` on each
page from a partial that predates the current footer.

`scripts/sync-nav.py` is the single source of truth for the header: it computes
the `../` prefix from each file's depth, is idempotent, and runs as a CI gate
(`scripts/sync-nav.py --check`). The `partials/` directory was removed with
this stub for the same reason — nothing reads it any more.
"""

import sys

sys.exit(
    "scripts/inject-layout.py is retired: it would regress the header on ~367 pages.\n"
    "Run `python3 scripts/sync-nav.py` (or `--check` to verify) instead."
)
