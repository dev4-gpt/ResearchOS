import React, { useState, useEffect, useRef } from 'react';
import { Layers, Cpu, ShieldCheck, FileCheck, ArrowRight, ChevronRight, Activity } from 'lucide-react';

interface Laptop3DWorkspaceProps {
  onEnterWorkspace: () => void;
}

export const Laptop3DWorkspace: React.FC<Laptop3DWorkspaceProps> = ({ onEnterWorkspace }) => {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [activeStage, setActiveStage] = useState<'all' | 'ingest' | 'council' | 'publisher'>('all');
  const [spatialTilt, setSpatialTilt] = useState(10);
  const zoomLevel = 1.0;
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const scrollParent = containerRef.current?.closest('.smooth-scroll-container') || containerRef.current?.closest('main') || window;

    const handleScroll = () => {
      let scrollY = 0;
      let maxScroll = 600;

      if (scrollParent === window) {
        scrollY = window.scrollY;
      } else if (scrollParent instanceof HTMLElement) {
        scrollY = scrollParent.scrollTop;
      }

      const progress = Math.min(1, Math.max(0, scrollY / maxScroll));
      setScrollProgress(progress);
    };

    scrollParent.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    return () => scrollParent.removeEventListener('scroll', handleScroll);
  }, []);

  // Compute dynamic 3D perspective shifts based on scroll & slider state
  const computedRotateX = Math.max(0, spatialTilt - scrollProgress * 8);
  const computedRotateY = Math.max(-4, -3 + scrollProgress * 3);
  const computedScale = Math.min(1.12, Math.max(0.92, zoomLevel + scrollProgress * 0.08));

  return (
    <div
      ref={containerRef}
      style={{
        position: 'relative',
        width: '100%',
        minHeight: '620px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
        padding: '0',
        background: '#0b0c10',
        borderRadius: '12px',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 12px 36px rgba(0, 0, 0, 0.45)',
        overflow: 'hidden'
      }}
    >
      {/* Faux-OS macOS Window Chrome Top Bar */}
      <div className="faux-mac-bar" style={{ width: '100%', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="mac-dot mac-dot-red" />
          <span className="mac-dot mac-dot-yellow" />
          <span className="mac-dot mac-dot-green" />
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', marginLeft: '8px' }}>
            ResearchingOS Studio — Spatial Deck
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <kbd className="kbd-shortcut">⌘K</kbd>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Workspace</span>
        </div>
      </div>

      {/* Internal Studio Workspace Area */}
      <div style={{ width: '100%', padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {/* Minimalist Top Studio Toolbar */}
        <div
          style={{
            width: '100%',
            maxWidth: '880px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '12px',
            padding: '10px 16px',
            borderRadius: '8px',
            background: 'rgba(18, 20, 28, 0.85)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            marginBottom: '20px',
            zIndex: 20
          }}
        >
          {/* Title Tag */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="minimalist-badge-amber">Spatial Deck</span>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontFamily: 'var(--font-heading)', fontWeight: '600' }}>
              Multi-Agent Executive Control
            </span>
          </div>

          {/* Stage Filter Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            {[
              { id: 'all', label: 'Overview' },
              { id: 'ingest', label: 'Ingestion' },
              { id: 'council', label: 'Council' },
              { id: 'publisher', label: 'Publisher' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveStage(tab.id as any)}
                style={{
                  padding: '4px 10px',
                  fontSize: '11px',
                  fontWeight: '600',
                  borderRadius: '6px',
                  fontFamily: 'var(--font-heading)',
                  border: activeStage === tab.id ? '1px solid rgba(255, 255, 255, 0.16)' : '1px solid transparent',
                  background: activeStage === tab.id ? 'rgba(255, 255, 255, 0.08)' : 'transparent',
                  color: activeStage === tab.id ? '#ffffff' : 'var(--text-muted)',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Controls & CTA */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-muted)' }}>
              <span>Tilt:</span>
              <input
                type="range"
                min="0"
                max="20"
                value={spatialTilt}
                onChange={(e) => setSpatialTilt(Number(e.target.value))}
                style={{ width: '60px', accentColor: '#f59e0b', cursor: 'pointer' }}
              />
              <span style={{ fontFamily: 'var(--font-mono)', width: '20px' }}>{Math.round(computedRotateX)}°</span>
            </div>

            <button
              onClick={onEnterWorkspace}
              style={{
                padding: '6px 14px',
                fontSize: '11px',
                fontWeight: '700',
                borderRadius: '6px',
                background: '#111111',
                color: '#ffffff',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                fontFamily: 'var(--font-heading)'
              }}
            >
              <span>Enter Studio</span>
              <ChevronRight size={13} />
            </button>
          </div>
        </div>

        {/* 3D SPATIAL STUDIO DECK STAGE */}
        <div
          className="spatial-canvas-viewport"
          style={{
            width: '100%',
            maxWidth: '880px',
            transform: `scale(${computedScale}) rotateX(${computedRotateX}deg) rotateY(${computedRotateY}deg)`,
            transition: 'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
            zIndex: 10
          }}
        >
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '14px',
              position: 'relative'
            }}
          >
            {/* Bento Card 1: Ingestion & Paper Corpus */}
            {(activeStage === 'all' || activeStage === 'ingest') && (
              <div className="minimalist-card">
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between', gap: '12px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-primary)', fontWeight: '700', fontSize: '13px' }}>
                        <Cpu size={15} color="#86efac" />
                        <span>Ingestion Pipeline</span>
                      </div>
                      <span className="minimalist-badge-green">25 Notes</span>
                    </div>
                    <h4 style={{ fontSize: '14px', fontWeight: '700', color: '#ffffff', marginBottom: '6px', fontFamily: 'var(--font-heading)' }}>
                      Scout & Analyst Ingestion
                    </h4>
                    <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                      Reciprocal Rank Fusion scoring across 12 primary scientific repositories with frontmatter metadata.
                    </p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-muted)', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px' }}>
                    <Activity size={12} color="#86efac" />
                    <span>Full PDF Ingestion Verified</span>
                  </div>
                </div>
              </div>
            )}

            {/* Bento Card 2: 7-Agent Council Boardroom */}
            {(activeStage === 'all' || activeStage === 'council') && (
              <div className="minimalist-card">
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between', gap: '12px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-primary)', fontWeight: '700', fontSize: '13px' }}>
                        <Layers size={15} color="#93c5fd" />
                        <span>7-Agent Council</span>
                      </div>
                      <span className="minimalist-badge-blue">Strong Accept</span>
                    </div>
                    <h4 style={{ fontSize: '14px', fontWeight: '700', color: '#ffffff', marginBottom: '6px', fontFamily: 'var(--font-heading)' }}>
                      Boardroom Synthesis
                    </h4>
                    <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                      Systems Engineer, Statistician, Reviewer #2, and Chairman evaluate proofs and control baselines.
                    </p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-muted)', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px' }}>
                    <ShieldCheck size={12} color="#93c5fd" />
                    <span>Hostile Peer Review Complete</span>
                  </div>
                </div>
              </div>
            )}

            {/* Bento Card 3: 5 Fail-Closed Release Gates */}
            {(activeStage === 'all' || activeStage === 'publisher') && (
              <div className="minimalist-card">
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between', gap: '12px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-primary)', fontWeight: '700', fontSize: '13px' }}>
                        <FileCheck size={15} color="#fde047" />
                        <span>Release Matrix</span>
                      </div>
                      <span className="minimalist-badge-amber">40 Venues Ready</span>
                    </div>
                    <h4 style={{ fontSize: '14px', fontWeight: '700', color: '#ffffff', marginBottom: '6px', fontFamily: 'var(--font-heading)' }}>
                      5 Fail-Closed Gates
                    </h4>
                    <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.55' }}>
                      Collection Originality (0.0% overlap), Substantive Value (100.0 score), Checkmate visual layout.
                    </p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-muted)', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px' }}>
                    <ShieldCheck size={12} color="#fde047" />
                    <span>IEEEtran, NeurIPS, CVPR, ACM Ready</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Minimalist Studio Action Footer Bar */}
          <div
            style={{
              marginTop: '16px',
              padding: '12px 18px',
              borderRadius: '8px',
              background: 'rgba(18, 20, 28, 0.85)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '16px'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#86efac' }} />
              <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '500' }}>
                Full 4-layer connectivity active
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <kbd className="kbd-shortcut">↵ Enter</kbd>
              <button
                onClick={onEnterWorkspace}
                style={{
                  padding: '7px 16px',
                  fontSize: '12px',
                  borderRadius: '6px',
                  background: '#ffffff',
                  color: '#0b0c10',
                  fontWeight: '700',
                  border: 'none',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  cursor: 'pointer',
                  fontFamily: 'var(--font-heading)'
                }}
              >
                <span>Launch Publisher Studio</span>
                <ArrowRight size={13} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Laptop3DWorkspace;
