import { useEffect, useState } from 'react';
import { apiFetch } from '../api';

type Job = { id: string; status: string; commit: string; note: string };
export function PaperOrchestraPanel() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState('');
  const [detail, setDetail] = useState('');
  const [busy, setBusy] = useState(false);
  async function refresh() {
    setBusy(true); setError('');
    try {
      const response = await apiFetch('/api/paperorchestra/jobs');
      if (!response.ok) throw new Error('Could not load writing jobs.');
      setJobs((await response.json()).jobs);
    } catch (e) { setError(e instanceof Error ? e.message : 'Request failed.'); }
    finally { setBusy(false); }
  }
  useEffect(() => { void refresh(); }, []);
  async function inspect(id: string) {
    setBusy(true); setError(''); setDetail('');
    try {
      const response = await apiFetch(`/api/paperorchestra/jobs/${encodeURIComponent(id)}`);
      if (!response.ok) throw new Error('This job is missing or its artifacts have changed.');
      setDetail(JSON.stringify(await response.json(), null, 2));
    } catch (e) { setError(e instanceof Error ? e.message : 'Request failed.'); }
    finally { setBusy(false); }
  }
  return <section style={{ marginTop: 32 }}>
    <h3>PaperOrchestra writing and review</h3>
    <p>Writing jobs can run in an isolated worker or accept imported LaTeX. Generated drafts require citation, claim, and venue review before publication.</p>
    <button onClick={() => void refresh()} disabled={busy}>Refresh writing jobs</button>
    {error && <p role="alert">{error}</p>}
    {!jobs.length && !busy && <p>No writing jobs prepared yet.</p>}
    {jobs.map(job => <article key={job.id}><h4>{job.id} · {job.status.replaceAll('_', ' ')}</h4><p>{job.note}</p><button disabled={busy} onClick={() => void inspect(job.id)}>Inspect handoff and artifact hashes</button></article>)}
    {detail && <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere', maxHeight: 500, overflow: 'auto' }}>{detail}</pre>}
  </section>;
}
