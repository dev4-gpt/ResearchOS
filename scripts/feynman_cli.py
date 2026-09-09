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

    return 0


if __name__ == "__main__":
    sys.exit(main())
