import os, shutil, json

mapping = {
    'p1': 'review_symbol_graph_rag_vs_qlora_swe_bench_lite',
    'p2': 'review_architectural_dynamics_long_12_page',
    'p3': 'autonomous_code_synthesis_and_self_healing_multi_agent_systems',
    'p4': 'review_enterprise_genai_roi',
    'p5': 'review_enterprise_adoption_of_multi_agent_ai_systems_infr'
}

master_p = 'papers/p'
manifest_path = os.path.join(master_p, 'publisher_readiness_manifest.json')
with open(manifest_path, 'r', encoding='utf-8') as f:
    master_manifest = json.load(f)

for folder, prefix in mapping.items():
    target = os.path.join('papers', folder)
    # Clear directory completely
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
        
    for fname in os.listdir(master_p):
        if fname.startswith(prefix):
            shutil.copyfile(os.path.join(master_p, fname), os.path.join(target, fname))
            
    sub_results = [r for r in master_manifest.get('results', []) if r.get('filename', '').startswith(prefix)]
    sub_ready = sum(1 for r in sub_results if r.get('publish_ready'))
    sub_total = len(sub_results)
    sub_manifest = {
        'ready_count': sub_ready,
        'total_tests': sub_total,
        'results': sub_results
    }
    with open(os.path.join(target, 'publisher_readiness_manifest.json'), 'w', encoding='utf-8') as mf:
        json.dump(sub_manifest, mf, indent=2)
    print(f"Synced {folder}: {len(os.listdir(target))} files (ready={sub_ready}/{sub_total})")
