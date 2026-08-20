"""Checks that a manuscript's claimed ResearchingOS workflow matches execution."""

from __future__ import annotations

import re
from typing import Any, Dict, List


REQUIRED_WORKFLOW_STAGES = (
    "Scout",
    "Analyst",
    "Engineer",
    "Statistician",
    "Reviewer #2",
    "Chairman",
    "Writer",
    "Red Team",
    "Peer Review",
    "Fact-check",
    "Checkmate",
    "Publisher",
)


def audit_researchingos_workflow(manuscript_markdown: str) -> Dict[str, Any]:
    """Fail closed when a paper presents an incomplete or stale internal workflow."""
    text = manuscript_markdown or ""
    lower = text.lower()
    claims_workflow = "researchingos multi-agent workflow" in lower or (
        "scout agent" in lower and "analyst agent" in lower
    )
    if not claims_workflow:
        return {
            "passed": True,
            "status": "NOT_APPLICABLE",
            "detail": "No ResearchingOS internal workflow claim detected",
            "missing_stages": [],
            "stale_linear_claim": False,
        }

    missing: List[str] = []
    for stage in REQUIRED_WORKFLOW_STAGES:
        aliases = [stage.lower()]
        if stage == "Reviewer #2":
            aliases.extend(("reviewer2", "reviewer # 2"))
        elif stage == "Fact-check":
            aliases.extend(("fact check", "factcheck"))
        elif stage == "Red Team":
            aliases.extend(("red-team", "redteam"))
        if not any(alias in lower for alias in aliases):
            missing.append(stage)

    stale_linear_claim = bool(re.search(
        r"\[?scout(?: agent)?\]?\s*[-=]+>\s*\[?analyst(?: agent)?\]?\s*[-=]+>\s*"
        r"\[?engineer(?: node| agent)?\]?\s*[-=]+>\s*\[?statistician\]?",
        lower,
    ))
    has_fanout = "||" in text or "parallel" in lower or "fan-out" in lower or "fanout" in lower
    passed = not missing and not stale_linear_claim and has_fanout
    problems = []
    if missing:
        problems.append("missing stages: " + ", ".join(missing))
    if stale_linear_claim:
        problems.append("stale linear Engineer -> Statistician claim")
    if not has_fanout:
        problems.append("parallel critique fan-out is not represented")
    return {
        "passed": passed,
        "status": "PASS" if passed else "NEEDS_REMEDIATION",
        "detail": "Workflow matches the ResearchingOS execution contract" if passed else "; ".join(problems),
        "missing_stages": missing,
        "stale_linear_claim": stale_linear_claim,
    }
