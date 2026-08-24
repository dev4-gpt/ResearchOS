import sys, os
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md')
body = doc.get('content', '')
title = 'Autonomous Code Synthesis and Self-Healing Multi-Agent Systems'
authors = ['Aryaman Singh Dev']
abstract = 'Executive Abstract'

for venue in ['IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM']:
    tex = exp.markdown_to_venue_latex(venue, title, authors, abstract, body)
    
    # Check for \begin{\equation} or \b\
    assert '\\begin{\\equation}' not in tex, f'Found \\begin{{\\equation}} in {venue}'
    assert '\\b\\begin' not in tex, f'Found \\b\\begin in {venue}'
    assert '\\b\\black' not in tex, f'Found \\b\\black in {venue}'
    
    pdf = exp.compile_pdflatex(tex, allow_package_fallback=True)
    assert pdf is not None and len(pdf) > 10000, f'PDF compilation failed for {venue}'
    print(f'[PASS] {venue}: compiled successfully ({len(pdf):,} bytes)')

print('ALL VENUE COMPILATIONS TESTED AND 100% SUCCESSFUL!')
