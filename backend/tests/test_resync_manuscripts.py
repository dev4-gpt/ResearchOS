"""The re-sync pass rewrites numbers inside finished manuscripts (ERR-072).

The cost of a bug here is a paper that states a value no run produced, which is
the exact failure the provenance gate was built to catch downstream. These tests
pin the two rules that keep it safe: what a literal is allowed to match, and what
the pass must refuse to decide on its own.
"""
import json
import os
import sys

import pytest

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                       "scripts", "experiments"))
sys.path.insert(0, SCRIPTS)

import resync_manuscripts as rs  # noqa: E402


# --------------------------------------------------------- literal generation

def literals(value):
    return [lit for lit, _decimals in rs.candidate_literals(value)]


def test_exact_integer_is_offered_plainly():
    assert "103" in literals(103.0)


def test_faithful_rounding_with_enough_digits_is_offered():
    # The drafts spell 4.0905 ms as '4.09'; that has to keep matching.
    assert "4.09" in literals(4.0905)
    assert "4.0905" in literals(4.0905)


def test_short_inexact_rounding_is_refused():
    """9.86 must never be allowed to match a bare '10'.

    '10' occurs throughout these manuscripts as a year, a section number and an
    unrelated count. Substituting all of them because a guard rate moved is
    silent corruption, and it is not recoverable by reading the diff.
    """
    assert "10" not in literals(9.86)
    assert "41" not in literals(40.57)
    assert "35" not in literals(35.26)


def test_small_signed_value_keeps_its_manuscript_spelling():
    assert "-0.0038" in literals(-0.00379)


# ------------------------------------------------------------------- locating

def test_locate_ignores_numbers_embedded_in_longer_numbers():
    text = "n = 103 queries, not 1039 and not 0.1034"
    assert rs.locate(text, "103") == [text.index("103")]


def test_locate_finds_every_standalone_occurrence():
    text = "103 here and 103 there"
    assert len(rs.locate(text, "103")) == 2


# -------------------------------------------------------- seeding and rewrite

@pytest.fixture
def draft(tmp_path, monkeypatch):
    """Point the module at a throwaway drafts directory."""
    drafts = tmp_path / "drafts"
    drafts.mkdir()
    monkeypatch.setattr(rs, "DRAFTS", str(drafts))
    monkeypatch.setattr(rs, "SIDECAR_DIR", str(drafts / ".sync"))

    def write(stem, body):
        (drafts / f"{stem}.md").write_text(body, encoding="utf-8")
        return stem
    return write


def test_seed_then_resync_updates_every_occurrence(draft):
    stem = draft("paper", "MRR 0.8739 in the abstract.\nAgain: 0.8739 in the table.\n")
    old = {"mrr_bm25": {"metric": "mrr_bm25", "value": 0.8739, "n": 103}}
    new = {"mrr_bm25": {"metric": "mrr_bm25", "value": 0.9128, "n": 124}}

    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    text, changes, blocked = rs.resync(stem, anchors, new)

    assert blocked == []
    assert "0.8739" not in text
    assert text.count("0.9128") == 2
    assert changes[0]["occurrences"] == 2


def test_resync_is_idempotent(draft):
    """Running twice must be a no-op, which is the whole point (ERR-072).

    The previous generators consumed their own anchors, so a second run could
    only skip. Here the anchor is the literal last written, so the second run
    finds nothing to do and leaves the draft byte-identical.
    """
    stem = draft("paper", "The rate is 46.34\\% overall.\n")
    old = {"rate": {"metric": "rate", "value": 46.34}}
    new = {"rate": {"metric": "rate", "value": 43.96}}

    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    text, changes, _ = rs.resync(stem, anchors, new)
    open(rs.draft_path(stem), "w", encoding="utf-8").write(text)
    assert len(changes) == 1

    text_again, changes_again, blocked_again = rs.resync(stem, anchors, new)
    assert changes_again == []
    assert blocked_again == []
    assert text_again == text


def test_shared_literal_is_applied_when_claimants_still_agree(draft):
    """Twelve retrieval metrics share the sample size 103. That is not ambiguity."""
    stem = draft("paper", "Reported on 103 unseen queries; 103 in total.\n")
    old = {"a": {"metric": "a", "value": 1.0, "n": 103},
           "b": {"metric": "b", "value": 2.0, "n": 103}}
    new = {"a": {"metric": "a", "value": 1.0, "n": 124},
           "b": {"metric": "b", "value": 2.0, "n": 124}}

    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    text, changes, blocked = rs.resync(stem, anchors, new)

    assert blocked == []
    assert text.count("124") == 2
    assert len(changes) == 1


def test_shared_literal_is_refused_once_claimants_diverge(draft):
    """P@5 was 94.17 for both systems and is now 97.58 and 98.39.

    One spelling has to become two, and which sentence gets which is an
    authoring decision. The pass must hold, not guess -- and must leave the
    draft untouched while it holds.
    """
    stem = draft("paper", "| BM25 | 94.17 |\n| PPR | 94.17 |\n")
    old = {"p5_bm25": {"metric": "p5_bm25", "value": 94.1748},
           "p5_ppr": {"metric": "p5_ppr", "value": 94.1748}}
    new = {"p5_bm25": {"metric": "p5_bm25", "value": 97.5806},
           "p5_ppr": {"metric": "p5_ppr", "value": 98.3871}}

    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    text, changes, blocked = rs.resync(stem, anchors, new)

    assert changes == []
    assert text.count("94.17") == 2
    assert len(blocked) == 1
    assert blocked[0]["reason"] == "claimants disagree"


def test_metric_dropped_from_the_run_is_reported_not_guessed(draft):
    stem = draft("paper", "The value is 46.34 overall.\n")
    old = {"rate": {"metric": "rate", "value": 46.34}}

    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    text, changes, blocked = rs.resync(stem, anchors, {})

    assert changes == []
    assert "46.34" in text
    assert blocked[0]["reason"] == "no longer recorded"


def test_hand_edited_draft_is_reported_not_overwritten(draft):
    stem = draft("paper", "An author rewrote this sentence entirely.\n")
    old = {"rate": {"metric": "rate", "value": 46.34}}
    anchors = [{"literal": "46.34", "lines": [1],
                "claims": [{"metric": "rate", "field": "value", "decimals": 2}]}]

    text, changes, blocked = rs.resync(stem, anchors, {"rate": {"value": 43.96}})

    assert changes == []
    assert text == "An author rewrote this sentence entirely.\n"
    assert "edited by hand" in blocked[0]["reason"]


def test_direction_words_near_a_changed_value_are_surfaced(draft):
    """A substitution cannot turn 'improves' into 'does not improve'."""
    text = "Diffusion improves MRR to 0.9128 over the baseline.\n"
    flagged = rs.stale_prose(text, [{"lines": [1], "was": "0.8739", "now": "0.9128"}])
    assert flagged and "improves" in flagged[0]


def test_sidecar_round_trips_as_json(draft):
    stem = draft("paper", "MRR 0.8739.\n")
    old = {"mrr": {"metric": "mrr", "value": 0.8739}}
    anchors = rs.seed(old, open(rs.draft_path(stem), encoding="utf-8").read())
    assert json.loads(json.dumps({"anchors": anchors}))["anchors"] == anchors


# ------------------------------------------------------- quoted source material

def test_quoted_abstract_is_never_substituted_into():
    """The real near-miss: p3 records 175 mutants; GPT-3 has 175 billion parameters.

    Both numbers are spelled '175'. One of them belongs to a quotation of a paper
    this manuscript cites. Rewriting it would put a number no one measured into
    someone else's sentence, under their name.
    """
    text = ("We generated 175 mutants for the substitution operator.\n"
            "**Language Models are Few-Shot Learners** [[arxiv_2005.14165]] reports: "
            "We train GPT-3, a 175-billion parameter autoregressive model.\n")
    hits = rs.locate(text, "175")
    assert len(hits) == 1
    assert hits[0] == text.index("175 mutants")


def test_citation_keys_are_protected():
    text = "See [[crossref_10.1175_JAS]] for the argument; we measured 175 mutants.\n"
    hits = rs.locate(text, "175")
    assert len(hits) == 1
    assert hits[0] == text.index("175 mutants")


def test_fenced_blocks_are_protected():
    text = "We measured 943 mutants.\n```\nseed = 943\n```\n"
    assert rs.locate(text, "943") == [text.index("943 mutants")]


def test_blockquotes_are_protected():
    text = "We measured 943 mutants.\n> Their table reports 943 cases.\n"
    assert rs.locate(text, "943") == [text.index("943 mutants")]


def test_yaml_frontmatter_is_protected():
    """checkmate_score: "100.0" is pipeline metadata, and a known false green.

    It collides with a real syntactic-validity percentage of 100.0. Rewriting it
    would silently edit an audit score to match an unrelated experiment.
    """
    text = ('---\ncheckmate_score: "100.0"\n---\n\n'
            'Syntactic validity was 100.0\\% for that operator.\n')
    hits = rs.locate(text, "100.0")
    assert len(hits) == 1
    assert hits[0] > text.index("---\n\n")


def test_latex_thousands_spelling_is_matched():
    """The drafts write 36032 as '36{,}032' so LaTeX sets the comma in maths mode.

    Without this spelling p3's abstract could not be matched at all, and its
    AST-node count stayed stale while the appendix table beside it was current.
    """
    assert "36{,}032" in literals(36032.0)
    assert rs.grouped_spelling("38413") == "38{,}413"
    assert rs.grouped_spelling("944") == "944"
    assert rs.grouped_spelling("-1234.5") == "-1{,}234.5"


def test_grouped_literal_is_located_and_replaced(tmp_path, monkeypatch):
    drafts = tmp_path / "d"
    drafts.mkdir()
    monkeypatch.setattr(rs, "DRAFTS", str(drafts))
    (drafts / "paper.md").write_text("a corpus of 36{,}032 AST nodes\n", encoding="utf-8")

    anchors = rs.seed({"nodes": {"metric": "nodes", "value": 36032}},
                      (drafts / "paper.md").read_text(encoding="utf-8"))
    text, changes, blocked = rs.resync("paper", anchors, {"nodes": {"value": 38413}})

    assert blocked == []
    assert "38{,}413" in text
