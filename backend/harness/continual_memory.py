import os
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class TrajectoryTelemetry:
    project_id: str
    topic: str
    fact_check_score: float
    verified_citations: int
    broken_citations: int
    grounded_metrics: int
    unverified_metrics: int
    duration_seconds: float
    timestamp: float

class ContinualMemoryManager:
    def __init__(self, memory_file_path: str = "vault/harness_memory.json"):
        self.memory_file_path = memory_file_path
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.memory_file_path):
            try:
                with open(self.memory_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "durable_prompt_refinements": {
                "Scout": "Prioritize empirical RCT studies, open-access PDFs, and landmark meta-analyses.",
                "Analyst": "Extract complete methodology, sample sizes (N), and formal p-values into frontmatter.",
                "Engineer": "Compute exact FLOPs scaling laws and GPU VRAM constraints.",
                "Statistician": "Rigorously audit control group baselines and statistical significance thresholds.",
                "Reviewer2": "Audit un-ablated baseline vulnerabilities, short-term horizon deficits, and overhype.",
                "Chairman": "Synthesize points of consensus and resolve technical tensions into 8 structured sections.",
                "Writer": "Enforce minimum 8,000+ words / 15+ pages IEEEtran format with zero commercial hype."
            },
            "learned_heuristics": [
                "Always verify DOI targets before adding inline wikilinks.",
                "Ground all percentage gains against raw ingested paper text.",
                "Ensure minimum 15 pages for full systematic literature review manuscripts."
            ],
            "trajectory_history": [],
            "total_runs": 0,
            "average_fact_check_score": 100.0
        }

    def save_state(self) -> None:
        os.makedirs(os.path.dirname(self.memory_file_path), exist_ok=True)
        with open(self.memory_file_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def record_telemetry(self, telemetry: TrajectoryTelemetry) -> Dict[str, Any]:
        """Records run telemetry and executes self-refinement logic."""
        telemetry_dict = asdict(telemetry)
        self.state["trajectory_history"].append(telemetry_dict)
        self.state["total_runs"] += 1

        # Recalculate average fact-check score
        scores = [t["fact_check_score"] for t in self.state["trajectory_history"]]
        self.state["average_fact_check_score"] = round(sum(scores) / len(scores), 2)

        # Trigger self-refinement if score < 90
        refinement_triggered = False
        if telemetry.fact_check_score < 90.0:
            refinement_triggered = True
            heuristic = f"Run {telemetry.project_id}: Fact-check score ({telemetry.fact_check_score}%) dropped. Strict verification required for {telemetry.topic}."
            if heuristic not in self.state["learned_heuristics"]:
                self.state["learned_heuristics"].append(heuristic)

        self.save_state()
        return {
            "success": True,
            "refinement_triggered": refinement_triggered,
            "average_score": self.state["average_fact_check_score"]
        }

    def get_agent_refinements(self, agent_name: str) -> str:
        """Retrieves learned prompt refinements for a given agent persona."""
        return self.state["durable_prompt_refinements"].get(agent_name, "")
