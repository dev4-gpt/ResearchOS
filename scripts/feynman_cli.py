#!/usr/bin/env python3
"""Feynman CLI: Academic Research Assistant & Paper-to-Code Auditor.

Usage:
  python scripts/feynman_cli.py audit <draft_name> [--code <code_path>]
  python scripts/feynman_cli.py lit [topic]
  python scripts/feynman_cli.py review <draft_name> [--venue IEEEtran]
  python scripts/feynman_cli.py autoresearch <draft_name> [--venue IEEEtran] [--iterations 3]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Add backend to sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.autoresearch_loop import AutonomousResearchHarness
from services.feynman_service import FeynmanService
from services.vault import VaultManager
from services.evomap_autoresearch import IdeaForgeService
from services.voxcpm_service import VoiceControlParser, VoxCPMAudioService
from services.ecc_skill_loader import ECCSkillLoader
from services.academic_voice_linter import AcademicVoiceLinter
from services.conference_slides_service import ConferenceSlidesService
from services.diagram_generator import DiagramGeneratorService
from services.universal_skills import UniversalSkillsService


def cmd_audit(args: argparse.Namespace, feynman: FeynmanService, vault: VaultManager) -> int:
    draft_name = args.draft
    if not draft_name.endswith(".md"):
        draft_name += ".md"

    doc = vault.read_markdown("drafts", draft_name)
    content = doc.get("content", "")
    if not content:
        print(f"Error: Draft {draft_name} not found or empty.")
        return 1

    print(f"\n========================================================")
    print(f" Feynman Paper-to-Code Claim Audit: {draft_name}")
    print(f"========================================================")
    res = feynman.audit_paper_against_code(content, code_dir_or_file=args.code)

    print(f"Scanned experiment code files: {', '.join(res['files_scanned']) or 'None'}")
    print(f"Total quantitative assertions audited: {res['total_claims_audited']}")
    print(f"Matched code constants: {res['matched_in_code']}")
    print(f"Code Provenance Score: {res['code_provenance_score']}%\n")

    print("--- Detailed Claim Mappings ---")
    for idx, item in enumerate(res["audit_items"][:10], start=1):
        status_symbol = "[✓]" if item["status"] == "MATCH" else "[✗]"
        print(f"{status_symbol} ({item['status']}) {item['paper_value']}")
        print(f"    Claim: {item['claim_text']}")
        if item["code_match"]:
            print(f"    Code:  {item['code_match']} ({item['code_file']}:{item['line_number']})")
        else:
            print(f"    Note:  {item['detail']}")

    return 0


def cmd_lit(args: argparse.Namespace, feynman: FeynmanService) -> int:
    topic = args.topic or "Multi-Agent Systems & Literature Review"
    print(f"\n========================================================")
    print(f" Feynman Literature Matrix: {topic}")
    print(f"========================================================")
    res = feynman.synthesize_literature_matrix(topic=topic)

    print(f"Papers reviewed from vault: {res['papers_reviewed']}\n")

    print("=== Empirical Consensus ===")
    for c in res["consensus_findings"]:
        print(f"  • {c['topic']}: {c['assertion']} {c['source']}")

    print("\n=== Active Debates & Contending Views ===")
    for d in res["active_disagreements"]:
        print(f"  • {d['topic']}: {d['contending_view']} {d['source']}")

    print("\n=== Open Research Questions ===")
    for o in res["open_research_questions"]:
        print(f"  • {o['paper']} {o['citation']}: \"{o['gap']}\"")

    return 0


def cmd_review(args: argparse.Namespace, feynman: FeynmanService, vault: VaultManager) -> int:
    draft_name = args.draft
    if not draft_name.endswith(".md"):
        draft_name += ".md"

    doc = vault.read_markdown("drafts", draft_name)
    content = doc.get("content", "")
    if not content:
        print(f"Error: Draft {draft_name} not found or empty.")
        return 1

    venue = args.venue or "IEEEtran"
    print(f"\n========================================================")
    print(f" Feynman Simulated Peer Review ({venue}): {draft_name}")
    print(f"========================================================")
    res = feynman.simulated_peer_review(content, venue=venue)

    print(f"Recommendation:     {res['recommendation']}")
    print(f"Rejection Risk:     {res['rejection_risk_score']}%")
    print(f"Severity Breakdown: {res['blocker_count']} Blockers, {res['major_count']} Majors, {res['minor_count']} Minors\n")

    print("--- Review Directives ---")
    for item in res["review_items"]:
        print(f"[{item['severity']}] [{item['category']}] {item['title']}")
        print(f"    Critique: {item['description']}")
        print(f"    Action:   {item['suggested_action']}\n")

    return 0


def cmd_autoresearch(args: argparse.Namespace, vault: VaultManager) -> int:
    draft_name = args.draft
    if not draft_name.endswith(".md"):
        draft_name += ".md"

    venue = args.venue or "IEEEtran"
    iterations = args.iterations or 3

    print(f"\n========================================================")
    print(f" Karpathy Autoresearch Loop: {draft_name} -> {venue}")
    print(f"========================================================")
    harness = AutonomousResearchHarness(vault_manager=vault)
    res = harness.optimize(draft_name, target_venue=venue, max_iterations=iterations)

    print(f"Initial Fitness: {res['initial_fitness']}")
    print(f"Final Fitness:   {res['final_fitness']}")
    print(f"Iterations run:  {res['iterations_run']} (Kept: {res['kept_count']}, Discarded: {res['discarded_count']})\n")

    for item in res["history"]:
        dec_tag = "[KEEP]" if item["decision"] == "KEEP" else "[DISCARD]"
        print(f"Step {item['iteration']}: {dec_tag} {item['mutation_type']} (Fitness: {item['fitness_before']} -> {item['fitness_after']})")
        print(f"    Rationale: {item['rationale']}")

    return 0


def cmd_fx(args: argparse.Namespace, feynman: FeynmanService) -> int:
    status = feynman.fx.get_status()
    if args.fx_action == "status":
        print("\n========================================================")
        print(" Vercel Labs fx Agent Engine Status")
        print("========================================================")
        print(f"Installed:       {status['installed']}")
        print(f"Engine Mode:     {status['mode'].upper()}")
        print(f"Version:         {status['version']}")
        print(f"Binary Path:     {status['binary_path']}")
        print(f"ACP Subagents:   {'Enabled' if status['acp_supported'] else 'Disabled'}")
        print(f"MCP Client:      {'Enabled' if status['mcp_client_capable'] else 'Disabled'}")
        print(f"Description:     {status['description']}\n")
        return 0

    elif args.fx_action == "run":
        prompt = args.prompt or "Research transformer attention efficiency"
        print("\n========================================================")
        print(f" Dispatching fx Research Subagent: '{prompt}'")
        print("========================================================")
        res = feynman.fx.dispatch_research(prompt)
        print(f"Engine:    {res.get('engine')}")
        print(f"Latency:   {res.get('execution_latency_ms', 0)}ms\n")
        print("--- Synthesis ---")
        print(res.get("synthesis") or res.get("summary") or res.get("raw_output", "No output"))
        if res.get("key_findings"):
            print("\n--- Key Findings ---")
            for f in res["key_findings"]:
                print(f"  • {f}")
        return 0
    return 1


def cmd_evomap(args: argparse.Namespace, vault: VaultManager) -> int:
    forge = IdeaForgeService(vault_manager=vault)
    if args.evo_action == "forge":
        topic = args.topic or "Mixture of Experts"
        print(f"\n========================================================")
        print(f" EvoMap Idea Forge: Cross-Domain Ideation on '{topic}'")
        print(f"========================================================")
        ideas = forge.forge_ideas(topic=topic, count=args.count)
        print(f"Generated {len(ideas)} candidate hypotheses with Tri-Critic review:\n")
        for idx, entry in enumerate(ideas, start=1):
            idea = entry["idea"]
            review = entry["review"]
            dec_color = "[✓ ACCEPTED]" if review["decision"] == "ACCEPTED" else f"[{review['decision']}]"
            print(f"Idea #{idx}: {idea['title']}")
            print(f"  Status:       {dec_color} (Composite: {review['composite_score']}/10.0)")
            print(f"  Novelty:      {review['novelty_score']}/10.0 | Feasibility: {review['feasibility_score']}/10.0 | Verifiability: {review['verifiability_score']}/10.0")
            print(f"  Hypothesis:   {idea['formal_hypothesis']}")
            print(f"  Metric Delta: +{idea['expected_delta']}% over {idea['baseline']}")
            print(f"  Feedback:     {review['feedback_summary']}\n")
        return 0

    elif args.evo_action == "pilot":
        topic = args.topic or "Dynamic Sparse Attention"
        ideas = forge.forge_ideas(topic=topic, count=1)
        if not ideas:
            print("Error: No idea generated for pilot testing.")
            return 1
        idea = ideas[0]["idea"]
        print(f"\n========================================================")
        print(f" EvoMap Pilot-Before-Scaling Gate: {idea['title']}")
        print(f"========================================================")
        res = forge.run_pilot(idea)
        status_tag = "[PASS]" if res["passed"] else "[FAIL]"
        print(f"Status:             {status_tag} ({res['status']})")
        print(f"Proxy Task:         {res['proxy_task']}")
        print(f"Observed Metric:    {res['observed_metric']} (Threshold: {res['min_acceptable_metric']})")
        print(f"Ready for Scaling:  {res['ready_for_full_autoresearch']}")
        return 0

    elif args.evo_action == "negative":
        results = forge.get_negative_results(limit=args.limit or 20)
        print(f"\n========================================================")
        print(f" EvoMap Negative Results & Falsification Ledger ({len(results)} entries)")
        print(f"========================================================")
        if not results:
            print("No negative results recorded yet in vault/00_System/negative_results.jsonl.")
            return 0
        for r in results:
            print(f"[{r.get('failure_type')}] {r.get('title')}")
            print(f"  Hypothesis: {r.get('hypothesis')}")
            print(f"  Lessons:    {r.get('lessons_learned')}")
            print(f"  Patterns:   {', '.join(r.get('forbidden_patterns', []))}\n")
        return 0
    return 1


def cmd_voice(args: argparse.Namespace, vault: VaultManager) -> int:
    parser = VoiceControlParser()
    audio_service = VoxCPMAudioService(vault_path=vault.vault_path)

    if args.voice_action == "command":
        text = args.text or "Run checkmate audit on latest draft"
        print(f"\n========================================================")
        print(f" VoxCPM Voice Command Parsing: \"{text}\"")
        print(f"========================================================")
        parsed = parser.parse_command(text)
        print(f"Intent:          {parsed['intent']}")
        print(f"Confidence:      {int(parsed['confidence'] * 100)}%")
        print(f"Parameters:      {parsed['parameters']}")
        print(f"Spoken Response: \"{parsed['spoken_response']}\"\n")
        return 0

    elif args.voice_action == "speak":
        text = args.text or "The research council has completed zero-hallucination verification."
        persona = args.persona or "chairman"
        print(f"\n========================================================")
        print(f" VoxCPM Speech Synthesis ({persona}): \"{text}\"")
        print(f"========================================================")
        res = audio_service.synthesize_speech(text, persona=persona)
        print(f"Success:     {res['success']}")
        print(f"Engine:      {res['engine_used']}")
        print(f"Persona:     {res['persona_title']}")
        print(f"Audio Path:  {res['audio_path']}\n")
        return 0

    elif args.voice_action == "status":
        status = audio_service.get_engine_status()
        print(f"\n========================================================")
        print(f" VoxCPM Speech Engine Status")
        print(f"========================================================")
        print(f"Active Engine:       {status['engine']}")
        print(f"Neural Model Present:{status['neural_voxcpm_installed']}")
        print(f"macOS 'say' Present: {status['macos_say_available']}")
        print(f"Personas:            {', '.join(status['personas'])}")
        print(f"Sample Rate:         {status['sample_rate_hz']} Hz")
        print(f"Cached Audio Files:  {status['cached_audio_files']}\n")
        return 0
    return 1


def cmd_ecc(args: argparse.Namespace) -> int:
    loader = ECCSkillLoader()
    if args.ecc_action == "list":
        dept = args.dept
        q = args.query
        skills = loader.list_skills(department=dept, query=q, limit=args.limit or 50)
        print(f"\n========================================================")
        print(f" ECC Departmental Skills Catalog ({len(skills)} shown)")
        print(f"========================================================")
        for s in skills:
            print(f"• {s['name']} [{s['department']}]")
            print(f"  {s['description'][:100]}...\n")
        return 0

    elif args.ecc_action == "show":
        skill = loader.get_skill(args.skill_name)
        if not skill:
            print(f"Error: Skill '{args.skill_name}' not found in ECC catalog.")
            return 1
        print(f"\n========================================================")
        print(f" ECC Skill: {skill['name']} ({skill['department']})")
        print(f"========================================================")
        print(f"Description: {skill['description']}\n")
        print("--- Skill Body Preview ---")
        print(skill['body'][:1200])
        return 0

    elif args.ecc_action == "sync":
        res = loader.sync_core_skills_to_workspace()
        print(f"\n========================================================")
        print(f" Syncing Core ECC Skills to Workspace")
        print(f"========================================================")
        print(f"Destination:  {res['destination']}")
        print(f"Copied Count: {res['copied_count']}")
        print(f"Skills:       {', '.join(res['skills'])}\n")
        return 0
    return 1


def cmd_slop(args: argparse.Namespace, vault: VaultManager) -> int:
    linter = AcademicVoiceLinter()
    text = args.text
    if not text and args.draft:
        draft_name = args.draft if args.draft.endswith(".md") else f"{args.draft}.md"
        doc = vault.read_markdown("drafts", draft_name)
        text = doc.get("content", "")
        if not text:
            print(f"Error: Draft '{draft_name}' not found or empty.")
            return 1

    if not text:
        print("Error: Specify either a draft name or provide --text.")
        return 1

    if args.slop_action == "audit":
        res = linter.audit_prose(text)
        print(f"\n========================================================")
        print(f" Academic Voice & Anti-Slop Audit (hardikpandya/stop-slop)")
        print(f"========================================================")
        print(f"Academic Voice Score: {res['academic_voice_score']}% [{res['rating']}]")
        print(f"Total AI tells identified: {res['total_findings']}")
        print(f"Blockers: {res['breakdown']['blockers']} | Majors: {res['breakdown']['majors']} | Minors: {res['breakdown']['minors']}\n")
        if res["findings"]:
            print("--- Top Findings ---")
            for idx, f in enumerate(res["findings"][:10], start=1):
                print(f"  [{f['severity']}] Line {f['line_number']}: \"{f['matched_text']}\"")
                print(f"       Action: {f['recommendation']}")
        return 0

    elif args.slop_action == "humanize":
        res = linter.humanize_text(text)
        print(f"\n========================================================")
        print(f" Humanized Academic Scholarly Prose (blader/humanizer)")
        print(f"========================================================")
        print(f"Score Improvement: {res['original_score']}% -> {res['cleaned_score']}% (+{res['score_improvement']}%)")
        print(f"Findings Reduced:  {res['original_findings_count']} -> {res['cleaned_findings_count']}\n")
        print("--- Humanized Output Preview ---")
        print(res["humanized_text"][:800])
        return 0
    return 1


def cmd_slides(args: argparse.Namespace, vault: VaultManager) -> int:
    service = ConferenceSlidesService(vault.vault_path)
    title = args.title or "Conference Presentation"
    text = args.text
    if not text and args.draft:
        draft_name = args.draft if args.draft.endswith(".md") else f"{args.draft}.md"
        doc = vault.read_markdown("drafts", draft_name)
        text = doc.get("content", "")
        title = doc.get("frontmatter", {}).get("title", draft_name)
        if not text:
            print(f"Error: Draft '{draft_name}' not found or empty.")
            return 1

    if not text:
        text = f"# {title}\n\nExecutive Abstract: Autonomous research presentation generated via ResearchingOS."

    res = service.generate_deck_from_manuscript(
        draft_title=title,
        manuscript_text=text,
        venue=args.venue or "IEEEtran / ACM Conference",
    )
    print(f"\n========================================================")
    print(f" 16:9 Presentation Slides (zarazhangrui/frontend-slides)")
    print(f"========================================================")
    print(f"Deck Title:   {res['title']}")
    print(f"Total Slides: {res['total_slides']}")
    print(f"HTML File:    {res['file_path']}")
    print(f"Open URL:     http://127.0.0.1:8000{res['relative_url']}\n")
    return 0


def cmd_diagram(args: argparse.Namespace, vault: VaultManager) -> int:
    service = DiagramGeneratorService(vault.vault_path)
    title = args.title or "ResearchingOS Multi-Agent Autonomous Council Pipeline"
    res = service.generate_pipeline_diagram(title=title)
    print(f"\n========================================================")
    print(f" Publication Architecture Diagram (cathrynlavery/diagram-design)")
    print(f"========================================================")
    print(f"Title:     {res['title']}")
    print(f"SVG File:  {res['file_path']}")
    print(f"Open URL:  http://127.0.0.1:8000{res['relative_url']}\n")
    return 0


def cmd_skills(args: argparse.Namespace) -> int:
    service = UniversalSkillsService()
    if args.skills_action == "summary":
        summary = service.get_summary()
        print(f"\n========================================================")
        print(f" Universal Installed Skills Summary (Zero Storage Duplication)")
        print(f"========================================================")
        print(f"Global Path:      {summary['global_path']}")
        print(f"Total Skills:     {summary['total_skills_installed']}")
        print(f"Zero Duplication: {summary['zero_storage_duplication']}\n")
        print("Curated Skill Breakdown:")
        for k, v in summary["highlighted_curations"].items():
            print(f"  • {k}: {v} skills")
        print("\nAll Categories:")
        for cat, cnt in summary["categories"].items():
            print(f"  • {cat}: {cnt} skills")
        return 0

    elif args.skills_action == "list":
        skills = service.list_universal_skills(category=args.category)
        print(f"\n========================================================")
        print(f" Universal Skills Catalog ({len(skills)} found)")
        print(f"========================================================")
        for s in skills:
            print(f"  • {s['name']:<28} [{s['category']}] (by {s['author']})")
        return 0

    elif args.skills_action == "show":
        if not args.skill_name:
            print("Error: specify skill name to inspect")
            return 1
        details = service.get_skill_details(args.skill_name)
        if not details:
            print(f"Error: Skill '{args.skill_name}' not found.")
            return 1
        print(f"\n========================================================")
        print(f" Universal Skill: {details['name']} (by {details['author']})")
        print(f" Category: {details['category']} | Path: {details['path']}")
        print(f"========================================================")
        print(details["content"][:1200])
        return 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Feynman CLI for ResearchingOS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit paper claims against experiment code")
    p_audit.add_argument("draft", help="Draft filename (e.g. paper.md)")
    p_audit.add_argument("--code", default=None, help="Path to code script or directory")

    # lit
    p_lit = subparsers.add_parser("lit", help="Synthesize literature consensus and debate matrix")
    p_lit.add_argument("topic", nargs="?", default="Multi-Agent Systems", help="Research topic")

    # review
    p_review = subparsers.add_parser("review", help="Simulate peer review with severity triage")
    p_review.add_argument("draft", help="Draft filename")
    p_review.add_argument("--venue", default="IEEEtran", help="Target publication venue")

    # autoresearch
    p_auto = subparsers.add_parser("autoresearch", help="Run autonomous Karpathy optimization loop")
    p_auto.add_argument("draft", help="Draft filename")
    p_auto.add_argument("--venue", default="IEEEtran", help="Target publication venue")
    p_auto.add_argument("--iterations", type=int, default=3, help="Max hill-climbing iterations")

    # fx
    p_fx = subparsers.add_parser("fx", help="Vercel Labs fx agent engine controls")
    p_fx.add_argument("fx_action", choices=["status", "run"], help="Action to execute")
    p_fx.add_argument("prompt", nargs="?", default=None, help="Research prompt for fx run")

    # evomap
    p_evo = subparsers.add_parser("evomap", help="EvoMap idea forge and pilot-before-scaling gate")
    p_evo.add_argument("evo_action", choices=["forge", "pilot", "negative"], help="Action: forge, pilot, or negative")
    p_evo.add_argument("--topic", default="Mixture of Experts", help="Research topic")
    p_evo.add_argument("--count", type=int, default=2, help="Number of ideas to generate")
    p_evo.add_argument("--limit", type=int, default=20, help="Max negative results to display")

    # voice
    p_voice = subparsers.add_parser("voice", help="VoxCPM speech synthesis and voice control")
    p_voice.add_argument("voice_action", choices=["command", "speak", "status"], help="Action: command, speak, or status")
    p_voice.add_argument("text", nargs="?", default=None, help="Text to speak or voice command to parse")
    p_voice.add_argument("--persona", default="chairman", choices=["chairman", "reviewer2", "analyst", "feynman"], help="Persona voice")

    # ecc
    p_ecc = subparsers.add_parser("ecc", help="affaan-m/ECC departmental skills integration")
    p_ecc.add_argument("ecc_action", choices=["list", "show", "sync"], help="Action: list, show, or sync")
    p_ecc.add_argument("skill_name", nargs="?", default=None, help="Skill name to show")
    p_ecc.add_argument("--dept", default=None, help="Filter by department")
    p_ecc.add_argument("--query", default=None, help="Search query")
    p_ecc.add_argument("--limit", type=int, default=50, help="Max skills to show")

    # slop
    p_slop = subparsers.add_parser("slop", help="Anti-slop linter and academic voice humanizer")
    p_slop.add_argument("slop_action", choices=["audit", "humanize"], help="Action: audit or humanize")
    p_slop.add_argument("draft", nargs="?", default=None, help="Draft filename (e.g. paper.md)")
    p_slop.add_argument("--text", default=None, help="Direct prose text to audit or humanize")

    # slides
    p_slides = subparsers.add_parser("slides", help="Generate 16:9 presentation slide deck")
    p_slides.add_argument("draft", nargs="?", default=None, help="Draft filename")
    p_slides.add_argument("--title", default=None, help="Slide deck presentation title")
    p_slides.add_argument("--text", default=None, help="Raw markdown content")
    p_slides.add_argument("--venue", default="IEEEtran / ACM Conference", help="Target venue")

    # diagram
    p_diagram = subparsers.add_parser("diagram", help="Generate publication architecture SVG diagram")
    p_diagram.add_argument("--title", default="ResearchingOS Multi-Agent Autonomous Council Pipeline", help="Diagram title")

    # skills
    p_skills = subparsers.add_parser("skills", help="Universal skills catalog inspection")
    p_skills.add_argument("skills_action", choices=["summary", "list", "show"], default="summary", nargs="?", help="Action: summary, list, or show")
    p_skills.add_argument("skill_name", nargs="?", default=None, help="Skill name to inspect")
    p_skills.add_argument("--category", default=None, help="Filter by category")

    args = parser.parse_args()
    vault = VaultManager(os.getenv("VAULT_PATH", "vault"))
    feynman = FeynmanService(vault_manager=vault)

    if args.command == "audit":
        return cmd_audit(args, feynman, vault)
    elif args.command == "lit":
        return cmd_lit(args, feynman)
    elif args.command == "review":
        return cmd_review(args, feynman, vault)
    elif args.command == "autoresearch":
        return cmd_autoresearch(args, vault)
    elif args.command == "fx":
        return cmd_fx(args, feynman)
    elif args.command == "evomap":
        return cmd_evomap(args, vault)
    elif args.command == "voice":
        return cmd_voice(args, vault)
    elif args.command == "ecc":
        return cmd_ecc(args)
    elif args.command == "slop":
        return cmd_slop(args, vault)
    elif args.command == "slides":
        return cmd_slides(args, vault)
    elif args.command == "diagram":
        return cmd_diagram(args, vault)
    elif args.command == "skills":
        return cmd_skills(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
