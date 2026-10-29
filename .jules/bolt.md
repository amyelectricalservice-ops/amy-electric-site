# Bolt's Journal - Critical Learnings

## 2026-10-24 - [Avoid Unhandled Event Beacons]
**Learning:** Client-side tracking scripts firing events that the backend endpoint rejects (`400 Bad Request`) cause unnecessary network requests (`sendBeacon`/`fetch`) on every user action (e.g., internal link clicks) and CPU overhead from `new URL()` allocations.
**Action:** Always verify that client-side event tracking matches the backend allowlist (e.g. `allowEvents` in `worker.js`) before emitting beacons.
