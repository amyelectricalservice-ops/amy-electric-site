export async function handleContact(request, env, waitUntil) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', Allow: 'POST' },
    });
  }

  try {
    const contentType = request.headers.get('Content-Type') || '';
    const data = contentType.includes('application/json')
      ? await request.json()
      : Object.fromEntries(await request.formData());

    if (data.website && data.website.trim() !== '') {
      return successResponse();
    }

    if (data._timestamp) {
      const elapsed = Date.now() - new Date(data._timestamp).getTime();
      if (elapsed < 3000) {
        return successResponse();
      }
    }

    data._timestamp = new Date().toISOString();
    data._ip = request.headers.get('CF-Connecting-IP') || '';

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
