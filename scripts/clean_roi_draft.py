import re

fpath = 'vault/04_Drafts/review_enterprise_genai_roi.md'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix "use \cases" -> "use cases"
text = re.sub(r'\buse\s+\\cases\b', 'use cases', text)

# 2. Fix "\aligned." -> "aligned."
text = re.sub(r'\\aligned\b(?!\s*\{)', 'aligned', text)

# 3. Fix "use \cases," -> "use cases,"
text = text.replace('use \\cases', 'use cases')
text = text.replace('use \\cases,', 'use cases,')
text = text.replace('use \\cases.', 'use cases.')

# 4. Fix \begin{\aligned} -> \begin{aligned}
text = text.replace('\\begin{\\aligned}', '\\begin{aligned}')
text = text.replace('\\end{\\aligned}', '\\end{aligned}')

# 5. Fix math with escaped underscores in math mode: C\_{inference} -> C_{\text{inference}}
def fix_math_underscores(match):
    m = match.group(0)
    m = m.replace('\\_', '_')
    m = m.replace('\\\\_', '_')
    return m

text = re.sub(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\\$|[^\$])+?\$', fix_math_underscores, text)

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned review_enterprise_genai_roi.md successfully!')
