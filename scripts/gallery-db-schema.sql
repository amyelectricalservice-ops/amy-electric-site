-- AMY Electric gallery database — SQLite / Cloudflare D1 compatible.
-- Rebuild with: python3 scripts/build-gallery-db.py
-- Apply with:  npx wrangler d1 execute amyelectric_db --remote --file=db/gallery-schema.sql
--              npx wrangler d1 execute amyelectric_db --remote --file=db/gallery-seed.sql
--
-- Category slugs and presentation colours mirror CATEGORY_LABELS in
-- scripts/update-gallery.py, which is what actually renders gallery.html.
-- The older gallery-pipeline/schema.sql used a different, unused category set
-- (ev-charger, panel-upgrade, ...) that the site never reads.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS gallery_categories (
  slug          TEXT PRIMARY KEY,
  label         TEXT NOT NULL,
  bg            TEXT NOT NULL,
  color         TEXT NOT NULL,
  display_order INTEGER NOT NULL DEFAULT 0
);

-- One row per published photo. `slug` is the join key to the on-disk filenames
-- (img/gallery/<slug>-{400,800,1200}w.{webp,jpg}).
CREATE TABLE IF NOT EXISTS gallery_images (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  slug          TEXT    NOT NULL UNIQUE,
  source_file   TEXT    NOT NULL,
  category      TEXT    NOT NULL REFERENCES gallery_categories(slug),
  caption       TEXT    NOT NULL,
  alt_text      TEXT    NOT NULL,
  city          TEXT    NOT NULL,
  shoot_year    INTEGER,
  width         INTEGER NOT NULL DEFAULT 1200,
  height        INTEGER NOT NULL DEFAULT 900,
  custom_crop   TEXT,
  display_order INTEGER NOT NULL DEFAULT 0,
  verified_at   TEXT    NOT NULL,
  FOREIGN KEY (category) REFERENCES gallery_categories(slug) ON UPDATE CASCADE
);

-- The four renditions emitted per photo by scripts/process-photos.py.
-- Recorded explicitly so a missing or empty file is detectable in SQL rather
-- than only as a 404 in a srcset.
CREATE TABLE IF NOT EXISTS gallery_image_variants (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  slug       TEXT    NOT NULL REFERENCES gallery_images(slug) ON DELETE CASCADE,
  variant    TEXT    NOT NULL CHECK (variant IN ('400w', '800w', '1200w')),
  format     TEXT    NOT NULL CHECK (format IN ('webp', 'jpg')),
  path       TEXT    NOT NULL,
  byte_size  INTEGER NOT NULL,
  width      INTEGER NOT NULL,
  height     INTEGER NOT NULL,
  UNIQUE (slug, variant, format)
);

CREATE INDEX IF NOT EXISTS idx_images_category      ON gallery_images(category);
CREATE INDEX IF NOT EXISTS idx_images_order         ON gallery_images(display_order);
CREATE INDEX IF NOT EXISTS idx_images_year          ON gallery_images(shoot_year);
CREATE INDEX IF NOT EXISTS idx_variants_slug        ON gallery_image_variants(slug);

INSERT OR IGNORE INTO gallery_categories (slug, label, bg, color, display_order) VALUES
  ('panel',            'Panel Upgrades',    'rgba(245,166,35,.2)', '#f5a623', 1),
  ('commercial',       'Commercial',         'rgba(74,144,217,.2)',  '#4a90d9', 2),
  ('new-construction', 'New Construction',   'rgba(126,200,80,.2)',  '#7ec850', 3),
  ('lighting',         'Lighting',           'rgba(232,123,156,.2)','#e87b9c', 4),
  ('team',             'Team',               'rgba(155,89,182,.2)',  '#9b59b6', 5),
  ('lifestyle',        'Lifestyle',          'rgba(230,126,34,.2)',  '#e67e22', 6),
  ('exterior',         'Exteriors',          'rgba(26,188,156,.2)',  '#1abc9c', 7),
  ('other',            'Equipment',          'rgba(149,165,166,.2)', '#95a5a6', 8);
