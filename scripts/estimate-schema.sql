-- AMY Electric estimate database — SQLite / Cloudflare D1 compatible.
-- Mirrors js/src/05-estimate-data.js table for table. The JS `appliesTo`
-- arrays are the denormalized view of service_adders below.
-- Apply: sqlite3 db/estimate.sqlite < scripts/estimate-schema.sql
-- D1:    npx wrangler d1 execute amyelectric_db --remote --file=scripts/estimate-schema.sql

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS estimate_services (
  id        TEXT PRIMARY KEY,
  name      TEXT NOT NULL,
  unit      TEXT NOT NULL,
  base_low  INTEGER NOT NULL,
  base_high INTEGER NOT NULL,
  permit_id TEXT REFERENCES estimate_permits(id),
  source    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimate_permits (
  id     TEXT PRIMARY KEY,
  name   TEXT NOT NULL,
  low    INTEGER NOT NULL,
  high   INTEGER NOT NULL,
  source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimate_materials (
  id        TEXT PRIMARY KEY,
  name      TEXT NOT NULL,
  unit      TEXT NOT NULL,
  unit_low  INTEGER,
  unit_high INTEGER,
  status    TEXT NOT NULL CHECK (status IN ('published', 'pending-vendor')),
  source    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimate_adders (
  id     TEXT PRIMARY KEY,
  name   TEXT NOT NULL,
  low    INTEGER NOT NULL,
  high   INTEGER NOT NULL,
  source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimate_service_adders (
  service_id TEXT NOT NULL REFERENCES estimate_services(id) ON UPDATE CASCADE,
  adder_id   TEXT NOT NULL REFERENCES estimate_adders(id) ON UPDATE CASCADE,
  PRIMARY KEY (service_id, adder_id)
);

CREATE TABLE IF NOT EXISTS estimate_size_tiers (
  id         TEXT PRIMARY KEY,
  service_id TEXT NOT NULL REFERENCES estimate_services(id) ON UPDATE CASCADE,
  min_sqft   INTEGER NOT NULL,
  max_sqft   INTEGER,
  low        INTEGER NOT NULL,
  high       INTEGER NOT NULL,
  label      TEXT NOT NULL,
  source     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimate_credits (
  id     TEXT PRIMARY KEY,
  name   TEXT NOT NULL,
  kind   TEXT NOT NULL CHECK (kind IN ('fixed-up-to', 'percent')),
  amount INTEGER NOT NULL,
  source TEXT NOT NULL,
  note   TEXT NOT NULL
);

-- Seeds mirror 05-estimate-data.js v1.0.0 exactly.
INSERT OR REPLACE INTO estimate_permits (id, name, low, high, source) VALUES
  ('permit-ev', 'EV Charger Permit Fees', 150, 400, 'ev-charger-installation.html');

INSERT OR REPLACE INTO estimate_services (id, name, unit, base_low, base_high, permit_id, source) VALUES
  ('panel-200a-replacement', '200A Panel Replacement', 'job', 2500, 4500, NULL, 'panel-upgrade.html, owner range decision 2026-10-08'),
  ('panel-main-service-upgrade', 'Main Service Upgrade', 'job', 3000, 6000, NULL, 'panel-upgrade.html'),
  ('panel-subpanel-add', 'Sub-Panel Add', 'job', 1200, 2500, NULL, 'panel-upgrade.html'),
  ('panel-100a-like-for-like', '100A Panel Replacement (like-for-like)', 'job', 1500, 2500, NULL, 'panel-100a-vs-200a.html'),
  ('ev-nema-1450', 'NEMA 14-50 Outlet Install', 'job', 350, 550, 'permit-ev', 'ev-charger-installation.html'),
  ('ev-tesla-wall', 'Tesla Wall Connector Install', 'job', 450, 750, 'permit-ev', 'ev-charger-installation.html'),
  ('ev-hardwired', 'Hardwired EVSE Install', 'job', 500, 900, 'permit-ev', 'ev-charger-installation.html'),
  ('ev-fleet-station', 'Commercial EV Fleet Station', 'station', 1500, 6000, NULL, 'commercial-ev-fleet-charging.html'),
  ('lighting-per-light', 'Recessed Lighting', 'light', 125, 250, NULL, 'llms.txt'),
  ('rewiring-base', 'Whole-Home Rewiring', 'job', 8000, 18000, NULL, 'whole-home-rewiring.html, llms.txt'),
  ('rewiring-partial', 'Partial Rewiring / Remediation', 'job', 800, 3000, NULL, 'whole-home-rewiring.html'),
  ('rewiring-per-circuit', 'Rewire (per circuit)', 'circuit', 300, 600, NULL, 'whole-home-rewiring.html'),
  ('generator-transfer-switch', 'Automatic Transfer Switch Install', 'job', 800, 1500, NULL, 'generator-transfer-switch.html'),
  ('generator-manual-switch', 'Manual Transfer Switch Install', 'job', 400, 800, NULL, 'generator-transfer-switch.html');

INSERT OR REPLACE INTO estimate_size_tiers (id, service_id, min_sqft, max_sqft, low, high, label, source) VALUES
  ('rewiring-small', 'rewiring-base', 0, 1200, 3000, 7000, 'Small home (1-2 BR, ~1,000 sq ft)', 'whole-home-rewiring.html'),
  ('rewiring-medium', 'rewiring-base', 1201, 1750, 6000, 12000, 'Medium home (3 BR, ~1,500 sq ft)', 'whole-home-rewiring.html'),
  ('rewiring-large', 'rewiring-base', 1751, NULL, 10000, 15000, 'Large home (4+ BR, 2,000+ sq ft)', 'whole-home-rewiring.html');

INSERT OR REPLACE INTO estimate_materials (id, name, unit, unit_low, unit_high, status, source) VALUES
  ('permit-ev', 'EV Permit Fees', 'job', 150, 400, 'published', 'ev-charger-installation.html'),
  ('evse-unit', 'Level 2 Charger Unit', 'unit', 400, 750, 'published', 'ev-charger-installation geo pages'),
  ('panel-200a-equipment', '200A Panel + Main Breaker Equipment', 'job', NULL, NULL, 'pending-vendor', ''),
  ('branch-breaker-2p', '2-Pole Branch Breaker', 'breaker', NULL, NULL, 'pending-vendor', ''),
  ('wire-thhn-per-ft', 'THHN Wire + Conduit (per ft installed run)', 'ft', NULL, NULL, 'pending-vendor', '');

INSERT OR REPLACE INTO estimate_adders (id, name, low, high, source) VALUES
  ('adder-ev-panel-upgrade', 'Panel Upgrade with EV Install', 2500, 4500, 'ev-charger-installation.html'),
  ('adder-trenching', 'Trenching for Underground Service', 800, 2500, 'panel-upgrade.html'),
  ('adder-service-mast', 'Service Mast / Weatherhead Replacement', 200, 600, 'panel-upgrade.html'),
  ('adder-grounding', 'Grounding Electrodes (code-required)', 200, 500, 'panel-upgrade.html'),
  ('adder-meter-socket', 'Meter Socket Replacement', 300, 700, 'panel-upgrade.html'),
  ('adder-distance-medium', 'Medium Wire Run (25-50 ft)', 100, 150, 'legacy estimator distAdjust'),
  ('adder-distance-long', 'Long Wire Run (50 ft+)', 200, 300, 'legacy estimator distAdjust');

INSERT OR REPLACE INTO estimate_service_adders (service_id, adder_id) VALUES
  ('ev-nema-1450', 'adder-ev-panel-upgrade'),
  ('ev-tesla-wall', 'adder-ev-panel-upgrade'),
  ('ev-hardwired', 'adder-ev-panel-upgrade'),
  ('panel-200a-replacement', 'adder-trenching'),
  ('panel-main-service-upgrade', 'adder-trenching'),
  ('ev-nema-1450', 'adder-trenching'),
  ('ev-tesla-wall', 'adder-trenching'),
  ('ev-hardwired', 'adder-trenching'),
  ('panel-200a-replacement', 'adder-service-mast'),
  ('panel-main-service-upgrade', 'adder-service-mast'),
  ('panel-200a-replacement', 'adder-grounding'),
  ('panel-main-service-upgrade', 'adder-grounding'),
  ('panel-200a-replacement', 'adder-meter-socket'),
  ('panel-main-service-upgrade', 'adder-meter-socket'),
  ('ev-nema-1450', 'adder-distance-medium'),
  ('ev-tesla-wall', 'adder-distance-medium'),
  ('ev-hardwired', 'adder-distance-medium'),
  ('ev-nema-1450', 'adder-distance-long'),
  ('ev-tesla-wall', 'adder-distance-long'),
  ('ev-hardwired', 'adder-distance-long');

INSERT OR REPLACE INTO estimate_credits (id, name, kind, amount, source, note) VALUES
  ('credit-ladwp-ev', 'LADWP EV Rebate', 'fixed-up-to', 500, 'ev-charger-installation.html', 'Residential customers; informational only, not subtracted from totals.'),
  ('credit-fed-30c', 'Federal Section 30C Tax Credit', 'percent', 30, 'ev-charger-installation.html', '30% of equipment cost; informational only, not subtracted from totals.');
