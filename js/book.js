/* AMY Electric — booking widget (book.html only, standalone, not bundled).
 * Date UI: flatpickr 4.6.13 (MIT, (c) 2017 Gregory Petrosyan) vendored at
 * js/vendor/flatpickr-4.6.13.min.js. Slot rules below are the pure layer,
 * tested by node --test scripts/test-book.mjs. Slots are REQUESTS, not
 * guaranteed bookings: every submit POSTs to /api/contact with
 * request_type "booking-request" and the owner confirms by text.
 */
(function () {
  'use strict';

  // Arrival windows mirror the published office hours in schema:
  // Mon-Fri 07:00-17:00, Sat 08:00-14:00, Sun closed.
  var WEEKDAY_WINDOWS = [
    ['08:00', '10:00'], ['10:00', '12:00'], ['12:00', '14:00'], ['14:00', '16:00']
  ];
  var SAT_WINDOWS = [['08:00', '10:00'], ['10:00', '12:00']];
  var MAX_DAYS_AHEAD = 60;

  function isBookableDay(d) {
    return d.getDay() !== 0; // closed Sundays
  }

  function windowsFor(d) {
    if (d.getDay() === 0) return [];
    if (d.getDay() === 6) return SAT_WINDOWS.slice();
    return WEEKDAY_WINDOWS.slice();
  }

  function minDate() {
    var t = new Date();
    t.setHours(0, 0, 0, 0);
    t.setDate(t.getDate() + 1); // at least a day ahead; need today? call us
    return t;
  }

  function maxDate() {
    var t = minDate();
    t.setDate(t.getDate() + MAX_DAYS_AHEAD);
    return t;
  }

  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  function fmtDate(d) {
    return DAYS[d.getDay()] + ', ' + MONTHS[d.getMonth()] + ' ' +
           d.getDate() + ', ' + d.getFullYear();
  }

  function fmtWindow(w) {
    function t(hhmm) {
      var h = parseInt(hhmm.slice(0, 2), 10);
      var m = hhmm.slice(3);
      var ap = h >= 12 ? 'PM' : 'AM';
      h = h % 12;
      if (h === 0) h = 12;
      return h + ':' + m + ' ' + ap;
    }
    return t(w[0]) + ' – ' + t(w[1]);
  }

  function slotLabel(d, w) {
    return fmtDate(d) + ', ' + fmtWindow(w);
  }

  var api = {
    VERSION: '1.0.0',
    WEEKDAY_WINDOWS: WEEKDAY_WINDOWS,
    SAT_WINDOWS: SAT_WINDOWS,
    MAX_DAYS_AHEAD: MAX_DAYS_AHEAD,
    isBookableDay: isBookableDay,
    windowsFor: windowsFor,
    minDate: minDate,
    maxDate: maxDate,
    fmtDate: fmtDate,
    fmtWindow: fmtWindow,
    slotLabel: slotLabel
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  if (typeof window !== 'undefined') window.AMY_BOOK = api;

  // ── Page wiring (browser only) ──
  function init() {
    var wrap = document.getElementById('book-widget');
    var fallback = document.getElementById('book-fallback');
    if (!wrap) return;
    if (!window.flatpickr) return; // vendor failed: leave the call/form fallback up
    var calEl = document.getElementById('book-calendar');
    var slotsEl = document.getElementById('book-slots');
    var form = document.getElementById('book-form');
    var slotInput = document.getElementById('book-slot');
    var chosenEl = document.getElementById('book-chosen');
    if (!calEl || !slotsEl || !form || !slotInput) return;

    wrap.style.display = '';
    if (fallback) fallback.style.display = 'none';

    var picked = null;

    function renderSlots(date) {
      slotsEl.innerHTML = '';
      picked = null;
      slotInput.value = '';
      chosenEl.textContent = 'Pick a date, then choose an arrival window.';
      windowsFor(date).forEach(function (w) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'slot-btn';
        b.textContent = fmtWindow(w);
        b.addEventListener('click', function () {
          picked = w;
          slotInput.value = slotLabel(date, w);
          chosenEl.textContent = 'Your requested window: ' + slotInput.value;
          var sibs = slotsEl.querySelectorAll('.slot-btn');
          for (var i = 0; i < sibs.length; i++) sibs[i].classList.remove('selected');
          b.classList.add('selected');
        });
        slotsEl.appendChild(b);
      });
    }

    window.flatpickr(calEl, {
      inline: true,
      appendTo: calEl,
      minDate: minDate(),
      maxDate: maxDate(),
      disable: [function (d) { return !isBookableDay(d); }],
      onChange: function (sel) { if (sel.length) renderSlots(sel[0]); }
    });

    var ts = form.querySelector('input[name="_timestamp"]');
    if (ts && !ts.value) ts.value = new Date().toISOString();

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = document.getElementById('book-form-error');
      function fail(msg) {
        if (err) { err.textContent = msg; err.style.display = 'block'; }
      }
      if (err) err.style.display = 'none';
      if (!slotInput.value) { fail('Please pick a date and arrival window first.'); return; }
      var btn = form.querySelector('.form-submit');
      var orig = btn.textContent;
      btn.textContent = 'Sending…';
      btn.disabled = true;
      fetch('/api/contact', { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
        .then(function (r) {
          return r.json().then(function (res) {
            if (res.success) {
              form.style.display = 'none';
              document.getElementById('book-form-success').style.display = 'block';
            } else if (r.status === 400) {
              fail(res.message || 'Please check the highlighted fields and try again.');
              btn.textContent = orig;
              btn.disabled = false;
            } else {
              throw new Error(res.message);
            }
          });
        })
        .catch(function () {
          fail('Connection issue — please call (818) 302-5614 and we will book you in directly.');
          btn.textContent = orig;
          btn.disabled = false;
        });
    });
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  }
})();
