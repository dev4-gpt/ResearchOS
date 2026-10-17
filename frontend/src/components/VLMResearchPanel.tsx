import { useCallback, useEffect, useMemo, useState } from 'react';
import { apiFetch } from '../api';
import { Activity, ArrowUpRight, Check, Circle, Clock3, RefreshCw, ShieldAlert } from 'lucide-react';
import './VLMResearchPanel.css';

type Intake = {
  run_id: string;
  created_at: string;
  status: string;
  manuscript_ready: boolean;
  judge_calibration: string;
  changed_inputs_since_snapshot?: string[];
  snapshot_current?: boolean;
  papers_ingested?: Array<{ paper_id?: string; source: string; error?: string }>;
  plans?: string[];
  notebooks?: Array<{ path: string }>;
  bundles?: Array<{ name: string; groups: Array<{ rows: number }> }>;
  blinded_queue_rows?: number;
  blinded_queue_path?: string;
  next_steps?: string[];
};
type ProjectStatus = {
  profile: { title: string; question: string; focus: string; repository: string; plan_files: string[]; notebooks: string[] };
  connection: { workspace: string; exists: boolean; repository_url: string; remote_matches: boolean; branch?: string | null; revision?: string | null; dirty?: boolean | null };
  latest: Intake | null;
  external_runs?: Array<{ name?: string; sha256?: string; archive?: string; created_at?: string; [key: string]: unknown }>;
};

type StepState = 'complete' | 'attention' | 'waiting' | 'blocked';

function formatDate(value?: string) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

export function VLMResearchPanel() {
  const [status, setStatus] = useState<ProjectStatus | null>(null);
  const [busy, setBusy] = useState<'refresh' | 'intake' | null>(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const refresh = useCallback(async () => {
    setBusy('refresh'); setError('');
    try {
      const response = await apiFetch('/api/research/projects/vlm-safety');
      if (!response.ok) throw new Error(`Project status returned HTTP ${response.status}.`);
      setStatus(await response.json());
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Could not load Blissful Bose project status.');
    } finally { setBusy(null); }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const runIntake = async () => {
    setBusy('intake'); setError(''); setNotice('');
    try {
      const response = await apiFetch('/api/research/projects/vlm-safety/prepare', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sample_per_group: 30 }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || `Intake returned HTTP ${response.status}.`);
      setStatus(current => current ? { ...current, latest: data } : current);
      setNotice(`Intake ${data.run_id} recorded. The connected research workspace was read without executing notebooks or starting model jobs.`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Could not prepare a new research intake.');
    } finally { setBusy(null); }
  };

  const latest = status?.latest;
  const connected = Boolean(status?.connection.exists && status.connection.remote_matches);
  const stale = Boolean(latest && latest.snapshot_current === false);
  const evidenceState: StepState = !latest ? 'waiting' : stale ? 'attention' : 'complete';
  const steps = useMemo(() => [
    { title: 'Connect the canonical project', state: connected ? 'complete' as StepState : 'blocked' as StepState,
      detail: connected ? 'The local workspace points to dev4-gpt/blissful-bose.' : 'The workspace or its expected GitHub origin is unavailable.' },
    { title: 'Freeze and inspect evidence', state: evidenceState,
      detail: !latest ? 'Create a read-only intake and hash the files used.' : stale ? `${latest.changed_inputs_since_snapshot?.length || 0} consulted input(s) changed after this snapshot.` : `Latest intake ${latest.run_id} · ${formatDate(latest.created_at)}.` },
    { title: 'Validate safety labels with people', state: latest?.judge_calibration === 'PASSED' ? 'complete' as StepState : 'attention' as StepState,
      detail: latest?.judge_calibration === 'PASSED' ? 'Human calibration gate recorded as passed.' : 'Required before interpreting refusal labels as safety outcomes; no labels are auto-approved.' },
    { title: 'Run the controlled measurement study', state: 'waiting' as StepState,
      detail: 'Review v3 provenance, prompt matching, comprehension checks, benign controls, and predeclared analysis before any GPU run.' },
    { title: 'Test the intervention-induced seesaw', state: 'waiting' as StepState,
      detail: 'A separate causal experiment follows the measurement gate; compare paired modalities across a prespecified intervention sweep.' },
    { title: 'Decide whether a paper is supported', state: latest?.manuscript_ready ? 'complete' as StepState : 'blocked' as StepState,
      detail: latest?.manuscript_ready ? 'Publication gate is recorded as passed.' : 'Blocked until provenance, human validation, analysis, novelty, and source-grounding gates pass.' },
  ], [connected, evidenceState, latest, stale]);

  const counts = latest?.bundles?.reduce((sum, bundle) => sum + (bundle.groups || []).reduce((n, group) => n + (group.rows || 0), 0), 0);
  const papers = latest?.papers_ingested?.filter(paper => paper.paper_id).length;

  return <section className="vlm-research" aria-label="Blissful Bose VLM research pipeline">
    <header className="vlm-research__header">
      <div>
        <div className="vlm-research__eyebrow"><Activity size={15} /> CONNECTED RESEARCH PROJECT</div>
        <h2>{status?.profile.title || 'Blissful Bose · VLM safety'}</h2>
        <p>{status?.profile.focus || 'Loading the connected research plan…'}</p>
      </div>
      <div className="vlm-research__actions">
        <button type="button" onClick={() => void refresh()} disabled={busy !== null}><RefreshCw size={15} /> Refresh</button>
        <button type="button" className="primary" onClick={() => void runIntake()} disabled={!connected || busy !== null}>
          <Activity size={15} /> {busy === 'intake' ? 'Preparing…' : 'Run read-only intake'}
        </button>
      </div>
    </header>

    {error && <p role="alert" className="vlm-research__alert">{error}</p>}
    {notice && <p role="status" className="vlm-research__notice">{notice}</p>}
    {!status && !error && <p className="vlm-research__muted">Loading project connection…</p>}

    {status && <>
      <div className="vlm-research__connection">
        <div><span className={`vlm-research__dot ${connected ? 'is-good' : 'is-bad'}`} />
          <strong>{connected ? 'Connected' : 'Connection needs attention'}</strong>
          <a href={status.connection.repository_url} target="_blank" rel="noreferrer">dev4-gpt/blissful-bose <ArrowUpRight size={13} /></a>
        </div>
        <span>{status.connection.branch || 'branch unavailable'}{status.connection.dirty ? ' · local changes present' : ''}</span>
      </div>

      <article className="vlm-research__question">
        <div><span>RESEARCH QUESTION</span><p>{status.profile.question}</p></div>
        <ShieldAlert size={20} aria-hidden="true" />
      </article>

      <div className="vlm-research__grid">
        <section className="vlm-research__stages" aria-label="Research phase stages">
          <h3>End-to-end research phase</h3>
          <p className="vlm-research__muted">The measurement question and the causal seesaw question have separate gates.</p>
          <ol>{steps.map((step, index) => <li key={step.title} className={`stage stage--${step.state}`}>
            <div className="stage__marker">{step.state === 'complete' ? <Check size={15} /> : step.state === 'blocked' ? <ShieldAlert size={15} /> : step.state === 'attention' ? <Clock3 size={15} /> : <Circle size={12} />}</div>
            <div><div className="stage__title"><span>{index + 1}. {step.title}</span><small>{step.state === 'complete' ? 'Done' : step.state === 'blocked' ? 'Gate' : step.state === 'attention' ? 'Required' : 'Next'}</small></div><p>{step.detail}</p></div>
          </li>)}</ol>
        </section>

        <aside className="vlm-research__evidence">
          <h3>Evidence on hand</h3>
          <dl>
            <div><dt>Latest intake</dt><dd>{latest ? formatDate(latest.created_at) : 'Not run'}</dd></div>
            <div><dt>Snapshot</dt><dd>{!latest ? 'No snapshot' : stale ? 'Stale · refresh intake' : 'Current'}</dd></div>
            <div><dt>Saved pilot records inspected</dt><dd>{counts ?? '—'}</dd></div>
            <div><dt>PDF notes in this intake</dt><dd>{papers ?? 'Not included in this intake'}</dd></div>
            <div><dt>Blinded review queue</dt><dd>{latest?.blinded_queue_rows ?? 'Not prepared'}</dd></div>
            <div><dt>Human judge calibration</dt><dd>{latest?.judge_calibration || 'Not recorded'}</dd></div>
          </dl>
          <p className="vlm-research__caveat">Saved judge labels are exploratory diagnostics. A refusal phrase or model-generated label is not a validated safety outcome.</p>
          {latest?.blinded_queue_path && <details><summary>Local audit queue location</summary><code>{latest.blinded_queue_path}</code></details>}
        </aside>
      </div>

      <details className="vlm-research__details"><summary>Phase plan and artifacts</summary>
        <div className="vlm-research__artifact-grid">
          <div><h4>Connected plans</h4><ul>{(latest?.plans?.length ? latest.plans : status.profile.plan_files).map(path => <li key={path}><code>{path}</code></li>)}</ul></div>
          <div><h4>Notebook versions</h4><ul>{(latest?.notebooks?.map(n => n.path) || status.profile.notebooks).map(path => <li key={path}><code>{path}</code></li>)}</ul></div>
          <div><h4>Current research outputs</h4><p>Proposal assessment and master plan are in the ResearchingOS vault. The pipeline does not execute notebooks, launch GPU jobs, read private Claude sessions, or draft a paper automatically.</p></div>
        </div>
        {latest?.next_steps?.length ? <ol className="vlm-research__next">{latest.next_steps.map(step => <li key={step}>{step}</li>)}</ol> : null}
      </details>
      {status.external_runs?.length ? <p className="vlm-research__muted">{status.external_runs.length} imported external run snapshot(s) are indexed for this project.</p> : null}
    </>}
  </section>;
}
