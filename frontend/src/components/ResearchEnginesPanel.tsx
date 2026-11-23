import { useEffect, useState } from 'react';
import { apiFetch } from '../api';
import { PaperOrchestraPanel } from './PaperOrchestraPanel';

type Metrics = { ndcg_at_10: number; recall_at_20: number; tasks: number };
type Verification = { integrity_verified: boolean; metrics_recomputed: boolean; publication_eligible: boolean; reason: string };
type Run = { id: string; engine: string; mode: string; seed: number; model: string; status: string; error?: string;
  synthetic: boolean; parent_run?: string; metrics: Record<string, Metrics>; usage?: { calls: number; tokens_reported: number; seconds: number; cost_ceiling_reserved_usd: number }; verification: Verification };
type Status = { engines: Record<string, { sources_verified: boolean; commit: string; enabled: boolean; error: string; integration_mode?: string }>; gemini_key_configured: boolean; docker_installed: boolean };
type Detail = { summary: Run; verification: Verification; artifacts: Record<string, string> };
async function read<T>(path: string): Promise<T> {
  const response = await apiFetch(`/api/research-engines/${path}`);
  if (!response.ok) throw new Error(`Research engine request failed (${response.status}).`);
  return response.json();
}
export function ResearchEnginesPanel() {
  const [status, setStatus] = useState<Status | null>(null);
  const [runs, setRuns] = useState<Run[]>([]);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [artifact, setArtifact] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  async function refresh() {
    setBusy(true); setError('');
    try {
      const [next, history] = await Promise.all([read<Status>('status'), read<{ runs: Run[] }>('runs')]);
      setStatus(next); setRuns(history.runs);
    } catch (e) { setError(e instanceof Error ? e.message : 'Unable to load runs.'); }
    finally { setBusy(false); }
  }
  useEffect(() => { void refresh(); }, []);
  async function inspect(id: string) {
    setBusy(true); setError(''); setDetail(null); setArtifact('');
    try { setDetail(await read<Detail>(`runs/${encodeURIComponent(id)}`)); }
    catch (e) { setError(e instanceof Error ? e.message : 'Unable to inspect run.'); }
    finally { setBusy(false); }
  }
  async function showArtifact(id: string, name: string) {
    setBusy(true); setError(''); setArtifact('');
    try {
      const response = await apiFetch(`/api/research-engines/runs/${encodeURIComponent(id)}/artifact?name=${encodeURIComponent(name)}`);
      if (!response.ok) throw new Error(`Artifact unavailable (${response.status}).`);
      setArtifact(await response.text());
    } catch (e) { setError(e instanceof Error ? e.message : 'Unable to read artifact.'); }
    finally { setBusy(false); }
  }
  return <section style={{ padding: 24, color: 'var(--text-primary, #e2e8f0)' }}>
    <h2>Research engines</h2>
    <p>AlphaEvolve develops ranking algorithms. Harness² refines research instructions using execution evidence. PaperOrchestra prepares manuscripts from research materials.</p>
    {status && Object.entries(status.engines).map(([name, engine]) => <p key={name}>
      <strong>{name}</strong>: {engine.sources_verified ? 'pinned sources verified' : 'setup needed'} · {engine.integration_mode === 'handoff-and-review' ? 'handoff and review only' : `live runs ${engine.enabled ? 'enabled' : 'disabled'}`}<br />
      <small>Revision {engine.commit.slice(0, 12)} {engine.error}</small>
    </p>)}
    <p>Launch runs through the local CLI. Fixture demonstrations cannot support publication claims.</p>
    <button onClick={() => void refresh()} disabled={busy}>Refresh runs</button>
    {error && <p role="alert">{error}</p>}
    {!busy && !runs.length && <p>No engine runs yet.</p>}
    {runs.map(run => <article key={run.id} style={{ marginTop: 20, padding: 16, border: '1px solid #475569', borderRadius: 8 }}>
      <h3>{run.engine} · {run.status}</h3>
      <p>{run.synthetic ? 'Synthetic fixture' : 'Research dataset'} · {run.mode === 'demo' ? 'deterministic demo; no model inference' : run.model} · seed {run.seed}</p>
      {run.parent_run && <p>Parent run: {run.parent_run}</p>}
      {run.error && <p role="alert">{run.error}</p>}
      {run.metrics && Object.keys(run.metrics).length > 0 && <table style={{ width: '100%', textAlign: 'left' }}>
        <caption>Held-out task measurements</caption>
        <thead><tr><th>Approach</th><th>Tasks</th><th>nDCG@10</th><th>Recall@20</th></tr></thead>
        <tbody>{Object.entries(run.metrics).map(([arm, m]) => <tr key={arm}><td>{arm}</td><td>{m.tasks}</td><td>{m.ndcg_at_10.toFixed(3)}</td><td>{m.recall_at_20.toFixed(3)}</td></tr>)}</tbody>
      </table>}
      {run.usage && <p>{run.usage.calls} model calls · {run.usage.tokens_reported} reported tokens · {run.usage.seconds.toFixed(1)} seconds · ${run.usage.cost_ceiling_reserved_usd.toFixed(3)} reserved ceiling (not billed cost)</p>}
      <p>{run.verification.metrics_recomputed ? 'Metrics independently recomputed' : 'Evidence unverified'} · {run.verification.reason}</p>
      <button onClick={() => void inspect(run.id)} disabled={busy}>Inspect evidence</button>
    </article>)}
    {detail && <section><h3>Run artifacts</h3><p>{detail.summary.id}</p>
      <ul>{Object.keys(detail.artifacts).filter(name => !name.startsWith('harness2/')).map(name => <li key={name}><button disabled={busy} onClick={() => void showArtifact(detail.summary.id, name)}>{name}</button></li>)}</ul>
      <details><summary>All artifact hashes</summary><pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{JSON.stringify(detail.artifacts, null, 2)}</pre></details>
      {artifact && <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere', maxHeight: 600, overflow: 'auto' }}>{artifact}</pre>}
    </section>}
    <PaperOrchestraPanel />
  </section>;
}
