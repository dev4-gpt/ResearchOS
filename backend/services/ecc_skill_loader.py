"""affaan-m/ECC (Everything Claude Code) Departmental Skill Loader for ResearchingOS.

Provides cross-departmental agent skill discovery, inspection, and runtime integration
from the affaan-m/ECC repository (288+ skills across Engineering, Research, QA, Security,
and Product Strategy).
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ECCSkillLoader:
    """Discovers, parses, and surfaces ECC skills for autonomous council augmentation."""

    # Candidate upstream ECC paths on the system
    CANDIDATE_PATHS = [
        Path("/Users/aryamandev/.claude/plugins/marketplaces/ecc/skills"),
        Path("/Users/aryamandev/Documents/Codex/Projects/AgentOS/ecc-integration-artifacts/upstream/skills"),
        Path(__file__).resolve().parent.parent.parent / ".agents" / "skills" / "ecc",
    ]

    DEPARTMENT_MAPPING = {
        "Engineering & Autonomous Systems": [
            "autonomous-loops",
            "autonomous-agent-harness",
            "agent-eval",
            "agent-architecture-audit",
            "agent-harness-construction",
            "agent-introspection-debugging",
            "agent-self-evaluation",
            "agentic-engineering",
            "agentic-os",
            "ai-first-engineering",
            "backend-patterns",
            "api-design",
            "api-connector-builder",
        ],
        "Research & Empirical Methodology": [
            "benchmark",
            "benchmark-methodology",
            "benchmark-optimization-loop",
            "article-writing",
            "scientific-analysis",
        ],
        "Quality Assurance & Security": [
            "ai-regression-testing",
            "automation-audit-ops",
            "browser-qa",
            "accessibility",
            "security-audit",
        ],
        "Product & Architecture Strategy": [
            "architecture-decision-records",
            "blueprint",
            "brand-voice",
            "brand-discovery",
        ],
    }

    def __init__(self, custom_skills_path: Optional[str] = None):
        self.skills_dir = self._resolve_skills_dir(custom_skills_path)

    def _resolve_skills_dir(self, custom_path: Optional[str] = None) -> Path:
        if custom_path:
            p = Path(custom_path)
            if p.exists():
                return p

        for candidate in self.CANDIDATE_PATHS:
            if candidate.exists() and candidate.is_dir():
                return candidate

        # Fallback to local workspace skills directory
        fallback = Path(__file__).resolve().parent.parent.parent / ".agents" / "skills" / "ecc"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

    def get_status(self) -> Dict[str, Any]:
        """Returns discovery status and skill counts."""
        exists = self.skills_dir.exists()
        count = len(list(self.skills_dir.glob("*/SKILL.md"))) if exists else 0
        return {
            "source_path": str(self.skills_dir),
            "available": exists and count > 0,
            "total_skills_discovered": count,
            "departments": list(self.DEPARTMENT_MAPPING.keys()),
        }

    def parse_skill_md(self, skill_md_path: Path) -> Dict[str, Any]:
        """Parses frontmatter and body of an ECC SKILL.md file."""
        if not skill_md_path.exists():
            return {}

        content = skill_md_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = {}
        body = content

        # Extract YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                raw_fm = parts[1]
                body = parts[2].strip()
                for line in raw_fm.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        frontmatter[k] = v

        name = frontmatter.get("name") or skill_md_path.parent.name
        description = frontmatter.get("description", "")
        
        # Determine department
        department = "General Cross-Functional"
        for dept_name, skills in self.DEPARTMENT_MAPPING.items():
            if name in skills or any(term in name for term in ["agent", "eval", "loop", "benchmark"]):
                if "eval" in name or "loop" in name or "agent" in name:
                    department = "Engineering & Autonomous Systems"
                    break
                elif "benchmark" in name or "writing" in name:
                    department = "Research & Empirical Methodology"
                    break

        return {
            "name": name,
            "department": department,
            "description": description,
            "frontmatter": frontmatter,
            "body": body[:1500],  # preview
            "full_path": str(skill_md_path),
        }

    def list_skills(
        self,
        department: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Lists skills with optional department filtering and search query."""
        if not self.skills_dir.exists():
            return []

        results = []
        for skill_dir in sorted(self.skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill_data = self.parse_skill_md(skill_file)
                    
                    # Filter by query
                    if query:
                        q = query.lower()
                        if (
                            q not in skill_data["name"].lower()
                            and q not in skill_data["description"].lower()
                        ):
                            continue

                    # Filter by department
                    if department:
                        if department.lower() not in skill_data["department"].lower():
                            continue

                    results.append(skill_data)
                    if len(results) >= limit:
                        break

        return results

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Fetches full content and metadata for a specific skill by name."""
        skill_dir = self.skills_dir / name
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            # Try case-insensitive search
            for d in self.skills_dir.iterdir():
                if d.is_dir() and d.name.lower() == name.lower():
                    skill_file = d / "SKILL.md"
                    break

        if not skill_file.exists():
            return None

        data = self.parse_skill_md(skill_file)
        # Include full unclipped markdown for execution context
        data["body"] = skill_file.read_text(encoding="utf-8", errors="replace")
        return data

    def sync_core_skills_to_workspace(self, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """Copies vital ECC core skills directly into workspace .agents/skills/ecc/ for local execution."""
        dest = Path(target_dir) if target_dir else (
            Path(__file__).resolve().parent.parent.parent / ".agents" / "skills" / "ecc"
        )
        dest.mkdir(parents=True, exist_ok=True)

        copied = []
        vital_skills = [
            "autonomous-loops",
            "autonomous-agent-harness",
            "agent-eval",
            "agent-self-evaluation",
            "agent-architecture-audit",
            "benchmark-methodology",
            "benchmark-optimization-loop",
            "agentic-engineering",
            "article-writing",
        ]

        for skill_name in vital_skills:
            source = self.skills_dir / skill_name
            if source.exists() and source.is_dir():
                target_skill_dir = dest / skill_name
                if not target_skill_dir.exists():
                    shutil.copytree(source, target_skill_dir)
                    copied.append(skill_name)

        return {
            "destination": str(dest),
            "copied_count": len(copied),
            "skills": copied,
        }
