#!/usr/bin/env python3
"""
GBP Weekly Post Scheduler
=========================
Reads gbp-posts-document.txt and prints the post scheduled for this ISO week.
Run every week via cron:
    0 8 * * 1  cd /home/amram/WEBSITE && python3 scripts/gbp-post-scheduler.py >> logs/gbp.log 2>&1

Usage:
    python3 scripts/gbp-post-scheduler.py           # Show this week's post
    python3 scripts/gbp-post-scheduler.py --all     # List all 30 posts with schedule dates
    python3 scripts/gbp-post-scheduler.py --week N  # Show post for specific week index (1-30)
"""

import argparse
import os
import re
import sys
from datetime import date, timedelta

POSTS_FILE = os.path.join(os.path.dirname(__file__), "..", "gbp-posts-document.txt")
CYCLE_WEEKS = 30  # Rotate through 30 posts


def load_posts(path: str) -> list[dict]:
    """Parse gbp-posts-document.txt into a list of post dicts."""
    posts = []
    current = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            # Detect "POST N: Title" header
            m = re.match(r"^POST (\d+): (.+)$", line)
            if m:
                if current:
                    posts.append(current)
                current = {
                    "index": int(m.group(1)),
                    "title": m.group(2).strip(),
                    "body": [],
                }
            elif line.startswith("---"):
                break
            elif current is not None:
                if line.strip():
                    current["body"].append(line)

    if current:
        posts.append(current)

    return posts


def week_index_for_date(d: date) -> int:
    """Return 1-based post index for the given date's ISO week."""
    epoch = date(2025, 1, 6)  # First Monday of 2025 (week 1 offset)
    delta_days = (d - epoch).days
    week_num = (delta_days // 7) % CYCLE_WEEKS
    return week_num + 1


def next_monday(d: date) -> date:
    """Return the next Monday on or after date d."""
    return d + timedelta(days=(7 - d.weekday()) % 7)


def print_post(post: dict, scheduled_date: date | None = None):
    width = 60
    print("=" * width)
    print(f"  POST {post['index']}: {post['title']}")
    if scheduled_date:
        print(f"  📅 Scheduled: {scheduled_date.strftime('%A, %B %d, %Y')}")
    print("=" * width)
    for line in post["body"]:
        print(line)
    print()


def main():
    parser = argparse.ArgumentParser(description="GBP Weekly Post Scheduler")
    parser.add_argument("--all", action="store_true", help="List all posts with scheduled dates")
    parser.add_argument("--week", type=int, metavar="N", help="Show specific post index (1-30)")
    args = parser.parse_args()

    if not os.path.exists(POSTS_FILE):
        print(f"ERROR: Posts file not found: {POSTS_FILE}", file=sys.stderr)
        sys.exit(1)

    posts = load_posts(POSTS_FILE)
    if not posts:
        print("ERROR: No posts found in file.", file=sys.stderr)
        sys.exit(1)

    today = date.today()

    if args.all:
        # Show full 30-week schedule starting from next Monday
        start = next_monday(today)
        print(f"{'='*60}")
        print(f"  GBP POST SCHEDULE — {CYCLE_WEEKS}-week rotation")
        print(f"  Starting: {start.strftime('%B %d, %Y')}")
        print(f"{'='*60}")
        for i, post in enumerate(posts):
            sched = start + timedelta(weeks=i)
            idx_str = f"[W{i+1:02d}]"
            print(f"  {idx_str} {sched.strftime('%Y-%m-%d')}  POST {post['index']:02d}: {post['title']}")
        print()
        return

    if args.week:
        idx = args.week
        if not 1 <= idx <= len(posts):
            print(f"ERROR: --week must be 1–{len(posts)}", file=sys.stderr)
            sys.exit(1)
        post = next((p for p in posts if p["index"] == idx), None)
        if not post:
            print(f"ERROR: Post {idx} not found.", file=sys.stderr)
            sys.exit(1)
        print_post(post)
        return

    # Default: show this week's scheduled post
    idx = week_index_for_date(today)
    post = next((p for p in posts if p["index"] == idx), posts[(idx - 1) % len(posts)])
    start_of_week = today - timedelta(days=today.weekday())
    print_post(post, scheduled_date=start_of_week)
    print(f"📋 To post this week: copy the text above to your Google Business Profile.")
    print(f"   https://business.google.com/posts")
    print()


if __name__ == "__main__":
    main()
