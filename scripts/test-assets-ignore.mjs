#!/usr/bin/env node
/* Guard: the ASSETS binding must not serve internal files.
 *
 * The ASSETS binding serves `directory: "."`, so every file in the repo is
 * public unless .assetsignore excludes it. Two leaks have already happened:
 *
 *   2026-11-14  worker.js and contact-handler.js were excluded but eleven other
 *               root modules were not — /crm-handler.js, /lead-store.js and
 *               friends served their full source (admin API shape, lead
 *               scoring, EspoCRM field mapping, GBP schedule).
 *   2026-11-15  .claude/, .gemini/, .vscode/, data/, markdown/, extensions/,
 *               wrangler.staging.jsonc and the root internal docs were all
 *               live (HTTP 200) — including data/photo-db.sqlite and
 *               wrangler.staging.jsonc with its D1 ids and bucket names.
 *
 * Both were found by hand. This test is the cheap version: it fails if any
 * tracked file that is not on the public allowlist would be uploaded.
 *
 * Run: node --test scripts/test-assets-ignore.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

/* Gitignore semantics, enough for .assetsignore:
 *   - a pattern ending in "/" matches that directory and everything under it
 *   - a pattern containing "/" is anchored at the repo root
 *   - a pattern without "/" matches any single path component
 *   - "*" does not cross "/", "**" does
 */
function compile(pattern) {
  const anchored = pattern.includes('/');
  const body = pattern.endsWith('/') ? pattern.slice(0, -1) : pattern;
  const rx = new RegExp(
    '^' +
      body
        .replace(/[.+^${}()|[\]\\]/g, '\\$&')
        .replace(/\*\*/g, '\u0000')
        .replace(/\*/g, '[^/]*')
        .replace(/\?/g, '[^/]')
        .replace(/\u0000/g, '.*') +
      '$'
  );
  return { rx, anchored, dir: pattern.endsWith('/') };
}

function patterns() {
  return readFileSync(join(ROOT, '.assetsignore'), 'utf8')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line && !line.startsWith('#'))
    .map(compile);
}

function isIgnored(file, pats) {
  const parts = file.split('/');
  return pats.some(p => {
    // "docs/" must match docs/ops/x.md, so test every ancestor directory.
    if (p.dir) {
      for (let i = 1; i < parts.length; i++) {
        if (p.rx.test(parts.slice(0, i).join('/'))) return true;
      }
      return false;
    }
    if (p.anchored) return p.rx.test(file);
    return parts.some(part => p.rx.test(part));
  });
}

function trackedFiles() {
  return execFileSync('git', ['ls-files', '-z'], { cwd: ROOT, encoding: 'utf8' })
    .split('\0')
    .filter(Boolean);
}

/* The only things that are meant to be reachable on the public site. */
const PUBLIC_DIRS = new Set([
  'img',
  'blog',
  'css',
  'js',
  'fonts',
  'case-studies',
  '.well-known',
]);

/* Root files that are deliberately served. Anything else at the root must be
 * ignored — that is where both leaks started. */
const PUBLIC_ROOT_FILES = new Set([
  'favicon.ico',
  'favicon.svg',
  'robots.txt',
  'sitemap.xml',
  'llms.txt',
  'llms-full.txt',
  'rsl.json',
  '_headers',
  '_redirects',
  'SECURITY.md',
  // IndexNow key files: the protocol requires them at /<key>.txt.
  '16076f14-4d06-4581-b281-38a7a89804ca.txt',
  'e73811d4fd18488f99e99987828567f9.txt',
]);

function publicFiles() {
  const pats = patterns();
  return trackedFiles().filter(file => !isIgnored(file, pats));
}

describe('assets exposure', () => {
  it('excludes every root-level Worker module from public assets', () => {
    const pats = patterns();
    const modules = trackedFiles().filter(f => !f.includes('/') && /\.(js|ts|mjs)$/.test(f));
    assert.ok(modules.length > 0, 'expected Worker modules at the repo root');

    const exposed = modules.filter(f => !isIgnored(f, pats));
    assert.deepEqual(exposed, [], `add to .assetsignore: ${exposed.join(', ')}`);
  });

  it('does not exclude the public site bundles', () => {
    const pats = patterns();
    for (const asset of ['js/site.min.js', 'js/estimator.min.js', 'css/style.min.css']) {
      assert.ok(!isIgnored(asset, pats), `${asset} must stay public`);
    }
  });

  it('serves nothing from an internal top-level directory', () => {
    const stray = publicFiles().filter(file => {
      const top = file.split('/')[0];
      return file.includes('/') && !PUBLIC_DIRS.has(top);
    });
    assert.deepEqual(stray, [], `internal directories are public: ${[...new Set(stray)].join(', ')}`);
  });

  it('serves no root file outside the public allowlist', () => {
    const stray = publicFiles()
      .filter(file => !file.includes('/'))
      .filter(file => !file.endsWith('.html') && !PUBLIC_ROOT_FILES.has(file));
    assert.deepEqual(stray, [], `unexpected public root files: ${stray.join(', ')}`);
  });

  it('ignores local secret files even though .gitignore already hides them', () => {
    const pats = patterns();
    for (const file of ['.dev.vars', '.dev.vars.production', '.env', '.env.local']) {
      assert.ok(isIgnored(file, pats), `${file} must be in .assetsignore`);
    }
  });

  it('ignores local tooling caches even though .gitignore already hides them', () => {
    const pats = patterns();
    const files = [
      '.ruff_cache/CACHEDIR.TAG',
      '.ruff_cache/0.15.9/12359970166167079670',
      '__pycache__/audit-site.cpython-312.pyc',
      '.pytest_cache/v/cache/lastfailed',
      '.mypy_cache/3.12/x.json',
      'lh-out/lh-1.json',
      '.server.log',
    ];
    const exposed = files.filter(file => !isIgnored(file, pats));
    assert.deepEqual(exposed, [], `add to .assetsignore: ${exposed.join(', ')}`);
  });
});