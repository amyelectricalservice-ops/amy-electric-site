#!/usr/bin/env python3
"""
Shared site data module — single source of truth for all hardcoded data.
Used by schema-tool.py, inject-layout.py, printo-pipeline.py, and others.
"""

import json

SITE_DIR = __file__.rsplit("/", 2)[0]

BUSINESS = {
    "name": "AMY Electric",
    "legalName": "AMY Electric",
    "telephone": "+1-818-302-5614",
    "telephone_display": "(818) 302-5614",
    "email": "info@amyelectric.com",
    "url": "https://amyelectric.com",
    "description": "Licensed C-10 electrical contractor in Los Angeles specializing in EV charger installation, panel upgrades, electrical repairs, and commercial electrical work.",
    "address": {
        "streetAddress": "20628 Londelius St",
        "addressLocality": "Winnetka",
        "addressRegion": "CA",
        "postalCode": "91306",
        "addressCountry": "US"
    },
    "geo": {"latitude": 34.22281, "longitude": -118.58241},
    "image": "https://amyelectric.com/img/hero-electrician.jpg",
    "logo": "https://amyelectric.com/img/og-home.jpg",
    "foundingDate": "2012",
    "priceRange": "$$",
    "license": "C-10 #981578",
    "evitp": "EVITP #4051604",
    "aggregateRating": {"ratingValue": "4.9", "reviewCount": "87", "bestRating": "5", "worstRating": "1"},
    "sameAs": [
        "https://www.yelp.com/biz/amy-electric-los-angeles",
        "https://g.page/r/CVdK9ZAvNBrZEAI/review",
        "https://maps.app.goo.gl/WTNSkHRUgULPBHpc9"
    ],
    "openingHours": [
        {"days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:00", "closes": "17:00", "desc": "Office hours"},
        {"days": "Saturday", "opens": "08:00", "closes": "14:00", "desc": "Office hours"},
        {"days": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "00:00", "closes": "23:59", "desc": "24/7 emergency service dispatch"}
    ],
    "credentials": [
        {"name": "C-10 Electrical Contractor License #981578"},
        {"name": "EVITP Certification #4051604"}
    ]
}

CITIES = [
    {"slug": "los-angeles",       "name": "Los Angeles",       "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "sherman-oaks",      "name": "Sherman Oaks",      "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "burbank",           "name": "Burbank",           "utility": "Burbank Water and Power",  "county": "Los Angeles"},
    {"slug": "glendale",          "name": "Glendale",          "utility": "Glendale Water & Power",    "county": "Los Angeles"},
    {"slug": "pasadena",          "name": "Pasadena",          "utility": "Pasadena Water and Power", "county": "Los Angeles"},
    {"slug": "studio-city",       "name": "Studio City",       "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "north-hollywood",   "name": "North Hollywood",   "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "hollywood",         "name": "Hollywood",         "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "beverly-hills",     "name": "Beverly Hills",     "utility": "Southern California Edison", "county": "Los Angeles"},
    {"slug": "west-la",           "name": "West Los Angeles",  "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "encino",            "name": "Encino",            "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "santa-monica",      "name": "Santa Monica",      "utility": "Southern California Edison", "county": "Los Angeles"},
    {"slug": "van-nuys",          "name": "Van Nuys",          "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "woodland-hills",    "name": "Woodland Hills",    "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "calabasas",         "name": "Calabasas",         "utility": "LADWP",                    "county": "Los Angeles"},
    {"slug": "culver-city",       "name": "Culver City",       "utility": "Southern California Edison", "county": "Los Angeles"},
]

CITY_LOOKUP = {c["slug"]: c for c in CITIES}

SERVICES = [
    {"slug": "ev-charger-installation",     "name": "EV Charger Installation",         "category": "ev"},
    {"slug": "panel-upgrade",               "name": "Panel Upgrade",                   "category": "panel"},
    {"slug": "electrical-repair",           "name": "Electrical Repair",               "category": "repair"},
    {"slug": "commercial-electrical",       "name": "Commercial Electrical",           "category": "commercial"},
    {"slug": "lighting-installation",       "name": "Lighting Installation",           "category": "lighting"},
    {"slug": "ceiling-fan-installation",    "name": "Ceiling Fan Installation",         "category": "fan"},
    {"slug": "outlet-switch-installation",  "name": "Outlet & Switch Installation",    "category": "outlet"},
    {"slug": "whole-home-rewiring",         "name": "Whole Home Rewiring",             "category": "rewire"},
    {"slug": "generator-transfer-switch",   "name": "Generator Transfer Switch",       "category": "generator"},
    {"slug": "dedicated-circuits",          "name": "Dedicated Circuits",              "category": "circuit"},
    {"slug": "smart-home-electrical",       "name": "Smart Home Electrical",           "category": "smart"},
    {"slug": "smoke-co-detector-installation", "name": "Smoke & CO Detector Installation", "category": "safety"},
    {"slug": "surge-protection",            "name": "Surge Protection",                "category": "surge"},
    {"slug": "electrical-safety-inspections", "name": "Electrical Safety Inspections", "category": "safety"},
    {"slug": "tesla-charger-installation",  "name": "Tesla Charger Installation",      "category": "ev"},
]

SERVICE_LOOKUP = {s["slug"]: s for s in SERVICES}

SERVICE_PAGES = [s["slug"] + ".html" for s in SERVICES]

COMPARISON_PAGES = [
    "panel-100a-vs-200a.html",
    "ev-charger-hardwired-vs-plug-in.html",
]

CITY_PAGES = [f"city-{c['slug']}.html" for c in CITIES]

GEO_SERVICE_PAGES = (
    [f"ev-charger-installation-{c['slug']}.html" for c in CITIES] +
    [f"panel-upgrade-{c['slug']}.html" for c in CITIES]
)

EMERGENCY_PAGES = [
    "emergency-electrician.html",
    "electrical-fire-emergency.html",
    "power-outage-electrician.html",
    "electrical-safety.html",
    "no-power-electrician.html",
]

ROOT_PAGES = ["index.html"] + SERVICE_PAGES + COMPARISON_PAGES + EMERGENCY_PAGES
ALL_PAGES = ROOT_PAGES + CITY_PAGES + GEO_SERVICE_PAGES

NAV_LINKS = [
    ("Home", "index"),
    ("EV Charger Installation", "ev-charger-installation"),
    ("Panel Upgrades", "panel-upgrade"),
    ("Electrical Repairs", "electrical-repair"),
    ("Commercial", "commercial-electrical"),
    ("Lighting", "lighting-installation"),
    ("Tesla Charger", "tesla-charger-installation"),
    ("Rewiring", "whole-home-rewiring"),
    ("Surge Protection", "surge-protection"),
    ("Reviews", "testimonials"),
    ("Gallery", "gallery"),
    ("Service Areas", "city-los-angeles"),
]

NAV_LINKS_BLOG = NAV_LINKS + [
    ("Outlet & Switch", "outlet-switch-installation"),
    ("Ceiling Fan", "ceiling-fan-installation"),
    ("Smoke & CO Detector", "smoke-co-detector-installation"),
    ("Generator Transfer Switch", "generator-transfer-switch"),
    ("Dedicated Circuits", "dedicated-circuits"),
    ("Smart Home", "smart-home-electrical"),
    ("Safety Inspections", "electrical-safety-inspections"),
]


def make_electrician(path=""):
    """Generate Electrician JSON-LD for a given page path."""
    url = f"https://amyelectric.com/{path}" if path else "https://amyelectric.com"
    return {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "@id": url,
        "name": BUSINESS["name"],
        "image": BUSINESS["image"],
        "url": url,
        "telephone": BUSINESS["telephone"],
        "email": BUSINESS["email"],
        "description": BUSINESS["description"],
        "address": BUSINESS["address"],
        "geo": BUSINESS["geo"],
        "foundingDate": BUSINESS["foundingDate"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"], "description": h["desc"]}
            for h in BUSINESS["openingHours"]
        ],
        "aggregateRating": BUSINESS["aggregateRating"],
        "hasCredential": BUSINESS["credentials"],
        "priceRange": BUSINESS["priceRange"],
        "sameAs": BUSINESS["sameAs"]
    }


def make_service(name=None):
    """Generate a Service schema stub."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "provider": {"@type": "Electrician", "name": BUSINESS["name"]},
        "areaServed": {
            "@type": "City",
            "name": "Los Angeles",
            "sameAs": "https://en.wikipedia.org/wiki/Los_Angeles"
        },
        "offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "USD"}}
    }


def make_faqpage(questions):
    """Generate FAQPage JSON-LD from a list of {q, a} dicts."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in questions
        ]
    }


def make_breadcrumb(items):
    """Generate BreadcrumbList JSON-LD.
    items: list of (position, name, url_path) tuples.
    """
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": pos, "name": name, "item": f"https://amyelectric.com/{url_path}"}
            for pos, name, url_path in items
        ]
    }


def make_blogposting(headline, description, image, date_published, date_modified, url_path, author_name="Amy"):
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": description,
        "image": image,
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {
            "@type": "Person",
            "name": author_name,
            "image": "https://amyelectric.com/img/author-amy-400w.jpg",
            "description": "California C-10 licensed electrical contractor with 15+ years of experience",
            "url": "https://amyelectric.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": BUSINESS["name"],
            "logo": {"@type": "ImageObject", "url": BUSINESS["logo"]}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://amyelectric.com/{url_path}"}
    }


def make_website():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BUSINESS["name"],
        "url": BUSINESS["url"],
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": f"{BUSINESS['url']}/?q={{search_term_string}}"}
        }
    }


def json_ld(data):
    """Render JSON-LD as an HTML script tag, minified."""
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'


def json_ld_pretty(data):
    """Render JSON-LD as an HTML script tag, pretty-printed."""
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2, ensure_ascii=False)}\n</script>'
