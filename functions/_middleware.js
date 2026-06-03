// HTTP → HTTPS redirect for Cloudflare Pages
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const forwardedProto = request.headers.get('x-forwarded-proto') || '';
  const cfVisitor = request.headers.get('cf-visitor') || '';
  const cloudflareForwardedProto = request.headers.get('Cloudflare-Forwarded-Proto') || '';

  // Try all known Cloudflare protocol signals
  const isHttp =
    url.protocol === 'http:' ||
    forwardedProto === 'http' ||
    cfVisitor.includes('"scheme":"http"') ||
    cloudflareForwardedProto === 'http';

  if (isHttp) {
    url.protocol = 'https:';
    url.port = '';
    return Response.redirect(url.toString(), 301);
  }

  const response = await context.next();
  // Debug: tag responses so we can see middleware ran
  const newHeaders = new Headers(response.headers);
  newHeaders.set('x-debug-proto', url.protocol);
  newHeaders.set('x-debug-fwd', forwardedProto);
  newHeaders.set('x-debug-cfproto', cloudflareForwardedProto);
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders,
  });
}
