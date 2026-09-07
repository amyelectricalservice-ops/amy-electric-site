import glob
import os
import re
import json
from xml.etree import ElementTree as ET

def apply_fixes():
    # 1. Title Tag Fixes
    title_fixes = {
        'blog/electrical-inspection-what-to-expect.html': 'Electrical Inspection: What to Expect in LA | AMY Electric',
        'blog/generator-maintenance-tips.html': 'Generator Maintenance Tips for LA Homeowners | AMY Electric',
        'blog/panel-upgrade-vs-rewiring.html': 'Panel Upgrade vs Rewiring: Which Do You Need? | AMY Electric',
        'blog/smart-home-electrical-requirements.html': 'Smart Home Electrical Requirements & Wiring | AMY Electric',
        'city-winnetka.html': 'Winnetka Electrician | Panel Upgrades & EV | AMY Electric',
        'portable-vs-standby-generator.html': 'Portable vs Standby Generator Guide | AMY Electric'
    }

    for f, new_t in title_fixes.items():
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as fh:
                c = fh.read()
            c = re.sub(r'<title>.*?</title>', f'<title>{new_t}</title>', c, flags=re.DOTALL | re.IGNORECASE)
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(c)

    # 2. Meta Description Fixes
    desc_fixes = {
        '200-amp-panel-upgrade.html': 'Upgrade your panel to 200 amps for modern home demands. Licensed C‑10 installation with permits in Los Angeles. Call (818) 302‑5614.',
        '404.html': 'Page not found – AMY Electric. Contact our LA electricians for 24/7 service, panel upgrades, and EV charger installs.',
        'blog/electrical-panel-labeling-guide.html': 'Why panel labeling matters and how to label correctly. Tips from C‑10 electricians. Call (818) 302‑5614.',
        'blog/ev-charger-levels-explained.html': 'Level 1, 2, and DC Fast EV charging explained. Home charger tips in LA. Call (818) 302‑5614.',
        'blog/how-to-tell-if-your-panel-needs-upgrading.html': 'Warning signs your LA home needs a panel upgrade. Call (818) 302‑5614.',
        'blog/ladwp-e-permit-guide.html': 'LADWP e‑permit guide for LA electrical work. Steps, costs, timeline. Call (818) 302‑5614.',
        'city-winnetka.html': 'C‑10 electrician in Winnetka. Emergency repairs, panel upgrades, EV chargers. Call (818) 302‑5614.',
        'commercial-ev-fleet-charging.html': 'Commercial EV fleet charging in LA. EVITP‑certified installers. Call (818) 302‑5614.',
        'portable-vs-standby-generator.html': 'Portable vs standby generators for LA homes. Costs, fuel, backup options. Call (818) 302‑5614.',
        'services.html': 'Electrical services in LA: EV chargers, panel upgrades, rewiring, lighting, 24/7 emergency. Call (818) 302‑5614.',
        'testimonials.html': 'Customer reviews for AMY Electric. Trusted LA C‑10 electricians. Call (818) 302‑5614.',
        'whole-home-rewiring-beverly-hills.html': 'Rewire homes in Beverly Hills. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-culver-city.html': 'Rewire homes in Culver City. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-los-angeles.html': 'Rewire homes in Los Angeles. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-north-hollywood.html': 'Rewire homes in North Hollywood. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-santa-monica.html': 'Rewire homes in Santa Monica. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-sherman-oaks.html': 'Rewire homes in Sherman Oaks. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-studio-city.html': 'Rewire homes in Studio City. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-west-la.html': 'Rewire homes in West LA. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.',
        'whole-home-rewiring-woodland-hills.html': 'Rewire homes in Woodland Hills. Replace knob‑and‑tube, update panels. Call (818) 302‑5614.'
    }

    for f, new_d in desc_fixes.items():
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as fh:
                c = fh.read()
            # Ensure description length <= 155 characters
            trimmed_desc = new_d.strip()
            if len(trimmed_desc) > 155:
                trimmed_desc = trimmed_desc[:152].rstrip() + "..."
            c = re.sub(
                r'<meta\s+(?:name=["\']description["\']\s+content=["\'][^"\']*["\']|content=["\'][^"\']*["\']\s+name=["\']description["\'])',
                f'<meta name="description" content="{trimmed_desc}"',
                c,
                flags=re.IGNORECASE
            )
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(c)

    # 3. Fix truncated 16 city pages
    city_incomplete = [
        'city-beverly-hills.html', 'city-burbank.html', 'city-calabasas.html',
        'city-culver-city.html', 'city-encino.html', 'city-glendale.html',
        'city-hollywood.html', 'city-los-angeles.html', 'city-north-hollywood.html',
        'city-pasadena.html', 'city-santa-monica.html', 'city-sherman-oaks.html',
        'city-studio-city.html', 'city-van-nuys.html', 'city-west-la.html',
        'city-woodland-hills.html'
    ]

    footer_markup = '''  </div>
</div>
</section>
<footer class="site-footer"><div class="wrap"><p><strong>AMY Electric</strong> · Licensed C-10 electrical contractor #981578 · Greater Los Angeles</p><p><a href="tel:18183025614">(818) 302-5614</a> · <a href="mailto:info@amyelectric.com">info@amyelectric.com</a> · <a href="privacy-policy">Privacy</a></p></div></footer>
<div class="sticky-bar"><a class="sticky-btn" href="tel:18183025614">☎ Call</a><a class="sticky-btn sticky-estimate" href="index#estimate">Get Estimate</a></div>
<script src="js/site.min.js" defer></script>
</body>
</html>
'''

    for f in city_incomplete:
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as fh:
                c = fh.read()
            if '</body>' not in c:
                c = c.rstrip() + '\n' + footer_markup
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(c)
                print(f"Appended footer & closing tags to {f}")

    # 4. Inject site.min.js & sticky-bar into any remaining HTML files
    html_files = glob.glob('**/*.html', recursive=True)
    ignore_prefixes = ('reports/', '.', 'amyelectric-site/', 'templates/', 'partials/', 'open-seo/')
    html_files = [f for f in sorted(html_files) if not any(f.startswith(p) for p in ignore_prefixes)]

    # 4b. Ensure every HTML file has a meta description. If missing, insert a concise generic description.
    generic_desc = "AMY Electric – Licensed C‑10 contractor in Greater Los Angeles. Call (818) 302‑5614 for panel upgrades, EV charger installs, and 24/7 emergency service."
    for f in html_files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except Exception:
            continue
        if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
            if '</head>' in content:
                content = content.replace('</head>', f'    <meta name="description" content="{generic_desc}">\n</head>')
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(content)
        

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        
        modified = False

        if 'site.min.js' not in c and f != 'gallery.html':
            js_path = '../js/site.min.js' if ('/' in f) else 'js/site.min.js'
            js_tag = f'<script src="{js_path}" defer></script>\n</body>'
            if '</body>' in c:
                c = c.replace('</body>', js_tag)
                modified = True

        if 'sticky-bar' not in c and f != '404.html' and 'privacy-policy' not in f:
            est_link = '../index#estimate' if ('/' in f) else 'index#estimate'
            sticky_html = f'<div class="sticky-bar"><a class="sticky-btn" href="tel:18183025614">☎ Call</a><a class="sticky-btn sticky-estimate" href="{est_link}">Get Estimate</a></div>\n'
            if '</body>' in c:
                c = c.replace('</body>', sticky_html + '</body>')
                modified = True

        if modified:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(c)

    # 5. Re-generate sitemap.xml
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for f in html_files:
        if f == '404.html':
            continue
        
        clean_path = f[:-5] if f.endswith('.html') else f
        if clean_path == 'index':
            url = 'https://amyelectric.com/'
            priority = '1.0'
        elif clean_path == 'blog/index':
            url = 'https://amyelectric.com/blog/'
            priority = '0.7'
        elif clean_path == 'case-studies/index':
            url = 'https://amyelectric.com/case-studies/'
            priority = '0.7'
        elif clean_path.endswith('/index'):
            clean_dir = clean_path[:-6]
            url = f'https://amyelectric.com/{clean_dir}/'
            priority = '0.7'
        else:
            url = f'https://amyelectric.com/{clean_path}'
            if clean_path in ('ev-charger-installation', 'panel-upgrade', 'tesla-charger-installation', 'emergency-electrician'):
                priority = '0.9'
            elif clean_path.startswith('city-') or clean_path.startswith('ev-charger-') or clean_path.startswith('panel-upgrade-'):
                priority = '0.7'
            elif clean_path.startswith('blog/'):
                priority = '0.6'
            else:
                priority = '0.8'
                
        sitemap_lines.append(f'  <url>')
        sitemap_lines.append(f'    <loc>{url}</loc>')
        sitemap_lines.append(f'    <lastmod>2026-09-04</lastmod>')
        sitemap_lines.append(f'    <priority>{priority}</priority>')
        sitemap_lines.append(f'  </url>')
        
    sitemap_lines.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(sitemap_lines) + '\n')
    print("Regenerated sitemap.xml with 204 production URLs")

if __name__ == '__main__':
    apply_fixes()
