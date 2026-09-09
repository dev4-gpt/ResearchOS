"""Tests for Vercel Labs fx agent harness integration in ResearchingOS."""

from services.fx_bridge import FXBridge
from services.fx_mcp_server import ResearchOSMCPServer
from services.feynman_service import FeynmanService


def test_fx_bridge_detection_and_status():
    bridge = FXBridge()
    status = bridge.get_status()
    assert "installed" in status
    assert "mode" in status
    assert status["mode"] in ["native", "emulated"]
    assert status["acp_supported"] is True
    assert status["mcp_client_capable"] is True
    assert "version" in status


def test_fx_dispatch_research_emulated():
    bridge = FXBridge()
    res = bridge.dispatch_research("Analyze sparse mixture-of-experts routing stability")
    assert res["success"] is True
    assert "engine" in res
    assert "synthesis" in res or "summary" in res or "raw_output" in res
    if res.get("engine") == "emulated_acp_subagent":
        assert len(res.get("key_findings", [])) >= 2
        assert res.get("execution_latency_ms", 0) < 50


def test_fx_parallel_paper_ingestion():
    bridge = FXBridge()
    papers = [
        {"filename": "paper_a.md", "title": "Paper A", "content": "Equation: $$E=mc^2$$ with N=100"},
        {"filename": "paper_b.md", "title": "Paper B", "content": "Descriptive text without math."},
    ]
    results = bridge.parallel_paper_ingestion(papers)
    assert len(results) == 2
    assert results[0]["has_formal_equations"] is True
    assert results[1]["has_formal_equations"] is False
    assert results[0]["status"] == "INGESTED"


def test_fx_mcp_server_schemas():
    server = ResearchOSMCPServer()
    tools = server.get_tool_definitions()
    tool_names = [t["name"] for t in tools]
    assert "researchos_vault_query" in tool_names
    assert "researchos_fact_check" in tool_names
    assert "researchos_feynman_code_audit" in tool_names
    assert "researchos_simulated_peer_review" in tool_names

    for tool in tools:
        assert "inputSchema" in tool
        assert "description" in tool


def test_fx_mcp_server_call_vault_query():
    server = ResearchOSMCPServer()
    res = server.call_tool("researchos_vault_query", {"query": "agent", "category": "all"})
    assert "total_matches" in res
    assert "matches" in res


def test_feynman_service_fx_integration():
    feynman = FeynmanService()
    res = feynman.research_topic_with_fx("state space models")
    assert res["success"] is True
    assert "engine" in res
