import { useEffect, useState, type ReactNode, type FormEvent } from 'react';
import { apiFetch } from '../api';

export function OperatorGate({ children }: { children: ReactNode }) {
  const [state, setState] = useState<'loading' | 'login' | 'ready' | 'error'>('loading');
  const [username, setUsername] = useState('operator');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  useEffect(() => {
    apiFetch('/api/session').then(res => {
      setState(res.ok ? 'ready' : res.status === 401 ? 'login' : 'error');
      if (res.status === 503) setMessage('Operator access needs to be configured on the server.');
    }).catch(() => { setState('error'); setMessage('Cannot connect to ResearchingOS.'); });
  }, []);
  async function login(event: FormEvent) {
    event.preventDefault();
    try {
      const bytes = new TextEncoder().encode(`${username}:${password}`);
      const authorization = 'Basic ' + btoa(Array.from(bytes, b => String.fromCharCode(b)).join(''));
      const response = await apiFetch('/api/session', { method: 'POST', headers: { Authorization: authorization } });
      setPassword('');
      if (!response.ok) { setMessage('Sign-in failed. Check your credentials and server configuration.'); return; }
      const verified = await apiFetch('/api/session');
      if (verified.ok) setState('ready');
      else setMessage('Session cookie was not accepted. Use the configured HTTPS address.');
    } catch { setMessage('Cannot connect to ResearchingOS.'); }
  }
  async function logout() {
    try {
      const response = await apiFetch('/api/session', { method: 'DELETE' });
      if (!response.ok) throw new Error('Sign-out failed.');
      // Dispose active streams and job state held by mounted child components.
      setState('login'); setMessage(''); setPassword('');
    } catch { setMessage('Could not sign out. Please try again.'); }
  }
  if (state === 'ready') return <>
    <div style={{ position: 'fixed', right: 16, top: 12, zIndex: 1000 }}>
      <button onClick={() => void logout()}>Sign out</button>
      {message && <p role="alert">{message}</p>}
    </div>
    {children}
  </>;
  return <main style={{ maxWidth: 440, margin: '15vh auto', padding: 24 }}>
    <h1>ResearchingOS</h1>
    {state === 'loading' ? <p>Checking access…</p> : state === 'login' ?
      <form onSubmit={login} style={{ display: 'grid', gap: 16 }}>
        <h2>Operator sign-in</h2>
        <label>Username<input autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} /></label>
        <label>Password<input type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} /></label>
        <button type="submit">Sign in</button>
      </form> : <p>Service unavailable. Check the server configuration and connection.</p>}
    {message && <p role="alert">{message}</p>}
  </main>;
}
