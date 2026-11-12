#!/usr/bin/env node
/* Tests for the lead platform: scoring, de-dupe keys, file validation and
 * admin auth. Uses in-memory stubs — no network, no real D1/R2, no secrets.
 * Run: node --test scripts/test-lead-platform.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  scoreLead, normalizePhone, normalizeEmail, buildLead, sha256Hex,
} from '../lead-store.js';
import { handleLeadFiles, isAdmin, draftEstimate } from '../crm-handler.js';

function stubDb({ duplicate = null } = {}) {
  const writes = [];
  return {
    writes,
    prepare(sql) {
      const stmt = {
        _args: [],
        bind(...args) { this._args = args; return this; },
        async first() {
          if (/SELECT COUNT\(\*\) AS n FROM lead_files/.test(sql)) return { n: 0 };
          if (/FROM leads/.test(sql)) return duplicate;
          return null;
        },
        async run() {
          writes.push({ sql: sql.replace(/\s+/g, ' ').trim(), args: this._args });
          return { meta: { changes: 1 } };
        },
        async all() { return { results: [] }; },
      };
      return stmt;
    },
  };
}

function stubR2() {
  const puts = [];
  return {
    puts,
    async put(key, body, opts) { puts.push({ key, size: body.length, opts }); },
    async get() { return null; },
  };
}

const JPEG = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10, 0x4a, 0x46]);
const PDF = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x37]);

describe('lead scoring', () => {
  it('emergency language outranks a planning enquiry', () => {
    const emergency = scoreLead({
      service: 'electrical-repair', message: 'Outlet is sparking and there is a burning smell',
      phone: '8183025614', city: 'Burbank', email: 'a@b.com',
    });
    const planning = scoreLead({
      service: 'lighting', message: 'Thinking about a remodel next month',
      phone: '8183025614', city: 'Burbank',
    });
    assert.equal(emergency.urgency, 'emergency');
    assert.equal(planning.urgency, 'planning');
    assert.ok(emergency.score > planning.score + 20);
  });

  it('classifies commercial enquiries from text', () => {
    const r = scoreLead({ service: 'panel-upgrade', message: 'We need a 400A service for our restaurant tenant improvement' });
    assert.equal(r.segment, 'commercial');
  });

  it('always returns a bounded integer score with reasons', () => {
    const r = scoreLead({ service: 'commercial', message: 'emergency asap gclid', email: 'x@y.z', city: 'LA', hasFiles: true, hasEstimate: true, gclid: 'abc', phone: '8185551234' });
    assert.ok(Number.isInteger(r.score));
    assert.ok(r.score >= 0 && r.score <= 100);
    assert.ok(Array.isArray(r.reasons) && r.reasons.length > 0);
  });
});

describe('normalisation', () => {
  it('reduces phone numbers to 10 digits', () => {
    assert.equal(normalizePhone('+1 (818) 302-5614'), '8183025614');
    assert.equal(normalizePhone('818.302.5614'), '8183025614');
  });
  it('lowercases email', () => {
    assert.equal(normalizeEmail('  Info@AMYelectric.com '), 'info@amyelectric.com');
  });
  it('hashes deterministically', async () => {
    assert.equal(await sha256Hex('abc'), await sha256Hex('abc'));
    assert.equal((await sha256Hex('abc')).length, 64);
  });
});

describe('lead record', () => {
  it('builds a dedupe key from the phone and keeps attribution', async () => {
    const lead = await buildLead(
      { name: 'Test User', phone: '(818) 302-5614', email: 'T@Example.com', service: 'panel-upgrade', message: 'panel is hot and tripping', city: 'Encino' },
      { source_page: '/panel-upgrade', utm_source: 'google', gclid: 'abc123', ip: '1.2.3.4' },
    );
    assert.equal(lead.dedupe_key, '8183025614');
    assert.equal(lead.email_norm, 't@example.com');
    assert.equal(lead.urgency, 'emergency');
    assert.equal(lead.utm_source, 'google');
    assert.equal(lead.gclid, 'abc123');
    assert.equal(lead.ip_hash.length, 64);
    assert.ok(JSON.parse(lead.score_reasons).length > 0);
  });
});

describe('file uploads', () => {
  function formRequest(bytes, name, type, token = 'abcdefghijklmnop1234') {
    const fd = new FormData();
    fd.append('file', new File([bytes], name, { type }));
    fd.append('upload_token', token);
    return new Request('https://amyelectric.com/api/lead-files', { method: 'POST', body: fd });
  }

  it('accepts a JPEG and stores it under a random private key', async () => {
    const env = { CRM_DB: stubDb(), LEAD_FILES: stubR2() };
    const res = await handleLeadFiles(formRequest(JPEG, 'panel photo.jpg', 'image/jpeg'), env, () => {});
    const body = await res.json();
    assert.equal(res.status, 200);
    assert.equal(body.success, true);
    assert.equal(body.file.type, 'image/jpeg');
    assert.match(body.file.id, /^file_[a-f0-9]+$/);
    assert.match(env.LEAD_FILES.puts[0].key, /^leads\/\d{4}-\d{2}-\d{2}\/abcdefghijklmnop1234\/file_/);
    assert.equal(env.LEAD_FILES.puts[0].opts.httpMetadata.cacheControl, 'private, no-store');
  });

  it('accepts a PDF plan set', async () => {
    const env = { CRM_DB: stubDb(), LEAD_FILES: stubR2() };
    const res = await handleLeadFiles(formRequest(PDF, 'plans.pdf', 'application/pdf'), env, () => {});
    assert.equal(res.status, 200);
  });

  it('rejects a disguised text file by its bytes', async () => {
    const env = { CRM_DB: stubDb(), LEAD_FILES: stubR2() };
    const res = await handleLeadFiles(
      formRequest(new TextEncoder().encode('<script>alert(1)</script>'), 'evil.jpg', 'image/jpeg'), env, () => {});
    assert.equal(res.status, 415);
    assert.equal(env.LEAD_FILES.puts.length, 0);
  });

  it('rejects a missing upload session token', async () => {
    const env = { CRM_DB: stubDb(), LEAD_FILES: stubR2() };
    const res = await handleLeadFiles(formRequest(JPEG, 'a.jpg', 'image/jpeg', 'x'), env, () => {});
    assert.equal(res.status, 400);
  });

  it('rejects files over 10 MB', async () => {
    const env = { CRM_DB: stubDb(), LEAD_FILES: stubR2() };
    const big = new Uint8Array(11 * 1024 * 1024);
    big.set(JPEG, 0);
    const res = await handleLeadFiles(formRequest(big, 'big.jpg', 'image/jpeg'), env, () => {});
    assert.equal(res.status, 413);
  });

  it('returns 503 when no bucket is configured', async () => {
    const res = await handleLeadFiles(formRequest(JPEG, 'a.jpg', 'image/jpeg'), {}, () => {});
    assert.equal(res.status, 503);
  });
});

describe('admin auth', () => {
  it('accepts a matching bearer token and rejects others', () => {
    const env = { ADMIN_TOKEN: 'correct-horse-battery-staple' };
    const ok = new Request('https://amyelectric.com/api/admin/stats', {
      headers: { Authorization: 'Bearer correct-horse-battery-staple' },
    });
    const bad = new Request('https://amyelectric.com/api/admin/stats', {
      headers: { Authorization: 'Bearer nope' },
    });
    assert.equal(isAdmin(ok, env), true);
    assert.equal(isAdmin(bad, env), false);
    assert.equal(isAdmin(ok, {}), false);
  });
});

describe('draft estimate', () => {
  it('uses canonical ranges for a panel lead', () => {
    const e = draftEstimate({ service: 'panel-upgrade', message: 'need a permit for 200A panel' });
    assert.equal(e.rangeLow, 2500);
    assert.equal(e.rangeHigh, 4500);
    assert.ok(e.lines.join(' ').toLowerCase().includes('permit'));
    assert.equal(e.currency, 'USD');
  });
});

describe('D1 statement shape', () => {
  it('lead INSERT has one placeholder per column', async () => {
    const { readFileSync } = await import('node:fs');
    const src = readFileSync(new URL('../lead-store.js', import.meta.url), 'utf8');
    const m = src.match(/INSERT INTO leads \(([\s\S]*?)\) VALUES \(([\s\S]*?)\)`/);
    assert.ok(m, 'lead INSERT not found');
    const cols = m[1].split(',').map((c) => c.trim()).filter(Boolean);
    const marks = (m[2].match(/\?/g) || []).length;
    const literals = (m[2].match(/'[^']*'/g) || []).length;
    assert.equal(marks + literals, cols.length,
      `columns=${cols.length} placeholders=${marks} literals=${literals}`);
  });

  it('lead_files INSERT has one placeholder per column', async () => {
    const { readFileSync } = await import('node:fs');
    const src = readFileSync(new URL('../crm-handler.js', import.meta.url), 'utf8');
    const m = src.match(/INSERT INTO lead_files \(([\s\S]*?)\)\s*VALUES \(([\s\S]*?)\)`/);
    assert.ok(m, 'lead_files INSERT not found');
    const cols = m[1].split(',').map((c) => c.trim()).filter(Boolean);
    const marks = (m[2].match(/\?/g) || []).length;
    const literals = (m[2].match(/'[^']*'/g) || []).length;
    assert.equal(marks + literals, cols.length,
      `columns=${cols.length} placeholders=${marks} literals=${literals}`);
  });
});
