import os
import sys


BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from services.workflow_audit import audit_researchingos_workflow


STALE_WORKFLOW = """> ResearchingOS Multi-Agent Workflow:
> [Scout Agent] --> [Analyst Agent] --> [Engineer Node] --> [Statistician]
> (Literature RRF) (AST Parsing) (Patch Synthesis) (SMT Verification)
> Closed-Loop Repair Feedback Loop Active
"""


CORRECT_WORKFLOW = """> ResearchingOS Multi-Agent Workflow:
> [Scout] --> [Analyst] --> {[Engineer] || [Statistician] || [Reviewer #2]}
> --> [Chairman Synthesis]
> [Planner] --> [Writer] --> [Assembler] --> [Red Team] --> [Peer Review]
> [Fact Check] --> [Checkmate/Layout] --> [Originality + Value + Venue Gates] --> [HITL Publisher]
"""


def test_stale_workflow_is_rejected_with_actionable_reasons():
    report = audit_researchingos_workflow(STALE_WORKFLOW)

    assert report["passed"] is False
    assert report["stale_linear_claim"] is True
    assert "Reviewer #2" in report["missing_stages"]
    assert "Chairman" in report["missing_stages"]
    assert "parallel critique fan-out" in report["detail"]


def test_correct_workflow_matches_execution_contract():
    report = audit_researchingos_workflow(CORRECT_WORKFLOW)

    assert report == {
        "passed": True,
        "status": "PASS",
        "detail": "Workflow matches the ResearchingOS execution contract",
        "missing_stages": [],
        "stale_linear_claim": False,
    }


def test_audit_is_not_applicable_without_internal_workflow_claim():
    report = audit_researchingos_workflow("## Methods\nWe evaluate three systems.")

    assert report["passed"] is True
    assert report["status"] == "NOT_APPLICABLE"
