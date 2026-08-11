from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

from domain.models import citation_key


NUMERIC_PATTERN = re.compile(
    r"(?:\b\d+(?:\.\d+)?%|\bN\s*=\s*\d+|\bp\s*[<>=]\s*0?\.\d+|\b\d+\.\d+\b|\b\d{4,}\b)"
)


class FactCheckerService:
    """Fail-closed claim and citation verifier.

    The legacy methods remain available for API compatibility, but release callers
    must provide source_records so each claim is checked against its cited source.
    """

    def __init__(self, vault_manager: Optional[Any] = None):
        self.vault_manager = vault_manager

    def _paper_keys(self) -> set[str]:
        keys: set[str] = set()
        if not self.vault_manager:
            return keys
        for file in self.vault_manager.list_files("papers"):
            filename = file.get("filename", "")
            metadata = file.get("metadata", {}) or {}
            keys.add(citation_key(filename))
            if metadata.get("id"):
                keys.add(citation_key(str(metadata["id"])))
        return keys

    def extract_citation_keys(self, content: str) -> List[str]:
        raw = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]|\\cite\{([^}]+)\}", content)
        values = []
        for wiki, latex in raw:
            value = wiki or latex
            values.append(citation_key(value.strip()))
        return sorted(set(values))

    def validate_citations(self, content: str) -> Dict[str, Any]:
        keys = self.extract_citation_keys(content)
        known = self._paper_keys()
        verified = []
        broken = []
        for key in keys:
            if not self.vault_manager or key in known:
                verified.append(key)
            else:
                broken.append(key)
        score = 100.0 if not keys else round((len(verified) / len(keys)) * 100, 1)
        return {
            "total_citations": len(keys),
            "verified_count": len(verified),
            "broken_count": len(broken),
            "verified_links": verified,
            "broken_links": broken,
            "citation_score": score,
        }

    def validate_numeric_claims(self, draft_content: str, source_texts: List[str],
                                source_records: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        claims = sorted(set(NUMERIC_PATTERN.findall(draft_content)))
        grounded = []
        unverified = []
        if source_records:
            corpus_by_key = {citation_key(key): text.lower() for key, text in source_records.items()}
            paragraphs = re.split(r"\n\s*\n", draft_content)
            for claim in claims:
                claim_lower = claim.lower()
                supported = False
                for paragraph in paragraphs:
                    if claim not in paragraph:
                        continue
                    cited = self.extract_citation_keys(paragraph)
                    supported = bool(cited) and any(claim_lower in corpus_by_key.get(key, "") for key in cited)
                    if supported:
                        break
                (grounded if supported else unverified).append(claim)
        else:
            # Legacy callers can still request a report, but an unscoped corpus is
            # intentionally not considered release-grade evidence.
            combined = " ".join(source_texts).lower()
            for claim in claims:
                (grounded if claim.lower() in combined else unverified).append(claim)

        score = 100.0 if not claims else round((len(grounded) / len(claims)) * 100, 1)
        return {
            "total_numeric_claims": len(claims),
            "grounded_count": len(grounded),
            "unverified_count": len(unverified),
            "grounded_claims": grounded,
            "unverified_claims": unverified,
            "metric_score": score,
        }

    def validate_bibliography(self, content: str, bibtex: str) -> Dict[str, Any]:
        """Verify that every manuscript citation has exactly one usable BibTeX key."""
        raw_keys = re.findall(r"@\w+\s*\{\s*([^,\s}]*)", bibtex or "")
        keys = [citation_key(key) for key in raw_keys if key.strip()]
        empty_keys = len(raw_keys) - len(keys)
        duplicates = sorted({key for key in keys if keys.count(key) > 1})
        cited = set(self.extract_citation_keys(content))
        bibliography_keys = set(keys)
        missing = sorted(cited - bibliography_keys)
        errors = []
        if empty_keys:
            errors.append(f"Bibliography contains {empty_keys} empty key(s).")
        if duplicates:
            errors.append("Duplicate bibliography keys: " + ", ".join(duplicates))
        if missing:
            errors.append("Cited keys missing from bibliography: " + ", ".join(missing))
        return {
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "entry_count": len(keys),
            "cited_count": len(cited),
            "uncited_entries": sorted(bibliography_keys - cited),
        }

    def audit_document(self, content: str, source_texts: Optional[List[str]] = None,
                       source_records: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        citation_report = self.validate_citations(content)
        metric_report = self.validate_numeric_claims(content, source_texts or [], source_records)
        blocking_errors: List[str] = []
        if citation_report["broken_links"]:
            blocking_errors.append("Broken paper citations: " + ", ".join(citation_report["broken_links"]))
        if metric_report["unverified_claims"]:
            blocking_errors.append("Unverified numeric claims: " + ", ".join(metric_report["unverified_claims"]))
        if source_records is None and metric_report["total_numeric_claims"]:
            blocking_errors.append("Numeric claims were checked without cited-source provenance.")

        score = round((citation_report["citation_score"] + metric_report["metric_score"]) / 2.0, 1)
        passed = not blocking_errors
        return {
            "fact_check_score": score,
            "citation_report": citation_report,
            "metric_report": metric_report,
            "status": "passed" if passed else "needs_review",
            "blocking_errors": sorted(set(blocking_errors)),
            "verification_matrix": {
                "verified_citations": citation_report["verified_links"],
                "broken_citations": citation_report["broken_links"],
                "grounded_metrics": metric_report["grounded_claims"],
                "unverified_metrics": metric_report["unverified_claims"],
            },
        }
