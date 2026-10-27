# Bolt's Journal

## 2026-10-27 - O(1) Map Lookup for Edge Geo Personalization Matching
**Learning:** `matchTargetCity` in Cloudflare Worker edge request path was iterating through an array of target city strings and calling `.toLowerCase()` in a loop on every request check. Pre-building a `Map` of lowercased target city names to canonical city strings converts $O(N)$ linear scans with repeated string allocations into an $O(1)$ constant time lookup (~6x faster, reducing lookup CPU overhead on edge workers).
**Action:** Use pre-computed static `Map` lookups for constant allowlists or target matching in hot Worker request paths.
