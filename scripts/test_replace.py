import os

fpath = 'vault/04_Drafts/autonomous_code_synthesis_and_self_healing_multi_agent_systems.md'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()

target = '\\b\\begin'
print(f'Count of {repr(target)}: {text.count(target)}')

text = text.replace(target, '\\begin')
print(f'Count after replace: {text.count(target)}')

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)

print('File written successfully.')
