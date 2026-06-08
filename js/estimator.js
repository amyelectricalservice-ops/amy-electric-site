(function () {
  'use strict';

  var step = 1;
  var data = {};
  var prices = {
    'nema14-50': { baseLow: 350, baseHigh: 550 },
    'tesla-wall': { baseLow: 450, baseHigh: 750 },
    'hardwired': { baseLow: 500, baseHigh: 900 }
  };
  var distAdjust = { 'short': { low: 0, high: 0 }, 'medium': { low: 100, high: 150 }, 'long': { low: 200, high: 300 } };
  var outdoorAdjust = { low: 50, high: 150 };
  var panelUpgrade = { low: 2500, high: 4500 };

  var vehicles = [
    { make: 'Tesla', model: 'Model 3' },
    { make: 'Tesla', model: 'Model Y' },
    { make: 'Tesla', model: 'Model S' },
    { make: 'Tesla', model: 'Model X' },
    { make: 'Tesla', model: 'Cybertruck' },
    { make: 'Ford', model: 'Mustang Mach-E' },
    { make: 'Ford', model: 'F-150 Lightning' },
    { make: 'Chevrolet', model: 'Bolt EV' },
    { make: 'Chevrolet', model: 'Bolt EUV' },
    { make: 'Chevrolet', model: 'Silverado EV' },
    { make: 'Hyundai', model: 'Ioniq 5' },
    { make: 'Hyundai', model: 'Ioniq 6' },
    { make: 'Hyundai', model: 'Kona Electric' },
    { make: 'Kia', model: 'EV6' },
    { make: 'Kia', model: 'EV9' },
    { make: 'Kia', model: 'Niro EV' },
    { make: 'Nissan', model: 'Leaf' },
    { make: 'Rivian', model: 'R1T' },
    { make: 'Rivian', model: 'R1S' },
    { make: 'Volkswagen', model: 'ID.4' },
    { make: 'BMW', model: 'i4' },
    { make: 'BMW', model: 'iX' },
    { make: 'Mercedes-Benz', model: 'EQS' },
    { make: 'Mercedes-Benz', model: 'EQE' },
    { make: 'Porsche', model: 'Taycan' },
    { make: 'Audi', model: 'Q4 e-tron' },
    { make: 'Audi', model: 'Q8 e-tron' },
    { make: 'Lucid', model: 'Air' },
    { make: 'Toyota', model: 'bZ4X' },
    { make: 'Subaru', model: 'Solterra' },
    { make: 'Volvo', model: 'EX30' },
    { make: 'Volvo', model: 'XC40 Recharge' },
    { make: 'Polestar', model: '2' },
    { make: 'Genesis', model: 'GV60' },
    { make: 'GMC', model: 'Hummer EV' },
    { make: 'Cadillac', model: 'Lyriq' },
    { make: 'Mazda', model: 'MX-30' },
    { make: 'Fiat', model: '500e' },
    { make: 'Toyota', model: 'Prius Prime' }
  ];

  function init() {
    var el = document.getElementById('quote-estimator');
    if (!el) return;
    populateVehicles();
    bindEvents();
    showStep(1);
  }

  function populateVehicles() {
    var makeSel = document.getElementById('qe-make');
    var modelSel = document.getElementById('qe-model');
    if (!makeSel || !modelSel) return;

    var makes = {};
    vehicles.forEach(function (v) { makes[v.make] = true; });
    Object.keys(makes).sort().forEach(function (m) {
      var opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m;
      makeSel.appendChild(opt);
    });

    makeSel.addEventListener('change', function () {
      populateModels(makeSel.value, modelSel);
    });
    populateModels(makeSel.value, modelSel);
  }

  function populateModels(make, modelSel) {
    modelSel.innerHTML = '<option value="">Select model...</option>';
    if (!make) return;
    vehicles.filter(function (v) { return v.make === make; }).forEach(function (v) {
      var opt = document.createElement('option');
      opt.value = v.model;
      opt.textContent = v.model;
      modelSel.appendChild(opt);
    });
  }

  function bindEvents() {
    // Service selection cards
    var cards = document.querySelectorAll('.qe-svc-card');
    cards.forEach(function (c) {
      c.addEventListener('click', function () {
        cards.forEach(function (x) { x.classList.remove('selected'); });
        c.classList.add('selected');
        data.service = c.getAttribute('data-value');
        if (data.service === 'panel-upgrade') {
          goToStep(3);
        } else if (data.service === 'other') {
          goToStep(3);
        } else {
          goToStep(2);
        }
      });
    });

    // Step 2 controls
    var chargerBtns = document.querySelectorAll('.qe-charger-btn');
    chargerBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        chargerBtns.forEach(function (x) { x.classList.remove('selected'); });
        b.classList.add('selected');
        data.charger = b.getAttribute('data-value');
      });
    });

    // Step 3 radio groups
    var radios = document.querySelectorAll('.qe-estimator input[type="radio"]');
    radios.forEach(function (r) {
      r.addEventListener('change', function () {
        data[r.name] = r.value;
      });
    });

    // Navigation buttons
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-qe]');
      if (!btn) return;
      var action = btn.getAttribute('data-qe');
      if (action === 'next-s2') { if (validateStep2()) goToStep(3); }
      else if (action === 'next-s3') { if (validateStep3()) goToStep(4); }
      else if (action === 'back-s1') { goToStep(1); }
      else if (action === 'back-s2') { goToStep(2); }
      else if (action === 'back-s3') { goToStep(3); }
    });

    // Step 4 form submit
    var form = document.getElementById('qe-form');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        submitEstimate();
      });
    }
  }

  function validateStep2() {
    if (!data.charger) { alert('Please select a charger type.'); return false; }
    if (!data.make || !data.model) { alert('Please select your vehicle make and model.'); return false; }
    return true;
  }

  function validateStep3() {
    if (!data.panel) { alert('Please select your current panel size.'); return false; }
    if (!data.distance) { alert('Please select the approximate distance from panel to installation location.'); return false; }
    if (!data.location) { alert('Please select the installation location.'); return false; }
    return true;
  }

  function showStep(n) {
    step = n;
    var steps = document.querySelectorAll('.qe-step');
    steps.forEach(function (s, i) {
      s.classList.toggle('active', i + 1 === n);
    });
    var dots = document.querySelectorAll('.qe-dot');
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i + 1 <= n);
    });
    var labels = document.querySelectorAll('.qe-step-label');
    labels.forEach(function (l, i) {
      l.classList.toggle('active', i + 1 <= n);
    });

    if (n === 4) {
      showResult();
    }

    document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function goToStep(n) {
    showStep(n);
  }

  function calculatePrice() {
    if (data.service === 'panel-upgrade') {
      return { low: 2500, high: 4500, parts: ['200A Panel Replacement: $2,500–$4,500'] };
    }
    if (data.service === 'other') {
      return null;
    }
    var p = prices[data.charger] || prices['nema14-50'];
    var d = distAdjust[data.distance] || distAdjust['short'];
    var totalLow = p.baseLow + d.low;
    var totalHigh = p.baseHigh + d.high;
    var parts = [];

    var chargerNames = { 'nema14-50': 'NEMA 14-50 Outlet', 'tesla-wall': 'Tesla Wall Connector', 'hardwired': 'Hardwired EVSE' };
    parts.push(chargerNames[data.charger] + ': $' + p.baseLow + '–$' + p.baseHigh);

    if (data.distance !== 'short') {
      parts.push('Run length (' + data.distance + '): +$' + d.low + '–$' + d.high);
    }
    if (data.location === 'outdoor') {
      totalLow += outdoorAdjust.low;
      totalHigh += outdoorAdjust.high;
      parts.push('Outdoor weatherproofing: +$' + outdoorAdjust.low + '–$' + outdoorAdjust.high);
    }
    if (data.panel === '100a') {
      totalLow += panelUpgrade.low;
      totalHigh += panelUpgrade.high;
      parts.push('100A → 200A Panel Upgrade: +$' + panelUpgrade.low + '–$' + panelUpgrade.high);
    }

    return { low: totalLow, high: totalHigh, parts: parts };
  }

  function showResult() {
    var result = document.getElementById('qe-result');
    var val = document.getElementById('qe-result-value');
    var breakdown = document.getElementById('qe-breakdown');
    var resultCta = document.getElementById('qe-result-cta');
    if (!result) return;

    var calc = calculatePrice();
    if (!calc) {
      val.innerHTML = 'Contact us for a custom quote';
      breakdown.innerHTML = '<p>Every electrical project is unique. Tell us what you need and we will provide a detailed estimate.</p>';
      resultCta.style.display = 'none';
      result.style.display = 'block';
      return;
    }

    val.innerHTML = '$' + calc.low.toLocaleString() + ' – $' + calc.high.toLocaleString();

    var html = '<ul style="list-style:none;padding:0;margin:0 0 20px;font-size:14px;color:var(--gray);text-align:left;max-width:400px;margin:0 auto 20px;">';
    calc.parts.forEach(function (p) {
      html += '<li style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.06);display:flex;gap:8px;"><span style="color:var(--gold);flex-shrink:0;">✓</span><span>' + p + '</span></li>';
    });
    html += '</ul>';
    breakdown.innerHTML = html;

    result.style.display = 'block';
    resultCta.style.display = '';
  }

  function submitEstimate() {
    var name = document.getElementById('qe-name').value.trim();
    var phone = document.getElementById('qe-phone').value.trim();
    if (!name || !phone) { alert('Please enter your name and phone number.'); return; }

    var btn = document.querySelector('#qe-form .form-submit');
    if (btn) { btn.textContent = 'Sending...'; btn.disabled = true; }

    var calc = calculatePrice();
    var formData = new FormData();
    formData.append('name', name);
    formData.append('phone', phone);
    formData.append('email', document.getElementById('qe-email').value.trim());
    formData.append('city', document.getElementById('qe-city').value.trim());
    formData.append('service', data.service === 'ev-charger' ? 'EV Charger Installation' : data.service === 'panel-upgrade' ? 'Panel Upgrade' : 'Other');
    formData.append('message', 'Quote Estimator - ' + JSON.stringify(data) + ' - Estimated: $' + (calc ? calc.low + '–$' + calc.high : 'TBD'));
    formData.append('_estimator', 'true');

    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: formData
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.success) {
          document.getElementById('qe-form-wrap').style.display = 'none';
          document.getElementById('qe-form-success').style.display = 'block';
        } else {
          throw new Error(res.message);
        }
      })
      .catch(function () {
        var body = 'Quote Estimator\\nName: ' + name + '\\nPhone: ' + phone + '\\nData: ' + JSON.stringify(data);
        window.location.href = 'mailto:info@amyelectric.com?subject=AMY%20Electric%20-%20Estimator%20Lead&body=' + encodeURIComponent(body);
        document.getElementById('qe-form-wrap').style.display = 'none';
        document.getElementById('qe-form-success').style.display = 'block';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
