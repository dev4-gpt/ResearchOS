import os, sys, re, json
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.checkmate_verifier import CheckmateVerifierService
from services.visual_auditor import VisualLayoutAuditorService
from services.venue_profiles import VENUE_PROFILES

try:
    import pypdf
except ImportError:
    import PyPDF2 as pypdf

p_dir = 'papers/p'
pdf_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.pdf')])
tex_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.tex')])

print(f"=== DEEP INSPECTION OF {len(pdf_files)} PDFs and {len(tex_files)} TeX FILES ===")

vm = VaultManager('vault')
vla = VisualLayoutAuditorService(vm)

report = {
    'total_pdfs': len(pdf_files),
    'total_texs': len(tex_files),
    'venue_breakdown': {},
    'anomalies': [],
    'pdf_details': []
}

# Venue mapping helper
def get_venue(filename):
    for v in ['IEEE_Access', 'SpringerOpen', 'Femington', 'IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM', 'MDPI', 'DOAJ', 'arXiv']:
        if filename.endswith(f'_{v}.pdf') or filename.endswith(f'_{v}.tex'):
            return v
    return 'Unknown'

for pf in pdf_files:
    venue = get_venue(pf)
    pdf_path = os.path.join(p_dir, pf)
    tex_path = os.path.join(p_dir, pf.replace('.pdf', '.tex'))
    
    # 1. Inspect PDF pages and text
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    file_size = os.path.getsize(pdf_path)
    
    full_text = ""
    page_texts = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        page_texts.append(t)
        full_text += f"\n--- PAGE {i+1} ---\n" + t
    
    # Check for text anomalies in PDF
    pdf_anomalies = []
    
    # Check for undefined citations
    if re.search(r'\[\?\]|\(\?\?\)|\bundefined citation\b', full_text, re.I):
        pdf_anomalies.append('Undefined citation [?] in PDF text')
        
    # Check for raw markdown artifacts
    if '**' in full_text:
        pdf_anomalies.append('Raw markdown bold ** found in PDF text')
    if '[[' in full_text and ']]' in full_text:
        pdf_anomalies.append('Raw Obsidian wikilink [[...]] found in PDF text')
        
    # Check for duplicate section numbering like "1 1 Executive Abstract" or "2 2 Introduction" on single line
    for page_t in page_texts:
        for line in page_t.split('\n'):
            if re.search(r'^\s*(\d+|[IVXLCDM]+)\s+(\1|\d+)\s+[A-Z]', line):
                pdf_anomalies.append(f'Duplicate section counter numbering on line: {line}')
        
    # Check for raw LaTeX syntax leaked into visible text
    if re.search(r'\\begin\{|\\end\{|\\blacksquare|\\text\{|\\cite\{', full_text):
        pdf_anomalies.append('Raw LaTeX macro code leaked into PDF text')
        
    # 2. Visual layout geometry check
    layout = vla.audit_layout_geometry(pdf_path, venue_key=venue)
    layout_passed = layout.get('passed', False)
    
    # 3. TeX source inspection
    tex_anomalies = []
    if os.path.exists(tex_path):
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        if re.search(r'\\+b\\+([a-zA-Z]+)', tex_content):
            tex_anomalies.append('Stray \\b\\ command prefix in TeX')
        if re.search(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', tex_content):
            tex_anomalies.append('Escaped environment name in begin/end')
        if re.search(r'(?<!\\)\b(begin|end)\{', tex_content):
            tex_anomalies.append('Unescaped begin/end')
        if re.search(r'(?<!\\)\bblacksquare\b', tex_content):
            tex_anomalies.append('Unescaped blacksquare')
        if re.search(r'(?<!\\)eta[0-9_]', tex_content):
            tex_anomalies.append('Unescaped eta')
            
        # Double-blind check
        prof = VENUE_PROFILES.get(venue)
        if prof and prof.anonymized_review:
            if 'Aryaman' in tex_content:
                tex_anomalies.append(f'Author name not anonymized in double-blind venue {venue}')
    else:
        tex_anomalies.append('TeX source file missing')

    status = 'PASS' if (not pdf_anomalies and not tex_anomalies and layout_passed) else 'FAIL'
    
    details = {
        'filename': pf,
        'venue': venue,
        'pages': num_pages,
        'size_bytes': file_size,
        'layout_passed': layout_passed,
        'pdf_anomalies': pdf_anomalies,
        'tex_anomalies': tex_anomalies,
        'status': status
    }
    report['pdf_details'].append(details)
    
    if status == 'FAIL':
        report['anomalies'].append(details)
        
    v_stat = report['venue_breakdown'].setdefault(venue, {'total': 0, 'passed': 0, 'failed': 0})
    v_stat['total'] += 1
    if status == 'PASS':
        v_stat['passed'] += 1
    else:
        v_stat['failed'] += 1

print(f"\n--- AUDIT RESULTS SUMMARY ---")
passed_count = sum(1 for d in report['pdf_details'] if d['status'] == 'PASS')
print(f"Total Papers Audited: {len(pdf_files)}")
print(f"Passed All Checks: {passed_count} / {len(pdf_files)}")
print(f"Failed Checks: {len(report['anomalies'])} / {len(pdf_files)}")

print("\n--- BREAKDOWN BY VENUE ---")
for v, stat in sorted(report['venue_breakdown'].items()):
    print(f"  {v:15s}: {stat['passed']}/{stat['total']} PASS")

if report['anomalies']:
    print("\n--- ANOMALIES FOUND ---")
    for a in report['anomalies']:
        print(f"[{a['venue']}] {a['filename']}:")
        if a['pdf_anomalies']:
            print(f"   PDF Issues: {a['pdf_anomalies']}")
        if a['tex_anomalies']:
            print(f"   TeX Issues: {a['tex_anomalies']}")
        if not a['layout_passed']:
            print(f"   Layout Geometry: FAILED")
else:
    print("\n>>> ZERO DEFECTS FOUND ACROSS ALL 60 PAPERS! <<<")
