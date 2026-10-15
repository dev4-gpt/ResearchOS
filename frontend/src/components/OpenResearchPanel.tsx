import { useEffect, useState } from 'react';
import { apiFetch } from '../api';
import './OpenResearchPanel.css';

interface Status {
  installed: boolean;
  enabled: boolean;
  available: boolean;
  version: string | null;
  error?: string;
}
interface Paper {
  id: string;
  title: string;
  abstract: string;
  published: string;
  discovery_url: string;
}
interface Project { id: string; name: string }
interface ProjectDetail { tree: string; runs: string }

async function readResponse<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await apiFetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || 'OpenResearch request failed.');
  return data;
}

export function OpenResearchPanel() {
  const [status, setStatus] = useState<Status | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [detail, setDetail] = useState<ProjectDetail | null>(null);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [searched, setSearched] = useState(false);
  const [query, setQuery] = useState('');
  const [strategy, setStrategy] = useState('keyword');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function refresh() {
    setBusy(true);
    setError('');
    try {
      const next = await readResponse<Status>('/api/openresearch/status');
      setStatus(next);
      setProjects([]);
      setDetail(null);
      if (next.available) {
        const data = await readResponse<{ projects: Project[] }>('/api/openresearch/projects');
        setProjects(data.projects);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not connect to OpenResearch.');
    } finally { setBusy(false); }
  }

  useEffect(() => {
    let active = true;
    async function connect() {
      try {
        const next = await readResponse<Status>('/api/openresearch/status');
        if (!active) return;
        setStatus(next);
        if (next.available) {
          const data = await readResponse<{ projects: Project[] }>('/api/openresearch/projects');
          if (active) setProjects(data.projects);
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : 'Could not connect to OpenResearch.');
      }
    }
    void connect();
    return () => { active = false; };
  }, []);

  async function search(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError('');
    setPapers([]);
    setSearched(false);
    try {
      const data = await readResponse<{ papers: Paper[] }>('/api/openresearch/discover', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, strategy, limit: 10 }),
      });
      setPapers(data.papers);
      setSearched(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Literature search failed.');
    } finally { setBusy(false); }
  }

  async function inspect(projectId: string) {
    setBusy(true);
    setError('');
    setDetail(null);
    try {
      setDetail(await readResponse<ProjectDetail>(`/api/openresearch/projects/${encodeURIComponent(projectId)}`));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not load the project.');
    } finally { setBusy(false); }
  }

  return <section aria-label="OpenResearch" className="openresearch-panel">
    <div>
      <h3>OpenResearch</h3>
      <p>Search alphaXiv literature and inspect experiments from your local OpenResearch workspace.</p>
      <p role="status" className="openresearch-status">{!status ? 'Checking connection…' : status.available
        ? `Connected · ${status.version}. Scout automatically includes keyword and semantic retrieval.`
        : !status.enabled ? 'OpenResearch is disabled in project settings.'
          : status.error || 'Install the OpenResearch CLI, then refresh to connect.'}</p>
      <button onClick={() => void refresh()} disabled={busy}>Refresh connection</button>{' '}
      <a href="http://127.0.0.1:4791" target="_blank" rel="noreferrer">Open local workspace</a>{' · '}
      <a href="https://github.com/alphaXiv/OpenResearch" target="_blank" rel="noreferrer">Setup guide</a>
    </div>
    {error && <p role="alert" style={{ color: '#fca5a5' }}>{error}</p>}
    <form onSubmit={search}>
      <label>Research topic <input value={query} onChange={event => setQuery(event.target.value)}
        required maxLength={2000} placeholder="Find relevant research" /></label>
      <label>Search approach <select value={strategy} onChange={event => setStrategy(event.target.value)}>
        <option value="keyword">Exact keywords</option><option value="embedding">Semantic search</option>
      </select></label>
      <button type="submit" disabled={busy || !status?.available || !query.trim()}>
        {busy ? 'Working…' : 'Search papers'}
      </button>
    </form>
    <p style={{ color: 'var(--text-secondary)' }}>Discovery results are candidates. During a research run,
      the pipeline ingests source papers before using them as manuscript evidence.</p>
    {searched && papers.length === 0 && <p>No matching papers returned.</p>}
    {papers.map(paper => <article key={paper.id}>
      <a href={paper.discovery_url} target="_blank" rel="noreferrer">{paper.title}</a>
      <p className="openresearch-metadata">{paper.published.slice(0, 10)} · {paper.id}</p>
      <details><summary>Read abstract</summary><p>{paper.abstract}</p></details>
    </article>)}
    <div>
      <h4>Local projects</h4>
      {status?.available && projects.length === 0 && <p>No local projects yet. Start OpenResearch
        and import your experiment repository in its workspace.</p>}
      {projects.map(project => <button key={project.id} disabled={busy}
        onClick={() => void inspect(project.id)}>{project.name}</button>)}
      {detail && <div><h4>Experiment tree</h4>
        <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{detail.tree}</pre>
        <h4>Run history</h4><pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{detail.runs}</pre>
      </div>}
    </div>
  </section>;
}
