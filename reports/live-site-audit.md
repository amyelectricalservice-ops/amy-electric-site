# Live Site Technical SEO Audit — amyelectric.com

**Audit Date:** June 18, 2026  
**Auditor:** Automated curl-based crawl  
**Canonical URL:** https://amyelectric.com

---

## 1. HTTP/HTTPS & www Redirect Status

| Check | Status | Detail |
|-------|--------|--------|
| HTTP → HTTPS | ✅ PASS | `http://amyelectric.com` → 301 → `https://amyelectric.com/` |
| HTTP www → HTTPS www | ✅ PASS | `http://www.amyelectric.com` → 301 → `https://www.amyelectric.com/` |
| HTTPS www → non-www | ❌ **FAIL** | `https://www.amyelectric.com` returns **522 Connection Timed Out** |

**Critical Issue:** The `www` subdomain returns a Cloudflare 522 error. This means:
- Users typing `www.amyelectric.com` see an error page
- Any old links pointing to the www version are broken
- There is no redirect from www → non-www as intended by `_redirects`

**Root cause:** The Cloudflare Pages project likely has `www.amyelectric.com` listed as a custom domain but the DNS records for the www subdomain aren't properly configured (missing or pointing to wrong target). The `_redirects` file can only handle redirects within a valid project domain — if the www domain isn't resolving to the project, the redirect never fires.

**Fix:** Either:
1. **Add a DNS CNAME** for `www.amyelectric.com` → `<project>.pages.dev` (then the `_redirects` rule will fire), OR
2. **Remove `www.amyelectric.com`** from the Cloudflare Pages custom domains and add a DNS-level 301 redirect at the registrar/Cloudflare DNS level

---

## 2. Response Headers Analysis

### Security Headers (Homepage — https://amyelectric.com)

| Header | Value | Verdict |
|--------|-------|---------|
| `strict-transport-security` | `max-age=31536000; includeSubDomains; preload` | ✅ Excellent — HSTS with preload |
| `content-security-policy` | Comprehensive CSP (see below) | ✅ Strong |
| `x-content-type-options` | `nosniff` | ✅ |
| `x-frame-options` | `DENY` | ✅ |
| `referrer-policy` | `strict-origin-when-cross-origin` | ✅ |
| `permissions-policy` | Restricts camera, mic, geolocation, etc. | ✅ |
| `expect-ct` | `max-age=86400, enforce` | ⚠️ Deprecated but harmless |

### CSP Analysis
```
default-src 'self';
script-src 'self' 'unsafe-inline' https://challenges.cloudflare.com https://static.cloudflareinsights.com https://www.googletagmanager.com;
style-src 'self' 'unsafe-inline';
font-src 'self';
img-src 'self' data: https://amyelectric.com;
connect-src 'self' https://api.mailchannels.net https://challenges.cloudflare.com https://www.google-analytics.com;
frame-ancestors 'none';
base-uri 'self';
form-action 'self' https://api.mailchannels.net;
```

**Notes:**
- `unsafe-inline` in script-src is needed for the inline Cloudflare challenge and JSON-LD schemas
- GA4 tag manager is whitelisted
- Cloudflare Web Analytics (`static.cloudflareinsights.com`) is whitelisted
- MailChannels API whitelisted for contact form email delivery
- No external font CDN needed (self-hosted fonts) ✅

### Caching Headers
| Header | Value | Verdict |
|--------|-------|---------|
| `cache-control` | `public, max-age=0, must-revalidate` | ⚠️ Edge-cached by Cloudflare but no browser cache. Consider `max-age=3600` for static assets |
| `cf-cache-status` | `HIT` | ✅ Cloudflare edge caching is working |

### Other Headers
- **Server:** `cloudflare` ✅
- **HTTP/2:** Supported ✅
- **alt-svc:** `h3=":443"` — HTTP/3 enabled ✅
- **NEL:** Reporting configured ✅

---

## 3. Sitemap Health

### Overview
| Metric | Value |
|--------|-------|
| Total URLs | **108** |
| Valid XML | ✅ Yes |
| All HTTPS | ✅ Yes (0 non-HTTPS URLs) |
| Valid lastmod dates | ✅ All between 2026-06-03 and 2026-06-17 |
| Image sitemap | ✅ Gallery page includes 30 `<image:image>` entries |

### URL Breakdown by Category
| Category | Count |
|----------|-------|
| Service pages | 23 |
| City/location pages | 16 |
| Geo service pages (EV + panel per city) | 35 |
| Blog posts (incl. index) | 34 |
| Special pages (gallery, testimonials, privacy) | 3 |
| **Total** | **108** |

### lastmod Date Analysis
| Date | Usage |
|------|-------|
| 2026-06-03 | Bulk of pages (initial publish) |
| 2026-06-04 | Gallery, comparison pages |
| 2026-06-08 | Privacy policy |
| 2026-06-17 | Two newest blog posts (code changes, LADWP rebate) |

**Verdict:** All dates are reasonable — no future dates, no stale dates older than publish cycle.

### Sample URL Validation (10 random from sitemap)
All 10 sampled URLs returned **HTTP 200** ✅

---

## 4. Robots.txt Analysis

```
User-agent: *
Allow: /
Disallow: /api/

User-agent: GPTBot
Allow: /
[... 8 AI crawlers explicitly allowed ...]

User-agent: CCBot
Disallow: /
User-agent: Bytespider
Disallow: /
User-agent: cohere-ai
Disallow: /

# RSL License: /rsl.json
Sitemap: https://amyelectric.com/sitemap.xml
```

**Verdict:**
- ✅ Sitemap reference present and correct
- ✅ AI search crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) explicitly allowed — excellent for AI Overviews/GEO
- ✅ Training crawlers (CCBot, Bytespider, cohere-ai) blocked
- ✅ `/api/` properly disallowed
- ✅ RSL license reference present

---

## 5. Page Load Times

### Initial Cold Load
| Page | Time |
|------|------|
| Homepage (`/`) | 0.83s |
| `panel-upgrade.html` | 0.61s |
| `city-los-angeles.html` | **16.31s** ⚠️ |
| `blog/` | 1.27s |
| `gallery.html` | 0.19s |

### Warm Cache (second request)
| Page | Time |
|------|------|
| Homepage (`/`) | 0.44s |
| `city-los-angeles` | 0.57s |
| `panel-upgrade` | 0.20s |
| `blog/` | 0.54s |
| `gallery.html` | 0.14s |

**Notes:**
- First load of `city-los-angeles` was abnormally slow (16.3s) — likely a cold start or Cloudflare edge miss. Second load was 0.57s, which is normal.
- `gallery.html` is the fastest page (static content, no complex rendering)
- All warm-cache times are under 0.6s — well within acceptable range
- Cloudflare edge caching (CF-Cache-Status: HIT) is working effectively

---

## 6. Critical File Availability

| File | Status | Notes |
|------|--------|-------|
| `favicon.svg` | ✅ 200 | Navy + gold AE lightning bolt |
| `llms.txt` | ✅ 200 | AI-friendly site description |
| `rsl.json` | ✅ 200 | Responsible AI licensing |
| `css/style.min.css` | ⚠️ Intermittent | Initial check timed out (000), second check 200 in 0.86s |
| `js/site.min.js` | ✅ 200 | |
| `fonts/BarlowCondensed-600.woff2` | ✅ 200 | Self-hosted, no external dependency |

**Note on CSS:** The CSS file returned a connection timeout on first attempt but succeeded on retry. This may indicate occasional cold-start delays at the Cloudflare edge. Not a persistent issue.

---

## 7. Broken Links / 404s

### Tested Pages (10 pages, with and without .html)

All 10 pages tested return **HTTP 200** when accessed without the `.html` extension:

| Page | Status |
|------|--------|
| `/ev-charger-installation` | ✅ 200 |
| `/panel-upgrade` | ✅ 200 |
| `/city-los-angeles` | ✅ 200 |
| `/city-santa-monica` | ✅ 200 |
| `/ev-charger-installation-los-angeles` | ✅ 200 |
| `/blog/california-electrical-code-changes-2026` | ✅ 200 |
| `/emergency-electrician` | ✅ 200 |
| `/gallery` | ✅ 200 |
| `/testimonials` | ✅ 200 |
| `/privacy-policy` | ✅ 200 |

**Note:** URLs with `.html` extension (e.g., `panel-upgrade.html`) return **301 → 301 → 200** (double redirect through extension-stripping). This is functional but not ideal — each hop adds latency. The canonical URLs in the HTML and sitemap correctly omit `.html`.

### Sample Sitemap URL Check (10 random)
All 10 random URLs from the sitemap returned **HTTP 200** ✅

---

## 8. Additional Findings

### GA4 / Google Analytics
- ✅ **Present:** `G-QVSNBR7PTS`
- Loaded via `https://www.googletagmanager.com/gtag/js?id=G-QVSNBR7PTS`
- Configured with `gtag('config', 'G-QVSNBR7PTS')`
- CSP properly whitelists `www.googletagmanager.com` and `www.google-analytics.com`

### Cloudflare Turnstile / Challenge Scripts
- ⚠️ **Present:** Cloudflare challenge-platform script injected on homepage
- Script: `/cdn-cgi/challenge-platform/scripts/jsd/main.js`
- This is Cloudflare's bot detection/challenge system (not Turnstile CAPTCHA for forms)
- It creates an invisible iframe for fingerprinting
- **Impact:** Adds ~50-100ms to page load for challenge evaluation. On fast connections this is negligible, but it does add JavaScript execution overhead.

### HTML Bug Found
**Line 21 of homepage:** Double closing bracket in `og:image:height` tag:
```html
<meta property="og:image:height" content="630">>
```
Should be:
```html
<meta property="og:image:height" content="630">
```
This produces invalid HTML and could confuse parsers. The `>>` is treated as text content by browsers but may cause issues with strict HTML validators and some social media crawlers.

### Schema Markup
- ✅ Electrician JSON-LD present on homepage
- ✅ FAQPage schema present
- ✅ BreadcrumbList present
- ✅ Open Graph and Twitter Card meta tags present

---

## 9. Summary & Priority Fixes

### Critical (Fix Immediately)
| # | Issue | Impact |
|---|-------|--------|
| 1 | **`www.amyelectric.com` returns 522** | Users/links to www domain see error page. No redirect to non-www working. |
| 2 | **OG meta tag HTML bug** (`>>`) | Invalid HTML, potential social media preview issues |

### High Priority
| # | Issue | Impact |
|---|-------|--------|
| 3 | **Double 301 redirect on .html URLs** | Each hop adds ~100-200ms latency. Clean up `.html` extension handling. |
| 4 | **CSS file cold-start timeout** | Occasional slow first loads for CSS. Consider adding `Cache-Control` headers for static assets. |

### Low Priority / Optimization
| # | Issue | Impact |
|---|-------|--------|
| 5 | **No browser cache headers** (`max-age=0`) | Static assets revalidate on every visit. Add `max-age` for CSS/JS/images. |
| 6 | **Cloudflare challenge script overhead** | Adds JS execution time. Consider if bot protection is needed on all pages. |
| 7 | **`expect-ct` header** | Deprecated by browsers. Can be removed. |

---

*Audit completed June 18, 2026. All checks performed via `curl` from Cloudflare edge (SJC PoP).*
