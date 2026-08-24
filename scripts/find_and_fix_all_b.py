import os, re

drafts_dir = 'vault/04_Drafts'
for fname in sorted(os.listdir(drafts_dir)):
    if fname.endswith('.md'):
        path = os.path.join(drafts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Replace any literal backslash followed by b followed by backslash
        orig_len = len(text)
        text = text.replace('\\b\\begin', '\\begin')
        text = text.replace('\\b\\end', '\\end')
        text = text.replace('\\b\\blacksquare', '\\blacksquare')
        text = text.replace('\\b\\cases', '\\cases')
        text = text.replace('\\b\\aligned', '\\aligned')
        text = text.replace('\\b\\equation', '\\equation')
        text = text.replace('\\b\\eta', '\\eta')
        text = text.replace('\\b\\Delta', '\\Delta')
        text = text.replace('\\b\\ln', '\\ln')
        text = text.replace('\\b\\text', '\\text')
        text = text.replace('\\b\\mu', '\\mu')
        text = text.replace('\\b\\lambda', '\\lambda')
        text = re.sub(r'\\b\\([a-zA-Z]+)', r'\\\1', text)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

print('Cleaned drafts with find_and_fix_all_b.py')
