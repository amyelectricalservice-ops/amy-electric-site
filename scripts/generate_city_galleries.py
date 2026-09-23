#!/usr/bin/env python3
"""Generate city-specific gallery pages from photo manifest."""

import csv
import json
import re
from pathlib import Path

WEBSITE = Path(__file__).parent.parent
MANIFEST = WEBSITE / "scripts/photo-manifest.csv"
GALLERY_TEMPLATE = WEBSITE / "gallery.html"
CITY_TEMPLATE = WEBSITE / "city-los-angeles.html"

CATEGORY_LABELS = {
    "panel": ("Panel Upgrades", "rgba(245,166,35,.2)", "#f5a623"),
    "commercial": ("Commercial", "rgba(74,144,217,.2)", "#4a90d9"),
    "new-construction": ("New Construction", "rgba(126,200,80,.2)", "#7ec850"),
    "lighting": ("Lighting", "rgba(232,123,156,.2)", "#e87b9c"),
    "team": ("Team", "rgba(155,89,182,.2)", "#9b59b6"),
    "lifestyle": ("Lifestyle", "rgba(230,126,34,.2)", "#e67e22"),
    "exterior": ("Exteriors", "rgba(26,188,156,.2)", "#1abc9c"),
    "equipment": ("Equipment", "rgba(149,165,166,.2)", "#95a5a6"),
    "uncategorized": ("Project", "rgba(149,165,166,.2)", "#95a5a6"),
}

CITY_SLUGS = {
    "Los Angeles": "los-angeles",
    "Sherman Oaks": "sherman-oaks",
    "Beverly Hills": "beverly-hills",
    "Studio City": "studio-city",
    "Encino": "encino",
    "Santa Monica": "santa-monica",
    "Pasadena": "pasadena",
    "North Hollywood": "north-hollywood",
    "Hollywood Hills": "hollywood-hills",
    "Glendale": "glendale",
    "Burbank": "burbank",
}

def read_manifest():
    with open(MANIFEST, newline="") as f:
        return list(csv.DictReader(f))

def slugify(text):
    return text.lower().replace(" ", "-").replace(".", "")

def get_city_photos(rows, city):
    return [r for r in rows if r.get("city", "").strip() == city]

def make_item_html(row):
    cat = row.get("category", "uncategorized").strip() or "uncategorized"
    label, bg, color = CATEGORY_LABELS.get(cat, CATEGORY_LABELS["uncategorized"])
    city = row.get("city", "Los Angeles").strip()
    year = row.get("year", "2025").strip() or "2025"
    caption = row.get("caption", "").strip() or "Electrical project by AMY Electric"
    slug = row["slug"].strip()
    alt = f"{caption} - AMY Electric {city}"
    return f'''    <div class="gallery-item" data-category="{cat}" data-city="{city}" data-year="{year}">
      <picture>
        <source srcset="img/gallery/{slug}-400w.webp 400w, img/gallery/{slug}-800w.webp 800w, img/gallery/{slug}-1200w.webp 1200w" type="image/webp" sizes="(max-width: 480px) calc(100vw - 48px), (max-width: 768px) calc(50vw - 36px), (max-width: 1400px) calc(33vw - 32px), 300px">
        <source srcset="img/gallery/{slug}-1200w.jpg" type="image/jpeg">
        <img src="img/gallery/{slug}-1200w.jpg" alt="{alt}" width="1200" height="900" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-overlay">
        <h3>{caption}</h3>
        <p class="gallery-location">{city}, CA &middot; {year}</p>
        <span class="gallery-tag" style="background:{bg};color:{color}">{label}</span>
      </div>
    </div>'''

def make_itemlist_json(rows, city):
    items = []
    for i, r in enumerate(rows, 1):
        slug = r["slug"]
        caption = r.get("caption", "").strip() or "Electrical project by AMY Electric"
        year = r.get("year", "2025").strip() or "2025"
        items.append(
            f'{{"@type":"ListItem","position":{i},"item":{{"@type":"ImageObject",'
            f'"contentUrl":"https://amyelectric.com/img/gallery/{slug}-1200w.webp",'
            f'"caption":"{caption} in {city}, CA","name":"{caption}",'
            f'"uploadDate":"{year}-01-01"}}}}'
        )
    return '{"@context":"https://schema.org","@type":"ItemList","itemListElement":[\n' + ",\n".join(items) + "\n]}"

def read_template(path):
    return path.read_text(encoding="utf-8")

def generate_city_gallery(city, photos, template):
    slug = CITY_SLUGS.get(city, slugify(city))
    city_lower = city.lower()
    city_title = city.title()
    
    # Count photos by category
    cat_counts = {}
    for r in photos:
        cat = r.get("category", "uncategorized").strip() or "uncategorized"
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    # Build filter chips
    filter_chips = ['<button class="filter-chip active" data-filter="all">All</button>']
    for cat in ["panel", "commercial", "new-construction", "lighting", "rewiring", "ev-charger"]:
        if cat in cat_counts:
            label = CATEGORY_LABELS.get(cat, (cat.title(), "", ""))[0]
            filter_chips.append(f'<button class="filter-chip" data-filter="{cat}">{label} ({cat_counts[cat]})</button>')
    
    filter_html = "  <div class=\"gallery-filters\">\n" + "\n".join(filter_chips) + "\n  </div>\n"
    
    # Gallery items HTML
    items_html = "\n".join(make_item_html(r) for r in photos)
    
    # ItemList JSON-LD
    itemlist_json = make_itemlist_json(photos, city)
    
    # LocalBusiness schema with city-specific areaServed
    localbusiness_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://amyelectric.com/gallery-{slug}",
  "name": "AMY Electric",
  "image": "https://amyelectric.com/img/hero-electrician.jpg",
  "url": "https://amyelectric.com/gallery-{slug}",
  "telephone": "+1-818-302-5614",
  "email": "info@amyelectric.com",
  "description": "View our gallery of real electrical projects completed in {city_title}, CA. Panel upgrades, EV charger installations, rewiring, lighting, and commercial work.",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "20628 Londelius St",
    "addressLocality": "Winnetka",
    "addressRegion": "CA",
    "postalCode": "91306",
    "addressCountry": "US"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": 34.22281,
    "longitude": -118.58241
  }},
  "areaServed": {{
    "@type": "City",
    "name": "{city_title}"
  }},
  "priceRange": "$$",
  "hasCredential": [
    {{"@type": "EducationalOccupationalCredential", "name": "C-10 Electrical Contractor License #981578"}},
    {{"@type": "EducationalOccupationalCredential", "name": "EVITP Certification #4051604"}}
  ],
  "sameAs": [
    "https://www.yelp.com/biz/amy-electric-los-angeles",
    "https://g.page/r/CVdK9ZAvNBrZEAI/review",
    "https://maps.app.goo.gl/WTNSkHRUgULPBHpc9",
    "https://www.facebook.com/people/Amy-Electric/100063766463600/"
  ]
}}
</script>'''

    if cat_counts.get("panel", 0) > 0:
        panel_answer = f"Yes — we have panel upgrade photos from {city_title}. Use the Panel Upgrades filter above to see them."
    else:
        panel_answer = f"We don't currently have panel upgrade photos from {city_title} in our gallery, but we've completed many panel upgrades in the area. Call us at (818) 302-5614 and we can share similar project examples."

    has_ev_photos = any("ev" in r.get("slug", "").lower() or "charger" in r.get("slug", "").lower() for r in photos)
    if has_ev_photos:
        ev_answer = f"Yes — use the filters above to see EV charger installations in {city_title}."
    else:
        ev_answer = f"We don't currently have EV charger photos from {city_title} in our gallery, but we're EVITP-certified and install chargers throughout {city_title}. Contact us for project examples."

    faq_data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Can I see photos of electrical work you've done in {city_title}?",
                "acceptedAnswer": {"@type": "Answer", "text": f"Yes — this gallery shows {len(photos)} real projects we've completed in {city_title}. You can browse panel upgrades, EV charger installations, lighting, rewiring, and commercial electrical work. Each photo includes a description of the work performed and the year it was completed."},
            },
            {
                "@type": "Question",
                "name": f"Do you have examples of panel upgrades in {city_title}?",
                "acceptedAnswer": {"@type": "Answer", "text": panel_answer},
            },
            {
                "@type": "Question",
                "name": f"Can I see EV charger installation photos from {city_title}?",
                "acceptedAnswer": {"@type": "Answer", "text": ev_answer},
            },
        ],
    }
    faq_schema = "<script type=\"application/ld+json\">" + json.dumps(faq_data, ensure_ascii=False) + "</script>"

    breadcrumb_schema = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://amyelectric.com/"}},{{"@type":"ListItem","position":2,"name":"Gallery","item":"https://amyelectric.com/gallery"}},{{"@type":"ListItem","position":3,"name":"{city_title} Gallery","item":"https://amyelectric.com/gallery-{slug}"}}]}}</script>'''

    # Replace placeholders in template
    content = template
    
    # Update title and meta
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{city_title} Project Gallery | AMY Electric Los Angeles</title>',
        content
    )
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="View our gallery of {len(photos)} real electrical projects in {city_title}, CA. Panel upgrades, EV charger installs, rewiring, lighting & commercial work. Call (818) 302-5614.">',
        content
    )
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{city_title} Project Gallery | AMY Electric">',
        content
    )
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="View our gallery of {len(photos)} real electrical projects in {city_title}, CA. Panel upgrades, EV charger installations, commercial work, lighting, and new construction.">',
        content
    )
    content = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="https://amyelectric.com/gallery-{slug}">',
        content
    )
    content = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="https://amyelectric.com/img/gallery/{photos[0]["slug"]}-1200w.webp">',
        content
    )
    content = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="https://amyelectric.com/gallery-{slug}">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{city_title} Project Gallery | AMY Electric">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="View our gallery of {len(photos)} real electrical projects in {city_title}, CA. Panel upgrades, EV charger installations, commercial work, lighting, and new construction.">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="https://amyelectric.com/img/gallery/{photos[0]["slug"]}-1200w.webp">',
        content
    )
    
    # Update page hero
    content = re.sub(
        r'<div class="breadcrumb">.*?</div>',
        f'<div class="breadcrumb"><a href="/">Home</a> › <a href="/gallery">Gallery</a> › {city_title}</div>',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<h1>.*?</h1>',
        f'<h1>{city_title} Project Gallery</h1>',
        content
    )
    photo_word = "project" if len(photos) == 1 else "projects"
    content = re.sub(
        r'<p>See our work in action across Los Angeles.*?</p>',
        f'<p>Browse {len(photos)} real electrical {photo_word} completed by AMY Electric in {city_title}, California. Panel upgrades, EV chargers, rewiring, lighting, and commercial work.</p>',
        content,
        flags=re.DOTALL
    )
    
    # Replace gallery section
    grid_start = content.find('<div class="gallery-grid" id="gallery-grid">')
    if grid_start == -1:
        # Try alternative pattern
        grid_start = content.find('<div class="gallery-grid">')
    if grid_start != -1:
        section_end = content.find('</section>', grid_start)
        if section_end != -1:
            new_grid = f'<div class="gallery-grid" id="gallery-grid">\n{items_html}\n  </div>\n{filter_html}</section>'
            content = content[:grid_start] + new_grid + content[section_end + len('</section>'):]
    
    # Replace FAQPage schema - match entire script tag
    content = re.sub(
        r'<script type="application/ld\+json">\{[^<]*"@type"\s*:\s*"FAQPage"[^<]*\}</script>',
        faq_schema.strip(),
        content,
        flags=re.DOTALL
    )
    
    # Replace BreadcrumbList schema - match entire script tag
    content = re.sub(
        r'<script type="application/ld\+json">\{[^<]*"@type"\s*:\s*"BreadcrumbList"[^<]*\}</script>',
        breadcrumb_schema.strip(),
        content,
        flags=re.DOTALL
    )
    
    # Replace ItemList schema (wrapped in @graph) - match entire script tag containing @graph and ItemList
    content = re.sub(
        r'<script type="application/ld\+json">\{[^<]*"@graph"[^<]*"@type"\s*:\s*"ItemList"[^<]*\}</script>',
        f'<script type="application/ld+json">{itemlist_json}</script>',
        content,
        flags=re.DOTALL
    )
    
    # Inject LocalBusiness schema before </head>
    head_end = content.find('</head>')
    if head_end != -1:
        content = content[:head_end] + "\n" + localbusiness_schema + content[head_end:]
    
    # Remove inline style blocks that duplicate CSS
    content = re.sub(r'<style>.*?</style>', '', content, count=1, flags=re.DOTALL)  # First inline style (full CSS)
    content = re.sub(r'<style>\s*\.gallery-filters.*?</style>', '', content, flags=re.DOTALL)  # Gallery CSS
    
    # Update structured data count in meta
    content = re.sub(
        r'View our gallery of \d+\+? real electrical projects',
        f'View our gallery of {len(photos)} real electrical projects',
        content
    )
    
    return content

def main():
    rows = read_manifest()
    template = read_template(GALLERY_TEMPLATE)
    
    # Group by city
    cities = {}
    for row in rows:
        city = row.get("city", "").strip()
        if city and city.lower() != "city":
            if city not in cities:
                cities[city] = []
            cities[city].append(row)
    
    print(f"Found {len(cities)} cities with photos")
    
    for city, photos in cities.items():
        if len(photos) < 1:
            continue
        slug = CITY_SLUGS.get(city, slugify(city))
        output_file = WEBSITE / f"gallery-{slug}.html"
        
        print(f"Generating {output_file.name} ({len(photos)} photos)...")
        content = generate_city_gallery(city, photos, template)
        output_file.write_text(content, encoding="utf-8")
    
    print("Done!")

if __name__ == "__main__":
    main()