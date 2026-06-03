// HTTP → HTTPS redirect middleware
// Checks the actual URL scheme reaching Pages (via request.url) plus standard headers
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const proto = url.protocol;
  const fwdProto = request.headers.get('x-forwarded-proto');
  const cfVisitor = request.headers.get('cf-visitor');
  if (
    proto === 'http:' ||
    fwdProto === 'http' ||
    (cfVisitor && cfVisitor.includes('"scheme":"http"'))
  ) {
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return context.next(request);
}
