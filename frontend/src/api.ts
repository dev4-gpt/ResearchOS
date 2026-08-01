/**
 * Bulletproof API fetcher for ResearchingOS frontend.
 * Tries relative `/api/...` first (Vite proxy), and if proxy fails or returns network error,
 * falls back to direct `http://127.0.0.1:8000/api/...` endpoint.
 */

const DIRECT_BACKEND_URL = 'http://127.0.0.1:8000';

export async function apiFetch(endpoint: string, options?: RequestInit): Promise<Response> {
  const url = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

  try {
    const res = await fetch(url, options);
    if (res.ok) {
      return res;
    }
  } catch (err) {
    console.warn(`Relative API proxy fetch failed for ${url}. Trying direct backend connection...`, err);
  }

  // Fallback: Direct call to http://127.0.0.1:8000
  const directUrl = `${DIRECT_BACKEND_URL}${url}`;
  return await fetch(directUrl, options);
}
