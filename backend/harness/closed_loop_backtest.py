"""Controlled, fail-closed manuscript backtest loop.

The loop borrows the useful part of autonomous optimization harnesses: a fixed
evaluation surface, a bounded candidate budget, and explicit keep/discard
decisions. Manuscript text is the only mutable candidate; venue contracts,
evidence checks, and the evaluator remain outside the remediation surface.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

from services.backtest_ledger import BacktestLedger
from services.fact_checker import FactCheckerService
from services.latex_exporter import LaTeXExporterService
from services.publisher_readiness import PublisherReadinessService
from services.visual_auditor import VisualLayoutAuditorService


class ClosedLoopBacktestHarness:
    """Run bounded, evidence-aware candidate iterations for one manuscript/venue."""

    def __init__(self, vault_manager: Any):
        self.vault_manager = vault_manager
        self.latex_exporter = LaTeXExporterService(vault_manager)
        self.visual_auditor = VisualLayoutAuditorService(vault_manager)
        self.fact_checker = FactCheckerService(vault_manager)
        self.publisher_readiness = PublisherReadinessService(vault_manager)
        self.ledger = BacktestLedger(vault_manager)

    @staticmethod
    def _rank(audit: Dict[str, Any], originality: bool, value: bool, evidence: bool) -> tuple:
        failed = len(audit.get("failed_checks", []))
        failures = failed + int(not originality) + int(not value) + int(not evidence)
        return (failures, -float(audit.get("score", 0.0)))

    def _sources(self) -> tuple[List[Dict[str, Any]], List[str], Dict[str, str]]:
        papers: List[Dict[str, Any]] = []
        paper_folder = getattr(self.vault_manager, "folders", {}).get("papers")
        paper_names = sorted(
            name for name in os.listdir(paper_folder or "") if name.endswith(".md")
        ) if paper_folder else []
        for paper_name in paper_names:
            try:
                data = self.vault_manager.read_markdown("papers", paper_name)
                data["filename"] = paper_name
                papers.append(data)
            except Exception:
                continue
        texts: List[str] = []
        records: Dict[str, str] = {}
        for paper in papers:
            text = paper.get("content", "")
            texts.append(text)
            metadata = paper.get("frontmatter", {}) or paper.get("metadata", {}) or {}
            for key in (paper.get("filename", ""), metadata.get("id", ""), metadata.get("title", "")):
                if key:
                    records[str(key)] = text
        return papers, texts, records

    def _research_quality(self, filename: str, content: str, all_documents: Dict[str, str],
                          source_texts: List[str], source_records: Dict[str, str]) -> Dict[str, Any]:
        documents = dict(all_documents)
        documents[filename] = content
        originality = self.publisher_readiness.audit_collection_originality(documents)
        value = self.publisher_readiness.audit_substantive_value(content)
        evidence = self.fact_checker.audit_document(content, source_texts=source_texts, source_records=source_records)
        original = originality.get("per_file", {}).get(filename, {"passed": True, "status": "PASS"})
        return {
            "originality": original,
            "value": value,
            "evidence": evidence,
            "originality_passed": bool(original.get("passed", False)),
            "value_passed": bool(value.get("substantive_value_passed", False)),
            "evidence_passed": evidence.get("status") == "passed" and not evidence.get("blocking_errors"),
        }

    def run_closed_loop(self, filename: str, venue_key: str = "IEEEtran", max_iters: int = 3) -> Dict[str, Any]:
        clean_filename = filename if filename.endswith(".md") else f"{filename}.md"
        doc = self.vault_manager.read_markdown("drafts", clean_filename)
        original_content = doc.get("content", "")
        meta = doc.get("frontmatter", {}) or {}
        title = meta.get("title", clean_filename.replace(".md", ""))
        authors = meta.get("authors") or ["Aryaman Singh Dev"]
        author_details = {
            "affiliation": meta.get("affiliation", "Pennsylvania State University"),
            "email": meta.get("email", "asd5520@psu.edu"),
        }

        all_documents: Dict[str, str] = {}
        for item in self.vault_manager.list_files("drafts"):
            try:
                all_documents[item["filename"]] = self.vault_manager.read_markdown("drafts", item["filename"]).get("content", "")
            except Exception:
                continue
        papers, source_texts, source_records = self._sources()
        run = self.ledger.start(filename=clean_filename, venue=venue_key, baseline_content=original_content, max_iters=max_iters)

        best_content = original_content
        best_audit: Dict[str, Any] = {}
        best_rank: Optional[tuple] = None
        history: List[Dict[str, Any]] = []
        current = original_content
        reason = "maximum iteration budget exhausted"

        for iteration in range(1, max_iters + 1):
            quality = self._research_quality(clean_filename, current, all_documents, source_texts, source_records)
            bib_code = self.latex_exporter.generate_bibtex(papers, manuscript_content=current)
            tex_code = self.latex_exporter.markdown_to_venue_latex(
                venue_key, title, authors, "Executive Abstract", current, author_details=author_details,
            )
            pdf_bytes = self.latex_exporter.compile_pdflatex(tex_code, bib_code=bib_code, allow_package_fallback=True)
            if pdf_bytes:
                pdf_name = f"{clean_filename.replace('.md', '')}_{venue_key}.pdf"
                pdf_path = os.path.join(self.vault_manager.vault_path, "04_Drafts", pdf_name)
                with open(pdf_path, "wb") as handle:
                    handle.write(pdf_bytes)
                audit = self.visual_auditor.audit_full_manuscript(
                    pdf_path, current, venue_key=venue_key,
                    tile_output_dir=os.path.join(self.vault_manager.vault_path, "04_Drafts", "preview_tiles"),
                    tex_source=tex_code,
                    package_fallback_used=self.latex_exporter.last_compile_used_package_fallback,
                    evidence_report=quality["evidence"],
                )
                audit["failed_checks"] = [
                    name for name, check in audit.get("checkmate_checks", {}).items() if not check.get("passed", False)
                ]
            else:
                audit = {
                    "score": 0.0,
                    "checkmate_passed": False,
                    "failed_checks": ["latex_compile"],
                    "compile_diagnostics": self.latex_exporter.last_build_log[-2000:],
                }

            candidate_rank = self._rank(audit, quality["originality_passed"], quality["value_passed"], quality["evidence_passed"])
            accepted = best_rank is None or candidate_rank < best_rank
            if accepted:
                best_rank, best_content, best_audit = candidate_rank, current, audit
            passed = bool(audit.get("checkmate_passed") and quality["originality_passed"] and quality["value_passed"] and quality["evidence_passed"])
            decision = "keep" if accepted else "discard"
            if passed:
                reason = "all immutable publication gates passed"
            history.append({
                "iteration": iteration,
                "score": audit.get("score", 0.0),
                "passed": passed,
                "decision": decision,
                "candidate_sha256": self.ledger.content_hash(current),
                "research_quality": {
                    "originality_passed": quality["originality_passed"],
                    "substantive_value_passed": quality["value_passed"],
                    "evidence_status": quality["evidence"].get("status"),
                },
                "failed_checks": audit.get("failed_checks", []),
            })
            self.ledger.record(run["run_id"], iteration=iteration, stage="evaluate", status=decision, content=current, details=history[-1])
            if passed or iteration == max_iters:
                break

            candidate = self._apply_remediation_nodes(current, audit)
            if candidate == current:
                reason = "remediation produced no candidate change"
                self.ledger.record(run["run_id"], iteration=iteration, stage="remediate", status="blocked", content=current, details={"reason": reason})
                break
            self.ledger.record(run["run_id"], iteration=iteration, stage="remediate", status="candidate_created", content=candidate, details={"from_sha256": self.ledger.content_hash(current)})
            current = candidate

        converged = bool(history and history[-1].get("passed"))
        if best_content != original_content:
            self.vault_manager.save_markdown("drafts", clean_filename, best_content, frontmatter=meta)
        if converged:
            meta.update({"checkmate_score": str(best_audit.get("score", 0.0)), "checkmate_status": "PASSED"})
            self.vault_manager.save_markdown("drafts", clean_filename, best_content, frontmatter=meta)
        final_status = "CONVERGED" if converged else "BLOCKED"
        manifest = self.ledger.finish(run["run_id"], status=final_status, final_content=best_content, iterations=len(history), reason=reason)
        return {
            "converged": converged,
            "iterations": len(history),
            "final_score": best_audit.get("score", 0.0),
            "audit": best_audit,
            "history": history,
            "run_id": run["run_id"],
            "ledger_manifest": manifest,
            "release_reason": reason,
        }

    def _apply_remediation_nodes(self, markdown_text: str, audit_res: Dict[str, Any]) -> str:
        text = markdown_text
        text = re.sub(r'\\cite\{([^}]+)\}', lambda m: "\\cite{" + ",".join(k.strip() for k in m.group(1).split(",")) + "}", text)
        text = re.sub(r'\b(In summary|Summary|Conclusion|Abstract|References)\s*\1\b', r'\1', text)
        if not re.search(r'#+\s*(?:Executive\s+)?Abstract', text, re.IGNORECASE):
            text = "# Executive Abstract\n\n" + text
        return text

    def run_multi_venue_backtest(self, target_filename: Optional[str] = None, venues: Optional[List[str]] = None) -> Dict[str, Any]:
        """Use the canonical all-draft/all-venue readiness matrix."""
        return self.publisher_readiness.run(target_filename=target_filename, venues=venues)
