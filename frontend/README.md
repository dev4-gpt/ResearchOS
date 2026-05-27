# ResearchingOS — Frontend

React 19 + TypeScript + Vite UI for the ResearchingOS agent pipeline.

## Setup

```bash
npm install
npm run dev      # http://localhost:5173 (proxies API calls to :8000)
npm run build    # production build → dist/
npm run lint     # ESLint
```

The backend must be running on port 8000 (see `../backend/README.md`).

## Components

| Component | Purpose |
| --- | --- |
| `App.tsx` | Root router / layout |
| `Dashboard.tsx` | Topic input, research trigger, live SSE log feed |
| `Boardroom.tsx` | Animated agent debate view — renders council turns in real time |
| `GraphView.tsx` | Force-directed knowledge graph from `GET /api/vault/graph` |
| `DocEditor.tsx` | Read/edit vault Markdown files with frontmatter preview |

## Tech stack

- React 19 (with React Compiler support available — see below)
- TypeScript 5
- Vite 6
- Lucide icons

## Enabling the React Compiler

The React Compiler is disabled by default for build-time performance. To enable it:

```bash
npm install babel-plugin-react-compiler
```

Then add to `vite.config.ts`:

```ts
babel: { plugins: ['babel-plugin-react-compiler'] }
```

## Environment

No frontend-specific env vars are required. The Vite dev server proxies `/api/*` to `http://localhost:8000` — see `vite.config.ts`.
