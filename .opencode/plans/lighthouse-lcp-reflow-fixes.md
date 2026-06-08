# Lighthouse Fixes — LCP Render Delay + Forced Reflow

## Fix 1: Eliminate forced reflow in estimator.js

**File:** `js/estimator.js:186`

**Change:** Replace `offsetTop` query (forces sync layout) with `scrollIntoView`:

```js
// BEFORE:
window.scrollTo({ top: document.getElementById('quote-estimator').offsetTop - 100, behavior: 'smooth' });

// AFTER:
document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
```

**CSS addition** (anywhere in `css/style.css`):
```css
#quote-estimator { scroll-margin-top: 100px; }
```

## Fix 2: Trim inline `<style>` block to critical-only CSS

**File:** `index.html` lines 30-88

**Keep inline** (above-the-fold critical only):
- `*, *::before, *::after { box-sizing }` (line 30)
- `:root { --navy ... }` (lines 31)
- `html { scroll-behavior }` (line 32)
- `body { font-family ... }` (lines 33-37)
- `a { color: var(--gold) }` (line 34)
- `img { max-width }` (line 35)
- `.wrap {}` (line 36)
- `.text-center {}` (line 37)
- `.sr-only {}` (line 38)
- `.skip-link {}` (lines 39-40)
- `*:focus-visible {}` (lines 41-42)
- `@media (prefers-reduced-motion) {}` (line 42)
- `.topbar {}` (lines 43-44)

**Move to external CSS** (`css/style.css`):
- `.topbar a:hover` (moved from inline — already exists in style.css:101)
- `header` (line 45)
- `.header-inner` (line 46)
- `.logo`, `.logo-mark`, `.logo-text`, `.logo-name`, `.logo-sub` (lines 47-54)
- `nav`, `nav a`, `.hamburger` (lines 55-57)
- `.nav-cta` (line 58)
- `h1` (line 59)
- `p` (line 60)
- `ul` (line 60)
- `.btn`, `.btn-gold`, `.btn-outline`, `.btn-navy` (lines 61-64)
- `.hero` (line 65)
- `.hero-inner` (line 66)
- `.hero-eyebrow` (line 67)
- `.hero h1` (line 68)
- `.hero-desc` (line 69)
- `.hero-badges` (line 70)
- `.badge` (lines 71-72)
- `.hero-ctas` (line 73)
- `.cta-band` (lines 74-77)
- `.section-label` (line 78)
- `h2` (line 79)
- `.page-hero` (line 80)
- `.breadcrumb` (lines 81-82)
- `.page-hero h1` (line 83)
- `.page-hero p` (line 84)
- `@media(max-width:900px)` (line 85)
- `@media(max-width:680px)` header/nav/hamburger (line 86)
- `.sticky-bar`, `.sticky-btn`, `.sticky-estimate` (lines 87-90)
- `@media(min-width:768px)` (line 90)
- `@media(max-width:767px)` (line 90)

**After trimming**, the inline block shrinks from ~58 lines to ~20 lines (~6KB → ~2KB). This reduces CSS parse time before first paint by ~60%, directly reducing the 590ms LCP element render delay.

## Fix 3: Add hero image to homepage

**File:** `index.html` line 530

**Change:** Replace `grid-template-columns: 1fr` with the standard 2-column grid and add the hero image:

```html
<!-- BEFORE: -->
<div class="hero-inner" style="grid-template-columns:1fr">
  <div class="hero-content">
    ...
  </div>
</div>

<!-- AFTER: -->
<div class="hero-inner">
  <div class="hero-content">
    ...
    <div class="hero-ctas">
      ...
    </div>
  </div>
  <div class="hero-image">
    <img src="img/hero-electrician.jpg" alt="Licensed electrician working on electrical panel in Los Angeles" width="560" height="420" loading="eager" fetchpriority="high">
  </div>
</div>
```

The `fetchpriority="high"` and `loading="eager"` ensure this image becomes the LCP element and loads immediately.

Also add `.hero-image` CSS (already exists in `style.css` at the relevant section, but ensure it's not in the inline block — if it is, it will be moved out in Fix 2).

## Files to modify
1. `js/estimator.js` + `js/estimator.min.js` — scrollIntoView
2. `css/style.css` — scroll-margin-top + moved CSS from inline
3. `index.html` — trim inline style block + hero image
4. `css/style.min.css`, `js/site.min.js`, `js/estimator.min.js` — re-minify after changes
