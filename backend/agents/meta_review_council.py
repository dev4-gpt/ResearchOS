"""Meta-Review & Cross-Venue Alignment Council (Tier 2 Multi-Agent Orchestration).

Orchestrates a four-agent council to expand raw drafts into publication-grade,
15-30+ citation authoritative literature reviews matching exact target venue style files.
"""

import os
import re
import json
import time
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel

from services.vault import VaultManager
from services.llm_router import llm_router
from services.venue_profiles import VENUE_PROFILES, SUPPORTED_VENUES
from services.latex_exporter import LaTeXExporterService

# Load master venue prompt for reference
_MASTER_PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "vault", "00_System", "MASTER_VENUE_WRITING_PROMPT.md"
)

def _load_master_prompt() -> str:
    try:
        with open(_MASTER_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


_WIKILINK_RE = re.compile(r"\[\[(.*?)\]\]")


def _citation_ids(text: str) -> set:
    """Extracts the paper-id half of every [[id]] or [[id|Label]] wikilink.

    Mirrors VaultManager.get_knowledge_graph's wikilink_re (services/vault.py) so
    citation counts here agree with the vault's own notion of what's cited --
    a plain `\\[\\[([^\\]]+)\\]\\]` would count "id|Label" as a distinct citation
    from "id" and fail to recognize an aliased link as already present.
    """
    return {link.split("|", 1)[0].strip() for link in _WIKILINK_RE.findall(text)}


def _extract_json_array(text: str) -> List[str]:
    """Pulls a JSON array of strings out of an LLM response, tolerating markdown fences/prose."""
    if not text:
        return []
    match = re.search(r"\[.*\]", text, flags=re.DOTALL)
    if not match:
        return []
    try:
        parsed = json.loads(match.group(0))
    except (json.JSONDecodeError, ValueError):
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed if isinstance(item, (str, int, float))]

META_COUNCIL_PERSONAS = {
    "CouncilChair": {
        "name": "Meta-Review Council Chair",
        "role": "Venue Readiness & Rubric Assessment",
        "provider": "GEMINI",
        "model": "gemini-2.5-flash",
        "instruction": (
            "You are the Chairman of the Meta-Review Council and Senior Area Chair for IEEE/ACM/NeurIPS venues. "
            "You audit manuscript submissions for structural completeness, section depth, word count adequacy, "
            "and target venue compliance. You identify shallow stubs and assign actionable directives to the council."
        )
    },
    "CitationExpander": {
        "name": "Citation Graph Expander",
        "role": "Vault Citation Enrichment (15-30+ Citations)",
        "provider": "OPENROUTER",
        "model": "meta-llama/llama-3.1-8b-instruct",
        "instruction": (
            "You are a Senior Bibliometric & Citation Graph Architect. "
            "Your objective is to enrich manuscript drafts with 15–30+ authentic peer-reviewed citations "
            "formatted as Obsidian wikilinks [[paper_id]]. You ensure zero orphan claims, dense paragraph grounding, "
            "and cross-referencing against the primary vault corpus."
        )
    },
    "RigorAuditor": {
        "name": "Technical Depth & Rigor Auditor",
        "role": "Formal Proofs, Tables & Empirical Rigor",
        "provider": "GROQ",
        "model": "llama-3.1-8b-instant",
        "instruction": (
            "You are a Principal Systems Auditor and Quantitative Methods Specialist. "
            "You evaluate drafts for mathematical rigor, formal LaTeX equations, tabular comparison matrices "
            "(tabular environments), sample size grounding (N=...), and Lyapunov stability bounds."
        )
    },
    "VenueRectifier": {
        "name": "Cross-Venue Publisher & Sanitizer",
        "role": "Venue Formatting & AI Artifact Scrubbing",
        "provider": "OLLAMA",
        "model": "qwen3.5:4b",
        "instruction": (
            "You are the Senior Cross-Venue Publication Editor. You reformat manuscripts precisely for target venue "
            "style files (IEEEtran, NeurIPS, ICML, CVPR, ACL, ACM). You enforce single-numbered sections, format "
            "executive abstracts, and ruthlessly scrub all synthetic AI filler words (delve into, tapestry of, crucial role)."
        )
    }
}

class MetaReviewResult(BaseModel):
    project_id: str
    target_venue: str
    target_length: str
    initial_words: int
    final_words: int
    initial_citations: int
    final_citations: int
    initial_score: float
    final_score: float
    tables_count: int
    equations_count: int
    revised_draft: str
    logs: List[Dict[str, Any]]

class MetaReviewCouncil:
    def __init__(self, vault_path: str = "../vault"):
        self.vault_manager = VaultManager(vault_path)
        self.exporter = LaTeXExporterService(self.vault_manager)

    def run_alignment_cycle(
        self,
        draft_content: str,
        target_venue: str = "IEEEtran",
        target_length: str = "full_journal",
        log_callback: Optional[Callable[[str, str, str, Optional[Dict[str, Any]]], None]] = None,
        is_dry_run: bool = False
    ) -> Dict[str, Any]:
        """Executes the full 4-agent Tier 2 Meta-Review and Cross-Venue Alignment Council."""

        def _log(stage: str, agent: str, message: str, data: Optional[Dict[str, Any]] = None):
            if log_callback:
                log_callback(stage, agent, message, data)

        _log("Initialization", "Meta-Review Council Chair", f"Convening Tier 2 Council for target venue: {target_venue} ({target_length})...")

        # Step 1: Chair Audit
        initial_words = len(draft_content.split())
        initial_citations = len(_citation_ids(draft_content))
        initial_tables = len(re.findall(r'\\begin\{tabular\}', draft_content))
        initial_equations = len(re.findall(r'\\begin\{equation\}|\$\$', draft_content))

        _log("Audit", "Meta-Review Council Chair", 
             f"Initial Draft Baseline: {initial_words} words, {initial_citations} unique citations, {initial_tables} tables, {initial_equations} equations.",
             {
                 "initial_words": initial_words,
                 "initial_citations": initial_citations,
                 "tables": initial_tables,
                 "equations": initial_equations,
             })

        # Step 2: Citation Graph Expander
        missing_requirements: List[str] = []
        warnings: List[str] = []
        _log("Citation-Expansion", "Citation Graph Expander", "Scanning vault paper corpus to expand citations toward 20-30+ density target...")
        vault_papers = self.vault_manager.list_files("papers")
        available_papers = [
            {
                "id": p["filename"].replace(".md", ""),
                "title": p.get("title", ""),
                "preview": p.get("content_preview", ""),
            }
            for p in vault_papers
            if not p["filename"].startswith(".")
        ]

        expanded_draft = draft_content
        newly_cited: List[str] = []
        if not available_papers:
            _log("Citation-Expansion", "Citation Graph Expander", "Vault paper corpus is empty; no candidate citations exist to ground the draft in.")
        else:
            # A fixed reference list forced into every manuscript regardless of
            # relevance is the same fabrication pattern as the empirical table:
            # it hits a density target with content that may not exist in the
            # vault or have anything to do with the draft. Instead, ask the
            # CitationExpander LLM to pick only from papers that genuinely exist
            # in the vault, and only insert ids it names -- never an invented one.
            persona = META_COUNCIL_PERSONAS["CitationExpander"]
            already_cited = _citation_ids(expanded_draft)
            candidates = [p for p in available_papers if p["id"] not in already_cited]
            if not candidates:
                _log("Citation-Expansion", "Citation Graph Expander", "Every vault paper is already cited in this draft.")
            elif is_dry_run:
                # Mirrors CouncilOrchestrator's dry-run contract elsewhere in this
                # codebase: a dry run must never place a live, potentially billed
                # API call. main.py already threads is_dry_run through for this.
                _log(
                    "Citation-Expansion",
                    "Citation Graph Expander",
                    f"Dry run: skipping live relevance check against {len(candidates)} candidate paper(s); no citations added.",
                )
            else:
                catalog = "\n".join(
                    f"- {p['id']}: {p['title']} — {p['preview'][:150]}" for p in candidates
                )
                prompt = (
                    f"Manuscript draft (target venue: {target_venue}):\n{draft_content[:6000]}\n\n"
                    f"Candidate vault papers (id: title — preview):\n{catalog}\n\n"
                    "List ONLY the paper ids from the candidate list above that are topically relevant to this "
                    "draft's actual claims and would genuinely belong in its References section. Respond with a "
                    "JSON array of ids only, e.g. [\"arxiv_1234.5678\"]. If none are relevant, respond with []. "
                    "Never invent an id that is not in the candidate list."
                )
                response = llm_router.generate_content(
                    prompt,
                    system_instruction=persona["instruction"],
                    provider=persona["provider"],
                    model=persona["model"],
                )
                if not response or response.startswith("[Error]"):
                    warnings.append("citation_expansion_unavailable")
                    _log(
                        "Citation-Expansion",
                        "Citation Graph Expander",
                        f"LLM relevance check unavailable ({response or 'no response'}); no citations added without grounding.",
                    )
                else:
                    valid_ids = {p["id"] for p in candidates}
                    for ref_id in _extract_json_array(response):
                        if (
                            ref_id in valid_ids
                            and ref_id not in _citation_ids(expanded_draft)
                            and "## References" in expanded_draft
                        ):
                            expanded_draft = expanded_draft.replace("## References", f"- [[{ref_id}]]\n## References", 1)
                            newly_cited.append(ref_id)

        final_citations = len(_citation_ids(expanded_draft))
        _log(
            "Citation-Expansion",
            "Citation Graph Expander",
            f"Citation Expansion Complete: {final_citations} distinct citations grounded in real vault papers"
            + (f" ({len(newly_cited)} newly added: {', '.join(newly_cited)})" if newly_cited else ""),
        )

        # Step 3: Technical Depth & Rigor Auditor
        _log("Rigor-Audit", "Technical Depth & Rigor Auditor", "Auditing formal proofs, Lyapunov stability constraints, and experimental tables...")
        if "\\begin{tabular}" not in expanded_draft:
            # This council has no wired source of real measured results (no
            # ExperimentRecorder/ledger access -- only the paper/concept/debate/
            # draft vault categories). Inventing benchmark numbers here would be
            # exactly the "estimate instead of measure" failure this project's
            # gate exists to catch (HANDOFF.md: "if a claim cannot be measured,
            # delete it, do not estimate"). Flag the gap instead of fabricating it.
            missing_requirements.append("empirical_results_table")
            _log(
                "Rigor-Audit",
                "Technical Depth & Rigor Auditor",
                "Gate failure: manuscript has no empirical results table (\\begin{tabular}), and no measured "
                "experiment data is available to this council to generate one. Refusing to fabricate results -- "
                "add a \\begin{tabular} table sourced from a real experiment run before resubmission."
            )

        # Step 4: Venue Rectifier & Sanitizer
        _log("Venue-Rectification", "Cross-Venue Publisher & Sanitizer", f"Sanitizing AI filler phrases and aligning layout to {target_venue} style profile...")
        banned_phrases = [
            (r"\bdelve\s+into\b", "investigate"),
            (r"\btapestry\s+of\b", "framework of"),
            (r"\bcrucial\s+role\b", "significant impact"),
            (r"\bit\s+is\s+important\s+to\s+note\s+that\b", "specifically,"),
            (r"\bgame-changer\b", "major advance"),
            (r"\bmasterclass\b", "rigorous study"),
            (r"\blandscape\s+of\b", "domain of"),
            (r"\bdeep\s+dive\b", "in-depth analysis"),
        ]
        for pattern, replacement in banned_phrases:
            expanded_draft = re.sub(pattern, replacement, expanded_draft, flags=re.IGNORECASE)

        final_words = len(expanded_draft.split())
        final_tables = len(re.findall(r'\\begin\{tabular\}', expanded_draft))
        final_equations = len(re.findall(r'\\begin\{equation\}|\$\$', expanded_draft))

        # The decision must reflect what was actually found, not a constant --
        # the council cannot certify a manuscript as publication-ready while a
        # required element (the results table) is known to be missing.
        decision = "REMEDIATION_REQUIRED" if missing_requirements else "APPROVED_FOR_HUMAN_REVIEW"

        _log("Consensus", "Meta-Review Council Chair",
             f"Meta-Review Alignment Council Concluded: Final words: {final_words}, Citations: {final_citations}, "
             f"Tables: {final_tables}, Equations: {final_equations}. Decision: {decision}"
             + (f" (missing: {', '.join(missing_requirements)})" if missing_requirements else "")
             + (f" (warnings: {', '.join(warnings)})" if warnings else ""),
             {
                 "final_words": final_words,
                 "final_citations": final_citations,
                 "final_tables": final_tables,
                 "final_equations": final_equations,
                 "decision": decision,
                 "missing_requirements": missing_requirements,
                 "warnings": warnings,
             })

        return {
            "success": True,
            "target_venue": target_venue,
            "target_length": target_length,
            "initial_words": initial_words,
            "final_words": final_words,
            "initial_citations": initial_citations,
            "final_citations": final_citations,
            "initial_tables": initial_tables,
            "final_tables": final_tables,
            "initial_equations": initial_equations,
            "final_equations": final_equations,
            "revised_draft": expanded_draft,
            "decision": decision,
            "missing_requirements": missing_requirements,
            "warnings": warnings,
        }
