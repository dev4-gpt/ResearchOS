"""
PrimeAgentHarness — Unified Prime Intellect-inspired Agent Infrastructure for ResearchingOS.
Combines RLM (Recursive Context Partitioning), Continual Memory Refinement, and Autonomous Harness Control.
"""

import os
import json
from typing import Any, Dict, List, Optional
from .continual_memory import ContinualMemoryManager, TrajectoryTelemetry
from .rlm_orchestrator import RLMContextPartitioning
from .autonomous_loop import AutonomousHarnessController


class PrimeAgentHarness:
    """Master Prime Agent Harness orchestrating continual memory, RLM context partitioning, and autonomous loops."""

    def __init__(self, memory_file_path: str = "vault/harness_memory.json"):
        self.continual_memory = ContinualMemoryManager(memory_file_path=memory_file_path)
        self.rlm = RLMContextPartitioning()
        self.autonomous_loop = AutonomousHarnessController()

    def record_step(self, agent_name: str, task: str, score: float, notes: str = "") -> TrajectoryTelemetry:
        """Records an agent execution step in continual memory telemetry."""
        return self.continual_memory.record_step(agent_name, task, score, notes)

    def partition_context(self, corpus: List[Dict[str, Any]], max_chunk_size: int = 4000) -> List[List[Dict[str, Any]]]:
        """Partitions large paper corpora using Recursive Context Partitioning (RLM)."""
        return self.rlm.partition_corpus(corpus, max_chunk_size=max_chunk_size)

    def run_autonomous_loop(self, task_name: str, agent_fn: Any, max_iterations: int = 5) -> Dict[str, Any]:
        """Runs an autonomous goal tracking loop with self-healing feedback."""
        return self.autonomous_loop.run_loop(task_name, agent_fn, max_iterations=max_iterations)

    def get_harness_status(self) -> Dict[str, Any]:
        """Returns the current operational status of the Prime Agent Harness infrastructure."""
        state = getattr(self.continual_memory, "state", {})
        return {
            "status": "active",
            "harness": "PrimeAgentHarness v1.0",
            "architecture": "Prime Intellect RLM + Continual Memory",
            "trajectory_entries": len(state.get("trajectory_history", [])),
            "refined_agent_prompts": list(state.get("durable_prompt_refinements", {}).keys()),
            "average_fact_check_score": state.get("average_fact_check_score", 100.0)
        }


# Singleton harness instance for backend services
prime_agent_harness = PrimeAgentHarness()
