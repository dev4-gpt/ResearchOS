from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

from domain.models import citation_key


NUMERIC_PATTERN = re.compile(
    r"(?:"
    r"\b\d+(?:,\d{3})*(?:\.\d+)?%"
    r"|\bN\s*=\s*\d+(?:,\d{3})*"
    r"|\bp\s*[<>=]\s*0?\.\d+"
    r"|\b[A-Za-z0-9_]+\s*=\s*\d+(?:,\d{3})*(?:\.\d+)?\b"
    r"|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ms|s|x|million|billion)\b"
    r"|\b\d+(?:,\d{3})*(?:\.\d+)?\s+(?:[A-Za-z-]+\s+){0,2}(?:agents?|codebases?|organizations?|engineers?|issues?|repositories?|samples?|instances?|months?|tasks?|projects?)\b"
    r")"
)


def is_non_metric_number(claim: str) -> bool:
    s = claim.strip()
    if s.isdigit() and 1900 <= int(s) <= 2099:
        return True
    if re.match(r"^\d{1,2}\.\d{1,2}$", s):
        return True
    if re.match(r"^p\s*[<>=]\s*0?\.\d+", s, re.IGNORECASE):
        return True
    # 'N = 1000' is a sample size, and NUMERIC_PATTERN has an alternation whose
    # only purpose is to find it. Discarding every string containing '=' undid
    # that: the detector went looking for sample sizes and the filter threw them
    # away again, which is most of why this counted 1 claim where 2 were asserted
    # (ERR-044). Loop variables and section numbers are still discarded.
    if re.match(r"^N\s*=\s*\d", s):
        return False
    if "=" in s or re.search(r"^(?:i|j|k|m|n|t|x|y|z|r|p|step|val|var|index|iter|phase|section|pillar|stage|table|figure|eq)\b", s, re.IGNORECASE):
        return True
    # Only structural nouns belong here. The scale nouns -- months, agents,
    # codebases, organizations -- are exactly what NUMERIC_PATTERN hunts, because
    # '500 enterprise codebases' is the shape a fabricated claim takes. Listing
    # them in both places meant the strongest claims were the ones never checked.
    if re.search(r"\b(phases?|sections?|stages?|pillars?|steps?|figures?|tables?)\b", s, re.IGNORECASE):
        return True
    if re.match(r"^\d+s$", s):
        return True
    # If the number is a single digit followed by verbs or section description words
    if re.match(r"^\d\s+(?:formalizes|presents|introduces|outlines|describes|evaluates|details)", s, re.IGNORECASE):
        return True
    return False


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
            fn_key = citation_key(filename)
            keys.add(fn_key)
            for prefix in ["crossref_", "arxiv_", "openalex_", "doi_", "pubmed_"]:
                if fn_key.startswith(prefix):
                    keys.add(fn_key[len(prefix):])
            if metadata.get("id"):
                meta_id = citation_key(str(metadata["id"]))
                keys.add(meta_id)
                for prefix in ["crossref_", "arxiv_", "openalex_", "doi_", "pubmed_"]:
                    if meta_id.startswith(prefix):
                        keys.add(meta_id[len(prefix):])
        return keys

    def extract_citation_keys(self, content: str) -> List[str]:
        raw = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]|\\cite\{([^}]+)\}", content)
        values = []
        for wiki, latex in raw:
            value = wiki or latex
            values.extend(citation_key(part.strip()) for part in value.split(",") if part.strip())
        return sorted(set(values))

    # Regex for a plausible standard academic author-year citation key
    # e.g. "rogers2003", "feuerriegel2023generativeai", "wooldridge2009"
    _AUTHOR_YEAR_RE = re.compile(r"^[a-z]+\d{4}[a-z0-9]*$")

    def validate_citations(self, content: str) -> Dict[str, Any]:
        keys = self.extract_citation_keys(content)
        known = self._paper_keys()
        verified = []
        broken = []
        unresolved = []  # plausible academic keys not in vault (not a blocking error)
        for key in keys:
            matched = False
            if not self.vault_manager or key in known:
                matched = True
            else:
                core_key = re.sub(r"^(crossref_|arxiv_|openalex_|doi_|pubmed_|europepmc_|pmc_|pmid_|dbsnp_|https?_)", "", key)
                for k_item in known:
                    core_known = re.sub(r"^(crossref_|arxiv_|openalex_|doi_|pubmed_|europepmc_|pmc_|pmid_|dbsnp_|https?_)", "", k_item)
                    if key in k_item or k_item in key or (core_key and (core_key in core_known or core_known in core_key)):
                        matched = True
                        break
            if matched:
                verified.append(key)
            elif self._AUTHOR_YEAR_RE.match(key):
                # Plausible author-year key — not in vault but not malformed
                unresolved.append(key)
            else:
                broken.append(key)
        # Score counts unresolved as half-credit (they're valid but not vault-verified)
        effective_verified = len(verified) + len(unresolved) * 0.5
        score = 100.0 if not keys else round((effective_verified / len(keys)) * 100, 1)
        return {
            "total_citations": len(keys),
            "verified_count": len(verified),
            "broken_count": len(broken),
            "unresolved_count": len(unresolved),
            "verified_links": verified,
            "broken_links": broken,
            "unresolved_links": unresolved,
            "citation_score": score,
        }

    def validate_numeric_claims(self, draft_content: str, source_texts: List[str],
                                source_records: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        clean_content_for_claims = re.sub(r"\[\[.*?\]\]|\\cite\{.*?\}|https?://\S+", " ", draft_content)
        raw_claims = sorted(set(NUMERIC_PATTERN.findall(clean_content_for_claims)))
        claims = [c for c in raw_claims if not is_non_metric_number(c)]
        grounded = []
        unverified = []
        if source_records:
            corpus_by_key = {citation_key(key): text.lower() for key, text in source_records.items()}
            combined_corpus = " ".join(source_texts).lower()
            paragraphs = re.split(r"\n\s*\n", draft_content)
            for claim in claims:
                claim_lower = claim.lower()
                supported = False
                for paragraph in paragraphs:
                    if claim not in paragraph:
                        continue
                    cited = self.extract_citation_keys(paragraph)
                    if cited and any(claim_lower in corpus_by_key.get(key, "") for key in cited):
                        supported = True
                        break
                if not supported and claim_lower in combined_corpus:
                    supported = True
                # There used to be a third chance here: a claim was accepted if the
                # paragraph containing it mentioned "table", "benchmark", "result",
                # "finding", "experiment" -- or a pipe character. That marks a claim
                # grounded because of the words around it rather than any evidence,
                # and it is how "500 enterprise codebases" passed while its only
                # cited source said "a conceptual framework only" (ERR-044). Claims
                # this project measured itself are absolved by
                # _absolve_measured_claims against recorded values, which is the
                # same job done against evidence instead of vocabulary.
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

    @staticmethod
    def _absolve_measured_claims(metric_report: Dict[str, Any],
                                 measured_values: List[float]) -> Dict[str, Any]:
        """Move claims matching a recorded measurement out of `unverified_claims`."""
        import re as _re

        def numeric(text: str) -> Optional[float]:
            match = _re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", str(text).replace(",", ""))
            if not match:
                return None
            try:
                return float(match.group(0))
            except ValueError:
                return None

        still_unverified, absolved = [], []
        for claim in metric_report.get("unverified_claims", []):
            value = numeric(claim)
            fraction = _re.search(r"\.(\d+)", str(claim))
            decimals = len(fraction.group(1)) if fraction else 0
            hit = value is not None and any(
                round(m, decimals) == round(value, decimals) for m in measured_values
            )
            (absolved if hit else still_unverified).append(claim)

        updated = dict(metric_report)
        updated["unverified_claims"] = still_unverified
        updated["unverified_count"] = len(still_unverified)
        if absolved:
            updated["measurement_backed_claims"] = absolved
            total = updated.get("total_numeric_claims") or 1
            updated["metric_score"] = round(
                100.0 * (total - len(still_unverified)) / total, 1
            )
        return updated

    def audit_document(self, content: str, source_texts: Optional[List[str]] = None,
                       source_records: Optional[Dict[str, str]] = None,
                       measured_values: Optional[List[float]] = None) -> Dict[str, Any]:
        """Audit citations and numeric claims.

        ``measured_values`` carries the values a recorded experiment produced for
        this draft. A claim this service cannot find in the literature but which
        an experiment measured is grounded, not unverified: without this the
        provenance gate and this checker disagree about the same manuscript, and
        a paper whose numbers all trace to artifacts still reports as blocked.
        """
        citation_report = self.validate_citations(content)
        metric_report = self.validate_numeric_claims(content, source_texts or [], source_records)
        if measured_values:
            metric_report = self._absolve_measured_claims(metric_report, measured_values)
        blocking_errors: List[str] = []
        # Only block on citations that are genuinely malformed/non-existent — NOT plausible author-year keys
        if citation_report["broken_links"]:
            blocking_errors.append("Broken paper citations: " + ", ".join(citation_report["broken_links"]))
        if metric_report["unverified_claims"] and source_records is not None:
            # Only block on unverified metrics when a source corpus was actually provided
            blocking_errors.append("Unverified numeric claims: " + ", ".join(metric_report["unverified_claims"]))

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
                "unresolved_citations": citation_report.get("unresolved_links", []),
                "grounded_metrics": metric_report["grounded_claims"],
                "unverified_metrics": metric_report["unverified_claims"],
            },
        }
