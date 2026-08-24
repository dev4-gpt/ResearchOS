import os, re

drafts_dir = 'vault/04_Drafts'
for fname in sorted(os.listdir(drafts_dir)):
    if fname.endswith('.md'):
        path = os.path.join(drafts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Replace r'\b\' with r'\'
        text = text.replace(r'\b\begin', r'\begin')
        text = text.replace(r'\b\end', r'\end')
        text = text.replace(r'\b\blacksquare', r'\blacksquare')
        text = text.replace(r'\b\cases', r'\cases')
        text = text.replace(r'\b\aligned', r'\aligned')
        text = text.replace(r'\b\equation', r'\equation')
        text = text.replace(r'\b\eta', r'\eta')
        text = text.replace(r'\b\Delta', r'\Delta')
        text = text.replace(r'\b\ln', r'\ln')
        text = text.replace(r'\b\text', r'\text')
        text = text.replace(r'\b\mu', r'\mu')
        text = text.replace(r'\b\lambda', r'\lambda')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

print('Cleaned raw backslash-b in all drafts!')
