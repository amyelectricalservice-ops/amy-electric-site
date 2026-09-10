#!/usr/bin/env python3
"""Generate city pages for all cities within 25 miles of Winnetka 91306."""

import os
import re

# Reference template (city-burbank.html structure)
TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">


<title>Electrician in {city_name}, {state_abbr} | Panel Upgrades | AMY Electric</title>
<meta name="description" content="Licensed {city_name} electrician. Panel upgrades, EV charger installation, rewiring & electrical repairs. C-10 #981578. Free estimates. Call (818) 302-5614.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://amyelectric.com/city-{slug}">
<!-- Open Graph -->
<meta property="og:title" content="Electrician in {city_name}, {state_abbr} | Panel Upgrades, EV Chargers &amp; Repairs | AMY Electric">
<meta property="og:description" content="Licensed electrician in {city_name}, {state_abbr}. Panel upgrades, EV charger installation, electrical repairs. EVITP-certified, C-10 #981578. Free estimates. (818) 302-5614.">
<meta property="og:url" content="https://amyelectric.com/city-{slug}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://amyelectric.com/img/hero-electrician.jpg">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:site_name" content="AMY Electric">
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Electrician in {city_name}, {state_abbr} | Panel Upgrades, EV Chargers &amp; Repairs | AMY Electric">
<meta name="twitter:description" content="Licensed electrician in {city_name}, {state_abbr}. Panel upgrades, EV charger installation, electrical repairs. EVITP-certified, C-10 #981578. Free estimates. (818) 302-5614.">
<meta name="twitter:image" content="https://amyelectric.com/img/hero-electrician.jpg">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preload" as="font" href="fonts/BarlowCondensed-600.woff2" crossorigin>
<link rel="preload" as="font" href="fonts/BarlowCondensed-700.woff2" crossorigin>
<link rel="preload" as="font" href="fonts/BarlowCondensed-800.woff2" crossorigin>
<link rel="preload" as="font" href="fonts/SourceSerif4-400.woff2" crossorigin>
<link rel="preload" as="font" href="fonts/SourceSerif4-400italic.woff2" crossorigin>
<style>*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0b1628;--navy2:#122040;--gold:#f5a623;--gold2:#e8951a;--white:#f4f1eb;--gray:#98a6b8;--mid:#1e3055;--accent:#3dd6f5;--radius:4px;--max:1140px;--serif:"Source Serif 4",Georgia,serif;--cond:"Barlow Condensed","Arial Narrow",sans-serif;--shadow:0 4px 24px rgba(0,0,0,.45)}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--serif);background:var(--navy);color:var(--white);font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}}
a{{color:var(--gold);text-decoration:none}}
img{{max-width:100%;display:block}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 24px}}
.text-center{{text-align:center}}
.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}}
.skip-link{{position:absolute;top:-100%;left:16px;background:var(--gold);color:var(--navy);padding:12px 24px;border-radius:0 0 var(--radius) var(--radius);font-family:var(--cond);font-weight:700;z-index:9999;text-decoration:none}}
.skip-link:focus{{top:0}}
:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}}}
.topbar{{background:var(--gold);color:var(--navy);font-family:var(--cond);font-size:14px;font-weight:700;letter-spacing:.04em;padding:7px 24px;display:flex;justify-content:space-between;align-items:center}}
.topbar a{{color:var(--navy)}}
header{{background:var(--navy2);border-bottom:3px solid var(--mid);position:sticky;top:0;z-index:100;box-shadow:0 2px 16px rgba(0,0,0,.5)}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;max-width:var(--max);margin:0 auto}}
.logo{{display:flex;align-items:center;gap:12px;text-decoration:none}}
.logo-mark{{width:44px;height:44px;background:var(--gold);color:var(--navy);font-family:var(--cond);font-weight:800;font-size:20px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius);flex-shrink:0}}
.logo-text{{font-family:var(--cond)}}
.logo-name{{font-size:22px;font-weight:800;color:var(--white);letter-spacing:.02em;display:block}}
.logo-sub{{font-size:11px;color:var(--gray);letter-spacing:.06em;text-transform:uppercase;display:block}}
nav{{display:flex;align-items:center;gap:4px;flex-wrap:wrap}}
nav a{{font-family:var(--cond);font-weight:600;font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--gray);padding:8px 12px;border-radius:var(--radius);transition:color .18s,background .18s;text-decoration:none}}
nav a:hover,nav a.active{{color:var(--gold);background:rgba(245,166,35,.1)}}
.nav-cta{{background:var(--gold)!important;color:var(--navy)!important;padding:8px 16px!important;margin-left:8px}}
.hamburger{{display:none;background:none;border:none;cursor:pointer;padding:8px}}
.hamburger span{{display:block;width:24px;height:24px;background:var(--white);margin:5px 0;transition:.3s}}
.btn{{display:inline-block;font-family:var(--cond);font-weight:700;font-size:17px;letter-spacing:.05em;text-transform:uppercase;padding:14px 28px;border-radius:var(--radius);border:none;cursor:pointer;transition:background .18s,transform .12s,box-shadow .18s;text-decoration:none}}
.btn-gold{{background:var(--gold);color:var(--navy);box-shadow:0 4px 16px rgba(245,166,35,.35)}}
.btn-outline{{background:transparent;color:var(--white);border:2px solid rgba(255,255,255,.4)}}
.hero{{background:linear-gradient(135deg,var(--navy2) 0%,#0d1e3a 60%,#091420 100%);padding:80px 24px 72px;position:relative;overflow:hidden}}
.hero-inner{{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}}
.hero-eyebrow{{font-family:var(--cond);font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:16px}}
.hero h1{{font-family:var(--cond);font-size:clamp(36px,5vw,64px);font-weight:800;line-height:1.05;color:var(--white);margin-bottom:20px}}
.hero h1 em{{color:var(--gold);font-style:normal}}
.hero-desc{{font-size:18px;color:rgba(244,241,235,.8);margin-bottom:32px;max-width:500px}}
.hero-badges{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:32px}}
.badge{{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:5px 14px;font-family:var(--cond);font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--white)}}
.badge .dot{{width:7px;height:7px;background:#4cdb7a;border-radius:50%}}
.hero-ctas{{display:flex;gap:14px;flex-wrap:wrap}}
.cta-band{{background:var(--gold);padding:56px 24px;text-align:center}}
.cta-band h2{{color:var(--navy);font-size:38px;margin-bottom:10px}}
.cta-band p{{color:var(--navy);opacity:.8;margin-bottom:28px}}
.cta-band .btn-navy{{background:var(--navy);color:var(--white)}}
.section-label{{font-family:var(--cond);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}}
h2{{font-family:var(--cond);font-weight:800;font-size:clamp(28px,4vw,46px);line-height:1.1;margin-bottom:16px;color:var(--white)}}
.page-hero{{background:linear-gradient(135deg,var(--navy2) 0%,#091420 100%);padding:56px 24px 48px;border-bottom:3px solid var(--mid)}}
.breadcrumb{{font-family:var(--cond);font-size:13px;color:var(--gray);margin-bottom:14px}}
.breadcrumb a{{color:var(--gray)}}
.page-hero h1{{font-family:var(--cond);font-weight:800;font-size:clamp(32px,5vw,56px);line-height:1.05;margin-bottom:16px;color:var(--white)}}
.page-hero p{{font-size:18px;color:rgba(244,241,235,.8);max-width:620px;margin-bottom:28px}}
@media(max-width:900px){{.hero-inner{{grid-template-columns:1fr}}}}
@media(max-width:680px){{header{{position:relative}}.header-inner{{flex-wrap:wrap;gap:12px}}nav{{display:none;width:100%;flex-direction:column;align-items:flex-start;padding-bottom:12px}}nav.open{{display:flex}}nav a{{width:100%}}.hamburger{{display:block}}}}
.sticky-bar{{position:fixed;bottom:0;left:0;right:0;display:flex;z-index:9999;box-shadow:0 -2px 10px rgba(0,0,0,.2);background:var(--gold)}}
.sticky-btn{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:8px 4px;min-height:60px;color:var(--navy);text-decoration:none;font-family:var(--cond);font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.04em;border-right:1px solid rgba(11,22,40,.15)}}
.sticky-estimate{{background:var(--navy);color:var(--gold)}}
@media(min-width:768px){{.sticky-bar{{display:none}}}}
@media(max-width:767px){{body{{padding-bottom:68px}}}}</style>
<link rel="preload" as="style" href="css/style.min.css" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="preload" as="style" href="css/style.min.css">
<link rel="stylesheet" href="css/style.min.css"></noscript>
<link rel="alternate" type="text/markdown" href="/llms.txt">"""

TEMPLATE_SCHEMA_LOCALBUSINESS = """
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://amyelectric.com/city-{slug}",
  "name": "AMY Electric",
  "image": "https://amyelectric.com/img/hero-electrician.jpg",
  "url": "https://amyelectric.com/city-{slug}",
  "telephone": "+1-818-302-5614",
  "email": "info@amyelectric.com",
  "description": "Licensed C-10 electrical contractor serving {city_name}, {state_abbr}. EV charger installation, panel upgrades, rewiring, and electrical repairs.",
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
  "foundingDate": "2012",
  "openingHoursSpecification": [
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:00",
      "closes": "17:00",
      "description": "Office hours"
    }},
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "14:00",
      "description": "Office hours"
    }},
    {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "00:00",
      "closes": "23:59",
      "description": "24/7 emergency service dispatch"
    }}
  ],
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "87",
    "bestRating": "5",
    "worstRating": "1"
  }},
  "hasCredential": [
    {{
      "@type": "EducationalOccupationalCredential",
      "name": "C-10 Electrical Contractor License #981578"
    }},
    {{
      "@type": "EducationalOccupationalCredential",
      "name": "EVITP Certification #4051604"
    }}
  ],
  "priceRange": "$$",
  "sameAs": [
    "https://www.yelp.com/biz/amy-electric-los-angeles",
    "https://g.page/r/CVdK9ZAvNBrZEAI/review",
    "https://maps.app.goo.gl/WTNSkHRUgULPBHpc9",
    "https://www.facebook.com/people/Amy-Electric/100063766463600/"
  ]
}}
</script>"""

TEMPLATE_SCHEMA_FAQ = """
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Do you serve {city_name} for same-day repairs?","acceptedAnswer":{{"@type":"Answer","text":"Yes — we provide 24/7 emergency dispatch for urgent electrical issues in {city_name}. Call (818) 302-5614 anytime, day or night. We prioritize emergencies including power outages affecting only your home, sparking or smoking panels, exposed wires, and any situation involving water near electricity. Our electricians carry diagnostic equipment and common replacement parts to handle most emergencies on the first visit. When availability allows, we dispatch same-day for non-emergency repairs as well."}}}},{{"@type":"Question","name":"Who handles permits for electrical work in {city_name}?","acceptedAnswer":{{"@type":"Answer","text":"We handle all permitting and inspections as part of every installation in {city_name}. We manage the entire process: permit applications, plan review submissions, utility coordination for service upgrades, scheduling inspections, and obtaining the final Certificate of Completion. Permitting ensures code compliance and protects your insurance."}}}},{{"@type":"Question","name":"Do you install EV chargers in {city_name}?","acceptedAnswer":{{"@type":"Answer","text":"Yes — we regularly install Level 2 EV chargers in {city_name} for Tesla, Rivian, ChargePoint, and all other EV brands. EVITP-certified, permits handled, free estimates."}}}},{{"@type":"Question","name":"Are you licensed and insured to work in {city_name}?","acceptedAnswer":{{"@type":"Answer","text":"Yes — AMY Electric is a licensed California C-10 electrical contractor (#981578) and EVITP-certified (#4051604). We carry full general liability insurance and workers' compensation insurance. Our license is active and in good standing with the CSLB, and we pull all required permits for every job in {city_name}. You can verify our license anytime at the California Contractors State License Board website."}}}},{{"@type":"Question","name":"Do you offer free estimates for electrical work in {city_name}?","acceptedAnswer":{{"@type":"Answer","text":"Yes — we provide free, no-obligation estimates for all electrical work in {city_name}. Whether you need a panel upgrade, EV charger installation, home rewiring, or commercial electrical service, we'll come out, assess the job, and provide a detailed written estimate. Call (818) 302-5614 or use our online form to schedule yours."}}}}]}}</script>"""

TEMPLATE_SCHEMA_BREADCRUMB = """
<script type="application/ld+json">{{"https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://amyelectric.com/"}}, {{"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://amyelectric.com/city-los-angeles"}}, {{"@type": "ListItem", "position": 3, "name": "{city_name}", "item": "https://amyelectric.com/city-{slug}"}}]}}</script>"""

TEMPLATE_SCHEMA_ELECTRICIAN = """
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Electrician","@id":"https://amyelectric.com/city-{slug}","name":"AMY Electric","image":"https://amyelectric.com/img/hero-electrician.jpg","url":"https://amyelectric.com/city-{slug}","telephone":"+1-818-302-5614","email":"info@amyelectric.com","description":"Licensed C-10 electrical contractor serving {city_name}, {state_abbr}. EV charger installation, panel upgrades, rewiring, and electrical repairs.","address":{{"streetAddress":"20628 Londelius St","addressLocality":"Winnetka","addressRegion":"CA","postalCode":"91306","addressCountry":"US"}},"geo":{{"latitude":34.22281,"longitude":-118.58241}},"foundingDate":"2012","founder":{{"@type":"Person","name":"AMY Electric Master Electrician","jobTitle":"Lead Master Electrician & Founder","description":"California C-10 Licensed Master Electrician with 15+ years experience in commercial & residential electrical engineering, EVITP certified.","worksFor":{{"@type":"Organization","name":"AMY Electric"}},"hasCredential":[{{"@type":"EducationalOccupationalCredential","name":"California C-10 Electrical Contractor License #981578","url":"https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578"}},{{"@type":"EducationalOccupationalCredential","name":"EVITP Certification #4051604"}}],"url":"https://amyelectric.com"}},"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"17:00","description":"Office hours"}},{{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"08:00","closes":"14:00","description":"Office hours"}}],"aggregateRating":{{"ratingValue":"4.9","reviewCount":"87","bestRating":"5","worstRating":"1"}},"hasCredential":[{{"name":"C-10 Electrical Contractor License #981578"}},{{"name":"EVITP Certification #4051604"}}],"priceRange":"$$","sameAs":["https://www.yelp.com/biz/amy-electric-los-angeles","https://g.page/r/CVdK9ZAvNBrZEAI/review","https://maps.app.goo.gl/WTNSkHRUgULPBHpc9"],"areaServed":{{"@type":"AdministrativeArea","name":"{city_name}, {state_abbr}"}}}}</script>"""

TEMPLATE_BODY_HEADER = """
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>

<div class="topbar">
  <span>📍 Los Angeles, CA &nbsp;·&nbsp; C-10 #981578 &nbsp;·&nbsp; EVITP #4051604</span>
  <a href="tel:18183025614">☎ (818) 302-5614</a>
</div>
<header><div class="header-inner">
  <a href="index" class="logo"><div class="logo-mark">AE</div><div class="logo-text"><span class="logo-name">AMY Electric</span><span class="logo-sub">Los Angeles Electricians</span></div></a>
  <button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>
  <nav>
      <a href="/services">Services</a>
    <a href="index">Home</a>
    <a href="ev-charger-installation">EV Chargers</a>
    <a href="panel-upgrade">Panel Upgrades</a>
    <a href="electrical-repair">Repairs</a>
    <a href="commercial-electrical">Commercial</a>
    <a href="lighting-installation">Lighting</a>
      <a href="tesla-charger-installation">Tesla Charger</a>
      <a href="whole-home-rewiring">Rewiring</a>
      <a href="surge-protection">Surge Protection</a>
      <a href="testimonials">Reviews</a>
      <a href="gallery">Gallery</a>
    <a href="city-los-angeles" class="active">Service Areas</a>
    <a href="tel:18183025614" class="nav-cta">Call Now</a>
  </nav>
</div></header>
<main id="main-content">

<div class="page-hero"><div class="wrap">
  <div class="breadcrumb"><a href="index">Home</a><span>›</span><a href="city-los-angeles">Service Areas</a><span>›</span> {city_name}</div>
  <h1>Electrician in<br><em>{city_name}, {state_abbr}</em></h1>

<div id="quick-answer" class="quick-answer">
  <p><strong>At a Glance:</strong> AMY Electric provides licensed C-10 electrical services throughout {city_name}, including EV charger installation, panel upgrades, rewiring, and 24/7 emergency repairs. Licensed #981578. Call (818) 302-5614 for a free estimate.</p>
</div>
  <p>Licensed, insured electricians serving {city_name} and surrounding communities. Panel upgrades, EV charger installation, repairs, and commercial electrical. Free estimates.</p>
  <div class="ctas">
    <a href="tel:18183025614" class="btn btn-gold">☎ Call (818) 302-5614</a>
    <a href="index#estimator" class="btn btn-outline">Free Estimate</a>
          <a href="index#estimator" class="btn btn-outline" style="border-color:var(--gold);color:var(--gold);">📅 Book Online</a>
  </div>
</div></div>

<div class="trust-bar"><div class="trust-bar-inner">
  <div class="trust-item"><span class="trust-icon">📍</span> Serving {city_name} &amp; Surrounding Areas</div>
  <div class="trust-item"><span class="trust-icon">🏅</span> C-10 Licensed &amp; Insured</div>
  <div class="trust-item"><span class="trust-icon">⚡</span> EVITP-Certified #4051604</div>
  <div class="trust-item"><span class="trust-icon">💰</span> Financing Available</div>
  <div class="trust-item"><span class="trust-icon">📋</span> All Permits Handled</div>
</div></div>"""

TEMPLATE_SERVICES_SECTION = """
<section class="section-pad"><div class="wrap">
  <div class="section-label">Local Electrical Services</div>
  <h2>Electrical Services in {city_name}</h2>
  <p><a href="service-areas">Explore all AMY Electric service areas</a> and find the right local electrical service for your project.</p>
  <p class="max-w-640">{local_intro}</p>

  <div class="card-grid mt-lg">
    <a href="ev-charger-installation" class="card no-underline">
      <div class="card-icon">🔌</div>
      <h3>EV Charger Installation</h3>
      <p>Level 2 EV charger installation for Tesla, Rivian, ChargePoint, and all EV brands. EVITP-certified, permits handled.</p>
      <span class="card-link">Learn More</span>
    </a>
    <a href="panel-upgrade" class="card no-underline">
      <div class="card-icon">🔧</div>
      <h3>200A Panel Upgrades</h3>
      <p>Service upgrades for {city_name} homes and businesses. LADWP-coordinated, permits included.</p>
      <span class="card-link">Learn More</span>
    </a>
    <a href="electrical-repair" class="card no-underline">
      <div class="card-icon">🛠️</div>
      <h3>Electrical Repairs</h3>
      <p>Fast, safe electrical diagnostics and repairs for {city_name} homes and businesses. Same-day service when available.</p>
      <span class="card-link">Learn More</span>
    </a>
    <a href="lighting-installation" class="card no-underline">
      <div class="card-icon">💡</div>
      <h3>Lighting Installation</h3>
      <p>Recessed lighting, outdoor security, landscape, and LED retrofits for {city_name} properties.</p>
      <span class="card-link">Learn More</span>
    </a>
    <a href="commercial-electrical" class="card no-underline">
      <div class="card-icon">🏢</div>
      <h3>Commercial Electrical</h3>
      <p>Tenant improvements, LED retrofits, panel upgrades, and EV fleet charging for {city_name} businesses.</p>
      <span class="card-link">Learn More</span>
    </a>
    <div class="card">
      <div class="card-icon">📍</div>
      <h3>Nearby Areas</h3>
      <p style="font-size:14px;">{nearby}</p>
    </div>
  </div>
</div></section>"""

TEMPLATE_LOCAL_KNOWLEDGE = """
<section class="section-pad"><div class="wrap">
<div class="section-label">Local Knowledge</div>
  <h2>{city_name} Neighborhoods &amp; Electrical Services</h2>
  <p style="max-width:680px;">{local_knowledge}</p>
</div></section>"""

TEMPLATE_FAQ = """
<section class="section-navy"><div class="wrap text-center">
  <div class="section-label">FAQ</div>
  <h2>Electrician in {city_name} — FAQ</h2>
  <div class="faq-list text-left">
    <details class="faq-item"><summary class="faq-q">Do you serve {city_name} for same-day repairs? <span class="faq-chevron">▾</span></summary><div class="faq-a">Yes — we provide 24/7 emergency dispatch for urgent electrical issues in {city_name}. Call (818) 302-5614 anytime, day or night. We prioritize emergencies including power outages affecting only your home, sparking or smoking panels, exposed wires, and any situation involving water near electricity. Our electricians carry diagnostic equipment and common replacement parts to handle most emergencies on the first visit. When availability allows, we dispatch same-day for non-emergency repairs as well.</div></details>
    <details class="faq-item"><summary class="faq-q">Who handles permits for electrical work in {city_name}? <span class="faq-chevron">▾</span></summary><div class="faq-a">We handle all permitting and inspections as part of every installation in {city_name}. We manage the entire process: permit applications, plan review submissions, utility coordination for service upgrades, scheduling inspections, and obtaining the final Certificate of Completion. Permitting ensures code compliance and protects your insurance.</div></details>
    <details class="faq-item"><summary class="faq-q">Do you install EV chargers in {city_name}? <span class="faq-chevron">▾</span></summary><div class="faq-a">Yes — we regularly install Level 2 EV chargers in {city_name} for Tesla, Rivian, ChargePoint, and all other EV brands. EVITP-certified, permits handled, free estimates.</div></details>
    <details class="faq-item"><summary class="faq-q">Are you licensed and insured to work in {city_name}? <span class="faq-chevron">▾</span></summary><div class="faq-a">Yes — AMY Electric is a licensed California C-10 electrical contractor (#981578) and EVITP-certified (#4051604). We carry full general liability insurance and workers' compensation insurance. Our license is active and in good standing with the CSLB, and we pull all required permits for every job in {city_name}.</div></details>
    <details class="faq-item"><summary class="faq-q">Do you offer free estimates for electrical work in {city_name}? <span class="faq-chevron">▾</span></summary><div class="faq-a">Yes — we provide free, no-obligation estimates for all electrical work in {city_name}. Whether you need a panel upgrade, EV charger installation, home rewiring, or commercial electrical service, we'll come out, assess the job, and provide a detailed written estimate. Call (818) 302-5614 or use our online form to schedule yours.</div></details>
  </div>
</div></section>"""

TEMPLATE_FOOTER = """
<footer class="site-footer"><div class="wrap"><p><strong>AMY Electric</strong> · Licensed C-10 electrical contractor #981578 · Greater Los Angeles</p><p><a href="tel:18183025614">(818) 302-5614</a> · <a href="mailto:info@amyelectric.com">info@amyelectric.com</a> · <a href="privacy-policy">Privacy</a></p></div></footer>
<div class="sticky-bar"><a class="sticky-btn" href="tel:18183025614">☎ Call</a><a class="sticky-btn sticky-estimate" href="index#estimate">Get Estimate</a></div>
<script src="js/site.min.js" defer></script>
</body>
</html>"""


# Cities to add: slug, display name, state, local intro, nearby, local knowledge
CITIES = [
    # San Fernando Valley - close
    {
        "slug": "northridge",
        "name": "Northridge",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Northridge. San Fernando Valley community near CSUN — we know the local permitting requirements and utility coordination process.",
        "nearby": "Winnetka, Reseda, Granada Hills, Chatsworth",
        "local_knowledge": "Northridge sits in the heart of the San Fernando Valley, home to Cal State Northridge and a mix of post-war ranch homes, newer apartment complexes along Nordhoff St, and commercial properties near the campus. The 1994 earthquake damaged many structures here, and some homes still have older wiring that predates modern seismic and electrical codes. We upgrade panels for EV charging, add dedicated circuits for home offices and student housing, and handle permits through LA Department of Building and Safety."
    },
    {
        "slug": "reseda",
        "name": "Reseda",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Reseda. San Fernando Valley neighborhood with diverse housing stock — we handle panel upgrades, EV chargers, and rewiring throughout the area.",
        "nearby": "Northridge, Tarzana, Encino, North Hills",
        "local_knowledge": "Reseda's housing ranges from 1950s tract homes to apartment buildings along Reseda Blvd and newer developments near the Orange Line corridor. Many properties still have original 100A panels that struggle to support modern loads like EV chargers, pool equipment, and central air. We work with LA Building & Safety on permits and evaluate service capacity before recommending panel upgrades for homes adding Level 2 charging."
    },
    {
        "slug": "tarzana",
        "name": "Tarzana",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Tarzana. San Fernando Valley community with hillside homes and established neighborhoods — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Encino, Reseda, Woodland Hills, Sherman Oaks",
        "local_knowledge": "Tarzana features a mix of flatland ranch homes and hillside properties with long driveway runs and detached garages. The area's older homes near Van Nuys Blvd often need panel upgrades to support EV charging alongside pool pumps and high-draw appliances. We plan circuit runs for hillside properties where the panel sits far from parking, and handle permits through LA Building & Safety."
    },
    {
        "slug": "canoga-park",
        "name": "Canoga Park",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Canoga Park. Western San Fernando Valley community with diverse housing — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Winnetka, West Hills, Chatsworth, Woodland Hills",
        "local_knowledge": "Canoga Park spans a wide area from the Topanga Corridor to the Westfield Topanga vicinity, with housing that ranges from post-war bungalows to newer apartment complexes. The neighborhood's mix of residential and commercial properties means varied electrical demands — from garage EV charging to dedicated circuits for small businesses along Sherman Way. We coordinate with LA Building & Safety on permits and plan circuits around the area's diverse building stock."
    },
    {
        "slug": "chatsworth",
        "name": "Chatsworth",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Chatsworth. Northwestern San Fernando Valley community with larger lots and hillside properties — we handle panel upgrades, EV chargers, and rewiring.",
        "nearby": "Northridge, Granada Hills, Porter Ranch, Canoga Park",
        "local_knowledge": "Chatsworth sits at the western edge of the San Fernando Valley with larger lots, equestrian properties, and hillside homes that have unique electrical needs. The area's properties often have longer circuit runs to detached garages and barns, requiring careful planning for EV charger installations. We handle permits for both LA city and county jurisdictions depending on the property location, and coordinate with LADWP for service upgrades."
    },
    {
        "slug": "porter-ranch",
        "name": "Porter Ranch",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Porter Ranch. Growing San Fernando Valley community with newer homes — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Chatsworth, Northridge, Granada Hills, North Hills",
        "local_knowledge": "Porter Ranch is one of the San Fernando Valley's newer master-planned communities, with homes built from the 1990s onward. While newer construction typically has adequate panels, many homeowners add EV chargers, solar systems, and smart-home equipment that push capacity. We evaluate service panels for expansion potential, install dedicated EV circuits, and handle permits through LA Building & Safety for modifications to newer homes."
    },
    {
        "slug": "granada-hills",
        "name": "Granada Hills",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Granada Hills. San Fernando Valley community with established neighborhoods — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Northridge, Chatsworth, Porter Ranch, North Hills",
        "local_knowledge": "Granada Hills features post-war ranch homes, hillside properties with views of the Valley, and the Granada Hills Charter High School area. Many homes along Occidental Ave and Zelzah Ave have original panels that need upgrading for modern electrical loads. We install Level 2 EV chargers, add circuits for home offices, and coordinate with LA Building & Safety on permits for panel upgrades and rewiring projects."
    },
    {
        "slug": "north-hills",
        "name": "North Hills",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in North Hills. Central San Fernando Valley community — we handle panel upgrades, EV chargers, and electrical repairs throughout the area.",
        "nearby": "Northridge, Granada Hills, Reseda, Van Nuys",
        "local_knowledge": "North Hills is a diverse San Fernando Valley neighborhood with a mix of apartment buildings, single-family homes, and commercial properties along Sepulveda Blvd. The area's older homes near the.original 'Mission Hills' section often have dated wiring that needs evaluation before adding EV chargers or high-draw appliances. We assess service capacity, handle permits through LA Building & Safety, and coordinate with LADWP for service upgrades."
    },
    {
        "slug": "west-hills",
        "name": "West Hills",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in West Hills. Western San Fernando Valley community with hillside properties — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Canoga Park, Chatsworth, Woodland Hills, Calabasas",
        "local_knowledge": "West Hills sits at the western edge of the San Fernando Valley where the flatlands meet the Santa Susana Mountains. The area features a mix of post-war ranch homes and hillside properties with larger lots and detached garages. EV charger installations often require longer circuit runs, and older homes may need panel upgrades to handle Level 2 charging alongside pool equipment and central air. We handle permits for both LA city and county jurisdictions."
    },
    # Actual cities
    {
        "slug": "san-fernando",
        "name": "San Fernando",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in San Fernando. Independent city in the San Fernando Valley — we handle panel upgrades, EV chargers, and electrical repairs with local permitting.",
        "nearby": "Sylmar, Pacoima, Mission Hills, North Hills",
        "local_knowledge": "San Fernando is an independent city surrounded by the City of Los Angeles, with its own building department and permitting process. The city features older homes from the 1920s-1960s, many with original wiring that predates modern electrical codes. We handle permits through the City of San Fernando Building Department, coordinate with LADWP for service upgrades, and specialize in rewiring older homes while preserving their character."
    },
    {
        "slug": "simi-valley",
        "name": "Simi Valley",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Simi Valley. Ventura County city northwest of the San Fernando Valley — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Moorpark, Thousand Oaks, Chatsworth, Porter Ranch",
        "local_knowledge": "Simi Valley is a Ventura County city about 11 miles northwest of Winnetka, with a mix of master-planned communities, older neighborhoods, and commercial areas along the 118 corridor. The city has its own building department and permitting process separate from LA. We handle permits through Simi Valley Building & Safety, coordinate with Southern California Edison for service upgrades, and install EV chargers throughout the community."
    },
    {
        "slug": "agoura-hills",
        "name": "Agoura Hills",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Agoura Hills. Ventura County city in the Santa Monica Mountains — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Calabasas, Westlake Village, Oak Park, Thousand Oaks",
        "local_knowledge": "Agoura Hills sits in the Santa Monica Mountains between Calabasas and Thousand Oaks, with properties ranging from hillside estates to equestrian ranches. The area's homes often have longer utility runs and larger lots that require careful planning for EV charger installations. We handle permits through the City of Agoura Hills, coordinate with Southern California Edison for service upgrades, and plan circuits for properties where the panel may be distant from parking areas."
    },
    {
        "slug": "thousand-oaks",
        "name": "Thousand Oaks",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Thousand Oaks. Ventura County city with established neighborhoods — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Westlake Village, Agoura Hills, Oak Park, Simi Valley",
        "local_knowledge": "Thousand Oaks is a large Ventura County city with diverse housing — from the original 1960s-1970s developments to newer master-planned communities. The city has its own building department and works with Southern California Edison for utility service. We handle permits through Thousand Oaks Building & Safety, install EV chargers for homes throughout the community, and evaluate panels for homes adding solar, pools, and high-draw appliances."
    },
    {
        "slug": "westlake-village",
        "name": "Westlake Village",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Westlake Village. Ventura County community straddling the LA/Ventura county line — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Thousand Oaks, Agoura Hills, Oak Park, Calabasas",
        "local_knowledge": "Westlake Village straddles the Los Angeles and Ventura county lines, which means different permitting jurisdictions depending on the property location. The community features upscale homes, many with private gated entries, long driveway runs, and hillside terrain. EV charger installations require careful planning for distance from the panel, and homes often need panel upgrades to support Level 2 charging alongside pool equipment and home automation systems."
    },
    {
        "slug": "west-hollywood",
        "name": "West Hollywood",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in West Hollywood. Independent city between Beverly Hills and Hollywood — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Hollywood, Beverly Hills, Century City, Los Angeles",
        "local_knowledge": "West Hollywood is an independent city with dense residential areas, apartment buildings, and commercial properties along the Sunset Strip and Santa Monica Blvd corridors. The city's mix of older buildings and newer developments creates varied electrical needs — from subpanel installs in converted apartments to EV charging in shared parking structures. We handle permits through West Hollywood Building & Safety and plan circuits around the area's dense, multi-tenant buildings."
    },
    {
        "slug": "manhattan-beach",
        "name": "Manhattan Beach",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Manhattan Beach. South Bay coastal city — we handle panel upgrades, EV chargers, and electrical repairs with local permitting.",
        "nearby": "Hermosa Beach, Redondo Beach, Torrance, El Segundo",
        "local_knowledge": "Manhattan Beach is a premium South Bay coastal community with compact lots, multi-story homes, and salt air that affects electrical equipment. Many properties have detached garages or parking structures that require careful planning for EV charger circuit runs. We handle permits through Manhattan Beach Building & Safety, evaluate panels for coastal corrosion, and install EV chargers for homes where the parking area may be below the main living level."
    },
    {
        "slug": "gardena",
        "name": "Gardena",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Gardena. South Bay city with diverse housing — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Torrance, Carson, Hawthorne, Compton",
        "local_knowledge": "Gardena is a diverse South Bay city with a mix of post-war tract homes, newer developments, and commercial properties along Artesia Blvd and Western Ave. The city's housing stock varies widely in age, and older homes often need panel upgrades to support modern electrical loads. We handle permits through Gardena Building & Safety, coordinate with Southern California Edison for service upgrades, and install EV chargers throughout the community."
    },
    {
        "slug": "hawthorne",
        "name": "Hawthorne",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Hawthorne. South Bay city near LAX — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Manhattan Beach, Gardena, Inglewood, El Segundo",
        "local_knowledge": "Hawthorne is a South Bay city adjacent to LAX with a mix of residential neighborhoods, commercial properties, and aerospace industry facilities. The city's housing ranges from 1940s-1950s bungalows to newer developments, and many homes need panel upgrades to support EV charging. We handle permits through Hawthorne Building & Safety, coordinate with Southern California Edison for service upgrades, and install EV chargers for homes and businesses throughout the area."
    },
    {
        "slug": "carson",
        "name": "Carson",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Carson. South Bay city with large lots and diverse housing — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Gardena, Torrance, Long Beach, Compton",
        "local_knowledge": "Carson is a South Bay city with larger lot sizes, a mix of single-family homes, and commercial/industrial properties. The city's homes often have spacious yards and detached garages that make EV charger installations straightforward, but older properties may need panel upgrades. We handle permits through Carson Building & Safety, coordinate with Southern California Edison for service upgrades, and plan circuits for homes adding EV chargers, pools, and high-draw appliances."
    },
    {
        "slug": "arcadia",
        "name": "Arcadia",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Arcadia. San Gabriel Valley city known for the Santa Anita area — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Monrovia, Temple City, Pasadena, Duarte",
        "local_knowledge": "Arcadia is a San Gabriel Valley city with upscale homes, many built from the 1960s onward with larger lots and mature landscaping. The area is popular with families and features homes with pools, spas, and high-draw HVAC systems that stress older electrical panels. We handle permits through Arcadia Building & Safety, coordinate with Southern California Edison for service upgrades, and install EV chargers for homes throughout the community."
    },
    {
        "slug": "covina",
        "name": "Covina",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Covina. San Gabriel Valley city with established neighborhoods — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "West Covina, Azusa, Glendora, Baldwin Park",
        "local_knowledge": "Covina is a San Gabriel Valley city with a mix of post-war tract homes, newer developments, and the historic Downtown Covina area. Many homes in the older neighborhoods have original panels that need upgrading for modern electrical loads. We handle permits through Covina Building & Safety, coordinate with Southern California Edison for service upgrades, and install Level 2 EV chargers for homes throughout the community."
    },
    {
        "slug": "west-covina",
        "name": "West Covina",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in West Covina. San Gabriel Valley city with large residential areas — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Covina, Baldwin Park, Walnut, Industry",
        "local_knowledge": "West Covina is a large San Gabriel Valley city with extensive residential neighborhoods, the Westfield West Covina shopping area, and commercial properties along the 10 and 605 corridors. The city's housing ranges from 1950s tract homes to newer developments, and many properties need panel upgrades to support EV charging. We handle permits through West Covina Building & Safety and coordinate with Southern California Edison for service upgrades."
    },
    {
        "slug": "el-monte",
        "name": "El Monte",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in El Monte. San Gabriel Valley city with diverse communities — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Temple City, Rosemead, Baldwin Park, West Covina",
        "local_knowledge": "El Monte is a San Gabriel Valley city with a diverse population and varied housing stock, from older bungalows to newer apartment complexes. The city's mix of residential and commercial properties means varied electrical demands, and many older homes need panel upgrades for modern loads. We handle permits through El Monte Building & Safety, coordinate with Southern California Edison for service upgrades, and install EV chargers throughout the community."
    },
    {
        "slug": "monrovia",
        "name": "Monrovia",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Monrovia. San Gabriel Valley city at the foothills of the San Gabriel Mountains — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Arcadia, Duarte, Azusa, Pasadena",
        "local_knowledge": "Monrovia sits at the base of the San Gabriel Mountains with a mix of historic downtown homes, hillside properties, and newer developments. The city features the Old Town Monrovia historic district and residential neighborhoods that range from 1920s bungalows to modern constructions. We handle permits through Monrovia Building & Safety, coordinate with Southern California Edison for service upgrades, and plan circuits for hillside properties with longer utility runs."
    },
    # Westside / other
    {
        "slug": "pacific-palisades",
        "name": "Pacific Palisades",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Pacific Palisades. Westside community near the coast — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Santa Monica, Brentwood, Malibu, Topanga",
        "local_knowledge": "Pacific Palisades is a Westside community between Santa Monica and Malibu with upscale homes, many on hillside lots with ocean views. The area's properties often have longer utility runs, detached guest houses, and high-end finishes that demand careful electrical planning. EV charger installations require evaluation of service capacity, and many homes need panel upgrades to support Level 2 charging alongside home automation and climate systems. We handle permits through LA Building & Safety."
    },
    {
        "slug": "century-city",
        "name": "Century City",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Century City. Westside business and residential district — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Westwood, Beverly Hills, West Hollywood, Sawtelle",
        "local_knowledge": "Century City is a Westside mixed-use district with high-rise condominiums, office towers, and the Westfield Century City shopping center. The area's residential buildings require coordination with property management for EV charger installations in structured parking, and commercial properties need dedicated circuits for office equipment and tenant improvements. We handle permits through LA Building & Safety and work with building managers on multi-unit electrical projects."
    },
    {
        "slug": "oak-park",
        "name": "Oak Park",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in Oak Park. Ventura County community near the LA county line — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Agoura Hills, Westlake Village, Thousand Oaks, Calabasas",
        "local_knowledge": "Oak Park is an unincorporated Ventura County community near the Los Angeles county line, with a mix of 1970s-1980s planned community homes and newer developments. The area's homes were built during a period of rapid growth and often have panels that are adequate for their original design but struggle with modern additions like EV chargers and solar systems. We handle permits through Ventura County Building & Safety and coordinate with Southern California Edison for service upgrades."
    },
    {
        "slug": "la-crescenta",
        "name": "La Crescenta",
        "state": "CA",
        "local_intro": "AMY Electric provides full-service residential and commercial electrical in La Crescenta. Unincorporated community at the base of the San Gabriel Mountains — we handle panel upgrades, EV chargers, and electrical repairs.",
        "nearby": "Glendale, Montrose, La Cañada Flintridge, Tujunga",
        "local_knowledge": "La Crescenta is an unincorporated community in the foothills of the San Gabriel Mountains, with a mix of mid-century homes, hillside properties, and the Montrose shopping area. The community's older homes near the village center often have panels that need upgrading, while hillside properties have unique challenges with longer utility runs and terrain. We handle permits through LA County Building & Safety and coordinate with Southern California Edison for service upgrades."
    },
]


def generate_city_page(city):
    """Generate a complete city page HTML file."""
    slug = city["slug"]
    name = city["name"]
    state = city["state"]
    nearby = city["nearby"]
    local_intro = city["local_intro"]
    local_knowledge = city["local_knowledge"]

    parts = []
    parts.append(TEMPLATE_HEAD.format(
        city_name=name, state_abbr=state, slug=slug
    ))
    parts.append(TEMPLATE_SCHEMA_LOCALBUSINESS.format(
        city_name=name, state_abbr=state, slug=slug
    ))
    parts.append(TEMPLATE_SCHEMA_FAQ.format(city_name=name))
    parts.append(TEMPLATE_SCHEMA_BREADCRUMB.format(city_name=name, slug=slug))
    parts.append(TEMPLATE_SCHEMA_ELECTRICIAN.format(
        city_name=name, state_abbr=state, slug=slug
    ))
    parts.append(TEMPLATE_BODY_HEADER.format(
        city_name=name, state_abbr=state, slug=slug
    ))
    parts.append(TEMPLATE_SERVICES_SECTION.format(
        city_name=name, local_intro=local_intro, nearby=nearby
    ))
    parts.append(TEMPLATE_LOCAL_KNOWLEDGE.format(
        city_name=name, local_knowledge=local_knowledge
    ))
    parts.append(TEMPLATE_FAQ.format(city_name=name))
    parts.append(TEMPLATE_FOOTER)

    return "".join(parts)


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..")

    # Check which cities already exist
    existing = set()
    for f in os.listdir(output_dir):
        if f.startswith("city-") and f.endswith(".html"):
            existing.add(f.replace("city-", "").replace(".html", ""))

    created = 0
    skipped = 0
    for city in CITIES:
        slug = city["slug"]
        if slug in existing:
            print(f"  SKIP (exists): {slug}")
            skipped += 1
            continue

        html = generate_city_page(city)
        filepath = os.path.join(output_dir, f"city-{slug}.html")
        with open(filepath, "w") as f:
            f.write(html)
        print(f"  CREATED: city-{slug}.html")
        created += 1

    print(f"\nDone: {created} created, {skipped} skipped (already exist)")


if __name__ == "__main__":
    main()
