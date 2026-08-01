import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, Maximize2, RotateCcw, Monitor, FileText, Users, Eye, Sliders } from 'lucide-react';

interface Laptop3DWorkspaceProps {
  onEnterWorkspace: () => void;
}

export const Laptop3DWorkspace: React.FC<Laptop3DWorkspaceProps> = ({ onEnterWorkspace }) => {
  // Start with lid open (75 degrees) so screen is vibrant and visible immediately!
  const [manualLidAngle, setManualLidAngle] = useState(75);
  const [manualZoom, setManualZoom] = useState(1.0);
  const [scrollProgress, setScrollProgress] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Listen for scroll events on nearest scrolling parent (<main>) AND window
    const scrollParent = containerRef.current?.closest('main') || window;

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
    handleScroll(); // Initial call

    return () => scrollParent.removeEventListener('scroll', handleScroll);
  }, []);

  // Compute active lid angle (combining manual controls + scroll progress)
  const activeLidAngle = Math.min(90, Math.max(0, manualLidAngle + scrollProgress * 15));
  const activeZoom = Math.min(2.5, Math.max(0.7, manualZoom + scrollProgress * 0.8));

  // Tilt angle flattens as zoom increases
  const tiltX = Math.max(0, 18 - scrollProgress * 18);
  const tiltY = Math.max(-10, -8 + scrollProgress * 8);

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
        justifyContent: 'center',
        perspective: '1200px',
        overflow: 'visible',
        padding: '30px 0',
        userSelect: 'none'
      }}
    >
      {/* Interactive Controls Bar */}
      <div 
        style={{
          width: '90%',
          maxWidth: '680px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '10px 16px',
          borderRadius: '12px',
          background: 'rgba(15, 23, 42, 0.85)',
          border: '1px solid var(--border-color)',
          backdropFilter: 'blur(16px)',
          marginBottom: '20px',
          zIndex: 30,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)', fontSize: '12px', fontWeight: '700' }}>
          <Sparkles size={15} />
          <span>3D LAPTOP WORKSPACE</span>
        </div>

        {/* Sliders for Lid Angle & Zoom */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
            <span>Lid:</span>
            <input 
              type="range" 
              min="0" 
              max="90" 
              value={manualLidAngle}
              onChange={(e) => setManualLidAngle(Number(e.target.value))}
              style={{ width: '80px', accentColor: 'var(--primary)', cursor: 'pointer' }}
            />
            <span style={{ fontFamily: 'monospace', width: '24px' }}>{Math.round(activeLidAngle)}°</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
            <span>Zoom:</span>
            <input 
              type="range" 
              min="0.7" 
              max="2.2" 
              step="0.05"
              value={manualZoom}
              onChange={(e) => setManualZoom(Number(e.target.value))}
              style={{ width: '80px', accentColor: 'var(--primary)', cursor: 'pointer' }}
            />
            <span style={{ fontFamily: 'monospace', width: '32px' }}>{activeZoom.toFixed(1)}x</span>
          </div>
        </div>

        {/* Enter Full HITL Publisher Button */}
        <button
          onClick={onEnterWorkspace}
          style={{
            padding: '6px 14px',
            fontSize: '12px',
            borderRadius: '6px',
            background: 'var(--primary)',
            color: '#000',
            fontWeight: 'bold',
            border: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            cursor: 'pointer',
            boxShadow: '0 0 15px rgba(59, 130, 246, 0.4)'
          }}
        >
          <Monitor size={13} />
          <span>Enter Workspace</span>
        </button>
      </div>

      {/* 3D LAPTOP CHASSIS CONTAINER */}
      <div
        style={{
          width: '680px',
          height: '420px',
          position: 'relative',
          transformStyle: 'preserve-3d',
          transform: `scale(${activeZoom}) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`,
          transition: 'transform 0.2s cubic-bezier(0.16, 1, 0.3, 1)',
          zIndex: 10
        }}
      >
        {/* LAPTOP DISPLAY LID (TOP SCREEN) */}
        <div
          style={{
            width: '680px',
            height: '420px',
            position: 'absolute',
            top: 0,
            left: 0,
            borderRadius: '16px 16px 4px 4px',
            background: 'linear-gradient(145deg, #1e293b, #0f172a)',
            border: '2px solid rgba(59, 130, 246, 0.4)',
            transformOrigin: 'bottom center',
            transformStyle: 'preserve-3d',
            transform: `rotateX(-${activeLidAngle}deg)`,
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(59, 130, 246, 0.2)',
            transition: 'transform 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
          }}
        >
          {/* INNER DISPLAY GLASS SCREEN */}
          <div
            style={{
              position: 'absolute',
              inset: '8px',
              borderRadius: '10px',
              background: '#040711',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: 'inset 0 0 40px rgba(0,0,0,0.9)'
            }}
          >
            {/* Screen Notch / Camera Bar */}
            <div style={{
              height: '24px',
              background: '#090d16',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0 16px',
              borderBottom: '1px solid rgba(255,255,255,0.08)'
            }}>
              <div style={{ display: 'flex', gap: '6px' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#ef4444' }}></span>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#f59e0b' }}></span>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981' }}></span>
              </div>
              <div style={{ fontSize: '10px', color: '#3b82f6', fontWeight: 'bold', letterSpacing: '0.5px' }}>ResearchingOS Workspace</div>
              <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }}></div>
            </div>

            {/* VIBRANT DISPLAY INTERFACE */}
            <div 
              style={{ 
                flex: 1, 
                padding: '16px', 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '12px',
                background: 'radial-gradient(circle at top right, rgba(30, 41, 59, 0.6), #040711)',
                opacity: activeLidAngle > 10 ? 1 : 0.2,
                transition: 'opacity 0.2s ease'
              }}
            >
              {/* Screen Top Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontSize: '10px', color: '#818cf8', fontWeight: 'bold', textTransform: 'uppercase' }}>Active Manuscript</span>
                  <h4 style={{ fontSize: '14px', fontWeight: '800', color: '#fff', margin: 0 }}>Systematic Review & Meta-Taxonomy of Generative AI</h4>
                </div>
                <span style={{ fontSize: '10px', background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.4)', padding: '2px 8px', borderRadius: '12px', fontWeight: 'bold' }}>
                  Fact-Check Score: 88.5%
                </span>
              </div>

              {/* Screen Split Content Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', flex: 1 }}>
                <div style={{ background: 'rgba(255, 255, 255, 0.04)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '10px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#3b82f6', fontSize: '11px', fontWeight: 'bold' }}>
                    <FileText size={12} />
                    <span>53 Ingested Vault Papers</span>
                  </div>
                  <p style={{ fontSize: '10px', color: 'var(--text-secondary)', lineHeight: '1.4', margin: 0 }}>
                    Extracted empirical productivity metrics, N=5,179 RCTs, and TRiSM security frameworks.
                  </p>
                </div>

                <div style={{ background: 'rgba(255, 255, 255, 0.04)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '8px', padding: '10px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#8b5cf6', fontSize: '11px', fontWeight: 'bold' }}>
                    <Users size={12} />
                    <span>7-Agent Council Consensus</span>
                  </div>
                  <p style={{ fontSize: '10px', color: 'var(--text-secondary)', lineHeight: '1.4', margin: 0 }}>
                    Senior Systems Engineer, Statistician, and Reviewer #2 consensus synthesis.
                  </p>
                </div>
              </div>

              {/* Bottom Callout Bar */}
              <div style={{ background: 'rgba(59, 130, 246, 0.12)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '6px', padding: '8px 12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '11px', color: '#93c5fd', fontWeight: '500' }}>Click to launch workspace & edit manuscript draft</span>
                <button 
                  onClick={onEnterWorkspace}
                  style={{ background: '#3b82f6', color: '#000', border: 'none', borderRadius: '4px', padding: '5px 12px', fontSize: '10px', fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 0 10px rgba(59, 130, 246, 0.5)' }}
                >
                  Launch Workspace →
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* LAPTOP KEYBOARD BASE DECK */}
        <div
          style={{
            width: '700px',
            height: '380px',
            position: 'absolute',
            top: '415px',
            left: '-10px',
            borderRadius: '4px 4px 20px 20px',
            background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 70%, #020617 100%)',
            border: '2px solid rgba(255, 255, 255, 0.15)',
            transformStyle: 'preserve-3d',
            transform: 'rotateX(90deg)',
            transformOrigin: 'top center',
            boxShadow: '0 30px 60px rgba(0,0,0,0.8), 0 0 40px rgba(59, 130, 246, 0.15)'
          }}
        >
          {/* Keyboard Recessed Well */}
          <div style={{
            margin: '20px auto 14px auto',
            width: '600px',
            height: '210px',
            background: '#090d16',
            borderRadius: '8px',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '10px',
            display: 'flex',
            flexDirection: 'column',
            gap: '5px',
            boxShadow: 'inset 0 4px 10px rgba(0,0,0,0.8)'
          }}>
            {/* Key Rows Simulation */}
            {[1, 2, 3, 4, 5].map((row) => (
              <div key={row} style={{ display: 'flex', gap: '4px', height: row === 5 ? '32px' : '28px' }}>
                {Array.from({ length: row === 5 ? 8 : 14 }).map((_, i) => (
                  <div
                    key={i}
                    style={{
                      flex: row === 5 && i === 3 ? 4 : 1,
                      background: 'linear-gradient(180deg, #1e293b, #0f172a)',
                      borderRadius: '3px',
                      border: '1px solid rgba(59, 130, 246, 0.2)',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.4)'
                    }}
                  />
                ))}
              </div>
            ))}
          </div>

          {/* Trackpad */}
          <div style={{
            margin: '0 auto',
            width: '200px',
            height: '100px',
            background: 'rgba(255, 255, 255, 0.03)',
            borderRadius: '8px',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            boxShadow: 'inset 0 0 10px rgba(0,0,0,0.5)'
          }} />
        </div>

        {/* Ambient Glow Shadow */}
        <div style={{
          position: 'absolute',
          top: '480px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: '640px',
          height: '80px',
          borderRadius: '50%',
          background: 'radial-gradient(ellipse at center, rgba(59, 130, 246, 0.3) 0%, rgba(0,0,0,0.8) 50%, transparent 80%)',
          filter: 'blur(20px)',
          pointerEvents: 'none'
        }} />
      </div>
    </div>
  );
};

export default Laptop3DWorkspace;
