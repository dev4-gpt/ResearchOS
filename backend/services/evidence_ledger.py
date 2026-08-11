from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional

from domain.models import ClaimRecord, RunManifest, SourceRecord, citation_key


class EvidenceLedger:
    """Small append-only JSONL ledger; Obsidian remains the readable projection."""

    def __init__(self, root: str = "runs"):
        self.root = Path(root)

    def run_dir(self, run_id: str) -> Path:
        path = self.root / run_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def create_manifest(self, run_id: str, topic: str, venue: Optional[str] = None,
                        cycle: Optional[str] = None, synthetic: bool = False) -> RunManifest:
        manifest = RunManifest(run_id=run_id, topic=topic, canonical_venue=venue,
                               venue_cycle=cycle, synthetic=synthetic)
        self.write_json(run_id, "manifest.json", manifest.model_dump())
        return manifest

    def write_json(self, run_id: str, filename: str, value: dict) -> None:
        path = self.run_dir(run_id) / filename
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def append_records(self, run_id: str, filename: str, records: Iterable[object]) -> None:
        path = self.run_dir(run_id) / filename
        with path.open("a", encoding="utf-8") as handle:
            for record in records:
                data = record.model_dump() if hasattr(record, "model_dump") else record
                handle.write(json.dumps(data, ensure_ascii=False) + "\n")

    def add_sources(self, run_id: str, sources: Iterable[SourceRecord]) -> List[SourceRecord]:
        normalized = []
        for source in sources:
            source.citation_key = source.citation_key or citation_key(source.paper_id)
            normalized.append(source)
        self.append_records(run_id, "sources.jsonl", normalized)
        return normalized

    def add_claims(self, run_id: str, claims: Iterable[ClaimRecord]) -> List[ClaimRecord]:
        normalized = list(claims)
        self.append_records(run_id, "claims.jsonl", normalized)
        return normalized

    def record_artifact(self, run_id: str, relative_path: str, data: bytes) -> str:
        path = self.run_dir(run_id) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return hashlib.sha256(data).hexdigest()
