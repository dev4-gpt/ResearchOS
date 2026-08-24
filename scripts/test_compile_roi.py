import sys, os
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'review_enterprise_genai_roi.md')
body = doc.get('content', '')
title = 'Systematic Review & Meta-Taxonomy of Generative AI in Enterprise Workflows'
authors = ['Aryaman Singh Dev']
abstract = 'Executive Abstract'

for venue in ['IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM', 'IEEE_Access', 'SpringerOpen', 'Femington', 'MDPI', 'arXiv', 'DOAJ']:
    tex = exp.markdown_to_venue_latex(venue, title, authors, abstract, body)
    
    # Check for \begin{\equation} or \b\
    assert '\\begin{\\equation}' not in tex, f'Found \\begin{{\\equation}} in {venue}'
    assert '\\b\\begin' not in tex, f'Found \\b\\begin in {venue}'
    assert '\\b\\black' not in tex, f'Found \\b\\black in {venue}'
    assert 'use \\cases' not in tex, f'Found use \\cases in {venue}'
    assert '\\aligned.' not in tex, f'Found \\aligned. in {venue}'
    
    pdf = exp.compile_pdflatex(tex, allow_package_fallback=True)
    assert pdf is not None and len(pdf) > 10000, f'PDF compilation failed for {venue}'
    print(f'[PASS] {venue}: compiled successfully ({len(pdf):,} bytes)')

print('ALL 12 VENUE COMPILATIONS TESTED AND 100% SUCCESSFUL FOR ROI PAPER!')
