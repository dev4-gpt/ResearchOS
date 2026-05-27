"""
Tests for agents/council.py — CouncilOrchestrator dry-run path.

GEMINI_API_KEY is never set in these tests so the orchestrator operates
entirely with mock data (no real network or LLM calls happen).

Coverage targets:
  - __init__               : is_dry_run flag, vault wired to correct path
  - _call_gemini (dry-run) : returns mock string, no API call made
  - run_research (dry-run) : completes successfully, returns expected shape,
                             writes files to vault, fires log callbacks
  - run_research           : empty-papers guard (via search mock)
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Ensure backend package is importable
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def make_orchestrator(tmp_path):
    """Helper: build a CouncilOrchestrator in dry-run mode at tmp_path."""
    # Guarantee no API key leaks in from the real environment
    os.environ.pop("GEMINI_API_KEY", None)
    from agents.council import CouncilOrchestrator
    return CouncilOrchestrator(str(tmp_path))


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

class TestCouncilOrchestratorInit:
    def test_is_dry_run_true_without_api_key(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        assert orch.is_dry_run is True

    def test_vault_path_matches_tmp(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        assert orch.vault.vault_path == str(tmp_path)

    def test_search_service_is_initialised(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        from services.search import AcademicSearchService
        orch = make_orchestrator(tmp_path)
        assert isinstance(orch.search_service, AcademicSearchService)

    def test_is_dry_run_false_when_key_present(self, tmp_path, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "fake-key-for-init-test")
        # Patch genai.configure to avoid real API setup
        with patch("google.generativeai.configure"):
            from agents.council import CouncilOrchestrator
            orch = CouncilOrchestrator(str(tmp_path))
        assert orch.is_dry_run is False


# ---------------------------------------------------------------------------
# _call_gemini (dry-run)
# ---------------------------------------------------------------------------

class TestCallGeminiDryRun:
    def test_returns_string(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        result = orch._call_gemini("Analyst", "some prompt")
        assert isinstance(result, str)

    def test_mock_response_mentions_agent_key(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        result = orch._call_gemini("Scout", "prompt")
        assert "Scout" in result

    def test_all_agent_keys_produce_response(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        from agents.council import AGENT_PERSONAS
        for key in AGENT_PERSONAS:
            result = orch._call_gemini(key, "prompt")
            assert result, f"Empty response for agent key '{key}'"

    def test_dry_run_does_not_call_genai(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        with patch("google.generativeai.GenerativeModel") as mock_model:
            orch._call_gemini("Engineer", "prompt")
            mock_model.assert_not_called()


# ---------------------------------------------------------------------------
# run_research — dry-run end-to-end
# ---------------------------------------------------------------------------

class TestRunResearchDryRun:
    def _collect_logs(self):
        logs = []
        def callback(log):
            logs.append(log)
        return logs, callback

    def test_returns_dict(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("test topic", cb)
        assert isinstance(result, dict)

    def test_success_true(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("large language models", cb)
        assert result.get("success") is True

    def test_result_contains_project_id(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("transformers", cb)
        assert "project_id" in result
        assert result["project_id"].startswith("project_")

    def test_result_contains_papers_count(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("attention mechanisms", cb)
        assert "papers_count" in result
        assert result["papers_count"] > 0

    def test_result_contains_debate_file(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("reinforcement learning", cb)
        assert "debate_file" in result
        assert result["debate_file"].endswith(".md")

    def test_result_contains_draft_file(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("neural scaling laws", cb)
        assert "draft_file" in result
        assert result["draft_file"].endswith(".md")

    def test_paper_files_written_to_vault(self, tmp_path, monkeypatch):
        """Paper notes must land in 01_Papers/ of the temp vault."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("few shot learning", cb)
        papers_dir = tmp_path / "01_Papers"
        md_files = list(papers_dir.glob("*.md"))
        assert len(md_files) > 0, "No markdown files written to 01_Papers/"

    def test_debate_file_written_to_vault(self, tmp_path, monkeypatch):
        """The debate/synthesis file must land in 03_Debates/."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("knowledge distillation", cb)
        debates_dir = tmp_path / "03_Debates"
        expected = debates_dir / result["debate_file"]
        assert expected.is_file(), f"Debate file not found: {expected}"

    def test_draft_file_written_to_vault(self, tmp_path, monkeypatch):
        """The final draft must land in 04_Drafts/."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("model compression", cb)
        drafts_dir = tmp_path / "04_Drafts"
        expected = drafts_dir / result["draft_file"]
        assert expected.is_file(), f"Draft file not found: {expected}"

    def test_log_callback_fired_at_least_once(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("prompt tuning", cb)
        assert len(logs) > 0

    def test_log_entries_have_required_fields(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("chain of thought", cb)
        for entry in logs:
            for field in ("projectId", "timestamp", "stage", "agent", "message"):
                assert field in entry, f"Log entry missing '{field}': {entry}"

    def test_initialization_log_fires_first(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("in-context learning", cb)
        assert logs[0]["stage"] == "Initialization"

    def test_completion_log_fires_last(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("mixture of experts", cb)
        assert logs[-1]["stage"] == "Completion"

    def test_completion_log_data_contains_success(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("speculative decoding", cb)
        completion_log = logs[-1]
        assert completion_log["data"]["success"] is True

    def test_all_five_pipeline_stages_logged(self, tmp_path, monkeypatch):
        """Every stage name must appear at least once in the log stream."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("retrieval augmented generation", cb)
        stages_seen = {log["stage"] for log in logs}
        for expected_stage in ("Initialization", "Ingestion", "Critique", "Debate", "Synthesis", "Drafting", "Completion"):
            assert expected_stage in stages_seen, f"Stage '{expected_stage}' never logged"

    def test_dry_run_flag_reported_in_init_log(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        orch.run_research("RLHF", cb)
        init_log = logs[0]
        assert init_log["data"]["dryRun"] is True

    def test_topic_slug_used_in_filenames(self, tmp_path, monkeypatch):
        """The topic text must appear (sanitised) in both output filenames."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("slm efficiency", cb)
        assert "slm" in result["debate_file"]
        assert "slm" in result["draft_file"]

    def test_special_chars_in_topic_do_not_crash(self, tmp_path, monkeypatch):
        """Topics containing special characters must not cause exceptions."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        result = orch.run_research("LLM: efficiency & scaling (2024)", cb)
        assert result.get("success") is True

    def test_very_long_topic_slug_truncated(self, tmp_path, monkeypatch):
        """The topic slug used in filenames must not exceed 50 chars + prefix."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        orch = make_orchestrator(tmp_path)
        logs, cb = self._collect_logs()
        long_topic = "a " * 40  # 80-word topic
        result = orch.run_research(long_topic, cb)
        # Filenames include prefix like "debate_" or "review_" then the slug
        debate_slug = result["debate_file"].replace("debate_", "").replace(".md", "")
        draft_slug = result["draft_file"].replace("review_", "").replace(".md", "")
        assert len(debate_slug) <= 50
        assert len(draft_slug) <= 50


# ---------------------------------------------------------------------------
# run_research — no-papers guard
# ---------------------------------------------------------------------------

class TestRunResearchNoPapers:
    def test_returns_failure_when_no_papers_found(self, tmp_path, monkeypatch):
        """If the search returns nothing and dry-run mock is overridden, the
        pipeline must return success=False gracefully."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        from agents.council import CouncilOrchestrator
        orch = CouncilOrchestrator(str(tmp_path))

        # Override the dry-run mock papers with an empty list
        original_run = orch.run_research

        def patched_run(topic, log_callback):
            # Temporarily flip is_dry_run off so the non-mock branch runs,
            # but mock the search service to return nothing.
            orch.is_dry_run = False
            with patch.object(orch.search_service, "run_combined_search", return_value=[]), \
                 patch.object(orch.search_service, "fetch_arxiv_by_ids", return_value=[]), \
                 patch.object(orch, "_call_gemini", return_value='["empty query"]'):
                result = original_run(topic, log_callback)
            orch.is_dry_run = True
            return result

        logs = []
        result = patched_run("obscure topic with no papers", logs.append)
        assert result.get("success") is False
