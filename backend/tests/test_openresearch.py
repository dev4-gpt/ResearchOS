"""CLI contract, fault isolation, and Scout integration without external calls."""
import json
import subprocess
import sys
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from services.openresearch import OpenResearchError, OpenResearchService


@pytest.fixture
def service(monkeypatch):
    monkeypatch.setenv("OPENRESEARCH_ENABLED", "true")
    return OpenResearchService(sys.executable)


def test_discovery_contract_preserves_query_and_does_not_invent_evidence(service, monkeypatch):
    calls = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return SimpleNamespace(returncode=0, stderr="", stdout=json.dumps([{
            "source": "alphaxiv", "id": "2405.01543v2", "title": "A paper",
            "abstract": "Original abstract", "publicationDate": "2024-05-02",
            "votes": 10000,
        }]))

    monkeypatch.setattr(subprocess, "run", run)
    query = "--help; $(touch /tmp/should-not-exist)"
    papers = service.discover(query, "embedding", 2)
    assert calls[0][0][-2:] == ["--", query]
    assert "--no-telemetry" in calls[0][0]
    assert not calls[0][1].get("shell", False)
    assert papers[0]["id"] == "arxiv:2405.01543"
    assert papers[0]["citations"] == 0  # Votes are not citations.
    assert papers[0]["authors"] == []  # The CLI does not supply authors.
    assert papers[0]["full_pdf_ingested"] is False
    assert papers[0]["url"] == "https://arxiv.org/abs/2405.01543"


@pytest.mark.parametrize("output", ["not json", '{}', '["wrong shape"]'])
def test_incompatible_cli_output_is_explicit(service, monkeypatch, output):
    monkeypatch.setattr(service, "_run", lambda *args: output)
    with pytest.raises(OpenResearchError):
        service.projects()


def test_bad_ids_are_not_promoted_to_papers(service, monkeypatch):
    monkeypatch.setattr(service, "_json_list", lambda *args: [
        {"source": "alphaxiv", "id": "invented", "title": "Invalid"},
        {"source": "alphaxiv", "id": "hep-th/9901001", "title": "Legacy"},
    ])
    assert [p["id"] for p in service.discover("topic")] == ["arxiv:hep-th/9901001"]


def test_missing_or_disabled_cli_skips_scout_and_reports_unavailable(service, monkeypatch):
    monkeypatch.setenv("OPENRESEARCH_ENABLED", "false")
    assert service.search_for_scout("topic", "keyword", 5) == []
    assert service.status()["available"] is False
    with pytest.raises(OpenResearchError, match="disabled"):
        service.projects()
    monkeypatch.setenv("OPENRESEARCH_ENABLED", "true")
    monkeypatch.setattr(service, "_binary", lambda: None)
    assert service.status()["installed"] is False
    assert service.search_for_scout("topic", "keyword", 5) == []


def test_timeout_has_no_fake_results(service, monkeypatch):
    def run(*args, **kwargs):
        raise subprocess.TimeoutExpired("orx", 20)
    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(OpenResearchError, match="timed out"):
        service.discover("topic")
    assert service.search_for_scout("topic", "keyword", 5) == []


def test_scout_uses_both_strategies_and_existing_pdf_path(service, monkeypatch):
    from services.search import AcademicSearchService
    search = AcademicSearchService()
    search.openresearch = service
    for name in ("arxiv", "openalex", "semanticscholar", "europepmc", "crossref",
                 "doaj", "plos", "hal", "pubmed", "dblp", "github", "huggingface"):
        monkeypatch.setattr(search, f"search_{name}", lambda *args, **kwargs: [])
    calls = []

    def discover(query, strategy, limit):
        calls.append(strategy)
        if strategy == "keyword":
            raise OpenResearchError("source temporarily unavailable")
        return [{"id": "arxiv:2405.01543", "title": "Found semantically", "abstract": "Abstract",
                 "authors": [], "url": "https://arxiv.org/abs/2405.01543", "published": "2024",
                 "citations": 0, "source": "alphaXiv (OpenResearch)"}]

    monkeypatch.setattr(service, "discover", discover)
    papers = search.run_combined_search("topic", 5)
    assert sorted(calls) == ["embedding", "keyword"]
    assert len(papers) == 1
    monkeypatch.setattr(search.pdf_extractor, "extract_text_from_url",
                        lambda url: {"success": True, "full_text": "Actual PDF text"})
    assert search.fetch_full_text_for_paper(papers[0])["full_pdf_ingested"] is True
    search.client.close()


def test_api_validates_requests_and_reports_dependency_failure(service, monkeypatch):
    import openresearch_api
    monkeypatch.setattr(openresearch_api, "service", service)
    app = FastAPI()
    app.include_router(openresearch_api.router)
    with TestClient(app) as client:
        assert client.post('/api/openresearch/discover', json={"query": "x", "limit": 1000}).status_code == 422
        assert client.post('/api/openresearch/discover', json={"query": "x", "strategy": "shell"}).status_code == 422
        assert client.get('/api/openresearch/projects/--help').status_code == 400
        monkeypatch.setenv("OPENRESEARCH_ENABLED", "false")
        assert client.get('/api/openresearch/status').status_code == 200
        assert client.get('/api/openresearch/projects').status_code == 503


def test_project_details_use_supported_commands(service, monkeypatch):
    calls = []
    def run(*args):
        calls.append(args)
        return "Evidence from CLI"
    monkeypatch.setattr(service, "_run", run)
    assert service.project("local_123")["runs"] == "Evidence from CLI"
    assert calls == [("project", "view", "local_123"), ("runs", "local_123")]
