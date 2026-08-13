# ResearchOS System Error Ledger & Prevention Manual

**Last Updated**: 2026-08-13 15:28:59  
**Total Errors Recorded & Resolved**: 12 / 12  
**Active Systemic Prevention Rules**: 12

---

## 🛡️ Active Systemic Prevention Rules

- **[R1]**: All PDF compilation endpoints must invoke compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)
- **[R2]**: PDF export route must return binary Response with application/pdf Content-Type
- **[R3]**: Strip all leading numerical prefixes from markdown section titles before converting to LaTeX \section
- **[R4]**: Automatically filter out hardcoded markdown References sections prior to appending LaTeX \bibliography
- **[R5]**: Enforce strict 4-page layout auditing for camera-ready IEEEtran submissions
- **[R6]**: R6: Provide safe \providecommand fallback definitions for venue-specific custom macros in all LaTeX templates
- **[R7]**: R7: Always place \begin{document} immediately after preamble packages and before \title and \maketitle
- **[R8]**: R8: Automatically convert Markdown bold (**text**) and italic (*text*) syntax into LaTeX \textbf and \textit
- **[R9]**: R9: Check for existing egin{ environments in wrap_display_math and ensure all equations in manuscripts are fully closed
- **[R10]**: R10: All cited keys must map to real paper metadata in vault/01_Papers/ or KNOWN_CITATIONS; synthetic fallback titles are forbidden
- **[R11]**: R11: Always complete multi-pass pdflatex + bibtex compilation and return non-empty document.pdf bytes if generated
- **[R12]**: R12: Explicitly re-raise HTTPException before generic catch-all handlers to preserve HTTP 422/404 status codes and error details

---

## 📜 Full Error History & Self-Healing Registry

### [ERR-001] Checkmate Audit Failed: Not Found due to missing route and compile_pdf method signature mismatch
- **Component / Stage**: `API / Backend Route` | `checkmate_audit`
- **Error Type**: `HTTP 404 / 500`
- **Root Cause**: latex_exporter lacked compile_pdf method and save_markdown had mismatched parameter ordering
- **Resolution**: Updated checkmate_audit to use compile_pdflatex and correct save_markdown argument order
- **Prevention Rule**: `R1: All PDF compilation endpoints must invoke compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-002] Download PDF returned PDF COMPILATION ERROR due to undefined 'verifier' variable and compile_pdf call
- **Component / Stage**: `LaTeX Exporter Service` | `export_venue_pdf`
- **Error Type**: `NameError & AttributeError`
- **Root Cause**: exporter.compile_pdf and verifier.audit_pdf used stale variable names
- **Resolution**: Replaced compile_pdf with compile_pdflatex and verifier with checkmate_verifier, streaming Response(content=pdf_bytes)
- **Prevention Rule**: `R2: PDF export route must return binary Response with application/pdf Content-Type`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-003] Section headings rendered as '1 1 EXECUTIVE ABSTRACT' due to LaTeX section counter appending to hardcoded markdown '1 '
- **Component / Stage**: `LaTeX Converter` | `section_heading_parsing`
- **Error Type**: `Double Section Numbering`
- **Root Cause**: heading_to_section regex skipped level 1 headings (# 1 ...), retaining leading digits
- **Resolution**: Updated heading_to_section to strip leading numbers (re.sub(r'^(\d+[\.\s]*)+', '', title)) across all heading levels
- **Prevention Rule**: `R3: Strip all leading numerical prefixes from markdown section titles before converting to LaTeX \section`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-004] Page 4 rendered two separate REFERENCES headings and duplicate reference lists
- **Component / Stage**: `Bibliography Generator` | `latex_compilation`
- **Error Type**: `Duplicate References Section`
- **Root Cause**: Markdown body ended with hardcoded ## References section alongside \bibliography{references}
- **Resolution**: Added regex stripping of hardcoded References sections in convert_markdown_body prior to LaTeX compilation
- **Prevention Rule**: `R4: Automatically filter out hardcoded markdown References sections prior to appending LaTeX \bibliography`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-005] Manuscript text spilled onto an orphan 5th page with only a few lines
- **Component / Stage**: `Layout & Page Fit` | `pdf_layout_audit`
- **Error Type**: `Orphan Page 5 Spillover`
- **Root Cause**: Uncalibrated markdown text volume caused minor overflow past the 4-page camera-ready limit
- **Resolution**: Tuned section text density so the document fills exactly 4 full pages with zero orphan spillover
- **Prevention Rule**: `R5: Enforce strict 4-page layout auditing for camera-ready IEEEtran submissions`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-006] pdflatex failed on ICML template fallback due to undefined \icmltitle macro
- **Component / Stage**: `LaTeX Exporter / ICML` | `pdflatex_compilation`
- **Error Type**: `Undefined Macro Error`
- **Root Cause**: ICML template used custom style macros that were undefined when geometry package fallback was triggered
- **Resolution**: Added preamble \providecommand fallback macros for \icmltitle, \icmlauthor, \icmlaffiliation, and \icmlkeywords
- **Prevention Rule**: `R6: R6: Provide safe \providecommand fallback definitions for venue-specific custom macros in all LaTeX templates`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-007] pdflatex failed on ACL template with '! LaTeX Error: Missing \begin{document}'
- **Component / Stage**: `LaTeX Exporter / ACL` | `template_assembly`
- **Error Type**: `Document Boundary Error`
- **Root Cause**: ACL template placed \title, \author, and \maketitle prior to \begin{document}
- **Resolution**: Re-ordered ACL template to place \begin{document} before \title, \author, and \maketitle
- **Prevention Rule**: `R7: R7: Always place \begin{document} immediately after preamble packages and before \title and \maketitle`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-008] Abstract rendered literal ** double asterisks around keywords
- **Component / Stage**: `LaTeX Exporter / Abstract Sanitizer` | `abstract_rendering`
- **Error Type**: `Raw Markdown Asterisk Leakage`
- **Root Cause**: sanitize_latex escaped special characters but did not convert markdown bold **text** to LaTeX \textbf{text}
- **Resolution**: Added regex conversion re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', clean_abstract)
- **Prevention Rule**: `R8: R8: Automatically convert Markdown bold (**text**) and italic (*text*) syntax into LaTeX \textbf and \textit`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-009] pdflatex compilation failed with ! LaTeX Error: egin{equation} ended by \end{document}
- **Component / Stage**: `LaTeX Exporter / Math Sanitizer` | `pdflatex_compilation`
- **Error Type**: `LaTeX Math Environment Error`
- **Root Cause**: Truncated math equation on line 100 and double equation wrapping in wrap_display_math
- **Resolution**: Repaired equation line and updated wrap_display_math to check for existing egin{ environments
- **Prevention Rule**: `R9: Check for existing egin{ environments in wrap_display_math and ensure all equations in manuscripts are fully closed`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-010] Checkmate audit failed real_bibliography check (score 85.7%) due to synthetic placeholder strings in references
- **Component / Stage**: `Bibliography Generator` | `checkmate_audit`
- **Error Type**: `Synthetic Placeholder Violation`
- **Root Cause**: generate_bibtex generated Foundational Research Study: ... and Journal of Enterprise AI Infrastructure fallbacks for unmapped keys
- **Resolution**: Mapped all keys in KNOWN_CITATIONS and purged synthetic fallback strings in generate_bibtex
- **Prevention Rule**: `R10: All cited keys must map to real paper metadata in vault/01_Papers/ or KNOWN_CITATIONS; synthetic fallback titles are forbidden`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-011] Download PDF button returned PDF compilation error alert even when document.pdf was successfully created
- **Component / Stage**: `LaTeX Exporter / pdflatex Pipeline` | `export_venue_pdf`
- **Error Type**: `Premature Abort on Pass 1 Warning`
- **Root Cause**: compile_pdflatex checked if first.returncode != 0 and returned None prematurely before bibtex and pass 2/3 ran
- **Resolution**: Removed premature pass 1 exit code check; compile_pdflatex now completes all passes and returns compiled PDF bytes if document.pdf exists
- **Prevention Rule**: `R11: Always complete multi-pass pdflatex + bibtex compilation and return non-empty document.pdf bytes if generated`
- **Status**: `VERIFIED_RESOLVED`

### [ERR-012] export_venue_pdf wrapped HTTPException(422) inside a generic except Exception as e: block, converting validation errors into HTTP 500 crashes
- **Component / Stage**: `Backend API / Main Routes` | `error_handling`
- **Error Type**: `HTTP 500 Swallowing HTTPException`
- **Root Cause**: Lack of explicit except HTTPException: re-raise block before generic catch-all exception handler
- **Resolution**: Added except HTTPException: raise explicitly to all FastAPI endpoints
- **Prevention Rule**: `R12: Explicitly re-raise HTTPException before generic catch-all handlers to preserve HTTP 422/404 status codes and error details`
- **Status**: `VERIFIED_RESOLVED`

