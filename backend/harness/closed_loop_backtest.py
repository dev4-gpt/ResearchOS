import os, re
from typing import Dict, Any, List
from services.latex_exporter import LaTeXExporterService
from services.visual_auditor import VisualLayoutAuditorService

class ClosedLoopBacktestHarness:
    """Autonomous Self-Healing DAG Graph Harness for ResearchingOS PDF Quality Control."""

    def __init__(self, vault_manager):
        self.vault_manager = vault_manager
        self.latex_exporter = LaTeXExporterService(vault_manager)
        self.visual_auditor = VisualLayoutAuditorService(vault_manager)

    def run_closed_loop(self, filename: str, venue_key: str = "IEEEtran", max_iters: int = 3) -> Dict[str, Any]:
        """Executes the closed-loop self-healing DAG graph until 100.0 Checkmate Score is achieved."""
        clean_filename = filename if filename.endswith(".md") else f"{filename}.md"
        doc = self.vault_manager.read_markdown("drafts", clean_filename)
        content = doc.get("content", "")
        meta = doc.get("frontmatter", {}) or {}
        title = meta.get("title", clean_filename.replace(".md", ""))
        authors = meta.get("authors") or ["Aryaman Singh Dev"]
        author_details = {"affiliation": "Pennsylvania State University", "email": "asd5520@psu.edu"}

        papers_data = []
        for p in self.vault_manager.list_files("papers"):
            try: papers_data.append(self.vault_manager.read_markdown("papers", p["filename"]))
            except Exception: pass

        current_markdown = content
        iteration_history = []

        for iteration in range(1, max_iters + 1):
            # Step 1: Re-compile LaTeX PDF
            bib_code = self.latex_exporter.generate_bibtex(papers_data, manuscript_content=current_markdown)
            tex_code = self.latex_exporter.markdown_to_venue_latex(venue_key, title, authors, "Executive Abstract", current_markdown, author_details=author_details)
            pdf_bytes = self.latex_exporter.compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)

            if not pdf_bytes:
                iteration_history.append({"iteration": iteration, "status": "COMPILATION_FAILED"})
                break

            # Save PDF to disk
            pdf_name = f"{clean_filename.replace('.md', '')}_{venue_key}.pdf"
            pdf_path = os.path.join(self.vault_manager.vault_path, "04_Drafts", pdf_name)
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            tile_dir = os.path.join(self.vault_manager.vault_path, "04_Drafts", "preview_tiles")
            audit_res = self.visual_auditor.audit_full_manuscript(pdf_path, current_markdown, venue_key=venue_key, tile_output_dir=tile_dir)
            score = audit_res.get("score", 0.0)
            passed = audit_res.get("checkmate_passed", False)

            iteration_history.append({
                "iteration": iteration,
                "score": score,
                "passed": passed,
                "total_pages": audit_res.get("total_pages", 0)
            })

            # Convergence check
            if passed and score >= 100.0:
                meta["checkmate_score"] = str(score)
                meta["checkmate_status"] = "PASSED"
                meta["checkmate_date"] = audit_res.get("certificate", {}).get("timestamp", "")
                self.vault_manager.save_markdown("drafts", clean_filename, current_markdown, frontmatter=meta)
                return {
                    "converged": True,
                    "iterations": iteration,
                    "final_score": score,
                    "audit": audit_res,
                    "history": iteration_history
                }

            # Remediate manuscript markdown if not converged
            current_markdown = self._apply_remediation_nodes(current_markdown, audit_res)

        # Final save if maximum iterations reached
        self.vault_manager.save_markdown("drafts", clean_filename, current_markdown, frontmatter=meta)
        return {
            "converged": False,
            "iterations": max_iters,
            "final_score": iteration_history[-1].get("score", 0) if iteration_history else 0,
            "audit": audit_res,
            "history": iteration_history
        }

    def _apply_remediation_nodes(self, markdown_text: str, audit_res: Dict[str, Any]) -> str:
        """Remediates markdown text based on identified defect patterns."""
        text = markdown_text

        # Node 1: Fix citation block whitespace
        text = re.sub(r'\\cite\{([^}]+)\}', lambda m: "\\cite{" + ",".join(k.strip() for k in m.group(1).split(",")) + "}", text)

        # Node 2: Fix duplicated section phrases
        text = re.sub(r'\b(In summary|Summary|Conclusion|Abstract|References)\s*\1\b', r'\1', text)

        # Node 3: Ensure Executive Abstract heading exists
        if not re.search(r'#+\s*(?:Executive\s+)?Abstract', text, re.IGNORECASE):
            text = "# Executive Abstract\n\n" + text

        return text
