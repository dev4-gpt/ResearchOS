"""Universal Skills Discovery Service for ResearchingOS.

Discovers and inspects globally installed skills from ~/.claude/skills and local .agents/skills
without duplicating storage or copying repositories.
Surfaces the 36+ UI, design, anti-slop, slides, and diagramming tools requested by the user.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class UniversalSkillsService:
    """Discovers and parses metadata for universally installed skills."""

    GLOBAL_SKILLS_PATH = Path(os.path.expanduser("~/.claude/skills"))
    LOCAL_SKILLS_PATH = Path(".agents/skills")

    CATEGORY_MAP = {
        "ui-ux-pro-max": "ui_ux_design",
        "design": "ui_ux_design",
        "design-system": "ui_ux_design",
        "ui-styling": "ui_ux_design",
        "brand": "ui_ux_design",
        "banner-design": "ui_ux_design",
        "brandkit": "ui_ux_design",
        "design-taste-frontend": "frontend_taste",
        "design-taste-frontend-v1": "frontend_taste",
        "high-end-visual-design": "frontend_taste",
        "minimalist-ui": "frontend_taste",
        "redesign-existing-projects": "frontend_taste",
        "gpt-taste": "frontend_taste",
        "stitch-design-taste": "frontend_taste",
        "industrial-brutalist-ui": "frontend_taste",
        "image-to-code": "frontend_taste",
        "imagegen-frontend-web": "frontend_taste",
        "imagegen-frontend-mobile": "frontend_taste",
        "impeccable": "frontend_taste",
        "stop-slop": "academic_voice",
        "humanizer": "academic_voice",
        "frontend-slides": "presentation",
        "slides": "presentation",
        "diagram-design": "diagrams",
        "understand": "code_comprehension",
        "understand-chat": "code_comprehension",
        "understand-dashboard": "code_comprehension",
        "understand-diff": "code_comprehension",
        "understand-domain": "code_comprehension",
        "understand-explain": "code_comprehension",
        "understand-figma": "code_comprehension",
        "understand-knowledge": "code_comprehension",
        "understand-onboard": "code_comprehension",
        "web-design-guidelines": "ui_ux_design",
        "playwright-cli": "browser_testing",
        "autoae": "video_motion",
    }

    AUTHOR_MAP = {
        "ui-ux-pro-max": "nextlevelbuilder",
        "design": "nextlevelbuilder",
        "design-system": "nextlevelbuilder",
        "ui-styling": "nextlevelbuilder",
        "brand": "nextlevelbuilder",
        "banner-design": "nextlevelbuilder",
        "impeccable": "pbakaus",
        "design-taste-frontend": "Leonxlnx",
        "high-end-visual-design": "Leonxlnx",
        "minimalist-ui": "Leonxlnx",
        "redesign-existing-projects": "Leonxlnx",
        "gpt-taste": "Leonxlnx",
        "stitch-design-taste": "Leonxlnx",
        "industrial-brutalist-ui": "Leonxlnx",
        "humanizer": "blader",
        "stop-slop": "hardikpandya",
        "understand": "Egonex-AI",
        "understand-chat": "Egonex-AI",
        "understand-dashboard": "Egonex-AI",
        "understand-diff": "Egonex-AI",
        "understand-domain": "Egonex-AI",
        "understand-explain": "Egonex-AI",
        "understand-figma": "Egonex-AI",
        "understand-knowledge": "Egonex-AI",
        "understand-onboard": "Egonex-AI",
        "frontend-slides": "zarazhangrui",
        "diagram-design": "cathrynlavery",
        "web-design-guidelines": "vercel",
        "autoae": "autoae-team",
        "playwright-cli": "microsoft",
    }

    def __init__(self, global_path: Optional[str] = None):
        if global_path:
            self.global_dir = Path(global_path)
        else:
            self.global_dir = self.GLOBAL_SKILLS_PATH

    def _extract_skill_description(self, skill_path: Path) -> str:
        """Extracts first heading or description from SKILL.md or README.md."""
        candidates = [skill_path / "SKILL.md", skill_path / "README.md"]
        for cand in candidates:
            if cand.is_file():
                try:
                    text = cand.read_text(encoding="utf-8", errors="ignore")
                    # Try frontmatter description
                    desc_match = re.search(r"^description:\s*['\"]?(.*?)['\"]?$", text, re.MULTILINE | re.IGNORECASE)
                    if desc_match and desc_match.group(1).strip():
                        return desc_match.group(1).strip()
                    # Try first non-header paragraph
                    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
                    if lines:
                        return lines[0][:160]
                except Exception:
                    pass
        return "Universal design/UI/academic skill."

    def list_universal_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists universally available skills without downloading duplicates."""
        skills = []
        if not self.global_dir.exists():
            return skills

        try:
            for item in sorted(self.global_dir.iterdir()):
                if not item.is_dir() and not item.is_symlink():
                    continue

                name = item.name
                assigned_category = self.CATEGORY_MAP.get(name, "other_utility")
                author = self.AUTHOR_MAP.get(name, "community")

                if category and assigned_category != category:
                    continue

                desc = self._extract_skill_description(item)

                skills.append({
                    "name": name,
                    "author": author,
                    "category": assigned_category,
                    "description": desc,
                    "path": str(item.resolve()),
                    "has_skill_md": (item / "SKILL.md").exists(),
                    "has_readme": (item / "README.md").exists(),
                    "is_symlink": item.is_symlink(),
                })
        except Exception:
            pass

        return skills

    def get_skill_details(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves documentation and content for a specific skill."""
        skill_dir = self.global_dir / skill_name
        if not skill_dir.exists():
            return None

        content = ""
        doc_path = skill_dir / "SKILL.md"
        if not doc_path.exists():
            doc_path = skill_dir / "README.md"

        if doc_path.exists():
            try:
                content = doc_path.read_text(encoding="utf-8", errors="ignore")
            except Exception as exc:
                content = f"Error reading skill doc: {exc}"

        return {
            "name": skill_name,
            "category": self.CATEGORY_MAP.get(skill_name, "other_utility"),
            "author": self.AUTHOR_MAP.get(skill_name, "community"),
            "path": str(skill_dir.resolve()),
            "content": content,
        }

    def get_summary(self) -> Dict[str, Any]:
        """Returns statistics on universally available skills."""
        all_skills = self.list_universal_skills()
        by_category: Dict[str, int] = {}
        for s in all_skills:
            cat = s["category"]
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_skills_installed": len(all_skills),
            "global_path": str(self.global_dir),
            "zero_storage_duplication": True,
            "categories": by_category,
            "highlighted_curations": {
                "ui_ux_pro_max": sum(1 for s in all_skills if s["author"] == "nextlevelbuilder"),
                "taste_skill": sum(1 for s in all_skills if s["author"] == "Leonxlnx"),
                "understand_anything": sum(1 for s in all_skills if s["author"] == "Egonex-AI"),
                "academic_voice": sum(1 for s in all_skills if s["category"] == "academic_voice"),
                "presentations": sum(1 for s in all_skills if s["category"] == "presentation"),
                "diagrams": sum(1 for s in all_skills if s["category"] == "diagrams"),
            },
        }
