import os, sys, glob, re, json

papers = sorted(glob.glob('vault/01_Papers/*.md'))
print(f"Total papers: {len(papers)}")

index = []
for p in papers:
    key = os.path.basename(p).replace('.md', '')
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
        
    title_m = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
    title = title_m.group(1).strip() if title_m else key
    
    author_m = re.search(r'authors:\s*\[(.*?)\]', content)
    authors = author_m.group(1).strip() if author_m else ""
    
    abstract_m = re.search(r'# Abstract\n+(.*?)(?=\n#|\Z)', content, re.DOTALL)
    abstract = abstract_m.group(1).strip() if abstract_m else ""
    
    index.append({
        'key': key,
        'title': title,
        'authors': authors,
        'abstract': abstract[:300]
    })

print(f"Indexed {len(index)} papers")
with open('vault/paper_index.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2)
