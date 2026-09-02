#!/usr/bin/env python3
"""Add inline project photos to service pages and city pages, update sitemap.

Usage: python3 scripts/add-page-photos.py

For each page, inserts a photo section with the closest matching project photo.
Updates sitemap.xml with image:image entries.
"""

import re
import os
from pathlib import Path

WEBSITE = Path(__file__).parent.parent

# Service pages: page_file -> [(slug, caption)]
SERVICE_PHOTOS = {
    "ev-charger-installation.html": [
        ("gallery-commercial-parking-team", "Three-man crew installing EV-ready panels in parking structure"),
        ("gallery-commercial-parking-conduit", "Conduit installation for commercial EV charging stations"),
        ("gallery-panel-siemens-stucco", "Siemens panel upgrade with capacity for EV charger"),
    ],
    "panel-upgrade.html": [
        ("gallery-panel-siemens-stucco", "Siemens 200A panel upgrade with exterior stucco finish"),
        ("gallery-panel-dual-meter", "Dual-meter exterior service installation"),
        ("gallery-panel-subpanel-labeled", "New subpanel installation with clearly labeled circuits"),
    ],
    "commercial-electrical.html": [
        ("gallery-commercial-switchgear-tall", "Tall Siemens switchgear in commercial electrical room"),
        ("gallery-commercial-bus-duct", "Bus duct with visible bus bars in commercial installation"),
        ("gallery-commercial-parking-team", "Three-man crew installing panels in commercial parking structure"),
    ],
    "lighting-installation.html": [
        ("gallery-lighting-kitchen", "Finished kitchen with pendant light installation and modern fixtures"),
        ("gallery-lighting-chandelier", "Dramatic chandelier installation on tall ladder"),
        ("gallery-lighting-commercial-install", "Electrician installing ceiling light fixtures in commercial space"),
    ],
}

# City pages: page_file -> best photo slug, caption, city
CITY_PHOTOS = {
    "city-los-angeles.html": ("gallery-panel-siemens-stucco", "Siemens 200A panel upgrade in Los Angeles", "Los Angeles"),
    "city-sherman-oaks.html": ("gallery-panel-subpanel-labeled", "New subpanel installation in Sherman Oaks", "Sherman Oaks"),
    "city-burbank.html": ("gallery-panel-meter-removal", "Old meter base removal during service upgrade in Burbank", "Burbank"),
    "city-glendale.html": ("gallery-panel-drywall-install", "New panel installation in Glendale home", "Glendale"),
    "city-pasadena.html": ("gallery-team-worker-foundation", "Conduit installation through foundation in Pasadena", "Pasadena"),
    "city-studio-city.html": ("gallery-commercial-parking-team", "EV-ready panels in Studio City parking structure", "Studio City"),
    "city-north-hollywood.html": ("gallery-construction-apartment", "New apartment building under construction in North Hollywood", "North Hollywood"),
    "city-hollywood.html": ("gallery-lifestyle-home-pool", "Luxury home electrical project with Hollywood Hills views", "Hollywood Hills"),
    "city-beverly-hills.html": ("gallery-lighting-kitchen", "Finished kitchen with pendant lighting in Beverly Hills", "Beverly Hills"),
    "city-west-la.html": ("gallery-commercial-switchgear-clean", "Commercial panel installation serving West Los Angeles", "West Los Angeles"),
    "city-encino.html": ("gallery-roughin-framing-conduit", "Electrical rough-in with conduit through framing in Encino", "Encino"),
    "city-santa-monica.html": ("gallery-exterior-spanish-apartment", "Spanish-style apartment building electrical work in Santa Monica", "Santa Monica"),
    "city-van-nuys.html": ("gallery-commercial-meter-bank", "Commercial meter bank installation in Van Nuys", "Van Nuys"),
    "city-woodland-hills.html": ("gallery-commercial-switchgear-200a", "Switchgear with 200A breakers near Woodland Hills", "Woodland Hills"),
    "city-calabasas.html": ("gallery-lighting-kitchen-alt", "Modern kitchen lighting installation near Calabasas", "Calabasas"),
    "city-culver-city.html": ("gallery-commercial-parking-conduit", "Conduit installation near Culver City", "Culver City"),
}


def make_photo_block(slug, caption, width_attr=True):
    """Generate HTML for a <picture> element referencing the photo."""
    w = ' width="1200" height="900"' if width_attr else ''
    return (
        f'<div class="inline-project-photo">'
        f'<picture>'
        f'<source srcset="img/gallery/{slug}-400w.webp 400w, img/gallery/{slug}-1200w.webp 1200w" type="image/webp" sizes="(max-width: 480px) 100vw, 600px">'
        f'<source srcset="img/gallery/{slug}-1200w.jpg" type="image/jpeg">'
        f'<img src="img/gallery/{slug}-1200w.jpg" alt="{caption} - AMY Electric" loading="lazy" decoding="async"{w}>'
        f'</picture>'
        f'<p class="photo-caption">{caption}</p>'
        f'</div>'
    )


def make_photo_grid(slugs_and_captions):
    """Generate a 3-column photo grid."""
    items = "".join(
        f'<div class="grid-item">{make_photo_block(slug, caption, False)}</div>'
        for slug, caption in slugs_and_captions
    )
    return f'<div class="photo-grid cols-3">{items}</div>'


HEADER_SECTION = """
<style>
.photo-grid {
  display: grid;
  gap: 20px;
  margin: 32px 0;
}
.photo-grid.cols-3 {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}
.inline-project-photo {
  border-radius: 6px;
  overflow: hidden;
  background: var(--navy2);
  border: 1px solid rgba(255,255,255,.08);
}
.inline-project-photo img,
.inline-project-photo picture {
  display: block;
  width: 100%;
  height: auto;
}
.photo-caption {
  padding: 10px 12px;
  font-size: 13px;
  color: var(--white);
  margin: 0;
  text-align: center;
  font-style: italic;
  opacity: 0.85;
}
</style>
"""


def find_insert_point(content, section_marker):
    """Find the safest place to insert a photo section."""
    patterns = [
        r'<section class="page-hero">.*?</section>',
        r'<div class="trust-bar">.*?</div>',
    ]
    for p in patterns:
        match = re.search(p, content, re.DOTALL)
        if match:
            return match.end()
    return None


def update_service_page(filepath, photos):
    """Add photo grid after the trust bar on a service page."""
    with open(filepath) as f:
        content = f.read()

    # Find insert point (after trust-bar)
    trust_match = re.search(r'<div class="trust-bar">.*?</div>', content, re.DOTALL)
    if not trust_match:
        print(f"  SKIP {filepath.name}: no trust-bar found")
        return False

    insert_at = trust_match.end()
    photo_html = make_photo_grid(photos)
    photo_section = f'\n<section style="padding:48px 24px 24px;"><div class="wrap">\n  <div class="section-label">Project Photos</div>\n  <h3>{filepath.stem.replace("-", " ").title().replace("Ev", "EV").replace("La", "LA")} Project Photos</h3>\n  <p style="max-width:640px;">Browse representative project photos from electrical work across Greater Los Angeles. Equipment and scope vary by property.</p>{photo_html}\n</div></section>\n'

    content = content[:insert_at] + photo_section + content[insert_at:]

    # Add inline styles if not present
    if 'photo-grid' not in content and 'inline-project-photo' not in content:
        content = content.replace('</head>', f'{HEADER_SECTION}\n</head>')

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  UPDATED {filepath.name}")
    return True


def update_city_page(filepath, slug, caption, city):
    """Add a local project photo to the Local Knowledge section of a city page."""
    with open(filepath) as f:
        content = f.read()

    # Find "Local Knowledge" section label
    lk_match = re.search(
        r'<div class="section-label">Local Knowledge</div>',
        content
    )
    if not lk_match:
        print(f"  SKIP {filepath.name}: no Local Knowledge section")
        return False

    insert_at = lk_match.start()
    photo_block = make_photo_block(slug, caption)

    # Add before Local Knowledge
    section = (
        f'\n<section style="padding:48px 24px;"><div class="wrap">\n'
        f'  <div class="section-label">Local Project</div>\n'
        f'  <h3>Project Highlight: {city}</h3>\n'
        f'  <p style="max-width:640px;margin-bottom:24px;">'
        f'A recent {city} project by our team — one of many completed throughout '
        f'the Greater Los Angeles area.</p>\n'
        f'  <div style="max-width:680px;">{photo_block}</div>\n'
        f'</div></section>\n\n'
    )

    content = content[:insert_at] + section + content[insert_at:]

    # Add inline styles if not present
    if 'inline-project-photo' not in content:
        content = content.replace('</head>', f'{HEADER_SECTION}\n</head>')

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  UPDATED {filepath.name}")
    return True


def update_sitemap():
    """Add image:image entries to sitemap.xml for all gallery photos."""
    sitemap = WEBSITE / "sitemap.xml"
    with open(sitemap) as f:
        content = f.read()

    # Find gallery URL entry
    gallery_url_match = re.search(
        r'(<url>\s*<loc>https://amyelectric\.com/gallery</loc>.*?</url>)',
        content, re.DOTALL
    )

    # Generate image tags for all 30 photos
    slugs_and_years = [
        ("gallery-panel-siemens-stucco", "2022"),
        ("gallery-panel-subpanel-labeled", "2022"),
        ("gallery-panel-dual-meter", "2022"),
        ("gallery-panel-three-wire", "2020"),
        ("gallery-panel-commercial-disconnect", "2023"),
        ("gallery-panel-meter-removal", "2022"),
        ("gallery-panel-drywall-install", "2022"),
        ("gallery-commercial-switchgear-tall", "2021"),
        ("gallery-commercial-switchgear-angle", "2021"),
        ("gallery-commercial-bus-duct", "2021"),
        ("gallery-commercial-parking-team", "2023"),
        ("gallery-commercial-meter-bank", "2020"),
        ("gallery-commercial-switchgear-clean", "2023"),
        ("gallery-commercial-switchgear-200a", "2023"),
        ("gallery-roughin-framing-conduit", "2020"),
        ("gallery-roughin-steel-stud", "2021"),
        ("gallery-roughin-foundation-pipe", "2021"),
        ("gallery-construction-apartment", "2021"),
        ("gallery-roughin-worker-framing", "2020"),
        ("gallery-lighting-kitchen", "2020"),
        ("gallery-lighting-commercial-install", "2022"),
        ("gallery-lighting-chandelier", "2022"),
        ("gallery-utility-crane", "2020"),
        ("gallery-team-worker-foundation", "2021"),
        ("gallery-team-utility-lines", "2022"),
        ("gallery-commercial-parking-conduit", "2022"),
        ("gallery-lifestyle-home-pool", "2023"),
        ("gallery-exterior-spanish-apartment", "2023"),
        ("gallery-lighting-kitchen-alt", "2020"),
        ("gallery-equipment-pipe-threader", "2023"),
    ]

    image_tags = "".join(
        f'<image:image><image:loc>https://amyelectric.com/img/gallery/{slug}-1200w.webp</image:loc></image:image>\n'
        for slug, _ in slugs_and_years
    )

    new_gallery_entry = (
        f'<url>\n'
        f'<loc>https://amyelectric.com/gallery</loc>\n'
        f'<lastmod>2026-06-04</lastmod>\n'
        f'<priority>0.7</priority>\n'
        f'{image_tags}'
        f'</url>'
    )

    if gallery_url_match:
        content = content.replace(gallery_url_match.group(1), new_gallery_entry)
        with open(sitemap, 'w') as f:
            f.write(content)
        print(f"  UPDATED sitemap.xml with {len(slugs_and_years)} image entries")
        return True
    else:
        print(f"  WARNING: gallery URL not found in sitemap.xml")
        return False


def main():
    print("=== Service Pages ===")
    for page, photos in SERVICE_PHOTOS.items():
        fp = WEBSITE / page
        if fp.exists():
            update_service_page(fp, photos)
        else:
            print(f"  SKIP {page}: file not found")

    print("\n=== City Pages ===")
    for page, (slug, caption, city) in CITY_PHOTOS.items():
        fp = WEBSITE / page
        if fp.exists():
            update_city_page(fp, slug, caption, city)
        else:
            print(f"  SKIP {page}: file not found")

    print("\n=== Sitemap ===")
    update_sitemap()


if __name__ == "__main__":
    main()
