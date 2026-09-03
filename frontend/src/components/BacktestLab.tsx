import React, { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  CircleDot,
  Eye,
  FlaskConical,
  Gauge,
  Layers3,
  LoaderCircle,
  Play,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  Zap,
} from 'lucide-react';
import { apiFetch } from '../api';
import { PDFVisualPreviewModal } from './PDFVisualPreviewModal';

interface DraftFile {
  filename: string;
  title?: string;
  modified?: string;
  size?: number;
}

interface AuditCheck {
  passed: boolean;
  detail?: string;
}

interface AuditData {
  score?: number;
  status?: string;
  checkmate_passed?: boolean;
  total_pages?: number;
  checkmate_checks?: Record<string, AuditCheck>;
  layout_geometry?: {
    overflow_count?: number;
    passed?: boolean;
  };
  page_tiles?: Array<{ page: number; filename: string; width: number; height: number }>;
}

interface RunRecord {
  iteration: number;
  score: number;
  passed: boolean;
  total_pages?: number;
}

interface ReadinessJob {
  job_id: string;
  status: string;
  run_id?: string;
  evaluator_version?: string;
  config_hash?: string;
  current_stage?: string;
  progress?: {
    drafts_tested?: number;
    venues_tested?: number;
    matrix_total?: number;
    compiled?: number;
    blocked?: number;
    ready?: number;
    last_filename?: string;
    last_venue?: string;
  };
  report?: {
    stage_events_path?: string;
    artifact_manifest?: string;
    release_note?: string;
  } | null;
  error?: string | null;
}

const FALLBACK_VENUES = ['IEEEtran'];
const DEFAULT_DRAFT = 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md';

const LOOP_STEPS = [
  { key: 'detect', label: 'Defect detector', detail: 'Find visual + textual defects', icon: AlertTriangle },
  { key: 'repair', label: 'Manuscript remediator', detail: 'Apply deterministic fixes', icon: Sparkles },
  { key: 'compile', label: 'Recompile + audit', detail: 'Render the candidate again', icon: TerminalSquare },
  { key: 'converge', label: 'Convergence validator', detail: 'Seal only when quality holds', icon: ShieldCheck },
];

const humanize = (value: string) => value.replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());

const titleFor = (draft: DraftFile) => {
  const base = draft.title || draft.filename.replace(/\.md$/, '').replace(/_/g, ' ');
  return base.replace(/\b\w/g, (letter) => letter.toUpperCase());
};

const scoreColor = (score: number) => (score >= 85 ? 'var(--success)' : score >= 60 ? 'var(--warning)' : 'var(--danger)');

const BacktestLab: React.FC = () => {
  const [drafts, setDrafts] = useState<DraftFile[]>([]);
  const [venues, setVenues] = useState<string[]>([]);
  const [filename, setFilename] = useState(DEFAULT_DRAFT);
  const [venue, setVenue] = useState('IEEEtran');
  const [audit, setAudit] = useState<AuditData | null>(null);
  const [history, setHistory] = useState<RunRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [readinessJob, setReadinessJob] = useState<ReadinessJob | null>(null);

  const selectedDraft = useMemo(
    () => drafts.find((draft) => draft.filename === filename),
    [drafts, filename],
  );

  const loadDrafts = async () => {
    try {
      const response = await apiFetch('/api/vault/files?category=drafts');
      if (!response.ok) throw new Error(`Unable to load drafts (HTTP ${response.status})`);
      const data = await response.json();
      const nextDrafts = (Array.isArray(data) ? data : []).filter(
        (item: DraftFile) => item.filename?.endsWith('.md'),
      );
      setDrafts(nextDrafts);
      if (nextDrafts.length && !nextDrafts.some((item: DraftFile) => item.filename === filename)) {
        setFilename(nextDrafts[0].filename);
      }
    } catch (loadError: any) {
      setError(loadError.message || 'Unable to load manuscript drafts.');
    }
  };

  const loadVenues = async () => {
    try {
      const response = await apiFetch('/api/venues');
      if (!response.ok) throw new Error(`Unable to load venue registry (HTTP ${response.status})`);
      const data = await response.json();
      const nextVenues = Array.isArray(data.venue_order)
        ? data.venue_order
        : Object.keys(data.release_profiles || data.venues || {});
      if (nextVenues.length) {
        setVenues(nextVenues);
        if (!nextVenues.includes(venue)) setVenue(nextVenues[0]);
      }
    } catch (loadError: any) {
      setError(loadError.message || 'Unable to load the venue registry.');
    }
  };

  const loadPreview = async (nextFilename = filename, nextVenue = venue) => {
    if (!nextFilename) return;
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ filename: nextFilename, venue: nextVenue });
      const response = await apiFetch(`/api/vault/backtest/preview-tiles?${params.toString()}`);
      if (!response.ok) throw new Error(`Preview compilation failed (HTTP ${response.status})`);
      const data = await response.json();
      setAudit(data.audit || null);
      const initialScore = Number(data.audit?.score ?? 0);
      setHistory((existing) => existing.length ? existing : [{ iteration: 0, score: initialScore, passed: Boolean(data.audit?.checkmate_passed) }]);
    } catch (loadError: any) {
      setAudit(null);
      setError(loadError.message || 'Unable to build the visual audit.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDrafts();
    void loadVenues();
  }, []);

  useEffect(() => {
    if (filename) void loadPreview(filename, venue);
  }, [filename, venue]);

  const runClosedLoop = async () => {
    if (!filename || running) return;
    setRunning(true);
    setError(null);
    try {
      const params = new URLSearchParams({ filename, venue });
      const response = await apiFetch(`/api/vault/backtest/auto-remediate?${params.toString()}`, { method: 'POST' });
      if (!response.ok) throw new Error(`Closed loop failed (HTTP ${response.status})`);
      const data = await response.json();
      const result = data.result || {};
      if (Array.isArray(result.history)) setHistory(result.history);
      if (result.audit) setAudit(result.audit);
      await loadPreview(filename, venue);
    } catch (runError: any) {
      setError(runError.message || 'The closed loop could not complete.');
    } finally {
      setRunning(false);
    }
  };

  const runPublisherReadiness = async () => {
    if (readinessJob?.status === 'running') return;
    setError(null);
    try {
      const response = await apiFetch('/api/vault/publisher/readiness', { method: 'POST' });
      if (!response.ok) throw new Error('Publisher matrix failed to start (HTTP ' + response.status + ')');
      const data = await response.json();
      let job: ReadinessJob = data.job;
      setReadinessJob(job);
      while (job?.status === 'running') {
        await new Promise((resolve) => window.setTimeout(resolve, 1200));
        const statusResponse = await apiFetch('/api/vault/publisher/readiness/status?job_id=' + encodeURIComponent(job.job_id));
        if (!statusResponse.ok) throw new Error('Unable to read publisher progress (HTTP ' + statusResponse.status + ')');
        const statusData = await statusResponse.json();
        job = statusData.job;
        setReadinessJob(job);
      }
      if (job?.status === 'failed') throw new Error(job.error || 'Publisher matrix failed.');
    } catch (runError: any) {
      setError(runError.message || 'The publisher matrix could not complete.');
    }
  };

  const score = Number(audit?.score ?? 0);
  const checks = Object.entries(audit?.checkmate_checks || {});
  const failedChecks = checks.filter(([, check]) => !check.passed).length;
  const overflowCount = audit?.layout_geometry?.overflow_count ?? 0;
  const passed = Boolean(audit?.checkmate_passed);
  const lastIteration = history[history.length - 1];
  const currentTitle = selectedDraft ? titleFor(selectedDraft) : filename.replace(/\.md$/, '');
  const venueOptions = venues.length ? venues : FALLBACK_VENUES;

  return (
    <div className="backtest-lab animate-entrance">
      <header className="backtest-hero">
        <div>
          <div className="eyebrow"><FlaskConical size={14} /> Closed-loop quality control</div>
          <h1>Backtest Lab</h1>
          <p>Watch every manuscript move from defect detection to a verified, human-review-ready release.</p>
        </div>
        <div className={`backtest-status ${passed ? 'is-passed' : 'is-pending'}`}>
          <CircleDot size={15} />
          <span>{loading ? 'Compiling candidate' : passed ? 'Converged' : 'Needs attention'}</span>
        </div>
      </header>

      <section className="backtest-controls glass">
        <div className="backtest-select-wrap">
          <span className="control-label">Manuscript</span>
          <div className="select-shell">
            <Layers3 size={15} />
            <select value={filename} onChange={(event) => { setHistory([]); setFilename(event.target.value); }}>
              {drafts.length === 0 && <option value={filename}>{filename}</option>}
              {drafts.map((draft) => <option key={draft.filename} value={draft.filename}>{titleFor(draft)}</option>)}
            </select>
            <ChevronDown size={14} />
          </div>
        </div>
        <div className="venue-control">
          <span className="control-label">Target venue</span>
          <div className="venue-pills">
            {venueOptions.map((candidate) => (
              <button key={candidate} className={venue === candidate ? 'is-active' : ''} onClick={() => { setHistory([]); setVenue(candidate); }}>
                {candidate}
              </button>
            ))}
          </div>
        </div>
        <div className="backtest-actions">
          <button className="icon-action" title="Refresh visual audit" onClick={() => void loadPreview()} disabled={loading || running}>
            <RefreshCw size={15} className={loading ? 'spin' : ''} />
          </button>
          <button className="primary-action" onClick={() => void runClosedLoop()} disabled={running || loading || !filename}>
            {running ? <LoaderCircle size={15} className="spin" /> : <Play size={15} fill="currentColor" />}
            {running ? 'Running loop' : 'Run closed loop'}
          </button>
          <button className="secondary-action" onClick={() => void runPublisherReadiness()} disabled={readinessJob?.status === 'running'}>
            {readinessJob?.status === 'running' ? <LoaderCircle size={15} className="spin" /> : <ShieldCheck size={15} />}
            {readinessJob?.status === 'running' ? 'Testing matrix' : 'Run all venue readiness'}
          </button>
        </div>
      </section>

      {error && <div className="backtest-error"><AlertTriangle size={16} /><span>{error}</span></div>}

      {readinessJob && (
        <section className="backtest-panel glass readiness-panel">
          <div className="panel-header">
            <div><span className="panel-kicker">HITL publisher matrix</span><h2>Strict evidence readiness</h2></div>
            <span className={readinessJob.status === 'completed' ? 'audit-count' : 'mono muted'}>
              {readinessJob.status === 'completed' ? 'complete' : readinessJob.status}
            </span>
          </div>
          <div className="readiness-summary">
            <span><strong>{readinessJob.progress?.ready ?? 0}</strong> ready</span>
            <span><strong>{readinessJob.progress?.blocked ?? 0}</strong> blocked</span>
            <span><strong>{readinessJob.progress?.compiled ?? 0}</strong> compiled</span>
            <span><strong>{readinessJob.progress?.matrix_total ?? 0}</strong> matrix cases</span>
          </div>
          <div className="readiness-detail">
            <span>Evaluator {readinessJob.evaluator_version || 'v2'}</span>
            <span>Stage {humanize(readinessJob.current_stage || 'prepare')}</span>
            {readinessJob.progress?.last_filename && <span>{readinessJob.progress.last_filename} / {readinessJob.progress.last_venue || 'all venues'}</span>}
            {readinessJob.status === 'completed' && <a href="/api/vault/publisher/readiness/bundle">Download verified bundle</a>}
          </div>
          <small>Strict evidence is fail-closed. "Ready" means ready for human review; external submission remains manual.</small>
        </section>
      )}

      <section className="backtest-kpis">
        <div className="backtest-kpi glass score-kpi">
          <div className="kpi-heading"><span>Checkmate score</span><Gauge size={15} /></div>
          <div className="score-line"><strong style={{ color: scoreColor(score) }}>{loading ? '--' : score.toFixed(1)}</strong><span>/ 100</span></div>
          <div className="score-bar"><span style={{ width: `${Math.min(score, 100)}%`, background: scoreColor(score) }} /></div>
          <small>{passed ? 'Verified seal issued' : `${failedChecks || 'No'} checks require attention`}</small>
        </div>
        <div className="backtest-kpi glass">
          <div className="kpi-heading"><span>Page budget</span><Layers3 size={15} /></div>
          <div className="kpi-value">{loading ? '--' : audit?.total_pages ?? 0}<span> pages</span></div>
          <small>{audit?.layout_geometry?.passed !== false ? 'Layout geometry is clean' : `${overflowCount} margin overflow${overflowCount === 1 ? '' : 's'}`}</small>
        </div>
        <div className="backtest-kpi glass">
          <div className="kpi-heading"><span>Loop iterations</span><Zap size={15} /></div>
          <div className="kpi-value">{lastIteration?.iteration ?? 0}<span> passes</span></div>
          <small>{lastIteration?.passed ? 'Converged on latest pass' : 'Run the loop to remediate'}</small>
        </div>
        <div className="backtest-kpi glass">
          <div className="kpi-heading"><span>Release state</span><ShieldCheck size={15} /></div>
          <div className={`release-value ${passed ? 'is-passed' : 'is-pending'}`}>{loading ? 'BUILDING' : passed ? 'APPROVED' : 'REVIEW'}</div>
          <small>{currentTitle}</small>
        </div>
      </section>

      <section className="backtest-main-grid">
        <div className="backtest-panel glass loop-panel">
          <div className="panel-header"><div><span className="panel-kicker">Execution graph</span><h2>Closed loop trajectory</h2></div><span className="live-tag"><span /> live</span></div>
          <div className="loop-rail">
            {LOOP_STEPS.map((step, index) => {
              const Icon = step.icon;
              const isComplete = passed || (!running && index < 3 && Boolean(audit));
              const isActive = running && index === 2;
              return (
                <React.Fragment key={step.key}>
                  <div className={`loop-node ${isComplete ? 'is-complete' : ''} ${isActive ? 'is-active' : ''}`}>
                    <div className="loop-icon"><Icon size={17} /></div>
                    <div><strong>{step.label}</strong><span>{step.detail}</span></div>
                  </div>
                  {index < LOOP_STEPS.length - 1 && <ArrowRight className={`loop-arrow ${isComplete ? 'is-complete' : ''}`} size={16} />}
                </React.Fragment>
              );
            })}
          </div>
          <div className="loop-summary"><span>{running ? 'Recompiling candidate and re-running geometry checks…' : passed ? 'Every gate is green. The artifact is ready for human review.' : 'Run the loop to turn audit findings into a convergence trace.'}</span><span className="mono">{venue} · {currentTitle}</span></div>
        </div>

        <div className="backtest-panel glass history-panel">
          <div className="panel-header"><div><span className="panel-kicker">Iteration telemetry</span><h2>Run history</h2></div><span className="mono muted">{history.length ? `${history.length} samples` : 'waiting'}</span></div>
          <div className="history-chart">
            {history.length ? history.map((run, index) => (
              <div className="history-column" key={`${run.iteration}-${index}`}>
                <div className="history-score">{run.score.toFixed(0)}</div>
                <div className="history-bar-track"><div className={`history-bar ${run.passed ? 'is-passed' : ''}`} style={{ height: `${Math.max(8, run.score)}%` }} /></div>
                <span>pass {run.iteration}</span>
              </div>
            )) : <div className="empty-chart"><Sparkles size={18} /><span>No runs yet</span></div>}
          </div>
          <div className="history-footer"><span><span className="legend-dot is-passed" /> converged</span><span><span className="legend-dot" /> iteration score</span></div>
        </div>
      </section>

      <section className="backtest-bottom-grid">
        <div className="backtest-panel glass audit-panel">
          <div className="panel-header"><div><span className="panel-kicker">Evidence surface</span><h2>Publication audit</h2></div><span className="audit-count">{checks.filter(([, check]) => check.passed).length}/{checks.length || 8} passed</span></div>
          <div className="audit-grid">
            {(checks.length ? checks : LOOP_STEPS.slice(0, 4).map((step) => [step.key, { passed: false, detail: 'Waiting for the first audit run' }] as [string, AuditCheck])).map(([key, check]) => (
              <div className={`audit-check ${check.passed ? 'is-passed' : ''}`} key={key}>
                {check.passed ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
                <div><strong>{humanize(key)}</strong><span>{check.detail || (check.passed ? 'Verified' : 'Remediation required')}</span></div>
              </div>
            ))}
          </div>
        </div>

        <div className="backtest-panel glass preview-panel">
          <div className="panel-header"><div><span className="panel-kicker">Rendered artifact</span><h2>Page tiles</h2></div><button className="text-action" onClick={() => setPreviewOpen(true)} disabled={!audit?.page_tiles?.length}><Eye size={14} /> inspect</button></div>
          <div className="tile-strip">
            {audit?.page_tiles?.length ? audit.page_tiles.slice(0, 5).map((tile) => {
              const cleanName = filename.replace(/\.md$/, '');
              // Keep preview images on the same origin so the Vite proxy works in
              // the browser as reliably as the JSON API does. A hard-coded
              // backend origin made the tiles look like missing files when the
              // UI was opened through a different localhost host/port.
              const imageUrl = `/api/vault/backtest/preview-tile-image/${encodeURIComponent(cleanName)}/${encodeURIComponent(venue)}/${tile.page}`;
              return <button key={tile.page} className="tile-card" onClick={() => setPreviewOpen(true)}><img src={imageUrl} alt={`Rendered page ${tile.page}`} /><span>p.{tile.page}</span></button>;
            }) : <div className="empty-tiles"><Layers3 size={18} /><span>Run an audit to render page tiles</span></div>}
          </div>
        </div>
      </section>

      {previewOpen && <PDFVisualPreviewModal filename={filename} venue={venue} onClose={() => setPreviewOpen(false)} />}
    </div>
  );
};

export default BacktestLab;
