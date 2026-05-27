# Vault — Conventions & Schema Reference

This directory is the Obsidian knowledge base populated by the ResearchingOS agent pipeline. All files are plain Markdown with YAML frontmatter.

## Folder structure

| Folder | Contents | Written by |
| --- | --- | --- |
| `01_Papers/` | One note per ingested research paper | Lead Analyst agent |
| `02_Concepts/` | Concept pages for recurring topics / methods | Reserved (future) |
| `03_Debates/` | Council debate transcript + Chairman synthesis per topic | Chairman agent |
| `04_Drafts/` | Full journal-ready literature review draft per topic | Writer agent |

## Filename patterns

| Category | Pattern | Example |
| --- | --- | --- |
| Papers | `{source}_{id}.md` | `arxiv_2203.11171.md`, `openalex_W4221161695.md` |
| Concepts | `{slug}.md` | `self_consistency.md` |
| Debates | `debate_{topic_slug}.md` | `debate_llm_alignment.md` |
| Drafts | `review_{topic_slug}.md` | `review_llm_alignment.md` |

`source` is one of: `arxiv`, `openalex`, `semanticscholar`, `europepmc`, `crossref`, `dblp`, `pubmed`, `doaj`, `plos`, `hal`, `huggingface`, `github`.

Topic slugs are lowercased, non-alphanumeric characters stripped, spaces replaced with `_`, truncated at 50 characters.

## Required frontmatter — Papers (`01_Papers/`)

```yaml
---
title: "Full paper title"
authors:
  - "Author Name"
url: "https://..."
published: "YYYY-MM-DD"
citations: 1234
source: "arXiv"          # or "OpenAlex", "arXiv & OpenAlex" for merged results
id: "arxiv:2203.11171"   # source-prefixed canonical ID
tags:
  - "research-paper"
  - "topic-slug"
---
```

## Required frontmatter — Debates (`03_Debates/`)

```yaml
---
title: "Council Debate on <topic>"
topic: "<topic>"
type: "debate_summary"
tags:
  - "topic-slug"
  - "debate"
---
```

## Required frontmatter — Drafts (`04_Drafts/`)

```yaml
---
title: "Literature Review: <topic>"
topic: "<topic>"
status: "draft"
format: "IEEE/ACM markdown"
tags:
  - "topic-slug"
  - "literature-review"
  - "draft"
---
```

## Wiki-link conventions

Use Obsidian-style `[[target]]` links to cross-reference notes:

- **Paper → Paper**: `[[arxiv_2203.11171]]`
- **Paper → Concept**: `[[Self-Consistency]]`
- **Debate → Papers**: `[[arxiv_2203.11171|Wang et al., 2022]]`

The knowledge graph endpoint (`GET /api/vault/graph`) resolves these links into graph edges. Unresolved links (no matching filename or title) are ignored by the graph builder but preserved in the Markdown.

## Deduplication policy

The same paper often appears in multiple sources (arXiv + OpenAlex + DBLP). The pipeline deduplicates by **normalized lowercase title** before writing to disk — only the first occurrence is saved. Sources are merged into the `source` field (e.g., `"arXiv & OpenAlex"`). If you see multiple notes for the same paper under different IDs, delete the lower-quality stub and keep the one with the fullest content.

## Stub notes

Notes with `[MOCK RESPONSE from ...]` in their body were created in dry-run mode and contain no real analysis. Re-run the pipeline with a valid `GEMINI_API_KEY` to populate them.

## Paper note template

Copy this template when creating manual paper notes:

```markdown
---
title: ""
authors:
  - ""
url: ""
published: ""
citations: 0
source: ""
id: ""
tags:
  - "research-paper"
---

## Summary

## Hypotheses

## Methodology

## Datasets

## Results

## Limitations

## Links

-
```
