(function () {
  'use strict';

  // Seed render timestamps for the server-side timing trap on every form
  // that carries the hidden field (handled or not).
  document.querySelectorAll('input[name="_timestamp"]').forEach(function (ts) {
    if (!ts.value) ts.value = new Date().toISOString();
  });

  var MAX_FILES = 5;
  var MAX_BYTES = 10 * 1024 * 1024;
  var ALLOWED = /^(image\/(jpeg|png|webp|heic|heif)|application\/pdf)$/i;

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') {
      return window.crypto.randomUUID();
    }
    return 't-' + Date.now() + '-' + Math.random().toString(16).slice(2, 12);
  }

  // Attribution travels with the lead: landing page, referrer, UTM and click IDs.
  function seedAttribution(form) {
    var params = new URLSearchParams(window.location.search);
    var fields = {
      source_page: window.location.pathname,
      referrer: document.referrer || '',
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_term: params.get('utm_term') || '',
      utm_content: params.get('utm_content') || '',
      gclid: params.get('gclid') || '',
      fbclid: params.get('fbclid') || ''
    };
    Object.keys(fields).forEach(function (name) {
      if (!fields[name] || form.querySelector('input[name="' + name + '"]')) return;
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      input.value = fields[name];
      form.appendChild(input);
    });
  }

  function fileInput(form) {
    return form.querySelector('input[type="file"][data-upload-input]');
  }

  function listUploads(form) {
    return form.querySelector('[data-upload-list]');
  }

  function validateFiles(files) {
    if (files.length > MAX_FILES) {
      return 'Please choose up to ' + MAX_FILES + ' files.';
    }
    for (var i = 0; i < files.length; i += 1) {
      var f = files[i];
      if (f.size > MAX_BYTES) {
        return 'Each file must be 10 MB or smaller (' + f.name + ').';
      }
      if (f.type && !ALLOWED.test(f.type)) {
        return 'Please upload a JPG, PNG, WebP, HEIC or PDF file.';
      }
    }
    return '';
  }

  function uploadOne(file, token) {
    var fd = new FormData();
    fd.append('file', file);
    fd.append('upload_token', token);
    return fetch('/api/lead-files', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: fd
    }).then(function (r) {
      return r.json().then(function (res) {
        if (!r.ok || !res.success) throw new Error(res.message || 'Upload failed');
        return res.file;
      });
    });
  }

  // Uploads run BEFORE the lead POST so a storage failure never loses the lead.
  function uploadFiles(form, onProgress) {
    var input = fileInput(form);
    if (!input || !input.files || !input.files.length) return Promise.resolve([]);
    var files = Array.prototype.slice.call(input.files);
    var problem = validateFiles(files);
    if (problem) return Promise.reject(new Error(problem));

    var token = uuid();
    var uploaded = [];
    var chain = Promise.resolve();
    files.forEach(function (file, index) {
      chain = chain.then(function () {
        if (onProgress) onProgress('Uploading ' + (index + 1) + ' of ' + files.length + '…');
        return uploadOne(file, token).then(function (meta) { uploaded.push(meta); });
      });
    });
    return chain.then(function () {
      return { token: token, files: uploaded };
    });
  }

  function renderUploadList(form, files) {
    var list = listUploads(form);
    if (!list) return;
    list.innerHTML = '';
    Array.prototype.forEach.call(files, function (f) {
      var li = document.createElement('li');
      li.textContent = f.name + ' · ' + Math.round(f.size / 1024) + ' KB';
      list.appendChild(li);
    });
  }

  function wireUploadUi(form) {
    var input = fileInput(form);
    if (!input) return;
    input.addEventListener('change', function () {
      var problem = validateFiles(Array.prototype.slice.call(input.files || []));
      var note = form.querySelector('[data-upload-error]');
      if (note) {
        note.textContent = problem;
        note.style.display = problem ? 'block' : 'none';
      }
      if (problem) input.value = '';
      renderUploadList(form, input.files || []);
    });
  }

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

    seedAttribution(form);
    wireUploadUi(form);

    var errorBox = document.getElementById(formId + '-error');

    function showError(message) {
      if (errorBox) {
        errorBox.textContent = message;
        errorBox.style.display = 'block';
      }
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (errorBox) errorBox.style.display = 'none';
      var btn = form.querySelector('.form-submit');
      var originalText = btn.textContent;
      btn.textContent = 'Sending\u2026';
      btn.disabled = true;

      function resetBtn() {
        btn.textContent = originalText;
        btn.disabled = false;
      }

      uploadFiles(form, function (msg) { btn.textContent = msg; })
        .then(function (upload) {
          var fd = new FormData(form);
          fd.delete('uploads'); // never send raw files to the lead endpoint
          if (upload && upload.files.length) {
            fd.set('files', JSON.stringify(upload.files.map(function (f) { return f.id; })));
            fd.set('upload_token', upload.token);
          }
          btn.textContent = 'Sending\u2026';
          return fetch('/api/contact', {
            method: 'POST',
            headers: { 'Accept': 'application/json' },
            body: fd
          });
        })
        .then(function (r) {
          return r.json().then(function (res) {
            if (res.success) {
              form.style.display = 'none';
              document.getElementById(successId).style.display = 'block';
            } else if (r.status === 400) {
              // Server-side validation failure: show inline, stay on page.
              showError(res.message || 'Please check the highlighted fields and try again.');
              resetBtn();
            } else {
              throw new Error(res.message);
            }
          });
        })
        .catch(function (err) {
          // Network, upload or server failure: the lead never reached us.
          // Never pretend it sent — show an honest error and leave the form
          // visible so the visitor can retry or use the phone/email fallback.
          showError((err && err.message && /^Uploading|file|Upload/.test(err.message))
            ? err.message + ' You can also call (818) 302-5614.'
            : "Couldn't send — please try again, or email info@amyelectric.com or call (818) 302-5614.");
          resetBtn();
        });
    });
  }

  handleForm('quick-form', 'quick-form-success');
  handleForm('estimate-form', 'estimate-form-success');
  // NOTE: qe-form is submitted by the legacy estimator engine
  // (js/estimator.min.js), which builds its own FormData. Registering it
  // here too would double-POST every estimator lead.

  // Open estimator when linked from other pages
  if (window.location.hash === '#estimator') {
    document.getElementById('estimator') && document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('quote-estimator') && document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
