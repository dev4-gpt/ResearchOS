import React, { useState } from 'react';
import { Search, Sparkles, BookOpen } from 'lucide-react';

interface DashboardProps {
  startResearch: (topic: string) => void;
  isResearching: boolean;
}

const AGENT_TEAM = [
  {
    name: 'Senior Scout Researcher',
    role: 'Literature Discovery',
    desc: 'Crawls databases (arXiv, OpenAlex), filters by impact and citation indexes, and maps the bibliography.',
    color: '#3b82f6', // Blue
  },
  {
    name: 'Lead Analyst',
    role: 'Extraction & Ingestion',
    desc: 'Parses details and abstracts, extracts exact claims, results, and parameters into structured markdown summaries.',
    color: '#10b981', // Emerald
  },
  {
    name: 'Senior Systems Engineer',
    role: 'Technical & Scaling Audit',
    desc: 'Audits algorithmic designs, mathematical equations, computational parameters, and deployment viability.',
    color: '#6366f1', // Indigo
  },
  {
    name: 'Senior Statistician',
    role: 'Methodological Rigor Critic',
    desc: 'Evaluates statistical significance, control sets, sample sizes, baselines, and mathematical proofs.',
    color: '#f59e0b', // Amber
  },
  {
    name: 'Reviewer #2',
    role: 'Peer Review Objections',
    desc: 'Skeptical academic evaluator. Identifies gaps, conflicts with prior art, and highlights rejection risks.',
    color: '#f43f5e', // Rose
  },
  {
    name: 'CEO / Chairman',
    role: 'Consensus Moderator',
    desc: 'Coordinates the council debate, evaluates points of consensus/tension, and drafts the research outline.',
    color: '#8b5cf6', // Violet
  },
  {
    name: 'Senior Research Writer',
    role: 'Journal Publisher',
    desc: 'Drafts the final manuscript in formal academic style (Nature, IEEE, ACM) with inline citation markdown.',
    color: '#ec4899', // Pink
  }
];

const SUGGESTIONS = [
  "Direct Preference Optimization (DPO) vs RLHF scaling limits",
  "Sparse Autoencoders for steering LLM concept activation",
  "Low-Rank Adaptation (LoRA) parameter efficiency in vision-transformers",
  "Self-correcting reasoning loops in mathematical LLMs"
];

const Dashboard: React.FC<DashboardProps> = ({ startResearch, isResearching }) => {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      startResearch(topic.trim());
    }
  };

  return (
    <div style={{ paddingRight: '6px', display: 'flex', flexDirection: 'column', gap: '28px', paddingBottom: '24px' }}>
      
      {/* Hero Welcome Deck */}
      <section className="hero-section glass glow-primary animate-entrance">
        {/* Background gradient orb */}
        <div style={{ position: 'absolute', top: '-50px', right: '-50px', width: '220px', height: '220px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(129,140,248,0.25) 0%, rgba(129,140,248,0) 70%)', filter: 'blur(35px)', pointerEvents: 'none' }}></div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)', fontWeight: '600', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1.5px', fontFamily: 'var(--font-heading)' }}>
          <Sparkles size={14} strokeWidth={1.5} />
          <span>Multi-Agent Research Lab</span>
        </div>
        
        <h2 className="hero-title">
          Accelerate your academic publishing pipeline.
        </h2>
        
        <p style={{ color: 'var(--text-secondary)', fontSize: '15px', maxWidth: '680px', lineHeight: '1.6', fontWeight: '400' }}>
          ResearchingOS runs a full academic debate council to vet scientific literature, construct a structured Obsidian knowledge graph (LLM Wiki), and format professional peer-review grade manuscript drafts.
        </p>

        {/* Input Query form */}
        <form onSubmit={handleSubmit} style={{ marginTop: '12px' }}>
          <div className="search-input-container">
            <Search size={18} strokeWidth={1.5} style={{ color: 'var(--text-secondary)', marginLeft: '16px', flexShrink: 0 }} />
            <input 
              type="text" 
              placeholder="Enter a research question or topic (e.g. DPO vs RLHF in sparse environments)..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={isResearching}
              style={{
                background: 'transparent', border: 'none', color: '#fff', fontSize: '14px', width: '100%', outline: 'none',
                fontFamily: 'var(--font-sans)',
              }}
            />
            <button 
              type="submit" 
              disabled={isResearching || !topic.trim()}
              className="btn-pill"
              style={{ padding: '8px 20px', fontSize: '13px', border: 'none' }}
            >
              <span>{isResearching ? 'Council In Session...' : 'Initiate Council'}</span>
              <div className="btn-icon-wrapper">
                <Sparkles size={12} strokeWidth={2} />
              </div>
            </button>
          </div>
        </form>

        {/* Suggestion Chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '4px', alignItems: 'center' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Suggestions:</span>
          {SUGGESTIONS.map((s, idx) => (
            <button
              key={idx}
              disabled={isResearching}
              onClick={() => setTopic(s)}
              style={{
                background: 'rgba(255,255,255,0.02)', border: '1px solid var(--border-color)', color: 'var(--text-secondary)', padding: '6px 14px', borderRadius: '9999px', fontSize: '11px', cursor: 'pointer',
                transition: 'var(--transition-fast)', fontFamily: 'var(--font-sans)', fontWeight: '500'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.06)';
                e.currentTarget.style.borderColor = 'rgba(129,140,248,0.3)';
                e.currentTarget.style.color = '#fff';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.02)';
                e.currentTarget.style.borderColor = 'var(--border-color)';
                e.currentTarget.style.color = 'var(--text-secondary)';
              }}
            >
              {s}
            </button>
          ))}
        </div>
      </section>

      {/* Agents Roster */}
      <section className="animate-entrance" style={{ animationDelay: '0.1s' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '20px', fontWeight: '800', marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '10px', letterSpacing: '-0.3px' }}>
          <BookOpen size={18} strokeWidth={1.5} color="var(--primary)" />
          <span>Research Institute Staff</span>
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
          {AGENT_TEAM.map((agent, index) => (
            <div key={index} className="double-bezel-outer tilt-3d" style={{ height: '100%' }}>
              <div className="double-bezel-inner">
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: agent.color, boxShadow: `0 0 10px ${agent.color}` }}></div>
                  <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', fontFamily: 'var(--font-heading)' }}>{agent.name}</h4>
                </div>
                <div style={{ fontSize: '10px', color: agent.color, fontWeight: '700', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '8px' }}>
                  {agent.role}
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                  {agent.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Pipeline Lifecycle Timeline */}
      <section className="glass animate-entrance" style={{ padding: '28px', display: 'flex', flexDirection: 'column', gap: '20px', animationDelay: '0.2s' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '18px', fontWeight: '800', letterSpacing: '-0.2px' }}>Research Pipeline Lifecycle</h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'var(--primary-glow)', color: 'var(--primary)', border: '1px solid rgba(129,140,248,0.2)', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', fontSize: '12px', fontWeight: '800', justifyContent: 'center' }}>1</div>
              <span style={{ fontSize: '13px', fontWeight: '700', fontFamily: 'var(--font-heading)' }}>Discovery</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>Scout searches academic databases and aggregates core paper metadata.</p>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'rgba(52,211,153,0.1)', color: 'var(--success)', border: '1px solid rgba(52,211,153,0.2)', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', fontSize: '12px', fontWeight: '800', justifyContent: 'center' }}>2</div>
              <span style={{ fontSize: '13px', fontWeight: '700', fontFamily: 'var(--font-heading)' }}>Vault Extraction</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>Analyst extracts claims and datasets, generating markdown files in the local vault.</p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'rgba(251,113,133,0.1)', color: 'var(--danger)', border: '1px solid rgba(251,113,133,0.2)', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', fontSize: '12px', fontWeight: '800', justifyContent: 'center' }}>3</div>
              <span style={{ fontSize: '13px', fontWeight: '700', fontFamily: 'var(--font-heading)' }}>Council Audit</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>Systems Engineer, Statistician, and Reviewer #2 write parallel math/technical audits.</p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'rgba(251,191,36,0.1)', color: 'var(--warning)', border: '1px solid rgba(251,191,36,0.2)', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', fontSize: '12px', fontWeight: '800', justifyContent: 'center' }}>4</div>
              <span style={{ fontSize: '13px', fontWeight: '700', fontFamily: 'var(--font-heading)' }}>CEO Synthesis</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>The Chairman moderates the debate, analyzes conflicts, and writes the review outline.</p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'rgba(236,72,153,0.1)', color: '#ec4899', border: '1px solid rgba(236,72,153,0.2)', width: '32px', height: '32px', borderRadius: '50%', display: 'flex', alignItems: 'center', fontSize: '12px', fontWeight: '800', justifyContent: 'center' }}>5</div>
              <span style={{ fontSize: '13px', fontWeight: '700', fontFamily: 'var(--font-heading)' }}>Journal Drafting</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>The Writer formats the final document into a high-level academic paper ready for HITL review.</p>
          </div>
        </div>
      </section>
      
    </div>
  );
};

export default Dashboard;
