from typing import Dict, Any, List

class O1AEvidenceTrackerService:
    """Evidence archive for O-1A work; never a legal eligibility determiner.

    O-1A and EB-1A are tracked as separate profiles. Evidence is recorded only
    when supported by external documentation; publication fact-check scores and
    automated peer review do not prove immigration criteria.
    """

    CRITERIA_MAPPING = {
        "scholarly_articles": {
            "basis": "O-1A USCIS Policy Manual, Volume 2, Part M, Chapter 4",
            "title": "Authorship of Scholarly Articles in Field",
            "description": "Evidence of the alien's authorship of scholarly articles in the field, in professional or major trade publications or other major media.",
            "target_venues": ["NeurIPS", "ICML", "CVPR", "ACL", "IEEEtran", "ACM"]
        },
        "original_contributions": {
            "basis": "O-1A USCIS Policy Manual, Volume 2, Part M, Chapter 4",
            "title": "Original Scientific or Scholarly Contributions of Major Significance",
            "description": "Evidence of the alien's original scientific, scholarly, or business-related contributions of major significance in the field.",
            "target_venues": ["NeurIPS", "ICML", "CVPR", "IEEEtran"]
        },
        "judging_work_of_others": {
            "basis": "O-1A USCIS Policy Manual, Volume 2, Part M, Chapter 4",
            "title": "Participation as a Judge of the Work of Others",
            "description": "Evidence of the alien's participation, either individually or on a panel, as a judge of the work of others in the same or an allied field.",
            "target_venues": ["ACL", "NeurIPS", "ICML", "ARR"]
        },
        "published_media": {
            "basis": "O-1A USCIS Policy Manual, Volume 2, Part M, Chapter 4",
            "title": "Published Material About the Alien in Professional or Major Media",
            "description": "Evidence of published material about the alien in professional or major trade publications or other major media.",
            "target_venues": ["CVPR", "Hugging Face Spaces", "TechCrunch", "VentureBeat"]
        }
    }

    def __init__(self, vault_manager: Any = None):
        self.vault_manager = vault_manager

    def audit_o1a_readiness(self, manuscripts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Reports documented portfolio evidence without making an eligibility finding."""
        total_papers = len(manuscripts)
        total_citations = sum(p.get("citations", 0) for p in manuscripts)

        criteria_status = {
            "scholarly_articles": {
                "met": False,
                "evidence_count": total_papers,
                "details": [f"Manuscript: '{p.get('title')}' ({p.get('venue', 'IEEE/ACM')})" for p in manuscripts]
            },
            "original_contributions": {
                "met": False,
                "evidence_count": sum(1 for p in manuscripts if p.get("original_contribution_evidence")),
                "details": ["Attach independent evidence of contribution significance; manuscript QA alone is not sufficient."]
            },
            "judging_work_of_others": {
                "met": False,
                "evidence_count": sum(1 for p in manuscripts if p.get("judging_evidence")),
                "details": ["Attach invitations, completed reviews, and organizer confirmation where applicable."]
            },
            "published_media": {
                "met": False,
                "evidence_count": sum(1 for p in manuscripts if p.get("published_media_evidence")),
                "details": ["Attach independent published-material evidence; citation counts alone do not establish this category."]
            }
        }

        met_count = sum(1 for c in criteria_status.values() if c["met"])
        readiness_percentage = round((met_count / 4.0) * 100, 1)

        return {
            "total_manuscripts": total_papers,
            "total_citations": total_citations,
            "met_criteria_count": met_count,
            "required_criteria_count": 3,
            "o1a_eligible": False,
            "readiness_percentage": readiness_percentage,
            "criteria_breakdown": criteria_status,
            "legal_recommendation": "Evidence inventory only; a qualified immigration attorney must assess O-1A eligibility and totality of evidence.",
            "profile": "O-1A",
            "not_a_legal_determination": True,
        }

    def generate_legal_dossier_markdown(self, manuscripts: List[Dict[str, Any]]) -> str:
        """Generates an O-1A evidence inventory, not a legal petition or eligibility finding."""
        audit = self.audit_o1a_readiness(manuscripts)

        md_lines = [
            "# O-1A Evidence Inventory",
            "**Petitioner**: Not configured",
            "**Field**: Not configured",
            "**Institution**: Not configured",
            f"**Overall Readiness**: {audit['readiness_percentage']}% ({audit['legal_recommendation']})",
            "",
            "---",
            "",
            "## 1. O-1A Evidence Categories",
            ""
        ]

        for key, info in self.CRITERIA_MAPPING.items():
            st = audit["criteria_breakdown"][key]
            status_symbol = "✅ MET" if st["met"] else "❌ PENDING"
            md_lines.append(f"### {info['title']} ({info['basis']}) — {status_symbol}")
            md_lines.append(f"*{info['description']}*")
            md_lines.append(f"- **Evidence Count**: {st['evidence_count']}")
            for d in st["details"]:
                md_lines.append(f"  - {d}")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("## 2. Documented Publications and External Evidence")
        md_lines.append("")

        for idx, p in enumerate(manuscripts, 1):
            md_lines.append(f"### Article {idx}: {p.get('title')}")
            md_lines.append(f"- **Venue**: {p.get('venue', 'IEEE/ACM Journal')}")
            md_lines.append(f"- **Acceptance/Publication Evidence**: {p.get('publication_evidence', 'Not documented')}")
            md_lines.append(f"- **Verification Evidence**: {p.get('fact_check_score', 'Not established')}")
            md_lines.append(f"- **Citation Anchor**: `[[{p.get('id', 'manuscript')}]]`")
            md_lines.append("")

        return "\n".join(md_lines)
