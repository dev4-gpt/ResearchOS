"""Autonomous Manuscript Hill-Climbing Optimization Harness (Karpathy autoresearch loop).

Evaluates candidate drafts against frozen publication evaluator contracts,
computes a composite scalar fitness F in [0, 100], executes atomic KEEP / DISCARD decisions,
and logs every iteration to an append-only ledger.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from domain.models import citation_key
from services.checkmate_verifier import CheckmateVerifierService
from services.fact_checker import FactCheckerService
from services.publication_harness import (
    PublicationEvaluationConfig,
    stable_hash,
    utc_now,
)
from services.vault import VaultManager


@dataclass
class FitnessScore:
    grounding_score: float = 0.0
    layout_score: float = 0.0
    originality_score: float = 0.0
    depth_score: float = 0.0
    compile_passed: bool = True
    blocked_claims: int = 0
    total_claims: int = 0
    total_words: int = 0

    @property
    def composite_fitness(self) -> float:
        """Composite scalar fitness F in [0, 100]."""
        if not self.compile_passed:
            return 0.0
        fitness = (
            0.35 * self.grounding_score
            + 0.25 * self.layout_score
            + 0.20 * self.originality_score
            + 0.20 * self.depth_score
        )
        return round(max(0.0, min(100.0, fitness)), 2)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["composite_fitness"] = self.composite_fitness
        return d


@dataclass
class IterationRecord:
    iteration: int
    timestamp: str
    mutation_type: str
    fitness_before: float
    fitness_after: float
    decision: str  # "KEEP" | "DISCARD"
    score_details: Dict[str, Any]
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AutonomousResearchHarness:
    """Closed-loop optimization agent for academic research manuscripts."""

    def __init__(
        self,
        vault_manager: Optional[VaultManager] = None,
        config: Optional[PublicationEvaluationConfig] = None,
        ledger_path: Optional[str] = None,
    ) -> None:
        self.vault = vault_manager or VaultManager(os.getenv("VAULT_PATH", "vault"))
        self.config = config or PublicationEvaluationConfig()
        self.fact_checker = FactCheckerService(self.vault)
        self.checkmate = CheckmateVerifierService(self.vault)
        self.ledger_path = Path(ledger_path or (Path(self.vault.vault_path) / "00_System" / "autoresearch_ledger.jsonl"))
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def evaluate_fitness(
        self,
        content: str,
        target_venue: str = "IEEEtran",
        source_records: Optional[Dict[str, str]] = None,
        measurement_records: Optional[List[Dict[str, Any]]] = None,
    ) -> FitnessScore:
        """Evaluate a draft candidate against frozen evaluator rules."""
        # 1. Depth & Word Count
        words = len(re.findall(r"\b\w+\b", content))
        target_words = 4500 if "journal" in target_venue.lower() else 2200
        depth_score = min(100.0, round((words / target_words) * 100.0, 1))

        # 2. Grounding & Claims
        claim_records = self.fact_checker.extract_claim_evidence_records(
            content,
            source_records=source_records or {},
            measurement_records=measurement_records or [],
            strict=self.config.strict_evidence,
        )
        total_claims = len(claim_records)
        blocked = sum(1 for c in claim_records if c.get("status") not in ("VERIFIED", "PASSED"))
        verified = total_claims - blocked
        grounding_score = 100.0 if total_claims == 0 else round((verified / total_claims) * 100.0, 1)

        # 3. Originality
        originality_score = 95.0

        # 4. Layout & Syntax
        has_broken_math = bool(re.search(r"\$\$[^\$]*$", content))
        layout_score = 50.0 if has_broken_math else 100.0

        return FitnessScore(
            grounding_score=grounding_score,
            layout_score=layout_score,
            originality_score=originality_score,
            depth_score=depth_score,
            compile_passed=not has_broken_math,
            blocked_claims=blocked,
            total_claims=total_claims,
            total_words=words,
        )

    def mutate_candidate(
        self,
        content: str,
        fitness: FitnessScore,
        source_records: Optional[Dict[str, str]] = None,
        measurement_records: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[str, str]:
        """Apply targeted surgical mutation based on evaluator feedback."""
        # Mutation 1: Auto-remediate formatting and math syntax
        remediated = self.checkmate.auto_remediate_markdown(content)
        if remediated != content:
            return remediated, "auto_remediate_syntax"

        # Mutation 2: Ground unbacked claims with measurement data if available
        if fitness.blocked_claims > 0 and measurement_records:
            for m in measurement_records:
                metric = str(m.get("metric", ""))
                val = m.get("value")
                unit = m.get("unit", "")
                if metric and val is not None:
                    pattern = re.compile(rf"\b{re.escape(metric.replace('_', ' '))}\b", re.I)
                    if pattern.search(remediated) and str(val) not in remediated:
                        remediated = pattern.sub(f"{metric.replace('_', ' ')} (measured: {val}{unit})", remediated, count=1)
                        return remediated, "ground_metric_anchor"

        # Mutation 3: LaTeX equation balancing
        if not fitness.compile_passed:
            fixed = content.replace("$$", "\n$$\n")
            return fixed, "balance_latex_math"

        return content, "no_mutation_needed"

    def optimize(
        self,
        draft_name: str,
        target_venue: str = "IEEEtran",
        max_iterations: int = 3,
        source_records: Optional[Dict[str, str]] = None,
        measurement_records: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Execute autonomous Karpathy-style optimization loop."""
        initial_doc = self.vault.read_markdown("drafts", draft_name)
        initial_content = initial_doc.get("content", "")
        current_best = initial_content
        best_fitness = self.evaluate_fitness(
            current_best, target_venue, source_records, measurement_records
        )

        history: List[IterationRecord] = []

        for step in range(1, max_iterations + 1):
            mutated, mutation_type = self.mutate_candidate(
                current_best, best_fitness, source_records, measurement_records
            )
            if mutated == current_best:
                break

            candidate_fitness = self.evaluate_fitness(
                mutated, target_venue, source_records, measurement_records
            )

            # Keep if fitness improved, or if syntax auto-remediation cleanly improved the document on parity
            improved = candidate_fitness.composite_fitness > best_fitness.composite_fitness
            parity_cleanup = (
                candidate_fitness.composite_fitness == best_fitness.composite_fitness
                and mutation_type == "auto_remediate_syntax"
                and mutated != current_best
            )

            if improved or parity_cleanup:
                decision = "KEEP"
                rationale = (
                    f"Fitness improved from {best_fitness.composite_fitness} to {candidate_fitness.composite_fitness}"
                    if improved
                    else f"Syntax cleanly remediated at fitness {best_fitness.composite_fitness}"
                )
                current_best = mutated
                best_fitness = candidate_fitness
            else:
                decision = "DISCARD"
                rationale = f"Candidate fitness {candidate_fitness.composite_fitness} did not beat current best {best_fitness.composite_fitness}"

            record = IterationRecord(
                iteration=step,
                timestamp=utc_now(),
                mutation_type=mutation_type,
                fitness_before=best_fitness.composite_fitness,
                fitness_after=candidate_fitness.composite_fitness,
                decision=decision,
                score_details=candidate_fitness.to_dict(),
                rationale=rationale,
            )
            history.append(record)
            self._append_ledger(draft_name, record)

        # Save improved draft back to vault if modified
        if current_best != initial_content:
            initial_doc["content"] = current_best
            self.vault.save_markdown(
                "drafts",
                draft_name,
                current_best,
                initial_doc.get("frontmatter", {}) or {},
            )

        return {
            "draft_name": draft_name,
            "target_venue": target_venue,
            "initial_fitness": history[0].fitness_before if history else best_fitness.composite_fitness,
            "final_fitness": best_fitness.composite_fitness,
            "iterations_run": len(history),
            "kept_count": sum(1 for r in history if r.decision == "KEEP"),
            "discarded_count": sum(1 for r in history if r.decision == "DISCARD"),
            "history": [r.to_dict() for r in history],
            "best_score": best_fitness.to_dict(),
        }

    def _append_ledger(self, draft_name: str, record: IterationRecord) -> None:
        entry = {
            "draft": draft_name,
            **record.to_dict(),
        }
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
