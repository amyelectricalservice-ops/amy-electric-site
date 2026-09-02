// Analytics tracking removed — using Cloudflare Web Analytics (auto-injected beacon)
// Event tracking (gtag) was removed with Google Analytics migration.

(function () {
  'use strict';

  function fireEvent(name, label, value) {
    var payload = { event: name, label: label || '', value: value || 0 };

    if (window.dataLayer && Array.isArray(window.dataLayer)) {
      window.dataLayer.push(payload);
      return;
    }

    if (window.gtag) {
      window.gtag('event', name, { event_label: label || '', value: value || 0 });
      return;
    }

    if (window.console) {
      console.log('[AMY Analytics]', name, label || '', value || 0);
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

    if (link.href && !/^mailto:|^tel:|^https?:/.test(link.href) && link.href.indexOf('amyelectric.com') === -1) {
      fireEvent('internal_link_click', link.getAttribute('href') || 'internal_link', 1);
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
