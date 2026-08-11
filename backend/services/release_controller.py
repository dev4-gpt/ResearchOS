from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from domain.models import BuildDecision, RunManifest


class ReleaseController:
    """Fail-closed release gate for generated research artifacts."""

    BLOCKING_STATES = {"DRAFT", "BLOCKED"}

    def evaluate(self, *, manifest: Optional[RunManifest] = None,
                 fact_audit: Optional[Dict[str, Any]] = None,
                 bibliography_report: Optional[Dict[str, Any]] = None,
                 qa_report: Optional[Dict[str, Any]] = None,
                 peer_review: Optional[Dict[str, Any]] = None,
                 synthetic: bool = False) -> BuildDecision:
        checks: Dict[str, bool] = {}
        errors: List[str] = []

        checks["non_synthetic"] = not synthetic and not (manifest.synthetic if manifest else False)
        if not checks["non_synthetic"]:
            errors.append("Synthetic or dry-run output cannot be released as camera-ready.")

        audit = fact_audit or {}
        checks["evidence_verified"] = audit.get("status") == "passed" and not audit.get("blocking_errors")
        if not checks["evidence_verified"]:
            errors.extend(audit.get("blocking_errors", []))
            if audit.get("status") != "passed":
                errors.append("Evidence audit did not pass.")

        if bibliography_report is not None:
            checks["bibliography_verified"] = (
                bibliography_report.get("status") == "passed"
                and not bibliography_report.get("errors")
            )
            if not checks["bibliography_verified"]:
                errors.extend(bibliography_report.get("errors", []))
                errors.append("Bibliography audit did not pass.")

        qa = qa_report or {}
        checks["pdf_qa_passed"] = bool(qa) and qa.get("status") == "passed" and not qa.get("errors")
        if not checks["pdf_qa_passed"]:
            errors.extend(qa.get("errors", []))
            if not qa:
                errors.append("No PDF QA report was provided.")

        review = peer_review or {}
        checks["peer_review_valid"] = bool(review.get("schema_valid")) and review.get("overall_decision") in {"ACCEPT", "WEAK ACCEPT"}
        if not checks["peer_review_valid"]:
            errors.append("Peer-review audit is missing, invalid, or non-accepting.")

        checks["manifest_present"] = manifest is not None
        if not checks["manifest_present"]:
            errors.append("Run manifest is missing.")

        status = "ready_for_human_signoff" if not errors else "blocked"
        return BuildDecision(status=status, checks=checks, errors=sorted(set(errors)))
