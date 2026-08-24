import os

drafts_dir = 'vault/04_Drafts'
targets = [
    ('\\b\\begin', '\\begin'),
    ('\\b\\end', '\\end'),
    ('\\b\\blacksquare', '\\blacksquare'),
    ('\\b\\cases', '\\cases'),
    ('\\b\\aligned', '\\aligned'),
    ('\\b\\equation', '\\equation'),
    ('\\b\\eta', '\\eta'),
    ('\\b\\Delta', '\\Delta'),
    ('\\b\\ln', '\\ln'),
    ('\\b\\text', '\\text'),
    ('\\b\\mu', '\\mu'),
    ('\\b\\lambda', '\\lambda'),
    ('lacksquare', '\\blacksquare'),
    ('\\\\blacksquare', '\\blacksquare')
]

for fname in sorted(os.listdir(drafts_dir)):
    if fname.endswith('.md'):
        path = os.path.join(drafts_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        replaced_total = 0
        for tgt, repl in targets:
            c = text.count(tgt)
            if c > 0:
                text = text.replace(tgt, repl)
                replaced_total += c
                
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
            
        print(f'{fname}: replaced {replaced_total} anomalies')

print('All drafts processed successfully.')
