// HTTP → HTTPS redirect (runs on every request at Cloudflare edge)
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const proto = request.headers.get('x-forwarded-proto') || 'https';
    if (proto === 'http' || url.protocol === 'http:') {
      url.protocol = 'https:';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
