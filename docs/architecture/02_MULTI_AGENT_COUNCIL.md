# Layer Specification: Multi-Agent Council Architecture

## 1. Overview

The **Multi-Agent Council** (`backend/agents/council.py`) is the deliberative core of ResearchingOS. It replaces naive single-prompt LLM completion with an adversarial, role-specialized boardroom debate between 7 principal researcher personas.

---

## 2. The 7 Principal Agent Personas

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        7-AGENT COUNCIL PERSONA ROSTER                                  │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│ 1. Scout          │ 2. Analyst        │ 3. Systems Eng.   │ 4. Statistician            │
│   (Literature)    │   (Ingestion)     │   (Scaling/Compute│   (Methodological Rigor)   │
├───────────────────┼───────────────────┼───────────────────┼────────────────────────────┤
│ 5. Reviewer #2    │ 6. CEO / Chairman │ 7. Research Writer│                            │
│   (Hostile Audit) │   (Synthesis)     │   (IEEE Drafts)   │                            │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

### 2.1 Senior Scout Researcher (`Scout`)
- **System Instruction**: *"You are a Senior Principal Literature Scout. Your objective is to discover, filter, and rank high-impact academic literature across arXiv, OpenAlex, PubMed, Europe PMC, Crossref, and DBLP."*
- **Model**: `gemini-2.5-flash`

### 2.2 Lead Analyst (`Analyst`)
- **System Instruction**: *"You are a Senior Academic Research Analyst specializing in paper extraction. Your objective is to parse full paper PDFs into structured Obsidian Markdown notes with frontmatter metadata."*
- **Model**: `gemini-2.5-flash`

### 2.3 Senior Systems Engineer (`Engineer`)
- **System Instruction**: *"You are a Principal Systems Engineer and HPC Architecture Expert. Your objective is to audit paper methodologies for algorithmic complexity, parameter efficiency, GPU memory footprints, and FLOPs scaling laws."*
- **Model**: `gemini-2.5-flash`

### 2.4 Senior Statistician & Methods Critic (`Statistician`)
- **System Instruction**: *"You are a Senior Quantitative Statistician. Your objective is to audit paper experimental designs, checking sample sizes (N), p-values, confidence intervals, control baselines, and statistical power."*
- **Model**: `gemini-2.5-flash`

### 2.5 Reviewer #2 / Academic Editor (`Reviewer2`)
- **System Instruction**: *"You are a notoriously skeptical Reviewer #2 for top computer science journals (NeurIPS, TKDE, CSUR). Your objective is to identify un-ablated baselines, short-term horizon deficits, overhype risks, and rejection vulnerabilities."*
- **Model**: `gemini-2.5-flash`

### 2.6 CEO / Institute Chairman (`Chairman`)
- **System Instruction**: *"You are an Academic Institute Director and Board Chairman. Your objective is to moderate council debates, reconcile points of consensus and tension, and draft structured synthesis outlines."*
- **Model**: `gemini-2.5-flash`

### 2.7 Senior Research Writer & Publisher (`Writer`)
- **System Instruction**: *"You are a Senior Research Writer and Journal Publisher. Your objective is to draft formal 15+ page IEEE/ACM literature review manuscripts with LaTeX formulas, PRISMA search flow, and zero-hallucination wikilink citations."*
- **Model**: `gemini-2.5-flash`

---

## 3. Resilience, Model Cascading, & Rate-Limit Backoff

### 3.1 Model Cascade Rotation
To prevent pipeline failure when a specific model API quota is exhausted, `_call_gemini` implements a model cascade:
`candidate_models = [primary_model, "gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash"]`

If a 429 Daily Quota Exceeded error occurs (`quota_id: GenerateRequestsPerDayPerProjectPerModel-FreeTier`), the orchestrator immediately rotates to the next candidate model in the cascade.

### 3.2 Exponential Rate-Limit Retries
For temporary rate limits (429 per-minute quotas), `_call_gemini` executes up to 8 retry attempts with exponential backoff:
$$\text{Delay} = \min\left(60.0, 1.8^{\text{attempt}} \times 4.0 + \text{uniform}(0.5, 1.5)\right)\text{ seconds}$$

### 3.3 Soft Research Fallback
If all candidate models exhaust their daily quotas, the orchestrator gracefully applies a high-density structured analysis fallback, ensuring the paper ingestion, debate, and fact-checking steps complete 100% cleanly without crashing.
