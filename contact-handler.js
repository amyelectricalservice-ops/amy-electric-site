export async function handleContact(request, env, waitUntil, extra = null) {
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

    /* --- Honeypot / spam traps --- */
    if (str(raw.website) !== '') {
      return successResponse();
    }
    if (raw._timestamp) {
      const elapsed = Date.now() - new Date(raw._timestamp).getTime();
      if (Number.isFinite(elapsed) && elapsed < 3000) {
        return successResponse();
      }
    }

    /* --- Data extraction + validation --- */
    const data = {
      name: str(raw.name).slice(0, 100),
      phone: str(raw.phone).slice(0, 25),
      email: str(raw.email).slice(0, 254),
      service: str(raw.service).slice(0, 50),
      city: str(raw.city).slice(0, 100),
      message: str(raw.message).slice(0, 5000),
      request_type: str(raw.request_type).slice(0, 50),
      estimate: parseEstimate(str(raw.estimate).slice(0, 2000)),
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

    /* --- Turnstile verification --- */
    const turnstileToken = str(raw['cf-turnstile-response']) || str(raw['g-recaptcha-response']);
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

    /* --- CRM webhook --- */
    if (env.GHL_WEBHOOK_URL) {
      waitUntil(
        fetch(env.GHL_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }).catch(() => {})
      );
    }

    /* --- Cloudflare Email Service or MailChannels fallback --- */
    if (env.EMAIL && typeof env.EMAIL.send === 'function') {
      waitUntil(
        env.EMAIL.send({
          to: 'info@amyelectric.com',
          from: 'noreply@amyelectric.com',
          subject: `[AMY Electric] ${data.service || data.request_type || 'New Lead'} — ${data.name || 'No name'}`,
          content: `formatLeadText(data, extra)`,
        }).catch(err => console.warn('Cloudflare Email Service error:', err))
      );
    } else {
      const notification = {
        personalizations: [{ to: [{ email: 'info@amyelectric.com' }] }],
        from: { email: 'noreply@amyelectric.com', name: 'AMY Electric Website' },
        subject: `[AMY Electric] ${data.service || data.request_type || 'New Lead'} — ${data.name || 'No name'}`,
        content: [{ type: 'text/plain', value: formatLeadText(data, extra) }],
      };
      waitUntil(
        fetch('https://api.mailchannels.net/tx/v1/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(notification),
        }).catch(() => {})
      );
    }

    /* --- PHASE 2: D1 Lead Persistence === */
    const crmDb = env.CRM_DB;
    if (crmDb) {
      // Normalize fields
      const phoneNorm = data.phone.replace(/\D/g, '');
      const emailNorm = data.email.toLowerCase().trim();
      const dedupeKey = phoneNorm || emailNorm;

      // Determine urgency and follow-up schedule
      let followUpAt;
      const urgencyText = (data.message || '').trim();
      const emergencyRe = /\b(sparking|smoking|burning|burn smell|fire|shock|exposed wire|water leak|no power|power outage|live wire|melted|scorch|overheat|hot panel|panel is hot|buzzing|very hot|really hot)\b/i;
      const sameDayRe = /\b(same[-]day|today|asap|urgent|emergency|right away|immediately)\b/i;
      if (emergencyRe.test(urgencyText)) {
        followUpAt = new Date(Date.now() + 15 * 60000).toISOString(); // 15 minutes
      } else if (sameDayRe.test(urgencyText)) {
        followUpAt = new Date(Date.now() + 2 * 3600000).toISOString(); // 2 hours
      } else {
        followUpAt = new Date(Date.now() + 24 * 3600000).toISOString(); // 24 hours
      }

      // Build the lead record for dedupe check + persist
      const nowIso = new Date().toISOString();
      const leadRecord = {
        id: 'tmp_' + Date.now() + Math.random().toString(36).slice(2), // temp id for dedupe check
        created_at: nowIso,
        updated_at: nowIso,
        name: data.name || '',
        phone: data.phone || '',
        phone_norm: phoneNorm,
        email: data.email || '',
        email_norm: emailNorm,
        city: data.city || '',
        service: data.service || '',
        request_type: data.request_type || '',
        message: data.message || '',
        estimate_json: data.estimate || '',
        segment: 'residential', // default; can be enhanced later
        urgency: followUpAt ? 'pending' : 'standard',
        score: 20, // base score; can be enhanced later with full scoreLead()
        score_reasons: '[\"base score\"]',
        source_page: data.request_type || '/contact',
        referrer: '',
        utm_source: '',
        utm_medium: '',
        utm_campaign: '',
        utm_term: '',
        utm_content: '',
        gclid: '',
        fbclid: '',
        status: 'new',
        crm_provider: '',
        crm_status: 'pending',
        dedupe_key: dedupeKey,
        duplicate_of: '',
        ip_hash: '',  // will be computed if needed
        user_agent: '',
        turnstile_ok: 1,
        follow_up_at: followUpAt,
      };

      // --- Check for duplicates (30-day window by phone_norm or email_norm) ---
      let isDuplicate = false;
      try {
        // Check by phone_norm
        if (phoneNorm && phoneNorm.length >= 7) {
          const row = await crmDb.prepare(
            `SELECT id, created_at FROM leads WHERE phone_norm = ? AND created_at >= ? AND duplicate_of = '' ORDER BY created_at DESC LIMIT 1`
          ).bind(phoneNorm, new Date(Date.now() - 30 * 86400000).toISOString()).first();
          if (row) {
            isDuplicate = true;
            leadRecord.duplicate_of = row.id;
            leadRecord.status = 'duplicate';
            leadRecord.crm_status = 'skipped';
          }
        }
        // If not duplicate by phone, check by email
        if (!isDuplicate && emailNorm) {
          const row = await crmDb.prepare(
            `SELECT id, created_at FROM leads WHERE email_norm = ? AND created_at >= ? AND duplicate_of = '' ORDER BY created_at DESC LIMIT 1`
          ).bind(emailNorm, new Date(Date.now() - 30 * 86400000).toISOString()).first();
          if (row) {
            isDuplicate = true;
            leadRecord.duplicate_of = row.id;
            leadRecord.status = 'duplicate';
            leadRecord.crm_status = 'skipped';
          }
        }
      } catch (e) {
        console.warn('D1 dedupe check failed:', e && e.message);
      }

      // --- Persist lead to D1 ---
      const insertLeadSql = `
        INSERT INTO leads (
          id, created_at, updated_at, name, phone, phone_norm, email, email_norm, city,
          service, request_type, message, estimate_json, segment, urgency, score,
          score_reasons, source_page, referrer, utm_source, utm_medium, utm_campaign,
          utm_term, utm_content, gclid, fbclid, status, crm_provider, crm_status,
          dedupe_key, duplicate_of, ip_hash, user_agent, turnstile_ok, follow_up_at
        ) VALUES (
          ?,?,?,?,?,?,?,?,?,
          ?,?,?,?,?,?,
          ?,?,?,?,?,
          ?,?,?,?,?,
          ?,?,?,?,?,
          ?,?,?,?
        )
      `;

      const leadIds = [
        leadRecord.id, leadRecord.created_at, leadRecord.updated_at, leadRecord.name,
        leadRecord.phone, leadRecord.phone_norm, leadRecord.email, leadRecord.email_norm,
        leadRecord.city, leadRecord.service, leadRecord.request_type, leadRecord.message,
        leadRecord.estimate_json, leadRecord.segment, leadRecord.urgency, leadRecord.score,
        leadRecord.score_reasons, leadRecord.source_page, leadRecord.referrer,
        leadRecord.utm_source, leadRecord.utm_medium, leadRecord.utm_campaign,
        leadRecord.utm_term, leadRecord.utm_content, leadRecord.gclid, leadRecord.fbclid,
        leadRecord.status, leadRecord.crm_provider, leadRecord.crm_status,
        leadRecord.dedupe_key, leadRecord.duplicate_of, leadRecord.ip_hash,
        leadRecord.user_agent, leadRecord.turnstile_ok, leadRecord.follow_up_at
      ];

      try {
        await crmDb.prepare(insertLeadSql).bind(...leadIds).run();
      } catch (err) {
        console.warn('D1 lead persist failed:', err && err.message);
        // Continue anyway — form submission should not fail because of DB write issues
      }

      // --- Record lead creation event ---
      try {
        const eventSql = `
          INSERT INTO lead_events (id, lead_id, event, label, page, meta, created_at)
          VALUES (?,?,?,?,?,?,?)
        `;
        const eventId = 'evt_' + Date.now() + Math.random().toString(36).slice(2);
        await crmDb.prepare(eventSql)
          .bind(eventId, leadRecord.id, 'lead_created', 'form submission', request.url,
            JSON.stringify({ score: leadRecord.score, segment: leadRecord.segment, duplicate: isDuplicate }),
          nowIso).run();
      } catch (e) {
        console.warn('D1 event record failed:', e && e.message);
      }
    }
    /* ------------------------------------------- */

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
