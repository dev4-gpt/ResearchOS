import React, { useState, useEffect } from 'react';
import { FolderOpen, Save, FileText, Check, AlertCircle, Eye, FileEdit, RefreshCw, Download } from 'lucide-react';
import { apiFetch } from '../api';

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

const DocEditor: React.FC = () => {
  const [files, setFiles] = useState<VaultFilesData | null>(null);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [activeFilename, setActiveFilename] = useState<string | null>(null);
  const [isLoadingList, setIsLoadingList] = useState(true);
  const [isLoadingFile, setIsLoadingFile] = useState(false);
  
  // Editor States
  const [content, setContent] = useState('');
  const [frontmatter, setFrontmatter] = useState<any>({});
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [editMode, setEditMode] = useState<'edit' | 'preview'>('edit');
  const [selectedVenue, setSelectedVenue] = useState<string>('NeurIPS');

  useEffect(() => {
    fetchFilesList();
  }, []);

  const fetchFilesList = async () => {
    setIsLoadingList(true);
    try {
      const res = await apiFetch('/api/vault/files');
      if (res.ok) {
        const data = await res.json();
        setFiles(data);
        
        // Auto-select the first draft file if available, or first debate
        if (data.drafts && data.drafts.length > 0) {
          loadFile('drafts', data.drafts[0].filename);
        } else if (data.debates && data.debates.length > 0) {
          loadFile('debates', data.debates[0].filename);
        }
      } else {
        setFiles(null);
      }
    } catch (e) {
      console.error('Failed to fetch files list:', e);
      setFiles(null);
    } finally {
      setIsLoadingList(false);
    }
  };

  const loadFile = async (category: string, filename: string) => {
    setIsLoadingFile(true);
    setSaveStatus('idle');
    try {
      const res = await apiFetch(`/api/vault/read?category=${category}&filename=${filename}`);
      if (res.ok) {
        const data = await res.json();
        setContent(data.content);
        setFrontmatter(data.frontmatter || {});
        setActiveCategory(category);
        setActiveFilename(filename);
      }
    } catch (e) {
      console.error('Failed to load file:', e);
    } finally {
      setIsLoadingFile(false);
    }
  };

  const handleSave = async () => {
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
          frontmatter: frontmatter
        })
      });
      
      if (res.ok) {
        setSaveStatus('saved');
        setTimeout(() => setSaveStatus('idle'), 2000);
        // Refresh previews in sidebar
        fetchFilesList();
      } else {
        setSaveStatus('error');
      }
    } catch (e) {
      setSaveStatus('error');
      console.error('Error saving file:', e);
    }
  };

  // Simple Markdown Parser for Preview Pane
  const renderMarkdown = (mdText: string) => {
    let html = mdText;
    
    // Escape HTML tags to prevent XSS
    html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    
    // Headers
    html = html.replace(/^# (.*?)$/gm, '<h1 style="font-family: var(--font-heading); font-size: 22px; font-weight: 800; margin: 18px 0 10px 0; border-bottom: 1px solid var(--border-color); padding-bottom: 6px;">$1</h1>');
    html = html.replace(/^## (.*?)$/gm, '<h2 style="font-family: var(--font-heading); font-size: 18px; font-weight: 700; margin: 16px 0 8px 0;">$1</h2>');
    html = html.replace(/^### (.*?)$/gm, '<h3 style="font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 12px 0 6px 0;">$1</h3>');
    
    // Bold & Italics
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // WikiLinks: [[LinkName]] -> styled span
    html = html.replace(/\[\[(.*?)\]\]/g, '<span style="color: var(--primary); text-decoration: underline; cursor: pointer; font-weight: 500;">$1</span>');
    
    // Bullet Lists
    html = html.replace(/^- (.*?)$/gm, '<li style="margin-left: 20px; list-style-type: square; margin-bottom: 4px;">$1</li>');
    
    // Line breaks
    html = html.replace(/\n/g, '<br />');

    return <div dangerouslySetInnerHTML={{ __html: html }} style={{ fontSize: '13px', lineHeight: '1.6' }} />;
  };

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
              {files.drafts.length > 0 && (
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
              {files.debates.length > 0 && (
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
              {files.papers.length > 0 && (
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
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', marginBottom: '16px' }}>
              <div>
                <span style={{ fontSize: '10px', color: 'var(--primary)', fontWeight: '700', textTransform: 'uppercase' }}>
                  {activeCategory} / {activeFilename}
                </span>
                <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '18px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span>{frontmatter.title || activeFilename.replace('.md', '')}</span>
                  {frontmatter.full_pdf_ingested && (
                    <span style={{ fontSize: '10px', background: 'rgba(16,185,129,0.15)', color: '#10b981', border: '1px solid rgba(16,185,129,0.3)', padding: '2px 8px', borderRadius: '12px', fontWeight: '600' }}>
                      Full PDF Ingested
                    </span>
                  )}
                  {frontmatter.fact_check_score !== undefined && (
                    <span style={{ fontSize: '10px', background: frontmatter.fact_check_score >= 80 ? 'rgba(16,185,129,0.15)' : 'rgba(244,63,94,0.15)', color: frontmatter.fact_check_score >= 80 ? '#10b981' : '#f43f5e', border: '1px solid var(--border-color)', padding: '2px 8px', borderRadius: '12px', fontWeight: '700' }}>
                      Fact-Check Score: {frontmatter.fact_check_score}%
                    </span>
                  )}
                </h3>
              </div>
              
              <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
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
                    <span>Markdown Source</span>
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
                    <span>Formatted Preview</span>
                  </button>
                </div>

                {/* Multi-Venue Format & LaTeX Exporter Controls */}
                {activeCategory === 'drafts' && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <select
                      value={selectedVenue}
                      onChange={(e) => setSelectedVenue(e.target.value)}
                      style={{
                        background: 'rgba(15,23,42,0.8)',
                        color: '#93c5fd',
                        border: '1px solid rgba(59,130,246,0.3)',
                        borderRadius: '6px',
                        padding: '5px 8px',
                        fontSize: '11px',
                        fontWeight: '600',
                        outline: 'none',
                        cursor: 'pointer'
                      }}
                    >
                      <option value="NeurIPS">NeurIPS (9-Page Single-Col)</option>
                      <option value="ICML">ICML (8-Page Two-Col)</option>
                      <option value="CVPR">CVPR (8-Page Two-Col)</option>
                      <option value="ACL">ACL / ARR (8-Page Two-Col)</option>
                      <option value="IEEEtran">IEEEtran (10-25 Page Journal)</option>
                      <option value="ACM">ACM (CSUR / SIGKDD)</option>
                      <option value="ALL">📦 Export All Venues (Multi-Path)</option>
                    </select>

                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        try {
                          const res = await apiFetch(`/api/vault/export-venue-latex?filename=${activeFilename}&venue=${selectedVenue}`);
                          if (res.ok) {
                            const data = await res.json();
                            if (selectedVenue === 'ALL' && data.bundle) {
                              Object.entries(data.bundle).forEach(([vKey, code]) => {
                                const blob = new Blob([code as string], { type: 'text/x-tex' });
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = `${activeFilename.replace('.md', '')}_${vKey}.tex`;
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                              });
                            } else if (data.tex_code) {
                              const blob = new Blob([data.tex_code], { type: 'text/x-tex' });
                              const url = URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = url;
                              a.download = data.tex_filename || `${activeFilename.replace('.md', '')}_${selectedVenue}.tex`;
                              document.body.appendChild(a);
                              a.click();
                              document.body.removeChild(a);
                              URL.revokeObjectURL(url);
                            }

                            if (data.bib_code) {
                              const bibBlob = new Blob([data.bib_code], { type: 'text/plain' });
                              const bibUrl = URL.createObjectURL(bibBlob);
                              const bibA = document.createElement('a');
                              bibA.href = bibUrl;
                              bibA.download = 'references.bib';
                              document.body.appendChild(bibA);
                              bibA.click();
                              document.body.removeChild(bibA);
                              URL.revokeObjectURL(bibUrl);
                            }
                          } else {
                            alert(`Export failed with status: ${res.status}`);
                          }
                        } catch (e) {
                          console.error('Failed to export venue LaTeX:', e);
                          alert('Failed to export LaTeX. Check browser console.');
                        }
                      }}
                      style={{
                        background: 'rgba(59,130,246,0.15)',
                        color: '#93c5fd',
                        border: '1px solid rgba(59,130,246,0.4)',
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
                      <FileText size={14} />
                      <span>Export {selectedVenue === 'ALL' ? 'Multi-Path Bundle' : selectedVenue + ' LaTeX'}</span>
                    </button>

                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        try {
                          const res = await apiFetch(`/api/vault/export-venue-latex?filename=${activeFilename}&venue=${selectedVenue}`);
                          if (res.ok) {
                            const data = await res.json();
                            const codeToCopy = data.tex_code || (data.bundle ? data.bundle[selectedVenue] || Object.values(data.bundle)[0] : '');
                            await navigator.clipboard.writeText(codeToCopy as string);
                            alert(`Copied ${selectedVenue} LaTeX code to clipboard! You can paste directly into Overleaf.`);
                          }
                        } catch (e) {
                          console.error('Failed to copy LaTeX:', e);
                        }
                      }}
                      style={{
                        background: 'rgba(168,85,247,0.15)',
                        color: '#c084fc',
                        border: '1px solid rgba(168,85,247,0.4)',
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
                      <Save size={14} />
                      <span>Copy LaTeX</span>
                    </button>

                    <button
                      onClick={async () => {
                        if (!activeFilename) return;
                        try {
                          const venue = selectedVenue === 'ALL' ? 'IEEEtran' : selectedVenue;
                          const pdfUrl = `http://127.0.0.1:8000/api/vault/export-venue-pdf?filename=${activeFilename}&venue=${venue}`;
                          const a = document.createElement('a');
                          a.href = pdfUrl;
                          a.download = `${activeFilename.replace('.md', '')}_${venue}.pdf`;
                          document.body.appendChild(a);
                          a.click();
                          document.body.removeChild(a);
                        } catch (e) {
                          console.error('Failed to download PDF:', e);
                          alert('Failed to trigger PDF download.');
                        }
                      }}
                      style={{
                        background: 'rgba(239,68,68,0.15)',
                        color: '#f87171',
                        border: '1px solid rgba(239,68,68,0.4)',
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
                      <Download size={14} />
                      <span>Download PDF</span>
                    </button>
                  </div>
                )}

                {/* Save Action */}
                <button
                  onClick={handleSave}
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
              </div>
            </div>

            {/* Split layout: Editor Text vs Preview/Frontmatter */}
            <div className={editMode === 'edit' ? "responsive-doc-split" : ""} style={{ gap: '16px', overflow: 'hidden', height: '100%', minHeight: '0' }}>
              
              {/* Primary Content Editor / Preview Pane */}
              <div style={{ height: '100%', minHeight: '0', overflow: 'hidden' }}>
                {editMode === 'edit' ? (
                  <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    style={{
                      width: '100%', height: '100%', background: 'rgba(0,0,0,0.15)', color: 'var(--text-primary)', border: '1px solid var(--border-color)',
                      borderRadius: '8px', padding: '16px', fontFamily: 'var(--font-mono)', fontSize: '13px', resize: 'none', outline: 'none', lineHeight: '1.6'
                    }}
                  />
                ) : (
                  <div style={{ height: '100%', overflowY: 'auto', background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '24px' }}>
                    {renderMarkdown(content)}
                  </div>
                )}
              </div>

              {/* Right Side Panel: YAML Frontmatter properties editor */}
              {editMode === 'edit' && (
                <div style={{ borderLeft: '1px solid var(--border-color)', paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto' }}>
                  <h4 style={{ fontFamily: 'var(--font-heading)', fontSize: '13px', fontWeight: '700', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
                    Metadata properties (YAML)
                  </h4>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {Object.entries(frontmatter).map(([key, val]) => {
                      if (key === 'tags') return null; // Handle tags separately
                      return (
                        <div key={key} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                          <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{key}</span>
                          <input
                            type="text"
                            value={String(val)}
                            onChange={(e) => setFrontmatter((prev: any) => ({ ...prev, [key]: e.target.value }))}
                            style={{
                              background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', fontSize: '12px', padding: '6px 8px', outline: 'none'
                            }}
                          />
                        </div>
                      );
                    })}

                    {/* Simple frontmatter tag creator */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Tags (comma separated)</span>
                      <input
                        type="text"
                        value={Array.isArray(frontmatter.tags) ? frontmatter.tags.join(', ') : ''}
                        onChange={(e) => {
                          const tagList = e.target.value.split(',').map(t => t.trim()).filter(Boolean);
                          setFrontmatter((prev: any) => ({ ...prev, tags: tagList }));
                        }}
                        style={{
                          background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', fontSize: '12px', padding: '6px 8px', outline: 'none'
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
      
    </div>
  );
};

export default DocEditor;
