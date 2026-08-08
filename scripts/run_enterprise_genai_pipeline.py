import sys
import os
import time

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from agents.council import CouncilOrchestrator

def main():
    topic = "Systematic Review & Meta-Taxonomy of Generative AI in Enterprise Workflows: Empirical Evidence, Economic Limits, Skill Equalization, and Task Boundary Frontiers"
    print(f"🚀 Launching ResearchingOS Multi-Agent Pipeline for Topic:\n'{topic}'\n")

    orchestrator = CouncilOrchestrator()

    def log_callback(log_data):
        agent = log_data.get("agent", "System")
        stage = log_data.get("stage", "General")
        msg = log_data.get("message", "")
        print(f"[{stage}] [{agent}]: {msg}")

    result = orchestrator.run_research(topic, log_callback, max_papers=20)
    print("\n✅ Research Pipeline Completed Successfully!")
    print(f"Project ID: {result.get('project_id')}")
    print(f"Ingested Papers Count: {result.get('papers_count')}")
    print(f"Debate Transcript: vault/03_Debates/{result.get('debate_file')}")
    print(f"Manuscript Draft: vault/04_Drafts/{result.get('draft_file')}")
    print(f"Fact-Check Score: {result.get('fact_check_score')}%")

if __name__ == "__main__":
    main()
