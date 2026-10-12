/* AMY Electric — geo personalization consumer (08-geo-personalize.js).
 *
 * worker.js personalizes the landing page for GEO_TARGET_AREAS visitors: it
 * injects `data-service-city` on <header> and sets window.AMY_GEO, and marks
 * the response private/no-store because the edge cannot Vary on cf.city.
 * That cache opt-out only buys something if a visitor can actually see their
 * city — this module is that consumer. Without it, matched visitors paid the
 * no-store penalty for a byte-identical page.
 *
 * It rewrites the existing hero eyebrow in place (same node, same position)
 * so there is no layout shift, and it no-ops everywhere else: pages without
 * window.AMY_GEO — every page except / — are untouched.
 *
 * Timing: worker.js injects the config inline before </body>, which runs
 * during parse, before deferred site.min.js and before DOMContentLoaded.
 */
(function () {
  'use strict';

  function cityOf() {
    if (typeof window === 'undefined' || !window.AMY_GEO) return null;
    var g = window.AMY_GEO;
    if (!g.matched || typeof g.city !== 'string' || !g.city) return null;
    return g.city;
  }

  function apply() {
    var city = cityOf();
    if (!city) return;
    if (typeof document === 'undefined' || !document.querySelector) return;
    var eyebrow = document.querySelector('.hero-eyebrow');
    if (!eyebrow) return;
    // Replace, never append: keeps the line one row tall (no CLS) and keeps
    // "Los Angeles" available in the h1 / hero copy below it.
    eyebrow.textContent = city + ' \u00b7 Residential & Commercial';
  }

  if (typeof document !== 'undefined' && document.addEventListener) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', apply);
    } else {
      apply();
    }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { apply: apply, cityOf: cityOf };
  } else if (typeof window !== 'undefined') {
    window.AMY_GEO_VISUAL = { apply: apply, cityOf: cityOf };
  }
})();
