"""Regenerate a dead vault/03_Debates placeholder for real, without touching vault/04_Drafts.

All 9 files in vault/03_Debates were dead placeholders ("API failure or quota
reached") -- the debate feature had never produced real output for any topic. The
only code path that produces a debate, CouncilOrchestrator.run_research(), also
writes the matching manuscript to vault/04_Drafts using the same filename convention
the hand-verified, gate-passing manuscripts already use, via a self-healing repair
loop that (until fixed alongside this script) could silently mis-cite content.

This script calls CouncilOrchestrator.run_debate_only() instead, which shares
Stages 1-4 (paper discovery, critique, boardroom debate, synthesis) with
run_research() through a common helper but stops right after saving to
vault/03_Debates -- Stage 5+ (drafting) is simply never reached, so vault/04_Drafts
is structurally unreachable from this code path.

Defaults to ONE topic (--topic) so a quota/API failure surfaces on one file, not all
nine. Pass --all only after confirming a single topic produces real content.

    backend/.venv/bin/python scripts/regenerate_debates.py --list
    backend/.venv/bin/python scripts/regenerate_debates.py --topic sparse-autoencoders-interpretability
    backend/.venv/bin/python scripts/regenerate_debates.py --all
"""
import argparse
import subprocess
import sys

sys.path.insert(0, "backend")

from agents.council import CouncilOrchestrator  # noqa: E402

# filename slug -> exact topic string from each debate file's own frontmatter, so the
# regenerated debate's slug matches (and overwrites) the existing placeholder file
# rather than creating a differently-named duplicate.
TOPICS = {
    "sparse-autoencoders-interpretability": "sparse-autoencoders-interpretability",
    "multi-agent-orchestration-security": "multi-agent-orchestration-security",
    "onpremise-slm-privacy-opex": "onpremise-slm-privacy-opex",
    "test-time-compute-reasoning": "test-time-compute-reasoning",
    "enterprise-genai-roi": "enterprise-genai-roi",
    "architectural-dynamics-econometric-risk": (
        "Architectural Dynamics, Econometric Modeling, and Risk Governance of "
        "Enterprise Generative AI Adoption"
    ),
    "autonomous-code-synthesis-self-healing": (
        "Autonomous Code Synthesis and Self-Healing Multi-Agent Systems: "
        "Architectural Topologies, Empirical Benchmarks, and Systemic Governance"
    ),
    "enterprise-adoption-infra": (
        "Enterprise Adoption of Multi-Agent AI Systems: Infrastructure Architectures, "
        "Organizational Implementation, and Labor Market Transformation"
    ),
    "comprehensive-journal-review": (
        "A comprehensive, technical, and business-oriented journal review analyzing "
        "enterprise generative AI integration across three key pillars: (1) System "
        "Architecture & Multi-Agent Orchestration (RAG vs. fine-tuning, latency-cost "
        "optimization, vector storage, sandboxed tool execution), (2) Econometric & "
        "Productivity Modeling (Cobb-Douglas production functions, supermodular labor "
        "complementarity, ROI cost-latency tradeoffs), and (3) Systemic Risk & "
        "Governance Frameworks (data privacy, hallucination auditing, cryptographic "
        "human-in-the-loop guardrails). Incorporates quantitative benchmark "
        "meta-analyses, formal mathematical equations, and actionable enterprise "
        "deployment roadmaps."
    ),
}


def _print_log(entry: dict) -> None:
    stage = entry.get("stage", "")
    agent = entry.get("agent", "")
    message = str(entry.get("message", ""))[:200]
    print(f"[{stage}] {agent}: {message}")


def _drafts_snapshot() -> str:
    """git status of vault/04_Drafts, used as a before/after safety check."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "vault/04_Drafts"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def regenerate(slug: str) -> bool:
    topic = TOPICS[slug]
    before = _drafts_snapshot()

    orchestrator = CouncilOrchestrator(vault_path="vault")
    print(f"\n=== Regenerating debate for '{slug}' (dry_run={orchestrator.is_dry_run}) ===")
    if orchestrator.is_dry_run:
        print("WARNING: no GEMINI_API_KEY/NVIDIA key configured -- this would only "
              "produce mock content. Aborting rather than overwrite a real placeholder "
              "with a synthetic one.")
        return False

    result = orchestrator.run_debate_only(topic, _print_log, max_papers=25)

    after = _drafts_snapshot()
    if after != before:
        print("SAFETY CHECK FAILED: vault/04_Drafts changed during a debate-only run. "
              "This should be structurally impossible -- stop and investigate before "
              "trusting any output from this script.")
        print("git status --porcelain -- vault/04_Drafts:\n" + after)
        return False

    if not result.get("success"):
        print(f"FAILED: {result}")
        return False

    print(f"OK: wrote vault/03_Debates/{result['debate_file']} "
          f"({result['papers_count']} papers). vault/04_Drafts unchanged (verified).")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="list topic slugs and exit")
    parser.add_argument("--topic", help="regenerate a single topic by slug")
    parser.add_argument("--all", action="store_true", help="regenerate all 9 topics")
    args = parser.parse_args()

    if args.list:
        for slug in TOPICS:
            print(slug)
        return 0

    if args.all:
        slugs = list(TOPICS)
    elif args.topic:
        if args.topic not in TOPICS:
            print(f"Unknown topic slug: {args.topic}. Use --list to see valid slugs.")
            return 1
        slugs = [args.topic]
    else:
        print("Pass --topic <slug> (test one first), --all, or --list. See --help.")
        return 1

    failures = []
    for slug in slugs:
        if not regenerate(slug):
            failures.append(slug)

    if failures:
        print(f"\n{len(failures)}/{len(slugs)} failed: {failures}")
        return 1
    print(f"\nAll {len(slugs)} regenerated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
