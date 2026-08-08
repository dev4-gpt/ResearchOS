# Architectural Specification: Obsidian & Graphify Knowledge Graph Engine

## 1. Overview & Core Answers

### Q1: Why did refreshing the Knowledge Graph produce a different visual outcome?
Previously, the force-directed physics layout in `GraphView.tsx` initialized node coordinates $(x, y)$ using pseudo-random math (`Math.random() - 0.5`). 

**Resolution Applied**: We replaced pseudo-random initialization with a **100% deterministic string hashing algorithm** (`hashStringToFloat(node.id)`). Now, refreshing the Knowledge Graph always yields the **exact same spatial layout and node positions**.

---

### Q2: How are Obsidian and Graphify used in ResearchingOS?

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OBSIDIAN & GRAPHIFY INTEGRATION                                 │
├───────────────────────────────┬───────────────────────────────┬────────────────────────┤
│ 1. Obsidian Vault Storage     │ 2. Graphify Knowledge Graph   │ 3. Deterministic 3D/2D │
│    (`vault/` Markdown System) │    (Community & God Nodes)    │    Interactive Visuals │
└───────────────────────────────┴───────────────────────────────┴────────────────────────┘
```

#### 1️⃣ Obsidian Vault Knowledge System (`vault/`)
- **Native File Format**: All research notes, concept cards, debate transcripts, and paper drafts are saved directly as `.md` files with **YAML frontmatter** and **Obsidian `[[WikiLinks]]`** (`[[crossref_10.2139_ssrn.5260645]]`).
- **Obsidian Interoperability**: The `vault/` directory can be opened directly as an Obsidian Vault in the official Obsidian app.

#### 2️⃣ Graphify Engine Integration (`GraphView.tsx` & `VaultManager`)
- **Graph Topology Extraction**: `VaultManager.get_knowledge_graph()` parses all markdown files and `[[WikiLinks]]`, constructing node-edge relationship matrices.
- **God Nodes & Category Clustering**:
  - `papers` (Emerald `#10b981`): Ingested literature notes.
  - `concepts` (Amber `#f59e0b`): Cross-paper taxonomy & entity cards.
  - `debates` (Violet `#8b5cf6`): Boardroom council debate transcripts.
  - `drafts` (Rose `#f43f5e`): 15+ page IEEEtran manuscripts.
