import { useEffect, useState } from 'react';
import { apiFetch } from '../api';
import './OpenResearchPanel.css';

interface Source { id: string; repository: string; url: string; revision: string; license_note: string }
interface Skill {
  id: string; name: string; description: string; source: string; stage: string;
  roles: string[]; status: string; active: boolean; mode: string; guidance: string;
  upstream_url: string; content?: string | null;
}
interface Catalog {
  summary: { enabled: boolean; total_skills: number; installed: number; active: number; sources: Source[]; roles: string[] };
  skills: Skill[];
}

export function ResearchSkillsPanel() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [source, setSource] = useState('');
  const [role, setRole] = useState('');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<Skill | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const res = await apiFetch('/api/skills/research');
        if (!res.ok) throw new Error('Could not load the research skill catalog.');
        const data: Catalog = await res.json();
        if (active) setCatalog(data);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : 'Could not load research skills.');
      }
    }
    void load();
    return () => { active = false; };
  }, []);

  async function inspect(skill: Skill) {
    setLoading(true);
    setError('');
    try {
      const res = await apiFetch(`/api/skills/research/${encodeURIComponent(skill.id)}`);
      if (!res.ok) throw new Error('Could not load this skill.');
      setSelected(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not read skill.');
    } finally { setLoading(false); }
  }

  const skills = catalog?.skills.filter(skill => (!source || skill.source === source)
    && (!role || skill.roles.includes(role))
    && `${skill.name} ${skill.description} ${skill.stage}`.toLowerCase().includes(query.toLowerCase())) || [];

  return <section className="openresearch-panel" aria-label="Research skills">
    <div><h3>Research Skills</h3>
      <p>Research methods from three pinned skill collections, mapped to the council and manuscript workflow.</p>
      {catalog && <p role="status" className="openresearch-status">
        {catalog.summary.installed} of {catalog.summary.total_skills} installed · {catalog.summary.active} advisory skills enabled
        {!catalog.summary.enabled && ' · Integration disabled'}
      </p>}
    </div>
    {error && <p role="alert">{error}</p>}
    {!catalog && !error && <p>Loading research methods…</p>}
    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
      <label>Collection<select value={source} onChange={e => setSource(e.target.value)}>
        <option value="">All collections</option>
        {catalog?.summary.sources.map(item => <option key={item.id} value={item.id}>{item.repository}</option>)}
      </select></label>
      <label>Council role<select value={role} onChange={e => setRole(e.target.value)}>
        <option value="">All roles</option>
        {catalog?.summary.roles.map(item => <option key={item}>{item}</option>)}
      </select></label>
      <label>Search skills<input value={query} onChange={e => setQuery(e.target.value)} placeholder="Statistics, citations, review…" /></label>
    </div>
    <p>Advisory skills supply reviewed method guidance to model calls. Reference skills can be inspected here.
      Existing citation, evidence, and publication checks still decide readiness.</p>
    {catalog && skills.length === 0 && <p>No matching skills.</p>}
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))', gap: 12 }}>
      {skills.map(skill => <article key={skill.id}>
        <h4>{skill.name}</h4><p>{skill.stage} · {skill.status} · {skill.mode}</p>
        <p className="openresearch-metadata">{catalog?.summary.sources.find(item => item.id === skill.source)?.repository}</p>
        <p>{skill.roles.length ? skill.roles.join(', ') : 'Reference library'}</p>
        <p>{skill.guidance}</p>
        <button disabled={loading} onClick={() => void inspect(skill)}>Inspect {skill.name}</button>
      </article>)}
    </div>
    {selected && <section aria-label="Skill details">
      <h4>{selected.name}</h4><button onClick={() => setSelected(null)}>Close details</button>{' '}
      <a href={selected.upstream_url} target="_blank" rel="noreferrer">Pinned upstream source</a>
      <p>{selected.guidance}</p>
      <details><summary>Original reference document</summary>
        <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{selected.content || `Reference unavailable (${selected.status}).`}</pre>
      </details>
    </section>}
    <details><summary>Sources and licensing</summary>
      {catalog?.summary.sources.map(item => <div key={item.id}>
        <a href={item.url} target="_blank" rel="noreferrer">{item.repository}</a>
        <p>Revision {item.revision.slice(0, 12)} · {item.license_note}</p>
      </div>)}
    </details>
  </section>;
}
