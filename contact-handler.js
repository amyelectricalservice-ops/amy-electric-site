export async function handleContact(request, env, waitUntil) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', Allow: 'POST' },
    });
  }

  try {
    const contentType = request.headers.get('Content-Type') || '';
    const raw = contentType.includes('application/json')
      ? await request.json()
      : Object.fromEntries(await request.formData());

    const str = (v) => (typeof v === 'string' ? v.trim() : '');

    if (str(raw.website) !== '') {
      return successResponse();
    }

    if (raw._timestamp) {
      const elapsed = Date.now() - new Date(raw._timestamp).getTime();
      if (Number.isFinite(elapsed) && elapsed < 3000) {
        return successResponse();
      }
    }

    // Allowlist + validate: unknown keys (file uploads, junk) are dropped.
    const data = {
      name: str(raw.name).slice(0, 100),
      phone: str(raw.phone).slice(0, 25),
      email: str(raw.email).slice(0, 254),
      service: str(raw.service).slice(0, 50),
      city: str(raw.city).slice(0, 100),
      message: str(raw.message).slice(0, 5000),
      request_type: str(raw.request_type).slice(0, 50),
    };

    if (data.name.length < 2) {
      return badRequest('Please enter your name (at least 2 characters).');
    }

    const digits = data.phone.replace(/\D/g, '');
    if (!/^[\d\s()+.-]{7,25}$/.test(data.phone) || digits.length < 7 || digits.length > 15) {
      return badRequest('Please enter a valid phone number with at least 7 digits.');
    }

    if (data.email !== '' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      return badRequest('Please enter a valid email address (or leave it blank).');
    }

    if (data.message !== '' && data.message.length < 5) {
      return badRequest('Please describe your project in a few more words.');
    }

    data._timestamp = new Date().toISOString();
    data._ip = request.headers.get('CF-Connecting-IP') || '';

    // Turnstile Token Validation
    const turnstileToken = data['cf-turnstile-response'] || data['g-recaptcha-response'];
    if (env.TURNSTILE_SECRET_KEY && turnstileToken) {
      const verifyRes = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          secret: env.TURNSTILE_SECRET_KEY,
          response: turnstileToken,
          remoteip: data._ip,
        }),
      });
      const verifyData = await verifyRes.json();
      if (!verifyData.success) {
        return new Response(
          JSON.stringify({ success: false, message: 'CAPTCHA verification failed. Please try again.' }),
          { status: 400, headers: { 'Content-Type': 'application/json' } }
        );
      }
    }

    if (env.GHL_WEBHOOK_URL) {
      waitUntil(
        fetch(env.GHL_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }).catch(() => {})
      );
    }

    const subject = `[AMY Electric] ${data.service || data.request_type || 'New Lead'} — ${data.name || 'No name'}`;
    const bodyText = formatLeadText(data);

    // 1. Cloudflare Email Service Binding (env.EMAIL or env.SEB)
    if (env.EMAIL && typeof env.EMAIL.send === 'function') {
      waitUntil(
        env.EMAIL.send({
          to: 'info@amyelectric.com',
          from: 'noreply@amyelectric.com',
          subject: subject,
          content: bodyText,
        }).catch(err => console.warn('Cloudflare Email Service error:', err))
      );
    } else {
      // 2. MailChannels REST API Fallback
      const notification = {
        personalizations: [{ to: [{ email: 'info@amyelectric.com' }] }],
        from: { email: 'noreply@amyelectric.com', name: 'AMY Electric Website' },
        subject: subject,
        content: [{ type: 'text/plain', value: bodyText }],
      };

      waitUntil(
        fetch('https://api.mailchannels.net/tx/v1/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(notification),
        }).catch(() => {})
      );
    }

    return successResponse();
  } catch (err) {
    return new Response(
      JSON.stringify({
        success: false,
        message: 'Something went wrong. Please try again or call (818) 302-5614.',
      }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}

function badRequest(message) {
  return new Response(JSON.stringify({ success: false, message }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' },
  });
}

function successResponse() {
  return new Response(JSON.stringify({ success: true, message: "Thank you! We'll be in touch shortly." }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}

function formatLeadText(data) {
  const lines = [];
  if (data.name) lines.push(`Name: ${data.name}`);
  if (data.phone) lines.push(`Phone: ${data.phone}`);
  if (data.email) lines.push(`Email: ${data.email}`);
  if (data.service) lines.push(`Service: ${data.service}`);
  if (data.city) lines.push(`City: ${data.city}`);
  if (data.message) lines.push(`Message:\n${data.message}`);
  if (data.request_type) lines.push(`Request Type: ${data.request_type}`);
  if (data._timestamp) lines.push(`Submitted: ${data._timestamp}`);
  return lines.join('\n') || 'No details provided.';
}
