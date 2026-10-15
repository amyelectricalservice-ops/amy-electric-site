# Electric Photo Library — DB + Website Content Plan

Built 2026-10-14 by scanning the local archive. The Google Photos link
(`photos.google.com/search/...`) requires login — it cannot be fetched by an
agent, **but its export was found locally**: `~/Pictures/Photos-website/Electric
Work/` (1,933 files) is the downloaded "electric" search set, and it is now
covered by the DB below. To import future Google Photos sets, export them first
(§5), then re-run `python3 scripts/scan-organized-photos.py`.

## 0. Shipped 2026-10-14/15: Winnetka job + 52-photo gallery promotion

- 4 photos curated from `Photos-website/Upgrade Electrical Panel Winnetka/`
  (before → meter-main → wide → wired), live on `city-winnetka.html` + gallery.
- 52 more promoted from the reviewed draft (all individually viewed, crops
  verified, captions corrected per-photo): gallery 314 → **366 photos**.
  4 needed custom crop bands (`20260727-01`, `20240504-01-v2`,
  `20260611-04`, `20260903-04`); 7 captions corrected after crop review caught
  day-caption mismatches; 6 dropped (tape-measure doc shots, non-electrical
  curb photo w/ house number, handwritten name-like tag, redundant sibling).
- Meter-serial policy: serials/IDs on meter faces are NOT LADWP account numbers,
  but all three legible ones are now blurred anyway (zero-doubt): `wired`
  (dial serial), `20260203-03` (dial serial), `20260904-01` (smart-meter display
  + serial sticker + DWP seal tag). Logged in `data/privacy-redactions.json`,
  applied by `scripts/apply-redactions.py` — which MUST be re-run after any
  future `process-photos.py` run (it overwrites redacted outputs with clean
  renders). One readable street address (`12301 Magnolia`,
  `photo-20230130-01-v2`) was dropped, never published.
- Gallery rebuilt (`update-gallery.py`); `audit-site.py` + `schema-tool.py
  validate` pass clean. DB patched to match (365/366 manifest sources resolved
  in scanned tree).

- 4 photos curated from `Photos-website/Upgrade Electrical Panel Winnetka/`:
  `gallery-winnetka-panel-before` (original meter+subpanel+service drop),
  `gallery-winnetka-meter-main` (new meter-main w/ emergency disconnect, close-up),
  `gallery-winnetka-panel-wide` (new unit in opened wall, wide),
  `gallery-winnetka-panel-wired` (open panel, wired breakers).
- Sources are EXIF-orientation-6 phone shots: pipeline `exif_transpose` makes them
  3000×4000 portrait, so `custom_crop` boxes in the manifest are in
  **post-transpose portrait coordinates** (verified: re-running
  `process-photos.py` reproduces all 16 outputs byte-identically).
- Gallery now **366 photos**; `city-winnetka.html` gained a
  "Local Project: 200A Panel Upgrade" before/during section (first photos on that
  page).
- Winnetka privacy check (zoomed 2–3x): before/meter-main/wide dials unreadable —
  clear. `wired` meter serial legible but is not an account number — ships logged.

## 1. What the DB is

| Artifact | Contents |
|---|---|
| `data/photo-db.sqlite` | Table `photos(file,folder,date,year,bytes,processed,junk,category,caption,city,slug)` — 1,928 rows: every file under `organized/` **plus** the Google Photos export (`Photos-website/Electric Work/`, `Upgrade Electrical Panel Winnetka/`) |
| `data/photo-inventory.json` | Same data as JSON (for scripts/themes) |
| `data/new-photos-draft.csv` | 166 manifest-ready rows: best unprocessed 2022+ photos across all sources, max 4/day by file size, junk + <500 KB skipped |
| `scripts/photo-manifest.csv` | Canonical manifest (366 published). Draft rows get appended here after review |
| `scripts/scan-organized-photos.py` | Re-runnable scanner that rebuilds all three `data/` files |

Query examples:

```sql
-- unprocessed pool by year
SELECT year, COUNT(*) FROM photos WHERE processed=0 AND junk=0 AND bytes>=300000 GROUP BY year;
-- published mix
SELECT category, COUNT(*) FROM photos WHERE processed=1 GROUP BY category;
```

## 2. Library snapshot

- `organized/`: 1,506 images, 205 date folders. 309 of the first 310 published photos trace back here.
- Google Photos export (`Photos-website/Electric Work/`, 1,933 files): 1,528 overlap
  `organized/`, 309 in manifest, **403 truly new — 393 dated 2026** (recent,
  unpublished work). Plus 19 more in `Upgrade Electrical Panel Winnetka/` (4 shipped,
  §0).
- Published (366): panel 90 · commercial 90 · new-construction 78 · lighting 50 ·
  other 25 · exterior 17 · team 13 · lifestyle 3.
- Remaining draft (`new-photos-draft.csv`): **109 rows**, all reviewed; the
  only unpromoted keeps are second-choice alternates the gallery didn't need.
  (59 days, 6 parallel reviewer passes; per-day keep/reject recorded in
  `data/review-verdicts.json`). Mix: new-construction 32 · commercial 25 ·
  other 17 · exterior 15 · lighting 13 · panel 12 · team 1, incl. 7 Winnetka
  panel-job alternates. 51 rows dropped as junk/duplicates. Zero `REVIEW`
  placeholders left; every caption is a human-verified description.
- Privacy holds found in review (must clear before those rows ship):
  `photo-20230130-01` DROPPED (readable street address "12301 Magnolia" on
  disconnect label — confirmed by zoom); `photo-20260904-01` (meter serial
  AND9-1684898 readable), `photo-20260203-03` (meter face partly readable),
  shipped `gallery-winnetka-panel-wired` (GE meter serial + reading legible —
  not an account number, but flagged). `20220707` dropped (worker face).

Spot-check findings (visual): burnt-breaker close-ups (great for repair pages), PVC-conduit rough-ins (good), plus non-electrical strays (e.g. skid-steer in a pool) and construction-context shots (tape measure on rebar) that should be **rejected at review**, not published.

## 3. Website content this unlocks

**a) Repair pages with zero photos (highest value).** `burning-smell-panel.html`,
`breaker-tripping.html`, `federal-pacific-zinsco-panel-replacement.html`, and
`subpanel-installation.html` have no `inline-project-photo`/`photo-grid` blocks.
The archive's burnt-breaker / old-panel close-ups (e.g. `organized/20170619/`)
are a direct fit — 1 captioned before/after or damage close-up per page via the
`add-page-photos.py` pattern (`make_photo_block` + `photo-grid cols-3`).

**b) Gallery growth.** Review → append draft rows to `photo-manifest.csv` → run
`process-photos.py` → `auto-caption.py` → `update-gallery.py`. Note
`process-photos.py` resolves `SRC / source_file` against the flat
`/home/amram/Pictures/Electric Work/` root, so `organized/<day>/<file>` sources
need to be visible there (copy or symlink by basename) before processing.

**c) Location freshness.** Draft rows have empty `city`. Assign the job city at
review time — that is what feeds gallery filters, `gallery-{city}.html` pages,
and the `city, CA · year` overlays.

**d) GBP + blog fuel.** Panel/burner close-ups → "signs you need a panel upgrade"
GBP posts and `breaker-tripping`/`burning-smell` blog cross-links. Rough-in and
conduit sets → new-construction / ADU content. Reject lifestyle-irrelevant
strays; keep the 4:3 EXIF-stripped pipeline output as the only publishable form.

## 4. Privacy gate (blocking)

AGENTS.md rule: no visible street number/address, customer name, identifiable
face (unless consenting team member), or LADWP account number. Every draft photo
must pass a visual check; use `custom_crop` or `scripts/redact-photos.py`
(`blur_box`/`blackout_box`) before it enters the manifest.

## 5. Getting (more) Google Photos in

Already-imported sources (do not re-add): `Photos-website/Electric Work/`
(1,933 files) and `Upgrade Electrical Panel Winnetka/` are fully in the DB.
`Electric Work-3-001Pic.zip` (3.6 GB, 1,528 files, extracted 2026-10-14) held
**0 new files** — every basename was already in the DB, so it was not imported.
`Photos.zip` (190 MB) is mostly WhatsApp videos — skipped unless you want video.

For future sets:
1. In Google Photos (logged in as the library owner): select the "electric"
   search results → ⋮ → Download, or for the full set use Google Takeout
   (takeout.google.com → Photos only → export).
2. Unzip into `/home/amram/Pictures/Electric Work/organized/<YYYYMMDD>/`
   (one folder per shoot day; any name matching `YYYYMMDD` works).
3. Run `python3 scripts/scan-organized-photos.py` — new files appear in
   `data/new-photos-draft.csv` automatically.
4. Review images → fill category/caption/city → append to
   `scripts/photo-manifest.csv` → process → gallery → deploy.
