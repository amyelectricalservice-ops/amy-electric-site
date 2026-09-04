/* AMY ELECTRIC — Site Scripts */
/* Source: js/src/ — edit modules, not this file */
/* Run: python3 scripts/build-js.py */
(function () {
  'use strict';

  var ham = document.querySelector('.hamburger');
  var nav = document.querySelector('nav');
  if (ham && nav) {
    ham.setAttribute('aria-expanded', 'false');
    ham.addEventListener('click', function () {
      var isOpen = ham.classList.toggle('open');
      nav.classList.toggle('open');
      ham.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  var links = document.querySelectorAll('nav a');
  var cur = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(function (l) {
    if (l.getAttribute('href') === cur || l.getAttribute('href') === './' + cur) {
      l.classList.add('active');
    }
  });
})();

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

(function () {
  'use strict';

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('.form-submit');
      btn.textContent = 'Sending\u2026';
      btn.disabled = true;

      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.success) {
            form.style.display = 'none';
            document.getElementById(successId).style.display = 'block';
          } else {
            throw new Error(res.message);
          }
        })
        .catch(function () {
          var data = Object.fromEntries(new FormData(form));
          var body = '';
          for (var k in data) {
            if (data.hasOwnProperty(k)) body += k + ': ' + data[k] + '\n';
          }
          window.location.href = 'mailto:info@amyelectric.com?subject=AMY%20Electric%20-%20' + encodeURIComponent(data.name || 'New Lead') + '&body=' + encodeURIComponent(body);
          form.style.display = 'none';
          document.getElementById(successId).style.display = 'block';
        });
    });
  }

  handleForm('quick-form', 'quick-form-success');
  handleForm('estimate-form', 'estimate-form-success');

  // Open estimator when linked from other pages
  if (window.location.hash === '#estimator') {
    document.getElementById('estimator') && document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('quote-estimator') && document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
