import React, { useState, useEffect } from 'react';
import { FolderOpen, Save, FileText, Check, AlertCircle, Eye, FileEdit, RefreshCw, Download, Sparkles, Target, User, Layers, ShieldCheck, BarChart3, LockKeyhole } from 'lucide-react';
import { apiFetch } from '../api';
import LinkRenderer from './LinkRenderer';
import { PDFVisualPreviewModal } from './PDFVisualPreviewModal';


interface VaultFile {
  filename: string;
  title: string;
  metadata: any;
  content_preview: string;
}

interface VaultFilesData {
  papers: VaultFile[];
  concepts: VaultFile[];
  debates: VaultFile[];
  drafts: VaultFile[];
}

const FALLBACK_VENUES = ['NeurIPS', 'ICML', 'CVPR', 'ACL', 'IEEEtran', 'ACM', 'IEEE_Access', 'SpringerOpen', 'DOAJ', 'arXiv', 'Femington', 'MDPI'];

const DocEditor: React.FC = () => {
  const [files, setFiles] = useState<VaultFilesData | null>(null);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [activeFilename, setActiveFilename] = useState<string | null>(null);
  const [isLoadingList, setIsLoadingList] = useState(true);
  const [isLoadingFile, setIsLoadingFile] = useState(false);

  const [content, setContent] = useState('');
  const [frontmatter, setFrontmatter] = useState<any>({});
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [editMode, setEditMode] = useState<'edit' | 'preview'>('edit');
  const [selectedVenue, setSelectedVenue] = useState<string>('IEEEtran');
  const [availableVenues, setAvailableVenues] = useState<string[]>(FALLBACK_VENUES);

  // Checkmate Final Layer Audit State
  const [checkmateOpen, setCheckmateOpen] = useState(false);
  const [checkmateData, setCheckmateData] = useState<any>(null);
  const [checkmateLoading, setCheckmateLoading] = useState(false);
  const [visualPreviewOpen, setVisualPreviewOpen] = useState(false);


  // Venue Advisor Panel State
  const [venueAdvisorOpen, setVenueAdvisorOpen] = useState(false);
  const [venueRecommendations, setVenueRecommendations] = useState<any[] | null>(null);
  const [venueAdvisorLoading, setVenueAdvisorLoading] = useState(false);
  const [venueAdvisorError, setVenueAdvisorError] = useState<string | null>(null);
  const [profileGoal, setProfileGoal] = useState('balanced');
  const [profileTimeline, setProfileTimeline] = useState('normal');
  const [profileCitations, setProfileCitations] = useState(0);

  // Publisher readiness matrix: all drafts x all supported venues, with
  // originality and substantive-value gates evaluated before release.
  const [publisherSuiteOpen, setPublisherSuiteOpen] = useState(false);
  const [publisherSuiteLoading, setPublisherSuiteLoading] = useState(false);
  const [publisherSuiteData, setPublisherSuiteData] = useState<any>(null);
  const [publisherSuiteError, setPublisherSuiteError] = useState<string | null>(null);
  const [publisherJobId, setPublisherJobId] = useState<string | null>(null);

  const runCheckmateAudit = async () => {
    if (!activeFilename) return;
    setCheckmateLoading(true);
    setCheckmateOpen(true);
    try {
      const res = await apiFetch(`/api/vault/checkmate-audit?filename=${activeFilename}&venue=${selectedVenue}`);
      const data = await res.json();
      if (res.ok && data.checkmate) {
        setCheckmateData(data.checkmate);
        if (data.checkmate.checkmate_passed) {
          setFrontmatter((prev: any) => ({ ...prev, checkmate_score: data.checkmate.score, checkmate_status: 'PASSED' }));
        }
      } else {
        alert(`Checkmate Audit Failed: ${data.detail || 'Error running audit'}`);
      }
    } catch (e: any) {
      alert(`Checkmate Audit Error: ${e.message || e}`);
    } finally {
      setCheckmateLoading(false);
    }
  };

  useEffect(() => {
    fetchFilesList();
    apiFetch('/api/venues').then(r => r.ok ? r.json() : null).then(d => {
      const nextVenues = Array.isArray(d?.venue_order) ? d.venue_order : Object.keys(d?.release_profiles || d?.venues || {});
      if (nextVenues.length) setAvailableVenues(nextVenues);
    }).catch(() => {});
    // Load user profile
    apiFetch('/api/user/profile').then(r => r.json()).then(d => {
      if (d.success && d.profile) {
        setProfileGoal(d.profile.submission_goals || 'balanced');
        setProfileTimeline(d.profile.target_timeline || 'normal');
        setProfileCitations(d.profile.min_citations || 0);
      }
    }).catch(() => {});
  }, []);

  const fetchFilesList = async () => {
    setIsLoadingList(true);
    try {
      const res = await apiFetch('/api/vault/files');
      if (res.ok) {
        const data: VaultFilesData = await res.json();
        setFiles(data);
        if (!activeFilename) {
          if (data.drafts && data.drafts.length > 0) {
            loadFile('drafts', data.drafts[0].filename);
          } else if (data.papers && data.papers.length > 0) {
            loadFile('papers', data.papers[0].filename);
          }
        }
      }
    } catch (err) {
      console.error('Failed to fetch vault files:', err);
    } finally {
      setIsLoadingList(false);
    }
  };

  const loadFile = async (category: string, filename: string) => {
    setIsLoadingFile(true);
    setActiveCategory(category);
    setActiveFilename(filename);
    try {
      const res = await apiFetch(`/api/vault/read?category=${category}&filename=${filename}`);
      if (res.ok) {
        const data = await res.json();
        setContent(data.content || '');
        setFrontmatter(data.frontmatter || {});
        setSaveStatus('idle');
      }
    } catch (err) {
      console.error('Failed to read file:', err);
    } finally {
      setIsLoadingFile(false);
    }
  };

  const pollPublisherJob = async (initialJobId: string) => {
    let currentJobId = initialJobId;
    setPublisherJobId(currentJobId);
    setPublisherSuiteOpen(true);
    setPublisherSuiteLoading(true);
    setPublisherSuiteError(null);

    for (let attempt = 0; attempt < 900; attempt += 1) {
      try {
        const res = await apiFetch(`/api/vault/publisher/readiness/status?job_id=${encodeURIComponent(currentJobId)}`);
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.detail || `Readiness status failed (HTTP ${res.status})`);
        const job = data.job || {};
        if (job.status === 'failed') throw new Error(job.error || 'Publisher readiness job failed.');
        if (job.status === 'completed') {
          if (job.next_job_id) {
            currentJobId = job.next_job_id;
            setPublisherJobId(currentJobId);
            continue;
          }
          setPublisherSuiteData(job.report || null);
          setPublisherSuiteLoading(false);
          await fetchFilesList();
          return;
        }
        await new Promise((resolve) => window.setTimeout(resolve, 2000));
      } catch (e: any) {
        setPublisherSuiteError(e.message || 'Publisher readiness job failed.');
        setPublisherSuiteLoading(false);
        return;
      }
    }
    setPublisherSuiteError('Publisher readiness job exceeded the 30-minute polling window.');
    setPublisherSuiteLoading(false);
  };

  const handleSave = async (triggerReadiness = true) => {
    if (!activeCategory || !activeFilename) return;
    setSaveStatus('saving');
    try {
      const res = await apiFetch('/api/vault/write', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: activeCategory,
          filename: activeFilename,
          content: content,
          frontmatter: frontmatter,
          trigger_readiness: triggerReadiness && activeCategory === 'drafts'
        })
      });
      if (res.ok) {
        const data = await res.json().catch(() => ({}));
        setSaveStatus('saved');
        if (data.readiness_job?.job_id && triggerReadiness) {
          void pollPublisherJob(data.readiness_job.job_id);
        }
        fetchFilesList();
        setTimeout(() => setSaveStatus('idle'), 2500);
      } else {
        setSaveStatus('error');
      }
    } catch (err) {
      setSaveStatus('error');
    }
  };

  const handleGetVenueRecommendation = async () => {
    setVenueAdvisorLoading(true);
    setVenueAdvisorError(null);
    setVenueAdvisorOpen(true);
    try {
      // Save profile first if changes pending
      await apiFetch('/api/user/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          submission_goals: profileGoal,
          target_timeline: profileTimeline,
          citation_count: profileCitations,
        })
      });

      const title = frontmatter.title || activeFilename?.replace('.md', '') || 'Untitled';
      const abstract = content.split('\n').slice(0, 30).join(' ').substring(0, 500);
      const keywords = frontmatter.keywords || frontmatter.tags || [];

      const res = await apiFetch('/api/venues/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          abstract,
          topic_keywords: Array.isArray(keywords) ? keywords : [],
        })
      });
      if (res.ok) {
        const data = await res.json();
        setVenueRecommendations(data.ranked_venues || []);
      } else {
        const err = await res.json();
        setVenueAdvisorError(err.detail || 'Recommendation failed');
      }
    } catch (e: any) {
      setVenueAdvisorError(e.message || 'Network error');
    } finally {
      setVenueAdvisorLoading(false);
    }
  };

  const runPublisherReadiness = async () => {
    setPublisherSuiteOpen(true);
    setPublisherSuiteLoading(true);
    setPublisherSuiteError(null);
    try {
      // Preserve any current HITL edits before the vault-wide run begins.
      await handleSave(false);
      const res = await apiFetch('/api/vault/publisher/readiness', { method: 'POST' });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || `Readiness suite failed (HTTP ${res.status})`);
      if (data.job?.job_id) {
        await pollPublisherJob(data.job.job_id);
      } else {
        setPublisherSuiteData(data);
        setPublisherSuiteLoading(false);
        await fetchFilesList();
      }
    } catch (e: any) {
      setPublisherSuiteError(e.message || 'Publisher readiness suite failed.');
      setPublisherSuiteLoading(false);
    } finally {
      // Background polling owns the loading state after a job is accepted.
    }
  };

  const runSinglePaperPublisherReadiness = async (targetFile?: string) => {
    const fileToTest = targetFile || activeFile;
    if (!fileToTest) return;
    setPublisherSuiteOpen(true);
    setPublisherSuiteLoading(true);
    setPublisherSuiteError(null);
    try {
      await handleSave(false);
      const res = await apiFetch(`/api/vault/publisher/readiness?filename=${encodeURIComponent(fileToTest)}`, { method: 'POST' });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || `Single paper readiness test failed (HTTP ${res.status})`);
      if (data.job?.job_id) {
        await pollPublisherJob(data.job.job_id);
      } else {
        setPublisherSuiteData(data);
        setPublisherSuiteLoading(false);
        await fetchFilesList();
      }
    } catch (e: any) {
      setPublisherSuiteError(e.message || 'Single paper publisher readiness test failed.');
      setPublisherSuiteLoading(false);
    }
  };

  const downloadPublisherBundle = async () => {
    try {
      const res = await apiFetch('/api/vault/publisher/readiness/bundle');
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || `Bundle download failed (HTTP ${res.status})`);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = 'researchingos-publish-ready-bundle.zip';
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
      URL.revokeObjectURL(url);
    } catch (e: any) {
      setPublisherSuiteError(e.message || 'Verified bundle download failed.');
      setPublisherSuiteOpen(true);
    }
  };

  const DIFFICULTY_COLOR: Record<string, string> = {
    'Easy': '#10b981',
    'Moderate': '#f59e0b',
    'Hard': '#f97316',
    'Very Hard': '#ef4444',
  };

  const O1A_STARS = (val: number) => '★'.repeat(val) + '☆'.repeat(5 - val);

  return (
    <div className="responsive-doc-layout">

      {/* Sidebar: File Explorer */}
      <div className="glass" style={{ display: 'grid', gridTemplateRows: 'auto 1fr', padding: '16px', overflow: 'hidden', minHeight: '0' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '15px', fontWeight: '700', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
          <FolderOpen size={16} />
          <span>Obsidian Vault Files</span>
        </h3>

        <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {isLoadingList ? (
            <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '12px' }}>
              Loading explorer...
            </div>
          ) : !files ? (
            <div style={{ padding: '20px 10px', textAlign: 'center', color: 'var(--danger)', fontSize: '12px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
              <AlertCircle size={20} />
              <span>Failed to connect to Vault.</span>
              <button
                onClick={fetchFilesList}
                style={{
                  background: 'rgba(59, 130, 246, 0.15)',
                  border: '1px solid rgba(59, 130, 246, 0.4)',
                  color: '#93c5fd',
                  padding: '6px 12px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '11px',
                  fontWeight: '600',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <RefreshCw size={12} />
                <span>Retry Connection</span>
              </button>
            </div>
          ) : (
            <>
              {/* Draft Reviews Section */}
              {files?.drafts && files.drafts.length > 0 && (
                <div>
                  <div style={{ fontSize: '10px', fontWeight: 'bold', color: '#f43f5e', textTransform: 'uppercase', marginBottom: '6px', letterSpacing: '0.5px' }}>Manuscript Drafts</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {files.drafts.map(f => (
                      <button
                        key={f.filename}
                        onClick={() => loadFile('drafts', f.filename)}
                        style={{
                          display: 'flex', alignItems: 'center', gap: '8px', border: 'none', background: activeFilename === f.filename ? 'rgba(244,63,94,0.1)' : 'transparent',
                          color: activeFilename === f.filename ? '#f43f5e' : 'var(--text-secondary)', padding: '6px 8px', borderRadius: '6px', cursor: 'pointer', textAlign: 'left', fontSize: '12px',
                          width: '100%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'
                        }}
                      >
                        <FileText size={14} style={{ flexShrink: 0 }} />
                        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{f.title}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Debates Section */}
              {files?.debates && files.debates.length > 0 && (
                <div>
                  <div style={{ fontSize: '10px', fontWeight: 'bold', color: '#8b5cf6', textTransform: 'uppercase', marginBottom: '6px', letterSpacing: '0.5px' }}>Debate Summaries</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {files.debates.map(f => (
                      <button
                        key={f.filename}
                        onClick={() => loadFile('debates', f.filename)}
                        style={{
                          display: 'flex', alignItems: 'center', gap: '8px', border: 'none', background: activeFilename === f.filename ? 'rgba(139,92,246,0.1)' : 'transparent',
                          color: activeFilename === f.filename ? '#8b5cf6' : 'var(--text-secondary)', padding: '6px 8px', borderRadius: '6px', cursor: 'pointer', textAlign: 'left', fontSize: '12px',
                          width: '100%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'
                        }}
                      >
                        <FileText size={14} style={{ flexShrink: 0 }} />
                        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{f.title}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Ingested Papers Section */}
              {files?.papers && files.papers.length > 0 && (
                <div>
                  <div style={{ fontSize: '10px', fontWeight: 'bold', color: '#10b981', textTransform: 'uppercase', marginBottom: '6px', letterSpacing: '0.5px' }}>Paper Summaries</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {files.papers.map(f => (
                      <button
                        key={f.filename}
                        onClick={() => loadFile('papers', f.filename)}
                        style={{
                          display: 'flex', alignItems: 'center', gap: '8px', border: 'none', background: activeFilename === f.filename ? 'rgba(16,185,129,0.1)' : 'transparent',
                          color: activeFilename === f.filename ? '#10b981' : 'var(--text-secondary)', padding: '6px 8px', borderRadius: '6px', cursor: 'pointer', textAlign: 'left', fontSize: '12px',
                          width: '100%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'
                        }}
                      >
                        <FileText size={14} style={{ flexShrink: 0 }} />
                        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{f.title}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Editor Panel */}
      <div className="glass" style={{ display: 'grid', gridTemplateRows: 'auto 1fr', padding: '16px', overflow: 'hidden', minHeight: '0' }}>
        {isLoadingFile ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <span className="pulse-loading" style={{ fontSize: '13px' }}>Reading markdown file from Obsidian Vault...</span>
          </div>
        ) : !activeFilename ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)', gap: '8px' }}>
            <FileText size={32} style={{ opacity: 0.3 }} />
            <span style={{ fontSize: '13px' }}>No document active.</span>
            <span style={{ fontSize: '11px' }}>Select an Obsidian card from the explorer sidebar.</span>
          </div>
        ) : (
          <>
            {/* Editor Action Header */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', borderBottom: '1px solid var(--border-color)', paddingBottom: '14px', marginBottom: '16px' }}>

              {/* Top Row: Title, Badges, View Toggle & Save */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <span style={{ fontSize: '10px', color: 'var(--primary)', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    {activeCategory} / {activeFilename}
                  </span>
                  <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '17px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', marginTop: '2px' }}>
                    <span>{frontmatter.title || activeFilename.replace('.md', '')}</span>
                    {frontmatter.full_pdf_ingested && (
                      <span style={{ fontSize: '10px', background: 'rgba(16,185,129,0.15)', color: '#10b981', border: '1px solid rgba(16,185,129,0.3)', padding: '2px 8px', borderRadius: '12px', fontWeight: '600' }}>
                        Full PDF Ingested
                      </span>
                    )}
                    {frontmatter.fact_check_score !== undefined && (
                      <span style={{ fontSize: '10px', background: frontmatter.fact_check_score >= 80 ? 'rgba(16,185,129,0.15)' : 'rgba(244,63,94,0.15)', color: frontmatter.fact_check_score >= 80 ? '#10b981' : '#f43f5e', border: '1px solid var(--border-color)', padding: '2px 8px', borderRadius: '12px', fontWeight: '700' }}>
                        Fact-Check: {frontmatter.fact_check_score}%
                      </span>
                    )}
                  </h3>
                </div>

                <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                  {/* View toggles */}
                  <div style={{ display: 'flex', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '2px' }}>
                    <button
                      onClick={() => setEditMode('edit')}
                      style={{
                        background: editMode === 'edit' ? 'var(--primary-glow)' : 'transparent',
                        color: editMode === 'edit' ? 'var(--primary)' : 'var(--text-secondary)',
                        border: 'none', padding: '4px 10px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px'
                      }}
                    >
                      <FileEdit size={12} />
                      <span>Source</span>
                    </button>
                    <button
                      onClick={() => setEditMode('preview')}
                      style={{
                        background: editMode === 'preview' ? 'var(--primary-glow)' : 'transparent',
                        color: editMode === 'preview' ? 'var(--primary)' : 'var(--text-secondary)',
                        border: 'none', padding: '4px 10px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px'
                      }}
                    >
                      <Eye size={12} />
                      <span>Preview</span>
                    </button>
                  </div>

                  {/* Save Action */}
                  <button
                    onClick={() => void handleSave()}
                    disabled={saveStatus === 'saving'}
                    style={{
                      backgroundColor: saveStatus === 'saved' ? 'var(--success)' : 'var(--primary)',
                      border: 'none', color: '#fff', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', fontSize: '12px',
                      display: 'flex', alignItems: 'center', gap: '6px', transition: 'var(--transition-fast)'
                    }}
                  >
                    {saveStatus === 'saving' ? (
                      <span>Saving...</span>
                    ) : saveStatus === 'saved' ? (
                      <>
                        <Check size={14} />
                        <span>Saved to Obsidian</span>
                      </>
                    ) : saveStatus === 'error' ? (
                      <>
                        <AlertCircle size={14} />
                        <span>Error Saving</span>
                      </>
                    ) : (
                      <>
                        <Save size={14} />
                        <span>Save to Vault</span>
                      </>
                    )}
                  </button>

                  {/* Checkmate Audit Action */}
                  <button
                    onClick={runCheckmateAudit}
                    disabled={checkmateLoading}
                    style={{
                      background: 'rgba(139,92,246,0.15)', color: '#c084fc', border: '1px solid rgba(139,92,246,0.4)',
                      padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', fontWeight: '700', fontSize: '12px',
                      display: 'flex', alignItems: 'center', gap: '6px'
                    }}
                  >
                    <Sparkles size={14} />
                    <span>{checkmateLoading ? 'Auditing...' : '♟️ Checkmate Audit'}</span>
                  </button>

                  {/* Visual Page Preview Action */}
                  <button
                    onClick={() => setVisualPreviewOpen(true)}
                    style={{
                      background: 'rgba(59,130,246,0.15)', color: '#60a5fa', border: '1px solid rgba(59,130,246,0.4)',
                      padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', fontWeight: '700', fontSize: '12px',
                      display: 'flex', alignItems: 'center', gap: '6px'
                    }}
                  >
                    <Layers size={14} />
                    <span>Visual Page Preview</span>
                  </button>

                </div>
              </div>

              {/* Checkmate Audit Results Panel */}
              {checkmateOpen && (
                <div style={{ background: 'rgba(139,92,246,0.06)', border: '1px solid rgba(139,92,246,0.3)', borderRadius: '10px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '16px' }}>♟️</span>
                      <span style={{ fontSize: '13px', fontWeight: '800', color: '#c084fc', textTransform: 'uppercase', letterSpacing: '0.5px' }}>The Checkmate Double-Tested Audit</span>
                      {checkmateData && (
                        <span style={{ fontSize: '11px', padding: '2px 8px', borderRadius: '10px', fontWeight: '800', background: checkmateData.checkmate_passed ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)', color: checkmateData.checkmate_passed ? '#10b981' : '#f87171', border: `1px solid ${checkmateData.checkmate_passed ? '#10b981' : '#f87171'}` }}>
                          {checkmateData.status} ({checkmateData.score}%)
                        </span>
                      )}
                    </div>
                    <button onClick={() => setCheckmateOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '18px' }}>×</button>
                  </div>

                  {checkmateLoading && (
                    <div style={{ color: 'var(--text-muted)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Sparkles size={14} style={{ animation: 'pulse 1.5s infinite' }} />
                      <span>Running multi-modal PDF layout, section numbering, author attribution, and bibliography audit...</span>
                    </div>
                  )}

                  {checkmateData && !checkmateLoading && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '8px' }}>
                        {Object.entries(checkmateData.checks || {}).map(([key, val]: [string, any]) => (
                          <div key={key} style={{ background: 'rgba(255,255,255,0.03)', border: `1px solid ${val.passed ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}`, borderRadius: '7px', padding: '10px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <span style={{ fontSize: '11px', fontWeight: '700', color: val.passed ? '#34d399' : '#f87171' }}>{key.replace(/_/g, ' ').toUpperCase()}</span>
                              <span style={{ fontSize: '12px' }}>{val.passed ? '✅' : '❌'}</span>
                            </div>
                            <span style={{ fontSize: '11px', color: '#94a3b8' }}>{val.detail}</span>
                          </div>
                        ))}
                      </div>

                      <div style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.3)', borderRadius: '8px', padding: '10px 14px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <Check size={16} style={{ color: '#10b981' }} />
                          <span style={{ fontSize: '12px', fontWeight: '700', color: '#34d399' }}>Certificate: {checkmateData.certificate?.title}</span>
                        </div>
                        <span style={{ fontSize: '11px', fontWeight: '800', color: '#10b981', background: 'rgba(16,185,129,0.2)', padding: '3px 10px', borderRadius: '12px' }}>
                          {checkmateData.certificate?.decision}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Sub Toolbar: Venue Advisor Agent Panel */}
              {activeCategory === 'drafts' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>

                  {/* Profile Quick-Config Row */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(255,255,255,0.02)', padding: '8px 12px', borderRadius: '8px', border: '1px solid var(--border-color)', flexWrap: 'wrap' }}>
                    <User size={12} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '600' }}>Profile:</span>

                    <select value={profileGoal} onChange={e => setProfileGoal(e.target.value)}
                      style={{ background: 'rgba(15,23,42,0.8)', color: '#a78bfa', border: '1px solid rgba(139,92,246,0.3)', borderRadius: '6px', padding: '4px 8px', fontSize: '11px', fontWeight: '600', outline: 'none', cursor: 'pointer' }}>
                      <option value="top_conference">🏆 Top Conference Only</option>
                      <option value="balanced">⚖️ Balanced Strategy</option>
                      <option value="safe_accept">✅ Safe Accept First</option>
                      <option value="journal_impact">📚 Journal Impact</option>
                    </select>

                    <select value={profileTimeline} onChange={e => setProfileTimeline(e.target.value)}
                      style={{ background: 'rgba(15,23,42,0.8)', color: '#67e8f9', border: '1px solid rgba(6,182,212,0.3)', borderRadius: '6px', padding: '4px 8px', fontSize: '11px', fontWeight: '600', outline: 'none', cursor: 'pointer' }}>
                      <option value="urgent">⚡ Urgent (weeks)</option>
                      <option value="normal">📅 Normal (months)</option>
                      <option value="journal">📖 Journal cycle (6-12mo)</option>
                    </select>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Citations:</span>
                      <input type="number" value={profileCitations} onChange={e => setProfileCitations(Number(e.target.value))}
                        style={{ background: 'rgba(15,23,42,0.8)', color: '#fff', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '4px 8px', fontSize: '11px', width: '72px', outline: 'none' }} />
                    </div>

                    {/* Manual Venue Dropdown */}
                    <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Quick select:</span>
                      <select value={selectedVenue} onChange={e => setSelectedVenue(e.target.value)}
                        style={{ background: 'rgba(15,23,42,0.8)', color: '#93c5fd', border: '1px solid rgba(59,130,246,0.3)', borderRadius: '6px', padding: '4px 8px', fontSize: '11px', fontWeight: '600', outline: 'none', cursor: 'pointer' }}>
                        {availableVenues.map(venue => <option key={venue} value={venue}>{venue}</option>)}
                        <option value="ALL">📦 All Venues</option>
                      </select>
                    </div>
                  </div>

                  {/* Action Buttons Row */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                    {/* AI Venue Recommendation Button */}
                    <button
                      onClick={handleGetVenueRecommendation}
                      disabled={venueAdvisorLoading}
                      style={{
                        background: venueAdvisorLoading ? 'rgba(139,92,246,0.08)' : 'rgba(139,92,246,0.18)',
                        color: '#c084fc',
                        border: '1px solid rgba(139,92,246,0.5)',
                        padding: '6px 14px',
                        borderRadius: '7px',
                        cursor: venueAdvisorLoading ? 'wait' : 'pointer',
                        fontSize: '12px',
                        fontWeight: '700',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        transition: 'all 0.2s'
                      }}
                    >
                      <Sparkles size={13} />
                      <span>{venueAdvisorLoading ? 'Analyzing...' : 'AI Venue Advisor'}</span>
                    </button>

                    {/* Single paper release test */}
                    {activeCategory === 'drafts' && activeFile && (
                      <button
                        onClick={() => runSinglePaperPublisherReadiness()}
                        disabled={publisherSuiteLoading}
                        style={{
                          background: publisherSuiteLoading ? 'rgba(59,130,246,0.08)' : 'rgba(59,130,246,0.16)',
                          color: '#93c5fd', border: '1px solid rgba(59,130,246,0.45)', padding: '6px 14px', borderRadius: '7px',
                          cursor: publisherSuiteLoading ? 'wait' : 'pointer', fontSize: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px'
                        }}
                        title={`Compile and audit current paper (${activeFile}) against all supported venues`}
                      >
                        {publisherSuiteLoading ? <RefreshCw size={13} className="spin" /> : <ShieldCheck size={13} />}
                        <span>{publisherSuiteLoading ? 'Testing paper…' : 'Test this paper × venues'}</span>
                      </button>
                    )}

                    {/* Vault-wide release matrix */}
                    <button
                      onClick={runPublisherReadiness}
                      disabled={publisherSuiteLoading}
                      style={{
                        background: publisherSuiteLoading ? 'rgba(45,212,191,0.08)' : 'rgba(45,212,191,0.16)',
                        color: '#5eead4', border: '1px solid rgba(45,212,191,0.45)', padding: '6px 14px', borderRadius: '7px',
                        cursor: publisherSuiteLoading ? 'wait' : 'pointer', fontSize: '12px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '6px'
                      }}
                      title="Compile and audit every draft against every supported venue"
                    >
                      {publisherSuiteLoading ? <RefreshCw size={13} className="spin" /> : <ShieldCheck size={13} />}
                      <span>{publisherSuiteLoading ? 'Testing all papers…' : 'Test all papers × venues'}</span>
                    </button>
                    <button
                      onClick={downloadPublisherBundle}
                      disabled={publisherSuiteLoading || !publisherSuiteData?.ready_count}
                      style={{
                        background: publisherSuiteData?.ready_count ? 'rgba(16,185,129,0.16)' : 'rgba(255,255,255,0.03)',
                        color: publisherSuiteData?.ready_count ? '#6ee7b7' : 'var(--text-muted)',
                        border: `1px solid ${publisherSuiteData?.ready_count ? 'rgba(16,185,129,0.42)' : 'var(--border-color)'}`,
                        padding: '6px 12px', borderRadius: '7px', cursor: publisherSuiteLoading || !publisherSuiteData?.ready_count ? 'not-allowed' : 'pointer',
                        fontSize: '12px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px'
                      }}
                      title={publisherSuiteData?.ready_count ? 'Download only verified publish-ready artifacts' : 'Available after at least one manuscript passes every release gate'}
                    >
                      <Download size={13} />
                      <span>Download verified bundle</span>
                    </button>

                    {/* Export LaTeX */}
                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        await handleSave();
                        try {
                          const res = await apiFetch(`/api/vault/export-venue-latex?filename=${activeFilename}&venue=${selectedVenue}`);
                          if (res.ok) {
                            const data = await res.json();
                            if (selectedVenue === 'ALL' && data.bundle) {
                              Object.entries(data.bundle).forEach(([vKey, code]) => {
                                const blob = new Blob([code as string], { type: 'text/x-tex' });
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url; a.download = `${activeFilename.replace('.md', '')}_${vKey}.tex`;
                                document.body.appendChild(a); a.click(); document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                              });
                            } else if (data.tex_code) {
                              const blob = new Blob([data.tex_code], { type: 'text/x-tex' });
                              const url = URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = url; a.download = data.tex_filename || `${activeFilename.replace('.md', '')}_${selectedVenue}.tex`;
                              document.body.appendChild(a); a.click(); document.body.removeChild(a);
                              URL.revokeObjectURL(url);
                            }
                            if (data.bib_code) {
                              const bibBlob = new Blob([data.bib_code], { type: 'text/plain' });
                              const bibUrl = URL.createObjectURL(bibBlob);
                              const bibA = document.createElement('a');
                              bibA.href = bibUrl; bibA.download = 'references.bib';
                              document.body.appendChild(bibA); bibA.click(); document.body.removeChild(bibA);
                              URL.revokeObjectURL(bibUrl);
                            }
                          }
                        } catch (e) { alert('Export failed'); }
                      }}
                      style={{ background: 'rgba(59,130,246,0.15)', color: '#93c5fd', border: '1px solid rgba(59,130,246,0.4)', padding: '6px 12px', borderRadius: '7px', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}
                    >
                      <FileText size={13} />
                      <span>Export {selectedVenue === 'ALL' ? 'All LaTeX' : `${selectedVenue} LaTeX`}</span>
                    </button>

                    {/* Copy LaTeX */}
                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        await handleSave();
                        try {
                          const res = await apiFetch(`/api/vault/export-venue-latex?filename=${activeFilename}&venue=${selectedVenue}`);
                          if (res.ok) {
                            const data = await res.json();
                            const code = data.tex_code || (data.bundle ? Object.values(data.bundle)[0] : '');
                            if (code) {
                              await navigator.clipboard.writeText(code as string);
                              alert(`Copied ${selectedVenue} LaTeX to clipboard! Paste into Overleaf.`);
                            } else {
                              alert('No LaTeX generated.');
                            }
                          } else {
                            const err = await res.json().catch(() => ({}));
                            alert(`Failed to copy LaTeX: ${err.detail || 'Server error'}`);
                          }
                        } catch (e: any) { alert(`Error copying LaTeX: ${e.message || e}`); }
                      }}
                      style={{ background: 'rgba(168,85,247,0.15)', color: '#c084fc', border: '1px solid rgba(168,85,247,0.4)', padding: '6px 12px', borderRadius: '7px', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}
                    >
                      <Save size={13} />
                      <span>Copy LaTeX</span>
                    </button>

                    {/* Download PDF */}
                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        await handleSave();
                        const venue = selectedVenue === 'ALL' ? 'IEEEtran' : selectedVenue;
                        try {
                          const res = await apiFetch(`/api/vault/export-venue-pdf?filename=${activeFilename}&venue=${venue}`);
                          if (res.ok) {
                            const blob = await res.blob();
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `${activeFilename.replace('.md', '')}_${venue}.pdf`;
                            document.body.appendChild(a); a.click(); document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                          } else {
                            const err = await res.json().catch(() => ({}));
                            const msg = typeof err.detail === 'object' ? JSON.stringify(err.detail) : (err.detail || 'PDF generation failed');
                            alert(`PDF Compilation Error: ${msg}`);
                          }
                        } catch (e: any) {
                          alert(`Failed to download PDF: ${e.message || e}`);
                        }
                      }}
                      style={{ background: 'rgba(239,68,68,0.15)', color: '#f87171', border: '1px solid rgba(239,68,68,0.4)', padding: '6px 12px', borderRadius: '7px', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}
                    >
                      <Download size={13} />
                      <span>Download PDF</span>
                    </button>
                  </div>

                  {/* Publisher Readiness Matrix */}
                  {publisherSuiteOpen && (
                    <div style={{ background: 'rgba(45,212,191,0.045)', border: '1px solid rgba(45,212,191,0.3)', borderRadius: '10px', padding: '14px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <BarChart3 size={15} style={{ color: '#5eead4' }} />
                          <div>
                            <div style={{ fontSize: '12px', fontWeight: '800', color: '#5eead4', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Publisher readiness matrix</div>
                            <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>Every draft × every venue · duplicate-content and substantive-value gates are fail-closed</div>
                          </div>
                        </div>
                        <button onClick={() => setPublisherSuiteOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '18px', lineHeight: 1 }}>×</button>
                      </div>

                      {publisherSuiteLoading && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px', color: 'var(--text-secondary)', fontSize: '11px', background: 'rgba(255,255,255,0.025)', borderRadius: '7px' }}>
                          <RefreshCw size={13} className="spin" />
                          <span>Compiling, auditing, and comparing all manuscripts{publisherJobId ? ` · job ${publisherJobId}` : ''}. This can take a few minutes for a large vault.</span>
                        </div>
                      )}

                      {publisherSuiteError && <div style={{ color: '#f87171', fontSize: '11px', padding: '9px 11px', background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '7px' }}>{publisherSuiteError}</div>}

                      {publisherSuiteData && !publisherSuiteLoading && (
                        <>
                          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '7px' }}>
                            {[
                              ['Manuscripts', publisherSuiteData.draft_count ?? 0, '#cbd5e1'],
                              ['Venue tests', publisherSuiteData.total_tests ?? 0, '#93c5fd'],
                              ['Compiled', publisherSuiteData.compiled_count ?? 0, '#a7f3d0'],
                              ['Ready', publisherSuiteData.ready_count ?? 0, '#5eead4'],
                              ['Blocked', publisherSuiteData.blocked_count ?? 0, '#fda4af'],
                            ].map(([label, value, color]) => (
                              <div key={String(label)} style={{ background: 'rgba(255,255,255,0.025)', border: '1px solid var(--border-color)', borderRadius: '7px', padding: '9px 10px' }}>
                                <div style={{ fontSize: '9px', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.4px' }}>{label}</div>
                                <div style={{ color: String(color), fontSize: '18px', fontWeight: '800', marginTop: '2px' }}>{value}</div>
                              </div>
                            ))}
                          </div>

                          <div style={{ display: 'flex', flexDirection: 'column', gap: '7px', maxHeight: '340px', overflowY: 'auto' }}>
                            {(publisherSuiteData.manuscripts || []).map((manuscript: any) => {
                              const isReady = manuscript.readiness === 'READY_FOR_HUMAN_REVIEW';
                              const originalityBlocked = manuscript.originality?.passed === false;
                              return (
                                <div key={manuscript.filename} style={{ background: 'rgba(255,255,255,0.025)', border: `1px solid ${isReady ? 'rgba(45,212,191,0.32)' : originalityBlocked ? 'rgba(244,63,94,0.35)' : 'var(--border-color)'}`, borderRadius: '8px', padding: '10px 11px' }}>
                                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' }}>
                                    <div style={{ minWidth: 0 }}>
                                      <div style={{ fontSize: '11px', fontWeight: '800', color: '#e2e8f0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{manuscript.title}</div>
                                      <div style={{ fontSize: '9px', color: 'var(--text-muted)', marginTop: '2px' }}>{manuscript.filename}</div>
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
                                      <button
                                        onClick={() => runSinglePaperPublisherReadiness(manuscript.filename)}
                                        disabled={publisherSuiteLoading}
                                        style={{
                                          background: 'rgba(59,130,246,0.12)', color: '#93c5fd', border: '1px solid rgba(59,130,246,0.35)',
                                          padding: '3px 8px', borderRadius: '6px', fontSize: '9px', fontWeight: '700',
                                          cursor: publisherSuiteLoading ? 'wait' : 'pointer', display: 'flex', alignItems: 'center', gap: '4px'
                                        }}
                                        title={`Re-test ${manuscript.filename} across all 12 venues`}
                                      >
                                        <RefreshCw size={10} className={publisherSuiteLoading ? 'spin' : ''} />
                                        <span>Test paper × venues</span>
                                      </button>
                                      <span style={{ fontSize: '9px', fontWeight: '800', padding: '3px 7px', borderRadius: '10px', color: isReady ? '#5eead4' : originalityBlocked ? '#fda4af' : '#fbbf24', background: isReady ? 'rgba(45,212,191,0.12)' : originalityBlocked ? 'rgba(244,63,94,0.12)' : 'rgba(251,191,36,0.12)' }}>{manuscript.readiness}</span>
                                    </div>
                                  </div>
                                  <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginTop: '8px', fontSize: '10px', color: 'var(--text-secondary)' }}>
                                    <span><LockKeyhole size={11} style={{ verticalAlign: 'middle', marginRight: '3px', color: originalityBlocked ? '#f87171' : '#34d399' }} />Originality: <strong style={{ color: originalityBlocked ? '#f87171' : '#34d399' }}>{manuscript.originality?.status || 'NOT RUN'}</strong></span>
                                    <span>Value: <strong style={{ color: manuscript.value?.substantive_value_passed ? '#34d399' : '#fbbf24' }}>{manuscript.value?.score ?? 0}%</strong></span>
                                    <span>Ready venues: <strong style={{ color: '#93c5fd' }}>{(manuscript.ready_venues || []).join(', ') || 'none'}</strong></span>
                                  </div>
                                  <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginTop: '8px' }}>
                                    {Object.entries(manuscript.venue_results || {}).map(([venueName, venueResult]: [string, any]) => (
                                      <span key={venueName} title={venueResult.error || (venueResult.publish_ready ? 'All release gates passed' : (venueResult.blocking_reasons || []).join(', ') || 'Needs review')} style={{ fontSize: '9px', padding: '3px 6px', borderRadius: '5px', border: `1px solid ${venueResult.publish_ready ? 'rgba(45,212,191,0.35)' : venueResult.compiled ? 'rgba(251,191,36,0.3)' : 'rgba(244,63,94,0.3)'}`, color: venueResult.publish_ready ? '#5eead4' : venueResult.compiled ? '#fbbf24' : '#fda4af', background: venueResult.publish_ready ? 'rgba(45,212,191,0.08)' : venueResult.compiled ? 'rgba(251,191,36,0.08)' : 'rgba(244,63,94,0.08)' }}>{venueName} {venueResult.publish_ready ? '✓' : venueResult.compiled ? '!' : '×'}</span>
                                    ))}
                                  </div>
                                  {!manuscript.value?.substantive_value_passed && (
                                    <div style={{ marginTop: '7px', fontSize: '10px', color: '#fbbf24' }}>Value gate: {Object.values(manuscript.value?.checks || {}).filter((check: any) => !check.passed).map((check: any) => check.detail).join(' · ')}</div>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                          {(publisherSuiteData.collection_originality?.pairs || []).length > 0 && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '7px', padding: '9px 10px', background: 'rgba(244,63,94,0.06)', border: '1px solid rgba(244,63,94,0.28)', borderRadius: '7px' }}>
                              <div style={{ fontSize: '10px', fontWeight: '800', color: '#fda4af', textTransform: 'uppercase', letterSpacing: '0.4px' }}>Cross-manuscript originality flags</div>
                              <div style={{ fontSize: '10px', color: 'var(--text-secondary)', lineHeight: 1.4 }}>These pairs require separate work before any venue submission. Exact duplicates are shown separately from high copied-prose overlap.</div>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '150px', overflowY: 'auto' }}>
                                {publisherSuiteData.collection_originality.pairs.map((pair: any) => (
                                  <div key={`${pair.file_1}-${pair.file_2}`} style={{ display: 'flex', justifyContent: 'space-between', gap: '8px', alignItems: 'center', fontSize: '9px', color: '#cbd5e1' }}>
                                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{pair.file_1} ↔ {pair.file_2}</span>
                                    <span style={{ flexShrink: 0, color: pair.exact_duplicate ? '#f87171' : '#fbbf24', fontWeight: '800' }}>{pair.exact_duplicate ? 'EXACT' : `${pair.five_gram_overlap_pct}% overlap`}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          <div style={{ fontSize: '10px', color: 'var(--text-muted)', lineHeight: 1.45, padding: '8px 10px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                            <strong style={{ color: '#cbd5e1' }}>Release rule:</strong> “Ready” means the manuscript passed PDF/venue checks, has no exact or high-overlap sibling, and states a grounded contribution with method/scope/limitations. It remains ready for human/journal review—not an automatic acceptance.
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {/* Venue Advisor Results Panel */}
                  {venueAdvisorOpen && (
                    <div style={{ background: 'rgba(139,92,246,0.04)', border: '1px solid rgba(139,92,246,0.25)', borderRadius: '10px', padding: '14px', display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '450px', overflow: 'hidden' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <Target size={14} style={{ color: '#c084fc' }} />
                          <span style={{ fontSize: '12px', fontWeight: '700', color: '#c084fc', textTransform: 'uppercase', letterSpacing: '0.5px' }}>AI Venue Recommendations</span>
                        </div>
                        <button onClick={() => setVenueAdvisorOpen(false)}
                          style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '18px', lineHeight: 1 }}>×</button>
                      </div>

                      {venueAdvisorLoading && (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '12px', color: 'var(--text-muted)', fontSize: '12px' }}>
                          <Sparkles size={14} style={{ animation: 'pulse 1.5s infinite' }} />
                          <span>Analyzing paper content, user profile, and O-1A criteria...</span>
                        </div>
                      )}

                      {venueAdvisorError && (
                        <div style={{ color: '#f87171', fontSize: '12px', padding: '8px 12px', background: 'rgba(239,68,68,0.1)', borderRadius: '6px', border: '1px solid rgba(239,68,68,0.3)' }}>
                          {venueAdvisorError}
                        </div>
                      )}

                      {venueRecommendations && !venueAdvisorLoading && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '380px', overflowY: 'auto', paddingRight: '6px' }}>
                          {venueRecommendations.map((rec: any, idx: number) => {
                            const diffKey = rec.difficulty || 'Moderate';
                            const diffColor = DIFFICULTY_COLOR[diffKey] || '#94a3b8';
                            const o1aNum = typeof rec.o1a_value === 'number' ? Math.max(0, Math.min(5, rec.o1a_value)) : 3;

                            let rationaleStr = '';
                            if (typeof rec.ai_rationale === 'string') {
                              rationaleStr = rec.ai_rationale;
                            } else if (rec.ai_rationale && typeof rec.ai_rationale === 'object') {
                              rationaleStr = rec.ai_rationale.rationale || rec.ai_rationale.strategic_tip || JSON.stringify(rec.ai_rationale);
                            } else if (rec.o1a_rationale) {
                              rationaleStr = String(rec.o1a_rationale);
                            }

                            const scoreNum = typeof rec.overall_score === 'number' ? rec.overall_score : 0;
                            const acceptPct = typeof rec.acceptance_rate === 'number' ? Math.round(rec.acceptance_rate * 100) : 0;
                            const venueName = rec.venue_key || rec.full_name || 'Venue';

                            return (
                              <div key={venueName || idx}
                                onClick={() => { setSelectedVenue(venueName); }}
                                style={{
                                  display: 'grid', gridTemplateColumns: 'auto 1fr auto', alignItems: 'start', gap: '12px',
                                  padding: '12px', borderRadius: '8px', cursor: 'pointer', transition: 'all 0.15s',
                                  background: selectedVenue === venueName ? 'rgba(139,92,246,0.15)' : 'rgba(255,255,255,0.02)',
                                  border: `1px solid ${selectedVenue === venueName ? 'rgba(139,92,246,0.5)' : 'var(--border-color)'}`,
                                }}
                              >
                                {/* Rank badge */}
                                <div style={{
                                  width: '28px', height: '28px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                                  background: idx === 0 ? 'rgba(250,204,21,0.2)' : idx === 1 ? 'rgba(156,163,175,0.2)' : 'rgba(180,83,9,0.2)',
                                  color: idx === 0 ? '#fbbf24' : idx === 1 ? '#9ca3af' : '#b45309',
                                  fontSize: '13px', fontWeight: '800', flexShrink: 0
                                }}>#{idx + 1}</div>

                                {/* Venue info */}
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', minWidth: 0 }}>
                                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                                    <span style={{ fontSize: '13px', fontWeight: '700', color: '#e2e8f0' }}>{venueName}</span>
                                    <span style={{ fontSize: '10px', padding: '1px 7px', borderRadius: '10px', fontWeight: '700',
                                      background: `${diffColor}22`, color: diffColor,
                                      border: `1px solid ${diffColor}44` }}>
                                      {diffKey}
                                    </span>
                                    <span style={{ fontSize: '10px', color: '#94a3b8' }}>{rec.type || ''}</span>
                                    <span style={{ fontSize: '10px', color: '#94a3b8' }}>Accept: {acceptPct}%</span>
                                  </div>
                                  <div style={{ fontSize: '11px', color: '#f59e0b', letterSpacing: '1px' }}>
                                    {O1A_STARS(o1aNum)} O-1A
                                  </div>
                                  {rationaleStr ? (
                                    <p style={{ fontSize: '11px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.5' }}>
                                      {rationaleStr}
                                    </p>
                                  ) : null}
                                </div>

                                {/* Score + Select button */}
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '6px', flexShrink: 0 }}>
                                  <span style={{ fontSize: '18px', fontWeight: '800',
                                    color: scoreNum >= 8 ? '#10b981' : scoreNum >= 6 ? '#f59e0b' : '#94a3b8'
                                  }}>{scoreNum.toFixed(1)}</span>
                                  <span style={{ fontSize: '9px', color: 'var(--text-muted)' }}>/ 10.0</span>
                                  {selectedVenue === venueName ? (
                                    <span style={{ fontSize: '10px', color: '#10b981', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '3px' }}>
                                      <Check size={10} /> Selected
                                    </span>
                                  ) : (
                                    <button onClick={(e) => { e.stopPropagation(); setSelectedVenue(venueName); }}
                                      style={{ fontSize: '10px', background: 'rgba(59,130,246,0.15)', color: '#93c5fd', border: '1px solid rgba(59,130,246,0.3)', padding: '3px 8px', borderRadius: '5px', cursor: 'pointer', fontWeight: '600' }}>
                                      Select
                                    </button>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Split layout: Editor Text vs Preview/Frontmatter */}
            <div className={editMode === 'edit' ? "responsive-doc-split" : ""} style={{ gap: '16px', overflowY: 'auto', height: '100%', minHeight: '0', flex: 1 }}>

              {/* Primary Content Editor / Preview Pane */}
              <div style={{ height: '100%', minHeight: '350px', overflowY: 'auto' }}>
                {editMode === 'edit' ? (
                  <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    style={{
                      width: '100%', minHeight: '450px', height: '100%', background: 'rgba(0,0,0,0.15)', color: 'var(--text-primary)', border: '1px solid var(--border-color)',
                      borderRadius: '8px', padding: '16px', fontFamily: 'var(--font-mono)', fontSize: '13px', resize: 'vertical', outline: 'none', lineHeight: '1.6', overflowY: 'auto'
                    }}
                  />
                ) : (
                  <div style={{ minHeight: '450px', height: '100%', overflowY: 'auto', background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '24px' }}>
                    <LinkRenderer
                      content={content}
                      onNavigateWikilink={(targetFilename) => {
                        if (!files) return;
                        for (const cat of ['drafts', 'debates', 'papers', 'concepts'] as const) {
                          const found = files[cat]?.find(f => f.filename === targetFilename || f.filename === `${targetFilename}.md`);
                          if (found) {
                            loadFile(cat, found.filename);
                            break;
                          }
                        }
                      }}
                    />
                  </div>
                )}
              </div>

              {/* Right Side Panel: YAML Frontmatter properties editor */}
              {editMode === 'edit' && (
                <div style={{ borderLeft: '1px solid var(--border-color)', paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto' }}>
                  <h4 style={{ fontFamily: 'var(--font-heading)', fontSize: '13px', fontWeight: '700', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
                    Metadata properties (YAML)
                  </h4>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                    {Object.entries(frontmatter).map(([key, val]) => {
                      // Skip complex objects and custom handled keys
                      if (['tags', 'verification_matrix', 'peer_review', 'verification_matrix_details'].includes(key)) return null;

                      const isLongText = key === 'topic' || key === 'title';

                      return (
                        <div key={key} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                          <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'capitalize', fontWeight: '600' }}>
                            {key.replace('_', ' ')}
                          </span>
                          {isLongText ? (
                            <textarea
                              rows={3}
                              value={String(val || '')}
                              onChange={(e) => setFrontmatter((prev: any) => ({ ...prev, [key]: e.target.value }))}
                              style={{
                                background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px',
                                color: '#fff', fontSize: '12px', padding: '8px', outline: 'none', resize: 'vertical',
                                fontFamily: 'var(--font-sans)', lineHeight: '1.4', width: '100%'
                              }}
                            />
                          ) : (
                            <input
                              type="text"
                              value={String(val || '')}
                              onChange={(e) => setFrontmatter((prev: any) => ({ ...prev, [key]: e.target.value }))}
                              style={{
                                background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px',
                                color: '#fff', fontSize: '12px', padding: '6px 8px', outline: 'none', width: '100%'
                              }}
                            />
                          )}
                        </div>
                      );
                    })}

                    {/* Simple frontmatter tag creator */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '600' }}>Tags (comma separated)</span>
                      <input
                        type="text"
                        value={Array.isArray(frontmatter.tags) ? frontmatter.tags.join(', ') : ''}
                        onChange={(e) => {
                          const tagList = e.target.value.split(',').map(t => t.trim()).filter(Boolean);
                          setFrontmatter((prev: any) => ({ ...prev, tags: tagList }));
                        }}
                        style={{
                          background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', fontSize: '12px', padding: '6px 8px', outline: 'none', width: '100%'
                        }}
                      />
                    </div>
                  </div>

                  {/* Automated Peer Reviewer Audit Card (Sakana AI Rubric) */}
                  {frontmatter.peer_review && (
                    <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <span style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', color: '#8b5cf6', letterSpacing: '0.5px' }}>
                          Peer Review Audit
                        </span>
                        <span style={{
                          fontSize: '10px', fontWeight: '800', padding: '2px 8px', borderRadius: '12px',
                          background: frontmatter.peer_review.overall_decision === 'ACCEPT' ? 'rgba(16,185,129,0.2)' : frontmatter.peer_review.overall_decision === 'WEAK ACCEPT' ? 'rgba(245,158,11,0.2)' : 'rgba(239,68,68,0.2)',
                          color: frontmatter.peer_review.overall_decision === 'ACCEPT' ? '#10b981' : frontmatter.peer_review.overall_decision === 'WEAK ACCEPT' ? '#f59e0b' : '#ef4444',
                          border: '1px solid var(--border-color)'
                        }}>
                          {frontmatter.peer_review.overall_decision}
                        </span>
                      </div>

                      {/* Score bars */}
                      {frontmatter.peer_review.scores && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                          {Object.entries(frontmatter.peer_review.scores).map(([sKey, sVal]: [string, any]) => (
                            <div key={sKey} style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--text-secondary)', textTransform: 'capitalize' }}>
                                <span>{sKey.replace('_', ' ')}</span>
                                <span style={{ fontWeight: '700', color: '#fff' }}>{sVal}/10</span>
                              </div>
                              <div style={{ height: '4px', width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                                <div style={{ height: '100%', width: `${(Number(sVal) / 10) * 100}%`, background: Number(sVal) >= 8 ? '#10b981' : '#f59e0b', borderRadius: '2px' }} />
                              </div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Key Strengths */}
                      {frontmatter.peer_review.key_strengths && frontmatter.peer_review.key_strengths.length > 0 && (
                        <div style={{ fontSize: '11px' }}>
                          <span style={{ fontWeight: '600', color: '#10b981' }}>Key Strengths:</span>
                          <ul style={{ paddingLeft: '14px', margin: '4px 0 0 0', color: 'var(--text-secondary)' }}>
                            {frontmatter.peer_review.key_strengths.map((str: string, idx: number) => (
                              <li key={idx}>{str}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {visualPreviewOpen && activeFilename && (
        <PDFVisualPreviewModal
          filename={activeFilename}
          venue={selectedVenue}
          onClose={() => setVisualPreviewOpen(false)}
        />
      )}
    </div>
  );
};


export default DocEditor;
