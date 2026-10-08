/* AMY Electric — estimate data tables (05-estimate-data.js).
 *
 * Every row carries a `source` naming the site page (or decision) its numbers
 * come from. Rows with unitLow null are PLACEHOLDERS for vendor-quoted parts:
 * the engine must surface them as exclusions, never price them at zero.
 *
 * RELATIONAL MAP — this file is the denormalized view of scripts/estimate-schema.sql:
 *   services(id PK, name, unit, base_low, base_high, permit_id FK NULL, source)
 *   materials(id PK, name, unit, unit_low NULL, unit_high NULL, status, source)
 *   adders(id PK, name, low, high, source)
 *   service_adders(service_id FK, adder_id FK)  -- the appliesTo arrays, normalized
 *   size_tiers(id PK, service_id FK, min_sqft, max_sqft NULL, low, high, label, source)
 *   permits(id PK, name, low, high, source)
 *   credits(id PK, name, kind, amount, source, note)
 * scripts/test-estimate-engine.mjs asserts the JS tables and the SQL seed agree.
 */

var AMY_ESTIMATE_DATA = (function () {
  'use strict';

  var SERVICES = [
    { id: 'panel-200a-replacement', name: '200A Panel Replacement', unit: 'job', baseLow: 2500, baseHigh: 4500, permitId: null, source: 'panel-upgrade.html, owner range decision 2026-10-08' },
    { id: 'panel-main-service-upgrade', name: 'Main Service Upgrade', unit: 'job', baseLow: 3000, baseHigh: 6000, permitId: null, source: 'panel-upgrade.html' },
    { id: 'panel-subpanel-add', name: 'Sub-Panel Add', unit: 'job', baseLow: 1200, baseHigh: 2500, permitId: null, source: 'panel-upgrade.html' },
    { id: 'panel-100a-like-for-like', name: '100A Panel Replacement (like-for-like)', unit: 'job', baseLow: 1500, baseHigh: 2500, permitId: null, source: 'panel-100a-vs-200a.html' },
    { id: 'ev-nema-1450', name: 'NEMA 14-50 Outlet Install', unit: 'job', baseLow: 350, baseHigh: 550, permitId: 'permit-ev', source: 'ev-charger-installation.html' },
    { id: 'ev-tesla-wall', name: 'Tesla Wall Connector Install', unit: 'job', baseLow: 450, baseHigh: 750, permitId: 'permit-ev', source: 'ev-charger-installation.html' },
    { id: 'ev-hardwired', name: 'Hardwired EVSE Install', unit: 'job', baseLow: 500, baseHigh: 900, permitId: 'permit-ev', source: 'ev-charger-installation.html' },
    { id: 'ev-fleet-station', name: 'Commercial EV Fleet Station', unit: 'station', baseLow: 1500, baseHigh: 6000, permitId: null, source: 'commercial-ev-fleet-charging.html' },
    { id: 'lighting-per-light', name: 'Recessed Lighting', unit: 'light', baseLow: 125, baseHigh: 250, permitId: null, source: 'llms.txt' },
    { id: 'rewiring-base', name: 'Whole-Home Rewiring', unit: 'job', baseLow: 8000, baseHigh: 18000, permitId: null, source: 'whole-home-rewiring.html, llms.txt' },
    { id: 'rewiring-partial', name: 'Partial Rewiring / Remediation', unit: 'job', baseLow: 800, baseHigh: 3000, permitId: null, source: 'whole-home-rewiring.html' },
    { id: 'rewiring-per-circuit', name: 'Rewire (per circuit)', unit: 'circuit', baseLow: 300, baseHigh: 600, permitId: null, source: 'whole-home-rewiring.html' },
    { id: 'generator-transfer-switch', name: 'Automatic Transfer Switch Install', unit: 'job', baseLow: 800, baseHigh: 1500, permitId: null, source: 'generator-transfer-switch.html' },
    { id: 'generator-manual-switch', name: 'Manual Transfer Switch Install', unit: 'job', baseLow: 400, baseHigh: 800, permitId: null, source: 'generator-transfer-switch.html' }
  ];

  var SIZE_TIERS = [
    { id: 'rewiring-small', serviceId: 'rewiring-base', minSqft: 0, maxSqft: 1200, low: 3000, high: 7000, label: 'Small home (1-2 BR, ~1,000 sq ft)', source: 'whole-home-rewiring.html' },
    { id: 'rewiring-medium', serviceId: 'rewiring-base', minSqft: 1201, maxSqft: 1750, low: 6000, high: 12000, label: 'Medium home (3 BR, ~1,500 sq ft)', source: 'whole-home-rewiring.html' },
    { id: 'rewiring-large', serviceId: 'rewiring-base', minSqft: 1751, maxSqft: null, low: 10000, high: 15000, label: 'Large home (4+ BR, 2,000+ sq ft)', source: 'whole-home-rewiring.html' }
  ];

  var MATERIALS = [
    { id: 'permit-ev', name: 'EV Permit Fees', unit: 'job', unitLow: 150, unitHigh: 400, status: 'published', source: 'ev-charger-installation.html' },
    { id: 'evse-unit', name: 'Level 2 Charger Unit', unit: 'unit', unitLow: 400, unitHigh: 750, status: 'published', source: 'ev-charger-installation geo pages' },
    { id: 'panel-200a-equipment', name: '200A Panel + Main Breaker Equipment', unit: 'job', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' },
    { id: 'branch-breaker-2p', name: '2-Pole Branch Breaker', unit: 'breaker', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' },
    { id: 'wire-thhn-per-ft', name: 'THHN Wire + Conduit (per ft installed run)', unit: 'ft', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' }
  ];

  var ADDERS = [
    { id: 'adder-ev-panel-upgrade', name: 'Panel Upgrade with EV Install', low: 2500, high: 4500, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'ev-charger-installation.html' },
    { id: 'adder-trenching', name: 'Trenching for Underground Service', low: 800, high: 2500, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade', 'ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'panel-upgrade.html' },
    { id: 'adder-service-mast', name: 'Service Mast / Weatherhead Replacement', low: 200, high: 600, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-grounding', name: 'Grounding Electrodes (code-required)', low: 200, high: 500, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-meter-socket', name: 'Meter Socket Replacement', low: 300, high: 700, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-distance-medium', name: 'Medium Wire Run (25-50 ft)', low: 100, high: 150, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'legacy estimator distAdjust' },
    { id: 'adder-distance-long', name: 'Long Wire Run (50 ft+)', low: 200, high: 300, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'legacy estimator distAdjust' }
  ];

  var PERMITS = [
    { id: 'permit-ev', name: 'EV Charger Permit Fees', low: 150, high: 400, source: 'ev-charger-installation.html' }
  ];

  var CREDITS = [
    { id: 'credit-ladwp-ev', name: 'LADWP EV Rebate', kind: 'fixed-up-to', amount: 500, source: 'ev-charger-installation.html', note: 'Residential customers; informational only, not subtracted from totals.' },
    { id: 'credit-fed-30c', name: 'Federal Section 30C Tax Credit', kind: 'percent', amount: 30, source: 'ev-charger-installation.html', note: '30% of equipment cost; informational only, not subtracted from totals.' }
  ];

  return {
    VERSION: '1.0.0',
    SERVICES: SERVICES,
    SIZE_TIERS: SIZE_TIERS,
    MATERIALS: MATERIALS,
    ADDERS: ADDERS,
    PERMITS: PERMITS,
    CREDITS: CREDITS
  };
})();
