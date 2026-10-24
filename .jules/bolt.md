## 2026-10-24 - Edge Worker Allocation Churn in Hot Path
**Learning:** In Cloudflare Workers (V8 Isolate runtime), converting byte arrays to hex via `[...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('')` and linear array lowercasing in geo-routing handlers create object allocation churn on every request.
**Action:** Use a module-level pre-computed `HEX_TABLE` and `Map` lookup for case-insensitive string matching to keep hot worker request paths O(1) and allocation-free.
