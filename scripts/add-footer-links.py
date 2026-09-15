#!/usr/bin/env python3
"""Add reviews and emergency-electrical links to footers across all HTML files."""

from pathlib import Path

WEBSITE_DIR = Path("/home/amram/WEBSITE")

def update_footer(content: str) -> str:
    """Add footer links if not present."""
    # Add emergency-electrical to Emergency footer section
    emergency_footer = '        <li><a href="emergency-electrician">Emergency Electrical Help</a></li>'
    emergency_new = '        <li><a href="emergency-electrical">Emergency Service</a></li>'
    if emergency_new not in content and emergency_footer in content:
        content = content.replace(emergency_footer, emergency_footer + '\n' + emergency_new)

    # Add reviews link to Company footer section
    testimonials_footer = '        <li><a href="testimonials">Reviews</a></li>'
    reviews_new = '        <li><a href="reviews">Customer Reviews</a></li>'
    if reviews_new not in content and testimonials_footer in content:
        content = content.replace(testimonials_footer, testimonials_footer + '\n' + reviews_new)

    return content

def main():
    files_updated = 0
    for html_file in WEBSITE_DIR.glob("*.html"):
        if html_file.name in ["reviews.html", "emergency-electrical.html"]:
            continue

        content = html_file.read_text(encoding="utf-8")
        original = content
        content = update_footer(content)

        if content != original:
            html_file.write_text(content, encoding="utf-8")
            files_updated += 1
            print(f"Updated: {html_file.name}")

    print(f"\nTotal files updated: {files_updated}")

if __name__ == "__main__":
    main()
