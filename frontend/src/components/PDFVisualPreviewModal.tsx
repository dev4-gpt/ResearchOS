import React, { useState, useEffect } from 'react';
import { X, CheckCircle2, AlertTriangle, RefreshCw, Layers, ShieldCheck, Download } from 'lucide-react';
import { apiFetch } from '../api';

interface PDFVisualPreviewModalProps {
  filename: string | null;
  venue: string;
  onClose: () => void;
}


export const PDFVisualPreviewModal: React.FC<PDFVisualPreviewModalProps> = ({ filename, venue, onClose }) => {
  const [selectedVenue, setSelectedVenue] = useState(venue || 'IEEEtran');
  const [venues, setVenues] = useState<string[]>([venue || 'IEEEtran']);
  const [loading, setLoading] = useState(true);
  const [remediating, setRemediating] = useState(false);
  const [auditData, setAuditData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [failedPages, setFailedPages] = useState<Set<number>>(new Set());

  const cleanFilename = filename ? (filename.endsWith('.md') ? filename : `${filename}.md`) : '';

  const fetchPreviewTiles = async (v: string) => {
    if (!cleanFilename) return;
    setLoading(true);
    setError(null);
    setFailedPages(new Set());
    try {
      const res = await apiFetch(`/api/vault/backtest/preview-tiles?filename=${encodeURIComponent(cleanFilename)}&venue=${encodeURIComponent(v)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch preview tiles`);
      const data = await res.json();
      if (data.success && data.audit) {
        setAuditData(data.audit);
      } else {
        throw new Error('Invalid preview data returned');
      }
    } catch (err: any) {
      setError(err.message || 'Error loading visual preview');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    apiFetch('/api/venues')
      .then((res) => res.ok ? res.json() : null)
      .then((data) => {
        const nextVenues = Array.isArray(data?.venue_order)
          ? data.venue_order
          : Object.keys(data?.release_profiles || data?.venues || {});
        if (nextVenues.length) setVenues(nextVenues);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (cleanFilename) {
      fetchPreviewTiles(selectedVenue);
    }
  }, [cleanFilename, selectedVenue]);

  const handleAutoRemediate = async () => {
    if (!cleanFilename) return;
    setRemediating(true);
    try {
      const res = await apiFetch(`/api/vault/backtest/auto-remediate?filename=${encodeURIComponent(cleanFilename)}&venue=${encodeURIComponent(selectedVenue)}`, {
        method: 'POST'
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}: Auto-remediation failed`);
      await fetchPreviewTiles(selectedVenue);
    } catch (err: any) {
      alert(`Auto-remediation error: ${err.message}`);
    } finally {
      setRemediating(false);
    }
  };

  if (!cleanFilename) return null;

  const score = auditData?.score || 100.0;
  const checkmatePassed = auditData?.checkmate_passed ?? true;
  const checks = auditData?.checkmate_checks || {};
  const cleanName = cleanFilename.replace('.md', '');
  const pageTiles = auditData?.page_tiles || [];
  const tileUrl = (page: number) =>
    `/api/vault/backtest/preview-tile-image/${encodeURIComponent(cleanName)}/${encodeURIComponent(selectedVenue)}/${page}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="relative w-full max-w-6xl h-[90vh] bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden text-slate-100">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight text-white flex items-center gap-2">
                In-Browser Visual Page Preview
                <span className={`px-2 py-0.5 text-xs font-mono rounded-full border ${checkmatePassed ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}`}>
                  {checkmatePassed ? 'Score: 100.0/100 (PASSED)' : `Score: ${score}/100 (REMEDIATION NEEDED)`}
                </span>
              </h2>
              <p className="text-xs text-slate-400 font-mono mt-0.5">{cleanFilename}</p>
            </div>
          </div>

          {/* Venue Selector & Close */}
          <div className="flex items-center gap-3">
            <div className="flex items-center bg-slate-900 p-1 rounded-xl border border-slate-800">
              {venues.map((v) => (
                <button
                  key={v}
                  onClick={() => setSelectedVenue(v)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${selectedVenue === v ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-slate-400 hover:text-slate-200'}`}
                >
                  {v}
                </button>
              ))}
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 flex overflow-hidden">

          {/* Left Pane: Page Image Viewer */}
          <div className="flex-1 flex flex-col bg-slate-900/30 p-6 relative overflow-y-auto items-center">
            {loading ? (
              <div className="flex flex-col items-center gap-3 text-slate-400 font-mono text-sm">
                <RefreshCw className="w-8 h-8 animate-spin text-blue-400" />
                <span>Compiling LaTeX & Rendering PNG Preview Tiles...</span>
              </div>
            ) : error ? (
              <div className="flex flex-col items-center gap-3 text-rose-400 text-sm font-mono max-w-md text-center">
                <AlertTriangle className="w-8 h-8" />
                <span>{error}</span>
              </div>
            ) : (
              <div className="w-full max-w-4xl space-y-5">
                <div className="sticky top-0 z-10 flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/95 px-4 py-2 text-xs font-mono text-slate-300 shadow-xl backdrop-blur">
                  <span>Continuous document preview</span>
                  <span className="text-slate-500">{pageTiles.length} pages · scroll to read</span>
                </div>
                {pageTiles.map((tile: any) => (
                  <figure key={tile.page} className="overflow-hidden rounded-xl border border-slate-800 bg-white shadow-2xl">
                    {failedPages.has(tile.page) ? (
                      <div className="flex min-h-32 items-center justify-center bg-slate-900 px-6 text-center text-xs font-mono text-rose-300">
                        Page {tile.page} preview is unavailable. Re-run the visual audit to regenerate it.
                      </div>
                    ) : (
                      <img
                        src={tileUrl(tile.page)}
                        alt={`Rendered page ${tile.page}`}
                        loading="lazy"
                        className="block h-auto w-full object-contain"
                        onError={() => setFailedPages((pages) => new Set(pages).add(tile.page))}
                      />
                    )}
                    <figcaption className="border-t border-slate-200 bg-slate-100 px-3 py-1 text-center text-[11px] font-mono text-slate-600">
                      Page {tile.page}
                    </figcaption>
                  </figure>
                ))}
              </div>
            )}
          </div>

          {/* Right Pane: Checkmate Audit Scorecard */}
          <div className="w-96 border-l border-slate-800 bg-slate-950 p-6 flex flex-col justify-between overflow-y-auto">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <h3 className="text-sm font-semibold text-white tracking-tight uppercase font-mono">
                  Checkmate Audit Scorecard
                </h3>
              </div>

              {/* Score Indicator */}
              <div className="mb-6 p-4 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="flex justify-between items-baseline mb-2">
                  <span className="text-xs text-slate-400 font-mono">Audit Decision</span>
                  <span className={`text-sm font-bold font-mono ${checkmatePassed ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {checkmatePassed ? 'VERIFIED SEAL' : 'NEEDS REMEDIATION'}
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-500 ${checkmatePassed ? 'bg-emerald-500' : 'bg-amber-500'}`}
                    style={{ width: `${score}%` }}
                  />
                </div>
              </div>

              {/* 7-Point Audit Checklist */}
              <div className="space-y-3">
                {Object.entries(checks).map(([key, item]: [string, any]) => (
                  <div key={key} className="flex items-start gap-3 p-2.5 rounded-lg bg-slate-900/40 border border-slate-800/50">
                    {item.passed ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <div className="text-xs font-medium text-slate-200 font-mono uppercase tracking-wider">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-[11px] text-slate-400 mt-0.5">
                        {item.detail || (item.passed ? 'Verified Zero Defects' : 'Remediation Required')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bottom Actions */}
            <div className="pt-6 border-t border-slate-800 space-y-3">
              {!checkmatePassed && (
                <button
                  disabled={remediating}
                  onClick={handleAutoRemediate}
                  className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-medium text-xs font-mono shadow-lg transition-all disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${remediating ? 'animate-spin' : ''}`} />
                  {remediating ? 'Running Self-Healing Loop...' : 'Run Self-Healing Repair'}
                </button>
              )}

              <a
                href={`/api/vault/export-venue-pdf?filename=${encodeURIComponent(cleanFilename)}&venue=${encodeURIComponent(selectedVenue)}`}
                target="_blank"
                rel="noreferrer"
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs font-mono shadow-lg transition-all"
              >
                <Download className="w-4 h-4" />
                Download Verified PDF
              </a>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
};
