import os, sys, time, json, re, shutil
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.publisher_readiness import PublisherReadinessService
from services.checkmate_verifier import CheckmateVerifierService
from services.visual_auditor import VisualLayoutAuditorService
from services.fact_checker import FactCheckerService
from services.venue_profiles import VENUE_PROFILES

try:
    import pypdf
except ImportError:
    import PyPDF2 as pypdf

print("=====================================================================")
print("=== STARTING MASTER RESEARCHING-OS MULTI-VENUE PUBLICATION SUITE ===")
print("=====================================================================")

vm = VaultManager('vault')
prs = PublisherReadinessService(vm)
cm = CheckmateVerifierService(vm)
vla = VisualLayoutAuditorService(vm)
fc = FactCheckerService(vm)

# STEP 1: Execute Full 60-build Publisher Readiness run
print("\n>>> STEP 1: Running PublisherReadinessService on all 5 drafts across all 12 venues...")
t0 = time.time()
report = prs.run()
t_elapsed = time.time() - t0

total_tests = report.get('total_tests', 0)
ready_count = report.get('ready_count', 0)
print(f"Publisher Readiness Run Complete in {t_elapsed:.1f}s: {ready_count}/{total_tests} Publish-Ready")

manifest_path = os.path.join(vm.vault_path, '04_Drafts', 'exports', 'publisher_readiness_manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

# STEP 2: Sync to papers/p and papers/p1..p5
print("\n>>> STEP 2: Synchronizing Distribution Release Bundles to papers/p and papers/p1..p5...")
exports_dir = os.path.join('vault', '04_Drafts', 'exports')
p_dir = os.path.join('papers', 'p')
os.makedirs(p_dir, exist_ok=True)

# Copy all to papers/p
for fname in os.listdir(exports_dir):
    src = os.path.join(exports_dir, fname)
    dst = os.path.join(p_dir, fname)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
print(f"Synced {len(os.listdir(p_dir))} files to {p_dir}")

mapping = {
    'p1': 'review_symbol_graph_rag_vs_qlora_swe_bench_lite',
    'p2': 'review_architectural_dynamics_long_12_page',
    'p3': 'autonomous_code_synthesis_and_self_healing_multi_agent_systems',
    'p4': 'review_enterprise_genai_roi',
    'p5': 'review_enterprise_adoption_of_multi_agent_ai_systems_infr'
}

for folder, prefix in mapping.items():
    target_dir = os.path.join('papers', folder)
    os.makedirs(target_dir, exist_ok=True)
    copied = 0
    for fname in os.listdir(exports_dir):
        if fname.startswith(prefix):
            shutil.copy2(os.path.join(exports_dir, fname), os.path.join(target_dir, fname))
            copied += 1
            
    sub_results = [r for r in report.get('results', []) if r.get('filename', '').startswith(prefix)]
    sub_ready = sum(1 for r in sub_results if r.get('publish_ready'))
    sub_total = len(sub_results)
    sub_manifest = {
        'ready_count': sub_ready,
        'total_tests': sub_total,
        'results': sub_results
    }
    with open(os.path.join(target_dir, 'publisher_readiness_manifest.json'), 'w', encoding='utf-8') as mf:
        json.dump(sub_manifest, mf, indent=2)
    print(f"Synced {copied + 1} files to {target_dir} (ready_count={sub_ready}/{sub_total})")

# STEP 3: Deep Backtesting & Text-Layer Auditing across all 60 PDFs & TeX files
print("\n>>> STEP 3: Running Deep Backtesting & Text-Layer Extraction Audit on all 60 PDF Artifacts...")
pdf_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.pdf')])
tex_files = sorted([f for f in os.listdir(p_dir) if f.endswith('.tex')])

def get_venue(filename):
    for v in ['IEEE_Access', 'SpringerOpen', 'Femington', 'IEEEtran', 'NeurIPS', 'ICML', 'CVPR', 'ACL', 'ACM', 'MDPI', 'DOAJ', 'arXiv']:
        if filename.endswith(f'_{v}.pdf') or filename.endswith(f'_{v}.tex'):
            return v
    return 'Unknown'

deep_anomalies = []
for pf in pdf_files:
    venue = get_venue(pf)
    pdf_path = os.path.join(p_dir, pf)
    tex_path = os.path.join(p_dir, pf.replace('.pdf', '.tex'))
    
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    file_size = os.path.getsize(pdf_path)
    
    full_text = ""
    page_texts = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        page_texts.append(t)
        full_text += f"\n--- PAGE {i+1} ---\n" + t
        
    issues = []
    # 1. Undefined citation check
    if re.search(r'\[\?\]|\(\?\?\)|\bundefined citation\b', full_text, re.I):
        issues.append('Undefined citation [?] in PDF text')
        
    # 2. Leaked markdown check
    if '**' in full_text:
        issues.append('Raw markdown bold ** found in PDF text')
    if '[[' in full_text and ']]' in full_text:
        issues.append('Raw Obsidian wikilink [[...]] found in PDF text')
        
    # 3. Duplicate numbering on single line
    for page_t in page_texts:
        for line in page_t.split('\n'):
            if re.search(r'^\s*(\d+|[IVXLCDM]+)\s+(\1|\d+)\s+[A-Z]', line):
                issues.append(f'Duplicate section counter numbering: {line}')
                
    # 4. Leaked raw LaTeX code in visible text
    if re.search(r'\\begin\{|\\end\{|\\blacksquare|\\text\{|\\cite\{', full_text):
        issues.append('Raw LaTeX macro code leaked into PDF text')
        
    # 5. Visual layout geometry check
    layout = vla.audit_layout_geometry(pdf_path, venue_key=venue)
    if not layout.get('passed', False):
        issues.append(f'Visual layout geometry failed: {layout.get("detail")}')
        
    # 6. TeX syntax inspection
    if os.path.exists(tex_path):
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        if re.search(r'\\+b\\+([a-zA-Z]+)', tex_content):
            issues.append('Stray \\b\\ command prefix in TeX')
        if re.search(r'\\*(begin|end)\{\\+([a-zA-Z]+)\}', tex_content):
            issues.append('Escaped environment name inside begin/end in TeX')
        if re.search(r'(?<!\\)\b(begin|end)\{', tex_content):
            issues.append('Unescaped begin/end in TeX')
        if re.search(r'(?<!\\)\bblacksquare\b', tex_content):
            issues.append('Unescaped blacksquare in TeX')
        if re.search(r'(?<!\\)eta[0-9_]', tex_content):
            issues.append('Unescaped eta in TeX')
        begins_eq = len(re.findall(r'\\begin\{equation\*?\}', tex_content))
        ends_eq = len(re.findall(r'\\end\{equation\*?\}', tex_content))
        if begins_eq != ends_eq:
            issues.append(f'Unbalanced equation environments ({begins_eq} vs {ends_eq})')
            
        # Double-blind check
        prof = VENUE_PROFILES.get(venue)
        if prof and prof.anonymized_review:
            if 'Aryaman' in tex_content:
                issues.append(f'Author name not anonymized in double-blind venue {venue}')
    else:
        issues.append('TeX source file missing')

    if issues:
        deep_anomalies.append({'filename': pf, 'venue': venue, 'issues': issues})

print(f"\nDeep Backtesting Complete: {len(pdf_files) - len(deep_anomalies)} / {len(pdf_files)} PASSED")
if deep_anomalies:
    print("ANOMALIES FOUND:")
    for a in deep_anomalies:
        print(f"  [{a['venue']}] {a['filename']}: {a['issues']}")
    sys.exit(1)
else:
    print(">>> ZERO DEFECTS FOUND ACROSS ALL 60 PAPERS! 100% PRODUCTION READY! <<<")

print("\n=====================================================================")
print("=== MASTER PUBLICATION AND BACKTESTING SUITE COMPLETED WITH 100% PASS ===")
print("=====================================================================")
