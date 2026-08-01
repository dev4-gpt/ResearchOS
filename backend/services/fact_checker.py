import re
from typing import List, Dict, Any, Optional

class FactCheckerService:
    def __init__(self, vault_manager: Optional[Any] = None):
        self.vault_manager = vault_manager

    def validate_citations(self, content: str) -> Dict[str, Any]:
        """Extracts and verifies all [[WikiLink]] citations against existing vault files."""
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        unique_links = sorted(list(set(wikilinks)))

        verified_links = []
        broken_links = []

        for link in unique_links:
            clean_link = link.split("|")[0].strip()
            # If link has extension, remove it
            if clean_link.endswith(".md"):
                clean_link = clean_link[:-3]

            found = False
            if self.vault_manager:
                # Check across all vault categories
                for category in ["papers", "concepts", "debates", "drafts"]:
                    files = self.vault_manager.list_files(category)
                    file_basenames = [f["filename"].replace(".md", "") for f in files]
                    if clean_link in file_basenames:
                        found = True
                        break

            if found or not self.vault_manager:
                verified_links.append(clean_link)
            else:
                broken_links.append(clean_link)

        citation_score = 100.0 if not unique_links else round((len(verified_links) / len(unique_links)) * 100, 1)

        return {
            "total_citations": len(unique_links),
            "verified_count": len(verified_links),
            "broken_count": len(broken_links),
            "verified_links": verified_links,
            "broken_links": broken_links,
            "citation_score": citation_score
        }

    def validate_numeric_claims(self, draft_content: str, source_texts: List[str]) -> Dict[str, Any]:
        """Extracts numeric statistics, percentages, and metrics from draft and verifies grounding."""
        # Regex to capture percentages, scientific notation, numbers with decimals, sample sizes
        pattern = r'(\b\d+(?:\.\d+)?%|\bN\s*=\s*\d+|\bp\s*<[=\s]*0\.\d+|\b\d+\.\d+\b|\b\d{4,}\b)'
        matches = re.findall(pattern, draft_content)
        unique_claims = sorted(list(set(matches)))

        combined_source = " ".join(source_texts).lower()

        grounded_claims = []
        unverified_claims = []

        for claim in unique_claims:
            claim_clean = claim.lower().strip()
            if claim_clean in combined_source:
                grounded_claims.append(claim)
            else:
                unverified_claims.append(claim)

        metric_score = 100.0 if not unique_claims else round((len(grounded_claims) / len(unique_claims)) * 100, 1)

        return {
            "total_numeric_claims": len(unique_claims),
            "grounded_count": len(grounded_claims),
            "unverified_count": len(unverified_claims),
            "grounded_claims": grounded_claims,
            "unverified_claims": unverified_claims,
            "metric_score": metric_score
        }

    def audit_document(self, content: str, source_texts: Optional[List[str]] = None) -> Dict[str, Any]:
        """Performs full fact-checking audit on a markdown document."""
        citation_report = self.validate_citations(content)
        metric_report = self.validate_numeric_claims(content, source_texts or [])

        # Composite Fact-Check Score (50% Citation Integrity, 50% Metric Grounding)
        composite_score = round((citation_report["citation_score"] + metric_report["metric_score"]) / 2.0, 1)

        return {
            "fact_check_score": composite_score,
            "citation_report": citation_report,
            "metric_report": metric_report,
            "status": "passed" if composite_score >= 80.0 else "needs_review",
            "verification_matrix": {
                "verified_citations": citation_report["verified_links"],
                "broken_citations": citation_report["broken_links"],
                "grounded_metrics": metric_report["grounded_claims"],
                "unverified_metrics": metric_report["unverified_claims"]
            }
        }
