"""Publication Architecture Diagram Generator for ResearchingOS.

Implements guidelines from cathrynlavery/diagram-design:
- Generates clean, publication-grade SVG/HTML architecture diagrams and schematics.
- Supports system pipelines, multi-agent council graphs, and state machines.
- Outputs crisp vector SVG ready for inclusion in LaTeX manuscripts and web dashboards.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class DiagramGeneratorService:
    """Generates editorial SVG diagrams for academic manuscripts and system documentation."""

    def __init__(self, vault_path: Optional[str] = None):
        base = Path(vault_path or os.getenv("VAULT_PATH", "vault"))
        self.diagrams_dir = base / "00_System" / "diagrams"
        self.diagrams_dir.mkdir(parents=True, exist_ok=True)

    def generate_pipeline_diagram(
        self,
        title: str = "ResearchingOS Multi-Agent Autonomous Council Pipeline",
        nodes: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Generates an editorial SVG pipeline flowchart."""
        default_nodes = [
            {"id": "scout", "title": "Scout Agent", "desc": "12-Repo Ingestion & RRF", "color": "#38bdf8"},
            {"id": "analyst", "title": "Lead Analyst", "desc": "Paper Parsing & Vault Notes", "color": "#10b981"},
            {"id": "critic", "title": "Tri-Critic (EvoMap)", "desc": "Novelty, Feasibility, Falsifiability", "color": "#f59e0b"},
            {"id": "pilot", "title": "Pilot Gate", "desc": "Pre-Scaling Verification", "color": "#a855f7"},
            {"id": "writer", "title": "Senior Writer", "desc": "IEEE/ACM LaTeX Synthesis", "color": "#ec4899"},
            {"id": "checker", "title": "Checkmate Linter", "desc": "Zero-Hallucination Gate", "color": "#06b6d4"},
        ]
        active_nodes = nodes or default_nodes

        width = 1200
        height = 360
        node_width = 160
        node_height = 110
        spacing = (width - 80 - (len(active_nodes) * node_width)) // (len(active_nodes) - 1)

        svg_elements = []
        
        # Background canvas
        svg_elements.append(f'<rect width="{width}" height="{height}" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="1.5"/>')
        
        # Title
        svg_elements.append(f'<text x="40" y="42" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700">{title}</text>')
        svg_elements.append(f'<text x="40" y="66" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Verified Architecture Schematic • cathrynlavery/diagram-design</text>')

        y_pos = 140

        for idx, node in enumerate(active_nodes):
            x_pos = 40 + idx * (node_width + spacing)
            color = node.get("color", "#38bdf8")

            # Connecting arrow to next node
            if idx < len(active_nodes) - 1:
                next_x = x_pos + node_width
                arrow_end = next_x + spacing
                svg_elements.append(f'''
                    <line x1="{next_x}" y1="{y_pos + node_height // 2}" x2="{arrow_end - 8}" y2="{y_pos + node_height // 2}" stroke="#334155" stroke-width="2" stroke-dasharray="4,4"/>
                    <polygon points="{arrow_end - 2},{y_pos + node_height // 2} {arrow_end - 10},{y_pos + node_height // 2 - 5} {arrow_end - 10},{y_pos + node_height // 2 + 5}" fill="#64748b"/>
                ''')

            # Node card
            svg_elements.append(f'''
                <rect x="{x_pos}" y="{y_pos}" width="{node_width}" height="{node_height}" rx="8" fill="#111827" stroke="{color}" stroke-width="1.5" stroke-opacity="0.7"/>
                <circle cx="{x_pos + 20}" cy="{y_pos + 22}" r="5" fill="{color}"/>
                <text x="{x_pos + 32}" y="{y_pos + 26}" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700">{node["title"]}</text>
                <text x="{x_pos + 16}" y="{y_pos + 56}" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="11" width="{node_width - 32}">{node["desc"]}</text>
                <rect x="{x_pos + 16}" y="{y_pos + 82}" width="50" height="16" rx="4" fill="{color}" fill-opacity="0.15"/>
                <text x="{x_pos + 24}" y="{y_pos + 94}" fill="{color}" font-family="monospace" font-size="9" font-weight="600">STAGE {idx + 1}</text>
            ''')

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
            {chr(10).join(svg_elements)}
        </svg>'''

        safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", title.lower())[:40] + "_arch.svg"
        output_path = self.diagrams_dir / safe_name
        output_path.write_text(svg_content, encoding="utf-8")

        return {
            "title": title,
            "file_path": str(output_path),
            "relative_url": f"/vault/00_System/diagrams/{safe_name}",
            "svg": svg_content,
        }
