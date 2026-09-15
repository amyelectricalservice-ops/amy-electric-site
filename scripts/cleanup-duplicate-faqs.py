#!/usr/bin/env python3
"""Remove duplicate FAQ items from city pages."""

import glob
import os
import re

SITE_DIR = os.path.join(os.path.dirname(__file__), "..")


def cleanup_file(filepath):
    """Remove duplicate FAQ items from a single file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all FAQ items with their full HTML
    faq_pattern = re.compile(
        r'(<details class="faq-item"><summary class="faq-q">)(.*?)(</summary><div class="faq-a">)(.*?)(</div></details>)',
        re.DOTALL
    )

    matches = list(faq_pattern.finditer(content))
    if not matches:
        return False

    # Track unique questions and their positions
    seen_questions = set()
    positions_to_remove = []

    for match in matches:
        question = match.group(2).strip()
        # Normalize question for comparison
        normalized = re.sub(r'\s+', ' ', question).lower()
        
        if normalized in seen_questions:
            positions_to_remove.append((match.start(), match.end()))
        else:
            seen_questions.add(normalized)

    if not positions_to_remove:
        return False

    # Remove duplicates in reverse order to preserve positions
    for start, end in reversed(positions_to_remove):
        # Also remove any trailing newline
        while end < len(content) and content[end] in ('\n', '\r'):
            end += 1
        content = content[:start] + content[end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return len(positions_to_remove)


def main():
    files = sorted(glob.glob(os.path.join(SITE_DIR, "city-*.html")))
    print(f"Found {len(files)} city files")

    total_removed = 0
    files_cleaned = 0

    for filepath in files:
        slug = os.path.basename(filepath).replace("city-", "").replace(".html", "")
        removed = cleanup_file(filepath)
        if removed:
            files_cleaned += 1
            total_removed += removed
            print(f"  {slug}: removed {removed} duplicate FAQs")

    print(f"\nDone: {files_cleaned} files cleaned, {total_removed} duplicate FAQs removed")


if __name__ == "__main__":
    main()
