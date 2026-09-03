"""Fail-closed venue contract checks for generated LaTeX artifacts.

Compilation alone does not prove that a PDF was produced with the requested
venue template.  This module checks the source preamble, policy-sensitive
content, page scope, and whether a local package fallback was used.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from services.venue_profiles import VENUE_PROFILES


VENUE_CONTRACTS: Dict[str, Dict[str, Any]] = {
    "NeurIPS": {"required_tokens": [r"\\usepackage\[final\]\{neurips_2026\}", r"\\documentclass"], "template_configured": True},
    "ICML": {"required_tokens": [r"\\usepackage\{icml2026\}", r"\\documentclass"], "template_configured": True},
    "CVPR": {"required_tokens": [r"\\usepackage\{cvpr\}", r"\\documentclass"], "template_configured": True},
    "ACL": {"required_tokens": [r"\\usepackage\[review\]\{acl\}", r"\\documentclass"], "template_configured": True},
    "IEEEtran": {"required_tokens": [r"\\documentclass\[[^]]*\]\{IEEEtran\}"], "template_configured": True},
    "ACM": {"required_tokens": [r"\\documentclass\[[^]]*\]\{acmart\}"], "template_configured": True},
    "IEEE_Access": {"required_tokens": [r"\\documentclass\[[^]]*\]\{IEEEtran\}"], "template_configured": True},
    "SpringerOpen": {"required_tokens": [r"\\documentclass"], "template_configured": True},
    "Femington": {"required_tokens": [r"\\documentclass"], "template_configured": True},
    "MDPI": {"required_tokens": [r"\\documentclass"], "template_configured": True},
    "arXiv": {"required_tokens": [r"\\documentclass\[[^]]*\]\{article\}"], "template_configured": True},
    # DOAJ is an index, not a publisher or manuscript template.
    "DOAJ": {"required_tokens": [], "template_configured": False, "index_only": True},
}


def venue_registry_gaps() -> Dict[str, List[str]]:
    """Return profile/contract mismatches instead of silently falling back."""
    profile_keys = set(VENUE_PROFILES)
    contract_keys = set(VENUE_CONTRACTS)
    return {
        "missing_contracts": sorted(profile_keys - contract_keys),
        "orphan_contracts": sorted(contract_keys - profile_keys),
    }


def _contains_any(text: str, tokens: Iterable[str]) -> List[str]:
    return [token for token in tokens if re.search(token, text, flags=re.IGNORECASE)]


def audit_venue_contract(
    venue_key: str,
    tex_source: str,
    pdf_text: str,
    manuscript_markdown: str,
    total_pages: int,
    package_fallback_used: bool = False,
) -> Dict[str, Any]:
    registry_gaps = venue_registry_gaps()
    profile = VENUE_PROFILES.get(venue_key)
    contract = VENUE_CONTRACTS.get(venue_key, {})
    source = tex_source or ""
    document_text = pdf_text or ""
    manuscript = manuscript_markdown or ""

    required_tokens = contract.get("required_tokens", [])
    missing_tokens = [token for token in required_tokens if not re.search(token, source, flags=re.IGNORECASE)]
    configured = bool(contract.get("template_configured", False)) and venue_key not in registry_gaps["missing_contracts"]
    index_only = bool(contract.get("index_only", False) or getattr(profile, "is_index_only", False))
    template_passed = bool(source) and configured and not missing_tokens and not package_fallback_used and not index_only

    normalized_pdf = document_text.lower()
    required_sections = list(getattr(profile, "required_sections", []) or []) if profile else []
    # Required-section checks are artifact checks: a heading in Markdown is not
    # evidence that the rendered PDF retained the section.
    def rendered_section_present(section: str) -> bool:
        if section.lower() in normalized_pdf:
            return True
        # acmart renders the abstract body without a text-extractable
        # ``Abstract`` heading. Verify the rendered body instead of accepting a
        # source-only heading, preserving the artifact-level contract check.
        if venue_key == "ACM" and section.lower() == "abstract":
            abstract_match = re.search(
                r"#+\s*(?:\d+[.\s]*)?(?:Executive\s+)?Abstract[^\n]*\n+([\s\S]*?)(?=\n+#{1,2}\s+|\Z)",
                manuscript,
                flags=re.IGNORECASE,
            )
            if abstract_match:
                abstract_body = re.sub(r"\[\[[^\]]+\]\]|\\cite\{[^}]+\}", " ", abstract_match.group(1))
                abstract_body = re.sub(
                    r"\b(?:arxiv|crossref|openalex|pubmed|doaj|plos|dblp|hal)[A-Za-z0-9_.-]*",
                    " ",
                    abstract_body,
                    flags=re.IGNORECASE,
                )
                fingerprint_words = re.findall(r"[a-z0-9]+", abstract_body.lower())[:18]
                rendered_words = set(re.findall(r"[a-z0-9]+", normalized_pdf))
                return len(fingerprint_words) >= 8 and all(word in rendered_words for word in fingerprint_words)
        return False

    missing_sections = [section for section in required_sections if not rendered_section_present(section)]
    forbidden_tokens = list(getattr(profile, "forbidden_tokens", []) or []) if profile else []
    forbidden_found = [token for token in forbidden_tokens if token.lower() in normalized_pdf]

    target_match = re.search(r"^target_pages:\s*[\"']?(\d+)", manuscript, flags=re.IGNORECASE | re.MULTILINE)
    target_pages = int(target_match.group(1)) if target_match else None
    configured_max = getattr(profile, "long_page_limit", None) or getattr(profile, "page_limit", None) or 16
    max_pages = target_pages or configured_max
    page_passed = 1 <= total_pages <= max_pages

    policy_passed = not missing_sections and not forbidden_found
    passed = template_passed and policy_passed and page_passed
    problems: List[str] = []
    if index_only:
        problems.append("DOAJ is an indexing service, not a manuscript venue/template")
    if not configured:
        problems.append("venue-specific official template is not configured")
    if venue_key in registry_gaps["missing_contracts"]:
        problems.append("venue is missing an explicit contract entry")
    if missing_tokens:
        problems.append("missing template markers: " + ", ".join(missing_tokens))
    if package_fallback_used:
        problems.append("local package fallback was used; artifact is preview-only")
    if missing_sections:
        problems.append("missing required sections: " + ", ".join(missing_sections))
    if forbidden_found:
        problems.append("forbidden identity tokens found: " + ", ".join(forbidden_found))
    if not page_passed:
        problems.append(f"page count {total_pages} outside allowed scope 1-{max_pages}")

    return {
        "passed": passed,
        "template_passed": template_passed,
        "policy_passed": policy_passed,
        "page_passed": page_passed,
        "status": "PASS" if passed else "NEEDS_REMEDIATION",
        "detail": "Venue contract satisfied" if passed else "; ".join(problems),
        "venue": venue_key,
        "template_configured": configured,
        "index_only": index_only,
        "package_fallback_used": package_fallback_used,
        "missing_template_markers": missing_tokens,
        "required_sections": required_sections,
        "missing_sections": missing_sections,
        "forbidden_tokens_found": forbidden_found,
        "total_pages": total_pages,
        "max_pages": max_pages,
        "target_pages": target_pages,
        "registry_gaps": registry_gaps,
    }
