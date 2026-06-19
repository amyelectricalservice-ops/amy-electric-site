#!/usr/bin/env python3
"""Regenerate gallery.html grid + ItemList JSON-LD + sitemap.xml for all photos."""
import csv
import re
from pathlib import Path

WEBSITE = Path(__file__).parent.parent
MANIFEST = WEBSITE / "scripts/photo-manifest.csv"
GALLERY_FILE = WEBSITE / "gallery.html"
SITEMAP_FILE = WEBSITE / "sitemap.xml"

CATEGORY_LABELS = {
    "panel": ("Panel Upgrades", "rgba(245,166,35,.2)", "#f5a623"),
    "commercial": ("Commercial", "rgba(74,144,217,.2)", "#4a90d9"),
    "new-construction": ("New Construction", "rgba(126,200,80,.2)", "#7ec850"),
    "lighting": ("Lighting", "rgba(232,123,156,.2)", "#e87b9c"),
    "team": ("Team", "rgba(155,89,182,.2)", "#9b59b6"),
    "lifestyle": ("Lifestyle", "rgba(230,126,34,.2)", "#e67e22"),
    "exterior": ("Exteriors", "rgba(26,188,156,.2)", "#1abc9c"),
    "other": ("Equipment", "rgba(149,165,166,.2)", "#95a5a6"),
}

def read_manifest():
    with open(MANIFEST, newline="") as f:
        return list(csv.DictReader(f))

def gallery_item_html(row):
    slug = row["slug"]
    cat = row.get("category", "other").strip()
    label, bg, color = CATEGORY_LABELS.get(cat, CATEGORY_LABELS["other"])
    city = row.get("city", "").strip() or "Los Angeles"
    year = row.get("year", "").strip() or "2025"
    caption = row.get("caption", "").strip() or f"Electrical project by AMY Electric"

    src_400 = f"img/gallery/{slug}-400w.webp"
    src_1200w = f"img/gallery/{slug}-1200w.webp"
    src_1200j = f"img/gallery/{slug}-1200w.jpg"
    alt = f"{caption} - AMY Electric {city}"

    return f'''
    <div class="gallery-item" data-category="{cat}" data-city="{city}" data-year="{year}">
      <picture>
        <source srcset="{src_400} 400w, {src_1200w} 1200w" type="image/webp" sizes="(max-width: 480px) 100vw, (max-width: 900px) 50vw, (max-width: 1400px) 33vw, 300px">
        <source srcset="{src_1200j}" type="image/jpeg">
        <img src="{src_1200j}" alt="{alt}" width="1200" height="900" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-overlay">
        <h3>{caption}</h3>
        <p class="gallery-location">{city}, CA &middot; {year}</p>
        <span class="gallery-tag" style="background:{bg};color:{color}">{label}</span>
      </div>
    </div>'''

def itemlist_json(rows):
    items = []
    for i, r in enumerate(rows, 1):
        slug = r["slug"]
        caption = r.get("caption", "").strip() or f"Electrical project by AMY Electric"
        city = r.get("city", "").strip() or "Los Angeles"
        year = r.get("year", "").strip() or "2025"
        items.append(
            f'{{"@type":"ListItem","position":{i},"item":{{"@type":"ImageObject",'
            f'"contentUrl":"https://amyelectric.com/img/gallery/{slug}-1200w.webp",'
            f'"caption":"{caption} in {city}, CA","name":"{caption}",'
            f'"uploadDate":"{year}-01-01"}}}}'
        )
    inner = ",\n".join(items)
    return '{"@context":"https://schema.org","@type":"ItemList","itemListElement":[\n' + inner + "]}"


def main():
    rows = read_manifest()
    total = len(rows)
    print(f"Building gallery for {total} photos...")

    # Generate all gallery items HTML
    all_items = "\n".join(gallery_item_html(r) for r in rows)

    # Read gallery.html
    content = GALLERY_FILE.read_text(encoding="utf-8")

    # Replace gallery grid content (between <div class="gallery-grid" id="gallery-grid"> and </div> after it)
    grid_start = content.find('<div class="gallery-grid" id="gallery-grid">')
    grid_end = content.find("</div>", grid_start) + 6
    # Find the actual end of the gallery-grid div - it's the first </div> that closes the grid, but
    # since grid items contain nested divs, we need to be smarter. The grid div is the one inside
    # the section section-pad, closed before the section end.
    # Let's find: the pattern is that after the grid, there's a newline then </div></section>
    # Better approach: find the unique closing pattern
    grid_section_start = content.find('<section class="section-pad">')
    grid_section_end = content.find('</section>', grid_section_start)
    grid_open = content.find('<div class="gallery-grid"', grid_section_start)
    grid_close = content.find('\n  </div>\n</div>\n</section>', grid_open)
    if grid_close == -1:
        grid_close = content.find('</div>', grid_open)
        # Find the right </div> - count nesting
        depth = 1
        pos = grid_open + len('<div class="gallery-grid" id="gallery-grid">')
        while depth > 0 and pos < len(content):
            next_open = content.find('<div', pos)
            next_close = content.find('</div>', pos)
            if next_close == -1: break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 5
            else:
                depth -= 1
                pos = next_close + 6
        grid_close = pos

    new_grid = f'<div class="gallery-grid" id="gallery-grid">\n{all_items}\n  </div>'
    content = content[:grid_open] + new_grid + content[grid_close:]

    # Update meta description count
    content = re.sub(
        r'<meta name="description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta name="description" content="View our gallery of {total} real electrical projects',
        content
    )
    content = re.sub(
        r'<meta property="og:description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta property="og:description" content="View our gallery of {total} real electrical projects',
        content
    )
    content = re.sub(
        r'<meta name="twitter:description" content="View our gallery of \d+\+? real electrical projects',
        f'<meta name="twitter:description" content="View our gallery of {total} real electrical projects',
        content
    )

    # Update itemlist JSON-LD
    itemlist = itemlist_json(rows)
    content = re.sub(
        r'\{"@context":"https://schema\.org","@type":"ItemList","itemListElement":\[.*?\]',
        itemlist,
        content,
        flags=re.DOTALL
    )

    GALLERY_FILE.write_text(content, encoding="utf-8")
    print(f"Updated {GALLERY_FILE}")

    # Update sitemap.xml
    update_sitemap(rows)
    
    print(f"\nDone — {total} photos in gallery.")


def update_sitemap(rows):
    sitemap_content = SITEMAP_FILE.read_text(encoding="utf-8")

    # Generate image tags for all photos
    image_tags = "".join(
        f'<image:image><image:loc>https://amyelectric.com/img/gallery/{r["slug"]}-1200w.webp</image:loc></image:image>\n'
        for r in rows
    )

    new_gallery_entry = (
        f'<url>\n'
        f'<loc>https://amyelectric.com/gallery</loc>\n'
        f'<lastmod>2026-06-18</lastmod>\n'
        f'<priority>0.7</priority>\n'
        f'{image_tags}'
        f'</url>'
    )

    # Find current gallery entry in sitemap
    pattern = r'<url>\s*<loc>https://amyelectric\.com/gallery</loc>.*?</url>'
    match = re.search(pattern, sitemap_content, re.DOTALL)
    if match:
        sitemap_content = sitemap_content.replace(match.group(0), new_gallery_entry)
        SITEMAP_FILE.write_text(sitemap_content, encoding="utf-8")
        print(f"Updated {SITEMAP_FILE} with {len(rows)} image entries")
    else:
        print("WARNING: gallery URL not found in sitemap.xml")


if __name__ == "__main__":
    main()
