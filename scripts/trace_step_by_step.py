import sys, re
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md')
body = doc.get('content', '')

print('1. body has \\b\\:', r'\b\\' in body)

# Step 1: remove abstract and references
body_for_export = re.sub(r'#+\s*[\d\.\s]*(?:Executive\s+)?Abstract[^\n]*\n+[\s\S]*?(?=\n+#{1,2}\s+|\Z)', '', body, flags=re.IGNORECASE)
body_for_export = re.sub(r'#+\s*[\d\.\s]*References[^\n]*\n+[\s\S]*$', '', body_for_export, flags=re.IGNORECASE)
body_for_export = re.sub(r'^#\s+.*$', '', body_for_export, flags=re.MULTILINE)
print('2. body_for_export has \\b\\:', r'\b\\' in body_for_export)

# Step 2: convert_markdown_body
latex_body = exp.convert_markdown_body(body_for_export)
print('3. latex_body has \\b\\:', r'\b\\' in latex_body)

for i, line in enumerate(latex_body.split('\n'), 1):
    if r'\b\\' in line or r'\b\begin' in line or r'\b\black' in line or r'\b\cases' in line:
        print(f'   Line {i}: {line[:80]}')
