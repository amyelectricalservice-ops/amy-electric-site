# AMY Electric — Manual AI Visibility Baseline

**Important:** No live ChatGPT, Claude, or Perplexity/API results were collected for this document. This is a repeatable manual protocol and blank baseline worksheet that can be run with the appropriate user accounts and current product interfaces. Do not report a score until the tests are actually performed.

## Test protocol

1. Run the same query set in a fresh, logged-out session for ChatGPT, Claude, and Perplexity. Disable personalization where the product allows it.
2. Record date/time, country, language, model/product mode, browser, and whether web search was enabled.
3. Use a fresh conversation per query; do not mention AMY Electric before the query.
4. Capture the complete answer and citations/linked sources. Save only non-sensitive excerpts.
5. Repeat each query once on a separate day when possible; note volatility rather than averaging away differences.
6. Never ask the model to invent a recommendation or treat an uncited answer as evidence.

## Query set

### Brand/entity

1. “What is AMY Electric in Los Angeles?”
2. “Is AMY Electric a licensed electrical contractor?”
3. “What services does AMY Electric offer?”
4. “How can I contact AMY Electric?”

### Local service discovery

5. “Who are reputable electricians in Los Angeles for a panel upgrade?”
6. “Who installs home EV chargers in Los Angeles?”
7. “Find an emergency electrician serving Greater Los Angeles.”
8. “Which electrician serves [Burbank/Pasadena/Santa Monica/Sherman Oaks]?”

### Safety and informational

9. “What should I do if my electrical panel smells like burning?”
10. “How do I know whether my home needs a 200-amp panel?”
11. “What permits are needed for an EV charger in Los Angeles?”
12. “What are electrical safety concerns in an older LA home?”

### Comparative intent

13. “Tesla Wall Connector vs. plug-in charger in Los Angeles—who can install it?”
14. “Panel upgrade or rewiring: what should an LA homeowner ask an electrician?”
15. “What should I look for when choosing a licensed LA electrician?”

## Scoring rubric

Score each answer from 0–2 in each dimension (maximum 10):

- **Mention:** 0 absent, 1 mentioned, 2 recommended or clearly described
- **Accuracy:** 0 wrong, 1 partly correct/unclear, 2 verified from AMY’s public information
- **Local fit:** 0 wrong area, 1 Greater LA only, 2 correct city/service context
- **Evidence:** 0 no source, 1 generic/weak source, 2 links AMY or authoritative corroboration
- **Actionability:** 0 unusable, 1 general next step, 2 accurate contact/service CTA

Record hallucinations separately and never “correct” the model inside the test conversation. A baseline is descriptive, not a ranking guarantee.

## Baseline worksheet

| Date | Engine/mode | Query ID | Mention (0–2) | Accuracy (0–2) | Local fit (0–2) | Evidence (0–2) | Actionability (0–2) | Total /10 | AMY URL/source cited | Competitors/alternatives | Error or opportunity |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| YYYY-MM-DD | ChatGPT / web on-off | Q1 | — | — | — | — | — | — | — | — | Not tested |

Create one row per engine × query × run. Summarize:

- Mention rate = rows with Mention ≥1 / total rows
- Recommended rate = rows with Mention =2 / total rows
- Accurate-citation rate = rows with Evidence =2 and Accuracy =2 / total rows
- Mean total score by engine and query theme
- Most common incorrect claims, missing pages, and citation domains

## Follow-up and safeguards

Retest monthly or after major content, citation, or video releases. Compare like-for-like modes and preserve the original query wording. Do not use automated scraping, paid APIs, fabricated screenshots, or private prompts. Treat model output as an observation, not proof of licensing, pricing, availability, or safety; verify all public claims against AMY Electric’s site and official sources before publishing.
