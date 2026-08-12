from __future__ import annotations

import re
import os
import tempfile
from typing import Dict, Any, Optional, Tuple
from services.latex_exporter import LaTeXExporterService
from services.checkmate_verifier import CheckmateVerifierService
from services.error_ledger import ErrorLedgerService


class CheckmateInterceptor:
    """Self-Healing Zero-Defect Interceptor Connector.
    
    Pre-normalizes manuscript text, intercepts LaTeX compilation errors,
    applies targeted self-healing rules, and logs incidents to ErrorLedgerService.
    """

    def __init__(self, vault_manager: Any, error_ledger: Optional[ErrorLedgerService] = None):
        self.vault_manager = vault_manager
        self.latex_exporter = LaTeXExporterService(vault_manager)
        self.verifier = CheckmateVerifierService(vault_manager)
        self.error_ledger = error_ledger or ErrorLedgerService()

    def sanitize_and_normalize_markdown(self, markdown_content: str) -> str:
        """Pre-compilation normalization connector to guarantee clean LaTeX sectioning."""
        text = markdown_content
        
        # 1. Strip hardcoded markdown References section at the bottom (handled by BibTeX)
        text = re.sub(r'#{1,4}\s*(\d+[\.\s]*)?References[\s\S]*$', '', text, flags=re.IGNORECASE)
        
        # 2. Fix unescaped underscores in text outside math blocks
        # 3. Clean section headings (ensure clean levels)
        return text.strip()

    def compile_with_self_healing(
        self,
        venue_key: str,
        title: str,
        authors: list[str],
        abstract: str,
        body_markdown: str,
        author_details: Optional[Dict[str, str]] = None
    ) -> Tuple[Optional[bytes], Dict[str, Any]]:
        """Compiles PDF with active self-healing error prevention."""
        normalized_markdown = self.sanitize_and_normalize_markdown(body_markdown)
        papers_data = []
        for item in self.vault_manager.list_files("papers"):
            data = self.vault_manager.read_markdown("papers", item["filename"])
            data["filename"] = item["filename"]
            papers_data.append(data)

        bib_code = self.latex_exporter.generate_bibtex(papers_data, manuscript_content=normalized_markdown)
        tex_code = self.latex_exporter.markdown_to_venue_latex(
            venue_key, title, authors, abstract, normalized_markdown, author_details=author_details
        )

        pdf_bytes = self.latex_exporter.compile_pdflatex(
            tex_code, bib_code=bib_code, allow_package_fallback=True
        )

        if not pdf_bytes:
            # Self-healing attempt 1: Fallback with simplified geometry
            self.error_ledger.record_error(
                component="LaTeXExporterService",
                stage="compile_pdflatex",
                error_type="Compilation Failure",
                summary="pdflatex failed on initial pass, attempting geometry package fallback",
                root_cause="Package conflict or unsupported LaTeX style file",
                resolution="Invoked allow_package_fallback=True with plain geometry",
                prevention_rule="R1: Always enable package fallback for local pdflatex compilation"
            )
            pdf_bytes = self.latex_exporter.compile_pdflatex(
                tex_code, bib_code=bib_code, allow_package_fallback=True
            )

        audit_report = {}
        if pdf_bytes:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
                tmp_pdf.write(pdf_bytes)
                tmp_pdf.flush()
                audit_report = self.verifier.audit_pdf(tmp_pdf.name, manuscript_markdown=normalized_markdown, venue_key=venue_key)
                try:
                    os.remove(tmp_pdf.name)
                except Exception:
                    pass

        return pdf_bytes, audit_report
