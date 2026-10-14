#!/usr/bin/env node
/* Tests for js/book.js (booking slot rules for book.html).
 * Standalone browser script: loaded via vm sandbox like test-estimator.mjs.
 * Run: node --test scripts/test-book.mjs
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function loadStandalone(path) {
  const code = readFileSync(join(root, path), 'utf8');
  const sb = { module: { exports: {} } };
  vm.createContext(sb);
  vm.runInContext(code + '\nthis.__M = module.exports;', sb, { filename: path });
  return sb.__M;
}

const BOOK = loadStandalone('js/book.js');

// Sundays closed, everything else bookable
test('Sundays are not bookable; Mon-Sat are', () => {
  const sun = new Date(2026, 9, 18); // a Sunday
  assert.equal(sun.getDay(), 0);
  assert.equal(BOOK.isBookableDay(sun), false);
  assert.deepEqual(JSON.parse(JSON.stringify(BOOK.windowsFor(sun))), []); // JSON: vm-realm arrays fail strict deepEqual
  for (let d = 1; d <= 6; d++) {
    const day = new Date(2026, 9, 18 + d);
    assert.equal(BOOK.isBookableDay(day), true, `weekday ${d}`);
  }
});

// Weekday vs Saturday windows mirror published office hours
test('weekday = 4 windows 8-16; Saturday = 2 windows 8-12', () => {
  const wed = new Date(2026, 9, 21);
  assert.deepEqual(JSON.parse(JSON.stringify(BOOK.windowsFor(wed))),
    [['08:00', '10:00'], ['10:00', '12:00'], ['12:00', '14:00'], ['14:00', '16:00']]);
  const sat = new Date(2026, 9, 24);
  assert.deepEqual(JSON.parse(JSON.stringify(BOOK.windowsFor(sat))), [['08:00', '10:00'], ['10:00', '12:00']]);
});

// Lead time: min tomorrow, max 60 days out
test('minDate is tomorrow at midnight; maxDate is +60 days', () => {
  const now = new Date();
  const min = BOOK.minDate();
  assert.equal(min.getHours(), 0);
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  assert.equal(Math.round((min - today) / 86400000), 1);
  const max = BOOK.maxDate();
  assert.equal(Math.round((max - min) / 86400000), BOOK.MAX_DAYS_AHEAD);
});

// Labels humans can read back on the phone
test('slotLabel formats date + window', () => {
  const wed = new Date(2026, 9, 21);
  assert.equal(BOOK.slotLabel(wed, ['08:00', '10:00']), 'Wed, Oct 21, 2026, 8:00 AM – 10:00 AM');
  assert.equal(BOOK.fmtWindow(['12:00', '14:00']), '12:00 PM – 2:00 PM');
});
