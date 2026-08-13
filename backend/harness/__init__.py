"""
Prime Agent Harness Module for ResearchingOS.
Inspired by Prime Intellect's prime-agent architecture.
Provides Recursive Context Partitioning (RLM), Continual Self-Refinement, and Autonomous Goal Tracking.
"""

from .continual_memory import ContinualMemoryManager, TrajectoryTelemetry
from .rlm_orchestrator import RLMContextPartitioning
from .autonomous_loop import AutonomousHarnessController
from .prime_harness import PrimeAgentHarness, prime_agent_harness

__all__ = [
    "ContinualMemoryManager",
    "TrajectoryTelemetry",
    "RLMContextPartitioning",
    "AutonomousHarnessController",
    "PrimeAgentHarness",
    "prime_agent_harness"
]
