---
name: camera-ready-latex-auditor
description: Audit and sanitize Markdown and LaTeX research manuscripts to ensure zero-defect camera-ready compilation (IEEE/ACM), clean section hierarchies, single unified bibliographies, and exact page budget compliance.
---

# 📜 Camera-Ready LaTeX Auditor Skill

Use this skill whenever drafting, editing, exporting, or compiling academic papers (IEEEtran, ACM, NeurIPS, ICML, CVPR, ACL).

---

## 🛠️ Mandatory Audit & Sanitization Rules

### Rule 1: Section Title Numbering (No Double Counters)
- **Problem**: Hardcoding numbers in Markdown headings (e.g., `# 1 Executive Abstract`, `## 2 Theoretical Foundations`) causes LaTeX section counters to prepend additional numbers, rendering `1 1 EXECUTIVE ABSTRACT`.
- **Action**: Always strip leading section numbers from Markdown heading strings before generating LaTeX section commands (`\section`, `\subsection`, `\subsubsection`).
- **Regex**: `title_text = re.sub(r'^(\d+[\.\s]*)+', '', title_text).strip()`

### Rule 2: Single Abstract Rendering (No Duplication)
- **Problem**: Placing the Executive Abstract in both `\begin{abstract}` and Section 1 body text creates duplicate abstract blocks.
- **Action**: Extract the full abstract into `clean_abstract` for the top `\begin{abstract}` environment, and strip the Abstract block from `body_for_export`.

### Rule 3: Single Unified Bibliography (No Duplicate References Headers)
- **Problem**: Retaining a hardcoded `## References` section in Markdown alongside `\bibliography{references}` renders two separate `REFERENCES` headings on the final page.
- **Action**: Filter out hardcoded markdown References sections (`re.sub(r'#{1,4}\s*(\d+[\.\s]*)?References[\s\S]*$', '', text)`) prior to LaTeX conversion, allowing `\bibliography{references}` to manage the official BibTeX list.

### Rule 4: Strict Page Budget Compliance
- **Short Papers / Letters**: Must fill **EXACTLY 4 camera-ready pages** without orphan line spillover onto Page 5.
- **Full Journal Reviews**: Must fill **EXACTLY 8–15 pages**.
- **Action**: Calibrate section text volume and paragraph spacing prior to final PDF submission.

### Rule 5: Math & Citation Character Escaping
- **Action**: Escape special LaTeX characters (`&` -> `\&`, `%` -> `\%`, `#` -> `\#`, `_` -> `\_`) in body text, while preserving math blocks (`$...$`, `$$...$$`) and citation keys (`\cite{...}`).

---

## 🧪 Verification Protocol
1. Run `python3 backend/services/checkmate_verifier.py` to audit PDF layout, section hierarchy, author attribution, and bibliography integrity.
2. Confirm `Checkmate Score` is **100.0% PASSED**.
