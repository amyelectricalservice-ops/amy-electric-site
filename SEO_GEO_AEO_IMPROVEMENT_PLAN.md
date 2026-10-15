# Master Strategy & Action Plan: SEO, GEO, and AEO Optimization

**Site:** AMY Electric (amyelectric.com)
**Date:** October 2026
**Target Goal:** Elevate organic search performance, Google Local Pack rankings, and AI Engine visibility (ChatGPT, Claude, Perplexity, Google AI Overviews) from 81/100 to 95+/100.

---

## Executive Summary

AMY Electric currently holds a strong foundational baseline across Technical SEO, Schema, and AI Crawler management (overall baseline score: **81/100**; GEO Readiness: **92/100**). However, critical gaps in **Footer NAP & Privacy Compliance**, **Schema Completeness & Precision**, **Local Citation Presence / GBP Ownership**, and **SXO Contextual Lead Capture** limit maximum ranking potential and search-to-lead conversion rates.

This Master Strategy & Action Plan outlines a comprehensive 3-Pillar Strategy covering:
1. **On-Site Technical & Schema Excellence** (Executed directly in codebase)
2. **Generative Engine Optimization (GEO/AEO)** (AI readability, passage citability, and `llms.txt`)
3. **Local SEO & Off-Site Authority** (GBP, Citation Building, IndexNow, and DNS)

---

## Pillar 1: On-Site Technical & Schema Optimizations (Codebase)

### 1.1 Footer Standardization Across All 106 HTML Files
- **Issue:** Missing explicit Privacy Policy link and physical street address in HTML body footers (present only in schema JSON-LD).
- **Impact:** Weakens E-E-A-T (Trustworthiness) and local NAP signals for both Google and AI engines.
- **Action:** Standardize the footer HTML in all 106 static HTML files:
  - Add physical street address: `20628 Londelius St, Winnetka, CA 91306`
  - Add explicit footer navigation link: `<a href="/privacy-policy">Privacy Policy</a>`

### 1.2 Schema Markup Enhancements
- **Issue 1:** Deprecated `query-input` property in `SearchAction` schema.
- **Issue 2:** Low Geo-coordinates precision (3 decimal places = ~111m radius).
- **Issue 3:** Missing unique `@id` references on Service, Person, and Organization schemas.
- **Issue 4:** Inconsistent `areaServed` coverage between service pages (e.g., `panel-upgrade.html` vs `ev-charger-installation.html`).
- **Issue 5:** Missing `BreadcrumbList` on index/blog archive pages.
- **Action:**
  - Remove deprecated `query-input` and clean up `SearchAction` schema across all pages.
  - Update `GeoCoordinates` to 5 decimal places (`latitude: 34.22281, longitude: -118.58241` => 1.1m precision).
  - Add explicit `@id` anchors (`https://amyelectric.com/#organization`, `https://amyelectric.com/#person`) to establish entity relationship graphs.
  - Align `areaServed` to list all 16 key target cities consistently.
  - Add missing `BreadcrumbList` schemas to `blog/index.html` and `testimonials.html`.

### 1.3 SXO & Lead Capture Optimization
- **Issue:** Service pages redirect users to the homepage for quote submission, creating friction.
- **Action:** Ensure top service pages feature inline estimate request forms and immediate call options.

---

## Pillar 2: Generative Engine Optimization (GEO / AEO)

### 2.1 AI File Infrastructure (`llms.txt` & `rsl.json`)
- **Action:**
  - Update `llms.txt` with clear last-modified metadata, concise citable factual definitions (134-167 words), and comprehensive pricing/service details.
  - Ensure `rsl.json` (Robots Search License 1.0) is active and properly referenced.

### 2.2 Passage-Level Citability & E-E-A-T
- **Action:**
  - Structure H2 headings as natural-language questions ("How much does an EV charger cost in LA?", "Do I need a permit for a panel upgrade?").
  - Provide direct, concise, answer-first paragraphs followed by structured bullet points or tables.

---

## Pillar 3: Local SEO & Off-Site Authority Plan

### 3.1 Google Business Profile (GBP) & Local Citations
- **Action:**
  1. Claim and verify Google Business Profile for **AMY Electric** (`20628 Londelius St, Winnetka, CA 91306`).
  2. Complete primary category (`Electrical Contractor`) and secondary categories (`Electric Vehicle Charging Station Contractor`, `Lighting Contractor`).
  3. Upload 20+ high-resolution, geotagged project photos.
  4. Submit local citations with exact matching NAP (Name, Address, Phone):
     - Yelp (verify details match site)
     - Better Business Bureau (BBB)
     - Angie's List / Angi
     - HomeAdvisor
     - Nextdoor
     - Facebook Business Page

### 3.2 IndexNow & Technical Search Infrastructure
- **Action:**
  - Implement IndexNow key file (`/16076f14-4d06-4581-b281-38a7a89804ca.txt`) to notify Bing, Yandex, and Seznam instantly upon publishing or updating content.
  - Configure `www` DNS CNAME record in Cloudflare DNS dashboard to resolve `www.amyelectric.com` to `amyelectric.com`.

---

## Phased Implementation Roadmap

| Phase | Timeline | Scope | Key Deliverables |
|-------|----------|-------|------------------|
| **Phase 1** | Immediate | On-Site Codebase Fixes | Footer NAP & Privacy link across all 106 HTML pages, Schema cleanup, IndexNow key file deployment, `llms.txt` refresh. |
| **Phase 2** | Week 1-2 | Off-Site Setup | GBP Claim/Verification, DNS www record, local citation submissions (Yelp, BBB, Nextdoor). |
| **Phase 3** | Week 2-4 | Content & GEO Depth | Expanding city pages to 800+ words, adding HowTo schema, YouTube channel setup with video embeds. |
| **Phase 4** | Ongoing | Monitoring & Refinement | Monthly AI visibility re-tests using `SEO_AI_VISIBILITY_BASELINE.md` protocol, Search Console indexing checks. |
