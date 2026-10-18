// Merged photo API handler (from amy-electric-photos + amy-electric-portfolio workers).
// Serves /api/photos, /api/photos/count, /api/dates, /api/photo, /api/map,
// /api/photo/file, /api/upload with CORS headers.

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders, ...extra },
  });
}

export async function handlePhotoRequest(request, env) {
  const url = new URL(request.url);
  const path = url.pathname;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  // /api/photos
  if (path === '/api/photos') {
    const date = url.searchParams.get('date');
    const location = url.searchParams.get('location');
    const category = url.searchParams.get('category');
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '50'), 200);
    const offset = parseInt(url.searchParams.get('offset') || '0');
    let query = 'SELECT * FROM photos WHERE 1=1';
    const params = [];
    if (date) { query += ' AND date = ?'; params.push(date); }
    if (location) { query += ' AND location LIKE ?'; params.push(`%${location}%`); }
    if (category) { query += ' AND category = ?'; params.push(category); }
    query += ' ORDER BY date DESC LIMIT ? OFFSET ?';
    params.push(limit, offset);
    const results = await env.DB.prepare(query).bind(...params).all();
    return json({ photos: results.results, total: results.meta?.total_count });
  }

  // /api/photos/count
  if (path === '/api/photos/count') {
    const results = await env.DB.prepare('SELECT COUNT(*) as count FROM photos').first();
    return json({ count: results?.count || 0 });
  }

  // /api/dates
  if (path === '/api/dates') {
    const results = await env.DB.prepare(
      'SELECT date, COUNT(*) as count FROM photos GROUP BY date ORDER BY date DESC'
    ).all();
    return json({ dates: results.results });
  }

  // /api/photo
  if (path === '/api/photo') {
    const id = url.searchParams.get('id');
    if (!id) return json({ error: 'id parameter required' }, 400);
    let photo = await env.DB.prepare('SELECT * FROM photos WHERE id = ?').bind(id).first();
    if (!photo) photo = await env.DB.prepare('SELECT * FROM photos ORDER BY id LIMIT 1').first();
    if (!photo) return json({ error: 'Photo not found' }, 404);
    return json({ photo });
  }

  // /api/map
  if (path === '/api/map') {
    const results = await env.DB.prepare(
      'SELECT id, filename, date, location, description FROM photos WHERE location LIKE "%deg%"'
    ).all();
    const points = results.results.filter((p) => p.location).map((p) => {
      const match = p.location.match(/(\d+) deg (\d+)' ([\d.]+)" ([NS]),(\d+) deg (\d+)' ([\d.]+)" ([EW])/);
      if (!match) return null;
      const lat = parseFloat(match[1]) + parseFloat(match[2]) / 60 + parseFloat(match[3]) / 3600;
      const lon = parseFloat(match[5]) + parseFloat(match[6]) / 60 + parseFloat(match[7]) / 3600;
      const finalLat = match[4] === 'S' ? -lat : lat;
      const finalLon = match[8] === 'W' ? -lon : lon;
      return { id: p.id, filename: p.filename, date: p.date, lat: finalLat, lon: finalLon, description: p.description };
    }).filter(Boolean);
    return json({ points });
  }

  // /api/photo/file
  if (path === '/api/photo/file') {
    const id = url.searchParams.get('id');
    if (!id) return json({ error: 'id parameter required' }, 400);
    const photo = await env.DB.prepare('SELECT * FROM photos WHERE id = ?').bind(id).first();
    if (!photo) return json({ error: 'Photo not found' }, 404);
    if (env.BUCKET) {
      const key = `photos/${photo.id}.${photo.extension}`;
      const object = await env.BUCKET.get(key);
      if (object) {
        return new Response(object.body, {
          headers: { 'Content-Type': `image/${photo.extension.replace('jpg', 'jpeg')}`, ...corsHeaders },
        });
      }
    }
    return json({ error: 'File not available. Enable R2 for file serving.' }, 404);
  }

  // /api/upload
  if (path === '/api/upload') {
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || authHeader !== `Bearer ${env.UPLOAD_TOKEN}`) {
      return json({ error: 'Unauthorized' }, 401);
    }
    const formData = await request.formData();
    const file = formData.get('file');
    const date = formData.get('date') || new Date().toISOString().slice(0, 10);
    const location = formData.get('location') || 'Uploaded';
    const description = formData.get('description') || '';
    const category = formData.get('category') || 'other';
    if (!file) return json({ error: 'No file provided' }, 400);

    const ext = file.name.split('.').pop()?.toLowerCase() || 'jpg';
    const buffer = await file.arrayBuffer();
    const fileSize = buffer.byteLength;

    if (env.BUCKET) {
      const insertResult = await env.DB.prepare(
        'INSERT INTO photos (filename, date, location, description, category, extension, filesize) VALUES (?, ?, ?, ?, ?, ?, ?)'
      ).bind(file.name, date, location, description, category, ext, fileSize).run();
      const newId = insertResult.meta?.last_row_id;
      const key = `photos/${newId}.${ext}`;
      await env.BUCKET.put(key, buffer, { httpMetadata: { contentType: file.type || 'image/jpeg' } });
      const photo = await env.DB.prepare('SELECT * FROM photos WHERE id = ?').bind(newId).first();
      return json({ success: true, photo }, 201);
    }
    return json({ error: 'R2 bucket not configured' }, 500);
  }

  return json({ error: 'Not found' }, 404);
}