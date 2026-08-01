# Layer Specification: Frontend Architecture & 3D Laptop Workspace

## 1. Overview

The **Frontend Subsystem** (`frontend/src/`) is built with **React 19**, **TypeScript 6.0**, **Vite 8.0**, and **3D CSS Transforms**. It provides a glassmorphic user interface featuring a 3D scroll-driven metallic laptop opening sequence, live boardroom streaming, interactive knowledge graphs, and a Human-in-the-Loop (HITL) document publisher.

---

## 2. Views & Navigation Structure

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND VIEW NAVIGATION STRUCTURE                              │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ 1. Control Deck   │ 2. Agent Boardroom│ 3. Knowledge Graph│ 4. HITL Publisher          │
│   (Dashboard.tsx) │   (Boardroom.tsx) │   (GraphView.tsx) │   (DocEditor.tsx)          │
│   3D Laptop Hero  │   Live SSE Logs   │   Obsidian Graph  │   IEEE Manuscript & LaTeX  │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

### 2.1 3D Laptop Workspace Component (`Laptop3DWorkspace.tsx`)
- **3D CSS Assembly**: Metallic Space Gray chassis (`perspective: 1200px`, `transform-style: preserve-3d`), keyboard well, glowing key caps, trackpad, and ambient shadow projection.
- **Scroll & Manual Controls**:
  - Automatically attaches scroll listeners to nearest parent container (`<main>`).
  - Lid opens from 0° to 90° (`rotateX(-lidAngle deg)`). Default state starts open at **75°** for vibrant display visibility.
  - Camera zooms inside display screen ($0.7\times$ to $2.2\times$).
  - Top control bar provides manual lid angle and zoom range sliders.

### 2.2 HITL Publisher & Document Editor (`DocEditor.tsx`)
- **Obsidian Vault Explorer**: Lists vault files categorized under `Manuscript Drafts (04_Drafts)`, `Debate Summaries (03_Debates)`, `Research Papers (01_Papers)`, and `Concept Notes (02_Concepts)`.
- **Live Markdown & Preview**: Toggle between Markdown source and rendered academic article preview.
- **Fact-Check Score Badge**: Displays `Fact-Check Score: 88.5%` (PASSED).
- **Export IEEEtran LaTeX & BibTeX**: One-click download button fetching `/api/vault/export-latex`.

### 2.3 Bulletproof API Client (`api.ts`)
- **Dual-Layer API Fetcher**: Tries relative `/api/...` endpoints first (Vite proxy). If proxy fails or returns a network error, falls back to direct `http://127.0.0.1:8000/api/...` backend URL.
- **UI Retry Button**: Built-in connection retry action when backend is initializing.
