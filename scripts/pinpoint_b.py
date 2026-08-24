import sys, re

with open('vault/04_Drafts/autonomous_code_synthesis_and_self_healing_multi_agent_systems.md', 'r') as f:
    text = f.read()

def check(step_name, s):
    has_b = '\\b\\' in s
    print(f'{step_name}: has \\b\\ = {has_b}')
    if has_b:
        for line in s.split('\n'):
            if '\\b\\' in line:
                print('   sample:', repr(line[:60]))
        sys.exit(0)

check('0. Initial', text)

text = text.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
check('1. Quotes', text)

text = text.replace('\x08', '')
check('2. Strip 0x08', text)

text = re.sub(r'(?:\\b|b|\x08)+\\*(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
check('3. sub begin/end 1', text)

text = re.sub(r'\\\\+(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
check('4. sub begin/end 2', text)

text = re.sub(r'(?<!\\)\b(begin|end)\{', lambda m: '\\' + m.group(1) + '{', text)
check('5. sub begin/end 3', text)

text = text.replace('egin{', '\\begin{')
check('6. replace egin', text)

text = text.replace('\text{', '\\text{').replace('\text', '\\text')
check('7. replace text', text)

text = text.replace('lacksquare', '\\blacksquare')
check('8. replace blacksquare', text)

text = re.sub(r'(?<!\\)eta([0-9])', lambda m: '\\eta_' + m.group(1), text)
check('9. eta 1', text)

text = re.sub(r'(?<!\\)eta_([0-9])', lambda m: '\\eta_' + m.group(1), text)
check('10. eta 2', text)
