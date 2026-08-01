import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, Maximize2, RotateCcw, Monitor, FileText, Network, Users } from 'lucide-react';

interface Laptop3DWorkspaceProps {
  onEnterWorkspace: () => void;
}

export const Laptop3DWorkspace: React.FC<Laptop3DWorkspaceProps> = ({ onEnterWorkspace }) => {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [isHovered, setIsHovered] = useState(false);
  const [isDocked, setIsDocked] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Monitor Y scroll within container to drive 3D transforms smoothly
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      // Calculate progress between 0 and 1 over first 800px
      const progress = Math.min(1, Math.max(0, scrollY / 600));
      setScrollProgress(progress);

      if (progress >= 0.95 && !isDocked) {
        setIsDocked(true);
      } else if (progress < 0.95 && isDocked) {
        setIsDocked(false);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isDocked]);

  // Derived 3D transform values based on scroll progress
  // 1. Lid opening angle: 0deg when closed, opens to 88deg as scrollProgress moves from 0.1 to 0.6
  const lidProgress = Math.min(1, Math.max(0, (scrollProgress - 0.05) / 0.5));
  const lidAngle = lidProgress * 88; // 0 -> 88 degrees

  // 2. Chassis tilt angle: starts isometric (25deg X, -12deg Y), flattens to 0deg as we zoom in
  const tiltX = (1 - scrollProgress) * 22;
  const tiltY = (1 - scrollProgress) * -8;

  // 3. Zoom scale: starts 0.85, zooms up to 2.8x inside screen as progress approaches 1
  const scale = 0.85 + scrollProgress * 1.8;

  // 4. Screen elevation & Y translation
  const translateY = scrollProgress * 80;

  return (
    <div 
      ref={containerRef}
      style={{
        position: 'relative',
        width: '100%',
        minHeight: '750px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        perspective: '1200px',
        overflow: 'visible',
        padding: '40px 0'
      }}
    >
      {/* Scroll Guidance Banner */}
      <div 
        style={{
          position: 'absolute',
          top: '10px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 16px',
          borderRadius: '20px',
          background: 'rgba(255, 255, 255, 0.04)',
          border: '1px solid var(--border-color)',
          backdropFilter: 'blur(12px)',
          color: 'var(--primary)',
          fontSize: '12px',
          fontWeight: '600',
          letterSpacing: '0.5px',
          zIndex: 20,
          opacity: Math.max(0.2, 1 - scrollProgress * 1.5),
          transition: 'opacity 0.3s ease'
        }}
      >
        <Sparkles size={14} className="animate-spin-slow" />
        <span>SCROLL TO OPEN 3D WORKSPACE & ENTER LAPTOP</span>
      </div>

      {/* Interactive 3D Controls Bar */}
      <div 
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          display: 'flex',
          gap: '8px',
          zIndex: 30
        }}
      >
        <button
          onClick={() => {
            window.scrollTo({ top: 550, behavior: 'smooth' });
          }}
          className="btn-glass"
          style={{
            padding: '8px 14px',
            fontSize: '12px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            cursor: 'pointer'
          }}
        >
          <Maximize2 size={13} />
          <span>Zoom Inside Screen</span>
        </button>

        <button
          onClick={onEnterWorkspace}
          style={{
            padding: '8px 16px',
            fontSize: '12px',
            borderRadius: '8px',
            background: 'var(--primary)',
            color: '#000',
            fontWeight: 'bold',
            border: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            cursor: 'pointer',
            boxShadow: '0 0 20px rgba(59, 130, 246, 0.4)'
          }}
        >
          <Monitor size={13} />
          <span>Open Full HITL Publisher</span>
        </button>
      </div>

      {/* 3D LAPTOP CONTAINER */}
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          width: '720px',
          height: '460px',
          position: 'relative',
          transformStyle: 'preserve-3d',
          transform: `scale(${scale}) translateY(${translateY}px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`,
          transition: 'transform 0.15s ease-out',
          zIndex: 10
        }}
      >
        {/* LAPTOP LID / DISPLAY SCREEN ASSEMBLY */}
        <div
          style={{
            width: '720px',
            height: '450px',
            position: 'absolute',
            top: 0,
            left: 0,
            borderRadius: '16px 16px 4px 4px',
            background: 'linear-gradient(145deg, #1e293b, #0f172a)',
            border: '2px solid rgba(255, 255, 255, 0.12)',
            transformOrigin: 'bottom center',
            transformStyle: 'preserve-3d',
            transform: `rotateX(-${lidAngle}deg)`,
            boxShadow: lidProgress > 0.1 ? '0 20px 50px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(255,255,255,0.05)' : 'none',
            transition: 'transform 0.1s ease-out'
          }}
        >
          {/* Outer Metal Shell Back (Appears when lid is closed/closing) */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              borderRadius: '16px 16px 4px 4px',
              background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #090d16 100%)',
              backfaceVisibility: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {/* Glowing Logo on Lid */}
            <div style={{
              width: '45px',
              height: '45px',
              borderRadius: '12px',
              background: 'rgba(59, 130, 246, 0.2)',
              border: '1px solid rgba(59, 130, 246, 0.5)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#3b82f6',
              boxShadow: '0 0 25px rgba(59, 130, 246, 0.5)'
            }}>
              <Sparkles size={24} />
            </div>
          </div>

          {/* INNER DISPLAY SCREEN GLASS (Inside Lid) */}
          <div
            style={{
              position: 'absolute',
              inset: '10px',
              borderRadius: '10px',
              background: '#040711',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              boxShadow: 'inset 0 0 30px rgba(0,0,0,0.9)'
            }}
          >
            {/* Screen Top Camera Bar */}
            <div style={{
              height: '22px',
              background: '#090d16',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0 16px',
              borderBottom: '1px solid rgba(255,255,255,0.05)'
            }}>
              <div style={{ display: 'flex', gap: '6px' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#ef4444' }}></span>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#f59e0b' }}></span>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981' }}></span>
              </div>
              <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#3b82f6', boxShadow: '0 0 8px #3b82f6' }}></div>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontFamily: 'monospace' }}>ResearchingOS v1.0.0</div>
            </div>

            {/* LIVE SCREEN CONTENT INTERFACE */}
            <div 
              style={{ 
                flex: 1, 
                padding: '16px', 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '12px',
                background: 'radial-gradient(circle at top right, rgba(30, 41, 59, 0.4), #040711)',
                opacity: Math.max(0, (lidAngle - 15) / 73),
                transition: 'opacity 0.2s ease'
              }}
            >
              {/* Screen Top Bar */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '2px', background: '#3b82f6' }}></div>
                  <span style={{ fontWeight: 'bold', fontSize: '13px', color: '#fff' }}>IEEE Systematic Review & Meta-Taxonomy</span>
                </div>
                <span style={{ fontSize: '10px', padding: '2px 8px', borderRadius: '10px', background: 'rgba(16, 185, 129, 0.2)', color: '#10b981', fontWeight: 'bold' }}>100% Fact-Checked</span>
              </div>

              {/* Screen Split Cards */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', flex: 1 }}>
                <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '8px', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#3b82f6', fontSize: '11px', fontWeight: 'bold' }}>
                    <FileText size={12} />
                    <span>53 Ingested Vault Papers</span>
                  </div>
                  <p style={{ fontSize: '10px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                    Empirical evidence, economic limits, and task boundary frontiers extracted across 12 scientific repositories.
                  </p>
                </div>

                <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '8px', padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#8b5cf6', fontSize: '11px', fontWeight: 'bold' }}>
                    <Users size={12} />
                    <span>7-Agent Council Debate</span>
                  </div>
                  <p style={{ fontSize: '10px', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                    Senior Systems Engineer, Statistician, and Reviewer #2 consensus synthesis.
                  </p>
                </div>
              </div>

              {/* Bottom Interactive Screen Prompt */}
              <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '6px', padding: '8px 12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '11px', color: '#93c5fd' }}>Click to launch workspace inside laptop screen</span>
                <button 
                  onClick={onEnterWorkspace}
                  style={{ background: '#3b82f6', color: '#000', border: 'none', borderRadius: '4px', padding: '4px 10px', fontSize: '10px', fontWeight: 'bold', cursor: 'pointer' }}
                >
                  Enter Workspace →
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* LAPTOP KEYBOARD BASE DECK */}
        <div
          style={{
            width: '740px',
            height: '420px',
            position: 'absolute',
            top: '445px',
            left: '-10px',
            borderRadius: '4px 4px 24px 24px',
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
            margin: '24px auto 16px auto',
            width: '640px',
            height: '240px',
            background: '#090d16',
            borderRadius: '10px',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px',
            boxShadow: 'inset 0 4px 10px rgba(0,0,0,0.8)'
          }}>
            {/* Key Rows Simulation */}
            {[1, 2, 3, 4, 5].map((row) => (
              <div key={row} style={{ display: 'flex', gap: '5px', height: row === 5 ? '38px' : '32px' }}>
                {Array.from({ length: row === 5 ? 8 : 14 }).map((_, i) => (
                  <div
                    key={i}
                    style={{
                      flex: row === 5 && i === 3 ? 4 : 1,
                      background: 'linear-gradient(180deg, #1e293b, #0f172a)',
                      borderRadius: '4px',
                      border: '1px solid rgba(255, 255, 255, 0.06)',
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
            width: '220px',
            height: '120px',
            background: 'rgba(255, 255, 255, 0.03)',
            borderRadius: '10px',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            boxShadow: 'inset 0 0 10px rgba(0,0,0,0.5)'
          }} />

          {/* Front Opening Notch */}
          <div style={{
            position: 'absolute',
            bottom: '0px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '70px',
            height: '6px',
            borderRadius: '6px 6px 0 0',
            background: 'rgba(255,255,255,0.2)'
          }} />
        </div>

        {/* Soft Ambient Shadow Projection */}
        <div style={{
          position: 'absolute',
          top: '520px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: '680px',
          height: '100px',
          borderRadius: '50%',
          background: 'radial-gradient(ellipse at center, rgba(59, 130, 246, 0.25) 0%, rgba(0,0,0,0.8) 50%, transparent 80%)',
          filter: 'blur(20px)',
          pointerEvents: 'none'
        }} />
      </div>
    </div>
  );
};

export default Laptop3DWorkspace;
