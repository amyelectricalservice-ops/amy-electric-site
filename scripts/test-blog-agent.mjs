#!/usr/bin/env node
/* Tests for scripts/blog-agent.py.
 * Run: node --test scripts/test-blog-agent.mjs
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

test('blog-agent --context returns business credentials and LA context', () => {
  const out = execSync('python3 scripts/blog-agent.py --context', { cwd: root, encoding: 'utf8' });
  assert.match(out, /AMY Electric/);
  assert.match(out, /C-10 License #981578/);
  assert.match(out, /EVITP #4051604/);
  assert.match(out, /\(818\) 302-5614/);
  assert.match(out, /LADWP/);
});

test('blog-agent --audit scans blog directory and reports scores', () => {
  const out = execSync('python3 scripts/blog-agent.py --audit', { cwd: root, encoding: 'utf8' });
  assert.match(out, /BLOG LEAD CONVERSION AUDIT/);
  assert.match(out, /Score/);
  assert.match(out, /\.html/);
});

test('blog-agent --brief generates structured blog brief', () => {
  const out = execSync('python3 scripts/blog-agent.py --brief "panel upgrade"', { cwd: root, encoding: 'utf8' });
  assert.match(out, /BLOG CONTENT BRIEF: panel upgrade/);
  assert.match(out, /target_audience/);
  assert.match(out, /conversion_elements/);
  assert.match(out, /suggested_faqs/);
});
