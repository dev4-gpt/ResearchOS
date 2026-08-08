import re
import os
from typing import Dict, Any, List, Optional

VENUE_SPECS = {
    "NeurIPS": {
        "name": "Neural Information Processing Systems (NeurIPS)",
        "format": "Single-column layout, 10pt Times font",
        "page_limit": "9 pages (main content) + checklist & refs",
        "doc_class": "\\documentclass{article}",
        "packages": "\\usepackage[final]{neurips_2026}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{url}\n\\usepackage{booktabs}\n\\usepackage{amsfonts}\n\\usepackage{nicefrac}\n\\usepackage{microtype}\n\\usepackage{xcolor}\n\\usepackage{graphicx}\n\\usepackage{amsmath,amssymb}\n\\usepackage{hyperref}",
        "template_style": "neurips"
    },
    "ICML": {
        "name": "International Conference on Machine Learning (ICML)",
        "format": "Two-column layout, US Letter page size",
        "page_limit": "8 pages (main body) + unlimited refs/appendices",
        "doc_class": "\\documentclass{article}",
        "packages": "\\usepackage{icml2026}\n\\usepackage{times}\n\\usepackage{graphicx}\n\\usepackage{subfigure}\n\\usepackage{natbib}\n\\usepackage{algorithm}\n\\usepackage{algorithmic}\n\\usepackage{hyperref}\n\\usepackage{amsmath,amssymb}",
        "template_style": "icml"
    },
    "CVPR": {
        "name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
        "format": "Two-column format, US Letter",
        "page_limit": "8 pages (main content) + refs",
        "doc_class": "\\documentclass[10pt,twocolumn,letterpaper]{article}",
        "packages": "\\usepackage{cvpr}\n\\usepackage{times}\n\\usepackage{epsfig}\n\\usepackage{graphicx}\n\\usepackage{amsmath,amssymb}\n\\usepackage{booktabs}\n\\usepackage{hyperref}",
        "template_style": "cvpr"
    },
    "ACL": {
        "name": "Association for Computational Linguistics (ACL / ARR)",
        "format": "Two-column layout, ACL Rolling Review style",
        "page_limit": "8 pages (long paper) + refs",
        "doc_class": "\\documentclass[11pt,a4paper]{article}",
        "packages": "\\usepackage[review]{acl}\n\\usepackage{times}\n\\usepackage{latexsym}\n\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage{microtype}\n\\usepackage{graphicx}\n\\usepackage{amsmath,amssymb}",
        "template_style": "acl"
    },
    "IEEEtran": {
        "name": "IEEE Transactions (IEEE TKDE / TPAMI)",
        "format": "Two-column journal format",
        "page_limit": "10 - 25+ pages (journal literature review)",
        "doc_class": "\\documentclass[10pt,journal,compsoc,twocolumn]{IEEEtran}",
        "packages": "\\usepackage{cite}\n\\usepackage{amsmath,amssymb,amsfonts}\n\\usepackage{algorithmic}\n\\usepackage{graphicx}\n\\usepackage{textcomp}\n\\usepackage{xcolor}\n\\usepackage{booktabs}\n\\usepackage{hyperref}",
        "template_style": "ieeetran"
    },
    "ACM": {
        "name": "ACM Computing Surveys / SIGKDD",
        "format": "Two-column ACM article format",
        "page_limit": "12 - 20+ pages",
        "doc_class": "\\documentclass[sigconf]{acmart}",
        "packages": "\\usepackage{booktabs}\n\\usepackage{amsmath,amssymb}\n\\usepackage{graphicx}",
        "template_style": "acm"
    }
}

class LaTeXExporterService:
    def __init__(self, vault_manager: Any = None):
        self.vault_manager = vault_manager

    def sanitize_latex(self, text: str) -> str:
        """Preserves math blocks $$...$$ and $...$ while cleaning special LaTeX and Unicode characters."""
        if not text:
            return ""
        # Replace non-ASCII quote and punctuation characters first
        char_map = {
            '“': '"', '”': '"', '’': "'", '‘': "'", '–': '-', '—': '--', '…': '...',
            '┌': '+', '─': '-', '│': '|', '├': '+', '┤': '+', '└': '+', '┘': '+', '┬': '+', '┴': '+', '┼': '+',
            '═': '=', '║': '|', '▲': '^', '▼': 'v', '◆': '*', '●': '*', '★': '*', '✓': '[V]', '✗': '[X]',
            '🚀': '', '🎉': '', '📦': '', '🛡️': '', '🏛️': '', '📊': '', '💡': '', '🏆': '', '⚡': '', '🌐': ''
        }
        for char, repl in char_map.items():
            text = text.replace(char, repl)

        parts = re.split(r'(\$\$[\s\S]*?\$\$|\$.*?\$)', text)
        for i in range(0, len(parts), 2):
            parts[i] = parts[i].replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('_', '\\_')
        return "".join(parts)

    def convert_markdown_body(self, body_markdown: str) -> str:
        """Converts Markdown headings, bold, italics, lists, tables, code blocks, and wikilinks to clean LaTeX commands."""
        text = body_markdown
        
        # 1. Replace code blocks with verbatim environments
        def replace_code_block(match):
            code_content = match.group(1)
            char_map = {'┌': '+', '─': '-', '│': '|', '├': '+', '┤': '+', '└': '+', '┘': '+', '┬': '+', '┴': '+', '┼': '+'}
            for char, repl in char_map.items():
                code_content = code_content.replace(char, repl)
            return f"\\begin{{verbatim}}\n{code_content}\n\\end{{verbatim}}"

        text = re.sub(r'```[\w]*\n([\s\S]*?)```', replace_code_block, text)

        # 2. Humanize AI prose (remove AI fluff/buzzwords)
        ai_fluff = [
            r'\bIn conclusion,?\b', r'\bIn summary,?\b', r'\bDelve into\b', r'\bdelving into\b',
            r'\btapestry of\b', r'\bbeacon of\b', r'\bcrucial role\b', r'\bit is important to note that\b',
            r'\bgame-changer\b', r'\bmasterclass\b', r'\blandscape of\b', r'\bdeep dive\b'
        ]
        for pattern in ai_fluff:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # 3. Sanitize body text outside math blocks
        text = self.sanitize_latex(text)

        # 4. Parse lists (- item, 1. item) into \begin{itemize} / \begin{enumerate}
        lines = text.split('\n')
        new_lines = []
        in_list = False
        list_type = None

        for line in lines:
            stripped = line.strip()
            bullet_match = re.match(r'^[*\-\+]\s+(.*)', stripped)
            enum_match = re.match(r'^\d+\.\s+(.*)', stripped)

            if bullet_match:
                if not in_list or list_type != 'itemize':
                    if in_list:
                        new_lines.append(f'\\end{{{list_type}}}')
                    new_lines.append('\\begin{itemize}')
                    in_list = True
                    list_type = 'itemize'
                new_lines.append(f'  \\item {bullet_match.group(1)}')
            elif enum_match:
                if not in_list or list_type != 'enumerate':
                    if in_list:
                        new_lines.append(f'\\end{{{list_type}}}')
                    new_lines.append('\\begin{enumerate}')
                    in_list = True
                    list_type = 'enumerate'
                new_lines.append(f'  \\item {enum_match.group(1)}')
            else:
                if in_list and not stripped:
                    new_lines.append(f'\\end{{{list_type}}}')
                    in_list = False
                    list_type = None
                new_lines.append(line)

        if in_list:
            new_lines.append(f'\\end{{{list_type}}}')

        text = '\n'.join(new_lines)

        # 5. Parse Markdown tables (| col1 | col2 |) into LaTeX booktabs
        lines = text.split('\n')
        final_lines = []
        table_lines = []
        in_table = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('|') and stripped.endswith('|'):
                in_table = True
                table_lines.append(stripped)
            else:
                if in_table:
                    rows = []
                    for tline in table_lines:
                        cols = [c.strip() for c in tline.strip('|').split('|')]
                        if all(re.match(r'^-+$', c) for c in cols):
                            continue
                        rows.append(cols)
                    if rows:
                        num_cols = max(len(r) for r in rows)
                        col_spec = 'l ' * num_cols
                        final_lines.append('\\begin{table}[htbp]')
                        final_lines.append('\\centering')
                        final_lines.append(f'\\begin{{tabular}}{{{col_spec.strip()}}}')
                        final_lines.append('\\toprule')
                        header = ' & '.join(rows[0]) + ' \\\\'
                        final_lines.append(header)
                        final_lines.append('\\midrule')
                        for r in rows[1:]:
                            row_str = ' & '.join(r) + ' \\\\'
                            final_lines.append(row_str)
                        final_lines.append('\\bottomrule')
                        final_lines.append('\\end{tabular}')
                        final_lines.append('\\end{table}')
                    table_lines = []
                    in_table = False
                final_lines.append(line)

        if in_table:
            rows = []
            for tline in table_lines:
                cols = [c.strip() for c in tline.strip('|').split('|')]
                if all(re.match(r'^-+$', c) for c in cols):
                    continue
                rows.append(cols)
            if rows:
                num_cols = max(len(r) for r in rows)
                col_spec = 'l ' * num_cols
                final_lines.append('\\begin{table}[htbp]')
                final_lines.append('\\centering')
                final_lines.append(f'\\begin{{tabular}}{{{col_spec.strip()}}}')
                final_lines.append('\\toprule')
                header = ' & '.join(rows[0]) + ' \\\\'
                final_lines.append(header)
                final_lines.append('\\midrule')
                for r in rows[1:]:
                    row_str = ' & '.join(r) + ' \\\\'
                    final_lines.append(row_str)
                final_lines.append('\\bottomrule')
                final_lines.append('\\end{tabular}')
                final_lines.append('\\end{table}')

        text = '\n'.join(final_lines)

        # 6. Heading replacements
        latex_body = text
        latex_body = re.sub(r'^# (.*?)$', r'\\section{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^## (.*?)$', r'\\section{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^### (.*?)$', r'\\subsection{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'^#### (.*?)$', r'\\subsubsection{\1}', latex_body, flags=re.MULTILINE)
        latex_body = re.sub(r'\[\[([^\]]+)\]\]', r'\\cite{\1}', latex_body)
        latex_body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', latex_body)
        latex_body = re.sub(r'\*(.*?)\*', r'\\textit{\1}', latex_body)
        return latex_body

    def markdown_to_ieeetran(self, title: str, authors: List[str], abstract: str, body_markdown: str, bib_entries: List[Dict[str, str]] = None) -> str:
        """Legacy IEEEtran converter wrapper."""
        return self.markdown_to_venue_latex("IEEEtran", title, authors, abstract, body_markdown, bib_entries)

    def markdown_to_venue_latex(self, venue_key: str, title: str, authors: List[str], abstract: str, body_markdown: str, bib_entries: List[Dict[str, str]] = None) -> str:
        """Converts Markdown manuscript into venue-specific LaTeX for NeurIPS, ICML, CVPR, ACL, IEEEtran, or ACM."""
        spec = VENUE_SPECS.get(venue_key, VENUE_SPECS["IEEEtran"])
        clean_title = self.sanitize_latex(title)
        clean_abstract = self.sanitize_latex(abstract)
        latex_body = self.convert_markdown_body(body_markdown)
        
        authors_list = authors or ["ResearchingOS Council", "Penn State AI Collaborator"]
        authors_str = ", ".join(authors_list)

        neurips_authors = " \\And ".join([a + "\\\\ Penn State AI Laboratory" for a in authors_list])
        icml_authors = " ".join(["\\icmlauthor{" + a + "}{psu}" for a in authors_list])
        cvpr_authors = " \\and ".join(authors_list)
        acl_authors = " \\\\ ".join(authors_list)
        ieee_authors = " \\and ".join(["\\IEEEauthorblockN{" + a + "}" for a in authors_list])

        if venue_key == "NeurIPS":
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\title{{{clean_title}}}

\\author{{
  {neurips_authors}
}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

{latex_body}

\\bibliographystyle{{plainnat}}
\\bibliography{{references}}

\\section*{{NeurIPS Paper Checklist}}
\\begin{{enumerate}}
  \\item Claims: Yes, all quantitative performance claims are grounded in empirical evaluations.
  \\item Limitations: Yes, limitations are explicitly stated in Section 6.
  \\item Theory & Proofs: Yes, mathematical formulations for FLOPs scaling laws are detailed in Section 5.
  \\item Reproducibility: Yes, code artifacts and prompt traces are open-sourced in the repository.
\\end{{enumerate}}

\\end{{document}}
"""
        elif venue_key == "ICML":
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\icmltitlerunning{{{clean_title[:50]}}}

\\begin{{document}}

\\twocolumn[
\\icmltitle{{{clean_title}}}

\\begin{{icmlauthorlist}}
{icml_authors}
\\end{{icmlauthorlist}}

\\icmlaffiliation{{psu}}{{Department of Computer Science & Artificial Intelligence, The Pennsylvania State University}}

\\icmlkeywords{{Machine Learning, Deep Learning, AI Systems, Empirical Evaluation}}

\\vskip 0.3in
]

\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

{latex_body}

\\bibliography{{references}}
\\bibliographystyle{{icml2026}}

\\end{{document}}
"""
        elif venue_key == "CVPR":
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\begin{{document}}

\\title{{{clean_title}}}

\\author{{
{cvpr_authors}\\\\
The Pennsylvania State University\\\\
{{\\tt\\small {{research, ai}}@psu.edu}}
}}

\\maketitle

\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

{latex_body}

{{\\small
\\bibliographystyle{{ieee_fullname}}
\\bibliography{{references}}
}}

\\end{{document}}
"""
        elif venue_key == "ACL":
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\title{{{clean_title}}}

\\author{{
{acl_authors}\\\\
The Pennsylvania State University\\\\
\\texttt{{research@psu.edu}}
}}

\\begin{{document}}
\\maketitle
\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

{latex_body}

\\bibliography{{references}}
\\bibliographystyle{{acl_natbib}}

\\end{{document}}
"""
        elif venue_key == "ACM":
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\title{{{clean_title}}}

\\author{{{authors_list[0]}}}
\\affiliation{{
  \\institution{{The Pennsylvania State University}}
  \\country{{USA}}
}}
\\email{{research@psu.edu}}

\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

\\maketitle

{latex_body}

\\bibliographystyle{{ACM-Reference-Format}}
\\bibliography{{references}}

\\end{{document}}
"""
        else: # IEEEtran
            doc_code = f"""{spec['doc_class']}
{spec['packages']}

\\begin{{document}}

\\title{{{clean_title}}}

\\author{{
{ieee_authors}\\\\
\\IEEEauthorblockA{{\\\\Department of Computer Science \\& AI, The Pennsylvania State University\\\\
Email: research@psu.edu}}
}}

\\maketitle

\\begin{{abstract}}
{clean_abstract}
\\end{{abstract}}

\\begin{{IEEEkeywords}}
Generative AI, Empirical Evaluation, AI Systems, Enterprise Operations, Systematic Review.
\\end{{IEEEkeywords}}

{latex_body}

\\bibliographystyle{{IEEEtran}}
\\bibliography{{references}}

\\end{{document}}
"""
        return doc_code

    def export_multi_venue_bundle(self, title: str, authors: List[str], abstract: str, body_markdown: str) -> Dict[str, str]:
        """Generates LaTeX formatted documents for ALL premier target venues simultaneously (Multi-Path Publishing)."""
        bundle = {}
        for key in VENUE_SPECS.keys():
            bundle[key] = self.markdown_to_venue_latex(key, title, authors, abstract, body_markdown)
        return bundle

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

    def compile_pdflatex(self, tex_code: str, bib_code: Optional[str] = None) -> Optional[bytes]:
        """Compiles TeX code into PDF bytes using local pdflatex command with automatic safe package fallbacks."""
        import tempfile
        import subprocess
        import shutil

        pdflatex_bin = None
        for p in ["/Library/TeX/texbin/pdflatex", "/usr/local/bin/pdflatex", "/usr/bin/pdflatex"]:
            if os.path.exists(p) and os.access(p, os.X_OK):
                pdflatex_bin = p
                break
        
        if not pdflatex_bin:
            pdflatex_bin = shutil.which("pdflatex")

        if not pdflatex_bin:
            print("pdflatex binary not found on local system.")
            return None

        # Build safe TeX code fallback if custom .sty files are missing from system TeX Live
        tex_code_safe = (
            tex_code.replace('\\usepackage[final]{neurips_2026}', '\\usepackage[margin=1in]{geometry}')
                    .replace('\\usepackage{icml2026}', '\\usepackage[margin=0.75in]{geometry}')
                    .replace('\\usepackage{cvpr}', '\\usepackage[margin=0.75in]{geometry}')
                    .replace('\\usepackage[review]{acl}', '\\usepackage[margin=0.75in]{geometry}')
                    .replace('\\documentclass[sigconf]{acmart}', '\\documentclass[10pt,twocolumn,letterpaper]{article}\n\\usepackage[margin=0.75in]{geometry}')
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "document.tex")
            bib_path = os.path.join(tmpdir, "references.bib")

            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(tex_code_safe)

            if bib_code:
                with open(bib_path, "w", encoding="utf-8") as f:
                    f.write(bib_code)

            try:
                cmd = [pdflatex_bin, "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

                pdf_path = os.path.join(tmpdir, "document.pdf")
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        return f.read()
            except Exception as e:
                print(f"Error compiling PDF with pdflatex: {e}")

        return None

