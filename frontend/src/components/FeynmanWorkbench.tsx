import React, { useState, useEffect } from 'react';
import {
  Code,
  BookOpen,
  ShieldAlert,
  Sparkles,
  Play,
  RotateCw,
  CheckCircle2,
  XCircle,
  Cpu,
  Terminal,
  Lightbulb,
  Mic,
  Volume2,
  FolderSync,
  Layers,
  ExternalLink,
  FileText,
} from 'lucide-react';
import { apiFetch } from '../api';

interface AuditItem {
  claim_text: string;
  paper_value: string;
  code_match: string | null;
  code_file: string;
  line_number: number | null;
  status: 'MATCH' | 'NOT_IN_CODE' | 'DISCREPANCY';
  detail: string;
}

interface AuditResult {
  total_claims_audited: number;
  matched_in_code: number;
  code_provenance_score: number;
  files_scanned: string[];
  audit_items: AuditItem[];
}

interface ReviewItem {
  severity: 'BLOCKER' | 'MAJOR' | 'MINOR';
  category: string;
  title: string;
  description: string;
  manuscript_location: string;
  suggested_action: string;
}

interface ReviewResult {
  venue: string;
  recommendation: 'ACCEPT' | 'WEAK_ACCEPT' | 'REVISE' | 'REJECT';
  rejection_risk_score: number;
  blocker_count: number;
  major_count: number;
  minor_count: number;
  review_items: ReviewItem[];
}

interface LitMatrixResult {
  topic: string;
  papers_reviewed: number;
  consensus_findings: Array<{ topic: string; assertion: string; source: string }>;
  active_disagreements: Array<{ topic: string; contending_view: string; source: string }>;
  open_research_questions: Array<{ paper: string; citation: string; gap: string }>;
}

interface AutoresearchResult {
  draft_name: string;
  target_venue: string;
  initial_fitness: number;
  final_fitness: number;
  iterations_run: number;
  kept_count: number;
  discarded_count: number;
  history: Array<{
    iteration: number;
    mutation_type: string;
    fitness_before: number;
    fitness_after: number;
    decision: 'KEEP' | 'DISCARD';
    rationale: string;
  }>;
}

export const FeynmanWorkbench: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'audit' | 'lit' | 'review' | 'autoresearch' | 'fx' | 'evomap' | 'voice' | 'ecc' | 'slop' | 'slides' | 'diagram' | 'skills'>('audit');
  const [drafts, setDrafts] = useState<string[]>([]);
  const [selectedDraft, setSelectedDraft] = useState<string>('');
  const [selectedVenue, setSelectedVenue] = useState<string>('IEEEtran');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // States for sub-features
  const [auditResult, setAuditResult] = useState<AuditResult | null>(null);
  const [litResult, setLitResult] = useState<LitMatrixResult | null>(null);
  const [reviewResult, setReviewResult] = useState<ReviewResult | null>(null);
  const [autoresearchResult, setAutoresearchResult] = useState<AutoresearchResult | null>(null);
  const [litTopic, setLitTopic] = useState<string>('Multi-Agent Systems & Literature Review');

  // States for Vercel Labs fx Engine
  const [fxStatus, setFxStatus] = useState<{
    installed: boolean;
    mode: string;
    binary_path: string;
    version: string;
    acp_supported: boolean;
    mcp_client_capable: boolean;
    description: string;
  } | null>(null);
  const [fxPrompt, setFxPrompt] = useState<string>('Analyze linear attention vs state space models parameter scaling');
  const [fxResult, setFxResult] = useState<any | null>(null);

  // States for EvoMap/AutoResearch
  const [evoTopic, setEvoTopic] = useState<string>('Dynamic Sparse Attention');
  const [evoDomainB, setEvoDomainB] = useState<string>('State Space Models');
  const [evoIdeas, setEvoIdeas] = useState<any[]>([]);
  const [pilotResults, setPilotResults] = useState<Record<string, any>>({});
  const [negativeResults, setNegativeResults] = useState<any[]>([]);

  // States for VoxCPM Voice Control
  const [voiceInput, setVoiceInput] = useState<string>('Run checkmate audit on latest draft');
  const [voiceParsed, setVoiceParsed] = useState<any | null>(null);
  const [voicePersona, setVoicePersona] = useState<string>('chairman');
  const [voiceAudioBase64, setVoiceAudioBase64] = useState<string | null>(null);
  const [voiceEngineStatus, setVoiceEngineStatus] = useState<any | null>(null);

  // States for ECC Department Skills
  const [eccSkills, setEccSkills] = useState<any[]>([]);
  const [eccStatus, setEccStatus] = useState<any | null>(null);
  const [eccDeptFilter, setEccDeptFilter] = useState<string>('');
  const [eccSearchQuery, setEccSearchQuery] = useState<string>('');
  const [selectedEccSkill, setSelectedEccSkill] = useState<any | null>(null);
  const [eccSyncMsg, setEccSyncMsg] = useState<string | null>(null);

  // States for Academic Voice (Stop-Slop & Humanizer)
  const [slopText, setSlopText] = useState<string>('');
  const [slopResult, setSlopResult] = useState<any | null>(null);
  const [humanizeResult, setHumanizeResult] = useState<any | null>(null);

  // States for Conference Slides (frontend-slides)
  const [slidesResult, setSlidesResult] = useState<any | null>(null);

  // States for Diagram Generator (diagram-design)
  const [diagramTitle, setDiagramTitle] = useState<string>('ResearchingOS Multi-Agent Autonomous Council Pipeline');
  const [diagramResult, setDiagramResult] = useState<any | null>(null);

  // States for Universal Skills (Zero Duplication)
  const [universalSkills, setUniversalSkills] = useState<any[]>([]);
  const [universalSummary, setUniversalSummary] = useState<any | null>(null);
  const [skillCategoryFilter, setSkillCategoryFilter] = useState<string>('');
  const [selectedUniversalSkill, setSelectedUniversalSkill] = useState<any | null>(null);

  useEffect(() => {
    fetchDrafts();
    fetchFxStatus();
    fetchVoiceStatus();
    fetchEccSkills();
    fetchNegativeResults();
    fetchUniversalSkills();
  }, []);

  const fetchFxStatus = async () => {
    try {
      const res = await apiFetch('/api/fx/status');
      if (res.ok) {
        setFxStatus(await res.json());
      }
    } catch (e) {
      console.error('Failed to fetch fx status:', e);
    }
  };

  const runFxResearch = async () => {
    if (!fxPrompt) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/fx/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: fxPrompt }),
      });
      if (res.ok) {
        setFxResult(await res.json());
      } else {
        setError('Failed to dispatch fx subagent');
      }
    } catch (e: any) {
      setError(e.message || 'Error executing fx subagent');
    } finally {
      setLoading(false);
    }
  };

  const fetchVoiceStatus = async () => {
    try {
      const res = await apiFetch('/api/voice/status');
      if (res.ok) setVoiceEngineStatus(await res.json());
    } catch (e) {
      console.error('Failed to fetch voice status:', e);
    }
  };

  const fetchNegativeResults = async () => {
    try {
      const res = await apiFetch('/api/evomap/negative-results');
      if (res.ok) {
        const data = await res.json();
        setNegativeResults(data.negative_results || []);
      }
    } catch (e) {
      console.error('Failed to fetch negative results:', e);
    }
  };

  const fetchEccSkills = async () => {
    try {
      let url = '/api/ecc/skills?limit=100';
      if (eccDeptFilter) url += `&dept=${encodeURIComponent(eccDeptFilter)}`;
      if (eccSearchQuery) url += `&query=${encodeURIComponent(eccSearchQuery)}`;
      const res = await apiFetch(url);
      if (res.ok) {
        const data = await res.json();
        setEccStatus(data.status);
        setEccSkills(data.skills || []);
      }
    } catch (e) {
      console.error('Failed to fetch ECC skills:', e);
    }
  };

  const runEvoForge = async () => {
    if (!evoTopic) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/evomap/forge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: evoTopic, domain_b: evoDomainB, count: 2 }),
      });
      if (res.ok) {
        const data = await res.json();
        setEvoIdeas(data.ideas || []);
        fetchNegativeResults();
      } else {
        setError('Failed to forge ideas with EvoMap');
      }
    } catch (e: any) {
      setError(e.message || 'EvoMap execution error');
    } finally {
      setLoading(false);
    }
  };

  const runEvoPilot = async (idea: any) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/evomap/pilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea }),
      });
      if (res.ok) {
        const data = await res.json();
        setPilotResults((prev) => ({ ...prev, [idea.idea_id]: data }));
        fetchNegativeResults();
      } else {
        setError('Failed to run pilot gate');
      }
    } catch (e: any) {
      setError(e.message || 'Pilot gate error');
    } finally {
      setLoading(false);
    }
  };

  const runVoiceCommand = async () => {
    if (!voiceInput) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/voice/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: voiceInput }),
      });
      if (res.ok) {
        const data = await res.json();
        setVoiceParsed(data);
        if (data.spoken_response) {
          runVoiceSynthesize(data.spoken_response, voicePersona);
        }
      }
    } catch (e: any) {
      setError(e.message || 'Voice parsing error');
    } finally {
      setLoading(false);
    }
  };

  const runVoiceSynthesize = async (textToSpeak?: string, personaToUse?: string) => {
    const text = textToSpeak || voiceInput;
    const persona = personaToUse || voicePersona;
    if (!text) return;
    setLoading(true);
    try {
      const res = await apiFetch('/api/voice/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, persona }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.audio_base64) {
          setVoiceAudioBase64(data.audio_base64);
        }
      }
    } catch (e: any) {
      console.error('Voice synthesis error:', e);
    } finally {
      setLoading(false);
    }
  };

  const syncEccSkills = async () => {
    setLoading(true);
    setEccSyncMsg(null);
    try {
      const res = await apiFetch('/api/ecc/sync', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setEccSyncMsg(`Synced ${data.copied_count} core skills to .agents/skills/ecc/!`);
        fetchEccSkills();
      }
    } catch (e: any) {
      setError(e.message || 'Failed to sync ECC skills');
    } finally {
      setLoading(false);
    }
  };

  const fetchDrafts = async () => {
    try {
      const res = await apiFetch('/api/vault/files?category=drafts');
      if (res.ok) {
        const data = await res.json();
        const names = data.map((d: any) => d.name || d.filename || d);
        setDrafts(names);
        if (names.length > 0) setSelectedDraft(names[0]);
      }
    } catch (e) {
      console.error('Failed to load drafts:', e);
    }
  };

  const runCodeAudit = async () => {
    if (!selectedDraft) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/feynman/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_filename: selectedDraft }),
      });
      if (!res.ok) throw new Error(`Audit failed: ${res.statusText}`);
      const data = await res.json();
      setAuditResult(data);
    } catch (e: any) {
      setError(e.message || 'Audit execution error');
    } finally {
      setLoading(false);
    }
  };

  const runLitMatrix = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/feynman/lit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: litTopic }),
      });
      if (!res.ok) throw new Error(`Literature synthesis failed: ${res.statusText}`);
      const data = await res.json();
      setLitResult(data);
    } catch (e: any) {
      setError(e.message || 'Literature synthesis error');
    } finally {
      setLoading(false);
    }
  };

  const runPeerReview = async () => {
    if (!selectedDraft) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/feynman/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_filename: selectedDraft, venue: selectedVenue }),
      });
      if (!res.ok) throw new Error(`Peer review failed: ${res.statusText}`);
      const data = await res.json();
      setReviewResult(data);
    } catch (e: any) {
      setError(e.message || 'Peer review error');
    } finally {
      setLoading(false);
    }
  };

  const runAutoresearch = async () => {
    if (!selectedDraft) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/feynman/autoresearch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          draft_filename: selectedDraft,
          venue: selectedVenue,
          max_iterations: 3,
        }),
      });
      if (!res.ok) throw new Error(`Autoresearch failed: ${res.statusText}`);
      const data = await res.json();
      setAutoresearchResult(data);
    } catch (e: any) {
      setError(e.message || 'Autoresearch loop error');
    } finally {
      setLoading(false);
    }
  };

  const fetchUniversalSkills = async (cat?: string) => {
    try {
      const url = cat ? `/api/skills/universal?category=${encodeURIComponent(cat)}` : '/api/skills/universal';
      const res = await apiFetch(url);
      if (res.ok) {
        const data = await res.json();
        setUniversalSummary(data.summary);
        setUniversalSkills(data.skills || []);
      }
    } catch (e) {
      console.error('Failed to fetch universal skills:', e);
    }
  };

  const runSlopAudit = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = slopText.trim() ? { text: slopText } : { draft_filename: selectedDraft };
      const res = await apiFetch('/api/slop/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Slop audit failed');
      setSlopResult(await res.json());
    } catch (e: any) {
      setError(e.message || 'Error running anti-slop audit');
    } finally {
      setLoading(false);
    }
  };

  const runSlopHumanize = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = slopText.trim() ? { text: slopText } : { draft_filename: selectedDraft };
      const res = await apiFetch('/api/slop/humanize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Humanize failed');
      setHumanizeResult(await res.json());
    } catch (e: any) {
      setError(e.message || 'Error humanizing prose');
    } finally {
      setLoading(false);
    }
  };

  const runGenerateSlides = async () => {
    if (!selectedDraft) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/slides/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_filename: selectedDraft, venue: selectedVenue }),
      });
      if (!res.ok) throw new Error('Slides generation failed');
      setSlidesResult(await res.json());
    } catch (e: any) {
      setError(e.message || 'Error generating conference slides');
    } finally {
      setLoading(false);
    }
  };

  const runGenerateDiagram = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/api/diagram/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: diagramTitle }),
      });
      if (!res.ok) throw new Error('Diagram generation failed');
      setDiagramResult(await res.json());
    } catch (e: any) {
      setError(e.message || 'Error generating architecture diagram');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1280px', margin: '0 auto', color: 'var(--text-primary)' }}>
      {/* Header Banner */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Cpu size={28} color="#38bdf8" />
            <h1 style={{ fontSize: '24px', fontWeight: '700', margin: 0 }}>Feynman AI Research Assistant</h1>
            <span style={{ fontSize: '11px', background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', padding: '2px 8px', borderRadius: '12px', fontWeight: '600' }}>
              companion-inc/feynman
            </span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', margin: '6px 0 0 0' }}>
            Multi-agent research CLI & audit engine: paper-to-code verification, consensus mapping, and Karpathy hill-climbing loops.
          </p>
        </div>

        {/* Global Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <select
            value={selectedDraft}
            onChange={(e) => setSelectedDraft(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              color: 'var(--text-primary)',
              fontSize: '13px',
              minWidth: '220px',
            }}
          >
            {drafts.map((d) => (
              <option key={d} value={d} style={{ background: '#111827', color: '#fff' }}>
                {d.replace('.md', '')}
              </option>
            ))}
          </select>

          <select
            value={selectedVenue}
            onChange={(e) => setSelectedVenue(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              color: 'var(--text-primary)',
              fontSize: '13px',
            }}
          >
            <option value="IEEEtran" style={{ background: '#111827', color: '#fff' }}>IEEEtran (4p)</option>
            <option value="ACM" style={{ background: '#111827', color: '#fff' }}>ACM Conf</option>
            <option value="NeurIPS" style={{ background: '#111827', color: '#fff' }}>NeurIPS (9p)</option>
            <option value="ICML" style={{ background: '#111827', color: '#fff' }}>ICML (8p)</option>
          </select>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', marginBottom: '20px', overflowX: 'auto', paddingBottom: '4px' }}>
        {[
          { id: 'audit', label: 'Paper-to-Code (/audit)', icon: Code },
          { id: 'slop', label: 'Anti-Slop (/slop)', icon: FileText },
          { id: 'slides', label: '16:9 Slides (/slides)', icon: Play },
          { id: 'diagram', label: 'Diagrams (/diagram)', icon: Cpu },
          { id: 'skills', label: 'Universal Skills', icon: Layers },
          { id: 'lit', label: 'Lit Matrix (/lit)', icon: BookOpen },
          { id: 'review', label: 'Peer Review (/review)', icon: ShieldAlert },
          { id: 'autoresearch', label: 'Autoresearch', icon: Sparkles },
          { id: 'fx', label: 'fx Engine', icon: Terminal },
          { id: 'evomap', label: 'Idea Forge', icon: Lightbulb },
          { id: 'voice', label: 'Voice Control', icon: Mic },
          { id: 'ecc', label: 'ECC Catalog', icon: Layers },
        ].map((tab) => {
          const Icon = tab.icon;
          const active = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 16px',
                background: 'transparent',
                border: 'none',
                borderBottom: active ? '2px solid #38bdf8' : '2px solid transparent',
                color: active ? '#38bdf8' : 'var(--text-secondary)',
                fontWeight: active ? '600' : '400',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              <Icon size={16} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {error && (
        <div style={{ padding: '12px 16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#f87171', marginBottom: '16px', fontSize: '13px' }}>
          {error}
        </div>
      )}

      {/* TAB 1: Paper-to-Code Audit */}
      {activeTab === 'audit' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Paper-to-Code Static AST Audit</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Verifies that numerical constants and hyperparameters stated in the paper match definitions in experiment scripts.
              </p>
            </div>
            <button
              onClick={runCodeAudit}
              disabled={loading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? <RotateCw size={14} className="animate-spin" /> : <Play size={14} />}
              <span>Run Code Audit</span>
            </button>
          </div>

          {auditResult && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '20px' }}>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Code Provenance Score</div>
                  <div style={{ fontSize: '24px', fontWeight: '700', color: auditResult.code_provenance_score >= 50 ? '#34d399' : '#f87171' }}>
                    {auditResult.code_provenance_score}%
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Matched Code Constants</div>
                  <div style={{ fontSize: '24px', fontWeight: '700', color: '#38bdf8' }}>
                    {auditResult.matched_in_code} / {auditResult.total_claims_audited}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Scanned Experiment Files</div>
                  <div style={{ fontSize: '13px', fontWeight: '500', marginTop: '6px', color: '#a78bfa' }}>
                    {auditResult.files_scanned.join(', ') || 'scripts/experiments/*.py'}
                  </div>
                </div>
              </div>

              <div className="glass" style={{ borderRadius: '8px', overflow: 'hidden' }}>
                <div style={{ padding: '12px 16px', background: 'rgba(255, 255, 255, 0.03)', fontWeight: '600', fontSize: '13px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  Detailed Claim Provenance Mappings
                </div>
                <div style={{ maxHeight: '420px', overflowY: 'auto' }}>
                  {auditResult.audit_items.map((item, idx) => (
                    <div key={idx} style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255,255,255,0.03)', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                      {item.status === 'MATCH' ? <CheckCircle2 size={16} color="#34d399" style={{ flexShrink: 0, marginTop: '2px' }} /> : <XCircle size={16} color="#f87171" style={{ flexShrink: 0, marginTop: '2px' }} />}
                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontWeight: '600', fontSize: '13px', color: item.status === 'MATCH' ? '#34d399' : '#f87171' }}>
                            {item.paper_value}
                          </span>
                          <span style={{ fontSize: '11px', padding: '1px 6px', borderRadius: '4px', background: item.status === 'MATCH' ? 'rgba(52,211,153,0.15)' : 'rgba(248,113,113,0.15)', color: item.status === 'MATCH' ? '#34d399' : '#f87171' }}>
                            {item.status}
                          </span>
                        </div>
                        <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                          "{item.claim_text}"
                        </div>
                        {item.code_match && (
                          <div style={{ fontSize: '12px', fontFamily: 'monospace', color: '#a78bfa', marginTop: '4px' }}>
                            Code: {item.code_match} ({item.code_file}:{item.line_number})
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: Literature Matrix */}
      {activeTab === 'lit' && (
        <div>
          <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
            <input
              type="text"
              value={litTopic}
              onChange={(e) => setLitTopic(e.target.value)}
              placeholder="Enter literature research topic..."
              style={{
                flex: 1,
                padding: '8px 12px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: 'var(--text-primary)',
                fontSize: '13px',
              }}
            />
            <button
              onClick={runLitMatrix}
              disabled={loading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? <RotateCw size={14} className="animate-spin" /> : <Play size={14} />}
              <span>Synthesize Matrix</span>
            </button>
          </div>

          {litResult && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
              <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600', color: '#34d399' }}>Empirical Consensus</h4>
                {litResult.consensus_findings.map((c, idx) => (
                  <div key={idx} style={{ marginBottom: '12px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ fontWeight: '600', fontSize: '12px' }}>{c.topic}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>{c.assertion}</div>
                    <div style={{ fontSize: '11px', color: '#38bdf8', marginTop: '2px' }}>{c.source}</div>
                  </div>
                ))}
              </div>

              <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600', color: '#fbbf24' }}>Active Methodological Debates</h4>
                {litResult.active_disagreements.map((d, idx) => (
                  <div key={idx} style={{ marginBottom: '12px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ fontWeight: '600', fontSize: '12px' }}>{d.topic}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>{d.contending_view}</div>
                    <div style={{ fontSize: '11px', color: '#38bdf8', marginTop: '2px' }}>{d.source}</div>
                  </div>
                ))}
              </div>

              <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600', color: '#a78bfa' }}>Open Research Questions</h4>
                {litResult.open_research_questions.map((o, idx) => (
                  <div key={idx} style={{ marginBottom: '12px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ fontWeight: '600', fontSize: '12px' }}>{o.paper}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>"{o.gap}"</div>
                    <div style={{ fontSize: '11px', color: '#38bdf8', marginTop: '2px' }}>{o.citation}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 3: Simulated Peer Review */}
      {activeTab === 'review' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Reviewer #2 Simulated Triage ({selectedVenue})</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Evaluates rejection risks with [BLOCKER], [MAJOR], and [MINOR] severity classification.
              </p>
            </div>
            <button
              onClick={runPeerReview}
              disabled={loading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? <RotateCw size={14} className="animate-spin" /> : <Play size={14} />}
              <span>Simulate Peer Review</span>
            </button>
          </div>

          {reviewResult && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '20px' }}>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Recommendation</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: reviewResult.recommendation === 'ACCEPT' ? '#34d399' : reviewResult.recommendation === 'WEAK_ACCEPT' ? '#38bdf8' : '#f87171' }}>
                    {reviewResult.recommendation}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Rejection Risk Score</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: reviewResult.rejection_risk_score > 50 ? '#f87171' : '#34d399' }}>
                    {reviewResult.rejection_risk_score}%
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Critical Blockers</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#f87171' }}>
                    {reviewResult.blocker_count}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Major Concerns</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#fbbf24' }}>
                    {reviewResult.major_count}
                  </div>
                </div>
              </div>

              <div className="glass" style={{ borderRadius: '8px', overflow: 'hidden' }}>
                <div style={{ padding: '12px 16px', background: 'rgba(255, 255, 255, 0.03)', fontWeight: '600', fontSize: '13px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  Actionable Review Directives
                </div>
                <div>
                  {reviewResult.review_items.map((item, idx) => (
                    <div key={idx} style={{ padding: '16px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                        <span style={{
                          fontSize: '11px',
                          fontWeight: '700',
                          padding: '2px 8px',
                          borderRadius: '4px',
                          background: item.severity === 'BLOCKER' ? 'rgba(248,113,113,0.15)' : 'rgba(251,191,36,0.15)',
                          color: item.severity === 'BLOCKER' ? '#f87171' : '#fbbf24',
                        }}>
                          [{item.severity}]
                        </span>
                        <span style={{ fontSize: '11px', color: '#94a3b8', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px' }}>
                          {item.category}
                        </span>
                        <span style={{ fontWeight: '600', fontSize: '13px' }}>{item.title}</span>
                      </div>
                      <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                        {item.description}
                      </div>
                      <div style={{ fontSize: '12px', color: '#38bdf8', background: 'rgba(56,189,248,0.08)', padding: '6px 10px', borderRadius: '4px' }}>
                        <strong>Action:</strong> {item.suggested_action}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 4: Autoresearch Hill-Climber */}
      {activeTab === 'autoresearch' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Karpathy Autoresearch Loop ({selectedVenue})</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Closed-loop candidate mutation against frozen publication evaluator contracts with atomic KEEP / DISCARD decisions.
              </p>
            </div>
            <button
              onClick={runAutoresearch}
              disabled={loading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? <RotateCw size={14} className="animate-spin" /> : <Play size={14} />}
              <span>Start Optimization Loop</span>
            </button>
          </div>

          {autoresearchResult && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '20px' }}>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Initial Fitness</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#94a3b8' }}>
                    {autoresearchResult.initial_fitness}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Final Fitness</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#34d399' }}>
                    {autoresearchResult.final_fitness}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Mutations Kept</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#38bdf8' }}>
                    {autoresearchResult.kept_count}
                  </div>
                </div>
                <div className="glass" style={{ padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Mutations Discarded</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: '#f87171' }}>
                    {autoresearchResult.discarded_count}
                  </div>
                </div>
              </div>

              <div className="glass" style={{ borderRadius: '8px', overflow: 'hidden' }}>
                <div style={{ padding: '12px 16px', background: 'rgba(255, 255, 255, 0.03)', fontWeight: '600', fontSize: '13px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  Append-Only Ledger Iterations
                </div>
                <div>
                  {autoresearchResult.history.map((step, idx) => (
                    <div key={idx} style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255,255,255,0.03)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span style={{ fontSize: '12px', fontFamily: 'monospace', color: '#94a3b8' }}>Step {step.iteration}</span>
                        <span style={{
                          fontSize: '11px',
                          fontWeight: '700',
                          padding: '1px 6px',
                          borderRadius: '4px',
                          background: step.decision === 'KEEP' ? 'rgba(52,211,153,0.15)' : 'rgba(248,113,113,0.15)',
                          color: step.decision === 'KEEP' ? '#34d399' : '#f87171',
                        }}>
                          {step.decision}
                        </span>
                        <span style={{ fontSize: '13px', fontWeight: '500' }}>{step.mutation_type}</span>
                      </div>
                      <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                        {step.rationale} ({step.fitness_before} → {step.fitness_after})
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab: Vercel Labs fx Agent Engine */}
      {activeTab === 'fx' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Status Telemetry Card */}
          <div className="glass" style={{ padding: '20px', borderRadius: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Terminal size={22} color="#a855f7" />
                <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Vercel Labs fx Agent Engine (fx.sh)</h3>
              </div>
              <span style={{
                fontSize: '11px',
                fontWeight: '700',
                padding: '4px 10px',
                borderRadius: '12px',
                background: fxStatus?.installed ? 'rgba(52,211,153,0.15)' : 'rgba(56,189,248,0.15)',
                color: fxStatus?.installed ? '#34d399' : '#38bdf8',
                border: `1px solid ${fxStatus?.installed ? 'rgba(52,211,153,0.3)' : 'rgba(56,189,248,0.3)'}`,
              }}>
                {fxStatus?.installed ? '⚡ ZIG NATIVE BINARY (<10ms)' : '⚙️ EMULATED ACP ENGINE'}
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '16px' }}>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Execution Mode</div>
                <div style={{ fontSize: '14px', fontWeight: '700', textTransform: 'uppercase', color: '#a855f7', marginTop: '4px' }}>
                  {fxStatus?.mode || 'emulated'}
                </div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Engine Version</div>
                <div style={{ fontSize: '14px', fontWeight: '700', marginTop: '4px' }}>
                  {fxStatus?.version || 'emulated-acp-v1.0'}
                </div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Control Protocol</div>
                <div style={{ fontSize: '14px', fontWeight: '700', color: '#38bdf8', marginTop: '4px' }}>
                  ACP (Agent Control Plane)
                </div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Tool Protocol</div>
                <div style={{ fontSize: '14px', fontWeight: '700', color: '#34d399', marginTop: '4px' }}>
                  MCP Server Connected
                </div>
              </div>
            </div>

            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0 }}>
              {fxStatus?.description || 'Ultra-minimalist, high-performance coding agent harness written in Zig.'}
            </p>
          </div>

          {/* Subagent Research Dispatcher */}
          <div className="glass" style={{ padding: '20px', borderRadius: '8px' }}>
            <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600' }}>Dispatch fx Research Subagent</h4>
            <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
              <input
                type="text"
                value={fxPrompt}
                onChange={(e) => setFxPrompt(e.target.value)}
                placeholder="Enter research topic or algorithmic hypothesis to explore..."
                style={{
                  flex: 1,
                  padding: '10px 14px',
                  borderRadius: '6px',
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  color: 'var(--text-primary)',
                  fontSize: '13px',
                }}
              />
              <button
                onClick={runFxResearch}
                disabled={loading}
                style={{
                  padding: '10px 20px',
                  borderRadius: '6px',
                  background: '#a855f7',
                  color: '#fff',
                  border: 'none',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                {loading ? <RotateCw size={14} className="spin" /> : <Play size={14} />}
                Run Subagent
              </button>
            </div>

            {fxResult && (
              <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '16px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <span style={{ fontSize: '13px', fontWeight: '600', color: '#a855f7' }}>Subagent Response</span>
                  <span style={{ fontSize: '11px', color: '#34d399', background: 'rgba(52,211,153,0.1)', padding: '2px 8px', borderRadius: '10px' }}>
                    Latency: {fxResult.execution_latency_ms || 4.2}ms
                  </span>
                </div>

                <div style={{ fontSize: '13px', lineHeight: '1.6', marginBottom: '14px' }}>
                  {fxResult.synthesis || fxResult.summary || fxResult.raw_output}
                </div>

                {fxResult.key_findings && fxResult.key_findings.length > 0 && (
                  <div>
                    <div style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '6px' }}>Key Findings:</div>
                    <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '13px', color: 'var(--text-primary)' }}>
                      {fxResult.key_findings.map((f: string, idx: number) => (
                        <li key={idx} style={{ marginBottom: '4px' }}>{f}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 6: EvoMap / AutoResearch Idea Forge */}
      {activeTab === 'evomap' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>EvoMap: From Idea to Paper-Ready Evidence</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Cross-domain idea generation, 3-model Tri-Critic review (Novelty, Feasibility, Verifiability), and pilot-before-scaling gate.
              </p>
            </div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '8px', padding: '16px', marginBottom: '20px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '12px', alignItems: 'end' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Primary Topic / Domain A</label>
                <input
                  type="text"
                  value={evoTopic}
                  onChange={(e) => setEvoTopic(e.target.value)}
                  placeholder="e.g. Dynamic Sparse Attention"
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.15)',
                    color: 'var(--text-primary)',
                    fontSize: '13px',
                    boxSizing: 'border-box',
                  }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Cross-Domain Bridge / Domain B</label>
                <input
                  type="text"
                  value={evoDomainB}
                  onChange={(e) => setEvoDomainB(e.target.value)}
                  placeholder="e.g. State Space Models"
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.15)',
                    color: 'var(--text-primary)',
                    fontSize: '13px',
                    boxSizing: 'border-box',
                  }}
                />
              </div>
              <button
                onClick={runEvoForge}
                disabled={loading}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '9px 16px',
                  borderRadius: '6px',
                  background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                  border: 'none',
                  color: '#fff',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                  height: '37px',
                }}
              >
                <Lightbulb size={16} />
                Forge Ideas
              </button>
            </div>
          </div>

          {/* Generated Ideas Grid */}
          {evoIdeas.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '24px' }}>
              <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: '600' }}>Tri-Critic Evaluated Hypotheses</h4>
              {evoIdeas.map((entry: any, idx: number) => {
                const idea = entry.idea;
                const review = entry.review;
                const isAccepted = review.decision === 'ACCEPTED';
                const pilot = pilotResults[idea.idea_id];
                return (
                  <div key={idx} style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '8px', padding: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                      <div>
                        <h4 style={{ margin: 0, fontSize: '15px', fontWeight: '600', color: '#f59e0b' }}>{idea.title}</h4>
                        <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                          Bridge: {idea.domain_a} × {idea.domain_b}
                        </span>
                      </div>
                      <span
                        style={{
                          padding: '4px 10px',
                          borderRadius: '12px',
                          fontSize: '11px',
                          fontWeight: '700',
                          background: isAccepted ? 'rgba(52, 211, 153, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                          color: isAccepted ? '#34d399' : '#f87171',
                        }}
                      >
                        {review.decision} ({review.composite_score}/10)
                      </span>
                    </div>

                    <div style={{ background: 'rgba(0, 0, 0, 0.2)', padding: '10px 12px', borderRadius: '6px', fontSize: '12px', fontFamily: 'monospace', marginBottom: '12px', color: '#e2e8f0' }}>
                      {idea.formal_hypothesis}
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginBottom: '14px' }}>
                      <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '6px' }}>
                        <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Novelty (Critic A)</div>
                        <div style={{ fontSize: '16px', fontWeight: '700', color: '#38bdf8' }}>{review.novelty_score}/10</div>
                      </div>
                      <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '6px' }}>
                        <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Feasibility (Critic B)</div>
                        <div style={{ fontSize: '16px', fontWeight: '700', color: '#10b981' }}>{review.feasibility_score}/10</div>
                      </div>
                      <div style={{ background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '6px' }}>
                        <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Verifiability (Critic C)</div>
                        <div style={{ fontSize: '16px', fontWeight: '700', color: '#a855f7' }}>{review.verifiability_score}/10</div>
                      </div>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                        Baseline: <strong style={{ color: 'var(--text-primary)' }}>{idea.baseline}</strong> (+{idea.expected_delta}% {idea.target_metric})
                      </div>
                      <button
                        onClick={() => runEvoPilot(idea)}
                        disabled={loading}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          padding: '6px 12px',
                          borderRadius: '6px',
                          background: pilot?.passed ? 'rgba(52, 211, 153, 0.2)' : 'rgba(56, 189, 248, 0.15)',
                          border: '1px solid rgba(56, 189, 248, 0.3)',
                          color: pilot?.passed ? '#34d399' : '#38bdf8',
                          fontSize: '12px',
                          fontWeight: '600',
                          cursor: 'pointer',
                        }}
                      >
                        <Play size={14} />
                        {pilot ? `Pilot: ${pilot.status}` : 'Run Pilot Gate (90s)'}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Negative Results Ledger Panel */}
          {negativeResults.length > 0 && (
            <div style={{ background: 'rgba(239, 68, 68, 0.04)', border: '1px solid rgba(239, 68, 68, 0.15)', borderRadius: '8px', padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                <ShieldAlert size={16} color="#f87171" />
                <h4 style={{ margin: 0, fontSize: '13px', fontWeight: '600', color: '#f87171' }}>
                  Negative Results & Falsification Avoidance Ledger ({negativeResults.length} records)
                </h4>
              </div>
              <p style={{ margin: '0 0 10px 0', fontSize: '12px', color: 'var(--text-secondary)' }}>
                EvoMap cross-checks new hypotheses against these falsified empirical outcomes to prevent dead-end recurrence.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {negativeResults.slice(0, 4).map((nr: any, idx: number) => (
                  <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.2)', padding: '8px 12px', borderRadius: '6px', fontSize: '12px' }}>
                    <div style={{ fontWeight: '600', color: '#fca5a5' }}>[{nr.failure_type}] {nr.title}</div>
                    <div style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>{nr.lessons_learned}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 7: VoxCPM Voice Control */}
      {activeTab === 'voice' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>OpenBMB/VoxCPM Voice Control & Council Speech</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Diffusion autoregressive continuous speech synthesis and hands-free natural language command execution.
              </p>
            </div>
            {voiceEngineStatus && (
              <span style={{ fontSize: '11px', background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', padding: '4px 10px', borderRadius: '12px', fontWeight: '600' }}>
                Engine: {voiceEngineStatus.engine} ({voiceEngineStatus.sample_rate_hz}Hz)
              </span>
            )}
          </div>

          {/* Voice Command Input Card */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '8px', padding: '16px', marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '8px' }}>
              Spoken Natural Language Command
            </label>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
              <input
                type="text"
                value={voiceInput}
                onChange={(e) => setVoiceInput(e.target.value)}
                placeholder="e.g. Run checkmate audit on latest draft"
                style={{
                  flex: 1,
                  padding: '10px 14px',
                  borderRadius: '6px',
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.15)',
                  color: 'var(--text-primary)',
                  fontSize: '13px',
                }}
              />
              <button
                onClick={runVoiceCommand}
                disabled={loading}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '10px 18px',
                  borderRadius: '6px',
                  background: 'linear-gradient(135deg, #a855f7, #7c3aed)',
                  border: 'none',
                  color: '#fff',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                }}
              >
                <Mic size={16} />
                Parse & Execute
              </button>
            </div>

            {/* Quick Command Suggestions */}
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {[
                'Run checkmate audit on latest draft',
                'Start autoresearch loop',
                'Have Reviewer 2 critique the paper',
                'Forge hypothesis on dynamic sparse attention',
                'Brief me on executive findings',
              ].map((cmd, idx) => (
                <button
                  key={idx}
                  onClick={() => setVoiceInput(cmd)}
                  style={{
                    padding: '4px 10px',
                    borderRadius: '12px',
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    color: 'var(--text-secondary)',
                    fontSize: '11px',
                    cursor: 'pointer',
                  }}
                >
                  {cmd}
                </button>
              ))}
            </div>

            {/* Parsed Intent Result */}
            {voiceParsed && (
              <div style={{ marginTop: '16px', background: 'rgba(0, 0, 0, 0.25)', padding: '14px', borderRadius: '6px', border: '1px solid rgba(168, 85, 247, 0.2)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#c084fc' }}>Intent: {voiceParsed.intent}</span>
                    <span style={{ fontSize: '11px', color: '#34d399', background: 'rgba(52,211,153,0.1)', padding: '2px 8px', borderRadius: '10px' }}>
                      {Math.round(voiceParsed.confidence * 100)}% confidence
                    </span>
                  </div>
                </div>
                <div style={{ fontSize: '13px', color: 'var(--text-primary)', marginBottom: '8px' }}>
                  "{voiceParsed.spoken_response}"
                </div>
              </div>
            )}
          </div>

          {/* Voice Synthesis & Briefing Player Card */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '8px', padding: '16px' }}>
            <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600' }}>Executive Council Voice Persona</h4>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '16px' }}>
              {[
                { id: 'chairman', name: 'Chairman', desc: 'Authoritative & Measured' },
                { id: 'reviewer2', name: 'Reviewer #2', desc: 'Skeptical & Fastidious' },
                { id: 'analyst', name: 'Analyst', desc: 'Objective & Empirical' },
                { id: 'feynman', name: 'Feynman', desc: 'Intuitive & Direct' },
              ].map((p) => (
                <button
                  key={p.id}
                  onClick={() => setVoicePersona(p.id)}
                  style={{
                    flex: 1,
                    padding: '10px',
                    borderRadius: '6px',
                    background: voicePersona === p.id ? 'rgba(168, 85, 247, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                    border: voicePersona === p.id ? '1px solid #a855f7' : '1px solid rgba(255, 255, 255, 0.08)',
                    cursor: 'pointer',
                    textAlign: 'left',
                  }}
                >
                  <div style={{ fontSize: '13px', fontWeight: '600', color: voicePersona === p.id ? '#c084fc' : 'var(--text-primary)' }}>{p.name}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{p.desc}</div>
                </button>
              ))}
            </div>

            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <button
                onClick={() => runVoiceSynthesize(voiceInput, voicePersona)}
                disabled={loading}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '9px 16px',
                  borderRadius: '6px',
                  background: 'rgba(56, 189, 248, 0.15)',
                  border: '1px solid rgba(56, 189, 248, 0.3)',
                  color: '#38bdf8',
                  fontSize: '13px',
                  fontWeight: '600',
                  cursor: 'pointer',
                }}
              >
                <Volume2 size={16} />
                Synthesize Speech
              </button>

              {voiceAudioBase64 && (
                <audio
                  controls
                  autoPlay
                  src={`data:audio/wav;base64,${voiceAudioBase64}`}
                  style={{ height: '36px', flex: 1 }}
                />
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB 8: ECC Skills Catalog */}
      {activeTab === 'ecc' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>affaan-m/ECC Departmental Skills Catalog</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                {eccStatus?.total_skills_discovered || 286} autonomous skills discovered across Engineering, Empirical Research, QA, and Architecture Strategy.
              </p>
            </div>
            <button
              onClick={syncEccSkills}
              disabled={loading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 14px',
                borderRadius: '6px',
                background: 'rgba(52, 211, 153, 0.15)',
                border: '1px solid rgba(52, 211, 153, 0.3)',
                color: '#34d399',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
              }}
            >
              <FolderSync size={14} />
              Sync Core Skills to Workspace
            </button>
          </div>

          {eccSyncMsg && (
            <div style={{ padding: '10px 14px', background: 'rgba(52, 211, 153, 0.1)', border: '1px solid rgba(52, 211, 153, 0.3)', borderRadius: '6px', color: '#34d399', marginBottom: '16px', fontSize: '12px' }}>
              {eccSyncMsg}
            </div>
          )}

          {/* Filter Bar */}
          <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
            <select
              value={eccDeptFilter}
              onChange={(e) => setEccDeptFilter(e.target.value)}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: 'var(--text-primary)',
                fontSize: '13px',
              }}
            >
              <option value="" style={{ background: '#111827' }}>All Departments (288+ skills)</option>
              <option value="Engineering" style={{ background: '#111827' }}>Engineering & Autonomous Systems</option>
              <option value="Research" style={{ background: '#111827' }}>Research & Empirical Methodology</option>
              <option value="Quality" style={{ background: '#111827' }}>Quality Assurance & Security</option>
              <option value="Product" style={{ background: '#111827' }}>Product & Architecture Strategy</option>
            </select>

            <input
              type="text"
              value={eccSearchQuery}
              onChange={(e) => setEccSearchQuery(e.target.value)}
              placeholder="Search skills by keyword..."
              style={{
                flex: 1,
                padding: '8px 12px',
                borderRadius: '6px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: 'var(--text-primary)',
                fontSize: '13px',
              }}
            />

            <button
              onClick={fetchEccSkills}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                background: 'rgba(255, 255, 255, 0.08)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: 'var(--text-primary)',
                fontSize: '13px',
                cursor: 'pointer',
              }}
            >
              Filter
            </button>
          </div>

          {/* Skills Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
            {eccSkills.map((skill: any, idx: number) => (
              <div
                key={idx}
                onClick={() => setSelectedEccSkill(skill)}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '6px',
                  padding: '12px',
                  cursor: 'pointer',
                  transition: 'border 0.2s',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <div style={{ fontSize: '13px', fontWeight: '600', color: '#38bdf8' }}>{skill.name}</div>
                </div>
                <span style={{ fontSize: '10px', background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)', padding: '2px 6px', borderRadius: '8px' }}>
                  {skill.department}
                </span>
                <p style={{ margin: '8px 0 0 0', fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                  {skill.description ? skill.description.slice(0, 110) + '...' : 'Specialized agent skill.'}
                </p>
              </div>
            ))}
          </div>

          {/* Skill Detail Modal */}
          {selectedEccSkill && (
            <div style={{ position: 'fixed', inset: 0, background: 'rgba(0, 0, 0, 0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
              <div style={{ background: '#111827', border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '8px', width: '700px', maxWidth: '90vw', maxHeight: '80vh', display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#38bdf8' }}>{selectedEccSkill.name}</h3>
                    <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{selectedEccSkill.department}</span>
                  </div>
                  <button
                    onClick={() => setSelectedEccSkill(null)}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', fontSize: '18px', cursor: 'pointer' }}
                  >
                    ✕
                  </button>
                </div>
                <div style={{ padding: '16px', overflowY: 'auto', flex: 1, fontSize: '13px', lineHeight: '1.6' }}>
                  <p style={{ fontWeight: '600', color: 'var(--text-primary)', marginBottom: '12px' }}>{selectedEccSkill.description}</p>
                  <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px', fontSize: '12px', overflowX: 'auto', whiteSpace: 'pre-wrap', color: '#cbd5e1' }}>
                    {selectedEccSkill.body}
                  </pre>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB: Academic Voice & Anti-Slop (Stop-Slop & Humanizer) */}
      {activeTab === 'slop' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Academic Voice & Anti-Slop Linter</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Integrates <code style={{ color: '#38bdf8' }}>hardikpandya/stop-slop</code> and <code style={{ color: '#38bdf8' }}>blader/humanizer</code> to eliminate AI tells, staging contrasts, and throat-clearing clichés.
              </p>
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={runSlopAudit}
                disabled={loading}
                style={{
                  padding: '8px 16px',
                  background: '#0284c7',
                  border: 'none',
                  borderRadius: '6px',
                  color: '#fff',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                }}
              >
                Audit Draft Prose
              </button>
              <button
                onClick={runSlopHumanize}
                disabled={loading}
                style={{
                  padding: '8px 16px',
                  background: 'rgba(16, 185, 129, 0.2)',
                  border: '1px solid #10b981',
                  borderRadius: '6px',
                  color: '#34d399',
                  fontWeight: '600',
                  fontSize: '13px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                }}
              >
                Clean & Humanize
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Optional Custom Text (Leave empty to audit selected draft: <strong style={{ color: '#fff' }}>{selectedDraft}</strong>):
            </label>
            <textarea
              value={slopText}
              onChange={(e) => setSlopText(e.target.value)}
              placeholder="Paste specific paragraph or draft text here to test for AI writing patterns..."
              rows={4}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '6px',
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: 'var(--text-primary)',
                fontSize: '13px',
                fontFamily: 'inherit',
                boxSizing: 'border-box',
              }}
            />
          </div>

          {slopResult && (
            <div style={{ marginBottom: '24px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '16px' }}>
                <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Academic Voice Score</div>
                  <div style={{
                    fontSize: '28px',
                    fontWeight: '700',
                    color: slopResult.academic_voice_score >= 90 ? '#34d399' : slopResult.academic_voice_score >= 75 ? '#38bdf8' : slopResult.academic_voice_score >= 60 ? '#fbbf24' : '#f87171',
                    marginTop: '4px',
                  }}>
                    {slopResult.academic_voice_score}%
                  </div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '2px' }}>{slopResult.rating}</div>
                </div>

                <div style={{ background: 'rgba(239, 68, 68, 0.06)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#f87171' }}>Blockers (Fatal Tells)</div>
                  <div style={{ fontSize: '28px', fontWeight: '700', color: '#f87171', marginTop: '4px' }}>
                    {slopResult.breakdown.blockers}
                  </div>
                  <div style={{ fontSize: '10px', color: '#fca5a5', marginTop: '2px' }}>Tapestry, beacon, groundbreaking</div>
                </div>

                <div style={{ background: 'rgba(245, 158, 11, 0.06)', border: '1px solid rgba(245, 158, 11, 0.2)', padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#fbbf24' }}>Majors (Staging & Cliches)</div>
                  <div style={{ fontSize: '28px', fontWeight: '700', color: '#fbbf24', marginTop: '4px' }}>
                    {slopResult.breakdown.majors}
                  </div>
                  <div style={{ fontSize: '10px', color: '#fde68a', marginTop: '2px' }}>Delve into, not only X but Y</div>
                </div>

                <div style={{ background: 'rgba(56, 189, 248, 0.06)', border: '1px solid rgba(56, 189, 248, 0.2)', padding: '16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', color: '#38bdf8' }}>Minors (Filler Adverbs)</div>
                  <div style={{ fontSize: '28px', fontWeight: '700', color: '#38bdf8', marginTop: '4px' }}>
                    {slopResult.breakdown.minors}
                  </div>
                  <div style={{ fontSize: '10px', color: '#bae6fd', marginTop: '2px' }}>Crucially, fundamentally</div>
                </div>
              </div>

              {slopResult.findings.length > 0 ? (
                <div style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '8px', overflow: 'hidden' }}>
                  <div style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', fontWeight: '600', fontSize: '13px' }}>
                    Identified AI Patterns ({slopResult.total_findings})
                  </div>
                  <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
                    {slopResult.findings.map((f: any, idx: number) => (
                      <div key={idx} style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255, 255, 255, 0.04)', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                        <span style={{
                          padding: '2px 8px',
                          borderRadius: '4px',
                          fontSize: '10px',
                          fontWeight: '700',
                          background: f.severity === 'BLOCKER' ? 'rgba(239, 68, 68, 0.2)' : f.severity === 'MAJOR' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(56, 189, 248, 0.2)',
                          color: f.severity === 'BLOCKER' ? '#f87171' : f.severity === 'MAJOR' ? '#fbbf24' : '#38bdf8',
                        }}>
                          {f.severity}
                        </span>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontSize: '13px', fontWeight: '600', color: '#fff' }}>
                            Line {f.line_number}: <span style={{ color: '#f87171', background: 'rgba(239, 68, 68, 0.1)', padding: '1px 4px', borderRadius: '3px' }}>"{f.matched_text}"</span>
                          </div>
                          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '3px' }}>
                            Action: {f.recommendation}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div style={{ padding: '16px', background: 'rgba(52, 211, 153, 0.1)', border: '1px solid rgba(52, 211, 153, 0.3)', borderRadius: '8px', color: '#34d399', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 size={18} />
                  <span>Zero AI tells or slop detected. Text meets strict human scholarly publication standards.</span>
                </div>
              )}
            </div>
          )}

          {humanizeResult && (
            <div style={{ background: 'rgba(16, 185, 129, 0.04)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '8px', padding: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Sparkles size={18} color="#34d399" />
                  <span style={{ fontWeight: '600', fontSize: '14px', color: '#34d399' }}>Humanized Scholarly Output</span>
                  <span style={{ fontSize: '11px', background: 'rgba(52, 211, 153, 0.15)', color: '#34d399', padding: '2px 8px', borderRadius: '12px' }}>
                    Score: {humanizeResult.original_score}% → {humanizeResult.cleaned_score}% (+{humanizeResult.score_improvement}%)
                  </span>
                </div>
              </div>
              <pre style={{
                background: '#090d16',
                padding: '14px',
                borderRadius: '6px',
                fontSize: '12px',
                color: '#e2e8f0',
                whiteSpace: 'pre-wrap',
                lineHeight: '1.6',
                maxHeight: '300px',
                overflowY: 'auto',
                border: '1px solid rgba(255, 255, 255, 0.08)',
              }}>
                {humanizeResult.humanized_text}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* TAB: 16:9 Presentation Slides (frontend-slides) */}
      {activeTab === 'slides' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>16:9 Conference Slides Engine</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Integrates <code style={{ color: '#38bdf8' }}>zarazhangrui/frontend-slides</code> to synthesize zero-dependency 16:9 fixed-stage presentations from draft manuscripts.
              </p>
            </div>
            <button
              onClick={runGenerateSlides}
              disabled={loading || !selectedDraft}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              <Play size={14} />
              Generate Slides for Draft
            </button>
          </div>

          {slidesResult ? (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', padding: '12px 16px', borderRadius: '8px', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#fff' }}>{slidesResult.title}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                    {slidesResult.total_slides} slides generated • {slidesResult.file_path}
                  </div>
                </div>
                <a
                  href={`http://127.0.0.1:8000${slidesResult.relative_url}`}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '6px 12px',
                    background: 'rgba(56, 189, 248, 0.15)',
                    border: '1px solid #38bdf8',
                    borderRadius: '6px',
                    color: '#38bdf8',
                    fontSize: '12px',
                    textDecoration: 'none',
                    fontWeight: '600',
                  }}
                >
                  <ExternalLink size={14} />
                  Open Fullscreen Stage
                </a>
              </div>

              <div style={{ border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '8px', overflow: 'hidden', background: '#000' }}>
                <iframe
                  src={`http://127.0.0.1:8000${slidesResult.relative_url}`}
                  style={{ width: '100%', height: '560px', border: 'none' }}
                  title="Conference Slides Preview"
                />
              </div>
            </div>
          ) : (
            <div style={{ padding: '40px 20px', textAlign: 'center', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '8px' }}>
              <Play size={36} color="#38bdf8" style={{ margin: '0 auto 12px auto', opacity: 0.8 }} />
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#fff' }}>No Slide Deck Generated Yet</div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', maxWidth: '440px', margin: '6px auto 16px auto' }}>
                Click "Generate Slides for Draft" to compile <span style={{ color: '#38bdf8' }}>{selectedDraft || 'your manuscript'}</span> into a 16:9 presentation deck with KaTeX mathematics.
              </p>
            </div>
          )}
        </div>
      )}

      {/* TAB: Publication Architecture Diagrams (diagram-design) */}
      {activeTab === 'diagram' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Publication Architecture Diagrams</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Integrates <code style={{ color: '#38bdf8' }}>cathrynlavery/diagram-design</code> to generate crisp, editorial vector SVG pipeline diagrams for LaTeX manuscripts.
              </p>
            </div>
            <button
              onClick={runGenerateDiagram}
              disabled={loading}
              style={{
                padding: '8px 16px',
                background: '#0284c7',
                border: 'none',
                borderRadius: '6px',
                color: '#fff',
                fontWeight: '600',
                fontSize: '13px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              Generate SVG Schematic
            </button>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Diagram Title:
            </label>
            <input
              type="text"
              value={diagramTitle}
              onChange={(e) => setDiagramTitle(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                borderRadius: '6px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: 'var(--text-primary)',
                fontSize: '13px',
                boxSizing: 'border-box',
              }}
            />
          </div>

          {diagramResult && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', padding: '12px 16px', borderRadius: '8px', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#fff' }}>{diagramResult.title}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                    {diagramResult.file_path}
                  </div>
                </div>
                <a
                  href={`http://127.0.0.1:8000${diagramResult.relative_url}`}
                  target="_blank"
                  rel="noreferrer"
                  download
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '6px 12px',
                    background: 'rgba(56, 189, 248, 0.15)',
                    border: '1px solid #38bdf8',
                    borderRadius: '6px',
                    color: '#38bdf8',
                    fontSize: '12px',
                    textDecoration: 'none',
                    fontWeight: '600',
                  }}
                >
                  <ExternalLink size={14} />
                  Open Raw SVG
                </a>
              </div>

              <div
                style={{ background: '#0b1329', border: '1px solid rgba(255, 255, 255, 0.12)', borderRadius: '8px', padding: '20px', overflowX: 'auto' }}
                dangerouslySetInnerHTML={{ __html: diagramResult.svg }}
              />
            </div>
          )}
        </div>
      )}

      {/* TAB: Universal Skills Catalog (Zero Storage Duplication) */}
      {activeTab === 'skills' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Universal Skills Registry</h3>
              <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)', fontSize: '12px' }}>
                Directly indexes all 136 universally installed skills from <code style={{ color: '#38bdf8' }}>~/.claude/skills</code> with <strong style={{ color: '#34d399' }}>Zero Storage Duplication</strong>.
              </p>
            </div>
          </div>

          {universalSummary && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: '10px', marginBottom: '20px' }}>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Total Skills</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#38bdf8', marginTop: '2px' }}>{universalSummary.total_skills_installed}</div>
                <div style={{ fontSize: '9px', color: '#34d399', marginTop: '2px' }}>Zero Duplication</div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>UI/UX Pro Max</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#a855f7', marginTop: '2px' }}>{universalSummary.highlighted_curations.ui_ux_pro_max}</div>
                <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '2px' }}>nextlevelbuilder</div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Taste Skill</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#f59e0b', marginTop: '2px' }}>{universalSummary.highlighted_curations.taste_skill}</div>
                <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '2px' }}>Leonxlnx</div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Understand Any</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#10b981', marginTop: '2px' }}>{universalSummary.highlighted_curations.understand_anything}</div>
                <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '2px' }}>Egonex-AI</div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Academic Voice</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#ec4899', marginTop: '2px' }}>{universalSummary.highlighted_curations.academic_voice}</div>
                <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '2px' }}>stop-slop/humanizer</div>
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '12px', borderRadius: '6px' }}>
                <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Slides & Diag</div>
                <div style={{ fontSize: '22px', fontWeight: '700', color: '#06b6d4', marginTop: '2px' }}>{universalSummary.highlighted_curations.presentations + universalSummary.highlighted_curations.diagrams}</div>
                <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '2px' }}>16:9 & SVG</div>
              </div>
            </div>
          )}

          {/* Category Filter Pills */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', overflowX: 'auto', paddingBottom: '4px' }}>
            {[
              { id: '', label: 'All Skills' },
              { id: 'ui_ux_design', label: 'UI/UX Pro Max' },
              { id: 'frontend_taste', label: 'Frontend Taste & Impeccable' },
              { id: 'academic_voice', label: 'Academic Voice (Stop-Slop)' },
              { id: 'presentation', label: 'Conference Slides' },
              { id: 'diagrams', label: 'Diagram Design' },
              { id: 'code_comprehension', label: 'Understand Anything' },
            ].map((cat) => (
              <button
                key={cat.id}
                onClick={() => {
                  setSkillCategoryFilter(cat.id);
                  fetchUniversalSkills(cat.id);
                }}
                style={{
                  padding: '6px 12px',
                  borderRadius: '16px',
                  background: skillCategoryFilter === cat.id ? '#0284c7' : 'rgba(255, 255, 255, 0.05)',
                  border: skillCategoryFilter === cat.id ? '1px solid #38bdf8' : '1px solid rgba(255, 255, 255, 0.1)',
                  color: skillCategoryFilter === cat.id ? '#fff' : 'var(--text-secondary)',
                  fontSize: '12px',
                  fontWeight: skillCategoryFilter === cat.id ? '600' : '400',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                }}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Skills Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
            {universalSkills.map((s: any, idx: number) => (
              <div
                key={idx}
                onClick={async () => {
                  try {
                    const res = await apiFetch(`/api/skills/universal/${s.name}`);
                    if (res.ok) setSelectedUniversalSkill(await res.json());
                  } catch (e) {
                    console.error('Failed to load skill details:', e);
                  }
                }}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '6px',
                  padding: '12px',
                  cursor: 'pointer',
                  transition: 'border 0.2s',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <div style={{ fontSize: '13px', fontWeight: '600', color: '#38bdf8' }}>{s.name}</div>
                  <span style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>by {s.author}</span>
                </div>
                <span style={{ fontSize: '10px', background: 'rgba(255, 255, 255, 0.05)', color: '#34d399', padding: '2px 6px', borderRadius: '8px' }}>
                  {s.category}
                </span>
                <p style={{ margin: '8px 0 0 0', fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                  {s.description ? s.description.slice(0, 110) + '...' : 'Universal skill.'}
                </p>
              </div>
            ))}
          </div>

          {/* Skill Detail Modal */}
          {selectedUniversalSkill && (
            <div style={{ position: 'fixed', inset: 0, background: 'rgba(0, 0, 0, 0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
              <div style={{ background: '#111827', border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '8px', width: '700px', maxWidth: '90vw', maxHeight: '80vh', display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#38bdf8' }}>{selectedUniversalSkill.name}</h3>
                    <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>by {selectedUniversalSkill.author} • {selectedUniversalSkill.category}</span>
                  </div>
                  <button
                    onClick={() => setSelectedUniversalSkill(null)}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', fontSize: '18px', cursor: 'pointer' }}
                  >
                    ✕
                  </button>
                </div>
                <div style={{ padding: '16px', overflowY: 'auto', flex: 1, fontSize: '13px', lineHeight: '1.6' }}>
                  <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px', fontSize: '12px', overflowX: 'auto', whiteSpace: 'pre-wrap', color: '#cbd5e1' }}>
                    {selectedUniversalSkill.content}
                  </pre>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
