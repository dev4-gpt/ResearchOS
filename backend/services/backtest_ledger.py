"""Append-only telemetry for manuscript backtest candidates.

Every candidate is tied to the exact manuscript hash, evaluator version, venue,
and decision that produced it. Blocked and discarded candidates are retained so
the self-healing loop cannot silently repeat a bad remediation.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class BacktestLedger:
    """Persist a run manifest and append-only candidate events under the vault."""

    EVALUATOR_VERSION = "researchingos-publication-evaluator-v2"

    def __init__(self, vault_manager: Any):
        self._vault_manager = vault_manager
        self._root: Optional[Path] = None

    @property
    def root(self) -> Path:
        """Resolved lazily: callers that never touch the ledger (e.g. the
        originality/value gates) can construct this class with no vault_manager."""
        if self._root is None:
            self._root = Path(self._vault_manager.vault_path) / "04_Drafts" / "backtest_runs"
            self._root.mkdir(parents=True, exist_ok=True)
        return self._root

    @staticmethod
    def content_hash(content: str) -> str:
        return hashlib.sha256((content or "").encode("utf-8")).hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def start(self, *, filename: str, venue: str, baseline_content: str,
              max_iters: int, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        run_id = f"backtest-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
        run_dir = self.root / run_id
        run_dir.mkdir(parents=True, exist_ok=False)
        manifest = {
            "run_id": run_id,
            "filename": filename,
            "venue": venue,
            "max_iterations": max_iters,
            "evaluator_version": self.EVALUATOR_VERSION,
            "baseline_sha256": self.content_hash(baseline_content),
            "started_at": self._now(),
            "status": "RUNNING",
        }
        if metadata:
            manifest.update(metadata)
        self._write_json(run_dir / "manifest.json", manifest)
        return {"run_id": run_id, "run_dir": str(run_dir), "manifest": manifest}

    def record(self, run_id: str, *, iteration: int, stage: str, status: str,
               content: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        event = {
            "timestamp": self._now(),
            "iteration": iteration,
            "stage": stage,
            "status": status,
            "content_sha256": self.content_hash(content),
            "details": details or {},
        }
        with (self.root / run_id / "events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
        return event

    def record_stage_event(self, run_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """Append a typed graph event without changing the candidate ledger."""
        path = self.root / run_id / "stage_events.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
        return event

    def finish(self, run_id: str, *, status: str, final_content: str,
               iterations: int, reason: str = "", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        path = self.root / run_id / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest.update({
            "finished_at": self._now(),
            "status": status,
            "iterations": iterations,
            "final_sha256": self.content_hash(final_content),
            "reason": reason,
        })
        if metadata:
            manifest.update(metadata)
        self._write_json(path, manifest)
        return manifest

    @staticmethod
    def _write_json(path: Path, value: Dict[str, Any]) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
