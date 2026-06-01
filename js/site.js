/* AMY Electric — site.js */
(function () {
  'use strict';

  /* ── Mobile nav ── */
  const ham = document.querySelector('.hamburger');
  const nav = document.querySelector('nav');
  if (ham && nav) {
    ham.setAttribute('aria-expanded', 'false');
    ham.addEventListener('click', () => {
      const isOpen = ham.classList.toggle('open');
      nav.classList.toggle('open');
      ham.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  /* ── Active nav link ── */
  const links = document.querySelectorAll('nav a');
  const cur = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(l => {
    if (l.getAttribute('href') === cur || l.getAttribute('href') === './' + cur) {
      l.classList.add('active');
    }
  });

  /* ── Estimate form ── */
  const form = document.getElementById('estimate-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = form.querySelector('.form-submit');
      btn.textContent = 'Sending…';
      btn.disabled = true;

      /* Collect data */
      const data = Object.fromEntries(new FormData(form));

      /* Send via Formspree (replace ACTION in HTML) or mailto fallback */
      const action = form.getAttribute('action');
      if (action && action.startsWith('https://formspree.io')) {
        fetch(action, {
          method: 'POST',
          headers: { 'Accept': 'application/json' },
          body: new FormData(form)
        })
        .then(r => r.ok ? showSuccess() : showFallback(data))
        .catch(() => showFallback(data));
      } else {
        /* mailto fallback */
        showFallback(data);
      }
    });

    function showSuccess() {
      document.getElementById('form-success').style.display = 'block';
      document.getElementById('estimate-form').style.display = 'none';
    }

    function showFallback(data) {
      /* Open mailto as fallback */
      const requestType = data.request_type === 'service' ? 'Service Request' : 'Free Estimate Request';
      const body = `Request Type: ${requestType}\nName: ${data.name}\nPhone: ${data.phone}\nEmail: ${data.email}\nService: ${data.service}\nCity: ${data.city}\nMessage: ${data.message}`;
      window.location.href = `mailto:info@amyelectric.com?subject=${encodeURIComponent(requestType + ' - ' + data.name)}&body=${encodeURIComponent(body)}`;
      showSuccess();
    }
  }

})();
