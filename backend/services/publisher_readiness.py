"""Fail-closed publisher readiness checks for the HITL Publisher.

This service keeps formatting checks and research-quality checks separate. A PDF can
be perfectly typeset and still be a duplicate, a stub, or too weak to submit. The
publisher gate therefore reports both kinds of evidence and only marks a venue
ready when every required gate passes.
"""

from __future__ import annotations

import hashlib
import json
import re
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Set

from services.checkmate_verifier import CheckmateVerifierService
from services.fact_checker import FactCheckerService
from services.latex_exporter import LaTeXExporterService
from services.venue_profiles import SUPPORTED_VENUES, VENUE_PROFILES
from services.backtest_ledger import BacktestLedger
from services.publication_harness import (
    EvaluationStageEvent, PublicationEvaluationConfig, PublicationRunState, PublicationStage,
    evaluator_source_hash, new_run_id, reproducibility_snapshot, stable_hash, venue_registry_hash,
)
from domain.models import citation_key


# New venue profiles automatically enter the all-venue readiness run. Each new
# profile must still provide an exporter and explicit venue contract to pass.
DEFAULT_PUBLISHER_VENUES = list(SUPPORTED_VENUES)

PLACEHOLDER_PATTERNS = (
    r"\bTBD\b",
    r"\[\?\]",
    r"to be expanded",
    r"unspecified authors",
    r"insert (?:results|citation|reference)",
)


class PublisherReadinessService:
    """Run the complete manuscript-by-venue release matrix."""

    def __init__(self, vault_manager: Any, config: Optional[PublicationEvaluationConfig] = None):
        self.vault_manager = vault_manager
        self._root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        source_hash = evaluator_source_hash(self._root)
        profile_hash = venue_registry_hash(VENUE_PROFILES)
        self.config = (config or PublicationEvaluationConfig()).with_hashes(
            source_hash=source_hash, venue_profile_hash=profile_hash,
        )
        self.ledger = BacktestLedger(vault_manager)
        self.checkmate = CheckmateVerifierService(vault_manager)
        self.fact_checker = FactCheckerService(vault_manager)
        self.exporter = LaTeXExporterService(vault_manager)

    @staticmethod
    def _body_for_comparison(content: str) -> str:
        """Normalize prose while retaining enough structure to catch copy/paste."""
        body = re.sub(r"```[\s\S]*?```", " ", content)
        body = re.sub(r"\$\$[\s\S]*?\$\$", " equation ", body)
        body = re.sub(r"\\begin\{[^}]+\}[\s\S]*?\\end\{[^}]+\}", " equation ", body)
        # The title is identity metadata, not research prose. Excluding the first
        # heading catches duplicate manuscripts exported under different titles.
        body = re.sub(r"^#\s+.*?$", " ", body, count=1, flags=re.M)
        # Bibliographies are intentionally excluded from similarity: shared sources
        # are normal, while copied prose and methods are not.
        body = re.split(r"^#{1,6}\s*(?:references|bibliography)\s*$", body, maxsplit=1, flags=re.I | re.M)[0]
        body = re.sub(r"[^a-zA-Z0-9%]+", " ", body.lower())
        return re.sub(r"\s+", " ", body).strip()

    @staticmethod
    def _tokens(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())

    @classmethod
    def _shingles(cls, text: str, size: int = 5) -> Set[str]:
        tokens = cls._tokens(text)
        if len(tokens) < size:
            return set()
        return {" ".join(tokens[i:i + size]) for i in range(len(tokens) - size + 1)}

    @staticmethod
    def _section_names(content: str) -> List[str]:
        return [m.group(1).strip().lower() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", content, re.M)]

    @classmethod
    def audit_substantive_value(cls, content: str, min_words: int = 450) -> Dict[str, Any]:
        """Check for a real research contribution, not just clean formatting."""
        normalized = cls._body_for_comparison(content)
        words = cls._tokens(normalized)
        headings = cls._section_names(content)
        lower = content.lower()

        citation_count = len(re.findall(r"\[[0-9]{1,3}\]|\([a-z][a-z-]+(?: et al\.)?,?\s*20\d{2}[a-z]?\)", lower))
        citation_count += len(re.findall(r"\\(?:cite|citep|citet|parencite)\s*(?:\[[^\]]*\])?\{[^}]+\}", lower))
        citation_count += len(re.findall(r"\[\[[^\]]+\]\]", content))
        numeric_claim_count = len(re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|ms|s|x|million|billion)?\b", lower))
        equation_count = len(re.findall(r"\$\$|\\begin\{(?:equation|align|aligned)\}", content))

        contribution = bool(re.search(
            r"\b(contribution|contribute|novel|we present|we propose|we develop|we introduce|our findings|our results|our framework)\b",
            lower,
        )) or any("contribution" in heading or "novel" in heading for heading in headings)
        evidence_or_synthesis = bool(re.search(
            r"\b(empirical|experiment|evaluation|benchmark|dataset|ablation|measurement|results?|finding|systematic review|prisma|meta-analysis|synthesis|taxonomy)\b",
            lower,
        ))
        method_or_scope = bool(re.search(
            r"\b(methodology|method|approach|protocol|algorithm|procedure|search strategy|inclusion criteria|research question)\b",
            lower,
        ))
        limitations = bool(re.search(r"\b(limitation|threats? to validity|boundary|caveat|future work)\b", lower))
        grounded = citation_count >= 3 or len(re.findall(r"^\s*\[?\d{1,3}\]?\s+.+$", content, re.M)) >= 3
        no_stub = not any(re.search(pattern, lower) for pattern in PLACEHOLDER_PATTERNS)

        checks = {
            "minimum_substance": {
                "passed": len(words) >= min_words,
                "detail": f"{len(words):,} normalized words (minimum {min_words})",
            },
            "explicit_contribution": {
                "passed": contribution,
                "detail": "Contribution or original claim is stated" if contribution else "No explicit contribution/novelty claim found",
            },
            "evidence_or_synthesis": {
                "passed": evidence_or_synthesis,
                "detail": "Evidence, evaluation, or structured synthesis is present" if evidence_or_synthesis else "No evidence, evaluation, or synthesis signal found",
            },
            "method_or_scope": {
                "passed": method_or_scope,
                "detail": "Method, protocol, or review scope is described" if method_or_scope else "Method or review scope is not explicit",
            },
            "grounded_references": {
                "passed": grounded,
                "detail": f"At least 3 citation/reference signals ({citation_count} inline citations)" if grounded else "Fewer than 3 citation/reference signals",
            },
            "limitations_or_boundary": {
                "passed": limitations,
                "detail": "Limitations or applicability boundary is stated" if limitations else "Limitations/boundaries are not stated",
            },
            "no_placeholder_stub": {
                "passed": no_stub,
                "detail": "No manuscript placeholder language detected" if no_stub else "Placeholder language detected",
            },
        }
        # A paper must state what it adds and ground that value in evidence or a
        # reproducible synthesis. Limitations and method are required for release,
        # but remain visible as individual checks when the paper is blocked.
        substantive_value_passed = all(checks[key]["passed"] for key in (
            "minimum_substance", "explicit_contribution", "evidence_or_synthesis",
            "method_or_scope", "grounded_references", "limitations_or_boundary", "no_placeholder_stub",
        ))
        score = round(sum(1 for check in checks.values() if check["passed"]) / len(checks) * 100, 1)
        return {
            "score": score,
            "substantive_value_passed": substantive_value_passed,
            "status": "PASS" if substantive_value_passed else "NEEDS_REVIEW",
            "metrics": {
                "word_count": len(words),
                "section_count": len(headings),
                "citation_signal_count": citation_count,
                "numeric_claim_count": numeric_claim_count,
                "equation_count": equation_count,
            },
            "checks": checks,
        }

    def audit_collection_originality(self, documents: Dict[str, str], max_ngram_overlap: float = 65.0, review_overlap: float = 35.0) -> Dict[str, Any]:
        """Detect exact duplicates and high copied-prose overlap across drafts."""
        normalized = {name: self._body_for_comparison(content) for name, content in documents.items()}
        hashes = {name: hashlib.sha256(text.encode("utf-8")).hexdigest() for name, text in normalized.items()}
        shingles = {name: self._shingles(text) for name, text in normalized.items()}
        pairs: List[Dict[str, Any]] = []
        max_overlap = 0.0
        names = sorted(normalized)

        for index, left in enumerate(names):
            for right in names[index + 1:]:
                left_shingles, right_shingles = shingles[left], shingles[right]
                union = left_shingles | right_shingles
                overlap = (len(left_shingles & right_shingles) / len(union) * 100) if union else 0.0
                exact = hashes[left] == hashes[right] and bool(normalized[left])
                max_overlap = max(max_overlap, overlap)
                if exact or overlap >= review_overlap:
                    pairs.append({
                        "file_1": left,
                        "file_2": right,
                        "exact_duplicate": exact,
                        "five_gram_overlap_pct": round(overlap, 1),
                        "severity": "BLOCK" if exact or overlap >= max_ngram_overlap else "REVIEW",
                    })

        blocked_files: Set[str] = set()
        for pair in pairs:
            if pair["severity"] == "BLOCK":
                blocked_files.update((pair["file_1"], pair["file_2"]))

        per_file = {}
        for name in names:
            related = [pair for pair in pairs if name in (pair["file_1"], pair["file_2"])]
            file_max = max((pair["five_gram_overlap_pct"] for pair in related), default=0.0)
            per_file[name] = {
                "exact_duplicate": name in blocked_files and any(pair["exact_duplicate"] and name in (pair["file_1"], pair["file_2"]) for pair in related),
                "max_five_gram_overlap_pct": file_max,
                "passed": name not in blocked_files,
                "status": "PASS" if name not in blocked_files else "BLOCKED_DUPLICATE_CONTENT",
                "detail": "No high-overlap sibling manuscript detected" if name not in blocked_files else "High-overlap or exact-duplicate manuscript detected; separate this work before submission",
            }

        return {
            "passed": not blocked_files,
            "max_five_gram_overlap_pct": round(max_overlap, 1),
            "max_allowed_blocking_overlap_pct": max_ngram_overlap,
            "pairs": pairs,
            "per_file": per_file,
        }

    @staticmethod
    def _abstract(content: str) -> str:
        match = re.search(r"^#{1,6}\s*(?:\d+[.\s]*)?(?:executive\s+)?abstract\s*$([\s\S]*?)(?=^#{1,6}\s|\Z)", content, re.I | re.M)
        return match.group(1).strip() if match else "Executive Abstract"

    @staticmethod
    def _recorded_measurements(draft_filename: str) -> List[float]:
        """Values recorded by the experiment bound to this draft, if any."""
        import json as _json

        stem = draft_filename[:-3] if draft_filename.endswith(".md") else draft_filename
        path = os.path.join("runs", f"draft-{stem}", "measurements.jsonl")
        if not os.path.exists(path):
            return []
        values: List[float] = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = _json.loads(line)
                    values.append(float(row["value"]))
                    for bound in row.get("ci95") or []:
                        values.append(float(bound))
                    # The sample size is recorded evidence too, and manuscripts
                    # state it constantly -- "N = 64 agents", "n = 138 queries".
                    # Without it the fact checker blocked all 12 of p5's venues on
                    # "Unverified numeric claims: N = 64", a number carried by the
                    # n field of nine measurements whose metric names literally
                    # spell it (messages_at_n64_mesh, and so on).
                    if row.get("n") is not None:
                        values.append(float(row["n"]))
                except (ValueError, KeyError, TypeError):
                    continue

        # The run manifest is recorded evidence too. Each draft's Reproducibility
        # table states the run's wall-clock duration, seed and measurement count,
        # and those are facts about the run rather than claims about the world --
        # so they are absent from measurements.jsonl by design. Without them here,
        # FactCheckerService reported "Unverified numeric claims: 10.575 s" and
        # blocked all 12 venues for a number taken verbatim from the manifest,
        # while the provenance gate called the same manuscript fully grounded.
        # That is ERR-056 again: two graders judging one property against
        # different evidence, which is a defect in the graders (R56).
        manifest_path = os.path.join("runs", f"draft-{stem}", "experiment_manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as handle:
                    manifest = _json.load(handle)
                for field in ("duration_s", "seed", "measurement_count"):
                    value = manifest.get(field)
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        values.append(float(value))
            except (ValueError, OSError):
                pass
        return values

    @staticmethod
    def _recorded_measurement_records(draft_filename: str) -> List[Dict[str, Any]]:
        """Load measurement provenance rows and attach stable artifact hashes."""
        import json as _json
        from pathlib import Path as _Path
        stem = draft_filename[:-3] if draft_filename.endswith(".md") else draft_filename
        path = _Path("runs") / f"draft-{stem}" / "measurements.jsonl"
        if not path.exists():
            return []
        artifact_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        records: List[Dict[str, Any]] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = _json.loads(line)
            except (ValueError, TypeError):
                continue
            row["artifact_ref"] = str(path) + f":line:{line_number}"
            row["artifact_sha256"] = artifact_hash
            records.append(row)
        return records

    def run(self, target_filename: Optional[str] = None, venues: Optional[List[str]] = None,
            config: Optional[PublicationEvaluationConfig] = None,
            progress_callback: Optional[Any] = None, run_id: Optional[str] = None) -> Dict[str, Any]:
        requested_venues = venues or DEFAULT_PUBLISHER_VENUES
        test_venues = [venue for venue in requested_venues if venue in VENUE_PROFILES]
        if not test_venues:
            raise ValueError("No supported publication venues were requested.")

        draft_items = self.vault_manager.list_files("drafts")
        all_documents: Dict[str, str] = {}
        all_docs_meta: Dict[str, Dict[str, Any]] = {}
        for item in draft_items:
            filename = item["filename"]
            try:
                document = self.vault_manager.read_markdown("drafts", filename)
            except Exception:
                continue
            all_documents[filename] = document.get("content", "")
            all_docs_meta[filename] = document.get("frontmatter", {}) or {}

        if target_filename:
            base = os.path.basename(target_filename.strip().replace(" ", ""))
            clean = base if base.endswith(".md") else f"{base}.md"
            selected = [clean] if clean in all_documents else []
        else:
            selected = sorted(all_documents)

        active_config = (config or self.config).with_hashes(
            source_hash=self.config.source_hash, venue_profile_hash=self.config.venue_profile_hash,
        )
        baseline_input = "\n".join(all_documents[name] for name in selected)
        ledger_context = self.ledger.start(
            filename=target_filename or "__all_drafts__", venue="ALL",
            baseline_content=baseline_input, max_iters=active_config.max_remediation_iterations,
            metadata={
                "scope": "matrix", "draft_count": len(selected), "venue_count": len(test_venues),
                "evaluator_version": active_config.evaluator_version,
                "config_hash": active_config.config_hash,
                "evaluator_source_hash": active_config.source_hash,
                "venue_profile_hash": active_config.venue_profile_hash,
            },
        )
        active_run_id = ledger_context["run_id"]
        stage_events: List[Dict[str, Any]] = []
        run_state = PublicationRunState(
            run_id=active_run_id,
            draft_filenames=selected,
            venues=test_venues,
            evaluator_version=active_config.evaluator_version,
            config_hash=active_config.config_hash,
        )

        def emit_stage(stage: PublicationStage, status: str, input_value: Any, output_value: Any,
                       diagnostics: Optional[Dict[str, Any]] = None, blocking_reason: str = "") -> None:
            timer_started = time.perf_counter()
            now = datetime.now(timezone.utc).isoformat()
            event = EvaluationStageEvent(
                event_id=f"{active_run_id}-{len(stage_events) + 1}", run_id=active_run_id,
                stage=stage.value, status=status, started_at=now, finished_at=now,
                duration_ms=round((time.perf_counter() - timer_started) * 1000, 3),
                input_hash=stable_hash(input_value), output_hash=stable_hash(output_value),
                retries=0, blocking_reason=blocking_reason, diagnostics=diagnostics or {},
            ).to_dict()
            stage_events.append(event)
            run_state.current_stage = stage.value
            run_state.stage_status[stage.value] = status
            if blocking_reason:
                run_state.failure_history.append({
                    "stage": stage.value, "reason": blocking_reason,
                })
            self.ledger.record_stage_event(active_run_id, event)
            if progress_callback:
                progress_callback(event)

        # Evaluate the same normalized candidate that is compiled below. This
        # prevents stale quality results when deterministic remediation changes
        # the manuscript between the originality/value pass and PDF generation.
        prepared_documents = {
            filename: self.checkmate.auto_remediate_markdown(content)
            for filename, content in all_documents.items()
        }
        emit_stage(
            PublicationStage.PREPARE, "passed", all_documents,
            prepared_documents, {"drafts_prepared": len(prepared_documents)},
        )
        originality = self.audit_collection_originality(
            prepared_documents,
            max_ngram_overlap=active_config.originality_block_overlap_pct,
            review_overlap=active_config.originality_review_overlap_pct,
        )
        emit_stage(
            PublicationStage.ORIGINALITY,
            "passed" if originality["passed"] else "blocked",
            prepared_documents, originality,
            {"pairs_reviewed": len(originality.get("pairs", []))},
            "" if originality["passed"] else "Exact or high-overlap manuscript content detected",
        )
        value_reports = {
            filename: self.audit_substantive_value(
                prepared_documents[filename], min_words=active_config.substantive_min_words,
            )
            for filename in selected
        }
        exports_dir = os.path.join(self.vault_manager.vault_path, "04_Drafts", "exports")
        os.makedirs(exports_dir, exist_ok=True)

        results: List[Dict[str, Any]] = []
        artifact_hashes: Dict[str, str] = {}
        manuscript_summaries: List[Dict[str, Any]] = []
        source_papers: List[Dict[str, Any]] = []
        # Build the literature evidence set once per matrix run. ``list_files``
        # intentionally returns previews for the UI and therefore caused a
        # second full read of all 1,000+ source papers here.
        paper_folder = getattr(self.vault_manager, "folders", {}).get("papers")
        cited_keys = {
            key
            for filename in selected
            for key in self.fact_checker.extract_citation_keys(prepared_documents[filename])
        }
        # The citation key is the retrieval key for the local corpus. Read only
        # cited records; unrelated papers cannot ground this manuscript and make
        # a full-vault scan needlessly expensive.
        paper_filenames = sorted(
            name for name in os.listdir(paper_folder or "")
            if name.endswith(".md") and (
                not cited_keys or any(
                    key == key_name or key in key_name or key_name in key
                    for key in cited_keys
                    for key_name in (citation_key(name),)
                )
            )
        ) if paper_folder else []
        for paper_name in paper_filenames:
            try:
                source = self.vault_manager.read_markdown("papers", paper_name)
                source["filename"] = paper_name
                source_papers.append(source)
            except Exception:
                continue
        source_records: Dict[str, str] = {}
        source_texts: List[str] = []
        for paper in source_papers:
            paper_text = paper.get("content", "")
            source_texts.append(paper_text)
            metadata = paper.get("frontmatter", {}) or paper.get("metadata", {}) or {}
            for key in (paper.get("filename", ""), metadata.get("id", ""), metadata.get("title", "")):
                if key:
                    source_records[str(key)] = paper_text
        source_corpus_hash = stable_hash(sorted(source_records.items()))
        measurement_records_by_file = {
            filename: self._recorded_measurement_records(filename) for filename in selected
        }
        claim_reports: Dict[str, Dict[str, Any]] = {}
        claim_inputs = {}
        for filename in selected:
            claim_records = self.fact_checker.extract_claim_evidence_records(
                prepared_documents[filename],
                source_records=source_records,
                measurement_records=measurement_records_by_file[filename],
                measured_values=self._recorded_measurements(filename),
                strict=active_config.strict_evidence,
            )
            claim_reports[filename] = self.fact_checker.claim_report(claim_records)
            claim_inputs[filename] = claim_records
        claim_blocked = sum(report["blocked_count"] for report in claim_reports.values())
        emit_stage(
            PublicationStage.CLAIM_EXTRACTION,
            "blocked" if claim_blocked else "passed",
            prepared_documents, claim_reports,
            {"claim_count": sum(report["claim_count"] for report in claim_reports.values()),
             "blocked_claim_count": claim_blocked},
            "" if not claim_blocked else "One or more quantitative or major claims lack provenance",
        )
        emit_stage(
            PublicationStage.EVIDENCE_RETRIEVAL,
            "passed" if source_records or not cited_keys else "blocked",
            sorted(cited_keys), source_records,
            {"retrieved_source_count": len(source_records), "requested_citation_count": len(cited_keys)},
            "" if source_records or not cited_keys else "No cited evidence was retrieved",
        )
        emit_stage(
            PublicationStage.EVIDENCE_GRADING,
            "blocked" if claim_blocked else "passed",
            claim_inputs, claim_reports,
            {"blocked_claim_count": claim_blocked},
            "" if not claim_blocked else "Strict evidence grading blocked claim-level records",
        )
        for filename in selected:
            content = prepared_documents[filename]
            meta = all_docs_meta[filename]
            title = meta.get("title", filename.replace(".md", "").replace("_", " ").title())
            authors = meta.get("authors", ["Aryaman Dev"])
            value_report = value_reports[filename]
            # Values this draft's own experiment recorded. Without them the fact
            # checker flags measured results as unverified simply because they are
            # not in the literature corpus, contradicting the provenance gate.
            evidence_report = self.fact_checker.audit_document(
                content,
                source_texts=source_texts,
                source_records=source_records,
                measured_values=self._recorded_measurements(filename),
                measurement_records=measurement_records_by_file[filename],
                strict_evidence=active_config.strict_evidence,
            )
            originality_report = originality["per_file"].get(filename, {"passed": True, "status": "PASS", "max_five_gram_overlap_pct": 0.0})
            venue_results: Dict[str, Any] = {}

            bib_code = self.exporter.generate_bibtex(source_papers, manuscript_content=content)
            bib_path = os.path.join(exports_dir, f"{filename.replace('.md', '')}_references.bib")
            with open(bib_path, "w", encoding="utf-8") as handle:
                handle.write(bib_code)
            for venue in test_venues:
                item_result: Dict[str, Any] = {"filename": filename, "title": title, "venue": venue, "compiled": False, "checkmate_passed": False, "layout_passed": False, "publish_ready": False}
                try:
                    emit_stage(
                        PublicationStage.VENUE_RENDERING, "started", content,
                        {"filename": filename, "venue": venue},
                        {"filename": filename, "venue": venue},
                    )
                    tex_code = self.exporter.markdown_to_venue_latex(
                        venue, title, authors, self._abstract(content), content,
                        author_details={"affiliation": meta.get("affiliation", ""), "email": meta.get("email", ""),
                                      "country": meta.get("country", "")},
                        anonymize=VENUE_PROFILES[venue].anonymized_review,
                    )
                    pdf_bytes = self.exporter.compile_pdflatex(
                        tex_code,
                        bib_code=bib_code,
                        allow_package_fallback=True,
                    )
                    if not pdf_bytes:
                        raise RuntimeError("LaTeX compilation returned no PDF bytes")
                    emit_stage(
                        PublicationStage.COMPILE, "passed", tex_code,
                        {"filename": filename, "venue": venue, "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest()},
                        {"filename": filename, "venue": venue},
                    )
                    pdf_filename = f"{filename.replace('.md', '')}_{venue}.pdf"
                    pdf_path = os.path.join(exports_dir, pdf_filename)
                    with open(pdf_path, "wb") as handle:
                        handle.write(pdf_bytes)
                    tex_path = os.path.join(exports_dir, f"{filename.replace('.md', '')}_{venue}.tex")
                    with open(tex_path, "w", encoding="utf-8") as handle:
                        handle.write(tex_code)
                    artifact_hashes[pdf_path] = hashlib.sha256(pdf_bytes).hexdigest()
                    artifact_hashes[tex_path] = hashlib.sha256(tex_code.encode("utf-8")).hexdigest()
                    artifact_hashes[bib_path] = hashlib.sha256(bib_code.encode("utf-8")).hexdigest()
                    audit = self.checkmate.audit_pdf(
                        pdf_path,
                        manuscript_markdown=content,
                        venue_key=venue,
                        tex_source=tex_code,
                        package_fallback_used=self.exporter.last_compile_used_package_fallback,
                        evidence_report=evidence_report,
                    )
                    emit_stage(
                        PublicationStage.PDF_AUDIT,
                        "passed" if audit.get("checkmate_passed") else "blocked",
                        {"pdf_path": pdf_path, "tex_hash": artifact_hashes[tex_path]},
                        audit,
                        {"filename": filename, "venue": venue},
                        "" if audit.get("checkmate_passed") else "PDF audit failed",
                    )
                    # Reuse the same geometry auditor as Backtest Lab. Preview tiles
                    # remain an explicit visual-inspection action, but every release
                    # candidate still gets an automated overflow/column audit here.
                    from services.visual_auditor import VisualLayoutAuditorService
                    layout = VisualLayoutAuditorService(self.vault_manager).audit_layout_geometry(pdf_path, venue_key=venue)
                    layout_passed = bool(layout.get("passed", False))
                    emit_stage(
                        PublicationStage.LAYOUT_AUDIT,
                        "passed" if layout_passed else "blocked",
                        {"pdf_path": pdf_path}, layout,
                        {"filename": filename, "venue": venue},
                        "" if layout_passed else "Layout geometry failed",
                    )
                    vc_check = audit.get("checks", {}).get("venue_contract", {})
                    is_index_only = bool(vc_check.get("index_only", False))
                    venue_passed = is_index_only or bool(audit.get("checkmate_passed", False))
                    template_passed = is_index_only or bool(vc_check.get("passed", False))
                    evidence_status = str(evidence_report.get("status", "NOT_RUN")).upper()
                    failed_claims = evidence_report.get("failed_count", 0)
                    evidence_passed = (evidence_status in ("PASSED", "PASS")) and (failed_claims in (0, None)) and claim_reports[filename]["status"] == "passed"
                    publish_ready = (
                        venue_passed
                        and layout_passed
                        and template_passed
                        and evidence_passed
                        and value_report["substantive_value_passed"]
                        and originality_report["passed"]
                    )
                    reasons = []
                    if not originality_report["passed"]:
                        reasons.append(originality_report["status"])
                    if not value_report["substantive_value_passed"]:
                        reasons.append("SUBSTANTIVE_VALUE_REVIEW")
                    if not venue_passed:
                        reasons.append("CHECKMATE_REMEDIATION")
                    if not layout_passed:
                        reasons.append("LAYOUT_GEOMETRY_REMEDIATION")
                    if not template_passed:
                        reasons.append("VENUE_TEMPLATE_REMEDIATION")
                    if not evidence_passed:
                        reasons.append("UNVERIFIED_EVIDENCE_OR_CITATIONS")
                    emit_stage(
                        PublicationStage.VENUE_CONTRACT,
                        "passed" if template_passed and venue_passed else "blocked",
                        {"venue": venue, "audit": audit.get("checks", {})},
                        {"template_passed": template_passed, "venue_passed": venue_passed},
                        {"filename": filename, "venue": venue},
                        "" if template_passed and venue_passed else "Venue contract failed",
                    )
                    emit_stage(
                        PublicationStage.CONVERGENCE_DECISION,
                        "passed" if publish_ready else "blocked",
                        {"filename": filename, "venue": venue},
                        {"publish_ready": publish_ready, "blocking_reasons": reasons},
                        {"filename": filename, "venue": venue},
                        "" if publish_ready else "; ".join(reasons),
                    )
                    item_result.update({
                        "compiled": True,
                        "checkmate_passed": venue_passed,
                        "checkmate_score": audit.get("score", 0.0),
                        "layout_passed": layout_passed,
                        "layout_geometry": layout,
                        "pdf_path": pdf_path,
                        "tex_path": tex_path,
                        "bib_path": bib_path,
                        "publish_ready": publish_ready,
                        "blocking_reasons": reasons,
                        "checks": audit.get("checks", {}),
                        "evidence_report": evidence_report,
                        "claim_report": claim_reports[filename],
                    })
                except Exception as error:
                    diagnostics = self.exporter.last_build_log.strip()
                    item_result["blocking_reasons"] = [
                        "LATEX_PREFLIGHT_FAILED" if diagnostics.startswith("LaTeX preflight failed") else "COMPILE_FAILED"
                    ]
                    item_result["error"] = str(error)
                    if diagnostics:
                        item_result["compile_diagnostics"] = diagnostics[-2000:]
                results.append(item_result)
                venue_results[venue] = item_result

            ready_venues = [venue for venue, result in venue_results.items() if result.get("publish_ready")]
            if ready_venues:
                readiness = "READY_FOR_HUMAN_REVIEW"
            elif not originality_report["passed"]:
                readiness = "BLOCKED_DUPLICATE_CONTENT"
            elif evidence_report.get("status") != "passed":
                readiness = "BLOCKED_UNVERIFIED_EVIDENCE"
            elif not value_report["substantive_value_passed"]:
                readiness = "BLOCKED_SUBSTANTIVE_VALUE"
            else:
                readiness = "NEEDS_VENUE_REMEDIATION"
            updated_meta = dict(meta)
            updated_meta.update({
                "publisher_readiness": readiness,
                "publisher_originality": originality_report["status"],
                "publisher_value_score": str(value_report["score"]),
                "publisher_tested_venues": ", ".join(test_venues),
                "publisher_best_venues": ", ".join(ready_venues),
            })
            self.vault_manager.save_markdown("drafts", filename, content, frontmatter=updated_meta)
            manuscript_summaries.append({
                "filename": filename,
                "title": title,
                "readiness": readiness,
                "originality": originality_report,
                "value": value_report,
                "evidence": evidence_report,
                "claim_report": claim_reports[filename],
                "venue_results": venue_results,
                "ready_venues": ready_venues,
            })

        progress = {
            "drafts_tested": len(selected),
            "venues_tested": len(test_venues),
            "matrix_total": len(selected) * len(test_venues),
            "compiled": sum(1 for result in results if result.get("compiled")),
            "blocked": sum(1 for result in results if not result.get("publish_ready")),
            "ready": sum(1 for result in results if result.get("publish_ready")),
            "current_stage": PublicationStage.ARTIFACT_BUNDLE.value,
        }
        emit_stage(
            PublicationStage.ARTIFACT_BUNDLE, "passed",
            {"results": results}, progress,
            {"artifact_count": len(artifact_hashes)},
        )
        final_content = stable_hash(results)
        snapshot = reproducibility_snapshot(
            root=self._root,
            config=active_config,
            manuscript_hashes={
                name: hashlib.sha256(prepared_documents[name].encode("utf-8")).hexdigest()
                for name in selected
            },
            source_corpus_hash=source_corpus_hash,
            artifact_hashes=artifact_hashes,
            stage_timings={event["stage"]: event["duration_ms"] for event in stage_events},
        )
        failure_history = [
            {
                "filename": result.get("filename"),
                "venue": result.get("venue"),
                "blocking_reasons": result.get("blocking_reasons", []),
                "error": result.get("error", ""),
            }
            for result in results
            if result.get("blocking_reasons") or result.get("error")
        ]
        final_decision = "READY_FOR_HUMAN_REVIEW" if progress["blocked"] == 0 else "COMPLETED_WITH_BLOCKED_CASES"
        run_manifest = self.ledger.finish(
            active_run_id,
            status="COMPLETED",
            final_content=final_content,
            iterations=0,
            reason="" if progress["blocked"] == 0 else "One or more matrix cases remain blocked",
            metadata={
                "stage_events_path": str(self.ledger.root / active_run_id / "stage_events.jsonl"),
                "reproducibility_snapshot": snapshot,
                "progress": progress,
                "failure_history": failure_history,
                "final_decision": final_decision,
            },
        )
        typed_run_state = {
            "run_id": run_state.run_id,
            "draft_filenames": run_state.draft_filenames,
            "venues": run_state.venues,
            "evaluator_version": run_state.evaluator_version,
            "config_hash": run_state.config_hash,
            "current_stage": run_state.current_stage,
            "stage_status": run_state.stage_status,
            "failure_history": run_state.failure_history,
        }
        def compact_manifest_result(result: Dict[str, Any]) -> Dict[str, Any]:
            compact = {
                key: result.get(key)
                for key in (
                    "filename", "title", "venue", "compiled", "publish_ready",
                    "blocking_reasons", "checkmate_passed", "checkmate_score",
                    "layout_passed", "pdf_path", "tex_path", "bib_path", "error",
                    "compile_diagnostics",
                )
            }
            compact_checks = dict(result.get("checks") or {})
            grounding = dict(compact_checks.get("evidence_grounding") or {})
            grounding.pop("report", None)
            if grounding:
                compact_checks["evidence_grounding"] = grounding
            compact["checks"] = compact_checks
            evidence = dict(result.get("evidence_report") or {})
            claim = dict(evidence.pop("claim_report", {}) or {})
            evidence["claim_report_hash"] = claim.get("claim_report_hash", "")
            evidence["claim_count"] = claim.get("claim_count", 0)
            evidence["blocked_claim_count"] = claim.get("blocked_count", 0)
            compact["evidence_report"] = evidence
            claim_report = dict(result.get("claim_report") or {})
            compact["claim_report"] = {
                "claim_count": claim_report.get("claim_count", 0),
                "blocked_count": claim_report.get("blocked_count", 0),
                "status": claim_report.get("status", "blocked"),
                "claim_report_hash": claim_report.get("claim_report_hash", ""),
            }
            return compact

        manifest = {
            "run_id": active_run_id,
            "evaluator_version": active_config.evaluator_version,
            "evaluator_config": active_config.to_dict(),
            "typed_run_state": typed_run_state,
            "config_hash": active_config.config_hash,
            "evaluator_source_hash": active_config.source_hash,
            "venue_profile_hash": active_config.venue_profile_hash,
            "strict_evidence": active_config.strict_evidence,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "venues": test_venues,
            "draft_count": len(selected),
            "total_tests": len(results),
            "compiled_count": sum(1 for result in results if result.get("compiled")),
            "ready_count": sum(1 for result in results if result.get("publish_ready")),
            "progress": progress,
            "stage_events": stage_events,
            "stage_events_path": run_manifest.get("stage_events_path"),
            "claim_report": {
                filename: claim_reports[filename] for filename in sorted(claim_reports)
            },
            "reproducibility_snapshot": snapshot,
            "failure_history": failure_history,
            "final_decision": final_decision,
            "results": [compact_manifest_result(result) for result in results],
        }
        manifest_path = os.path.join(exports_dir, "publisher_readiness_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, sort_keys=True)

        return {
            "success": True,
            "run_id": active_run_id,
            "evaluator_version": active_config.evaluator_version,
            "config_hash": active_config.config_hash,
            "strict_evidence": active_config.strict_evidence,
            "evaluator_config": active_config.to_dict(),
            "typed_run_state": typed_run_state,
            "venues": test_venues,
            "draft_count": len(selected),
            "total_tests": len(results),
            "compiled_count": sum(1 for result in results if result.get("compiled")),
            "venue_pass_count": sum(1 for result in results if result.get("checkmate_passed")),
            "ready_count": sum(1 for result in results if result.get("publish_ready")),
            "blocked_count": sum(1 for summary in manuscript_summaries if summary["readiness"].startswith("BLOCKED")),
            "collection_originality": originality,
            "manuscripts": manuscript_summaries,
            "results": results,
            "progress": progress,
            "stage_events": stage_events,
            "stage_events_path": run_manifest.get("stage_events_path"),
            "claim_report": {filename: claim_reports[filename] for filename in sorted(claim_reports)},
            "reproducibility_snapshot": snapshot,
            "failure_history": failure_history,
            "final_decision": final_decision,
            "artifact_manifest": manifest_path,
            "release_note": "Ready means formatting, originality, and substantive-value gates passed; human author/journal review is still required.",
        }
