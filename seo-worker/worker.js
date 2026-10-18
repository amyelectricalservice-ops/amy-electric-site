/* amy-electric-seo — edge wrapper in front of amy-electric-site.
 *
 * It owns every amyelectric.com zone route, but amy-electric-site owns the
 * content: this Worker only forwards, adding the CORS headers cross-origin
 * callers need on /api/ responses. It deliberately generates nothing.
 *
 * An earlier revision answered its own /sitemap.xml, /robots.txt, /llms.txt,
 * /faq, /<service>, /electrician-<city> and /<service>-<city> pages before
 * contacting the origin, and rewrote the origin's HTML on the way back. That
 * shadowed the site's real pages (a 233-URL sitemap over the site's 306, one
 * identical <title> on ~300 pages, duplicate canonical/description/OG tags),
 * and the ~200 pages only it had were linked from nowhere and listed in no
 * sitemap. Those paths now fall through to the site, which answers 404 — with
 * its own 404 page — wherever it has no page.
 *
 * See scripts/test-seo-wrapper.mjs.
 */
const SITE = "https://amyelectric.com";

export default {
  async fetch(request, env) {
    const resp = await env.ORIGIN.fetch(request);
    const path = new URL(request.url).pathname;

    if (path.indexOf("/api/") === 0) {
      const headers = new Headers(resp.headers);
      headers.set("Access-Control-Allow-Origin", SITE);
      headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
      headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
      return new Response(resp.body, { status: resp.status, headers });
    }

    return resp;
  },
};
