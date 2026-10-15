#!/usr/bin/env node
/* Tests for gbp-agent.js (stateless GBP posting cadence + payload).
 * Direct ESM import: root package.json is type:module and gbp-agent.js
 * touches no browser globals at import time.
 * Run: node --test scripts/test-gbp-agent.mjs
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  CALENDAR_START, CADENCE_DAYS, BOOK_URL,
  isPostingDay, pickPostIndex, getPost, buildLocalPost, handleScheduled,
} from '../gbp-agent.js';

const day = (s) => new Date(s + 'T12:00:00Z');

test('calendar starts 2026-10-21 on a 2-day cadence', () => {
  assert.equal(CALENDAR_START, '2026-10-21');
  assert.equal(CADENCE_DAYS, 2);
});

test('posting days are every other day from start', () => {
  assert.equal(isPostingDay(day('2026-10-21')), true);  // POST 1
  assert.equal(isPostingDay(day('2026-10-22')), false);
  assert.equal(isPostingDay(day('2026-10-23')), true);  // POST 2
  assert.equal(isPostingDay(day('2026-12-18')), true);  // POST 30
  assert.equal(isPostingDay(day('2026-12-19')), false);
});

test('index maps to the calendar order and wraps after 30', () => {
  assert.equal(pickPostIndex(day('2026-10-21')), 0);
  assert.equal(pickPostIndex(day('2026-10-23')), 1);
  assert.equal(pickPostIndex(day('2026-10-22')), -1); // not a posting day
  assert.equal(pickPostIndex(day('2026-10-20')), -1); // before start
  // 30 posts × 2 days = 60-day rotation; day 60 wraps to index 0
  assert.equal(pickPostIndex(day('2026-12-20')), 0);
  assert.equal(getPost(0).n, 1);
  assert.equal(getPost(29).n, 30);
  assert.equal(getPost(30), null);
});

test('LocalPost payload fits GBP limits with booking CTA', () => {
  const payload = buildLocalPost(getPost(0));
  assert.equal(payload.topicType, 'STANDARD');
  assert.equal(payload.languageCode, 'en-US');
  assert.ok(payload.summary.length <= 1500, `summary ${payload.summary.length} chars`);
  assert.equal(payload.callToAction.actionType, 'LEARN_MORE');
  assert.equal(payload.callToAction.url, BOOK_URL);
});

test('handler skips quietly without secrets, dry-runs without posting', async () => {
  const skipped = await handleScheduled({}, day('2026-10-21'));
  assert.equal(skipped.status, 'skipped_no_secrets');
  assert.ok(skipped.missing.includes('GBP_REFRESH_TOKEN'));

  const env = {
    GBP_CLIENT_ID: 'x', GBP_CLIENT_SECRET: 'x', GBP_REFRESH_TOKEN: 'x',
    GBP_ACCOUNT_ID: 'x', GBP_LOCATION_ID: 'x', GBP_DRY_RUN: '1',
  };
  const off = await handleScheduled(env, day('2026-10-22'));
  assert.equal(off.status, 'skipped_not_posting_day');
  const dry = await handleScheduled(env, day('2026-10-21'));
  assert.equal(dry.status, 'dry_run');
  assert.equal(dry.post, 1);
});
