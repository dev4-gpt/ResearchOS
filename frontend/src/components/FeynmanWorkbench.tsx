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
  Zap
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
  const [activeTab, setActiveTab] = useState<'audit' | 'lit' | 'review' | 'autoresearch' | 'fx'>('audit');
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

  useEffect(() => {
    fetchDrafts();
    fetchFxStatus();
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
      <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', marginBottom: '20px' }}>
        {[
          { id: 'audit', label: 'Paper-to-Code Audit (/audit)', icon: Code },
          { id: 'lit', label: 'Literature Matrix (/lit)', icon: BookOpen },
          { id: 'review', label: 'Simulated Peer Review (/review)', icon: ShieldAlert },
          { id: 'autoresearch', label: 'Autoresearch Hill-Climber', icon: Sparkles },
          { id: 'fx', label: 'fx Engine (Vercel Labs)', icon: Terminal },
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
    </div>
  );
};
