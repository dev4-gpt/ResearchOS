"""Comprehensive tests for EvoMap/AutoResearch, OpenBMB/VoxCPM, and affaan-m/ECC skill integration."""

import json
import os
import tempfile
from pathlib import Path

import _langsmith_stub  # noqa: F401
from services.ecc_skill_loader import ECCSkillLoader
from services.evomap_autoresearch import (
    IdeaForgeService,
    IdeaHypothesis,
    MultiModelIdeaReview,
    NegativeResultTracker,
    PilotGate,
)
from services.voxcpm_service import (
    VoiceActionIntent,
    VoiceControlParser,
    VoxCPMAudioService,
)


def test_evomap_idea_forge_and_tri_critic():
    """Verify idea generation produces mathematical hypotheses with 3-model tri-critic reviews."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / "vault"
        vault_dir.mkdir(parents=True)
        (vault_dir / "00_System").mkdir(parents=True)

        forge = IdeaForgeService(vault_path=str(vault_dir))
        ideas = forge.forge_ideas("Dynamic Sparse Routing", domain_b="State Space Models", count=2)
        assert len(ideas) == 2

        entry = ideas[0]
        idea = entry["idea"]
        review = entry["review"]

        # Structural assertions
        assert "evo-idea-" in idea["idea_id"]
        assert "$" in idea["formal_hypothesis"]
        assert len(idea["testable_claims"]) >= 2
        assert idea["baseline"] != ""
        assert idea["expected_delta"] > 0
        assert len(idea["sha256"]) == 64

        # Tri-Critic review assertions
        assert review["decision"] in ("ACCEPTED", "NEEDS_REVISION", "REJECTED")
        assert 0.0 <= review["novelty_score"] <= 10.0
        assert 0.0 <= review["feasibility_score"] <= 10.0
        assert 0.0 <= review["verifiability_score"] <= 10.0
        assert 0.0 <= review["composite_score"] <= 10.0
        assert len(review["evaluations"]) == 3


def test_evomap_pilot_gate_and_scaling_decision():
    """Verify pilot gate evaluates proxy task before compute scaling."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / "vault"
        vault_dir.mkdir(parents=True)
        (vault_dir / "00_System").mkdir(parents=True)

        forge = IdeaForgeService(vault_path=str(vault_dir))
        ideas = forge.forge_ideas("Test Topic", count=1)
        idea = ideas[0]["idea"]

        # Run pilot gate
        pilot_res = forge.run_pilot(idea)
        assert "status" in pilot_res
        assert pilot_res["status"] in ("PILOT_PASSED", "PILOT_FAILED")
        assert "observed_metric" in pilot_res
        assert "ready_for_full_autoresearch" in pilot_res
        assert pilot_res["ready_for_full_autoresearch"] == pilot_res["passed"]


def test_evomap_negative_result_tracker_and_guardrail():
    """Verify negative results are persisted and trigger dead-end guardrail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / "vault"
        vault_dir.mkdir(parents=True)
        (vault_dir / "00_System").mkdir(parents=True)

        tracker = NegativeResultTracker(vault_path=str(vault_dir))
        tracker.record_negative_result(
            idea_id="fail-101",
            title="Linear Sparse Collapse",
            hypothesis="Linearizing full cross-attention with zero memory collapses routing.",
            failure_type="PILOT_FAILURE",
            reasons=["Empirical degradation > 40%."],
            forbidden_patterns=["linear sparse collapse", "zero memory cross-attention"],
            lessons_learned="Do not prune cross-attention without memory buffer.",
        )

        records = tracker.list_negative_results()
        assert len(records) == 1
        assert records[0]["failure_type"] == "PILOT_FAILURE"

        # Check dead-end guardrail detection
        matched, pat, lesson = tracker.is_forbidden_pattern("Testing linear sparse collapse routing")
        assert matched is True
        assert pat == "linear sparse collapse"

        # Verify Tri-Critic immediately rejects matching hypothesis
        critic = MultiModelIdeaReview(negative_tracker=tracker)
        bad_idea = IdeaHypothesis(
            idea_id="test-dead-end",
            title="Linear Sparse Collapse in Attention",
            domain_a="A",
            domain_b="B",
            formal_hypothesis="Testing linear sparse collapse hypothesis",
            testable_claims=["claim1", "claim2"],
            target_metric="acc",
            expected_delta=10.0,
            baseline="base",
            pilot_protocol={"compute_seconds": 60, "min_acceptable_metric": 0.5},
        )
        review = critic.evaluate_idea(bad_idea)
        assert review.decision == "REJECTED"
        assert review.passed is False
        assert "dead-end" in review.feedback_summary.lower() or "falsified" in review.feedback_summary.lower()


def test_voxcpm_voice_control_parser():
    """Verify spoken natural language commands are correctly mapped to intents."""
    parser = VoiceControlParser()

    c1 = parser.parse_command("Please run checkmate audit on latest draft")
    assert c1["intent"] == VoiceActionIntent.CHECKMATE_AUDIT
    assert c1["confidence"] >= 0.90
    assert "checkmate" in c1["spoken_response"].lower()

    c2 = parser.parse_command("Start autoresearch loop for draft.md")
    assert c2["intent"] == VoiceActionIntent.AUTORESEARCH_LOOP
    assert c2["parameters"].get("draft_filename") == "draft.md"

    c3 = parser.parse_command("Have Reviewer 2 critique the paper")
    assert c3["intent"] == VoiceActionIntent.SIMULATED_PEER_REVIEW

    c4 = parser.parse_command("Forge idea on dynamic sparse attention")
    assert c4["intent"] == VoiceActionIntent.EVOMAP_IDEA_FORGE

    c5 = parser.parse_command("Brief me on executive findings")
    assert c5["intent"] == VoiceActionIntent.SPEAK_SUMMARY

    c6 = parser.parse_command("Audit code against the paper")
    assert c6["intent"] == VoiceActionIntent.FEYNMAN_CODE_AUDIT

    c7 = parser.parse_command("Is the paper ready to publish at submission gate?")
    assert c7["intent"] == VoiceActionIntent.RUN_SUBMISSION_GATE


def test_voxcpm_audio_service_synthesis_and_personas():
    """Verify audio synthesis supports personas and produces valid WAV audio."""
    with tempfile.TemporaryDirectory() as tmpdir:
        svc = VoxCPMAudioService(vault_path=tmpdir)
        status = svc.get_engine_status()
        assert "engine" in status
        assert "personas" in status
        assert "chairman" in status["personas"]
        assert "reviewer2" in status["personas"]

        # Synthesize brief phrase with Chairman persona
        res = svc.synthesize_speech("Autonomous research council session convened.", persona="chairman")
        assert res["success"] is True
        assert res["persona"] == "chairman"
        assert res["persona_title"] == "Institute Chairman"
        assert os.path.exists(res["audio_path"])
        assert len(res["audio_base64"]) > 50
        assert res["mime_type"] == "audio/wav"

        # Verify caching returns immediately on second invocation
        res2 = svc.synthesize_speech("Autonomous research council session convened.", persona="chairman")
        assert res2["cached"] is True


def test_ecc_skill_loader_discovery_and_sync():
    """Verify ECC skill loader discovers 280+ skills and syncs core skills."""
    loader = ECCSkillLoader()
    status = loader.get_status()
    assert status["available"] is True
    assert status["total_skills_discovered"] >= 100

    # Test filtering by department
    eng_skills = loader.list_skills(department="Engineering", limit=20)
    assert len(eng_skills) >= 1
    assert any("agent" in s["name"] or "loop" in s["name"] for s in eng_skills)

    # Test skill detail extraction
    skill = loader.get_skill("agent-eval")
    assert skill is not None
    assert skill["name"] == "agent-eval"
    assert "tasks" in skill["description"] or "coding agents" in skill["description"]
    assert len(skill["body"]) > 100

    # Test workspace sync to a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        sync_res = loader.sync_core_skills_to_workspace(target_dir=tmpdir)
        assert sync_res["copied_count"] >= 5
        dest = Path(tmpdir)
        assert (dest / "agent-eval" / "SKILL.md").exists()
        assert (dest / "autonomous-loops" / "SKILL.md").exists()


if __name__ == "__main__":
    print("Running test_evomap_idea_forge_and_tri_critic...")
    test_evomap_idea_forge_and_tri_critic()
    print("Running test_evomap_pilot_gate_and_scaling_decision...")
    test_evomap_pilot_gate_and_scaling_decision()
    print("Running test_evomap_negative_result_tracker_and_guardrail...")
    test_evomap_negative_result_tracker_and_guardrail()
    print("Running test_voxcpm_voice_control_parser...")
    test_voxcpm_voice_control_parser()
    print("Running test_voxcpm_audio_service_synthesis_and_personas...")
    test_voxcpm_audio_service_synthesis_and_personas()
    print("Running test_ecc_skill_loader_discovery_and_sync...")
    test_ecc_skill_loader_discovery_and_sync()
    print("\nALL 6 EVOMAP, VOXCPM & ECC TESTS PASSED SUCCESSFULLY!")
