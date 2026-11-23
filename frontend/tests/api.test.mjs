import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import ts from 'typescript';
const source = fs.readFileSync(new URL('../src/api.ts', import.meta.url), 'utf8')
  .replace('import.meta.env.VITE_BACKEND_URL', "'https://research.example'");
const compiled = ts.transpile(source, { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 });
const { apiFetch, apiUrl, downloadPublisherBundle, submitResearchJob } = await import('data:text/javascript;base64,' + Buffer.from(compiled).toString('base64'));

test('failed mutations are never silently retried', async () => {
  const original = globalThis.fetch;
  const calls = [];
  globalThis.fetch = async (url, options) => { calls.push({ url, options }); return { ok: false, status: 500 }; };
  try {
    const response = await apiFetch('/api/research/start', { method: 'POST' });
    assert.equal(response.status, 500);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, 'https://research.example/api/research/start');
    assert.equal(calls[0].options.credentials, 'include');
  } finally { globalThis.fetch = original; }
});
test('an explicit resubmission reuses the key after an ambiguous response', async () => {
  const originalFetch = globalThis.fetch;
  const originalStorage = globalThis.sessionStorage;
  const storage = new Map();
  globalThis.sessionStorage = {
    getItem: key => storage.get(key),
    setItem: (key, value) => storage.set(key, value),
    removeItem: key => storage.delete(key),
  };
  const keys = [];
  globalThis.fetch = async (_, options) => {
    keys.push(options.headers.get('Idempotency-Key'));
    if (keys.length === 1) throw new Error('response lost');
    return new Response(JSON.stringify({ project_id: 'accepted' }), { status: 202 });
  };
  try {
    const payload = { topic: 'reproducibility' };
    await assert.rejects(submitResearchJob('/api/research/start', payload), /response lost/);
    assert.equal(keys.length, 1);
    assert.equal((await submitResearchJob('/api/research/start', payload)).project_id, 'accepted');
    assert.ok(keys[0]);
    assert.equal(keys[0], keys[1]);
    await submitResearchJob('/api/research/start', payload);
    assert.notEqual(keys[1], keys[2]);
  } finally {
    globalThis.fetch = originalFetch;
    if (originalStorage === undefined) delete globalThis.sessionStorage;
    else globalThis.sessionStorage = originalStorage;
  }
});
test('streams and artifacts share origin and foreign paths are rejected', () => {
  assert.equal(apiUrl('/api/research/stream/job'), 'https://research.example/api/research/stream/job');
  assert.equal(apiUrl('/vault/paper.pdf'), 'https://research.example/vault/paper.pdf');
  assert.throws(() => apiUrl('//foreign.example/'));
});

test('publisher download requests the selected job and surfaces integrity failures', async () => {
  const original = globalThis.fetch;
  globalThis.fetch = async (url, options) => {
    assert.equal(url, 'https://research.example/api/vault/publisher/readiness/bundle?job_id=job%26selected');
    assert.equal(options.credentials, 'include');
    return new Response(JSON.stringify({ detail: 'Publisher bundle failed integrity verification' }), { status: 409 });
  };
  try {
    await assert.rejects(downloadPublisherBundle('job&selected'), /failed integrity verification/);
  } finally { globalThis.fetch = original; }
});
