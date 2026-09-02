"""Immutable publication-evaluation contracts and typed run telemetry.

The publication harness deliberately keeps policy separate from candidate content.
The service may remediate a manuscript, but a run receives a frozen evaluator
configuration and records the exact inputs, tools, and decisions that produced it.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(value: Any) -> str:
    """Hash JSON-like values canonically so repeat runs compare meaningfully."""
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class PublicationStage(str, Enum):
    PREPARE = "prepare"
    ORIGINALITY = "originality"
    CLAIM_EXTRACTION = "claim_extraction"
    EVIDENCE_RETRIEVAL = "evidence_retrieval"
    EVIDENCE_GRADING = "evidence_grading"
    VENUE_RENDERING = "venue_rendering"
    COMPILE = "compile"
    PDF_AUDIT = "pdf_audit"
    LAYOUT_AUDIT = "layout_audit"
    VENUE_CONTRACT = "venue_contract"
    CONVERGENCE_DECISION = "convergence_decision"
    ARTIFACT_BUNDLE = "artifact_bundle"


@dataclass(frozen=True)
class PublicationEvaluationConfig:
    """Frozen policy surface for a publication evaluation run."""

    evaluator_version: str = "researchingos-publication-evaluator-v2"
    source_hash: str = ""
    venue_profile_hash: str = ""
    strict_evidence: bool = True
    originality_review_overlap_pct: float = 35.0
    originality_block_overlap_pct: float = 65.0
    substantive_min_words: int = 450
    require_artifact_for_major_claims: bool = True
    require_provenance_for_quantitative_claims: bool = True
    max_remediation_iterations: int = 3
    held_out_fixture_version: str = "publication-fixtures-v2"
    ruleset: str = "fail_closed_claims_and_venue_contracts"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def config_hash(self) -> str:
        return stable_hash(self.to_dict())

    def with_hashes(self, *, source_hash: str, venue_profile_hash: str) -> "PublicationEvaluationConfig":
        return replace(self, source_hash=source_hash, venue_profile_hash=venue_profile_hash)


@dataclass
class ClaimEvidenceRecord:
    claim_id: str
    normalized_text: str
    manuscript_location: str
    claim_category: str
    cited_source_keys: list[str] = field(default_factory=list)
    experiment_artifact_refs: list[str] = field(default_factory=list)
    artifact_sha256: list[str] = field(default_factory=list)
    verification_method: str = ""
    status: str = "BLOCKED"
    blocking_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationStageEvent:
    event_id: str
    run_id: str
    stage: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: float
    input_hash: str
    output_hash: str
    retries: int = 0
    blocking_reason: str = ""
    diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PublicationRunState:
    """Typed state for the bounded publication graph."""

    run_id: str
    draft_filenames: list[str]
    venues: list[str]
    evaluator_version: str
    config_hash: str
    current_stage: str = PublicationStage.PREPARE.value
    stage_status: Dict[str, str] = field(default_factory=dict)
    candidate_hashes: Dict[str, str] = field(default_factory=dict)
    claim_report: Dict[str, Any] = field(default_factory=dict)
    artifacts: list[Dict[str, Any]] = field(default_factory=list)
    failure_history: list[Dict[str, Any]] = field(default_factory=list)
    retries: Dict[str, int] = field(default_factory=dict)
    _allowed: Dict[str, tuple[str, ...]] = field(default_factory=lambda: {
        PublicationStage.PREPARE.value: (PublicationStage.ORIGINALITY.value,),
        PublicationStage.ORIGINALITY.value: (PublicationStage.CLAIM_EXTRACTION.value,),
        PublicationStage.CLAIM_EXTRACTION.value: (PublicationStage.EVIDENCE_RETRIEVAL.value,),
        PublicationStage.EVIDENCE_RETRIEVAL.value: (PublicationStage.EVIDENCE_GRADING.value,),
        PublicationStage.EVIDENCE_GRADING.value: (PublicationStage.VENUE_RENDERING.value,),
        PublicationStage.VENUE_RENDERING.value: (PublicationStage.COMPILE.value,),
        PublicationStage.COMPILE.value: (PublicationStage.PDF_AUDIT.value,),
        PublicationStage.PDF_AUDIT.value: (PublicationStage.LAYOUT_AUDIT.value,),
        PublicationStage.LAYOUT_AUDIT.value: (PublicationStage.VENUE_CONTRACT.value,),
        PublicationStage.VENUE_CONTRACT.value: (PublicationStage.CONVERGENCE_DECISION.value,),
        PublicationStage.CONVERGENCE_DECISION.value: (PublicationStage.ARTIFACT_BUNDLE.value,),
        PublicationStage.ARTIFACT_BUNDLE.value: (),
    }, repr=False)

    def transition(self, next_stage: PublicationStage | str) -> None:
        next_value = next_stage.value if isinstance(next_stage, PublicationStage) else str(next_stage)
        if next_value not in self._allowed.get(self.current_stage, ()):
            raise ValueError(f"Invalid publication graph transition: {self.current_stage} -> {next_value}")
        self.current_stage = next_value


@dataclass
class PublicationRunManifest:
    run_id: str
    evaluator_version: str
    config_hash: str
    status: str
    baseline_sha256: str
    final_sha256: str = ""
    started_at: str = field(default_factory=utc_now)
    finished_at: str = ""
    draft_count: int = 0
    venue_count: int = 0
    failure_history: list[Dict[str, Any]] = field(default_factory=list)
    stage_events_path: str = ""
    reproducibility_snapshot: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluator_source_hash(root: str | Path) -> str:
    """Hash evaluator implementation files, excluding generated artifacts."""
    root_path = Path(root)
    relative_files = (
        "backend/services/publication_harness.py",
        "backend/services/publisher_readiness.py",
        "backend/services/fact_checker.py",
        "backend/services/checkmate_verifier.py",
        "backend/services/latex_exporter.py",
        "backend/services/venue_contract.py",
    )
    payload = []
    for relative in relative_files:
        path = root_path / relative
        if path.exists():
            payload.append((relative, sha256_file(path)))
    return stable_hash(payload)


def venue_registry_hash(profiles: Mapping[str, Any]) -> str:
    serialized = {}
    for key in sorted(profiles):
        profile = profiles[key]
        if hasattr(profile, "model_dump"):
            serialized[key] = profile.model_dump()
        elif hasattr(profile, "dict"):
            serialized[key] = profile.dict()
        else:
            serialized[key] = str(profile)
    return stable_hash(serialized)


def _tool_version(command: str) -> str:
    try:
        completed = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5, check=False)
        return (completed.stdout or completed.stderr or "").splitlines()[0][:300]
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def reproducibility_snapshot(*, root: str | Path, config: PublicationEvaluationConfig,
                             manuscript_hashes: Mapping[str, str], source_corpus_hash: str,
                             artifact_hashes: Optional[Mapping[str, str]] = None,
                             stage_timings: Optional[Mapping[str, float]] = None) -> Dict[str, Any]:
    root_path = Path(root)
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root_path, capture_output=True, text=True, timeout=5, check=False).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=root_path, capture_output=True, text=True, timeout=5, check=False).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        commit, dirty = "unknown", None
    package_versions: Dict[str, str] = {}
    for package in ("fastapi", "pydantic", "pytest", "requests", "python-multipart"):
        try:
            package_versions[package] = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            package_versions[package] = "unavailable"
    return {
        "git_commit": commit,
        "git_worktree_dirty": dirty,
        "evaluator_version": config.evaluator_version,
        "evaluator_source_hash": config.source_hash,
        "config_hash": config.config_hash,
        "manuscript_baseline_hashes": dict(sorted(manuscript_hashes.items())),
        "source_corpus_snapshot_hash": source_corpus_hash,
        "venue_profile_hash": config.venue_profile_hash,
        "python_version": sys.version,
        "python_packages": package_versions,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "pdflatex_version": _tool_version("pdflatex"),
        "bibtex_version": _tool_version("bibtex"),
        "stage_timings_ms": dict(stage_timings or {}),
        "artifact_sha256": dict(sorted((artifact_hashes or {}).items())),
    }


def new_run_id(prefix: str = "publication") -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"


class StageTimer:
    def __init__(self) -> None:
        self.started = time.perf_counter()

    @property
    def duration_ms(self) -> float:
        return round((time.perf_counter() - self.started) * 1000, 3)
