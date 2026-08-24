import os, re

for fname in ['autonomous_code_synthesis_and_self_healing_multi_agent_systems.md', 'review_architectural_dynamics_long_12_page.md']:
    path = f'vault/04_Drafts/{fname}'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = re.sub(r'\\+b\\+blacksquare', r'\\blacksquare', text)
    text = text.replace(r'\b\blacksquare', r'\blacksquare')
    text = text.replace('$\\b\\blacksquare$', '$\\blacksquare$')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print('Cleaned blacksquare end tokens.')
