#!/usr/bin/env python3
"""
Batch schema enrichment for AMY Electric site.

For each page:
  - If no standalone Electrician schema exists, inject a full one
  - If standalone Electrician exists but is incomplete (no openingHoursSpecification
    or hasCredential), replace it with the full version
  - Ensure 24/7 emergency hours in openingHoursSpecification
  - Add FAQPage schema to testimonials.html and gallery.html
"""
import re
import json
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent

CITIES = [
    "los-angeles", "sherman-oaks", "burbank", "glendale", "pasadena",
    "studio-city", "north-hollywood", "hollywood", "beverly-hills",
    "west-la", "encino", "santa-monica", "van-nuys", "woodland-hills",
    "calabasas", "culver-city"
]

ALL_HTML = [f.stem for f in SITE_DIR.glob("*.html")
            if f.is_file() and not f.name.startswith('_')
            and 'amyelectric-site' not in str(f)]

FULL_ELEC = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Electrician",
  "@id": "https://amyelectric.com/__PATH__",
  "name": "AMY Electric",
  "image": "https://amyelectric.com/img/hero-electrician.jpg",
  "url": "https://amyelectric.com/__PATH__",
  "telephone": "+1-818-302-5614",
  "email": "info@amyelectric.com",
  "description": "Licensed C-10 electrical contractor in Los Angeles. Specializing in EV charger installation, panel upgrades, electrical repairs, and commercial electrical work.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "20628 Londelius St",
    "addressLocality": "Winnetka",
    "addressRegion": "CA",
    "postalCode": "91306",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 34.22281,
    "longitude": -118.58241
  },
  "foundingDate": "2012",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:00",
      "closes": "17:00",
      "description": "Office hours"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "14:00",
      "description": "Office hours"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "00:00",
      "closes": "23:59",
      "description": "24/7 emergency service dispatch"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "87",
    "bestRating": "5",
    "worstRating": "1"
  },
  "hasCredential": [
    {
      "@type": "EducationalOccupationalCredential",
      "name": "C-10 Electrical Contractor License #981578"
    },
    {
      "@type": "EducationalOccupationalCredential",
      "name": "EVITP Certification #4051604"
    }
  ],
  "priceRange": "$$",
  "sameAs": [
    "https://www.yelp.com/biz/amy-electric-los-angeles",
    "https://g.page/r/CVdK9ZAvNBrZEAI/review",
    "https://maps.app.goo.gl/WTNSkHRUgULPBHpc9"
  ]
}
</script>"""

FAQ_TESTIMONIALS = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How can I leave a review for AMY Electric?","acceptedAnswer":{"@type":"Answer","text":"You can leave a review on Google, Yelp, or Nextdoor. The fastest way is to use our direct Google review link: https://g.page/r/CVdK9ZAvNBrZEAI/review. We appreciate detailed feedback about your experience with our electrical services."}},{"@type":"Question","name":"How quickly do you respond to reviews?","acceptedAnswer":{"@type":"Answer","text":"We respond to all reviews within 48 hours, including weekends. Each review is personally read and responded to. If you've had a less-than-perfect experience, please mention it in your review so we can make it right."}},{"@type":"Question","name":"Are your Google reviews verified?","acceptedAnswer":{"@type":"Answer","text":"Yes — every review on our Google Business Profile is from a verified Google user who has interacted with our business. We never solicit fake reviews or offer incentives for positive reviews. Our 4.9-star rating across 87+ reviews reflects real customer experiences with our electrical services."}}]}</script>"""

FAQ_GALLERY = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What types of electrical projects are shown in the gallery?","acceptedAnswer":{"@type":"Answer","text":"Our gallery features real projects completed by AMY Electric across Los Angeles, including panel upgrades, EV charger installations, new construction wiring, commercial electrical work, lighting installations, and service upgrades. Each photo includes a description of the work performed."}},{"@type":"Question","name":"How are the gallery photos selected?","acceptedAnswer":{"@type":"Answer","text":"We select photos that showcase our best work and represent the range of electrical services we offer. All photos are of actual projects we've completed for real clients in Los Angeles, Sherman Oaks, Burbank, Glendale, Pasadena, and surrounding areas."}},{"@type":"Question","name":"Can I request photos of work similar to my project?","acceptedAnswer":{"@type":"Answer","text":"Yes — if you're considering a specific type of electrical work and want to see examples, call us at (818) 302-5614. We can share photos of similar projects we've completed and arrange a free on-site estimate to discuss your specific needs."}}]}</script>"""


def get_electrician_block(content):
    """Return (script_start, script_end, data) for the standalone Electrician block, or None."""
    blocks = re.finditer(
        r'<script type="application/ld\+json">(.*?)</script>',
        content, re.DOTALL
    )
    for m in blocks:
        block_text = m.group(1).strip()
        try:
            data = json.loads(block_text)
            if isinstance(data, dict) and data.get('@type') == 'Electrician':
                if '@graph' not in data:
                    return (m.start(), m.end(), data)
            if isinstance(data, dict) and '@graph' in data:
                for item in data['@graph']:
                    if isinstance(item, dict) and item.get('@type') == 'Electrician':
                        return (m.start(), m.end(), data)
        except json.JSONDecodeError:
            pass
    return None


def electrician_is_complete(data):
    """Check if an Electrician schema has all required fields."""
    if isinstance(data, dict) and '@graph' in data:
        for item in data['@graph']:
            if isinstance(item, dict) and item.get('@type') == 'Electrician':
                data = item
                break
    required_keys = ['openingHoursSpecification', 'hasCredential', 'aggregateRating']
    return all(k in data for k in required_keys)


def has_faqpage(content):
    """Check if page already has FAQPage schema."""
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        content, re.DOTALL
    )
    for block in blocks:
        try:
            data = json.loads(block.strip())
            if isinstance(data, dict) and data.get('@type') == 'FAQPage':
                return True
        except json.JSONDecodeError:
            pass
    return False


def replace_elec_block(content, path):
    """Replace existing standalone Electrician block with full version, or inject one."""
    result = get_electrician_block(content)
    block = FULL_ELEC.replace('__PATH__', path)

    if result:
        start, end, data = result
        if electrician_is_complete(data) and '24/7' in json.dumps(data):
            return content  # Already complete
        # Replace old block with new
        return content[:start] + block + '\n' + content[end:]
    else:
        # No standalone Electrician at all — inject before first Service or before </head>
        svc = re.search(
            r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org"\s*,\s*"@type":\s*"Service"',
            content, re.DOTALL
        )
        if svc:
            pos = svc.start()
            return content[:pos] + '\n' + block + '\n' + content[pos:]
        # Inject before </head>
        return content.replace('</head>', block + '\n</head>', 1)


def inject_faq(content, faq_block, anchor_before='BreadcrumbList'):
    """Inject FAQPage schema before the first BreadcrumbList script or before </head>."""
    pattern = re.compile(
        fr'<script type="application/ld\+json">{{"@context":"https://schema\.org","@type":"{anchor_before}"'
    )
    match = pattern.search(content)
    if match:
        pos = match.start()
        return content[:pos] + '\n' + faq_block + '\n' + content[pos:]
    return content.replace('</head>', faq_block + '\n</head>', 1)


def main():
    changed_files = []

    for html_file in sorted(SITE_DIR.glob("*.html")):
        fname = html_file.name
        if 'amyelectric-site' in str(html_file):
            continue

        content = html_file.read_text(encoding='utf-8')
        stem = html_file.stem
        path = stem if stem != 'index' else ''
        modified = False

        # --- Electrician schema ---
        elec = get_electrician_block(content)
        if elec:
            _, _, data = elec
            if not electrician_is_complete(data) or '24/7' not in json.dumps(data):
                new_content = replace_elec_block(content, path)
                if new_content != content:
                    content = new_content
                    modified = True
                    print(f"  ~ Replaced Electrician -> {fname}")
            else:
                pass  # already complete
        else:
            new_content = replace_elec_block(content, path)
            if new_content != content:
                content = new_content
                modified = True
                print(f"  + Injected Electrician -> {fname}")

        # --- FAQPage schema ---
        needs_faq = False
        faq_block = None
        if fname == 'testimonials.html':
            needs_faq = True
            faq_block = FAQ_TESTIMONIALS
        elif fname == 'gallery.html':
            needs_faq = True
            faq_block = FAQ_GALLERY

        if needs_faq and not has_faqpage(content):
            new_content = inject_faq(content, faq_block)
            if new_content != content:
                content = new_content
                modified = True
                print(f"  + FAQPage -> {fname}")

        if modified:
            html_file.write_text(content, encoding='utf-8')
            changed_files.append(fname)

    print(f"\n{'='*60}")
    print(f"Schema enrichment complete. {len(changed_files)} files changed.")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
