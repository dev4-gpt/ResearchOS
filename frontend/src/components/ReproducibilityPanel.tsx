import { useEffect, useState } from 'react';
import { apiFetch } from '../api';

interface Arm { tasks: number; resolved: number; seconds: number; tokens: number }
interface Run { id: string; synthetic: boolean; model: string; arms: Record<string, Arm> }
interface Status { endpoint_configured: boolean; docker_installed: boolean; official_harness_validated: boolean }
interface Detail { id: string; report: string; artifacts: Record<string, string> }

async function read<T>(path: string): Promise<T> {
  const response = await apiFetch(`/api/reproducibility/${path}`);
  if (!response.ok) throw new Error('Could not load reproducibility evidence.');
  return response.json();
}

export function ReproducibilityPanel() {
  const [status, setStatus] = useState<Status | null>(null);
  const [runs, setRuns] = useState<Run[]>([]);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  async function refresh() {
    setBusy(true); setError('');
    try {
      const [next, history] = await Promise.all([read<Status>('status'), read<{ runs: Run[] }>('runs')]);
      setStatus(next); setRuns(history.runs);
    } catch (err) { setError(err instanceof Error ? err.message : 'Connection failed.'); }
    finally { setBusy(false); }
  }
  useEffect(() => { void refresh(); }, []);
  async function inspect(id: string) {
    setBusy(true); setError(''); setDetail(null);
    try { setDetail(await read<Detail>(`runs/${encodeURIComponent(id)}`)); }
    catch (err) { setError(err instanceof Error ? err.message : 'Could not load run.'); }
    finally { setBusy(false); }
  }
  return <section style={{ padding: 24, color: 'var(--text-primary, #e2e8f0)' }}>
    <h2>Reproducibility Agent</h2>
    <p>Research question → pinned code → repair → fixed tests → recorded evidence.</p>
    {status && <p>Gemma endpoint: {status.endpoint_configured ? 'configured' : 'not configured'} · Docker: {status.docker_installed ? 'installed' : 'missing'} · Competition harness: {status.official_harness_validated ? 'validated' : 'not yet validated'}</p>}
    <p>Run experiments through the local CLI. Each approach receives the same time, token, and step limits. Fixture demos do not measure model performance.</p>
    <button onClick={() => void refresh()} disabled={busy}>Refresh runs</button>
    {error && <p role="alert">{error}</p>}
    {!runs.length && !busy && <p>No experiments recorded yet.</p>}
    {runs.map(run => <article key={run.id} style={{ marginTop: 24, padding: 16, border: '1px solid #475569', borderRadius: 8 }}>
      <h3>{run.synthetic ? 'Fixture demo — no model inference' : 'Local Gemma evaluation'}</h3>
      <p>{run.id} · {run.model}</p>
      <table style={{ width: '100%', textAlign: 'left' }}>
        <thead><tr><th>Approach</th><th>Resolved / tasks</th><th>Seconds</th><th>Tokens</th></tr></thead>
        <tbody>{Object.entries(run.arms).map(([arm, row]) => <tr key={arm}>
          <td>{arm}</td><td>{row.resolved} / {row.tasks}</td><td>{row.seconds.toFixed(2)}</td><td>{row.tokens}</td>
        </tr>)}</tbody>
      </table>
      <button onClick={() => void inspect(run.id)} disabled={busy}>Inspect report and artifact hashes</button>
    </article>)}
    {detail && <div style={{ marginTop: 24 }}><h3>Evidence report</h3>
      <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{detail.report}</pre>
      <ul>{Object.keys(detail.artifacts).filter(path => path.endsWith('.json') || path.endsWith('.diff')).map(path =>
        <li key={path}><a href={`/api/reproducibility/runs/${encodeURIComponent(detail.id)}/artifact?path=${encodeURIComponent(path)}`} target="_blank" rel="noreferrer">{path}</a></li>
      )}</ul>
      <details><summary>Artifact SHA-256 manifest</summary><pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{JSON.stringify(detail.artifacts, null, 2)}</pre></details>
    </div>}
  </section>;
}
