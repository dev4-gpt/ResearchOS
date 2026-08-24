import glob, os, re

for fpath in glob.glob('vault/04_Drafts/*.md'):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    orig = text
    
    # 1. Fix "use \cases" -> "use cases"
    text = re.sub(r'\\cases\b', 'cases', text)
    
    # 2. Fix "\aligned" in prose -> "aligned"
    text = re.sub(r'\\aligned\b(?!\s*\{)', 'aligned', text)
    
    # 3. Fix \b\command
    text = re.sub(r'\\+b\\+([a-zA-Z]+)', r'\\\1', text)
    
    # 4. Fix \begin{\aligned} -> \begin{aligned}
    text = re.sub(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', r'\\\1{\2}', text)
    
    # 5. Fix \b\begin or \b\black
    text = text.replace('\\b\\begin', '\\begin').replace('\\b\\black', '\\black')
    
    if text != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Cleaned {os.path.basename(fpath)}')
    else:
        print(f'Already pristine: {os.path.basename(fpath)}')

print('All drafts audited and sanitized.')
