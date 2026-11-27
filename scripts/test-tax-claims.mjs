#!/usr/bin/env node
/* Guard: no production page may advertise an expired federal energy credit.
 *
 * Public Law 119-21 (OBBB, 2025-07-04) accelerated these terminations:
 *   25C  energy-efficient home improvement  ... placed in service after 2025-12-31
 *   25D  residential clean energy           ... expenditures after 2025-12-31
 *   25E  previously-owned clean vehicle     ... acquired after 2025-09-30
 *   30C  alternative-fuel refueling         ... placed in service after 2026-06-30
 *   30D  new clean vehicle                  ... acquired after 2025-09-30
 *   179D commercial buildings deduction     ... construction begins after 2026-06-30
 * See the IRS OBBB credit FAQ. Historical mentions are fine when they say the
 * credit ended; a live claim ("30 percent federal credit", "you may qualify")
 * is not.
 *
 * Run: node --test scripts/test-tax-claims.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

function collect(rel = '') {
  const files = [];
  for (const entry of readdirSync(join(ROOT, rel))) {
    const r = rel ? `${rel}/${entry}` : entry;
    const abs = join(ROOT, r);
    if (statSync(abs).isDirectory()) files.push(...collect(r));
    else if (/\.(html|js)$/.test(entry) && !entry.includes('.min.')) files.push(r);
  }
  return files;
}

const FILES = [
  ...collect().filter(f => !f.includes('/') && f.endsWith('.html')),
  ...collect('blog'),
  ...collect('case-studies'),
  ...collect('js/src'),
  'worker.js',
];

const CLAIM = /\b(?:federal|irs|inflation reduction act)\b[^$<]{0,90}?\b(?:credits?|deductions?|incentives?)\b|\b(?:30\s*percent|30\s*%)[^<]{0,40}?\b(?:credits?|incentives?)\b|\b(?:25C|25D|25E|30C|30D|179D)\b/gi;
const EXPIRED = /ended|expired|no longer|used to|repeal|terminated|sunset|after June 30, 2026|after December 31, 2025|after September 30, 2025|historical|not available/i;
// The estimate data table carries a legacy 30C row that is never subtracted
// from totals and never rendered to a visitor (see test-estimate-engine.mjs).
// It is data, not a claim on a page — don't rebuild every JS bundle for it.
const DORMANT_DATA_ROW = /informational only, not subtracted from totals/i;

function liveClaims(text) {
  const hits = [];
  for (const m of text.matchAll(CLAIM)) {
    const window = text.slice(Math.max(0, m.index - 350), m.index + m[0].length + 350);
    if (EXPIRED.test(window) || DORMANT_DATA_ROW.test(window)) continue;
    hits.push(text.slice(Math.max(0, m.index - 60), m.index + m[0].length + 100).replace(/\s+/g, ' '));
  }
  return hits;
}

describe('expired federal energy credits', () => {
  it('finds at least one historical, clearly-expired mention', () => {
    // Keeps the detector honest — an empty-match regex would pass vacuously.
    const found = FILES.some(f => /30C|25C|179D/i.test(readFileSync(join(ROOT, f), 'utf8')));
    assert.ok(found, 'expected at least one historical credit mention in the repo');
  });

  it('does not advertise an expired credit as available', () => {
    const failures = [];
    for (const file of FILES) {
      const hits = liveClaims(readFileSync(join(ROOT, file), 'utf8'));
      if (hits.length) failures.push(`${file}: ${hits.slice(0, 2).join(' | ')}`);
    }
    assert.deepEqual(failures, [], `live credit claims found:\n${failures.join('\n')}`);
  });

  it('detects a synthetic live claim', () => {
    assert.ok(
      liveClaims('The federal tax credit offers up to $7,500 for new EVs.').length > 0,
      'detector must flag a live-looking claim'
    );
    assert.equal(
      liveClaims('The federal tax credit ended for vehicles acquired after September 30, 2025.').length,
      0,
      'detector must accept an expired claim'
    );
  });
});
