"""
Tests for agents/meta_review_council.py — MetaReviewCouncil.run_alignment_cycle().

This council must never fabricate an empirical results table, a fixed
"decision" verdict, or a citation to a paper that doesn't genuinely exist in
the vault. It has no wired source of real measured results (no
ExperimentRecorder/ledger access, only the paper/concept/debate/draft vault
categories), so a draft missing a `\\begin{tabular}` table must be flagged as
missing required content, not patched with invented numbers (HANDOFF.md:
"if a claim cannot be measured, delete it, do not estimate"). Citation
expansion may only add a wikilink for a paper that is both present in the
vault paper corpus and named by the CitationExpander LLM call as relevant —
never an id it invents.

GEMINI_API_KEY/GROQ_API_KEY/OPENROUTER_API_KEY/NVIDIA_NIM_API_KEY are never
set in these tests, and generate_content is mocked directly wherever the
citation-expansion path is exercised, so no real network call is ever made.
"""

import os
import sys
from unittest.mock import patch

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

for _key in ["GEMINI_API_KEY", "GEMINI_API_KEYS", "GROQ_API_KEY", "OPENROUTER_API_KEY", "NVIDIA_NIM_API_KEY", "NVIDIA_API_KEY"]:
    os.environ.pop(_key, None)

from agents.meta_review_council import MetaReviewCouncil  # noqa: E402


def make_council(tmp_path):
    return MetaReviewCouncil(vault_path=str(tmp_path))


def add_paper(tmp_path, paper_id, title="Test Paper", body="Body text about the topic."):
    papers_dir = tmp_path / "01_Papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    (papers_dir / f"{paper_id}.md").write_text(f'---\ntitle: "{title}"\n---\n{body}')


def _collect_logs():
    logs = []

    def callback(stage, agent, message, data=None):
        logs.append({"stage": stage, "agent": agent, "message": message, "data": data})

    return logs, callback


class TestNoTableInDraft:
    """The draft has no results table and the council has no real measurements."""

    def test_no_fabricated_table_is_injected(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "## 6 Results\nSome prose about the approach.\n## References\n"
        result = council.run_alignment_cycle(draft, log_callback=cb)
        assert "\\begin{tabular}" not in result["revised_draft"]
        assert "74.2" not in result["revised_draft"]

    def test_decision_is_remediation_required(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        result = council.run_alignment_cycle("## 6 Results\nNo table here.\n", log_callback=cb)
        assert result["decision"] == "REMEDIATION_REQUIRED"

    def test_missing_requirements_lists_the_table(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        result = council.run_alignment_cycle("## 6 Results\nNo table here.\n", log_callback=cb)
        assert "empirical_results_table" in result["missing_requirements"]

    def test_gap_is_logged_not_silently_accepted(self, tmp_path):
        council = make_council(tmp_path)
        logs, cb = _collect_logs()
        council.run_alignment_cycle("## 6 Results\nNo table here.\n", log_callback=cb)
        rigor_logs = [l for l in logs if l["stage"] == "Rigor-Audit"]
        assert any("Refusing to fabricate" in l["message"] for l in rigor_logs)


class TestTablePresentInDraft:
    """A draft that already has a genuine table must not be flagged or altered."""

    def test_existing_table_is_left_untouched(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "## 6 Results\n\\begin{tabular}{ll}\nA & B\\\\\n\\end{tabular}\n"
        result = council.run_alignment_cycle(draft, log_callback=cb)
        assert result["revised_draft"].count("\\begin{tabular}") == 1

    def test_decision_is_approved_for_human_review(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "## 6 Results\n\\begin{tabular}{ll}\nA & B\\\\\n\\end{tabular}\n"
        result = council.run_alignment_cycle(draft, log_callback=cb)
        assert result["decision"] == "APPROVED_FOR_HUMAN_REVIEW"
        assert result["missing_requirements"] == []


class TestCitationExpansionWithPapersInVault:
    """Regression: list_files() returns dicts, not filename strings."""

    def test_does_not_crash_when_papers_exist_in_vault(self, tmp_path):
        add_paper(tmp_path, "arxiv_9999.0001")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        with patch("agents.meta_review_council.llm_router.generate_content", return_value="[]"):
            result = council.run_alignment_cycle("## References\n", log_callback=cb)
        assert result["success"] is True


class TestCitationExpansionGrounding:
    """Citations may only come from papers that genuinely exist in the vault."""

    def test_llm_approved_real_paper_is_cited(self, tmp_path):
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        with patch("agents.meta_review_council.llm_router.generate_content", return_value='["arxiv_1111.1111"]'):
            result = council.run_alignment_cycle("## References\n", log_callback=cb)
        assert "[[arxiv_1111.1111]]" in result["revised_draft"]

    def test_llm_naming_an_id_outside_the_vault_is_ignored(self, tmp_path):
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        # The LLM hallucinates an id that was never in the candidate catalog.
        with patch("agents.meta_review_council.llm_router.generate_content", return_value='["arxiv_9999.9999"]'):
            result = council.run_alignment_cycle("## References\n", log_callback=cb)
        assert "arxiv_9999.9999" not in result["revised_draft"]

    def test_no_papers_in_vault_adds_no_citations_and_does_not_call_llm(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        with patch("agents.meta_review_council.llm_router.generate_content") as mock_gen:
            result = council.run_alignment_cycle("## References\n", log_callback=cb)
            mock_gen.assert_not_called()
        assert result["final_citations"] == 0

    def test_llm_unavailable_is_flagged_as_a_warning_not_fabricated(self, tmp_path):
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        with patch("agents.meta_review_council.llm_router.generate_content", return_value="[Error] OPENROUTER_API_KEY not set."):
            result = council.run_alignment_cycle("## References\n", log_callback=cb)
        assert "citation_expansion_unavailable" in result["warnings"]
        assert "[[arxiv_1111.1111]]" not in result["revised_draft"]

    def test_dry_run_skips_the_live_llm_call(self, tmp_path):
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        with patch("agents.meta_review_council.llm_router.generate_content") as mock_gen:
            result = council.run_alignment_cycle("## References\n", log_callback=cb, is_dry_run=True)
            mock_gen.assert_not_called()
        assert "arxiv_1111.1111" not in result["revised_draft"]

    def test_already_cited_paper_is_not_resent_to_the_llm(self, tmp_path):
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "- [[arxiv_1111.1111]]\n## References\n"
        with patch("agents.meta_review_council.llm_router.generate_content") as mock_gen:
            council.run_alignment_cycle(draft, log_callback=cb)
            mock_gen.assert_not_called()

    def test_aliased_wikilink_counts_as_already_cited(self, tmp_path):
        """[[id|Custom Label]] must match VaultManager's own wikilink parsing,
        not be treated as a distinct, uncited reference (services/vault.py's
        wikilink_re strips the |Label half the same way)."""
        add_paper(tmp_path, "arxiv_1111.1111")
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "- [[arxiv_1111.1111|Some Custom Title]]\n## References\n"
        with patch("agents.meta_review_council.llm_router.generate_content") as mock_gen:
            result = council.run_alignment_cycle(draft, log_callback=cb)
            mock_gen.assert_not_called()
        assert result["final_citations"] == 1
        assert result["revised_draft"].count("arxiv_1111.1111") == 1


class TestSanitization:
    def test_banned_filler_phrases_are_replaced(self, tmp_path):
        council = make_council(tmp_path)
        _, cb = _collect_logs()
        draft = "This paper will delve into the tapestry of modern systems.\n## References\n"
        result = council.run_alignment_cycle(draft, log_callback=cb)
        assert "delve into" not in result["revised_draft"]
        assert "tapestry of" not in result["revised_draft"]
