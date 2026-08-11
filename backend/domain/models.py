from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def citation_key(value: str) -> str:
    """Return the one canonical key used by Markdown, LaTeX, and BibTeX."""
    value = value.replace(".md", "")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_").lower()


class EvidenceSpan(BaseModel):
    page: Optional[int] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    text_hash: str = ""
    excerpt: str = ""


class SourceRecord(BaseModel):
    paper_id: str
    citation_key: str
    title: str
    authors: List[str] = Field(default_factory=list)
    source: str = "unknown"
    url: str = ""
    published: str = ""
    doi: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    retrieved_at: str = Field(default_factory=utc_now)
    content_sha256: str = ""
    extraction_quality: Literal["full_text", "abstract_only", "ocr", "failed"] = "abstract_only"
    synthetic: bool = False


class ClaimRecord(BaseModel):
    claim_id: str
    claim_text: str
    claim_type: str = "qualitative"
    source_paper_ids: List[str] = Field(default_factory=list)
    evidence_spans: List[EvidenceSpan] = Field(default_factory=list)
    is_derived: bool = False
    derivation: Optional[str] = None
    verification_status: Literal["unverified", "verified", "rejected"] = "unverified"
    notes: List[str] = Field(default_factory=list)


class VenueProfile(BaseModel):
    venue: str
    cycle: str
    official_template_url: str = ""
    template_version: str = ""
    template_hash: str = ""
    document_class: str = ""
    page_scope: str = "main_body"
    page_limit: Optional[int] = None
    anonymized_review: bool = False
    required_sections: List[str] = Field(default_factory=list)
    required_tokens: List[str] = Field(default_factory=list)
    forbidden_tokens: List[str] = Field(default_factory=list)
    allow_package_fallback: bool = False


class BuildDecision(BaseModel):
    status: Literal["blocked", "ready_for_human_signoff", "released"]
    checks: Dict[str, bool] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=utc_now)


class RunManifest(BaseModel):
    run_id: str
    topic: str
    canonical_venue: Optional[str] = None
    venue_cycle: Optional[str] = None
    created_at: str = Field(default_factory=utc_now)
    synthetic: bool = False
    state: str = "DRAFT"
    source_count: int = 0
    claim_count: int = 0
    build_decision: Optional[BuildDecision] = None
