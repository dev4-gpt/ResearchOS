import sys, re
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md')
body = doc.get('content', '')

# Step 1: Check body for any \b
for i, line in enumerate(body.split('\n'), 1):
    if '\\b\\' in line:
        print(f'Body line {i} has \\b\\: {repr(line)}')

# Step 2: Run convert_markdown_body
converted = exp.convert_markdown_body(body)
for i, line in enumerate(converted.split('\n'), 1):
    if '\\b\\' in line:
        print(f'Converted line {i} has \\b\\: {repr(line)}')

# Step 3: Run markdown_to_venue_latex
tex = exp.markdown_to_venue_latex('IEEEtran', 'Title', ['Author'], 'Abstract', body)
for i, line in enumerate(tex.split('\n'), 1):
    if '\\b\\' in line:
        print(f'Tex line {i} has \\b\\: {repr(line)}')

print('Trace complete.')
