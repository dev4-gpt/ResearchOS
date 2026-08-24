import os, sys, re, json, time
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.checkmate_verifier import CheckmateVerifierService
from services.visual_auditor import VisualLayoutAuditorService
from services.latex_exporter import LaTeXExporterService, VENUE_SPECS
from services.venue_profiles import VENUE_PROFILES
from services.publisher_readiness import PublisherReadinessService

try:
    import pypdf
except ImportError:
    import PyPDF2 as pypdf

print("================================================================================")
print("=== DEEP VENUE AUDIT & CROSS-CHECK ON ALL 60 PAPERS IN papers/p ===")
print("================================================================================")

vm = VaultManager('vault')
cm = CheckmateVerifierService(vm)
vla = VisualLayoutAuditorService(vm)
prs = PublisherReadinessService(vm)

p_dir = os.path.join('papers', 'p')
pdf_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.pdf')])

def get_venue(filename):
    for v in ['IEEE_Access', 'SpringerOpen', 'Femington', 'IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM', 'MDPI', 'DOAJ', 'arXiv']:
        if filename.endswith(f'_{v}.pdf') or filename.endswith(f'_{v}.tex'):
            return v
    return 'Unknown'

print(f"Total PDFs found: {len(pdf_files)}")

results_matrix = []
all_passed = True

for pf in pdf_files:
    venue = get_venue(pf)
    pdf_path = os.path.join(p_dir, pf)
    tex_path = os.path.join(p_dir, pf.replace('.pdf', '.tex'))
    
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    file_size_kb = os.path.getsize(pdf_path) / 1024
    
    page_texts = [p.extract_text() or "" for p in reader.pages]
    full_text = "\n".join(page_texts)
    
    issues = []
    
    # 1. Page Budget Check
    prof = VENUE_PROFILES.get(venue)
    spec = VENUE_SPECS.get(venue, {})
    expected_short = spec.get('short_page_limit', 4)
    expected_long = spec.get('long_page_limit', 20)
    
    # Check page count against venue profile
    if prof:
        max_allowed = prof.long_page_limit or prof.page_limit or 20
        if num_pages > max_allowed:
            issues.append(f"Page count ({num_pages}) exceeds venue maximum allowed ({max_allowed})")
    
    # 2. Text-layer Macro Leak Check
    if re.search(r'\\begin\{|\\end\{|\\blacksquare|\\text\{|\\cite\{', full_text):
        issues.append("Raw LaTeX macro code leaked in PDF text layer")
    if '**' in full_text:
        issues.append("Raw markdown bold ** leaked in PDF text layer")
    if '[[' in full_text and ']]' in full_text:
        issues.append("Raw Obsidian wikilinks [[...]] leaked in PDF text layer")
    if re.search(r'\[\?\]|\(\?\?\)|\bundefined citation\b', full_text, re.I):
        issues.append("Undefined citation [?] in PDF text layer")
        
    # 3. Duplicate Section Numbering Check
    for page_t in page_texts:
        for line in page_t.split('\n'):
            if re.search(r'^\s*(\d+|[IVXLCDM]+)\s+(\1|\d+)\s+[A-Z]', line):
                issues.append(f"Duplicate section counter on single line: {line.strip()}")
                
    # 4. TeX Syntax Check
    if os.path.exists(tex_path):
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_code = f.read()
        if re.search(r'\\+b\\+([a-zA-Z]+)', tex_code):
            issues.append("Stray \\b\\ command prefix in TeX source")
        if re.search(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', tex_code):
            issues.append("Escaped environment name inside begin/end in TeX")
        if re.search(r'(?<!\\)\b(begin|end)\{', tex_code):
            issues.append("Unescaped begin/end in TeX")
        if re.search(r'(?<!\\)\bblacksquare\b', tex_code):
            issues.append("Unescaped blacksquare in TeX")
            
        begins_eq = len(re.findall(r'\\begin\{equation\*?\}', tex_code))
        ends_eq = len(re.findall(r'\\end\{equation\*?\}', tex_code))
        if begins_eq != ends_eq:
            issues.append(f"Unbalanced equation environments ({begins_eq} vs {ends_eq})")
            
        # Double-blind Anonymization Check
        if prof and prof.anonymized_review:
            if 'Aryaman' in tex_code:
                issues.append(f"Author name not anonymized in double-blind venue {venue}")
    else:
        issues.append("TeX source file missing")
        
    # 5. Visual Layout Geometry Check
    layout = vla.audit_layout_geometry(pdf_path, venue_key=venue)
    if not layout.get('passed', False):
        issues.append(f"Visual layout geometry error: {layout.get('detail')}")
        
    status = "PASS" if not issues else "FAIL"
    if issues:
        all_passed = False
        
    results_matrix.append({
        'filename': pf,
        'venue': venue,
        'pages': num_pages,
        'size_kb': round(file_size_kb, 1),
        'status': status,
        'issues': issues
    })

print("\n--- DETAILED AUDIT RESULTS ---")
for r in results_matrix:
    status_str = f"✅ PASS ({r['pages']}p, {r['size_kb']}KB)" if r['status'] == 'PASS' else f"❌ FAIL ({r['issues']})"
    print(f"[{r['venue']:<12}] {r['filename']:<75} : {status_str}")

print("\n--- SUMMARY BY VENUE ---")
venue_counts = {}
for r in results_matrix:
    v = r['venue']
    if v not in venue_counts:
        venue_counts[v] = {'pass': 0, 'fail': 0}
    if r['status'] == 'PASS':
        venue_counts[v]['pass'] += 1
    else:
        venue_counts[v]['fail'] += 1

for v, c in sorted(venue_counts.items()):
    print(f"  {v:<15}: {c['pass']}/5 PASS (Failures: {c['fail']})")

print("\n================================================================================")
if all_passed:
    print(">>> 100% PERFECT: ALL 60 PAPERS ARE ZERO-DEFECT AND PUBLICATION READY! <<<")
else:
    print(">>> FAILURES DETECTED - AUTOMATED SELF-HEALING REQUIRED <<<")
print("================================================================================")
