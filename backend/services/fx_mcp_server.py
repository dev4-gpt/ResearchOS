"""ResearchingOS Model Context Protocol (MCP) Server for Vercel Labs fx.

Exposes ResearchingOS's literature vault, zero-hallucination fact checking,
Feynman AST paper-to-code auditing, and 12-venue LaTeX publisher as standard
Model Context Protocol (MCP) tools that fx or any MCP client can consume.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.fact_checker import FactCheckerService
from services.feynman_service import FeynmanService
from services.vault import VaultManager


class ResearchOSMCPServer:
    """MCP Server exposing ResearchingOS publishing and verification tools."""

    def __init__(self, vault_path: Optional[str] = None) -> None:
        v_path = vault_path or os.getenv("VAULT_PATH", "vault")
        self.vault = VaultManager(v_path)
        self.fact_checker = FactCheckerService(self.vault)
        self.feynman = FeynmanService(self.vault)

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns MCP-compliant tool definitions and JSON schemas."""
        return [
            {
                "name": "researchos_vault_query",
                "description": "Search papers, concepts, and debate notes stored in the ResearchingOS Obsidian Vault.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search keyword or paper topic"},
                        "category": {
                            "type": "string",
                            "enum": ["papers", "concepts", "debates", "drafts", "all"],
                            "description": "Vault directory to search within",
                            "default": "all",
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "researchos_fact_check",
                "description": "Audit manuscript markdown for zero hallucinated citations and grounded numerical claims.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Markdown text of manuscript draft"},
                        "strict": {"type": "boolean", "description": "Enforce strict fail-closed gating", "default": True},
                    },
                    "required": ["content"],
                },
            },
            {
                "name": "researchos_feynman_code_audit",
                "description": "Cross-examine numerical paper claims against actual Python experiment code AST constants.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "draft_name": {"type": "string", "description": "Filename of manuscript in vault/04_Drafts"},
                        "code_path": {"type": "string", "description": "Path to Python script or experiment directory"},
                    },
                    "required": ["draft_name"],
                },
            },
            {
                "name": "researchos_simulated_peer_review",
                "description": "Run Reviewer #2 simulated peer review triage with [BLOCKER], [MAJOR], [MINOR] tags.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "draft_name": {"type": "string", "description": "Filename of manuscript in vault/04_Drafts"},
                        "venue": {
                            "type": "string",
                            "enum": ["IEEEtran", "NeurIPS", "ICML", "ACM", "CVPR", "ACL"],
                            "default": "IEEEtran",
                        },
                    },
                    "required": ["draft_name"],
                },
            },
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches an MCP tool call and returns structured JSON output."""
        if tool_name == "researchos_vault_query":
            query = arguments.get("query", "").lower()
            category = arguments.get("category", "all")
            target_dirs = ["01_Papers", "02_Concepts", "03_Debates", "04_Drafts"]
            if category == "papers":
                target_dirs = ["01_Papers"]
            elif category == "concepts":
                target_dirs = ["02_Concepts"]
            elif category == "debates":
                target_dirs = ["03_Debates"]
            elif category == "drafts":
                target_dirs = ["04_Drafts"]

            matches = []
            vault_p = Path(self.vault.vault_path)
            for d in target_dirs:
                sub_dir = vault_p / d
                if sub_dir.exists():
                    for md in sorted(sub_dir.glob("*.md"))[:15]:
                        try:
                            text = md.read_text(encoding="utf-8")
                            if query in text.lower() or query in md.name.lower():
                                matches.append({
                                    "filename": md.name,
                                    "category": d,
                                    "snippet": text[:200].replace("\n", " "),
                                })
                        except Exception:
                            continue
            return {"total_matches": len(matches), "matches": matches[:10]}

        elif tool_name == "researchos_fact_check":
            content = arguments.get("content", "")
            strict = arguments.get("strict", True)
            report = self.fact_checker.audit_document(content, source_texts=[], strict_evidence=strict)
            return {
                "fact_check_score": report.get("fact_check_score", 0),
                "status": report.get("status", "unknown"),
                "total_claims": report.get("claim_report", {}).get("total_claims", 0),
                "blocked_claims": report.get("claim_report", {}).get("blocked_count", 0),
                "blocking_errors": report.get("blocking_errors", []),
            }

        elif tool_name == "researchos_feynman_code_audit":
            draft_name = arguments.get("draft_name", "")
            if not draft_name.endswith(".md"):
                draft_name += ".md"
            doc = self.vault.read_markdown("drafts", draft_name)
            content = doc.get("content", "")
            code_path = arguments.get("code_path")
            return self.feynman.audit_paper_against_code(content, code_dir_or_file=code_path)

        elif tool_name == "researchos_simulated_peer_review":
            draft_name = arguments.get("draft_name", "")
            if not draft_name.endswith(".md"):
                draft_name += ".md"
            doc = self.vault.read_markdown("drafts", draft_name)
            content = doc.get("content", "")
            venue = arguments.get("venue", "IEEEtran")
            return self.feynman.simulated_peer_review(content, venue=venue)

        else:
            raise ValueError(f"Unknown MCP tool: {tool_name}")
