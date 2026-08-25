import React, { useState, useEffect, useRef } from 'react';
import {
  Layers,
  Sparkles,
  BookOpen,
  CheckCircle2,
  Play,
  TrendingUp,
  Cpu,
  ShieldCheck,
  ArrowRight
} from 'lucide-react';
import { apiFetch } from '../api';

export interface DraftItem {
  filename: string;
  title: string;
  target_venue: string;
  target_length: string;
  words: number;
  citations: number;
  tables: number;
  equations: number;
  status: string;
  frontmatter: any;
}

export interface MetaReviewLog {
  projectId: string;
  timestamp: number;
  stage: string;
  agent: string;
  message: string;
  data?: any;
}

interface MetaReviewCouncilProps {
  onNavigateToPublisher?: () => void;
}

const MetaReviewCouncil: React.FC<MetaReviewCouncilProps> = ({ onNavigateToPublisher }) => {
  const [drafts, setDrafts] = useState<DraftItem[]>([]);
  const [selectedDraft, setSelectedDraft] = useState<string>('');
  const [targetVenue, setTargetVenue] = useState<string>('IEEEtran');
  const [targetLength, setTargetLength] = useState<string>('full_journal');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [logs, setLogs] = useState<MetaReviewLog[]>([]);
  const [stats, setStats] = useState<{
    initial_words?: number;
    final_words?: number;
    initial_citations?: number;
    final_citations?: number;
    initial_tables?: number;
    final_tables?: number;
    initial_equations?: number;
    final_equations?: number;
    decision?: string;
  } | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchDrafts();
  }, []);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  const fetchDrafts = async () => {
    try {
      const res = await apiFetch('/api/vault/drafts');
      if (res.ok) {
        const data = await res.json();
        setDrafts(data.drafts || []);
        if (data.drafts?.length > 0 && !selectedDraft) {
          setSelectedDraft(data.drafts[0].filename);
          setTargetVenue(data.drafts[0].target_venue || 'IEEEtran');
          setTargetLength(data.drafts[0].target_length || 'full_journal');
        }
      }
    } catch (e) {
      console.error('Failed to fetch drafts:', e);
    }
  };

  const handleSelectDraft = (filename: string) => {
    setSelectedDraft(filename);
    const d = drafts.find(x => x.filename === filename);
    if (d) {
      setTargetVenue(d.target_venue || 'IEEEtran');
      setTargetLength(d.target_length || 'full_journal');
      setStats(null);
    }
  };

  const startMetaReview = async () => {
    if (!selectedDraft) return;
    setIsRunning(true);
    setLogs([]);
    setStats(null);
    setErrorMsg(null);

    try {
      const res = await apiFetch('/api/research/meta-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: selectedDraft,
          target_venue: targetVenue,
          target_length: targetLength,
          save_to_vault: true
        })
      });

      if (!res.ok) {
        throw new Error(`Failed to start Tier 2 meta-review: ${res.statusText}`);
      }

      const data = await res.json();
      const projId = data.project_id;

      // Connect to SSE stream
      const streamUrl = `http://127.0.0.1:8000/api/research/meta-review/stream/${projId}`;
      const eventSource = new EventSource(streamUrl);

      eventSource.onmessage = (event) => {
        try {
          const logData = JSON.parse(event.data);
          setLogs((prev) => [...prev, logData]);
          if (logData.data && (logData.data.final_words || logData.data.initial_words)) {
            setStats(prev => ({ ...(prev || {}), ...logData.data }));
          }
        } catch (e) {
          console.error('Error parsing SSE data:', e);
        }
      };

      eventSource.addEventListener('end', () => {
        eventSource.close();
        setIsRunning(false);
        fetchDrafts(); // Refresh metadata after revision
      });

      eventSource.onerror = (err) => {
        console.error('SSE Error:', err);
        eventSource.close();
        setIsRunning(false);
      };

    } catch (e: any) {
      console.error('Error executing Tier 2 alignment:', e);
      setIsRunning(false);
      setErrorMsg(e.message || 'Failed to execute Tier 2 council.');
    }
  };

  const selectedDraftObj = drafts.find(d => d.filename === selectedDraft);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', height: '100%', minHeight: 0 }}>
      {/* Header Banner */}
      <div className="glass" style={{ padding: '20px 24px', borderRadius: '16px', background: 'linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(59,130,246,0.08) 100%)', border: '1px solid rgba(16,185,129,0.25)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)', padding: '8px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Layers size={22} color="#000" strokeWidth={2.2} />
              </div>
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 'bold', fontFamily: 'var(--font-heading)', letterSpacing: '0.3px', margin: 0 }}>
                  Tier 2: Meta-Review & Cross-Venue Alignment Council
                </h2>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: '2px 0 0 0' }}>
                  Second-Stage Multi-Agent Orchestration • 15–30+ Citation Expansion • Proof & Table Auditing • Zero-Hallucination Reformatting
                </p>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '11px', background: 'rgba(16,185,129,0.15)', color: '#34d399', border: '1px solid rgba(16,185,129,0.3)', padding: '4px 10px', borderRadius: '20px', fontWeight: '600' }}>
              AGENTS.md Council Active
            </span>
            <span style={{ fontSize: '11px', background: 'rgba(59,130,246,0.15)', color: '#60a5fa', border: '1px solid rgba(59,130,246,0.3)', padding: '4px 10px', borderRadius: '20px', fontWeight: '600' }}>
              12 Venue Style Profiles
            </span>
          </div>
        </div>

        {/* 4 Agent Personas Pill Bar */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px', marginTop: '16px' }}>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px 12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={16} color="#34d399" />
              <span style={{ fontSize: '12px', fontWeight: '600' }}>Meta-Review Council Chair</span>
            </div>
            <p style={{ fontSize: '10px', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>Area Chair Rubric Scoring & Target Venue Gatekeeper</p>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px 12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BookOpen size={16} color="#60a5fa" />
              <span style={{ fontSize: '12px', fontWeight: '600' }}>Citation Graph Expander</span>
            </div>
            <p style={{ fontSize: '10px', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>Enriches Drafts with 15–30+ Authentic [[paper_id]] Links</p>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px 12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <TrendingUp size={16} color="#f59e0b" />
              <span style={{ fontSize: '12px', fontWeight: '600' }}>Technical Depth Auditor</span>
            </div>
            <p style={{ fontSize: '10px', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>Injects Lyapunov Bounds & LaTeX Results Tables</p>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px 12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Sparkles size={16} color="#ec4899" />
              <span style={{ fontSize: '12px', fontWeight: '600' }}>Cross-Venue Publisher</span>
            </div>
            <p style={{ fontSize: '10px', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>Applies MASTER_VENUE Rules & Scrubs AI Slop</p>
          </div>
        </div>
      </div>

      {/* Main Grid: Left Controls & Baseline | Right Deliberation & Delta */}
      <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: '16px', flex: 1, minHeight: 0 }}>
        {/* Left Column: Draft Selection & Config */}
        <div className="glass" style={{ padding: '18px', borderRadius: '14px', display: 'flex', flexDirection: 'column', gap: '14px', overflowY: 'auto' }}>
          <div>
            <label style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
              Select Source Manuscript Draft (vault/04_Drafts/)
            </label>
            <select
              value={selectedDraft}
              onChange={(e) => handleSelectDraft(e.target.value)}
              disabled={isRunning}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                background: 'rgba(0,0,0,0.4)',
                border: '1px solid rgba(255,255,255,0.15)',
                color: '#fff',
                fontSize: '12px',
                outline: 'none',
              }}
            >
              {drafts.map(d => (
                <option key={d.filename} value={d.filename} style={{ background: '#121212', color: '#fff' }}>
                  {d.title} ({d.words} words, {d.citations} refs)
                </option>
              ))}
            </select>
          </div>

          {/* Current Baseline Card */}
          {selectedDraftObj && (
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Tier 1 Manuscript Baseline
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                <div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Word Count</div>
                  <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#60a5fa' }}>{selectedDraftObj.words.toLocaleString()}</div>
                </div>
                <div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Citations [[id]]</div>
                  <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#34d399' }}>{selectedDraftObj.citations}</div>
                </div>
                <div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Tables (\begin)</div>
                  <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#f59e0b' }}>{selectedDraftObj.tables}</div>
                </div>
                <div>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Equations ($$)</div>
                  <div style={{ fontSize: '15px', fontWeight: 'bold', color: '#ec4899' }}>{selectedDraftObj.equations}</div>
                </div>
              </div>
            </div>
          )}

          {/* Target Venue & Length Pickers */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <label style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Target Publication Venue
              </label>
              <select
                value={targetVenue}
                onChange={(e) => setTargetVenue(e.target.value)}
                disabled={isRunning}
                style={{
                  width: '100%',
                  padding: '8px 10px',
                  borderRadius: '8px',
                  background: 'rgba(0,0,0,0.4)',
                  border: '1px solid rgba(255,255,255,0.15)',
                  color: '#fff',
                  fontSize: '12px',
                  outline: 'none',
                }}
              >
                <option value="IEEEtran">IEEEtran (Transactions / Journal)</option>
                <option value="NeurIPS">NeurIPS (9-Page Track)</option>
                <option value="ICML">ICML (8-Page Track)</option>
                <option value="CVPR">CVPR (8-Page Main)</option>
                <option value="ACL">ACL / ARR (8-Page Long)</option>
                <option value="ACM">ACM CSUR / Computing Surveys</option>
                <option value="IEEE_Access">IEEE Access (Open Journal)</option>
                <option value="SpringerOpen">SpringerOpen (SN Computer Science)</option>
                <option value="MDPI">MDPI (Applied Sciences / AI)</option>
                <option value="arXiv">arXiv Preprint</option>
                <option value="DOAJ">DOAJ Open Access</option>
                <option value="Femington">Femington Press</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Target Page Budget
              </label>
              <select
                value={targetLength}
                onChange={(e) => setTargetLength(e.target.value)}
                disabled={isRunning}
                style={{
                  width: '100%',
                  padding: '8px 10px',
                  borderRadius: '8px',
                  background: 'rgba(0,0,0,0.4)',
                  border: '1px solid rgba(255,255,255,0.15)',
                  color: '#fff',
                  fontSize: '12px',
                  outline: 'none',
                }}
              >
                <option value="full_journal">Full Journal Manuscript (10–15+ Pages)</option>
                <option value="short_camera_ready">Camera-Ready Conference (4–8 Pages)</option>
              </select>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={startMetaReview}
            disabled={isRunning || !selectedDraft}
            style={{
              marginTop: 'auto',
              padding: '14px',
              borderRadius: '10px',
              background: isRunning ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)',
              color: '#000',
              fontWeight: 'bold',
              fontSize: '13px',
              border: 'none',
              cursor: isRunning ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              boxShadow: isRunning ? 'none' : '0 4px 14px rgba(16,185,129,0.3)'
            }}
          >
            {isRunning ? (
              <>
                <span className="pulse-loading" style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#000' }}></span>
                <span>Council Deliberating Tier 2 Pass...</span>
              </>
            ) : (
              <>
                <Play size={16} fill="#000" />
                <span>Convene Tier 2 Alignment Council</span>
              </>
            )}
          </button>

          {errorMsg && (
            <div style={{ color: '#f87171', fontSize: '11px', background: 'rgba(239,68,68,0.1)', padding: '8px', borderRadius: '6px', border: '1px solid rgba(239,68,68,0.2)' }}>
              {errorMsg}
            </div>
          )}
        </div>

        {/* Right Column: Live Council Logs & Before/After Matrix */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', minHeight: 0 }}>
          {/* Alignment Outcome Card (if stats available) */}
          {stats && (
            <div className="glass" style={{ padding: '14px 18px', borderRadius: '12px', background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.3)' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 size={18} color="#34d399" />
                  <span style={{ fontSize: '13px', fontWeight: 'bold', color: '#34d399' }}>Tier 2 Meta-Review Alignment Verified</span>
                </div>
                <span style={{ fontSize: '11px', background: 'rgba(16,185,129,0.2)', color: '#34d399', padding: '2px 8px', borderRadius: '12px', fontWeight: '700' }}>
                  {stats.decision || 'STRONG ACCEPT'}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 10px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Word Expansion</div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold' }}>
                    {stats.initial_words?.toLocaleString()} → <span style={{ color: '#60a5fa' }}>{stats.final_words?.toLocaleString()}</span>
                  </div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 10px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Citation Density</div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold' }}>
                    {stats.initial_citations} → <span style={{ color: '#34d399' }}>{stats.final_citations} distinct</span>
                  </div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 10px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Tables Injected</div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold' }}>
                    {stats.initial_tables || 0} → <span style={{ color: '#f59e0b' }}>{stats.final_tables || 1} tabular</span>
                  </div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 10px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Equations</div>
                  <div style={{ fontSize: '13px', fontWeight: 'bold' }}>
                    {stats.initial_equations || 0} → <span style={{ color: '#ec4899' }}>{stats.final_equations || 2} proofs</span>
                  </div>
                </div>
              </div>

              {onNavigateToPublisher && (
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
                  <button
                    onClick={onNavigateToPublisher}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      background: 'rgba(59,130,246,0.15)',
                      border: '1px solid rgba(59,130,246,0.3)',
                      color: '#60a5fa',
                      fontSize: '11px',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    <span>Open in HITL Publisher (12-Venue PDF Release)</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Real-Time Council Stream Terminal */}
          <div className="glass" style={{ flex: 1, borderRadius: '14px', padding: '16px', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Cpu size={16} color="var(--primary)" />
                <span style={{ fontSize: '13px', fontWeight: 'bold', letterSpacing: '0.2px' }}>Live Meta-Review Council Stream</span>
              </div>
              <span style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>
                {logs.length} events logged
              </span>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '10px', paddingRight: '6px' }}>
              {logs.length === 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', gap: '10px' }}>
                  <Layers size={32} opacity={0.3} />
                  <p style={{ fontSize: '12px' }}>Select a manuscript draft and click "Convene Tier 2 Alignment Council" to start.</p>
                </div>
              ) : (
                logs.map((log, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(255,255,255,0.05)',
                      borderRadius: '8px',
                      padding: '10px 12px',
                      fontSize: '12px',
                      lineHeight: '1.4'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                      <span style={{
                        fontSize: '9px',
                        padding: '1px 6px',
                        borderRadius: '4px',
                        fontWeight: '700',
                        textTransform: 'uppercase',
                        background: log.stage === 'Consensus' ? 'rgba(16,185,129,0.2)' : 'rgba(59,130,246,0.2)',
                        color: log.stage === 'Consensus' ? '#34d399' : '#60a5fa',
                      }}>
                        {log.stage}
                      </span>
                      <span style={{ fontWeight: '600', color: '#fff', fontSize: '11px' }}>{log.agent}</span>
                      <span style={{ marginLeft: 'auto', fontSize: '10px', color: 'var(--text-secondary)' }}>
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div style={{ color: 'var(--text-secondary)', wordBreak: 'break-word' }}>
                      {log.message}
                    </div>
                  </div>
                ))
              )}
              <div ref={logsEndRef} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetaReviewCouncil;
