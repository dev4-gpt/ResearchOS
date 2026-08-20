import React, { useState } from 'react';
import { Search, Sparkles, BookOpen } from 'lucide-react';
import Laptop3DWorkspace from './Laptop3DWorkspace';

interface DashboardProps {
  startResearch: (topic: string, venue: string, length: string) => void;
  isResearching: boolean;
  onEnterWorkspace?: () => void;
}

const AGENT_TEAM = [
  {
    name: 'Senior Scout Researcher',
    role: 'Literature Discovery',
    desc: 'Crawls databases (arXiv, OpenAlex), filters by impact and citation indexes, and maps the bibliography.',
    badgeClass: 'minimalist-badge-blue',
  },
  {
    name: 'Lead Analyst',
    role: 'Extraction & Ingestion',
    desc: 'Parses details and abstracts, extracts exact claims, results, and parameters into structured markdown summaries.',
    badgeClass: 'minimalist-badge-green',
  },
  {
    name: 'Senior Systems Engineer',
    role: 'Technical & Scaling Audit',
    desc: 'Audits algorithmic designs, mathematical equations, computational parameters, and deployment viability.',
    badgeClass: 'minimalist-badge-blue',
  },
  {
    name: 'Senior Statistician',
    role: 'Methodological Rigor Critic',
    desc: 'Evaluates statistical significance, control sets, sample sizes, baselines, and mathematical proofs.',
    badgeClass: 'minimalist-badge-amber',
  },
  {
    name: 'Reviewer #2',
    role: 'Peer Review Objections',
    desc: 'Skeptical academic evaluator. Identifies gaps, conflicts with prior art, and highlights rejection risks.',
    badgeClass: 'minimalist-badge-red',
  },
  {
    name: 'CEO / Chairman',
    role: 'Consensus Moderator',
    desc: 'Coordinates the council debate, evaluates points of consensus/tension, and drafts the research outline.',
    badgeClass: 'minimalist-badge-amber',
  },
  {
    name: 'Senior Research Writer',
    role: 'Journal Publisher',
    desc: 'Drafts the final manuscript in formal academic style (Nature, IEEE, ACM) with inline citation markdown.',
    badgeClass: 'minimalist-badge-green',
  }
];

const SUGGESTIONS = [
  "Direct Preference Optimization (DPO) vs RLHF scaling limits",
  "Sparse Autoencoders for steering LLM concept activation",
  "Low-Rank Adaptation (LoRA) parameter efficiency in vision-transformers",
  "Self-correcting reasoning loops in mathematical LLMs"
];

const Dashboard: React.FC<DashboardProps> = ({ startResearch, isResearching, onEnterWorkspace }) => {
  const [topic, setTopic] = useState('');
  const [targetVenue, setTargetVenue] = useState('IEEEtran');
  const [targetLength, setTargetLength] = useState('short_camera_ready');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      startResearch(topic.trim(), targetVenue, targetLength);
    }
  };

  return (
    <div style={{ paddingRight: '6px', display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '24px' }}>

      {/* Minimalist Hero Bento Header */}
      <section className="minimalist-card animate-entrance">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="minimalist-badge-amber">Multi-Agent Engine</span>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>V1.0.0 Pro</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <kbd className="kbd-shortcut">↵ Enter</kbd>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Launch</span>
          </div>
        </div>

        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '24px', fontWeight: '700', color: '#ffffff', letterSpacing: '-0.02em', marginBottom: '8px' }}>
          Accelerate your academic publishing pipeline.
        </h2>

        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', maxWidth: '680px', lineHeight: '1.6', fontWeight: '400', marginBottom: '20px' }}>
          ResearchingOS runs a 7-agent debate council to vet scientific literature, construct a structured Obsidian knowledge graph (LLM Wiki), and format publication-ready IEEE/ACM LaTeX manuscripts.
        </p>

        {/* Minimalist Input Form */}
        <form onSubmit={handleSubmit}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              background: 'rgba(10, 12, 18, 0.9)',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              borderRadius: '8px',
              padding: '6px 12px',
              gap: '10px'
            }}
          >
            <Search size={16} strokeWidth={1.5} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <input
              type="text"
              placeholder="Enter a research topic or paper title..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={isResearching}
              style={{
                background: 'transparent', border: 'none', color: '#ffffff', fontSize: '13px', width: '100%', outline: 'none',
                fontFamily: 'var(--font-sans)',
              }}
            />
            <button
              type="submit"
              disabled={isResearching || !topic.trim()}
              style={{
                padding: '7px 16px',
                fontSize: '12px',
                fontWeight: '700',
                background: isResearching || !topic.trim() ? 'rgba(255,255,255,0.06)' : '#ffffff',
                color: isResearching || !topic.trim() ? 'var(--text-muted)' : '#0b0c10',
                border: 'none',
                borderRadius: '6px',
                cursor: isResearching || !topic.trim() ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                fontFamily: 'var(--font-heading)',
                transition: 'all 0.15s ease'
              }}
            >
              <Sparkles size={13} />
              <span>{isResearching ? 'Deliberating...' : 'Launch Council'}</span>
            </button>
          </div>

          {/* Venue & Target Length Selectors */}
          <div style={{ display: 'flex', gap: '12px', marginTop: '12px', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(255,255,255,0.04)', padding: '5px 10px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '600' }}>Venue:</span>
              <select
                value={targetVenue}
                onChange={(e) => setTargetVenue(e.target.value)}
                disabled={isResearching}
                style={{ background: 'transparent', color: '#ffffff', border: 'none', outline: 'none', fontSize: '11px', cursor: 'pointer', fontWeight: '600' }}
              >
                <option value="IEEEtran" style={{ background: '#111', color: '#fff' }}>IEEEtran (Transactions / Short)</option>
                <option value="NeurIPS" style={{ background: '#111', color: '#fff' }}>NeurIPS (Conference 9p)</option>
                <option value="ICML" style={{ background: '#111', color: '#fff' }}>ICML (Conference 8p)</option>
                <option value="CVPR" style={{ background: '#111', color: '#fff' }}>CVPR (Conference 8p)</option>
                <option value="ACL" style={{ background: '#111', color: '#fff' }}>ACL / ARR (Short/Long)</option>
                <option value="ACM" style={{ background: '#111', color: '#fff' }}>ACM Computing Surveys</option>
              </select>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(255,255,255,0.04)', padding: '5px 10px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '600' }}>Length:</span>
              <select
                value={targetLength}
                onChange={(e) => setTargetLength(e.target.value)}
                disabled={isResearching}
                style={{ background: 'transparent', color: '#ffffff', border: 'none', outline: 'none', fontSize: '11px', cursor: 'pointer', fontWeight: '600' }}
              >
                <option value="short_camera_ready" style={{ background: '#111', color: '#fff' }}>Short Camera-Ready (4 Pages)</option>
                <option value="full_journal" style={{ background: '#111', color: '#fff' }}>Full Journal / Survey (12 Pages)</option>
              </select>
            </div>
          </div>
        </form>

        {/* Quick Topic Chips */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginTop: '14px' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '500' }}>Quick Topics:</span>
          {SUGGESTIONS.map((s, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setTopic(s)}
              style={{
                background: 'rgba(255,255,255,0.03)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '6px',
                padding: '3px 8px',
                fontSize: '11px',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              {s}
            </button>
          ))}
        </div>
      </section>

      {/* 3D SCROLL-DRIVEN SPATIAL STUDIO WORKSPACE */}
      <section className="animate-entrance" style={{ borderRadius: '12px', overflow: 'visible' }}>
        <Laptop3DWorkspace onEnterWorkspace={onEnterWorkspace || (() => {})} />
      </section>

      {/* Minimalist Agents Roster Bento Grid */}
      <section className="animate-entrance" style={{ animationDelay: '0.1s' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '18px', fontWeight: '700', color: '#ffffff', letterSpacing: '-0.01em', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <BookOpen size={16} strokeWidth={1.5} color="var(--primary)" />
            <span>Council Roster</span>
          </h3>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>7 Persona Agents Active</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(270px, 1fr))', gap: '12px' }}>
          {AGENT_TEAM.map((agent, index) => (
            <div key={index} className="minimalist-card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <h4 style={{ fontSize: '13px', fontWeight: '700', color: '#ffffff', fontFamily: 'var(--font-heading)' }}>{agent.name}</h4>
                <span className={agent.badgeClass}>{agent.role}</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                {agent.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Minimalist Pipeline Lifecycle */}
      <section className="minimalist-card animate-entrance" style={{ animationDelay: '0.2s' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16px', fontWeight: '700', color: '#ffffff', marginBottom: '16px', letterSpacing: '-0.01em' }}>
          Pipeline Execution Stages
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '16px' }}>
          {[
            { num: '01', title: 'Discovery', desc: 'Scout searches academic repositories & filters by Reciprocal Rank Fusion.' },
            { num: '02', title: 'Vault Extraction', desc: 'Analyst extracts core claims into structured Obsidian markdown notes.' },
            { num: '03', title: 'Council Audit', desc: 'Systems Engineer, Statistician, Reviewer #2 write parallel audits.' },
            { num: '04', title: 'CEO Synthesis', desc: 'Chairman moderates boardroom debate & synthesizes final outline.' },
            { num: '05', title: 'Journal Drafting', desc: 'Writer formats 15+ page IEEE/ACM LaTeX manuscript bundle.' }
          ].map((stage) => (
            <div key={stage.num} style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--primary)', fontWeight: '700' }}>{stage.num}</span>
                <span style={{ fontSize: '12px', fontWeight: '700', color: '#ffffff', fontFamily: 'var(--font-heading)' }}>{stage.title}</span>
              </div>
              <p style={{ fontSize: '11px', color: 'var(--text-secondary)', lineHeight: '1.45' }}>{stage.desc}</p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
};

export default Dashboard;
