-- AMY Electric — lead platform schema (D1)
-- Apply with:
--   npx wrangler d1 execute amy-electric-confirmed --remote --file=scripts/lead-schema.sql
-- Idempotent: safe to re-run.

CREATE TABLE IF NOT EXISTS leads (
  id                TEXT PRIMARY KEY,
  created_at        TEXT NOT NULL,
  updated_at        TEXT NOT NULL,
  -- contact
  name              TEXT NOT NULL,
  phone             TEXT NOT NULL,
  phone_norm        TEXT NOT NULL,
  email             TEXT,
  email_norm        TEXT,
  city              TEXT,
  -- request
  service           TEXT,
  request_type      TEXT,
  message           TEXT,
  estimate_json     TEXT,
  -- classification
  segment           TEXT NOT NULL DEFAULT 'residential',   -- residential | commercial
  urgency           TEXT NOT NULL DEFAULT 'standard',      -- emergency | same-day | standard | planning
  score             INTEGER NOT NULL DEFAULT 0,            -- 0-100
  score_reasons     TEXT,                                  -- JSON array
  -- attribution
  source_page       TEXT,
  referrer          TEXT,
  utm_source        TEXT,
  utm_medium        TEXT,
  utm_campaign      TEXT,
  utm_term          TEXT,
  utm_content       TEXT,
  gclid             TEXT,
  fbclid            TEXT,
  -- pipeline
  status            TEXT NOT NULL DEFAULT 'new',           -- new | contacted | qualified | quoted | won | lost | duplicate
  owner             TEXT,
  follow_up_at      TEXT,
  -- crm
  crm_provider      TEXT,
  crm_status        TEXT NOT NULL DEFAULT 'pending',       -- pending | synced | failed | skipped
  crm_contact_id    TEXT,
  crm_deal_id       TEXT,
  crm_task_id       TEXT,
  crm_error         TEXT,
  -- guards
  dedupe_key        TEXT NOT NULL,
  duplicate_of      TEXT,
  ip_hash           TEXT,
  user_agent        TEXT,
  turnstile_ok      INTEGER
);

CREATE INDEX IF NOT EXISTS idx_leads_created   ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_dedupe    ON leads(dedupe_key, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_status    ON leads(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_segment   ON leads(segment, created_at DESC);

-- Uploaded project photos / PDF plans. Objects live in R2 and are never
-- public: the key is random and downloads require the admin bearer token.
CREATE TABLE IF NOT EXISTS lead_files (
  id              TEXT PRIMARY KEY,
  upload_token    TEXT NOT NULL,
  lead_id         TEXT,
  created_at      TEXT NOT NULL,
  r2_key          TEXT NOT NULL,
  filename        TEXT NOT NULL,          -- sanitized display name
  content_type    TEXT NOT NULL,
  bytes           INTEGER NOT NULL,
  sha256          TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'pending',  -- pending | linked | deleted
  ip_hash         TEXT
);

CREATE INDEX IF NOT EXISTS idx_lead_files_token ON lead_files(upload_token);
CREATE INDEX IF NOT EXISTS idx_lead_files_lead  ON lead_files(lead_id);

-- Append-only funnel events, independent of Google Analytics.
CREATE TABLE IF NOT EXISTS lead_events (
  id          TEXT PRIMARY KEY,
  lead_id     TEXT,
  event       TEXT NOT NULL,
  label       TEXT,
  page        TEXT,
  meta        TEXT,
  created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lead_events_created ON lead_events(created_at DESC);

-- Paid-media spend, for cost-per-qualified-lead reporting (AE-038).
CREATE TABLE IF NOT EXISTS ad_spend (
  id            TEXT PRIMARY KEY,
  day           TEXT NOT NULL,            -- YYYY-MM-DD
  channel       TEXT NOT NULL,            -- google-ads | lsa | organic | referral
  campaign      TEXT NOT NULL,
  spend_cents   INTEGER NOT NULL DEFAULT 0,
  impressions   INTEGER NOT NULL DEFAULT 0,
  clicks        INTEGER NOT NULL DEFAULT 0,
  leads         INTEGER NOT NULL DEFAULT 0,
  qualified     INTEGER NOT NULL DEFAULT 0,
  notes         TEXT,
  created_at    TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_ad_spend_day ON ad_spend(day, channel, campaign);

-- Booked work and revenue (AE-045).
CREATE TABLE IF NOT EXISTS jobs (
  id            TEXT PRIMARY KEY,
  lead_id       TEXT,
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'quoted',  -- quoted | scheduled | completed | cancelled
  service       TEXT,
  quoted_cents  INTEGER NOT NULL DEFAULT 0,
  revenue_cents INTEGER NOT NULL DEFAULT 0,
  scheduled_at  TEXT,
  completed_at  TEXT,
  notes         TEXT
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status, created_at DESC);

-- Commercial prospect database (AE-036) and permit-monitor opportunities
-- (AE-037). A prospect is a company/person we may sell to; a permit row is an
-- opportunity discovered from LADBS open data.
CREATE TABLE IF NOT EXISTS prospects (
  id              TEXT PRIMARY KEY,
  created_at      TEXT NOT NULL,
  updated_at      TEXT NOT NULL,
  company         TEXT,
  contact_name    TEXT,
  email           TEXT,
  phone           TEXT,
  city            TEXT,
  segment         TEXT NOT NULL DEFAULT 'general-contractor',
  source          TEXT NOT NULL DEFAULT 'manual',   -- manual | permit-monitor | referral | maps
  permit_ref      TEXT,
  project_address TEXT,
  zip             TEXT,
  project_type    TEXT,
  score           INTEGER NOT NULL DEFAULT 0,
  status          TEXT NOT NULL DEFAULT 'new',      -- new | contacted | qualified | won | lost
  notes           TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_prospects_permit ON prospects(source, permit_ref);
CREATE INDEX IF NOT EXISTS idx_prospects_status ON prospects(status, score DESC);
