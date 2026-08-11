# Research OS Component: AI Venue Formatting & O-1A Alignment Hub

> **Evidence-system boundary:** O-1A and EB-1A are distinct immigration classifications. This document is an evidence-collection and portfolio-tracking specification, not legal advice or an eligibility determination. Regulatory mappings must be reviewed against the current USCIS Policy Manual by qualified counsel.

This document integrates submission rules for elite AI venues with actionable **O-1A Visa Alignment Strategies**, **Model Context Protocol (MCP)** architectures, and **Developer Ecosystem Tools** to automate a high-impact research pipeline at Penn State.

---

## 1. Elite AI Venue Technical Specifications & O-1A Mapping

### A. NeurIPS (Neural Information Processing Systems)
* **Core Formatting:**
  * **Page Limit:** 9 pages max (main text, figures, tables). Unlimited pages for references/appendices.
  * **Layout:** Single-column layout. Main text font size is 10pt Times New Roman/Computer Modern.
  * **LaTeX Boilerplate:** `\usepackage{neurips_2026}` (use `[final]` option only after acceptance).
  * **Anonymization:** Double-blind. Mask all author names, institutional affiliations (Penn State), and explicit grant IDs. Use placeholders like `Anonymous Project GitHub` for repositories.
* **O-1A Visa Alignment Strategy:**
  * **Primary Target Criteria:** **Scholarly Articles** (8 CFR § 204.5(h)(3)(vi)).
  * **Leverage Point:** NeurIPS is highly selective. Highlight its sub-15% oral or sub-25% poster acceptance rates in your visa petition letters. 
  * **Citation Multiplier:** Open-source your training algorithms via Hugging Face. Submit code alongside your paper to trigger high GitHub traction and citation rates.

### B. ICML (International Conference on Machine Learning)
* **Core Formatting:**
  * **Page Limit:** 9 pages max for the camera-ready version (excluding references/appendix).
  * **Layout:** Two-column format. US Letter size strictly required (do not use A4). Font size is 10pt.
  * **LaTeX Boilerplate:** `\usepackage{icml2026}` (use `[accepted]` option for final camera-ready).
  * **Anonymization:** Double-blind. Third-person phrasing for self-citations (e.g., "Smith et al. [1] previously proved..." instead of "In our previous work [1], we proved...").
* **O-1A Visa Alignment Strategy:**
  * **Primary Target Criteria:** **Original Scientific Contributions of Major Significance** (8 CFR § 204.5(h)(3)(v)).
  * **Leverage Point:** Target core algorithmic breakthroughs. Focus on optimization stability or architectural efficiency.
  * **Citation Multiplier:** Release an executable benchmarking suite or dataset. Framework papers inherently command 3x higher citation loops than purely theoretical variants.

### C. CVPR (Conference on Computer Vision and Pattern Recognition)
* **Core Formatting:**
  * **Page Limit:** 8 pages max (excluding references).
  * **Layout:** Two-column format with line numbers enabled for the review draft. Font size is 9pt or 10pt.
  * **LaTeX Boilerplate:** `\usepackage{cvpr}` (use `[final]` option for camera-ready submission).
  * **Anonymization:** Strict anonymization. Strip camera EXIF data and sensor metadata from all supplemental visual assets or video demos.
* **O-1A Visa Alignment Strategy:**
  * **Primary Target Criteria:** **Scholarly Articles** & **Published Material About the Alien** (8 CFR § 204.5(h)(3)(iii)).
  * **Leverage Point:** Visual generative models or computer vision frameworks are ideal for public or technical media coverage.
  * **Citation Multiplier:** Build an interactive demo hosted via Gradio on Hugging Face Spaces. High visibility drives organic mentions in industry newsletters and downstream research.

### D. ACL (Association for Computational Linguistics)
* **Core Formatting:**
  * **Page Limit:** 8 pages for long papers; 4 pages for short papers (excluding references).
  * **Layout:** Two-column layout using specific ACL style packages.
  * **LaTeX Boilerplate:** `\usepackage{acl}`.
  * **Anonymization:** Centralized via the **ACL Rolling Review (ARR)**. Mask pipeline weights, model hosting links, and fine-tuning prompt templates.
* **O-1A Visa Alignment Strategy:**
  * **Primary Target Criteria:** **Judging the Work of Others** (8 CFR § 204.5(h)(3)(iv)).
  * **Leverage Point:** Publishing in ACL fast-tracks your invitation to serve as a program committee member or workshop reviewer for subsequent ARR cycles.
  * **Citation Multiplier:** Publish complete, reproducible prompt libraries and fine-tuning system messages in a dedicated, structured GitHub repository.

---

## 2. Research OS Automation: Model Context Protocol (MCP) & Connectors

To elevate your research workflow from a manual writing process to an integrated AI-driven OS, deploy the following technical stack. These tools leverage **Model Context Protocol (MCP)**, connecting LLMs directly to your local execution loops, literature graphs, and codebase infrastructure.

```
                  +---------------------------------------+
                  |              RESEARCH OS              |
                  +---------------------------------------+
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
       v                              v                              v
+--------------------------+   +--------------------------+   +--------------------------+
|  LITERATURE REASONING   |   |   COMPUTATIONAL ENGINE   |   |   WRITING & PIPELINE     |
|  - Semantic Scholar MCP  |   |   - Local Execution Host |   |   - Zotero Citation API  |
|  - ResearchRabbit Graph  |   |   - Git/GitHub Tracking  |   |   - Overleaf/LaTeX Sync  |
+--------------------------+   +--------------------------+   +--------------------------+
```

### A. Literature Search & Citation Graph Connectors
* **Semantic Scholar MCP Server:** 
  * *Capability:* Connects your IDE or LLM assistant directly to the Semantic Scholar API.
  * *Execution Loop:* Dynamically searches papers, pulls citation counts, extracts abstract metadata, and generates formatted `\bibitem` elements via natural language prompts.
* **ResearchRabbit & Connected Papers:** 
  * *Capability:* Bi-directional sync tools that monitor your foundational literature.
  * *Execution Loop:* Automatically maps out citation networks, alerts you to newly published competition, and identifies co-citation clusters to cite in your related work section.

### B. Computational & Repository Connectors
* **Local Execution MCP Server:** 
  * *Capability:* Provides secure sandbox execution layers allowing your AI system to read local Python logs, track execution steps, and analyze training outputs.
  * *Execution Loop:* Analyzes PyTorch loss curves, cross-checks hyperparameter logs against your LaTeX results section, and autogenerates exact PGF/TikZ plotting code.
* **GitHub Connector:** 
  * *Capability:* Keeps codebases synced directly with paper claims.
  * *Execution Loop:* Automates code packaging, runs code formatting standard reviews, builds anonymized mirror repositories, and populates GitHub Release notes for open-source criteria traction.

### C. Writing & Publication Synchronization Connectors
* **Zotero API Connector:** 
  * *Capability:* Standardized reference manager integration.
  * *Execution Loop:* Monitors specific collection folders (e.g., `PennState_O1_NeurIPS_2026`). Automatically exports, reformats, and syncs an updated, clean `.bib` citation file to your active working path.
* **Overleaf Git Integration:** 
  * *Capability:* Secure continuous synchronization with online document editors.
  * *Execution Loop:* Allows you to treat your Overleaf paper project as a standard git remote repository. Seamlessly push updates, run automated local spelling and syntax checks, and pull collaborative comments written by your Penn State advisor.

---

## 3. High-Velocity Skills Setup Guide for O-1A Success

Implement these five operational skills to maximize your publication volume and visa tracking during your Master's program:

1. **Automated Citation Pipeline:** Use Zotero coupled with BibTeX auto-export to maintain a clean local citation library, completely eliminating manual editing cycles.
2. **Abstract and Introduction Prototyping:** Frame your research pitches strictly around the **Problem-Method-Experiment (PME)** paradigm to optimize for clarity and reduce structural review friction.
3. **Continuous Benchmarking:** Build your PyTorch training pipelines using logging frameworks like TensorBoard or Weights & Biases. This preserves data integrity and simplifies generating experimental tables.
4. **Anonymized Artifact Generation:** Utilize automated shell scripts to strip specific system paths, user names, and institutional metadata from your source code prior to submission deadlines.
5. **O-1 Evidence Tracking:** Log every workshop review invitation, paper acceptance notification, and milestone citation in a central database to simplify future immigration petitions.
