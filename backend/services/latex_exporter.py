import re
import os
from typing import Dict, Any, List

class LaTeXExporterService:
    def __init__(self, vault_manager: Any = None):
        self.vault_manager = vault_manager

    def markdown_to_ieeetran(self, title: str, authors: List[str], abstract: str, body_markdown: str, bib_entries: List[Dict[str, str]] = None) -> str:
        """Converts Markdown text into a formal IEEEtran two-column LaTeX document."""
        
        # Clean latex special characters in text blocks
        def sanitize_latex(text: str) -> str:
            # Preserve math blocks $$...$$ and $...$
            parts = re.split(r'(\$\$[\s\S]*?\$\$|\$.*?\$)', text)
            for i in range(0, len(parts), 2):
                parts[i] = parts[i].replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('_', '\\_')
            return "".join(parts)

        # Convert markdown headers to LaTeX section commands
        latex_body = body_markdown
        latex_body = re.sub(r'^# (.*?)$', r'\\section{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^## (.*?)$', r'\\section{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^### (.*?)$', r'\\subsection{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^#### (.*?)$', r'\\subsubsection{\1}', latex_body, flags=re.MULTILINE)

        # Convert Wikilinks [[paper_id]] to \cite{paper_id}
        latex_body = re.sub(r'\[\[([^\]]+)\]\]', r'\\cite{\1}', latex_body)

        # Convert markdown bold/italics
        latex_body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', latex_body)
        latex_body = re.sub(r'\*(.*?)\*', r'\\textit{\1}', latex_body)

        # Format authors string
        authors_str = " \\and ".join([f"\\IEEEauthorblockN{{{a}}}" for a in (authors or ["ResearchingOS Council"])])

        tex_document = f"""\\documentclass[10pt,journal,compsoc,twocolumn]{{IEEEtran}}
\\usepackage{{cite}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{algorithmic}}
\\usepackage{{graphicx}}
\\usepackage{{textcomp}}
\\usepackage{{xcolor}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}

\\begin{{document}}

\\title{{{sanitize_latex(title)}}}

\\author{{
{authors_str}
\\IEEEauthorblockA{{\\\\ResearchingOS Multi-Agent Academic Council\\\\
Email: research@researchingos.org}}
}}

\\maketitle

\\begin{{abstract}}
{sanitize_latex(abstract)}
\\end{{abstract}}

\\begin{{IEEEkeywords}}
Generative AI, Enterprise Workflows, Empirical ROI, Multi-Agent Systems, Jagged Technological Frontier, Systematic Review.
\\end{{IEEEkeywords}}

{latex_body}

\\bibliographystyle{{IEEEtran}}
\\bibliography{{references}}

\\end{{document}}
"""
        return tex_document

    def generate_bibtex(self, papers: List[Dict[str, Any]]) -> str:
        """Generates a complete BibTeX references file from ingested vault papers."""
        bib_lines = []
        for p in papers:
            paper_id = p.get("filename", "").replace(".md", "").replace(":", "_").replace(".", "_")
            title = p.get("frontmatter", {}).get("title", "Untitled Paper")
            authors_list = p.get("frontmatter", {}).get("authors", ["Unknown Author"])
            if isinstance(authors_list, str):
                authors_list = [authors_list]
            authors = " and ".join(authors_list)
            url = p.get("frontmatter", {}).get("url", "")
            year = p.get("frontmatter", {}).get("published", "2024")[:4]

            entry = f"""@article{{{paper_id},
  title={{{title}}},
  author={{{authors}}},
  journal={{Academic Research Repository}},
  year={{{year}}},
  url={{{url}}}
}}
"""
            bib_lines.append(entry)
        return "\n".join(bib_lines)
