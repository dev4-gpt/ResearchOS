# 📐 Master Venue Formatting, Page-Budget & Length Specifications
**ResearchingOS Academic Camera-Ready Submission Standard**

To eliminate automated desk rejections, page-budget violations, and formatting discrepancies across target academic venues, all generated manuscripts in ResearchingOS must comply strictly with the following specifications.

---

## 🏛️ Venue Comparison Matrix

| Venue Identifier | Venue Full Name | Column Layout | Font & Page Size | Main Body Page Budget | References Limit | Anonymization Rule | Desk Rejection Risk |
|---|---|---|---|---|---|---|---|
| **`IEEEtran`** | IEEE Transactions / Short Papers | **Two-Column** | 10pt Times, US Letter | **4 Pages** (Short/Camera-Ready) or **10–14 Pages** (Journal) | Included in page budget | Single-Blind (Author names included) | ❌ 3-page underflow or 5-page spillover page |
| **`NeurIPS`** | Neural Information Processing Systems | **Single-Column** | 10pt Times, US Letter | **9 Pages** (Max main content) | Unlimited (after p.9) + Checklist | **Double-Blind** (Mask names, grants, repos) | ❌ Content past p.9 before references |
| **`ICML`** | International Conference on ML | **Two-Column** | 10pt Times, US Letter | **8 Pages** (Max main body) | Unlimited (after p.8) | **Double-Blind** (Use 3rd-person self-citations) | ❌ Main body text spilling onto page 9 |
| **`CVPR`** | IEEE/CVF Conf. on Computer Vision | **Two-Column** | 10pt Times, US Letter | **8 Pages** (Max main body) | Unlimited (after p.8) | **Double-Blind** (Strip metadata & repo links) | ❌ Content past p.8 before references |
| **`ACL` / `ARR`** | Association for Computational Linguistics | **Two-Column** | 11pt Times, A4 Paper | **8 Pages** (Long) / **4 Pages** (Short) | Unlimited (after p.8/4) + Ethics | **Double-Blind** (Mask model/prompt identifiers) | ❌ Body overflow past page 8 or page 4 |
| **`ACM`** | ACM Computing Surveys / SIGKDD | **Two-Column** | 10pt Libertine, US Letter | **10–12 Pages** (Survey) / **9 Pages** (Conf) | Included in page budget | Single / Double-Blind depending on track | ❌ Orphan 1-paragraph final page |
| **`arXiv`** | arXiv Preprint Server | **Single or Two-Col** | Flexible (10pt standard) | **Flexible** (Recommended 4–15 pages) | Included | Single-Blind | ❌ TeX compilation errors / missing BibTeX |
| **`Nature` / `Springer`** | Nature Portfolio / Springer Nature | **Single-Column** | 10pt Computer Modern, A4 | **3,000–5,000 Words** (~6–10 pages) | Max 50 references | Single / Double-Blind | ❌ Word count overflow or citation format mismatch |

---

## 🔍 Detailed Venue Specifications & Rules

### 1. IEEEtran (IEEE Transactions & Short Conference Papers)
* **LaTeX Class:** `\documentclass[10pt,journal,compsoc,twocolumn]{IEEEtran}`
* **Page Budget Rule:** Camera-ready short papers must be **EXACTLY 4 PAGES**.
  * **3-Page Underflow Defect:** A 3-page manuscript leaves 1.5 columns of unutilized whitespace.
  * **5-Page Overflow Defect:** Spilling 3–10 lines onto page 5 causes immediate automated rejection.
* **Vertical Compression Strategy:** Use `\setlength{\parskip}{0pt}`, `\setlength{\parsep}{0pt}`, `\setlength{\topsep}{2pt plus 1pt}`, and `\setlength{\itemsep}{1pt}`.
* **Math Protection:** Wrap all inline math inside bullet items with `\mbox{$...$}` to prevent pdflatex from breaking math symbols vertically across lines.

### 2. NeurIPS (Neural Information Processing Systems)
* **LaTeX Class:** `\documentclass{article}` with `\usepackage[final]{neurips_2026}`
* **Page Budget Rule:** Main text (Sections 1 through 10) must fit within **9 pages**. References and the mandatory NeurIPS Paper Checklist start on page 10 and do not count toward the 9-page limit.
* **Anonymization:** Double-blind mandatory. Must replace author names with `Anonymous Authors` and remove all self-identifying grant numbers or internal repo links.

### 3. ICML (International Conference on Machine Learning)
* **LaTeX Class:** `\documentclass{article}` with `\usepackage{icml2026}`
* **Page Budget Rule:** Main text limit is **8 pages**. References and appendices are unlimited and start after page 8.
* **Layout:** Two-column format. Figures and tables must not cross column margins unless using `table*` or `figure*`.

### 4. CVPR (IEEE/CVF Conference on Computer Vision)
* **LaTeX Class:** `\documentclass[10pt,twocolumn,letterpaper]{article}` with `\usepackage{cvpr}`
* **Page Budget Rule:** **8 pages** maximum for main content. References begin on page 9.
* **Anonymization:** Double-blind. Rulers and line numbers are enabled during review mode.

### 5. ACL / ARR (ACL Rolling Review)
* **LaTeX Class:** `\documentclass[11pt,a4paper]{article}` with `\usepackage[review]{acl}`
* **Page Budget Rule:** Long papers: **8 pages**. Short papers: **4 pages**.
* **Special Requirement:** Requires an explicit *Limitations* section and an optional *Ethics Statement* after the main body.

### 6. ACM (ACM Computing Surveys / SIGKDD)
* **LaTeX Class:** `\documentclass[10pt,twocolumn,letterpaper]{article}`
* **Page Budget Rule:** Surveys target **10–12 pages**. Must avoid orphan spill pages where the final page contains fewer than 15 lines of text.

---

## 🛡️ Anti-Desk-Rejection Checklist (Zero-Defect Prevention)

1. **Page Budget Strictness:**
   - **IEEEtran Camera-Ready:** Target **exactly 4.0 pages** (100% column density on page 4).
   - **NeurIPS / ICML / CVPR / ACL:** Main body text must terminate before the page limit boundary before references begin.
2. **Inline Math Protection:**
   - Every inline math expression inside `\item` bullet points MUST be wrapped with `\mbox{$...$}` so pdflatex never stacks math characters vertically.
3. **Bibliography Cleanliness:**
   - No stray spaces before commas or periods (`Free Press,` NOT `Free Press ,`).
   - Every inline `\cite{}` must resolve to a valid numeric `[1]` or `[2]` entry (no `[?]` artifacts).
4. **Abstract & Title Typography:**
   - Zero raw Markdown syntax (`**bold**` or `*italic*`) leaking into the compiled PDF abstract or section headings.
5. **Fail-Closed Evidence Auditor Gate:**
   - All numeric percentage metrics must either be backed by cited empirical sources or expressed in qualitative academic prose to prevent HTTP 422/500 release gate blocks.

---

*Document stored in vault system for persistent cross-agent retrieval.*
