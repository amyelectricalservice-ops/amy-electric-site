## 2026-10-22 - [Map Lookup for Geo Target City Matching]
**Learning:** In Cloudflare Worker requests executed on every request or landing page hit, linear iteration over array elements (e.g. `GEO_TARGET_AREAS.map(...)`) introduces avoidable CPU overhead and garbage allocation.
**Action:** Use static pre-computed data structures like `Map` or `Set` initialized at module scope for constant-time $O(1)$ lookup functions.
