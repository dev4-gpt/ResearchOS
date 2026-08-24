import os, re

for fname in ['autonomous_code_synthesis_and_self_healing_multi_agent_systems.md', 'review_architectural_dynamics_long_12_page.md']:
    path = f'vault/04_Drafts/{fname}'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Print occurrences
    for m in re.finditer(r'\\b\\[a-zA-Z]+', text):
        print(f'{fname}: found {m.group(0)}')
    
    # Strip \b before any backslash command
    text = re.sub(r'\\b\\([a-zA-Z]+)', r'\\\1', text)
    text = re.sub(r'\\b\\b\\([a-zA-Z]+)', r'\\\1', text)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print('Surgically cleaned stray \\b in both files.')
