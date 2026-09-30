// Analytics tracking removed — using Cloudflare Web Analytics (auto-injected beacon)
// Event tracking (gtag) was removed with Google Analytics migration.

(function () {
  'use strict';

  // Conversion events are logged server-side at /api/events (visible in
  // Workers Logs) so they survive without any third-party tracker.
  // sendBeacon with a plain string avoids a CORS preflight.
  function fireEvent(name, label, value) {
    try {
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

    // link.href is always absolute in the DOM, so scheme/host tests have to run
    // against the resolved URL rather than the raw attribute.
    if (link.href && !/^(mailto:|tel:|sms:)/i.test(link.href)) {
      var sameSite = false;
      try {
        sameSite = new URL(link.href, window.location.href).origin === window.location.origin;
      } catch (err) {
        sameSite = false;
      }
      if (sameSite) {
        fireEvent('internal_link_click', link.getAttribute('href') || 'internal_link', 1);
      }
    }
  });

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form || !form.id) return;
    if (form.id === 'quick-form' || form.id === 'estimate-form') {
      fireEvent('form_submit', form.id, 1);
    }
  });
})();
