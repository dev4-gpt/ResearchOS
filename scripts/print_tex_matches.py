import os

for f in ['autonomous_code_synthesis_and_self_healing_multi_agent_systems_IEEEtran.tex', 'review_architectural_dynamics_long_12_page_IEEEtran.tex']:
    path = os.path.join('papers/p', f)
    with open(path, 'r') as fh:
        for i, line in enumerate(fh, 1):
            if '\\b\\' in line or '\\b\\begin' in line or '\\b\\black' in line:
                print(f'{f}:{i}: {line.strip()[:120]}')
