# Citation Review

Citations flagged by `CitationRelevanceService` as having little topical
overlap with the sentence citing them. The scorer measures vocabulary, not
whether a source supports a claim, so this is triage and not a verdict: it
flags foundational citations whose relevance is contextual.

Decisions are recorded in `citation_decisions.json` and subtracted here, so
this list can reach zero. **No replacement is suggested.** Lexical similarity
cannot judge whether a source supports a claim, and when it was asked to try
it proposed replacing InstructGPT with a paper on fracture image captioning
(ERR-062, R62).

## Resolved automatically: 40 false attributions removed

These were not weak citations. In each, the prose named a paper, a system or
an author, and the key resolved to a different work entirely -- 'Adapter
layers' citing GPT-3, 'Paged attention' citing a sparse-autoencoder paper,
'Byzantine fault tolerance' citing one on fine-tuning CLIP. The citation was
deleted and the sentence left standing without attribution, which is the
honest state; supplying the correct source is authorship.

| Manuscript | Named in prose | Key | Resolved to |
|:---|:---|:---|:---|
| * | (whole key) | `arxiv_2010.11146` |  |
| * | (whole key) | `arxiv_2203.02155` |  |
| * | (whole key) | `arxiv_2308.12898` |  |
| * | (whole key) | `arxiv_2310.09270` |  |
| * | (whole key) | `arxiv_2404.01131` |  |
| * | (whole key) | `arxiv_2411.15594` |  |
| * | (whole key) | `arxiv_2412.06333` |  |
| * | (whole key) | `crossref_10.1109_access.2026.36563` |  |
| * | (whole key) | `crossref_10.1145_3689096.3689462` |  |
| * | (whole key) | `crossref_10.18653_v1_2026.findings` |  |
| * | (whole key) | `doaj_001772c2113c476d9d5d40452c8e1` |  |
| * | (whole key) | `openalex_W4400993506` |  |
| * | (whole key) | `pubmed_42380865` |  |
| * | (whole key) | `arxiv_2406.00584` |  |
| * | (whole key) | `arxiv_2501.02497` |  |
| * | (whole key) | `arxiv_2305.18290` |  |
| * | (whole key) | `arxiv_2005.14165` |  |
| * | (whole key) | `arxiv_2312.03893` |  |
| autonomous_code_synthesis_and_self | AST transformations | `crossref_10.1145_3689096.3689462` | Comparative Analysis of Deep Learning Models for Breast  |
| autonomous_code_synthesis_and_self | Classical APR | `arxiv_2010.11146` | A Decentralised Self-Healing Approach for Network Topolo |
| review_architectural_dynamics_long | Adapter layers | `arxiv_2005.14165` | Language Models are Few-Shot Learners |
| review_architectural_dynamics_long | Aghajanyan et al. | `arxiv_2208.14227` | CLUDA : Contrastive Learning in Unsupervised Domain Adap |
| review_architectural_dynamics_long | Chinchilla) | `arxiv_2005.14165` | Language Models are Few-Shot Learners |
| review_architectural_dynamics_long | Chinchilla) scaling law | `arxiv_2005.14165` | Language Models are Few-Shot Learners |
| review_architectural_dynamics_long | Expert choice routing | `arxiv_2404.01131` | GOV-REK: Governed Reward Engineering Kernels for Designi |
| review_architectural_dynamics_long | Mixtral 8×7B | `arxiv_2412.06333` | Augmenting the action space with conventions to improve  |
| review_architectural_dynamics_long | Paged attention | `arxiv_2406.04028` | Contrastive Sparse Autoencoders for Interpreting Plannin |
| review_architectural_dynamics_long | Switch Transformer | `arxiv_2412.06333` | Augmenting the action space with conventions to improve  |
| review_composable_ai_systems_for_t | SMT solvers | `arxiv_2404.01131` | GOV-REK: Governed Reward Engineering Kernels for Designi |
| review_enterprise_adoption_of_mult | GDPR, SEC Rule 17a-4) | `arxiv_2411.15594` | A Survey on LLM-as-a-Judge |
| review_spatio_temporal_grounding_i | Vision Transformer backbone | `arxiv_2010.11146` | A Decentralised Self-Healing Approach for Network Topolo |
| review_symbol_graph_rag_vs_qlora_s | Adapter layers | `arxiv_2005.14165` | Language Models are Few-Shot Learners |
| review_symbol_graph_rag_vs_qlora_s | Agentless systems | `arxiv_2501.02497` | A Survey of Test-Time Compute: From Intuitive Inference  |
| review_symbol_graph_rag_vs_qlora_s | Personalized PageRank diffusion | `crossref_10.1145_3689096.3689462` | Comparative Analysis of Deep Learning Models for Breast  |
| review_symbol_graph_rag_vs_qlora_s | Reward-guided agent orchestration | `crossref_10.1109_access.2026.36563` | Fine-Tuning CLIP With Dynamic Prompt Tuning and Cross-Mo |
| review_symbol_graph_rag_vs_qlora_s | Test-time compute scaling | `arxiv_2203.11171` | Self-Consistency Improves Chain of Thought Reasoning in  |
| review_trustworthy_multi_agent_sys | BT-CCP) | `crossref_10.1145_3689096.3689462` | Comparative Analysis of Deep Learning Models for Breast  |
| review_trustworthy_multi_agent_sys | Byzantine fault tolerance | `crossref_10.1109_access.2026.36563` | Fine-Tuning CLIP With Dynamic Prompt Tuning and Cross-Mo |
| review_trustworthy_multi_agent_sys | FactChecker verification linter | `arxiv_2404.01131` | GOV-REK: Governed Reward Engineering Kernels for Designi |
| review_trustworthy_multi_agent_sys | GPU tokens without convergence | `arxiv_2501.02497` | A Survey of Test-Time Compute: From Intuitive Inference  |

## Open: 0 occurrences needing an author decision

Keep, remove, or replace. To retire one without changing the draft, add a
`"decision": "keep"` entry for it in `citation_decisions.json`.

| Manuscript | Line | Score | Cited work | Citing context |
|:---|---:|---:|:---|:---|
