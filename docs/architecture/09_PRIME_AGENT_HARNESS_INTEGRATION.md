# Architectural Specification: Prime Agent Harness Integration

## 1. Overview & Inspiration

Inspired by **Prime Intellect's `prime-agent`** harness ([github.com/PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent)), ResearchingOS integrates a **Recursive Language Model (RLM) & Continual Harness Engine** to convert static single-pass research execution into an autonomous, self-improving, persistent multi-agent publishing engine.

---

## 2. Core Architectural Pillars

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRIME AGENT HARNESS FOR RESEARCHINGOS                           │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ Pillar 1: RLM     │ Pillar 2: Continual│ Pillar 3: Dynamic │ Pillar 4: Autonomous       │
│    Context Split  │    Refinement     │    Sub-Agent      │    Heartbeat Monitor       │
│   (Recursive      │   (Self-Improving │    Delegation     │   (Goal Tracking &         │
│    Partitioning)  │    Prompts/Skills)│   (Python Kernel) │    State Persistence)      │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

### 2.1 Recursive Language Model (RLM) Context Partitioning
- **Concept**: Treat LLM context as a dynamic variable rather than a fixed window.
- **Implementation (`rlm_orchestrator.py`)**: When ingesting large corpora (20–50+ paper PDFs), the main orchestrator splits search clusters into recursive sub-agent contexts. Each sub-agent processes a subset of papers, generates structured paper notes in `vault/01_Papers/`, and returns compressed semantic representations to the parent context.

### 2.2 Continual Harness & Self-Refining Trajectory (`/refine`)
- **Concept**: The agent maintains durable runtime state, self-auditing its execution after every run to refine its own prompts, verification rules, and vault skills.
- **Implementation (`continual_memory.py`)**: After `FactCheckerService` audits a manuscript, the `/refine` pipeline evaluates citation link coverage, metric grounding, and Reviewer #2 objections. If fact-check scores fall below target thresholds, the harness updates agent prompt memory (`durable_memory.json`) and refines search heuristics automatically.

### 2.3 Autonomous Heartbeat Monitor & Goal Controller
- **Concept**: Long-running autonomous research execution with goal status tracking and heartbeat safety bounds.
- **Implementation (`autonomous_loop.py`)**: Monitors multi-step paper discovery, full-text ingestion, council debate, and IEEEtran compilation, ensuring zero pipeline deadlocks.

---

## 3. Integration Plan with Existing Subsystems

- **`CouncilOrchestrator` (`backend/agents/council.py`)**: Enhanced with RLM sub-agent spawning and continual memory state injection.
- **`FactCheckerService` (`backend/services/fact_checker.py`)**: Emits trajectory telemetry to `ContinualHarnessRefiner` after every manuscript audit.
- **FastAPI Endpoints (`backend/main.py`)**:
  - `POST /api/harness/refine`: Manually trigger harness self-refinement.
  - `GET /api/harness/state`: Retrieve durable memory state and execution trajectory metrics.
