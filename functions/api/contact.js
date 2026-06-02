// Cloudflare Pages Function — Form handler
// POST /api/contact — accepts form submissions from quick-form & estimate-form

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', Allow: 'POST' },
    });
  }

  try {
    const contentType = request.headers.get('Content-Type') || '';
    let data;

    if (contentType.includes('application/json')) {
      data = await request.json();
    } else {
      const formData = await request.formData();
      data = Object.fromEntries(formData);
    }

    data._timestamp = new Date().toISOString();
    data._ip = request.headers.get('CF-Connecting-IP') || '';

    // Forward to GoHighLevel if webhook URL is configured
    if (env.GHL_WEBHOOK_URL) {
      context.waitUntil(
        fetch(env.GHL_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }).catch(() => { /* silent */ })
      );
    }

    // Send notification email via MailChannels (Cloudflare Pages free tier)
    const notification = {
      personalizations: [{ to: [{ email: 'info@amyelectric.com' }] }],
      from: { email: 'noreply@amyelectric.com' },
      subject: `[AMY Electric] ${data.service || data.request_type || 'New Lead'} — ${data.name || 'No name'}`,
      content: [
        {
          type: 'text/plain',
          value: formatLeadText(data),
        },
      ],
    };

    context.waitUntil(
      fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(notification),
      }).catch(() => { /* silent */ })
    );

    return new Response(
      JSON.stringify({ success: true, message: 'Thank you! We\'ll be in touch shortly.' }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ success: false, message: 'Something went wrong. Please try again or call (818) 302-5614.' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
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
