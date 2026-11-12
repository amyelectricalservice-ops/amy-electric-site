// Analytics tracking removed — using Cloudflare Web Analytics (auto-injected beacon)
// Event tracking (gtag) was removed with Google Analytics migration.

(function () {
  'use strict';

  // Conversion events are logged server-side at /api/events (visible in
  // Workers Logs) so they survive without any third-party tracker.
  // sendBeacon with a plain string avoids a CORS preflight.
  function fireEvent(name, label, value) {
    try {
      // Forward to GA4 when the edge injected gtag (GA4_ID secret is set).
      // Without it this is a no-op and the first-party beacon below still runs.
      if (typeof window.gtag === 'function') {
        window.gtag('event', name, {
          event_label: String(label || '').slice(0, 200),
          value: value || 0,
          page_path: window.location.pathname
        });
      }
      var payload = JSON.stringify({
        event: name,
        label: String(label || '').slice(0, 200),
        value: value || 0,
        page: window.location.pathname.slice(0, 200),
      });
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/events', payload);
        return;
      }
      fetch('/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
        body: payload,
        keepalive: true,
      }).catch(function () {});
    } catch (err) {
      if (window.console) {
        console.log('[AMY Analytics]', name, label || '', value || 0);
      }
    }
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a');
    if (!link) return;

    if (link.href && /^tel:/.test(link.href)) {
      fireEvent('phone_click', 'phone_link', 1);
    }

    if (link.href && /estimate|contact|quote/i.test(link.href)) {
      fireEvent('cta_click', link.textContent.trim() || 'cta_link', 1);
    }

    // Performance optimization: Removed 'internal_link_click' event firing.
    // /api/events in worker.js explicitly rejects 'internal_link_click' (400 Bad Request).
    // Eliminating this check avoids URL parsing overhead on every click and prevents
    // useless network requests on every internal link navigation across the site.
  });

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form || !form.id) return;
    if (form.id === 'quick-form' || form.id === 'estimate-form' || form.id === 'lf-form') {
      fireEvent('form_submit', form.id, 1);
    }
  });

  // A lead is only real when the worker accepts it. Wrapping fetch catches
  // every submission path (quick form, detailed form, lead wizard and the
  // legacy estimator bundle) exactly once, and never fires on validation
  // failures or upload errors.
  if (typeof window.fetch === 'function' && !window.__amyFetchWrapped) {
    window.__amyFetchWrapped = true;
    var nativeFetch = window.fetch.bind(window);
    window.fetch = function (input, init) {
      var url = typeof input === 'string' ? input : ((input && input.url) || '');
      return nativeFetch(input, init).then(function (res) {
        try {
          if (res && res.ok && /\/api\/(contact|lead)$/.test(url)) {
            var cfg = window.AMY_ANALYTICS;
            if (typeof window.gtag === 'function') {
              window.gtag('event', 'generate_lead', { page_path: window.location.pathname });
              if (cfg && cfg.adsId && cfg.adsLabel) {
                window.gtag('event', 'conversion', { send_to: cfg.adsId + '/' + cfg.adsLabel });
              }
            }
            fireEvent('lead_accepted', url, 1);
          }
        } catch (err) { /* never break the page */ }
        return res;
      });
    };
  }
})();
