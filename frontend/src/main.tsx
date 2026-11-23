import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { OperatorGate } from './components/OperatorGate'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <OperatorGate><App /></OperatorGate>
  </StrictMode>,
)
