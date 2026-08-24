import os, re

drafts_dir = 'vault/04_Drafts'
for fname in sorted(os.listdir(drafts_dir)):
    if fname.endswith('.md'):
        path = os.path.join(drafts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        matches = []
        # Missing backslash in blacksquare
        if re.search(r'(?<!\\)blacksquare', text) or re.search(r'(?<!\\b)lacksquare', text):
            matches.append('malformed blacksquare')
        
        # Missing backslash in begin/end
        if re.search(r'(?<!\\)\b(begin|end)\{', text):
            matches.append('malformed begin/end')
            
        # Stray \b in text
        if '\\b\\begin' in text or '\\b\\end' in text or '\\b\\eta' in text or '\\b\\black' in text:
            matches.append('stray \\b prefix')
            
        # Unescaped eta with index
        if re.search(r'(?<!\\)eta[0-9_]', text):
            matches.append('unescaped eta')
            
        # Raw markdown bold/headers in math
        if re.search(r'\$\$[^\$]*\*\*[^\$]*\$\$', text):
            matches.append('bold in math')
        
        if matches:
            print(f'{fname}: {matches}')
        else:
            print(f'{fname}: 100% CLEAN')
