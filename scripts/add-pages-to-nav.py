#!/usr/bin/env python3
"""Add reviews and emergency pages to nav across all HTML files and sitemap."""

import re
import os
from pathlib import Path

WEBSITE_DIR = Path("/home/amram/WEBSITE")

# New nav links to add
REVIEWS_NAV = '      <a href="reviews">Reviews</a>\n'
EMERGENCY_NAV = '      <a href="emergency-electrical">Emergency</a>\n'

# Find where to insert (after gallery, before blog)
NAV_MARKER = '      <a href="gallery">Gallery</a>\n'

def update_nav(content: str) -> str:
    """Add reviews and emergency links to nav if not present."""
    if 'href="reviews"' not in content and NAV_MARKER in content:
        content = content.replace(NAV_MARKER, NAV_MARKER + REVIEWS_NAV)
    if 'href="emergency-electrical"' not in content and NAV_MARKER in content:
        # Insert emergency after reviews if reviews exists, else after gallery
        if 'href="reviews"' in content:
            marker = '      <a href="reviews">Reviews</a>\n'
            content = content.replace(marker, marker + EMERGENCY_NAV)
        else:
            content = content.replace(NAV_MARKER, NAV_MARKER + EMERGENCY_NAV)
    return content

def update_footer(content: str) -> str:
    """Add links to footer if not present."""
    # Add to Company section in footer
    footer_marker = '        <li><a href="testimonials">Reviews</a></li>'
    if 'href="reviews"' not in content and footer_marker in content:
        content = content.replace(
            footer_marker,
            footer_marker + '\n        <li><a href="reviews">Customer Reviews</a></li>'
        )
    # Add emergency to Emergency section if exists
    emergency_footer = '        <li><a href="emergency-electrician">Emergency Electrical Help</a></li>'
    if 'href="emergency-electrical"' not in content and emergency_footer in content:
        content = content.replace(
            emergency_footer,
            emergency_footer + '\n        <li><a href="emergency-electrical">Emergency Service</a></li>'
        )
    return content

def main():
    files_updated = 0
    for html_file in WEBSITE_DIR.glob("*.html"):
        if html_file.name in ["reviews.html", "emergency-electrical.html"]:
            continue  # Skip the new pages themselves
        
        content = html_file.read_text(encoding='utf-8')
        original = content
        
        content = update_nav(content)
        content = update_footer(content)
        
        if content != original:
            html_file.write_text(content, encoding='utf-8')
            files_updated += 1
            print(f"Updated: {html_file.name}")
    
    print(f"\nTotal files updated: {files_updated}")

if __name__ == "__main__":
    main()
