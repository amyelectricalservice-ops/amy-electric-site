# SEO Action Plan — AMY Electric

**Generated:** June 18, 2026  
**Overall Score:** 7.6/10

---

## CRITICAL — Fix Immediately

| # | Task | Pages | Effort | Impact |
|---|------|-------|--------|--------|
| 1 | **Fix www.amyelectric.com 522 error** — Add DNS CNAME or redirect | DNS | 5 min | Users typing www see error page |
| 2 | **Fix og:image closing tag** — Add `>` to og:image, remove extra `>` from og:image:height | 107 | 5 min (find/replace) | Social previews broken |
| 3 | **Fix JSON-LD on comparison pages** — Remove stray comma + duplicate fields | 2 | 5 min each | Entire schema rejected by Google |
| 4 | **Fix breadcrumb text concatenation** — "Emergency Electrician24/7 Service" etc. | 5 | 10 min | Rich results display nonsense |
| 5 | **Consolidate 3 duplicate blog pairs** — 301 redirect shorter to longer | 6→3 | 15 min | Duplicate content diluting rankings |

---

## HIGH PRIORITY — Week 1

| # | Task | Pages | Effort | Impact |
|---|------|-------|--------|--------|
| 6 | **Add FAQ sections to all blog posts** — 3–5 Qs + FAQPage schema per post | 32 | 2–3 hrs | Zero blog posts have FAQs |
| 7 | **Expand 10 thin blog posts** to 1,500+ words with unique value | 10 | 3–4 hrs | Thin content risk |
| 8 | **Add author byline to all blog posts** — "By Amy, Licensed C-10 Electrician" | 32 | 30 min | E-E-A-T gap |
| 9 | **Add external source citations** — NEC, NFPA, LADWP, CSLB, DOE on each service page | 14 | 1 hr | Only 1/15 cites sources |
| 10 | **Add Electrician schema to emergency pages** | 5 | 15 min | No local rich results |
| 11 | **Add Service schema to geo service pages** | 32 | 30 min | No service rich results |
| 12 | **Assign page-specific OG images** to high-value service pages | 15 | 30 min | All share same generic image |
| 13 | **Fix breadcrumb middle level** — Add "Services" intermediate on emergency/comparison pages | 7 | 15 min | Missing hierarchy |

---

## MEDIUM PRIORITY — Week 2–3

| # | Task | Pages | Effort | Impact |
|---|------|-------|--------|--------|
| 14 | **Add SpeakableSchema to remaining 90 pages** | 90 | 1 hr | Voice search gap |
| 15 | **Add Quick Answer sections** to city + geo pages | 48 | 2 hrs | AI citation gap |
| 16 | **Add visible publication dates** to blog posts | 32 | 30 min | Freshness signal |
| 17 | **Create /about page** with Amy's full credentials | 1 | 2 hrs | Major E-E-A-T gap |
| 18 | **Expand city page FAQs** to 5–7 questions with unique local content | 16 | 2 hrs | Only 3 Qs, copy-pasted |
| 19 | **Improve blog internal linking** — target 5–7 cross-links per post | 32 | 1 hr | Averaging only 3 |
| 20 | **Deduplicate emergency FAQ answers** — each question gets unique answer | 5 | 30 min | Same answer for all 3 Qs |

---

## LOW PRIORITY — Month 2+

| # | Task | Pages | Effort | Impact |
|---|------|-------|--------|--------|
| 21 | **Add WebSite/SearchAction schema** to homepage | 1 | 15 min | Sitelinks search box |
| 22 | **Add dateModified to city pages** | 16 | 15 min | Freshness signal |
| 23 | **Remove deprecated expect-ct header** | _headers | 2 min | Clean headers |
| 24 | **Create project case studies** with photos | New | 4 hrs | Authority + E-E-A-T |
| 25 | **Add video content** to service pages | 15 | Ongoing | Engagement + dwell time |

---

## Dashboard Actions Required (User)

| # | Action | Where | Impact |
|---|--------|-------|--------|
| A | Add DNS CNAME for www.amyelectric.com → project.pages.dev | Cloudflare DNS | Fix 522 error |
| B | Disable Cloudflare Web Analytics beacon | Workers & Pages → Metrics | −200ms TBT |
| C | Set Security Level to "Essentially Off" | Security → Settings | −500ms TBT |
| D | Enable Cloudflare Polish (Lossy + WebP) | Speed → Settings | Image optimization |
| E | Reduce Turnstile security or disable on static pages | Turnstile settings | −500ms exec |

---

*Estimated total effort: ~20 hours for Critical + High priority items.*
*Estimated SEO score improvement: 7.6 → 8.5+ after completing items 1–13.*
