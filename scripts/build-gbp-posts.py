#!/usr/bin/env python3
"""Build scripts/gbp-posts.json from gbp-posts-document.txt.

The .txt is the human-editable source; the .json is what the GBP agent
(worker scheduled handler) consumes. Hashtag lines are stripped: GBP
local posts do not support hashtags, and they would render as dead text.

Usage:
  python3 scripts/build-gbp-posts.py            # regenerate + validate
"""
import json
import os
import re
import sys

SITE_DIR = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(SITE_DIR, 'gbp-posts-document.txt')
OUT = os.path.join(os.path.dirname(__file__), 'gbp-posts.json')

GBP_BODY_LIMIT = 1500  # Google local-post summary limit


def parse_posts(text):
    # Split on "POST N:" headers; first chunk is the doc title.
    chunks = re.split(r'^POST\s+(\d+):\s*(.+)$', text, flags=re.M)
    posts = []
    for i in range(1, len(chunks), 3):
        n, title, body = int(chunks[i]), chunks[i + 1].strip(), chunks[i + 2]
        lines = [ln.strip() for ln in body.strip().splitlines() if ln.strip()]
        # Drop hashtag lines (useless on GBP) and the "Now booking" locator
        # stays — it carries the rotated city.
        kept = [ln for ln in lines if not ln.startswith('#')]
        city_m = re.search(r'Now booking in (.+?) —', ' '.join(kept))
        posts.append({
            'n': n,
            'title': title,
            'body': '\n'.join(kept),
            'city': city_m.group(1) if city_m else '',
        })
    return sorted(posts, key=lambda p: p['n'])


def main():
    with open(SRC, encoding='utf-8') as f:
        text = f.read()
    posts = parse_posts(text)
    errors = []
    if len(posts) != 30:
        errors.append(f'expected 30 posts, found {len(posts)}')
    if [p['n'] for p in posts] != list(range(1, 31)):
        errors.append('post numbers are not 1..30 contiguous')
    for p in posts:
        if len(p['body']) > GBP_BODY_LIMIT:
            errors.append(f"POST {p['n']}: body {len(p['body'])} chars > {GBP_BODY_LIMIT}")
        if not p['city']:
            errors.append(f"POST {p['n']}: no rotated city found")
    if errors:
        print('gbp-posts build FAILED:')
        for e in errors:
            print(f'  • {e}')
        return 1
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=1, ensure_ascii=False)
        f.write('\n')
    longest = max(len(p['body']) for p in posts)
    print(f'wrote {OUT}: {len(posts)} posts, longest body {longest}/{GBP_BODY_LIMIT} chars')
    return 0


if __name__ == '__main__':
    sys.exit(main())
