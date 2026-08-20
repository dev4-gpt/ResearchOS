import React, { useEffect, useRef } from 'react';
import { Users, Loader, CheckCircle } from 'lucide-react';
import type { AgentLog } from '../App';
import LinkRenderer from './LinkRenderer';

interface BoardroomProps {
  logs: AgentLog[];
  isResearching: boolean;
  activeTopic: string;
}

// Map agent names to styling themes
const AGENT_META: Record<string, { color: string; short: string; bg: string }> = {
  'Senior Scout Researcher': { color: '#3b82f6', short: 'Scout', bg: 'rgba(59, 130, 246, 0.1)' },
  'Lead Analyst': { color: '#10b981', short: 'Analyst', bg: 'rgba(16, 185, 129, 0.1)' },
  'Senior Systems Engineer': { color: '#6366f1', short: 'Engineer', bg: 'rgba(99, 102, 241, 0.1)' },
  'Senior Statistician & Methods Critic': { color: '#f59e0b', short: 'Statistician', bg: 'rgba(245, 158, 11, 0.1)' },
  'Reviewer #2 / Academic Editor': { color: '#f43f5e', short: 'Reviewer2', bg: 'rgba(244, 63, 94, 0.1)' },
  'CEO / Institute Chairman': { color: '#8b5cf6', short: 'Chairman', bg: 'rgba(139, 92, 246, 0.1)' },
  'Senior Research Writer & Publisher': { color: '#ec4899', short: 'Writer', bg: 'rgba(236, 72, 153, 0.1)' },
  'System': { color: '#9ca3af', short: 'System', bg: 'rgba(156, 163, 175, 0.1)' }
};

const Boardroom: React.FC<BoardroomProps> = ({ logs, isResearching, activeTopic }) => {
  const logEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom of log stream
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  // Find the agent that is currently speaking/working based on logs
  const getActiveAgent = (): string | null => {
    if (!isResearching || logs.length === 0) return null;
    const lastLog = logs[logs.length - 1];
    if (lastLog.stage === 'Completion' || lastLog.message.includes('completed successfully')) return null;
    return lastLog.agent;
  };

  const activeAgent = getActiveAgent();

  return (
    <div style={{ display: 'grid', gridTemplateRows: 'auto 175px 1fr', height: '100%', gap: '16px', overflow: 'hidden' }}>

      {/* Top Banner */}
      <div className="glass" style={{ padding: '20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <span style={{ fontSize: '10px', color: 'var(--primary)', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '1px', fontFamily: 'var(--font-heading)' }}>
            Active Session
          </span>
          <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '18px', fontWeight: '800' }}>
            {activeTopic ? `Topic: ${activeTopic}` : 'No Active Session'}
          </h2>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {isResearching ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(129,140,248,0.15)', color: 'var(--primary)', padding: '6px 14px', borderRadius: '9999px', fontSize: '12px', fontWeight: '700', fontFamily: 'var(--font-heading)', border: '1px solid rgba(129,140,248,0.2)' }}>
              <Loader size={12} strokeWidth={2} className="pulse-loading" style={{ animation: 'spin 2s linear infinite' }} />
              <span>Council Deliberating</span>
            </div>
          ) : activeTopic ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(52,211,153,0.15)', color: 'var(--success)', padding: '6px 14px', borderRadius: '9999px', fontSize: '12px', fontWeight: '700', fontFamily: 'var(--font-heading)', border: '1px solid rgba(52,211,153,0.2)' }}>
              <CheckCircle size={12} strokeWidth={2} />
              <span>Session Completed</span>
            </div>
          ) : (
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', fontFamily: 'var(--font-heading)', fontWeight: '600' }}>Idle</div>
          )}
        </div>
      </div>

      {/* Agents Grid (Office Layout) */}
      <div style={{ display: 'flex', gap: '12px', overflowX: 'auto', paddingBottom: '8px', scrollSnapType: 'x mandatory' }}>
        {Object.entries(AGENT_META).map(([agentName, meta]) => {
          if (agentName === 'System') return null;
          const isCurrentSpeaker = activeAgent === agentName;
          return (
            <div
              key={agentName}
              className="double-bezel-outer tilt-3d"
              style={{
                flex: '0 0 190px', scrollSnapAlign: 'start',
                border: isCurrentSpeaker ? `1px solid ${meta.color}` : '1px solid var(--border-color)',
                boxShadow: isCurrentSpeaker ? `0 0 16px ${meta.color}25` : 'none',
              }}
            >
              <div className="double-bezel-inner" style={{ padding: '14px', gap: '4px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '2px' }}>
                  {/* Status Dot */}
                  <div
                    className={isCurrentSpeaker ? 'agent-active-glow' : ''}
                    style={{
                      width: '6px', height: '6px', borderRadius: '50%',
                      backgroundColor: isCurrentSpeaker ? 'var(--primary)' : isResearching ? 'var(--text-muted)' : 'var(--success)',
                    }}
                  ></div>
                  <span style={{ fontSize: '9px', fontWeight: '800', color: meta.color, textTransform: 'uppercase', letterSpacing: '0.8px', fontFamily: 'var(--font-heading)' }}>
                    {meta.short}
                  </span>
                </div>
                <h4 style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontFamily: 'var(--font-heading)' }}>
                  {agentName.split(' ')[0] + ' ' + (agentName.split(' ')[1] || '')}
                </h4>
                <p style={{ fontSize: '11px', color: 'var(--text-secondary)', lineHeight: '1.2', height: '24px', overflow: 'hidden' }}>
                  {agentName.includes('Scout') ? 'Ingestion Core' : agentName.includes('Analyst') ? 'Summaries' : agentName.includes('Writer') ? 'Publisher' : 'Critiques'}
                </p>
                {isCurrentSpeaker && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: 'auto' }}>
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span style={{ fontSize: '9px', color: 'var(--text-secondary)', animation: 'pulse-opacity 1s infinite', fontWeight: '500' }}>Speaking...</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Debate & Communication Log Panel */}
      <div className="glass" style={{ display: 'grid', gridTemplateRows: 'auto 1fr', padding: '20px', overflow: 'hidden' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '16px', fontWeight: '800', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Users size={16} strokeWidth={1.5} />
          <span>Council Communication Log</span>
        </h3>

        <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px', padding: '12px 6px', height: '100%' }}>
          {logs.length === 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)', gap: '8px' }}>
              <Users size={32} style={{ opacity: '0.4' }} />
              <p style={{ fontSize: '13px' }}>The boardroom is currently empty.</p>
              <p style={{ fontSize: '11px' }}>Initiate a topic on the Control Deck to summon the council.</p>
            </div>
          ) : (
            logs.map((log, index) => {
              const meta = AGENT_META[log.agent] || { color: '#ffffff', short: 'Agent', bg: 'rgba(255,255,255,0.05)' };
              const isSystem = log.agent === 'System';

              return (
                <div
                  key={index}
                  style={{
                    display: 'flex', flexDirection: 'column', gap: '6px',
                    alignSelf: isSystem ? 'center' : 'flex-start',
                    width: isSystem ? '90%' : '100%',
                    backgroundColor: isSystem ? 'rgba(255,255,255,0.01)' : 'transparent',
                    borderLeft: isSystem ? 'none' : `3px solid ${meta.color}`,
                    padding: isSystem ? '10px' : '4px 0 4px 12px',
                    borderRadius: isSystem ? '6px' : '0',
                    border: isSystem ? '1px dashed var(--border-color)' : 'none'
                  }}
                >
                  {/* Speaker Header */}
                  {!isSystem && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--text-primary)' }}>{log.agent}</span>
                      <span style={{ fontSize: '9px', padding: '1px 6px', borderRadius: '4px', backgroundColor: meta.bg, color: meta.color, fontWeight: '600', textTransform: 'uppercase' }}>
                        {log.stage}
                      </span>
                      <span style={{ fontSize: '10px', color: 'var(--text-muted)', marginLeft: 'auto' }}>
                        {new Date(log.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                      </span>
                    </div>
                  )}

                  {/* Message Bubble */}
                  <div style={{
                    fontSize: '13px',
                    color: isSystem ? 'var(--text-secondary)' : 'var(--text-primary)',
                    lineHeight: '1.5',
                    fontFamily: isSystem ? 'var(--font-mono)' : 'var(--font-sans)',
                  }}>
                    {isSystem && <span style={{ color: 'var(--primary)', marginRight: '6px' }}>&gt;</span>}
                    <LinkRenderer content={log.message} />
                  </div>
                </div>
              );
            })
          )}
          {isResearching && (
            <div style={{ display: 'flex', gap: '10px', padding: '10px 0', borderLeft: '3px solid var(--primary)', paddingLeft: '12px' }}>
              <Loader size={16} className="pulse-loading" style={{ animation: 'spin 2s linear infinite', color: 'var(--primary)', flexShrink: 0 }} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontStyle: 'italic' }}>Generating next review step...</span>
              </div>
            </div>
          )}
          <div ref={logEndRef} />
        </div>
      </div>

    </div>
  );
};

export default Boardroom;
