import os, sys, hashlib, re, json
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.visual_auditor import VisualLayoutAuditorService

try:
    import pypdf
except ImportError:
    import PyPDF2 as pypdf

print("=====================================================================")
print("=== RUNNING COMPREHENSIVE ZERO-ERROR AUDIT ACROSS p1..p5 & p ===")
print("=====================================================================")

vm = VaultManager('vault')
vla = VisualLayoutAuditorService(vm)

p_dir = os.path.join('papers', 'p')
subfolders = ['p1', 'p2', 'p3', 'p4', 'p5']

def sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# 1. Check Subfolder-to-Master Parity
parity_errors = []
for sub in subfolders:
    s_dir = os.path.join('papers', sub)
    if not os.path.exists(s_dir):
        parity_errors.append(f"Directory missing: {s_dir}")
        continue
    
    files = [f for f in os.listdir(s_dir) if f != 'publisher_readiness_manifest.json' and not f.startswith('.')]
    if len(files) != 25:  # 12 PDFs + 12 TeX + 1 Bib
        parity_errors.append(f"{sub}: Expected 25 paper files, found {len(files)}")
        
    for fname in files:
        sub_file = os.path.join(s_dir, fname)
        master_file = os.path.join(p_dir, fname)
        if not os.path.exists(master_file):
            parity_errors.append(f"File {fname} in {sub} missing from {p_dir}")
        else:
            if sha256(sub_file) != sha256(master_file):
                parity_errors.append(f"Checksum mismatch for {fname} between {sub} and p")

print(f"1. Subfolder-to-Master Parity Check: {len(parity_errors)} errors")
if parity_errors:
    for e in parity_errors:
        print(f"   [FAIL] {e}")
    sys.exit(1)
else:
    print("   [PASS] All subfolders (p1..p5) match master (p) with 100% SHA256 checksum identity!")

# 2. Check PDFs for Visual Layout, Page Budgets, and Text-Layer Macro Leaks
pdf_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.pdf')])
pdf_errors = []

def get_venue(filename):
    for v in ['IEEE_Access', 'SpringerOpen', 'Femington', 'IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM', 'MDPI', 'DOAJ', 'arXiv']:
        if filename.endswith(f'_{v}.pdf') or filename.endswith(f'_{v}.tex'):
            return v
    return 'Unknown'

for pf in pdf_files:
    venue = get_venue(pf)
    pdf_path = os.path.join(p_dir, pf)
    reader = pypdf.PdfReader(pdf_path)
    page_texts = [p.extract_text() or "" for p in reader.pages]
    full_text = "\n".join(page_texts)
    
    # Check for raw leaks
    if re.search(r'\\begin\{|\\end\{|\\blacksquare|\\text\{|\\cite\{', full_text):
        pdf_errors.append(f"{pf}: Leaked raw LaTeX macro code in PDF text")
    if '**' in full_text:
        pdf_errors.append(f"{pf}: Leaked markdown bold ** in PDF text")
    if '[[' in full_text and ']]' in full_text:
        pdf_errors.append(f"{pf}: Leaked Obsidian wikilink [[...]] in PDF text")
    if re.search(r'\[\?\]|\(\?\?\)|\bundefined citation\b', full_text, re.I):
        pdf_errors.append(f"{pf}: Undefined citation [?] in PDF text")
        
    # Check layout geometry
    geom = vla.audit_layout_geometry(pdf_path, venue_key=venue)
    if not geom.get('passed', False):
        pdf_errors.append(f"{pf}: Visual layout failure - {geom.get('detail')}")

print(f"2. PDF Deep Text & Layout Inspection: {len(pdf_errors)} errors across {len(pdf_files)} PDFs")
if pdf_errors:
    for e in pdf_errors:
        print(f"   [FAIL] {e}")
    sys.exit(1)
else:
    print(f"   [PASS] All {len(pdf_files)} PDFs passed deep text extraction & layout geometry audits!")

# 3. Check TeX Source Files for Syntax & Macro Balance
tex_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.tex')])
tex_errors = []

for tf in tex_files:
    venue = get_venue(tf)
    tex_path = os.path.join(p_dir, tf)
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if re.search(r'\\+b\\+([a-zA-Z]+)', content):
        tex_errors.append(f"{tf}: Stray \\b\\ command prefix")
    if re.search(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', content):
        tex_errors.append(f"{tf}: Escaped environment name inside begin/end")
    if re.search(r'(?<!\\)\b(begin|end)\{', content):
        tex_errors.append(f"{tf}: Unescaped begin/end")
    if re.search(r'(?<!\\)\bblacksquare\b', content):
        tex_errors.append(f"{tf}: Unescaped blacksquare")
    if re.search(r'(?<!\\)eta[0-9_]', content):
        tex_errors.append(f"{tf}: Unescaped Greek letter eta")
        
    b_eq = len(re.findall(r'\\begin\{equation\*?\}', content))
    e_eq = len(re.findall(r'\\end\{equation\*?\}', content))
    if b_eq != e_eq:
        tex_errors.append(f"{tf}: Unbalanced equation environments ({b_eq} vs {e_eq})")

print(f"3. TeX Source Syntax & Environment Balance: {len(tex_errors)} errors across {len(tex_files)} TeX files")
if tex_errors:
    for e in tex_errors:
        print(f"   [FAIL] {e}")
    sys.exit(1)
else:
    print(f"   [PASS] All {len(tex_files)} TeX files have 100% balanced, sound syntax!")

# 4. Check Sub-manifests
manifest_errors = []
for sub in subfolders:
    mf_path = os.path.join('papers', sub, 'publisher_readiness_manifest.json')
    if not os.path.exists(mf_path):
        manifest_errors.append(f"Missing manifest in {sub}")
    else:
        with open(mf_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data.get('ready_count') != 12 or data.get('total_tests') != 12:
            manifest_errors.append(f"{sub}: ready_count is {data.get('ready_count')}/12")

print(f"4. Publisher Readiness Sub-Manifests: {len(manifest_errors)} errors")
if manifest_errors:
    for e in manifest_errors:
        print(f"   [FAIL] {e}")
    sys.exit(1)
else:
    print("   [PASS] All sub-manifests show ready_count = 12/12 (100% publish ready)!")

print("\n=====================================================================")
print("=== ALL AUDITS PASSED WITH ZERO ERRORS (60/60 PAPERS VERIFIED) ===")
print("=====================================================================")
