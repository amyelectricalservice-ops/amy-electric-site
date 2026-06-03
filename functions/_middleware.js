// Pages Function middleware — runs for requests that reach the Workers runtime
// NOTE: HTTP→HTTPS redirect requires "Always Use HTTPS" in Cloudflare dashboard
// (SSL/TLS → Edge Certificates). This middleware covers edge cases where the
// request reaches Pages via HTTP despite that setting (e.g., direct origin access).
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  if (url.protocol === 'http:' || request.headers.get('x-forwarded-proto') === 'http') {
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}