# ACTION-PLAN.md — AMY Electric SEO Priorities

**Generated:** July 24, 2026  
**Overall Score:** 91/100  
**Baseline:** 89/100 (Jul 23, 2026)

---

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## CRITICAL — Fix Immediately

*None identified.* The site has no critical issues blocking indexing or causing penalties.

---

## HIGH — Fix Within 1 Week

### H1. Replace `Electrician` schema with `LocalBusiness` (or `ElectricalContractor`)
**Impact:** Affects 130 schema blocks across 107+ pages  
**Effort:** Medium (batch script)  
**Why:** `Electrician` is not a recognized schema.org type. Google may ignore these schemas entirely, losing rich result eligibility.  
**Action:**
- Change `@type: "Electrician"` to `@type: "LocalBusiness"` with `subType: "ElectricalContractor"` (or use the proposed `ElectricalContractor` type if Google adds support)
- Update all 107 pages via batch script
- Validate with Google Rich Results Test

### H2. Reduce LCP below 2.5s target
**Impact:** Performance score capped at 82, LCP at 3.2s  
**Effort:** Medium  
**Why:** LCP is a Core Web Vitals ranking signal. Currently 0.7s above target.  
**Action:**
- Consider converting hero image to AVIF format (30-50% smaller than WebP)
- Preload the exact LCP element (hero image) with `fetchpriority="high"` (already done)
- Test with Cloudflare Image Resizing for automatic format negotiation
- Consider inlining critical CSS to reduce render-blocking resources

### H3. Add "Latest Articles" section to homepage
**Impact:** 26 of 33 blog posts orphaned from strongest internal link hub  
**Effort:** Low (30 min)  
**Why:** Internal links from high-authority pages (homepage) pass the most link equity. 79% of blog posts have no homepage link.  
**Action:**
- Add a "Latest Articles" or "Electrical Resources" section to `index.html`
- Link to all 33 blog posts (or at minimum the 26 orphaned ones)
- Use a grid layout with article title + brief description

### H4. Add Apple Maps and Bing Places sameAs profiles
**Impact:** Missing citation signals for AI crawlers and local SEO  
**Effort:** Low (requires manual profile claiming)  
**Why:** Apple Maps feeds Siri/Apple Intelligence; Bing Places feeds Bing/Copilot. Both are citation sources for AI search.  
**Action:**
- Claim Apple Maps business profile at mapsconnect.apple.com
- Claim Bing Places profile at bingplaces.com
- Add URLs to sameAs arrays in homepage schema (Electrician, Organization, WebSite)

---

## MEDIUM — Fix Within 1 Month

### M1. Add `WebSite` schema to all service and blog pages
**Impact:** 92 pages lack WebSite schema  
**Effort:** Low (batch script)  
**Why:** WebSite schema enables sitelinks search box in Google SERPs.  
**Action:**
- Add WebSite schema block to all service pages and blog posts
- Include `potentialAction: SearchAction`

### M2. Add `SpeakableSpecification` to 32 geo service pages
**Impact:** Voice assistants can't read these pages  
**Effort:** Low (batch script)  
**Why:** Speakable markup enables Google Assistant to read page content aloud.  
**Action:**
- Add SpeakableSpecification to all `ev-charger-installation-{city}.html` and `panel-upgrade-{city}.html` pages
- Target `.page-hero h1` and `.page-hero p` selectors

### M3. Remove deprecated `Expect-CT` header
**Impact:** ~40 bytes added to every response, no benefit  
**Effort:** Trivial (2 min)  
**Why:** Chrome removed Expect-CT enforcement in 2022. The header is purely informational and adds unnecessary bytes.  
**Action:**
- Remove `Expect-CT: max-age=86400, enforce` from `_headers`

### M4. Fix 3 blog redirect stubs
**Impact:** Low (noindex'd pages)  
**Effort:** Low  
**Why:** These pages have incomplete BlogPosting schemas (missing author, datePublished). While noindex'd, they could still appear in AI training data.  
**Action:**
- Either: complete the schemas to match other blog posts
- Or: remove the BlogPosting schema entirely (since they're redirects)

### M5. Add FAQPage schema to 3 blog posts
**Impact:** These posts lose FAQ rich results  
**Effort:** Low (5 min each)  
**Action:**
- Add FAQPage schema to `blog/how-to-choose-electrician-los-angeles.html`
- Add FAQPage schema to `blog/signs-you-need-electrical-panel-upgrade.html`
- Add FAQPage schema to `blog/smart-home-electrical-upgrades-la.html`

---

## LOW — Backlog

### L1. Expand 3 thin blog posts
**Impact:** Minor — these posts are 2.2-2.3KB  
**Effort:** Medium  
**Action:**
- Expand `signs-you-need-electrical-panel-upgrade`, `smart-home-electrical-upgrades-la`, `how-to-choose-electrician` with more content (target 3KB+)

### L2. Polish truncated meta descriptions
**Impact:** Minor — some descriptions end with `"... & more."`  
**Effort:** Low  
**Action:**
- Rewrite descriptions that end with truncated text to read naturally

### L3. Add YouTube channel sameAs
**Impact:** YouTube is the #1 AI citation source (0.737 correlation)  
**Effort:** Medium (requires creating channel + uploading videos)  
**Action:**
- Create YouTube channel
- Upload the 5 video scripts from `reports/youtube-scripts-2026-07-24.md`
- Add channel URL to sameAs arrays

### L4. Build Reddit presence
**Impact:** Reddit is 46.7% of Perplexity sources — AMY Electric has zero Reddit mentions  
**Effort:** Medium (ongoing)  
**Action:**
- Get customers to mention AMY Electric in r/LosAngeles electrician recommendation threads
- Consider an AMA or helpful comment presence (not promotional)

### L5. Claim BBB profile
**Impact:** BBB is a trusted citation source  
**Effort:** Low  
**Action:**
- Claim profile at bbb.org
- Add URL to sameAs arrays

### L6. Claim LinkedIn company page
**Impact:** LinkedIn is a trusted business citation  
**Effort:** Low  
**Action:**
- Create LinkedIn company page
- Add URL to sameAs arrays

---

## Summary

| Priority | Count | Effort |
|----------|-------|--------|
| Critical | 0 | — |
| High | 4 | 2 medium, 2 low |
| Medium | 5 | 1 trivial, 4 low |
| Low | 6 | 2 medium, 4 low |

**Estimated total effort:** ~4-6 hours for all High + Medium items  
**Expected score improvement:** 91 → 95+ (with High items completed)

---

*Generated by opencode SEO audit — July 24, 2026*
