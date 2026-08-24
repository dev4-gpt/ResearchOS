import re

fpath = 'vault/04_Drafts/review_enterprise_genai_roi.md'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix \begin{\equation} and \end{\equation}
text = text.replace('\\begin{\\equation}', '\\begin{equation}')
text = text.replace('\\end{\\equation}', '\\end{equation}')
text = text.replace('\\begin{\\aligned}', '\\begin{aligned}')
text = text.replace('\\end{\\aligned}', '\\end{aligned}')

# Fix math mode underscores and labels
text = text.replace('C_{data\\_transfer}', 'C_{\\text{transfer}}')
text = text.replace('C_{data_transfer}', 'C_{\\text{transfer}}')
text = text.replace('C_{inference}', 'C_{\\text{inference}}')
text = text.replace('C_{infrastructure}', 'C_{\\text{infrastructure}}')
text = text.replace('C_{storage}', 'C_{\\text{storage}}')
text = text.replace('\\label{eq:operational_cost}', '')
text = text.replace('X_{GenAI}', 'X_{\\text{GenAI}}')

# Ensure wrap equations in $$...$$ for clean markdown math blocks
eq1 = """$$
\\begin{aligned}
\\text{ROI} = \\frac{\\text{Net Profit attributable to GenAI}}{\\text{Cost of GenAI Investment}} \\times 100\\%
\\end{aligned}
$$"""

eq2 = """$$
\\begin{aligned}
\\text{ROI} = \\frac{(\\Delta R + \\Delta C) - I}{I} \\times 100\\%
\\end{aligned}
$$"""

eq3 = """$$
\\begin{aligned}
C_{\\text{op}} = & N_{\\text{req}} \\times (C_{\\text{inference}} + C_{\\text{transfer}}) \\\\
& + C_{\\text{infrastructure}} + C_{\\text{storage}}
\\end{aligned}
$$"""

eq4 = """$$
\\begin{aligned}
Y = & \\alpha + \\tau X_{\\text{GenAI}} \\\\
& + \\sum_{i=1}^k \\eta_i Z_i + \\epsilon
\\end{aligned}
$$"""

# Replace all 4 equation blocks cleanly
text = re.sub(r'\\begin\{equation\}[\s\S]*?\\end\{equation\}', '@@EQ@@', text)
parts = text.split('@@EQ@@')
if len(parts) == 5:
    text = parts[0] + eq1 + parts[1] + eq2 + parts[2] + eq3 + parts[3] + eq4 + parts[4]

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated ROI draft with pristine display math blocks!')
