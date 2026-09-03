import { handleContact } from './contact-handler.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.protocol === 'http:' || request.headers.get('x-forwarded-proto') === 'http') {
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === '/api/contact') {
      return handleContact(request, env, ctx.waitUntil.bind(ctx));
    }

    return env.ASSETS.fetch(request);
  },
};
