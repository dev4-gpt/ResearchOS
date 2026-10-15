"""Optional adapter to alphaXiv/OpenResearch's public orx CLI.

Discovery is metadata, never verified evidence. PDF ingestion and publication
gates remain owned by ResearchingOS. No shell or arbitrary command endpoint.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class OpenResearchError(RuntimeError):
    pass


class OpenResearchService:
    def __init__(self, binary_path: str | None = None):
        self.binary_path = binary_path

    def _binary(self) -> str | None:
        explicit = self.binary_path or os.getenv("OPENRESEARCH_BIN_PATH")
        if explicit:
            return shutil.which(explicit)
        local = PROJECT_ROOT / ".tools" / "openresearch" / "orx"
        return shutil.which(str(local)) or shutil.which("orx")

    @property
    def enabled(self) -> bool:
        return os.getenv("OPENRESEARCH_ENABLED", "true").lower() not in {"0", "false", "no", "off"}

    @property
    def available(self) -> bool:
        return self.enabled and self._binary() is not None

    def _run(self, *args: str, timeout: int = 20) -> str:
        binary = self._binary()
        if not self.enabled:
            raise OpenResearchError("OpenResearch is disabled by OPENRESEARCH_ENABLED.")
        if not binary:
            raise OpenResearchError("OpenResearch CLI is not installed. Install orx or set OPENRESEARCH_BIN_PATH.")
        try:
            result = subprocess.run(
                [binary, "--no-telemetry", *args], cwd=PROJECT_ROOT,
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise OpenResearchError(f"OpenResearch timed out after {timeout} seconds.") from exc
        except OSError as exc:
            raise OpenResearchError("OpenResearch CLI could not be started.") from exc
        if result.returncode:
            raise OpenResearchError(result.stderr.strip()[:1000] or "OpenResearch command failed.")
        return result.stdout.strip()

    def _json_list(self, *args: str) -> list[dict]:
        try:
            value = json.loads(self._run(*args))
        except json.JSONDecodeError as exc:
            raise OpenResearchError("OpenResearch returned invalid JSON; check the installed CLI version.") from exc
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise OpenResearchError("OpenResearch returned an unexpected result format.")
        return value

    def status(self) -> dict:
        result = {
            "installed": self._binary() is not None, "enabled": self.enabled,
            "available": False, "version": None,
            "repository_url": "https://github.com/alphaXiv/OpenResearch",
            "dashboard_url": "http://127.0.0.1:4791",
        }
        if not self.available:
            return result
        try:
            result["version"] = self._run("--version", timeout=3)
            result["available"] = True
        except OpenResearchError as exc:
            result["error"] = str(exc)
        return result

    def discover(self, query: str, strategy: str = "keyword", limit: int = 10) -> list[dict]:
        if strategy not in {"keyword", "embedding"}:
            raise ValueError("strategy must be keyword or embedding")
        if not query.strip() or len(query) > 2000 or not 1 <= limit <= 50:
            raise ValueError("Supply a query of 1–2000 characters and a limit of 1–50.")
        # The terminator keeps a user query beginning with '-' a positional argument.
        hits = self._json_list("discover", strategy, "--limit", str(limit), "--", query)
        papers = []
        for hit in hits[:limit]:
            paper_id = str(hit.get("id", ""))
            title = hit.get("title")
            if hit.get("source") != "alphaxiv" or not isinstance(title, str) or not title.strip():
                continue
            # Accept only actual arXiv identifiers, including legacy identifiers.
            if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-zA-Z.-]+/\d{7})(?:v\d+)?", paper_id):
                continue
            paper_id = re.sub(r"v\d+$", "", paper_id)
            papers.append({
                "id": f"arxiv:{paper_id}", "title": title.strip(),
                "authors": [], "abstract": hit.get("abstract") or "",
                "url": f"https://arxiv.org/abs/{paper_id}",
                "published": hit.get("publicationDate") or "",
                "citations": 0, "source": "alphaXiv (OpenResearch)",
                "discovery_strategy": strategy,
                "discovery_url": f"https://www.alphaxiv.org/abs/{paper_id}",
                "full_pdf_ingested": False,
            })
        return papers

    def search_for_scout(self, query: str, strategy: str, limit: int) -> list[dict]:
        """Fail independently per retrieval strategy without stopping other sources."""
        if not self.available:
            return []
        try:
            return self.discover(query, strategy, min(limit, 50))
        except OpenResearchError as exc:
            logger.warning("OpenResearch %s discovery unavailable: %s", strategy, exc)
            return []

    @staticmethod
    def _identifier(value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,199}", value):
            raise ValueError("Invalid OpenResearch identifier.")
        return value

    def projects(self) -> list[dict]:
        return self._json_list("projects", "--json")

    def project(self, project_id: str) -> dict:
        project_id = self._identifier(project_id)
        return {
            "project_id": project_id,
            "tree": self._run("project", "view", project_id),
            "runs": self._run("runs", project_id),
        }
