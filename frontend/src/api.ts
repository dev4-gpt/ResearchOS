// Same-origin in production; Vite proxies locally. Never retry a mutation implicitly.
const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL || '').replace(/\/$/, '');

export function apiUrl(endpoint: string): string {
  if (!endpoint.startsWith('/') || endpoint.startsWith('//')) {
    throw new Error('API paths must be relative to the configured backend');
  }
  return `${BACKEND_URL}${endpoint}`;
}

export async function apiFetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const headers = new Headers(options.headers);
  return fetch(apiUrl(endpoint), { ...options, headers, credentials: 'include' });
}

export async function submitResearchJob(endpoint: '/api/research/start' | '/api/research/meta-review', payload: object) {
  const body = JSON.stringify(payload);
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body));
  const fingerprint = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
  const pending = `researchingos.submission:${apiUrl(endpoint)}:${fingerprint}`;
  const key = sessionStorage.getItem(pending) || crypto.randomUUID();
  sessionStorage.setItem(pending, key);
  const response = await apiFetch(endpoint, {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': key }, body,
  });
  if (!response.ok) throw new Error(`Job submission failed (HTTP ${response.status})`);
  const job = await response.json();
  if (!job.project_id) throw new Error('Job submission returned no ID');
  // Keep the request key if the response or its body was lost.
  if (sessionStorage.getItem(pending) === key) sessionStorage.removeItem(pending);
  return job;
}

export async function downloadPublisherBundle(jobId: string): Promise<void> {
  const response = await apiFetch(`/api/vault/publisher/readiness/bundle?job_id=${encodeURIComponent(jobId)}`);
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || `Bundle download failed (HTTP ${response.status})`);
  }
  const url = URL.createObjectURL(await response.blob());
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = 'researchingos-publish-ready-bundle.zip';
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
