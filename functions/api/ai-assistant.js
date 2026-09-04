// Cloudflare Pages Function — AI Electrical Assistant Endpoint
// POST /api/ai-assistant — processes user queries regarding EV chargers, panel upgrades, LADWP rebates, and costs

const KNOWLEDGE_BASE = {
  rebates: "LADWP offers up to $500 rebate for residential Level 2 EV charger installations (up to $1,000 for income-qualified customers). SCE offers up to $4,200 for panel upgrades when adding EV charging in select areas.",
  panel_upgrade: "Standard 200-amp panel upgrade costs between $2,500 and $5,000 in Los Angeles, including LADBS permits, utility coordination, and full inspection.",
  ev_charger: "Level 2 EV charger installation runs $1,000 to $2,500 depending on distance from panel to garage and whether panel capacity allows a 40A/50A 240V breaker.",
  permits: "LADBS (Los Angeles Dept of Building and Safety) electrical permits are required for all panel swaps and 240V circuits. AMY Electric includes permit acquisition in all estimates.",
  licensing: "AMY Electric holds California C-10 License #981578 and EVITP Certification #4051604, fully bonded and insured with 15+ years experience in Greater LA."
};

export async function onRequest(context) {
  const { request, env } = context;

  // Enable CORS Preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }

  try {
    const data = await request.json();
    const query = (data.query || '').trim();

    if (!query) {
      return new Response(JSON.stringify({ error: 'Query is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    let responseText = "";

    // 1. Check if Cloudflare Workers AI binding `env.AI` is configured
    if (env && env.AI) {
      try {
        const aiResponse = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
          messages: [
            {
              role: 'system',
              content: `You are AMY Electric's AI Assistant for Los Angeles. Provide helpful, accurate, concise answers about EV chargers, 200A panel upgrades, LADWP rebates, LADBS permits, and local LA electrical codes. Key facts: ${JSON.stringify(KNOWLEDGE_BASE)}. Phone: (818) 302-5614.`
            },
            { role: 'user', content: query }
          ],
          max_tokens: 300,
        });

        if (aiResponse && aiResponse.response) {
          responseText = aiResponse.response;
        }
      } catch (aiErr) {
        console.warn('Workers AI binding error, using fallback logic:', aiErr);
      }
    }

    // 2. Structured Domain Engine Fallback if Workers AI is not bound or returned empty
    if (!responseText) {
      const q = query.toLowerCase();
      if (q.includes('rebate') || q.includes('ladwp') || q.includes('sce') || q.includes('credit')) {
        responseText = `${KNOWLEDGE_BASE.rebates} Need help claiming your rebate? Call AMY Electric at (818) 302-5614 for a free estimate!`;
      } else if (q.includes('panel') || q.includes('200 amp') || q.includes('100 amp') || q.includes('upgrade')) {
        responseText = `${KNOWLEDGE_BASE.panel_upgrade} ${KNOWLEDGE_BASE.permits} Call (818) 302-5614 to schedule an on-site load calculation.`;
      } else if (q.includes('ev') || q.includes('charger') || q.includes('tesla') || q.includes('level 2')) {
        responseText = `${KNOWLEDGE_BASE.ev_charger} We install Tesla Wall Connectors, ChargePoint, JuiceBox, and NEMA 14-50 outlets. Call (818) 302-5614 to get started.`;
      } else if (q.includes('permit') || q.includes('ladbs') || q.includes('city')) {
        responseText = `${KNOWLEDGE_BASE.permits} We handle 100% of permitting and inspection scheduling with LADBS across all 16 LA city areas.`;
      } else {
        responseText = `AMY Electric is a licensed C-10 (#981578) and EVITP (#4051604) contractor in Greater Los Angeles. For EV chargers, 200A panel upgrades, rewiring, or emergency service, call us directly at (818) 302-5614 for a free estimate!`;
      }
    }

    return new Response(JSON.stringify({ answer: responseText, success: true }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-store',
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error', detail: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }
}
