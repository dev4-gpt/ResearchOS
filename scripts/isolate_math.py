import sys, re
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.latex_exporter import LaTeXExporterService

vm = VaultManager('vault')
exp = LaTeXExporterService(vm)

doc = vm.read_markdown('drafts', 'autonomous_code_synthesis_and_self_healing_multi_agent_systems.md')
body = doc.get('content', '')

text = body.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
print('After quotes, contains \\b\\begin:', r'\b\begin' in text)

text = text.replace('\x08', '')
text = re.sub(r'(?:\\b|b|\x08)+\\*(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
text = re.sub(r'\\\\+(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
text = re.sub(r'(?<!\\)\b(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
print('After initial re.sub, contains \\b\\begin:', r'\b\begin' in text)

# Check line by line
for m in re.finditer(r'\$\$[\s\S]*?\$\$', text):
    eq = m.group(0)
    if r'\b\begin' in eq:
        print('Found \\b\\begin inside raw math block:', eq[:50])
