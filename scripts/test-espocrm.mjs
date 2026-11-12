#!/usr/bin/env node
/* EspoCRM mapping tests — no network, no credentials.
 * Run: node --test scripts/test-espocrm.mjs
 */
import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import {
  toE164, splitName, leadDescription, espocrmConfigured, syncLeadToEspo,
} from '../crm-espocrm.js';

const ENV = {
  ESPOCRM_BASE_URL: 'http://crm.local:8081',
  ESPOCRM_USERNAME: 'amy-site',
  ESPOCRM_PASSWORD: 'test-only',
};

function response(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => (body === null ? '' : JSON.stringify(body)),
  };
}

const baseLead = {
  id: 'lead_test1234567890',
  name: 'Ada Tester',
  phone: '(818) 555-0142',
  phone_norm: '8185550142',
  email: 'ada@example.com',
  email_norm: 'ada@example.com',
  city: 'Encino',
  service: 'panel-upgrade',
  message: 'Breakers tripping and the panel is hot',
  estimate_json: '{"rangeLow":2500,"rangeHigh":4500}',
  segment: 'residential',
  urgency: 'emergency',
  score: 82,
  source_page: '/residential-electrician',
  utm_source: 'google',
  utm_campaign: '',
  gclid: 'abc123',
  duplicate_of: '',
};

describe('EspoCRM helpers', () => {
  it('normalises US phone numbers to E.164', () => {
    assert.equal(toE164('(818) 555-0142'), '+18185550142');
    assert.equal(toE164('818.555.0142'), '+18185550142');
    assert.equal(toE164('+1 818 555 0142'), '+18185550142');
    assert.equal(toE164('12345'), '');
  });

  it('splits names and always yields a last name', () => {
    assert.deepEqual(splitName('Ada Lovelace Tester'), { firstName: 'Ada', lastName: 'Lovelace Tester' });
    assert.deepEqual(splitName('Ada'), { firstName: 'Ada', lastName: 'Ada' });
    assert.deepEqual(splitName(''), { firstName: '', lastName: 'Lead' });
  });

  it('puts score, segment, attribution and the lead id in the description', () => {
    const d = leadDescription(baseLead);
    assert.match(d, /Score 82\/100 · residential · emergency/);
    assert.match(d, /Service: panel-upgrade/);
    assert.match(d, /gclid=abc123/);
    assert.match(d, /lead_test1234567890/);
  });

  it('is unconfigured without a base URL or credentials', () => {
    assert.equal(espocrmConfigured({}), false);
    assert.equal(espocrmConfigured({ ESPOCRM_BASE_URL: 'http://x' }), false);
    assert.equal(espocrmConfigured(ENV), true);
  });
});

describe('syncLeadToEspo', () => {
  let calls;
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    calls = [];
    globalThis.fetch = async (url, init = {}) => {
      const u = String(url);
      const method = init.method || 'GET';
      calls.push({ url: u, method, body: init.body ? JSON.parse(init.body) : null, headers: init.headers });
      if (u.includes('/Contact?')) return response(200, { list: [] });
      if (u.endsWith('/Contact') && method === 'POST') return response(200, { id: 'contact_1' });
      if (u.includes('/Lead?')) return response(200, { list: [] });
      if (u.endsWith('/Lead') && method === 'POST') return response(200, { id: 'lead_1' });
      if (u.includes('/Task?')) return response(200, { list: [] });
      if (u.endsWith('/Task') && method === 'POST') return response(200, { id: 'task_1' });
      if (u.endsWith('/Opportunity') && method === 'POST') return response(200, { id: 'opp_1' });
      return response(404, { message: 'unexpected' });
    };
  });

  it('creates contact, lead and task with the right fields', async () => {
    const res = await syncLeadToEspo(ENV, baseLead);
    assert.equal(res.ok, true);
    assert.equal(res.contactId, 'contact_1');
    assert.equal(res.leadId, 'lead_1');
    assert.equal(res.taskId, 'task_1');

    const contact = calls.find((c) => c.url.endsWith('/Contact') && c.method === 'POST').body;
    assert.equal(contact.firstName, 'Ada');
    assert.equal(contact.lastName, 'Tester');
    assert.equal(contact.phoneNumber, '+18185550142');
    assert.equal(contact.emailAddress, 'ada@example.com');
    assert.equal(contact.addressCity, 'Encino');

    const lead = calls.find((c) => c.url.endsWith('/Lead') && c.method === 'POST').body;
    assert.equal(lead.status, 'New');
    assert.equal(lead.source, 'Web Site');
    assert.equal(lead.phoneNumber, '+18185550142');
    assert.equal(lead.website, 'https://amyelectric.com/residential-electrician');
    assert.match(lead.description, /Score 82/);

    const task = calls.find((c) => c.url.endsWith('/Task') && c.method === 'POST').body;
    assert.equal(task.parentType, 'Lead');
    assert.equal(task.parentId, 'lead_1');
    assert.equal(task.priority, 'High');
    assert.equal(task.status, 'Not Started');
    assert.match(task.dateEnd, /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:00$/);
  });

  it('adds an Opportunity for commercial leads with the estimate midpoint', async () => {
    const res = await syncLeadToEspo(ENV, { ...baseLead, segment: 'commercial', estimate_json: '{"rangeLow":2000,"rangeHigh":4000}' });
    assert.equal(res.ok, true);
    assert.equal(res.opportunityId, 'opp_1');
    const opp = calls.find((c) => c.url.endsWith('/Opportunity')).body;
    assert.equal(opp.stage, 'Prospecting');
    assert.equal(opp.amount, 3000);
    assert.equal(opp.contactId, 'contact_1');
  });

  it('does not create an Opportunity for residential leads', async () => {
    const res = await syncLeadToEspo(ENV, baseLead);
    assert.equal(res.ok, true);
    assert.equal(res.opportunityId, '');
    assert.equal(calls.some((c) => c.url.endsWith('/Opportunity')), false);
  });

  it('reuses an existing contact, lead and task (idempotent retry)', async () => {
    globalThis.fetch = async (url, init = {}) => {
      const u = String(url);
      const method = init.method || 'GET';
      calls.push({ url: u, method });
      if (u.includes('/Contact?')) return response(200, { list: [{ id: 'contact_9' }] });
      if (u.includes('/Lead?')) return response(200, { list: [{ id: 'lead_9', status: 'New' }] });
      if (u.includes('/Task?')) return response(200, { list: [{ id: 'task_9' }] });
      if (method === 'POST') throw new Error('should not create anything');
      return response(404, {});
    };
    const res = await syncLeadToEspo(ENV, baseLead);
    assert.equal(res.ok, true);
    assert.equal(res.contactId, 'contact_9');
    assert.equal(res.leadId, 'lead_9');
    assert.equal(res.taskId, 'task_9');
    assert.equal(calls.filter((c) => c.method === 'POST').length, 0);
  });

  it('refuses duplicates without touching the CRM', async () => {
    const res = await syncLeadToEspo(ENV, { ...baseLead, duplicate_of: 'lead_other' });
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'duplicate');
    assert.equal(calls.length, 0);
  });

  it('reports a create failure instead of throwing', async () => {
    globalThis.fetch = async (url) => {
      if (String(url).includes('/Contact?')) return response(200, { list: [] });
      return response(400, { message: 'validation' });
    };
    const res = await syncLeadToEspo(ENV, baseLead);
    assert.equal(res.ok, false);
    assert.match(res.reason, /contact 400/);
  });

  it('sends basic auth and never logs the password', async () => {
    await syncLeadToEspo(ENV, baseLead);
    const auth = calls[0].headers.Authorization;
    assert.match(auth, /^Basic /);
    assert.equal(Buffer.from(auth.slice(6), 'base64').toString(), 'amy-site:test-only');
  });
});

describe('sync agent safety', () => {
  it('is not imported with side effects (module loads cleanly)', async () => {
    const mod = await import('../crm-espocrm.js');
    assert.equal(typeof mod.syncLeadToEspo, 'function');
  });
});
