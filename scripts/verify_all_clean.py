import os, re

drafts_dir = 'vault/04_Drafts'
for fname in sorted(os.listdir(drafts_dir)):
    if fname.endswith('.md'):
        path = os.path.join(drafts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        matches = []
        for line in text.split('\n'):
            if r'\b\\' in line or r'\b\begin' in line or r'\b\black' in line or r'\b\end' in line or r'\b\cases' in line:
                matches.append(line.strip()[:60])
        
        if matches:
            print(f'{fname}: {matches}')
        else:
            print(f'{fname}: 100% CLEAN')
