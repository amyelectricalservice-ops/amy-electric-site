# Blog Context & Lead Optimization Agent — Documentation

The Blog Context & Lead Optimization Agent (`scripts/blog-agent.py`) is designed to supply rich local Los Angeles business and regulatory context for blog posts and automatically audit & optimize blog articles to convert organic search traffic into high-value leads.

---

## Capabilities

1. **Local Context Generator (`--context`)**:
   Provides a single source of truth for business credentials (C-10 License #981578, EVITP #4051604), phone CTAs `(818) 302-5614`, local utilities (LADWP, SCE), permitting authorities (LADBS), transparent pricing ranges, and internal money-page target URLs.

2. **Lead Conversion Auditor (`--audit`)**:
   Scans every article in `blog/` for essential conversion elements:
   - Phone call triggers (`tel:18183025614`)
   - Online estimate triggers (`/get-quote` or `#estimator`)
   - High-converting lead CTA blocks
   - Local FAQPage schema
   - Internal links to core money pages

3. **Lead CTA Injector (`--inject-ctas`)**:
   Idempotently injects a styled lead capture box into blog posts. The CTA block features:
   - Direct click-to-call phone button
   - Online estimate request trigger
   - Trust signals: C-10 License #981578, EVITP #4051604, upfront pricing guarantee, LADWP permit handling

4. **Blog Topic Brief Generator (`--brief "<topic>"`)**:
   Generates a structured content brief with high-intent keyword targets, conversion elements, and local LA FAQs for creating new blog articles.

---

## CLI Usage

```bash
# View local business & regulatory context
python3 scripts/blog-agent.py --context

# Run lead conversion audit across all blog posts
python3 scripts/blog-agent.py --audit

# Inject high-converting CTA blocks into blog articles
python3 scripts/blog-agent.py --inject-ctas

# Generate blog brief for a specific topic
python3 scripts/blog-agent.py --brief "panel upgrade"
```

---

## Testing

Run unit tests via Node test runner:
```bash
node --test scripts/test-blog-agent.mjs
```
