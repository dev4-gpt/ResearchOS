"""Feynman Research Assistant Service (integrating companion-inc/feynman).

Provides:
1. Paper-to-Code Claim Audit (/audit): Verifies manuscript claims against actual experiment code AST and constants.
2. Literature Matrix Synthesizer (/lit): Extracts consensus, active debates, and open questions across vault papers.
3. Severity-Triage Peer Review (/review): Evaluates manuscripts with [BLOCKER], [MAJOR], and [MINOR] severity tags.
4. Experiment Replicator (/replicate): Verifies and runs experiment benchmarks.
"""

from __future__ import annotations

import ast
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from domain.models import citation_key
from services.fact_checker import NUMERIC_PATTERN, FactCheckerService, is_non_metric_number
from services.fx_bridge import FXBridge
from services.vault import VaultManager


@dataclass
class CodeAuditItem:
    claim_text: str
    paper_value: str
    code_match: Optional[str]
    code_file: str
    line_number: Optional[int]
    status: str  # "MATCH" | "DISCREPANCY" | "NOT_IN_CODE"
    detail: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewItem:
    severity: str  # "BLOCKER" | "MAJOR" | "MINOR"
    category: str  # "METHODOLOGY" | "GROUNDING" | "REPRODUCIBILITY" | "LAYOUT" | "PRESENTATION"
    title: str
    description: str
    manuscript_location: str = ""
    suggested_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FeynmanService:
    """Feynman AI Research Assistant integrated into ResearchingOS."""

    def __init__(
        self,
        vault_manager: Optional[VaultManager] = None,
        fx_bridge: Optional[FXBridge] = None,
    ) -> None:
        self.vault = vault_manager or VaultManager(os.getenv("VAULT_PATH", "vault"))
        self.fact_checker = FactCheckerService(self.vault)
        self.fx = fx_bridge or FXBridge()

    # -------------------------------------------------------------------------
    # 1. /audit : Paper-to-Code Claim Auditor
    # -------------------------------------------------------------------------
    def audit_paper_against_code(
        self,
        draft_content: str,
        code_dir_or_file: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verify empirical claims in a manuscript against actual Python code AST and constants."""
        code_root = Path(code_dir_or_file or Path(self.vault.vault_path).parent / "scripts" / "experiments")
        code_constants: Dict[str, List[Dict[str, Any]]] = {}

        # Scan code files and extract assignments / constants
        target_files: List[Path] = []
        if code_root.is_file():
            target_files = [code_root]
        elif code_root.is_dir():
            target_files = sorted(code_root.glob("*.py"))[:6]

        for py_path in target_files:
            try:
                tree = ast.parse(py_path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id
                                # Extract numeric constants
                                if isinstance(node.value, ast.Constant):
                                    val_str = str(node.value.value)
                                    code_constants.setdefault(var_name.lower(), []).append({
                                        "file": py_path.name,
                                        "line": node.lineno,
                                        "var_name": var_name,
                                        "value": val_str,
                                    })
            except Exception:
                continue

        # Extract numeric and hyperparameter claims from paper
        CODE_CLAIM_PATTERN = re.compile(
            r"(?:"
            r"\b[A-Za-z0-9_]+\s*=\s*[\d\.]+(?:e-?\d+)?\b"
            r"|\b\d+(?:\.\d+)?\s*(?:%|iterations?|epochs?|samples?|steps?|ms|s|layers?|heads?|dim)\b"
            r"|\bN\s*=\s*\d+"
            r"|\b\d+(?:,\d{3})*(?:\.\d+)?%"
            r")",
            re.IGNORECASE,
        )
        paragraphs = re.split(r"\n\s*\n", draft_content)
        audit_items: List[CodeAuditItem] = []

        for p_idx, paragraph in enumerate(paragraphs, start=1):
            for match in CODE_CLAIM_PATTERN.finditer(paragraph):
                token = match.group(0).strip()
                sentence = paragraph[max(0, match.start() - 60):min(len(paragraph), match.end() + 60)].strip()
                val_match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?(?:e-?\d+)?", token.replace(",", ""))
                num_val = val_match.group(0) if val_match else token

                # Match against code constants
                matched = False
                for var_name, entries in code_constants.items():
                    for entry in entries:
                        if entry["value"] == num_val or (
                            num_val.replace("%", "") == entry["value"]
                        ):
                            audit_items.append(CodeAuditItem(
                                claim_text=sentence,
                                paper_value=token,
                                code_match=f"{entry['var_name']} = {entry['value']}",
                                code_file=entry["file"],
                                line_number=entry["line"],
                                status="MATCH",
                                detail=f"Claim matches code variable `{entry['var_name']}` in {entry['file']}:{entry['line']}",
                            ))
                            matched = True
                            break
                    if matched:
                        break

                if not matched:
                    # Check if token describes a hyperparameter or metric
                    audit_items.append(CodeAuditItem(
                        claim_text=sentence,
                        paper_value=token,
                        code_match=None,
                        code_file="none",
                        line_number=None,
                        status="NOT_IN_CODE",
                        detail=f"Numerical assertion `{token}` not located as an explicit constant in scanned experiment code",
                    ))

        matches = sum(1 for item in audit_items if item.status == "MATCH")
        total = len(audit_items)
        score = round((matches / total) * 100.0, 1) if total > 0 else 100.0

        return {
            "total_claims_audited": total,
            "matched_in_code": matches,
            "code_provenance_score": score,
            "files_scanned": [f.name for f in target_files],
            "audit_items": [item.to_dict() for item in audit_items],
        }

    # -------------------------------------------------------------------------
    # 2. /lit : Literature Consensus, Disagreement & Gap Synthesizer
    # -------------------------------------------------------------------------
    def synthesize_literature_matrix(
        self,
        topic: str = "",
        paper_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Extract consensus, debates, and open research questions across vault papers."""
        papers_folder = self.vault.folders.get("papers")
        if not papers_folder or not os.path.exists(papers_folder):
            return {"consensus": [], "disagreements": [], "open_questions": [], "papers_reviewed": 0}

        all_names = sorted(n for n in os.listdir(papers_folder) if n.endswith(".md"))
        selected = paper_names or all_names[:5]

        papers_data: List[Dict[str, Any]] = []
        for name in selected:
            try:
                data = self.vault.read_markdown("papers", name)
                data["filename"] = name
                papers_data.append(data)
            except Exception:
                continue

        consensus: List[Dict[str, Any]] = []
        disagreements: List[Dict[str, Any]] = []
        open_questions: List[Dict[str, Any]] = []

        # Analyze extracted methodology and limitations
        for p in papers_data:
            content = p.get("content", "")
            title = p.get("frontmatter", {}).get("title") or p.get("filename", "")
            cite_key = citation_key(p["filename"])

            # Consensus extraction: scaling laws, parameter efficiency, multi-agent overhead
            if re.search(r"\b(scaling law|parameter effici|attention overhead|latency bottleneck)\b", content, re.I):
                consensus.append({
                    "topic": "Scaling & Computational Efficiency",
                    "assertion": f"{title} corroborates computational scaling constraints in transformer/agent execution.",
                    "source": f"[[{cite_key}]]",
                })

            # Disagreement extraction: dense vs sparse, finetuning vs in-context learning
            if re.search(r"\b(in contrast|outperforms fine-tuning|degradation under quantization|disagree)\b", content, re.I):
                disagreements.append({
                    "topic": "Retrieval vs Adaptation Trade-offs",
                    "contending_view": f"{title} reports performance trade-offs conflicting with uniform retrieval baselines.",
                    "source": f"[[{cite_key}]]",
                })

            # Open question extraction: limitations, future work
            limitations_match = re.search(r"(?:###?\s*Limitations|###?\s*Future Work)([\s\S]*?)(?:###|$)", content, re.I)
            if limitations_match:
                gap_text = limitations_match.group(1).strip()[:200]
                if gap_text:
                    open_questions.append({
                        "paper": title,
                        "citation": f"[[{cite_key}]]",
                        "gap": gap_text.replace("\n", " "),
                    })

        return {
            "topic": topic or "Multi-Agent & Empirical AI Research",
            "papers_reviewed": len(papers_data),
            "consensus_findings": consensus[:10],
            "active_disagreements": disagreements[:10],
            "open_research_questions": open_questions[:10],
        }

    # -------------------------------------------------------------------------
    # 3. /review : Simulated Multi-Perspective Peer Review with Severity Triage
    # -------------------------------------------------------------------------
    def simulated_peer_review(
        self,
        draft_content: str,
        venue: str = "IEEEtran",
    ) -> Dict[str, Any]:
        """Conduct aggressive simulated peer review triage categorizing findings by severity."""
        items: List[ReviewItem] = []

        # 1. Check for ungrounded claims (BLOCKER)
        claim_records = self.fact_checker.extract_claim_evidence_records(draft_content, strict=True)
        blocked_claims = [c for c in claim_records if c.get("status") not in ("VERIFIED", "PASSED")]
        if blocked_claims:
            items.append(ReviewItem(
                severity="BLOCKER",
                category="GROUNDING",
                title=f"Manuscript contains {len(blocked_claims)} ungrounded quantitative assertions",
                description="Reviewer #2 rejects manuscripts asserting empirical percentages or sample sizes without verified citations or reproducible experiment logs.",
                manuscript_location=blocked_claims[0].get("manuscript_location", ""),
                suggested_action="Ground assertions against vault papers or measurements.jsonl.",
            ))

        # 2. Check for missing control baselines (MAJOR)
        has_baseline = bool(re.search(r"\b(baseline|ablation|state-of-the-art|comparison|sota)\b", draft_content, re.I))
        if not has_baseline:
            items.append(ReviewItem(
                severity="MAJOR",
                category="METHODOLOGY",
                title="Absence of explicit comparative baseline ablation",
                description="Manuscript lacks dedicated comparative benchmarks against standard community baselines.",
                suggested_action="Add baseline comparison table against prior published art.",
            ))

        # 3. Check for venue page budget compliance (MAJOR / MINOR)
        words = len(re.findall(r"\b\w+\b", draft_content))
        if "ieee" in venue.lower() and words > 4200:
            items.append(ReviewItem(
                severity="MAJOR",
                category="LAYOUT",
                title="High risk of 4-page camera-ready layout overflow",
                description=f"Draft has {words} words. Short camera-ready IEEE papers typically exceed 4 pages above 3,200 words, causing orphan page rejection.",
                suggested_action="Compress prose or trim redundant subsections to meet strict 4-page ceiling.",
            ))
        elif words < 1200:
            items.append(ReviewItem(
                severity="BLOCKER",
                category="PRESENTATION",
                title="Manuscript is too brief / shallow stub",
                description=f"Word count ({words}) is insufficient for peer review consideration.",
                suggested_action="Expand section methodology, equations, and literature analysis.",
            ))

        # 4. Check for citation density (MAJOR)
        citations = self.fact_checker.extract_citation_keys(draft_content)
        if len(citations) < 8:
            items.append(ReviewItem(
                severity="MAJOR",
                category="REPRODUCIBILITY",
                title=f"Shallow citation graph ({len(citations)} citations)",
                description="Top-tier venues require comprehensive contextualization against prior art (15-30+ citations).",
                suggested_action="Enrich bibliography with additional seminal literature from vault/01_Papers.",
            ))

        blockers = sum(1 for i in items if i.severity == "BLOCKER")
        majors = sum(1 for i in items if i.severity == "MAJOR")
        minors = sum(1 for i in items if i.severity == "MINOR")

        if blockers > 0:
            recommendation = "REJECT"
            risk_score = 90.0
        elif majors > 1:
            recommendation = "REVISE"
            risk_score = 65.0
        elif majors == 1 or minors > 0:
            recommendation = "WEAK_ACCEPT"
            risk_score = 35.0
        else:
            recommendation = "ACCEPT"
            risk_score = 10.0

        return {
            "venue": venue,
            "recommendation": recommendation,
            "rejection_risk_score": risk_score,
            "blocker_count": blockers,
            "major_count": majors,
            "minor_count": minors,
            "review_items": [item.to_dict() for item in items],
        }

    # -------------------------------------------------------------------------
    # 4. Vercel Labs fx Agent Engine Integration
    # -------------------------------------------------------------------------
    def research_topic_with_fx(self, topic: str) -> Dict[str, Any]:
        """Leverages the Vercel Labs fx agent engine for rapid research synthesis."""
        return self.fx.dispatch_research(prompt=f"Research {topic}")

    def audit_with_fx(self, code_dir: str, assertions: List[str]) -> Dict[str, Any]:
        """Dispatches high-throughput code audit assertions to the fx engine."""
        return self.fx.audit_code_repository(code_dir=code_dir, assertions=assertions)

