#!/usr/bin/env python3
"""Add real, visible FAQ sections to gallery.html and testimonials.html.

scripts/schema-tool.py hardcodes a FAQPage requirement for exactly these two
pages. Their previous FAQ blocks were fabricated (questions that appeared
nowhere in the body) and were removed, so the honest way to satisfy both CI and
Google's structured-data policy is to publish the questions on the page and let
the schema mirror them. Run sync-faq-schema.py afterwards to generate the JSON-LD.
"""

GALLERY = """<section class="section-navy"><div class="wrap text-center">
  <div class="section-label">FAQ</div>
  <h2>Questions About Our Electrical Project Photos</h2>
  <div class="faq-list text-left">
    <details class="faq-item"><summary class="faq-q">Can I see photos of your electrical work? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Yes. This gallery is built from our own project photography, not stock images. It covers panel upgrades, EV charger installations, whole-home rewiring, lighting work, subpanels, and repairs across Greater Los Angeles.</div></details>
    <details class="faq-item"><summary class="faq-q">Do you have examples of panel upgrades? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Yes. The gallery includes 100A-to-200A service upgrades, subpanel installations, and Federal Pacific and Zinsco panel replacements, so you can see the finished enclosure and the labelled circuits before you commit to a project.</div></details>
    <details class="faq-item"><summary class="faq-q">Can I see EV charger installation photos? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Yes. EV charger installations are documented, including Tesla Wall Connector and NEMA 14-50 outlet work. The photos show the conduit routing and the panel capacity that makes the install possible, which is usually the part homeowners want to check first.</div></details>
    <details class="faq-item"><summary class="faq-q">Are the photos from my part of Los Angeles? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">The gallery spans Greater Los Angeles, from the San Fernando Valley to Hollywood Hills and the Westside. Each photo is labelled with its project type and location area. If you want to see work from your specific city, call and we will tell you what is comparable.</div></details>
    <details class="faq-item"><summary class="faq-q">How current are these photos? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">They come from ongoing work and are added as projects complete. Panels, chargers, and lighting in recent LA homes are very similar to what most homeowners install today.</div></details>
    <details class="faq-item"><summary class="faq-q">Can I request a photo of a project like mine? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Call (818) 302-5614 and describe the work. We will tell you whether a comparable project exists in the gallery, and if it does not we will walk you through what your project involves instead.</div></details>
  </div>
</div></section>

"""

TESTIMONIALS = """<section class="section-navy"><div class="wrap text-center">
  <div class="section-label">FAQ</div>
  <h2>Questions About Our Customer Reviews</h2>
  <div class="faq-list text-left">
    <details class="faq-item"><summary class="faq-q">Where can I read your reviews? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">This page links straight to our Google Business Profile and our Yelp listing. We would rather you read third-party reviews in full, including the critical ones, than a curated selection on a marketing page.</div></details>
    <details class="faq-item"><summary class="faq-q">What should I check when hiring an electrician in Los Angeles? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Four things: a current C-10 licence you can verify with the state, insurance, who pulls the permit, and a written scope and estimate before any work starts. If a contractor cannot give you all four, that is worth asking about.</div></details>
    <details class="faq-item"><summary class="faq-q">How do I verify your licence is valid? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Look up licence C-10 #981578 with the California State Licensing Board. The CSLB record shows the licence class, status, and any disciplinary history. It is a public lookup and takes under a minute.</div></details>
    <details class="faq-item"><summary class="faq-q">Do you offer a written estimate before work starts? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Yes. We provide a free, no-obligation estimate before any work begins, so you know the scope and the cost before deciding. Call (818) 302-5614 or request one from the homepage form.</div></details>
    <details class="faq-item"><summary class="faq-q">What do reviews usually praise? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Customers most often mention arriving on time, protecting floors and finishes, clean workmanship, and explaining what was being done in plain language. Permit and inspection coordination comes up often on panel and charger work.</div></details>
    <details class="faq-item"><summary class="faq-q">What if a review mentions a problem? <span class="faq-chevron">&#9662;</span></summary><div class="faq-a">Call us directly and ask for the manager. We would rather resolve an issue with you directly than leave it sitting in a public review.</div></details>
  </div>
</div></section>

"""

for path, block in [("gallery.html", GALLERY), ("testimonials.html", TESTIMONIALS)]:
    doc = open(path, encoding="utf-8").read()
    if 'class="faq-list text-left"' in doc:
        print("  %-22s already has a FAQ section" % path)
        continue
    marker = '<section class="section-navy"><div class="wrap text-center">\n  <div class="section-label">Service Areas'
    i = doc.find(marker)
    if i == -1:
        print("  %-22s anchor not found" % path)
        continue
    open(path, "w", encoding="utf-8").write(doc[:i] + block + doc[i:])
    print("  %-22s +%d visible FAQ items" % (path, block.count("<details")))
