import React, { useState, useEffect } from 'react';
import { 
  Terminal, 
  Users, 
  Network, 
  FileText, 
  Activity, 
  AlertCircle,
  HelpCircle
} from 'lucide-react';
import Dashboard from './components/Dashboard';
import Boardroom from './components/Boardroom';
import GraphView from './components/GraphView';
import DocEditor from './components/DocEditor';

import { apiFetch } from './api';

export interface AgentLog {
  projectId: string;
  timestamp: number;
  stage: string;
  agent: string;
  message: string;
  data?: any;
}

export type ViewType = 'dashboard' | 'boardroom' | 'graph' | 'editor';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewType>('dashboard');
  const [activeTopic, setActiveTopic] = useState<string>('');
  const [logs, setLogs] = useState<AgentLog[]>([]);

  const [isResearching, setIsResearching] = useState<boolean>(false);
  const [apiHealth, setApiHealth] = useState<{ status: string; is_dry_run: boolean } | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Check health on mount
  useEffect(() => {
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await apiFetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setApiHealth(data);
      } else {
        setApiHealth({ status: 'error', is_dry_run: true });
      }
    } catch (e) {
      setApiHealth({ status: 'disconnected', is_dry_run: true });
      console.error('Failed to connect to backend api:', e);
    }
  };

  // Launch research query
  const startResearch = async (topicStr: string) => {
    if (!topicStr.trim()) return;
    setErrorMsg(null);
    setIsResearching(true);
    setLogs([]);
    setActiveTopic(topicStr);
    setCurrentView('boardroom'); // Automatically jump to Boardroom to watch the agents debate!

    try {
      const res = await fetch('/api/research/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topicStr })
      });

      if (!res.ok) {
        throw new Error(`Failed to start pipeline: ${res.statusText}`);
      }

      const data = await res.json();
      const projId = data.project_id;

      // Connect to SSE stream
      const eventSource = new EventSource(`/api/research/stream/${projId}`);

      eventSource.onmessage = (event) => {
        try {
          const logData = JSON.parse(event.data);
          setLogs((prev) => [...prev, logData]);
        } catch (e) {
          console.error('Error parsing SSE data:', e);
        }
      };

      eventSource.addEventListener('end', () => {
        console.log('Research stream finished');
        eventSource.close();
        setIsResearching(false);
      });

      eventSource.onerror = (err) => {
        console.error('SSE Error:', err);
        eventSource.close();
        setIsResearching(false);
        setErrorMsg('Lost connection to research stream. The process may still be running in the background.');
      };

    } catch (e: any) {
      console.error('Failed to start research:', e);
      setIsResearching(false);
      setErrorMsg(e.message || 'Failed to start research loop.');
      setCurrentView('dashboard');
    }
  };

  return (
    <div className="layout-grid">
      <div className="mesh-bg"></div>
      {/* Sidebar Navigation */}
      <aside className="sidebar glass">
        <div>
          {/* App Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '32px' }}>
            <div style={{ background: 'var(--primary)', width: '32px', height: '32px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '18px', color: '#000', fontFamily: 'var(--font-heading)', flexShrink: 0 }}>R</div>
            <div className="sidebar-text">
              <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '16px', fontWeight: 'bold', letterSpacing: '0.5px' }}>ResearchingOS</h1>
              <p style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>V1.0.0-PRO-Deliberate</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <button 
              onClick={() => setCurrentView('dashboard')}
              className="sidebar-nav-btn"
              style={{
                backgroundColor: currentView === 'dashboard' ? 'var(--primary-glow)' : 'transparent',
                color: currentView === 'dashboard' ? 'var(--primary)' : 'var(--text-secondary)',
                fontWeight: currentView === 'dashboard' ? '600' : '400',
              }}
            >
              <Terminal size={18} strokeWidth={1.5} style={{ flexShrink: 0 }} />
              <span className="sidebar-text">Control Deck</span>
            </button>

            <button 
              onClick={() => setCurrentView('boardroom')}
              className="sidebar-nav-btn"
              style={{
                backgroundColor: currentView === 'boardroom' ? 'var(--primary-glow)' : 'transparent',
                color: currentView === 'boardroom' ? 'var(--primary)' : 'var(--text-secondary)',
                fontWeight: currentView === 'boardroom' ? '600' : '400',
              }}
            >
              <Users size={18} strokeWidth={1.5} style={{ flexShrink: 0 }} />
              <span className="sidebar-text" style={{ display: 'flex', alignItems: 'center', width: '100%', gap: '8px' }}>
                <span>Agent Boardroom</span>
                {isResearching && (
                  <span className="pulse-loading" style={{ marginLeft: 'auto', width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--primary)' }}></span>
                )}
              </span>
            </button>

            <button 
              onClick={() => setCurrentView('graph')}
              className="sidebar-nav-btn"
              style={{
                backgroundColor: currentView === 'graph' ? 'var(--primary-glow)' : 'transparent',
                color: currentView === 'graph' ? 'var(--primary)' : 'var(--text-secondary)',
                fontWeight: currentView === 'graph' ? '600' : '400',
              }}
            >
              <Network size={18} strokeWidth={1.5} style={{ flexShrink: 0 }} />
              <span className="sidebar-text">Knowledge Graph</span>
            </button>

            <button 
              onClick={() => setCurrentView('editor')}
              className="sidebar-nav-btn"
              style={{
                backgroundColor: currentView === 'editor' ? 'var(--primary-glow)' : 'transparent',
                color: currentView === 'editor' ? 'var(--primary)' : 'var(--text-secondary)',
                fontWeight: currentView === 'editor' ? '600' : '400',
              }}
            >
              <FileText size={18} strokeWidth={1.5} style={{ flexShrink: 0 }} />
              <span className="sidebar-text">HITL Publisher</span>
            </button>
          </nav>
        </div>

        {/* System Health / API indicator */}
        <div className="glass sidebar-health" style={{ padding: '14px', fontSize: '12px', display: 'flex', flexDirection: 'column', gap: '8px', backgroundColor: 'rgba(255,255,255,0.01)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={14} strokeWidth={1.5} color={apiHealth?.status === 'healthy' ? 'var(--success)' : 'var(--warning)'} />
            <span style={{ fontWeight: '500' }}>Backend API</span>
            <span style={{ marginLeft: 'auto', fontSize: '9px', padding: '2px 6px', borderRadius: '4px', background: apiHealth?.status === 'healthy' ? 'rgba(52,211,153,0.15)' : 'rgba(251,191,36,0.15)', color: apiHealth?.status === 'healthy' ? 'var(--success)' : 'var(--warning)' }}>
              {apiHealth?.status || 'checking'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <HelpCircle size={14} strokeWidth={1.5} color="var(--text-secondary)" />
            <span>Gemini LLMs</span>
            <span style={{ marginLeft: 'auto', fontSize: '9px', padding: '2px 6px', borderRadius: '4px', background: apiHealth?.is_dry_run ? 'rgba(251,113,133,0.15)' : 'rgba(52,211,153,0.15)', color: apiHealth?.is_dry_run ? 'var(--danger)' : 'var(--success)' }}>
              {apiHealth?.is_dry_run ? 'Dry Run' : 'Active'}
            </span>
          </div>

          {errorMsg && (
            <div style={{ display: 'flex', gap: '6px', color: 'var(--danger)', marginTop: '8px', fontSize: '10px', lineHeight: '1.2' }}>
              <AlertCircle size={12} style={{ flexShrink: 0 }} />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main style={{ padding: '12px 12px 12px 6px', height: '100%', overflow: 'auto' }}>
        {currentView === 'dashboard' && (
          <Dashboard 
            startResearch={startResearch} 
            isResearching={isResearching} 
            onEnterWorkspace={() => setCurrentView('editor')}
          />
        )}
        {currentView === 'boardroom' && (
          <Boardroom 
            logs={logs} 
            isResearching={isResearching}
            activeTopic={activeTopic}
          />
        )}
        {currentView === 'graph' && (
          <GraphView />
        )}
        {currentView === 'editor' && (
          <DocEditor />
        )}
      </main>
    </div>
  );
};

export default App;
