import re
from typing import Dict, Any, List

class CitationGraphEngine:
    """Graph-based citation traversal and contradiction detection engine across paper vault metadata."""

    def __init__(self, vault_manager: Any = None):
        self.vault_manager = vault_manager

    def build_citation_graph(self, papers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds citation network nodes, edges, and mines empirical contradictions across papers."""
        nodes = []
        edges = []
        contradictions = []

        paper_map = {}
        for p in papers_data:
            meta = p.get("frontmatter", {}) or p.get("metadata", {})
            filename = p.get("filename", "")
            clean_id = filename.replace(".md", "").replace(":", "_").replace(".", "_")
            title = meta.get("title", filename)
            authors = meta.get("authors", ["Unknown Author"])
            year = meta.get("published", "2024")[:4]

            node = {
                "id": clean_id,
                "filename": filename,
                "title": title,
                "authors": authors,
                "year": year,
                "citations_count": 0,
                "sample_size": meta.get("sample_size"),
                "has_compute_baseline": meta.get("has_compute_baseline", False)
            }
            nodes.append(node)
            paper_map[clean_id] = node

        # Traversal for wikilinks and citations in content
        for p in papers_data:
            filename = p.get("filename", "")
            source_id = filename.replace(".md", "").replace(":", "_").replace(".", "_")
            content = p.get("content", "")

            # Find all [[paper_id]] citations
            citations = re.findall(r'\[\[([^\]]+)\]\]', content)
            for c in citations:
                target_id = c.replace(".md", "").replace(":", "_").replace(".", "_")
                if target_id in paper_map:
                    edges.append({
                        "source": source_id,
                        "target": target_id,
                        "type": "cites"
                    })
                    paper_map[target_id]["citations_count"] += 1

            # Contradiction Detection Rules
            # 1. Low sample size hazard (N < 30)
            sample_size = p.get("frontmatter", {}).get("sample_size") or p.get("metadata", {}).get("sample_size")
            if sample_size and isinstance(sample_size, int) and sample_size < 30:
                contradictions.append({
                    "paper_id": source_id,
                    "title": paper_map[source_id]["title"],
                    "type": "Low-Power Validation Deficit",
                    "severity": "HIGH",
                    "details": f"Clinical validation panel sample size N={sample_size} is underpowered (<30). Subject to high variance."
                })

            # 2. Compute-equivalent baseline deficit
            if "Self-Consistency" in content and "greedy baseline" in content and "compute-equivalent" not in content.lower():
                contradictions.append({
                    "paper_id": source_id,
                    "title": paper_map[source_id]["title"],
                    "type": "Unmetered Compute Scaling Deficit",
                    "severity": "HIGH",
                    "details": "Multi-path decoding accuracy gains are compared against single-path greedy baselines without equal token/FLOP budgets."
                })

            # 3. LLM-as-a-Judge circularity hazard
            if "LLM-as-a-Judge" in content or "GPT-4 Judge" in content:
                if "Fleiss" not in content and "Cohen" not in content and "Kappa" not in content:
                    contradictions.append({
                        "paper_id": source_id,
                        "title": paper_map[source_id]["title"],
                        "type": "Epistemological Circularity & Bias Risk",
                        "severity": "MEDIUM",
                        "details": "Automated LLM evaluator deployed without psychometric inter-rater agreement calibration (Fleiss/Cohen Kappa)."
                    })

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges,
            "contradictions": contradictions
        }
