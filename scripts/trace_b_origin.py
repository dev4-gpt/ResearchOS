import sys, re
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md')
body = doc.get('content', '')

print('1. Markdown contains \\b\\:', r'\b\\' in body)

# Test _markdown_to_latex_body
cleaned = exp._markdown_to_latex_body(body)
print('2. Cleaned latex body contains \\b\\:', r'\b\\' in cleaned)

# Test latex_to_venue
tex = exp.markdown_to_venue_latex('IEEEtran', 'Title', ['Author'], 'Abstract', body)
print('3. Venue latex contains \\b\\:', r'\b\\' in tex)

for i, line in enumerate(tex.split('\n'), 1):
    if r'\b\\' in line or r'\b\begin' in line or r'\b\black' in line:
        print(f'   Line {i}: {line[:80]}')
