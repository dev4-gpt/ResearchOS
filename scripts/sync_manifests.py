import os, sys, shutil, json

# Sync exports to papers/p and papers/p1..p5
exports_dir = os.path.join('vault', '04_Drafts', 'exports')
p_all_dir = os.path.join('papers', 'p')
os.makedirs(p_all_dir, exist_ok=True)

# Copy all to papers/p
for fname in os.listdir(exports_dir):
    src = os.path.join(exports_dir, fname)
    dst = os.path.join(p_all_dir, fname)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
print(f'Synced {len(os.listdir(p_all_dir))} files to {p_all_dir}')

# Mapping to p1..p5
mapping = {
    'p1': 'review_symbol_graph_rag_vs_qlora_swe_bench_lite',
    'p2': 'review_architectural_dynamics_long_12_page',
    'p3': 'autonomous_code_synthesis_and_self_healing_multi_agent_systems',
    'p4': 'review_enterprise_genai_roi',
    'p5': 'review_enterprise_adoption_of_multi_agent_ai_systems_infr'
}

with open(os.path.join(exports_dir, 'publisher_readiness_manifest.json'), 'r') as mf:
    full_manifest = json.load(mf)

for folder, prefix in mapping.items():
    target_dir = os.path.join('papers', folder)
    os.makedirs(target_dir, exist_ok=True)
    
    # Filter and copy matching files
    copied = 0
    for fname in os.listdir(exports_dir):
        if fname.startswith(prefix):
            shutil.copy2(os.path.join(exports_dir, fname), os.path.join(target_dir, fname))
            copied += 1
            
    sub_results = [r for r in full_manifest.get('results', []) if r.get('filename', '').startswith(prefix)]
    sub_ready = sum(1 for r in sub_results if r.get('publish_ready'))
    sub_total = len(sub_results)
    sub_manifest = {
        'ready_count': sub_ready,
        'total_tests': sub_total,
        'results': sub_results
    }
    with open(os.path.join(target_dir, 'publisher_readiness_manifest.json'), 'w') as mf:
        json.dump(sub_manifest, mf, indent=2)
    print(f'Synced {copied + 1} files to {target_dir} (ready_count={sub_ready}/{sub_total})')

print('=== SYNC COMPLETED SUCCESSFULLY ===')
