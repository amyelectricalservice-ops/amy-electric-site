#!/usr/bin/env python3
"""
Blog Context & Lead Optimization Agent for AMY Electric.

Generates local LA context for blog posts, audits blog articles for lead-capture
conversion elements, injects high-converting CTA blocks & internal money-page links,
and produces high-intent blog topic briefs.

Usage:
  python3 scripts/blog-agent.py --context          # Display local LA business & regulatory context
  python3 scripts/blog-agent.py --audit            # Audit all blog articles for lead-gen elements
  python3 scripts/blog-agent.py --inject-ctas      # Inject high-converting lead CTAs into blog articles
  python3 scripts/blog-agent.py --brief "panel"    # Generate structured blog content brief for a topic
"""

import os, sys, glob, re, json

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(SITE_ROOT, 'blog')

BUSINESS_CONTEXT = {
    "name": "AMY Electric",
    "license": "C-10 License #981578",
    "certification": "EVITP #4051604 (Electric Vehicle Infrastructure Training Program)",
    "phone": "(818) 302-5614",
    "phone_raw": "+1-818-302-5614",
    "email": "info@amyelectric.com",
    "service_area": "Greater Los Angeles (San Fernando Valley, Westside, Downtown, Tri-Cities, South Bay)",
    "primary_utilities": ["LADWP (Los Angeles Department of Water and Power)", "SCE (Southern California Edison)"],
    "permitting_authorities": ["LADBS (Los Angeles Dept of Building and Safety)", "Burbank Water & Power", "Pasadena Water & Power"],
    "pricing_reference": {
        "panel_upgrade_200a": "$3,800 – $5,200 (includes permit, LADWP coordination, SDG/Siemens equipment)",
        "ev_charger_install": "$450 – $1,200 (Level 2 Wall Connector, dedicated 240V circuit)",
        "whole_home_rewire": "$8,000 – $18,000 (copper wiring, code-compliant grounding, drywall patching included)",
        "commercial_ti": "Custom quote (panel distribution, LED retrofits, Title 24 compliance)"
    },
    "money_pages": [
        {"keyword": "panel upgrade", "url": "/panel-upgrade-los-angeles"},
        {"keyword": "200 amp panel upgrade", "url": "/200-amp-panel-upgrade"},
        {"keyword": "ev charger installation", "url": "/ev-charger-installation-los-angeles"},
        {"keyword": "tesla charger installation", "url": "/tesla-charger-installation-los-angeles"},
        {"keyword": "whole home rewiring", "url": "/whole-home-rewiring-los-angeles"},
        {"keyword": "emergency electrician", "url": "/emergency-electrician-los-angeles"},
        {"keyword": "commercial electrical", "url": "/commercial-electrical-los-angeles"}
    ]
}

CTA_BLOCK_HTML = '''<section class="blog-lead-cta" style="margin: 40px 0; padding: 32px 24px; background: var(--navy2); border: 2px solid var(--gold); border-radius: var(--radius); text-align: center;">
  <h3 style="color: var(--gold); font-family: var(--cond); font-size: 24px; margin-bottom: 12px; text-transform: uppercase;">Need Professional Electrical Service in Los Angeles?</h3>
  <p style="color: var(--white); font-size: 16px; line-height: 1.6; max-width: 680px; margin: 0 auto 20px;">AMY Electric is a licensed C-10 contractor (License #981578, EVITP #4051604) offering upfront pricing, same-day repairs, and full LADWP permit handling across Greater LA.</p>
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px;">
    <a href="tel:18183025614" class="btn" style="background: var(--gold); color: var(--navy); padding: 12px 24px; font-weight: 700; text-decoration: none; border-radius: 4px; display: inline-flex; align-items: center; gap: 8px;">
      📞 Call (818) 302-5614
    </a>
    <a href="/get-quote" class="btn" style="background: transparent; color: var(--gold); border: 2px solid var(--gold); padding: 10px 24px; font-weight: 700; text-decoration: none; border-radius: 4px; display: inline-flex; align-items: center; gap: 8px;">
      ⚡ Request Free Online Estimate
    </a>
  </div>
</section>'''


def get_context():
    return json.dumps(BUSINESS_CONTEXT, indent=2)


def audit_blog_posts():
    files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
    report = []

    for fpath in files:
        fname = os.path.basename(fpath)
        if fname == 'index.html':
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        has_phone_cta = bool(re.search(r'tel:1?8183025614', html))
        has_quote_link = bool(re.search(r'href=[\'"]/?get-quote[\'"]', html) or re.search(r'index#estimator', html) or re.search(r'#estimate', html))
        has_lead_cta_block = 'class="blog-lead-cta"' in html or 'blog-lead-cta' in html
        has_faq_schema = 'FAQPage' in html
        has_internal_links = any(m['url'] in html or m['url'].lstrip('/') in html for m in BUSINESS_CONTEXT['money_pages'])

        score = sum([has_phone_cta, has_quote_link, has_lead_cta_block, has_faq_schema, has_internal_links])

        report.append({
            "file": fname,
            "score": f"{score}/5",
            "has_phone_cta": has_phone_cta,
            "has_quote_link": has_quote_link,
            "has_lead_cta_block": has_lead_cta_block,
            "has_faq_schema": has_faq_schema,
            "has_internal_links": has_internal_links
        })

    return report


def inject_lead_ctas():
    files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
    updated_count = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        if fname == 'index.html':
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        if 'class="blog-lead-cta"' in html:
            continue

        # Target insertion: before <section class="related-guides"> or before </main> or before </article>
        if '<section class="related-guides"' in html:
            new_html = html.replace('<section class="related-guides"', CTA_BLOCK_HTML + '\n<section class="related-guides"')
        elif '</main>' in html:
            new_html = html.replace('</main>', CTA_BLOCK_HTML + '\n</main>')
        elif '</article>' in html:
            new_html = html.replace('</article>', CTA_BLOCK_HTML + '\n</article>')
        else:
            continue

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        updated_count += 1

    return updated_count


def generate_brief(topic):
    brief = {
        "topic": topic,
        "target_audience": "Los Angeles homeowners, property managers, and business owners",
        "primary_keywords": [
            f"{topic} cost los angeles",
            f"best {topic} electrician los angeles",
            f"ladwp {topic} requirements",
            f"licensed {topic} contractor la"
        ],
        "conversion_elements": [
            "Phone CTA: Call (818) 302-5614 for immediate dispatch",
            "Online Estimate Trigger: /get-quote",
            "Trust Signals: C-10 #981578, EVITP #4051604, 100% Licensed & Insured",
            "Pricing Transparency: Exact itemized range ($3,800–$5,200 panel / $450–$1,200 EV)",
            "Local Authority: LADWP permit process & Title 24 compliance details"
        ],
        "suggested_faqs": [
            f"How much does {topic} cost in Los Angeles?",
            f"Do I need an LADWP permit for {topic}?",
            f"How long does {topic} take to complete?",
            "Why choose AMY Electric for electrical work in LA?"
        ]
    }
    return json.dumps(brief, indent=2)


def main():
    args = sys.argv[1:]
    if not args or '--context' in args:
        print("=== AMY ELECTRIC BLOG LOCAL CONTEXT ===")
        print(get_context())
    elif '--audit' in args:
        print("=== BLOG LEAD CONVERSION AUDIT ===")
        report = audit_blog_posts()
        print(f"{'File':<45} | {'Score':<6} | {'Phone':<5} | {'Quote':<5} | {'CTA Block':<9} | {'FAQ Schema':<10}")
        print("-" * 90)
        for item in report:
            print(f"{item['file']:<45} | {item['score']:<6} | {str(item['has_phone_cta']):<5} | {str(item['has_quote_link']):<5} | {str(item['has_lead_cta_block']):<9} | {str(item['has_faq_schema']):<10}")
    elif '--inject-ctas' in args:
        count = inject_lead_ctas()
        print(f"Injected lead CTA blocks into {count} blog articles.")
    elif '--brief' in args:
        idx = args.index('--brief')
        topic = args[idx+1] if idx + 1 < len(args) else "electrical panel upgrade"
        print(f"=== BLOG CONTENT BRIEF: {topic} ===")
        print(generate_brief(topic))
    else:
        print("Unknown flag. Use --context, --audit, --inject-ctas, or --brief <topic>")


if __name__ == '__main__':
    main()
