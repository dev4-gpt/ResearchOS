import json
from types import SimpleNamespace

import httpx
import pytest

from services.scout_discovery import ScoutDiscovery
from services.search import AcademicSearchService
from services.spend_ledger import SpendLedger


@pytest.fixture(autouse=True)
def scout_spending(tmp_path, monkeypatch):
    path = tmp_path / 'spend.sqlite3'
    SpendLedger(path, 1)
    monkeypatch.setenv('RESEARCHINGOS_SPEND_LEDGER', str(path))
    monkeypatch.setenv('RESEARCHINGOS_SPEND_CAP_USD', '1')
    monkeypatch.setenv('RESEARCHINGOS_NEBIUS_APPROVED_MODELS', 'fixture-model')
    monkeypatch.setenv('NEBIUS_MODEL', 'fixture-model')
    monkeypatch.setenv('RESEARCHINGOS_NEBIUS_TOKEN_PRICE_CEILING', '100')
    monkeypatch.setenv('RESEARCHINGOS_TAVILY_SEARCH_PRICE_CEILING', '0.05')


def test_disabled_or_missing_credentials_make_no_calls(monkeypatch):
    monkeypatch.delenv("SCOUT_NEBIUS_ENABLED", raising=False)
    monkeypatch.delenv("SCOUT_TAVILY_ENABLED", raising=False)
    monkeypatch.setenv("NEBIUS_API_KEY", "test")
    monkeypatch.setenv("TAVILY_API_KEY", "test")
    monkeypatch.setattr("services.scout_discovery.OpenAI", lambda **kw: pytest.fail("unexpected Nebius call"))
    monkeypatch.setattr(httpx, "post", lambda *a, **kw: pytest.fail("unexpected Tavily call"))
    service = ScoutDiscovery()
    assert service.plan_queries("topic") is None
    assert service.search_leads("topic") == []
    monkeypatch.setenv("SCOUT_NEBIUS_ENABLED", "true")
    monkeypatch.setenv("SCOUT_TAVILY_ENABLED", "true")
    monkeypatch.delenv("NEBIUS_API_KEY")
    monkeypatch.delenv("TAVILY_API_KEY")
    assert service.plan_queries("topic") is None
    assert service.search_leads("topic") == []


@pytest.mark.parametrize("content,expected", [
    ('["first", "second"]', ["first", "second"]),
    ("not JSON", None), ('["valid", 3]', None), (json.dumps(["x"] * 7), None),
    ('["https://example.com"]', None),
])
def test_nebius_plan_validation(monkeypatch, content, expected):
    monkeypatch.setenv("SCOUT_NEBIUS_ENABLED", "true")
    monkeypatch.setenv("NEBIUS_API_KEY", "test")
    calls = []
    def client(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kw:
            SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))]))))
    monkeypatch.setattr("services.scout_discovery.OpenAI", client)
    assert ScoutDiscovery().plan_queries("a topic") == expected
    assert 0 < calls[0]["timeout"] <= 20 and calls[0]["max_retries"] == 0


def test_provider_failures_and_tavily_limits(monkeypatch):
    monkeypatch.setenv("SCOUT_NEBIUS_ENABLED", "true")
    monkeypatch.setenv("SCOUT_TAVILY_ENABLED", "true")
    monkeypatch.setenv("NEBIUS_API_KEY", "test")
    monkeypatch.setenv("TAVILY_API_KEY", "test")
    def fail(*a, **kw):
        raise httpx.TimeoutException("timeout")
    monkeypatch.setattr("services.scout_discovery.OpenAI", fail)
    monkeypatch.setattr(httpx, "post", fail)
    service = ScoutDiscovery()
    assert service.plan_queries("topic") is None
    assert service.search_leads("topic") == []
    def post(url, **kwargs):
        assert 0 < kwargs["timeout"] <= 20
        assert kwargs["json"]["max_results"] == 5
        assert kwargs["json"]["search_depth"] == "advanced"
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"results": [{"url": str(i)} for i in range(8)]})
    monkeypatch.setattr(httpx, "post", post)
    assert len(service.search_leads("topic")) == 5


def test_only_resolved_arxiv_leads_enter_ranked_results(monkeypatch):
    search = AcademicSearchService()
    monkeypatch.setattr(search.openresearch.__class__, "available", property(lambda self: False))
    for name in ("arxiv", "openalex", "semanticscholar", "europepmc", "crossref", "doaj", "plos", "hal", "pubmed", "dblp", "github", "huggingface"):
        monkeypatch.setattr(search, f"search_{name}", lambda *a, **kw: [])
    def resolve(ids):
        assert ids == ["2405.01543", "2401.00001"]
        return [{"id": "arxiv:2405.01543", "title": "Paper", "authors": [], "abstract": "arxiv abstract", "url": "https://arxiv.org/abs/2405.01543", "published": "2024", "citations": 0, "source": "arXiv"}]
    monkeypatch.setattr(search, "fetch_arxiv_by_ids", resolve)
    papers = search.run_combined_search("topic", tavily_leads=[
        {"url": "https://arxiv.org/pdf/2405.01543v2.pdf", "content": "untrusted snippet"},
        {"url": "https://arxiv.org/abs/2401.00001"},
        {"url": "https://example.org/abs/2402.00001"},
        {"url": "https://arxiv.org.evil.test/abs/2402.00001"},
    ])
    assert len(papers) == 1
    assert papers[0]["abstract"] == "arxiv abstract"
    assert papers[0]["discovery_urls"] == ["https://arxiv.org/pdf/2405.01543v2.pdf"]
    search.client.close()


def test_scout_caps_tavily_calls_and_falls_back(tmp_path, monkeypatch):
    from agents.council import CouncilOrchestrator
    monkeypatch.setenv("RESEARCHINGOS_RUN_MODE", "dry_run")
    orch = CouncilOrchestrator(str(tmp_path / "vault"), memory_file_path=str(tmp_path / "memory.json"))
    orch.is_dry_run = False
    monkeypatch.setattr(orch.scout_discovery, "plan_queries", lambda topic: None)
    monkeypatch.setattr(orch, "_call_gemini", lambda *a, **kw: json.dumps([f"query {i}" for i in range(8)]))
    calls = []
    monkeypatch.setattr(orch.scout_discovery, "search_leads", lambda query: calls.append(query) or [])
    monkeypatch.setattr(orch.search_service, "run_combined_search", lambda *a, **kw: [])
    result = orch._run_ingestion_critique_debate("a sufficiently long research topic with many words", lambda _: None)
    assert result["success"] is False
    assert len(calls) == 6


def test_dry_run_skips_optional_providers(tmp_path, monkeypatch):
    from agents.council import CouncilOrchestrator
    monkeypatch.setenv("RESEARCHINGOS_RUN_MODE", "dry_run")
    orch = CouncilOrchestrator(str(tmp_path / "vault"), memory_file_path=str(tmp_path / "memory.json"))
    monkeypatch.setattr(orch.scout_discovery, "plan_queries", lambda *_: pytest.fail("Nebius called in dry run"))
    monkeypatch.setattr(orch.scout_discovery, "search_leads", lambda *_: pytest.fail("Tavily called in dry run"))
    def stop_at_ingestion(*args, **kwargs):
        raise RuntimeError("reached ingestion")
    monkeypatch.setattr(orch.vault, "save_markdown", stop_at_ingestion)
    with pytest.raises(RuntimeError, match="reached ingestion"):
        orch._run_ingestion_critique_debate("a sufficiently long research topic with many words", lambda _: None)
