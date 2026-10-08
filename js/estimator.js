/* AMY Electric — project estimator (js/estimator.js).
 *
 * Standalone pure-logic module: no DOM, no network, no side effects.
 * Estimate a job from system parameters and return a structured JSON-ready
 * object with a price range, typical material lines, labor band, and a
 * city-permit flag. Priced numbers come only from published site content
 * (each row carries `source`); unpriced parts are explicit nulls surfaced
 * in `exclusions`, never silent zeros.
 *
 * Usage (browser): window.AMY_PROJECT_ESTIMATOR.estimateProject({...})
 * Usage (node):    const E = require('./js/estimator.js')
 *
 * Related: js/src/05-estimate-data.js + 06-estimate-engine.js (bundled
 * calculator) and scripts/estimate-schema.sql (relational mirror).
 * scripts/test-estimator.mjs asserts the shared values agree.
 */

(function (root, factory) {
  'use strict';
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = factory();
  } else {
    root.AMY_PROJECT_ESTIMATOR = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var VERSION = '1.0.0';

  var PROJECT_TYPES = ['panel-upgrade', 'ev-charger', 'subpanel-installation'];
  var AMPERAGES = ['100A', '200A'];

  // Installed base ranges. permitHandling: 'included' (range already covers
  // permit fees), 'separate' (permit fees publish separately and are added),
  // 'unpublished' (permit cost not published; flagged, never guessed).
  var BASE_RANGES = {
    'panel-upgrade': {
      '200A': { low: 2500, high: 4500, permitHandling: 'included', source: 'panel-upgrade.html, owner range 2026-10-08' },
      '100A': { low: 1500, high: 2500, permitHandling: 'included', source: 'panel-100a-vs-200a.html like-for-like' }
    },
    'ev-charger': {
      '200A': { low: 350, high: 900, permitHandling: 'separate', source: 'ev-charger-installation.html' },
      '100A': { low: 350, high: 900, permitHandling: 'separate', source: 'ev-charger-installation.html' }
    },
    'subpanel-installation': {
      '200A': { low: 1200, high: 2500, permitHandling: 'unpublished', source: 'panel-upgrade.html sub-panel row' },
      '100A': { low: 1200, high: 2500, permitHandling: 'unpublished', source: 'panel-upgrade.html sub-panel row' }
    }
  };

  // Typical bill of materials per project type. scope: 'included' (covered by
  // the installed range), 'customer-supplied' (bought separately, listed but
  // never totalled), 'vendor' (quoted per job, price unpublished).
  // qtyMayScaleWithDistance marks wire/conduit whose qty = linearDistanceFt.
  var BOMS = {
    'panel-upgrade': [
      { item: '200A panel + main breaker', qty: 1, unit: 'job', estLow: null, estHigh: null, scope: 'included', note: 'equipment vendor-quoted; covered by installed range' },
      { item: 'Branch breakers (as needed)', qty: 1, unit: 'lot', estLow: null, estHigh: null, scope: 'included', note: 'count varies by existing circuits; covered by installed range' },
      { item: 'Wire + conduit', qty: 'distance', unit: 'ft', estLow: null, estHigh: null, scope: 'included', note: 'run length from job walk; covered by installed range' }
    ],
    'ev-charger': [
      { item: 'Level 2 charger unit', qty: 1, unit: 'unit', estLow: 400, estHigh: 750, scope: 'customer-supplied', note: 'unit price separate from installation', source: 'ev-charger-installation geo pages' },
      { item: '40/50A branch breaker', qty: 1, unit: 'breaker', estLow: null, estHigh: null, scope: 'included', note: 'vendor-quoted; covered by installed range' },
      { item: 'Wire + conduit', qty: 'distance', unit: 'ft', estLow: null, estHigh: null, scope: 'included', note: 'run length from job walk; covered by installed range' }
    ],
    'subpanel-installation': [
      { item: 'Subpanel enclosure + feeder breaker', qty: 1, unit: 'job', estLow: null, estHigh: null, scope: 'included', note: 'equipment vendor-quoted; covered by installed range' },
      { item: 'Feeder wire + conduit', qty: 'distance', unit: 'ft', estLow: null, estHigh: null, scope: 'included', note: 'run length from job walk; covered by installed range' }
    ]
  };

  // Distance bands. Only EV carries a priced run adjustment (legacy
  // distAdjust precedent); elsewhere the band is informational.
  // Thresholds: straightforward installs sit within 25-50 ft of the panel.
  function distanceBand(ft) {
    if (ft <= 25) return { band: 'short', low: 0, high: 0 };
    if (ft <= 50) return { band: 'medium', low: 100, high: 150 };
    return { band: 'long', low: 200, high: 300 };
  }

  var PERMIT_EV = { low: 150, high: 400, source: 'ev-charger-installation.html' };

  function permitFor(projectType) {
    if (projectType === 'panel-upgrade') {
      return { required: true, note: 'LADBS permit + inspection included in range (panel-upgrade.html).' };
    }
    if (projectType === 'ev-charger') {
      return { required: true, note: 'Permit required for all new EV charger circuits in LA; fees separate, see materials.' };
    }
    return { required: true, note: 'New circuits require LADBS permit + inspection; fee unpublished for this scope.' };
  }

  function estimateProject(input) {
    if (!input || typeof input !== 'object') {
      throw new Error('estimator: input object with projectType, serviceAmperage, linearDistance is required');
    }
    var projectType = input.projectType;
    var serviceAmperage = input.serviceAmperage;
    var linearDistance = input.linearDistance;

    if (PROJECT_TYPES.indexOf(projectType) === -1) {
      throw new Error('estimator: unknown projectType ' + projectType + '; valid: ' + PROJECT_TYPES.join(', '));
    }
    if (AMPERAGES.indexOf(serviceAmperage) === -1) {
      throw new Error('estimator: unknown serviceAmperage ' + serviceAmperage + '; valid: ' + AMPERAGES.join(', '));
    }
    if (typeof linearDistance !== 'number' || !(linearDistance >= 0)) {
      throw new Error('estimator: linearDistance must be a non-negative number of feet');
    }

    var base = BASE_RANGES[projectType][serviceAmperage];
    var band = distanceBand(linearDistance);

    var materials = [];
    var exclusions = [];
    var bom = BOMS[projectType];
    for (var i = 0; i < bom.length; i++) {
      var m = bom[i];
      var qty = m.qty === 'distance' ? linearDistance : m.qty;
      var line = { item: m.item, qty: qty, unit: m.unit, estLow: m.estLow, estHigh: m.estHigh, scope: m.scope, note: m.note };
      if (m.source) line.source = m.source;
      materials.push(line);
      if (m.estLow === null) {
        exclusions.push({ item: m.item, reason: 'unit price unpublished; excluded from totals' });
      }
    }

    var permitLow = 0;
    var permitHigh = 0;
    if (base.permitHandling === 'separate') {
      permitLow = PERMIT_EV.low;
      permitHigh = PERMIT_EV.high;
      materials.push({ item: 'Permit fees', qty: 1, unit: 'job', estLow: permitLow, estHigh: permitHigh, scope: 'included', note: 'added to totals', source: 'ev-charger-installation.html' });
    } else if (base.permitHandling === 'unpublished') {
      exclusions.push({ item: 'Permit fees', reason: 'permit cost unpublished for this scope; excluded from totals' });
    }

    var distLow = 0;
    var distHigh = 0;
    var possibleAdders = [];
    if (projectType === 'ev-charger') {
      distLow = band.low;
      distHigh = band.high;
    }
    if (projectType === 'ev-charger' && serviceAmperage === '100A') {
      possibleAdders.push({ name: 'Panel upgrade with EV install', low: 2500, high: 4500, condition: 'if load calculation shows the 100A service cannot carry a dedicated 40/50A circuit', source: 'ev-charger-installation.html' });
    }
    if (projectType === 'panel-upgrade') {
      possibleAdders.push({ name: 'Trenching for underground service', low: 800, high: 2500, condition: 'underground service conversion only', source: 'panel-upgrade.html' });
    }

    var laborLow = base.low + distLow;
    var laborHigh = base.high + distHigh;
    var low = laborLow + permitLow;
    var high = laborHigh + permitHigh;

    var laborBasis = projectType === 'panel-upgrade' || projectType === 'subpanel-installation'
      ? 'installed work (equipment + licensed labor); equipment vendor-quoted per job'
      : 'installation labor + misc hardware; charger unit customer-supplied separately';

    return {
      version: VERSION,
      projectType: projectType,
      serviceAmperage: serviceAmperage,
      linearDistanceFt: linearDistance,
      distanceBand: band.band,
      priceRange: { low: low, high: high, currency: 'USD', basis: base.source },
      materials: materials,
      labor: { low: laborLow, high: laborHigh, basis: laborBasis },
      permit: permitFor(projectType),
      possibleAdders: possibleAdders,
      exclusions: exclusions
    };
  }

  return {
    VERSION: VERSION,
    PROJECT_TYPES: PROJECT_TYPES.slice(),
    AMPERAGES: AMPERAGES.slice(),
    estimateProject: estimateProject,
    distanceBand: distanceBand
  };
}));
