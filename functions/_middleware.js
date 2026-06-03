// HTTP → HTTPS redirect middleware
export async function onRequest(context) {
  const { request } = context;
  const proto = request.headers.get('x-forwarded-proto');
  if (proto === 'http') {
    const url = new URL(request.url);
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return context.next(request);
}
