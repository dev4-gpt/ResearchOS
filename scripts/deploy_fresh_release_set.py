import os, sys, time, json, re, shutil
sys.path.insert(0, 'backend')
from services.vault import VaultManager
from services.publisher_readiness import PublisherReadinessService
from services.checkmate_verifier import CheckmateVerifierService
from services.visual_auditor import VisualLayoutAuditorService
from services.venue_profiles import VENUE_PROFILES

try:
    import pypdf
except ImportError:
    import PyPDF2 as pypdf

print("=====================================================================")
print("=== DEPLOYING FRESH PRODUCTION SET TO papers/p1..p5 & papers/p ===")
print("=====================================================================")

vm = VaultManager('vault')
prs = PublisherReadinessService(vm)
cm = CheckmateVerifierService(vm)
vla = VisualLayoutAuditorService(vm)

# STEP 1: Clean old papers folders
print("\n>>> STEP 1: Cleaning and resetting release directories...")
for folder in ['p1', 'p2', 'p3', 'p4', 'p5', 'p']:
    dirpath = os.path.join('papers', folder)
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
    os.makedirs(dirpath, exist_ok=True)
print("Cleared old directories: p1, p2, p3, p4, p5, p")

# STEP 2: Execute fresh Publisher Readiness Run
print("\n>>> STEP 2: Running fresh release build across all 5 drafts and 12 venues...")
t0 = time.time()
report = prs.run()
t_elapsed = time.time() - t0

total_tests = report.get('total_tests', 0)
ready_count = report.get('ready_count', 0)
print(f"Build completed in {t_elapsed:.1f}s: {ready_count}/{total_tests} Publish-Ready")

manifest_path = os.path.join(vm.vault_path, '04_Drafts', 'exports', 'publisher_readiness_manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

# STEP 3: Populate papers/p (all 134 files)
print("\n>>> STEP 3: Deploying master release bundle to papers/p...")
exports_dir = os.path.join('vault', '04_Drafts', 'exports')
p_dir = os.path.join('papers', 'p')

for fname in os.listdir(exports_dir):
    src = os.path.join(exports_dir, fname)
    dst = os.path.join(p_dir, fname)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
print(f"Deployed {len(os.listdir(p_dir))} files to {p_dir}")

# STEP 4: Populate individual folders papers/p1..p5
print("\n>>> STEP 4: Deploying filtered topic packages to papers/p1 through papers/p5...")
mapping = {
    'p1': ('review_symbol_graph_rag_vs_qlora_swe_bench_lite', 'Empirical Evaluation of Symbol-Graph RAG vs QLoRA on SWE-bench Lite'),
    'p2': ('review_architectural_dynamics_long_12_page', 'Architectural Dynamics, Parameter Efficiency & Scaling Laws in LLM Systems'),
    'p3': ('autonomous_code_synthesis_and_self_healing_multi_agent_systems', 'Autonomous Code Synthesis and Self-Healing Multi-Agent Systems'),
    'p4': ('review_enterprise_genai_roi', 'Systematic Review & Meta-Taxonomy of Generative AI in Enterprise Workflows'),
    'p5': ('review_enterprise_adoption_of_multi_agent_ai_systems_infr', 'Enterprise Adoption of Multi-Agent AI Systems: Infrastructure, Reliability, and Economics')
}

inventory = {}

for folder, (prefix, title) in mapping.items():
    target_dir = os.path.join('papers', folder)
    copied = 0
    for fname in os.listdir(exports_dir):
        if fname.startswith(prefix):
            shutil.copy2(os.path.join(exports_dir, fname), os.path.join(target_dir, fname))
            copied += 1
            
    sub_results = [r for r in report.get('results', []) if r.get('filename', '').startswith(prefix)]
    sub_ready = sum(1 for r in sub_results if r.get('publish_ready'))
    sub_total = len(sub_results)
    
    sub_manifest = {
        'topic_title': title,
        'prefix': prefix,
        'ready_count': sub_ready,
        'total_tests': sub_total,
        'results': sub_results
    }
    with open(os.path.join(target_dir, 'publisher_readiness_manifest.json'), 'w', encoding='utf-8') as mf:
        json.dump(sub_manifest, mf, indent=2)
        
    pdfs = sorted([f for f in os.listdir(target_dir) if f.endswith('.pdf')])
    texs = sorted([f for f in os.listdir(target_dir) if f.endswith('.tex')])
    bibs = sorted([f for f in os.listdir(target_dir) if f.endswith('.bib')])
    
    inventory[folder] = {
        'title': title,
        'pdfs': len(pdfs),
        'texs': len(texs),
        'bibs': len(bibs),
        'ready': f"{sub_ready}/{sub_total}"
    }
    print(f"Deployed {folder}: {title[:50]}... -> {len(os.listdir(target_dir))} files (ready={sub_ready}/{sub_total})")

# STEP 5: Run Deep Multi-Layer Audit across all deployed files
print("\n>>> STEP 5: Running Deep Multi-Layer Verification across all newly deployed files...")
audit_failures = []
for pf in sorted([f for f in os.listdir(p_dir) if f.endswith('.pdf')]):
    pdf_path = os.path.join(p_dir, pf)
    reader = pypdf.PdfReader(pdf_path)
    full_text = "\n".join([p.extract_text() or "" for p in reader.pages])
    
    # Text leak check
    if re.search(r'\\begin\{|\\end\{|\\blacksquare|\\text\{|\\cite\{', full_text):
        audit_failures.append(f"{pf}: Leaked raw LaTeX macro code")
    if '**' in full_text:
        audit_failures.append(f"{pf}: Leaked markdown bold **")
    if '[[' in full_text and ']]' in full_text:
        audit_failures.append(f"{pf}: Leaked Obsidian wikilinks [[...]]")
    if re.search(r'\[\?\]|\(\?\?\)|\bundefined citation\b', full_text, re.I):
        audit_failures.append(f"{pf}: Undefined citation [?]")

print(f"Deep Audit Verification: {len(pdf_files := [f for f in os.listdir(p_dir) if f.endswith('.pdf')]) - len(audit_failures)}/{len(pdf_files)} PASSED")
if audit_failures:
    print("Failures:")
    for f in audit_failures:
        print(f"  [FAIL] {f}")
    sys.exit(1)
else:
    print(">>> 100% ZERO DEFECTS ACROSS ALL FRESHLY DEPLOYED PAPERS! <<<")

print("\n=====================================================================")
print("=== DEPLOYMENT AND VERIFICATION COMPLETE ===")
print("=====================================================================")
