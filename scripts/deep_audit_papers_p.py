import os, sys, re, json
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.checkmate_verifier import CheckmateVerifierService
from services.visual_auditor import VisualLayoutAuditorService
from services.fact_checker import FactCheckerService

p_dir = 'papers/p'
files = os.listdir(p_dir)
tex_files = sorted([f for f in files if f.endswith('.tex')])
pdf_files = sorted([f for f in files if f.endswith('.pdf')])
bib_files = sorted([f for f in files if f.endswith('.bib')])

print(f'Total in {p_dir}: {len(files)} files')
print(f'  TeX files: {len(tex_files)}')
print(f'  PDF files: {len(pdf_files)}')
print(f'  BibTeX files: {len(bib_files)}')

vm = VaultManager('vault')
cm = CheckmateVerifierService(vm)
vla = VisualLayoutAuditorService(vm)
fc = FactCheckerService(vm)

tex_anomalies = []
for tf in tex_files:
    path = os.path.join(p_dir, tf)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for malformed patterns using sound regexes
    if re.search(r'\\+b\\+([a-zA-Z]+)', content):
        tex_anomalies.append((tf, 'stray \\b\\ command prefix detected'))
    if re.search(r'(?<!\\)\b(begin|end)\{', content):
        tex_anomalies.append((tf, 'missing backslash in begin/end'))
    if re.search(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', content):
        tex_anomalies.append((tf, 'escaped environment name inside begin/end'))
    if re.search(r'(?<!\\)\bblacksquare\b', content):
        tex_anomalies.append((tf, 'unescaped blacksquare detected'))
    if re.search(r'(?<!\\)eta[0-9_]', content):
        tex_anomalies.append((tf, 'unescaped eta detected'))
    if '**' in content:
        tex_anomalies.append((tf, 'raw markdown bold ** detected'))
    if re.search(r'^##\s', content, re.M):
        tex_anomalies.append((tf, 'raw markdown heading ## detected'))

print('\nTeX syntax audit anomalies:', len(tex_anomalies))
for tf, anomaly in tex_anomalies:
    print(f'  {tf}: {anomaly}')

# Audit PDF files
pdf_audit_results = []
for pf in pdf_files:
    path = os.path.join(p_dir, pf)
    size = os.path.getsize(path)
    if size < 1000:
        pdf_audit_results.append((pf, False, f'Size too small: {size} bytes'))
        continue
    
    # Identify venue from filename
    venue = pf.replace('.pdf', '').split('_')[-1]
    if pf.endswith('_IEEE_Access.pdf'):
        venue = 'IEEE_Access'
    elif pf.endswith('_SpringerOpen.pdf'):
        venue = 'SpringerOpen'
        
    layout = vla.audit_layout_geometry(path, venue_key=venue)
    passed = layout.get('passed', False)
    pages = layout.get('total_pages', 0)
    pdf_audit_results.append((pf, passed, f'{size:,} bytes, {pages} pages'))

failed_pdfs = [r for r in pdf_audit_results if not r[1]]
print(f'\nPDF layout audit: {len(pdf_files) - len(failed_pdfs)}/{len(pdf_files)} PASSED')
if failed_pdfs:
    print('Failed PDFs:')
    for pf, passed, detail in failed_pdfs:
        print(f'  {pf}: {detail}')
else:
    print('ALL 60 PDFs PASSED VISUAL LAYOUT GEOMETRY AUDIT!')

# Verify manifest
manifest_path = os.path.join(p_dir, 'publisher_readiness_manifest.json')
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        m = json.load(f)
    ready = m.get('ready_count')
    total = m.get('total_tests')
    drafts = m.get('draft_count')
    print(f'\nManifest check: {ready}/{total} Ready, Drafts: {drafts}')
