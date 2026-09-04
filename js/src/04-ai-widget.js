// Cloudflare Workers AI Widget for AMY Electric
// Provides instant questions & answers for LADWP rebates, panel sizing, and EV charger costs

(function() {
  if (typeof document === 'undefined') return;

  function initAIWidget() {
    const existing = document.getElementById('ae-ai-widget');
    if (existing) return;

    const container = document.createElement('div');
    container.id = 'ae-ai-widget';
    container.style.cssText = 'position:fixed;bottom:80px;right:20px;z-index:9999;font-family:system-ui,sans-serif';

    container.innerHTML = `
      <button id="ae-ai-toggle" aria-label="Ask AI Assistant" style="background:#f59e0b;color:#0a192f;border:none;border-radius:50px;padding:12px 20px;font-weight:700;font-size:14px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.3);display:flex;align-items:center;gap:8px">
        ⚡ Ask AI Electrician
      </button>
      <div id="ae-ai-box" style="display:none;position:absolute;bottom:60px;right:0;width:320px;background:#0f233e;border:1px solid #1e3a5f;border-radius:12px;padding:16px;box-shadow:0 10px 25px rgba(0,0,0,0.5);color:#fff">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;border-bottom:1px solid #1e3a5f;padding-bottom:8px">
          <strong style="font-size:15px;color:#f59e0b">⚡ AMY AI Assistant</strong>
          <button id="ae-ai-close" style="background:none;border:none;color:#94a3b8;font-size:18px;cursor:pointer">&times;</button>
        </div>
        <p style="font-size:13px;color:#cbd5e1;margin-bottom:12px;line-height:1.4">Ask about LADWP $500 rebates, 200A panel upgrade costs, or EV charger permits!</p>
        <div id="ae-ai-output" style="max-height:160px;overflow-y:auto;font-size:13px;background:#0a192f;padding:10px;border-radius:6px;margin-bottom:12px;color:#e2e8f0;display:none"></div>
        <form id="ae-ai-form" style="display:flex;gap:6px">
          <input type="text" id="ae-ai-input" placeholder="e.g. LADWP rebate amount?" style="flex:1;background:#0a192f;border:1px solid #1e3a5f;border-radius:6px;padding:8px 10px;color:#fff;font-size:13px" required>
          <button type="submit" style="background:#f59e0b;color:#0a192f;border:none;border-radius:6px;padding:8px 12px;font-weight:700;font-size:13px;cursor:pointer">Ask</button>
        </form>
      </div>
    `;

    document.body.appendChild(container);

    const toggleBtn = document.getElementById('ae-ai-toggle');
    const closeBtn = document.getElementById('ae-ai-close');
    const box = document.getElementById('ae-ai-box');
    const form = document.getElementById('ae-ai-form');
    const input = document.getElementById('ae-ai-input');
    const output = document.getElementById('ae-ai-output');

    toggleBtn.addEventListener('click', function() {
      box.style.display = box.style.display === 'none' ? 'block' : 'none';
      if (box.style.display === 'block') input.focus();
    });

    closeBtn.addEventListener('click', function() {
      box.style.display = 'none';
    });

    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const q = input.value.trim();
      if (!q) return;

      output.style.display = 'block';
      output.innerHTML = '<em style="color:#94a3b8">Consulting Workers AI...</em>';
      input.value = '';

      try {
        const res = await fetch('/api/ai-assistant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q })
        });
        const data = await res.json();
        if (data && data.answer) {
          output.innerHTML = data.answer;
        } else {
          output.innerHTML = 'Call (818) 302-5614 for an immediate estimate!';
        }
      } catch (err) {
        output.innerHTML = 'Call (818) 302-5614 for an immediate estimate!';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAIWidget);
  } else {
    initAIWidget();
  }
})();
