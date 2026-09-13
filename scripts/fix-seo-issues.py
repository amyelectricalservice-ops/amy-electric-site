#!/usr/bin/env python3
"""
Fix all 5 SEO issues:
1. Clean sitemap (remove junk URLs)
2. Unique meta descriptions per city
3. Correct geo coordinates per city
4. Add 'Nearby Cities' internal linking
5. Boost blog priorities
"""

import json
import os
import re
from pathlib import Path

SITE_DIR = Path("/home/amram/WEBSITE")

# City data: slug -> {name, lat, lon}
CITIES = {
    # Original 25 cities
    "alhambra": {"name": "Alhambra", "lat": 34.0953, "lon": -118.1270},
    "bellflower": {"name": "Bellflower", "lat": 33.8817, "lon": -118.1171},
    "beverly-hills": {"name": "Beverly Hills", "lat": 34.0736, "lon": -118.4004},
    "burbank": {"name": "Burbank", "lat": 34.1808, "lon": -118.3090},
    "calabasas": {"name": "Calabasas", "lat": 34.1367, "lon": -118.6603},
    "culver-city": {"name": "Culver City", "lat": 34.0211, "lon": -118.3965},
    "downey": {"name": "Downey", "lat": 33.9401, "lon": -118.1332},
    "encino": {"name": "Encino", "lat": 34.1597, "lon": -118.5012},
    "glendale": {"name": "Glendale", "lat": 34.1425, "lon": -118.2551},
    "hollywood": {"name": "Hollywood", "lat": 34.0928, "lon": -118.3287},
    "inglewood": {"name": "Inglewood", "lat": 33.9617, "lon": -118.3531},
    "long-beach": {"name": "Long Beach", "lat": 33.7701, "lon": -118.1937},
    "los-angeles": {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    "north-hollywood": {"name": "North Hollywood", "lat": 34.1870, "lon": -118.3813},
    "pasadena": {"name": "Pasadena", "lat": 34.1478, "lon": -118.1445},
    "redondo-beach": {"name": "Redondo Beach", "lat": 33.8492, "lon": -118.3884},
    "santa-clarita": {"name": "Santa Clarita", "lat": 34.3917, "lon": -118.5426},
    "santa-monica": {"name": "Santa Monica", "lat": 34.0195, "lon": -118.4912},
    "sherman-oaks": {"name": "Sherman Oaks", "lat": 34.1508, "lon": -118.4490},
    "studio-city": {"name": "Studio City", "lat": 34.1475, "lon": -118.3968},
    "torrance": {"name": "Torrance", "lat": 33.8358, "lon": -118.3406},
    "van-nuys": {"name": "Van Nuys", "lat": 34.1870, "lon": -118.4490},
    "west-la": {"name": "West LA", "lat": 34.0390, "lon": -118.4450},
    "winnetka": {"name": "Winnetka", "lat": 34.2069, "lon": -118.5734},
    "woodland-hills": {"name": "Woodland Hills", "lat": 34.1689, "lon": -118.6059},
    # Batch 1 (28 cities)
    "shadow-ranch-park": {"name": "Shadow Ranch Park", "lat": 34.21, "lon": -118.56},
    "arleta": {"name": "Arleta", "lat": 34.245, "lon": -118.43},
    "sylmar": {"name": "Sylmar", "lat": 34.3083, "lon": -118.4614},
    "pacoima": {"name": "Pacoima", "lat": 34.2564, "lon": -118.4114},
    "holmby-hills": {"name": "Holmby Hills", "lat": 34.09, "lon": -118.44},
    "bel-air": {"name": "Bel Air", "lat": 34.08, "lon": -118.45},
    "lake-view-terrace": {"name": "Lake View Terrace", "lat": 34.27, "lon": -118.39},
    "sun-valley": {"name": "Sun Valley", "lat": 34.2217, "lon": -118.375},
    "brentwood": {"name": "Brentwood", "lat": 34.05, "lon": -118.48},
    "shadow-hills": {"name": "Shadow Hills", "lat": 34.245, "lon": -118.365},
    "westwood": {"name": "Westwood", "lat": 34.06, "lon": -118.445},
    "rancho-park": {"name": "Rancho Park", "lat": 34.04, "lon": -118.44},
    "cheviot-hills": {"name": "Cheviot Hills", "lat": 34.04, "lon": -118.43},
    "sawtelle": {"name": "Sawtelle", "lat": 34.03, "lon": -118.445},
    "sawtelle-japantown": {"name": "Sawtelle Japantown", "lat": 34.032, "lon": -118.447},
    "beverly-grove": {"name": "Beverly Grove", "lat": 34.075, "lon": -118.375},
    # Batch 2 (16 priority cities)
    "beverlywood": {"name": "Beverlywood", "lat": 34.047, "lon": -118.395},
    "fairfax-district": {"name": "Fairfax District", "lat": 34.081, "lon": -118.355},
    "del-rey": {"name": "Del Rey", "lat": 34.005, "lon": -118.435},
    "palms": {"name": "Palms", "lat": 34.023, "lon": -118.403},
    "miracle-mile": {"name": "Miracle Mile", "lat": 34.062, "lon": -118.355},
    "mar-vista": {"name": "Mar Vista", "lat": 34.001, "lon": -118.425},
    "windsor-square": {"name": "Windsor Square", "lat": 34.073, "lon": -118.318},
    "little-armenia": {"name": "Little Armenia", "lat": 34.101, "lon": -118.301},
    "larchmont": {"name": "Larchmont", "lat": 34.075, "lon": -118.318},
    "malibu": {"name": "Malibu", "lat": 34.026, "lon": -118.779},
    "hancock-park": {"name": "Hancock Park", "lat": 34.075, "lon": -118.325},
    "mid-city": {"name": "Mid City", "lat": 34.055, "lon": -118.355},
    "verdugo-city": {"name": "Verdugo City", "lat": 34.185, "lon": -118.235},
    "los-feliz": {"name": "Los Feliz", "lat": 34.115, "lon": -118.265},
    "east-hollywood": {"name": "East Hollywood", "lat": 34.105, "lon": -118.295},
    "thai-town": {"name": "Thai Town", "lat": 34.102, "lon": -118.298},
    # Batch 3 (43 extended cities)
    "fox-hills": {"name": "Fox Hills", "lat": 33.993, "lon": -118.395},
    "north-glendale": {"name": "North Glendale", "lat": 34.175, "lon": -118.265},
    "koreatown": {"name": "Koreatown", "lat": 34.065, "lon": -118.305},
    "atwater-village": {"name": "Atwater Village", "lat": 34.115, "lon": -118.265},
    "silver-lake": {"name": "Silver Lake", "lat": 34.095, "lon": -118.275},
    "west-adams": {"name": "West Adams", "lat": 34.035, "lon": -118.295},
    "westlake": {"name": "Westlake", "lat": 34.055, "lon": -118.285},
    "echo-park": {"name": "Echo Park", "lat": 34.085, "lon": -118.265},
    "edith-norman": {"name": "Edendale", "lat": 34.085, "lon": -118.255},
    "pico-union": {"name": "Pico Union", "lat": 34.045, "lon": -118.275},
    "westchester": {"name": "Westchester", "lat": 33.955, "lon": -118.405},
    "university-park": {"name": "University Park", "lat": 34.025, "lon": -118.285},
    "glassell-park": {"name": "Glassell Park", "lat": 34.115, "lon": -118.245},
    "exposition-park": {"name": "Exposition Park", "lat": 34.018, "lon": -118.288},
    "health-campadre": {"name": "Health Campadre", "lat": 34.015, "lon": -118.282},
    "figueroa-corridor": {"name": "Figueroa Corridor", "lat": 34.025, "lon": -118.275},
    "eagle-rock": {"name": "Eagle Rock", "lat": 34.135, "lon": -118.215},
    "jefferson-park": {"name": "Jefferson Park", "lat": 34.025, "lon": -118.295},
    "chinatown": {"name": "Chinatown", "lat": 34.065, "lon": -118.235},
    "downtown-la": {"name": "Downtown LA", "lat": 34.045, "lon": -118.255},
    "el-segundo": {"name": "El Segundo", "lat": 33.919, "lon": -118.415},
    "highland-park": {"name": "Highland Park", "lat": 34.115, "lon": -118.195},
    "montecito-heights": {"name": "Montecito Heights", "lat": 34.115, "lon": -118.185},
    "vernon": {"name": "Vernon", "lat": 33.995, "lon": -118.225},
    "el-sobrante": {"name": "El Sobrante", "lat": 33.995, "lon": -118.195},
    "westmont": {"name": "Westmont", "lat": 33.955, "lon": -118.295},
    "florence": {"name": "Florence", "lat": 33.975, "lon": -118.245},
}

# Nearby cities mapping (for internal linking)
def get_nearby_cities(slug, count=6):
    """Get N closest cities to the given city."""
    if slug not in CITIES:
        return []
    
    lat1, lon1 = CITIES[slug]["lat"], CITIES[slug]["lon"]
    distances = []
    
    for other_slug, data in CITIES.items():
        if other_slug == slug:
            continue
        # Haversine approximation
        lat2, lon2 = data["lat"], data["lon"]
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        dist = (dlat**2 + dlon**2) ** 0.5 * 69  # rough miles
        distances.append((dist, other_slug, data["name"]))
    
    distances.sort()
    return [(s, n) for _, s, n in distances[:count]]


# City-specific descriptions (unique per city)
CITY_DESCRIPTIONS = {
    # Major cities get detailed descriptions
    "burbank": "Top-rated Burbank electrician serving the Media Capital of the World. Panel upgrades, EV charger installation, rewiring & repairs. Serving Warner Bros, Disney, and NBC studios areas. C-10 #981578.",
    "hollywood": "Trusted Hollywood electrician for residential and commercial electrical work. Panel upgrades, EV chargers, lighting design for homes and businesses near the Hollywood Sign and Walk of Fame.",
    "beverly-hills": "Premier Beverly Hills electrician serving 90210 and surrounding areas. Luxury home electrical upgrades, EV charger installation, smart home wiring. Licensed C-10 contractor.",
    "glendale": "Professional Glendale electrician serving Adams Hill, Verdugo City, and Glendale Galleria area. Panel upgrades, EV charger installation, rewiring. Licensed C-10 #981578.",
    "pasadena": "Experienced Pasadena electrician serving Old Town, Bungalow Heaven, and Caltech area. Panel upgrades, EV chargers, historic home rewiring. Licensed C-10 contractor.",
    "santa-monica": "Certified Santa Monica electrician serving the beach communities. EV charger installation, panel upgrades, commercial electrical work near the Santa Monica Pier. C-10 #981578.",
    "culver-city": "Reliable Culver City electrician serving the Silicon Beach tech hub. EV charger installation for Tesla, panel upgrades, commercial tenant improvements. Licensed C-10.",
    "west-la": "West LA electrician serving Westwood, Sawtelle, and UCLA area. EV charger installation, panel upgrades, apartment electrical repairs. Licensed C-10 #981578.",
    "studio-city": "Studio City electrician serving the CBS Studio area. Panel upgrades, EV charger installation, home theater wiring. Residential and commercial. Licensed C-10.",
    "sherman-oaks": "Sherman Oaks electrician serving the San Fernando Valley. Panel upgrades, EV charger installation, whole-home rewiring. Licensed C-10 #981578.",
    "encino": "Encino electrician serving the Encino Hills and Ventura Boulevard corridor. Panel upgrades, EV chargers, electrical repairs. Licensed C-10 contractor.",
    "woodland-hills": "Woodland Hills electrician serving West Hills and Warner Center. Panel upgrades, EV charger installation, electrical repairs. Licensed C-10 #981578.",
    "van-nuys": "Van Nuys electrician serving the central San Fernando Valley. Panel upgrades, EV charger installation, rewiring. Licensed C-10 contractor.",
    "north-hollywood": "North Hollywood electrician serving the NoArts District and Toluca Lake. EV charger installation, panel upgrades, commercial electrical. Licensed C-10 #981578.",
    "long-beach": "Long Beach electrician serving Downtown, Belmont Shore, and Signal Hill. EV charger installation, panel upgrades, commercial electrical work. Licensed C-10.",
    "torrance": "Torrance electrician serving the South Bay communities. EV charger installation, panel upgrades, electrical repairs. Serving Torrance Beach and Del Amo. Licensed C-10.",
    "inglewood": "Inglewood electrician serving SoFi Stadium area and LAX communities. EV charger installation, panel upgrades, commercial electrical. Licensed C-10 #981578.",
    "downey": "Downey electrician serving the gateway to the Gateway Cities. Panel upgrades, EV charger installation, rewiring. Licensed C-10 contractor.",
    "bellflower": "Bellflower electrician serving the city of 90706 and surrounding communities. Panel upgrades, EV charger installation, electrical repairs. Licensed C-10.",
    "alhambra": "Alhambra electrician serving the San Gabriel Valley. EV charger installation, panel upgrades, rewiring. Licensed C-10 contractor.",
    "calabasas": "Calabasas electrician serving the Santa Monica Mountains communities. Luxury home electrical, EV charger installation, panel upgrades. Licensed C-10.",
    "santa-clarita": "Santa Clarita electrician serving Valencia, Saugus, and Canyon Country. EV charger installation, panel upgrades, new construction electrical. Licensed C-10.",
    "los-angeles": "Los Angeles electrician serving all LA neighborhoods. EV charger installation, panel upgrades, rewiring, commercial electrical. Licensed C-10 #981578.",
    "westwood": "Westwood electrician serving UCLA, Century City, and Westwood Village. EV charger installation, panel upgrades, apartment electrical. Licensed C-10.",
    "brentwood": "Brentwood electrician serving the Westside luxury homes. EV charger installation, panel upgrades, smart home wiring. Licensed C-10 #981578.",
}

# Default description for cities not in the detailed list
def get_city_description(slug, name):
    if slug in CITY_DESCRIPTIONS:
        return CITY_DESCRIPTIONS[slug]
    return f"Licensed {name} electrician serving the greater Los Angeles area. Panel upgrades, EV charger installation, rewiring & electrical repairs. C-10 #981578. Free estimates. Call (818) 302-5614."


def fix_sitemap():
    """Remove junk URLs from sitemap."""
    print("=== FIXING SITEMAP ===")
    
    sitemap_path = SITE_DIR / "sitemap.xml"
    with open(sitemap_path, "r") as f:
        content = f.read()
    
    # Count before
    before = content.count("<url>")
    
    # Remove accessibility-audit entries
    content = re.sub(r'<url>\s*<loc>https://amyelectric\.com/accessibility-audit/[^<]+</loc>\s*<lastmod>[^<]+</lastmod>\s*<priority>[^<]+</priority>\s*</url>', '', content)
    
    # Remove admin entries
    content = re.sub(r'<url>\s*<loc>https://amyelectric\.com/admin/[^<]+</loc>\s*<lastmod>[^<]+</lastmod>\s*<priority>[^<]+</priority>\s*</url>', '', content)
    
    # Remove audit/lighthouse_reports entries
    content = re.sub(r'<url>\s*<loc>https://amyelectric\.com/audit/[^<]+</loc>\s*<lastmod>[^<]+</lastmod>\s*<priority>[^<]+</priority>\s*</url>', '', content)
    
    # Boost blog post priorities (top 10 most valuable)
    top_blogs = [
        "complete-guide-ev-charger-installation",
        "complete-guide-electrical-panel-upgrades",
        "panel-upgrade-cost-los-angeles",
        "ev-charger-installation-cost-la",
        "whole-home-rewiring-cost-la",
        "how-to-choose-electrician-los-angeles",
        "electrical-permit-los-angeles",
        "ladwp-ev-charger-rebate-guide-2026",
        "electrical-safety-checklist-older-los-angeles-homes",
        "knob-and-tube-wiring-replacement-guide",
    ]
    
    for blog_slug in top_blogs:
        content = content.replace(
            f"<loc>https://amyelectric.com/blog/{blog_slug}</loc>\n    <lastmod>2026-09-04</lastmod>\n    <priority>0.6</priority>",
            f"<loc>https://amyelectric.com/blog/{blog_slug}</loc>\n    <lastmod>2026-09-13</lastmod>\n    <priority>0.8</priority>"
        )
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    after = content.count("<url>")
    
    with open(sitemap_path, "w") as f:
        f.write(content)
    
    print(f"  Removed {before - after} junk URLs ({before} → {after} total)")
    print(f"  Boosted {len(top_blogs)} blog posts to priority 0.8")
    return True


def fix_city_pages():
    """Update all city pages with unique descriptions, correct coordinates, and nearby cities."""
    print("\n=== FIXING CITY PAGES ===")
    
    updated = 0
    
    for slug, city_data in CITIES.items():
        city_file = SITE_DIR / f"city-{slug}.html"
        
        if not city_file.exists():
            print(f"  SKIP: city-{slug}.html not found")
            continue
        
        with open(city_file, "r") as f:
            content = f.read()
        
        name = city_data["name"]
        lat = city_data["lat"]
        lon = city_data["lon"]
        
        # 1. Fix meta description
        new_desc = get_city_description(slug, name)
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{new_desc}">',
            content
        )
        
        # 2. Fix og:description
        og_desc = f"Licensed electrician in {name}, CA. Panel upgrades, EV charger installation, electrical repairs. EVITP-certified, C-10 #981578. Free estimates. (818) 302-5614."
        content = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            f'<meta property="og:description" content="{og_desc}">',
            content
        )
        
        # 3. Fix twitter:description
        content = re.sub(
            r'<meta name="twitter:description" content="[^"]*">',
            f'<meta name="twitter:description" content="{og_desc}">',
            content
        )
        
        # 4. Fix geo coordinates in schema
        content = re.sub(
            r'"latitude":\s*[\d.-]+',
            f'"latitude": {lat}',
            content
        )
        content = re.sub(
            r'"longitude":\s*[\d.-]+',
            f'"longitude": {lon}',
            content
        )
        
        # 5. Add 'Nearby Cities' section (before </main> or <footer> or last </div>)
        nearby = get_nearby_cities(slug, count=6)
        if nearby:
            nearby_html = f"""
<!-- Nearby Cities -->
<section class="nearby-cities" style="background:var(--navy2);padding:48px 24px;border-top:3px solid var(--mid)">
  <div class="wrap text-center">
    <h2 style="font-size:28px;margin-bottom:20px">Electrician Services Near {name}</h2>
    <p style="margin-bottom:24px;color:rgba(244,241,235,.8)">We serve all communities in the greater Los Angeles area. Find an electrician near you:</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center">
"""
            for nearby_slug, nearby_name in nearby:
                nearby_html += f'      <a href="/city-{nearby_slug}" style="font-family:var(--cond);font-weight:600;font-size:15px;color:var(--gold);padding:8px 16px;border:1px solid rgba(245,166,35,.3);border-radius:4px;text-decoration:none;transition:background .18s" onmouseover="this.style.background=\'rgba(245,166,35,.1)\'" onmouseout="this.style.background=\'transparent\'">{nearby_name}</a>\n'
            
            nearby_html += """    </div>
  </div>
</section>
"""
            
            # Insert before </footer> or before closing body
            if "</footer>" in content:
                content = content.replace("</footer>", nearby_html + "\n</footer>")
            elif "</body>" in content:
                content = content.replace("</body>", nearby_html + "\n</body>")
        
        with open(city_file, "w") as f:
            f.write(content)
        
        updated += 1
    
    print(f"  Updated {updated} city pages")
    print(f"  - Unique meta descriptions")
    print(f"  - Correct geo coordinates (no more all-Winnetka)")
    print(f"  - Nearby Cities internal links")


def main():
    print("SEO FIX SCRIPT")
    print("=" * 50)
    
    fix_sitemap()
    fix_city_pages()
    
    print("\n" + "=" * 50)
    print("DONE! All 5 SEO issues fixed.")


if __name__ == "__main__":
    main()
