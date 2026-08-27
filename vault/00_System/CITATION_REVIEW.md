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

## Resolved automatically: 35 false attributions removed

These were not weak citations. In each, the prose named a paper, a system or
an author, and the key resolved to a different work entirely -- 'Adapter
layers' citing GPT-3, 'Paged attention' citing a sparse-autoencoder paper,
'Byzantine fault tolerance' citing one on fine-tuning CLIP. The citation was
deleted and the sentence left standing without attribution, which is the
honest state; supplying the correct source is authorship.

| Manuscript | Named in prose | Key | Resolved to |
|:---|:---|:---|:---|
| * | (whole key) | `doaj_001772c2113c476d9d5d40452c8e1` |  |
| * | (whole key) | `crossref_10.1145_3689096.3689462` |  |
| * | (whole key) | `pubmed_42380865` |  |
| * | (whole key) | `crossref_10.1109_access.2026.36563` |  |
| * | (whole key) | `arxiv_2404.01131` |  |
| * | (whole key) | `crossref_10.18653_v1_2026.findings` |  |
| * | (whole key) | `arxiv_2412.06333` |  |
| * | (whole key) | `arxiv_2010.11146` |  |
| * | (whole key) | `arxiv_2310.09270` |  |
| * | (whole key) | `arxiv_2411.15594` |  |
| * | (whole key) | `arxiv_2308.12898` |  |
| * | (whole key) | `arxiv_2203.02155` |  |
| * | (whole key) | `openalex_W4400993506` |  |
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

## Open: 43 occurrences needing an author decision

Keep, remove, or replace. To retire one without changing the draft, add a
`"decision": "keep"` entry for it in `citation_decisions.json`.

| Manuscript | Line | Score | Cited work | Citing context |
|:---|---:|---:|:---|:---|
| autonomous_code_synthesis_and_self | 27 | 0.082 | A Survey of Test-Time Compute: From Intuitiv | Repair convergence is measured over 300 seeded defects: the node-multiset distance to the  |
| autonomous_code_synthesis_and_self | 33 | 0.0812 | Language Models are Few-Shot Learners | Probabilistic generative models exhibit strong semantic reasoning but suffer hallucination |
| review_architectural_dynamics_long | 90 | 0.1201 | A Blueprint Architecture of Compound AI Syst | To reconcile high-capacity reasoning with hardware constraints, modern architectures incor |
| review_architectural_dynamics_long | 320 | 0.0856 | Self-Consistency Improves Chain of Thought R | The marginal benefit of additional test-time compute follows $\partial\text{Pass@}k/\parti |
| review_architectural_dynamics_long | 588 | 0.1936 | Direct Preference Optimization: Your Languag | Since $B$ is initialized to zero and $A$ is initialized with Gaussian noise, the early tra |
| review_architectural_dynamics_long | 934 | 0.018 | A Blueprint Architecture of Compound AI Syst | This fundamentally motivates parameter sparsity and quantization as efficiency levers — re |
| review_architectural_dynamics_long | 1068 | 0.1567 | Language Models are Few-Shot Learners | scaling laws [[arxiv_2005.14165]] established the foundational power-law framework |
| review_architectural_dynamics_long | 1068 | 0.2115 | Self-Consistency Improves Chain of Thought R | Subsequent work on test-time compute scaling [[arxiv_2203.11171]] established that inferen |
| review_architectural_dynamics_long | 1068 | 0.0544 | A Survey of Test-Time Compute: From Intuitiv | Recent analyses of emergent capabilities [[arxiv_2501.02497]] demonstrate discontinuous ju |
| review_architectural_dynamics_long | 1096 | 0.0169 | A Survey of Test-Time Compute: From Intuitiv | Extrapolation to frontier-scale training ($>10^{26}$ FLOPs) may encounter emergent capabil |
| review_composable_ai_systems_for_t | 50 | 0.0188 | Deliberative Technology for Alignment | However, prevailing industry deployments rely predominantly on monolithic prompt-chaining  |
| review_composable_ai_systems_for_t | 53 | 0.0128 | A Blueprint Architecture of Compound AI Syst | **Compounding Hallucination Cascades:** Unverified reasoning errors in early pipeline stag |
| review_composable_ai_systems_for_t | 54 | 0.0503 | A Survey of Test-Time Compute: From Intuitiv | **State Divergence & Race Conditions:** Unstructured shared scratchpads lack deterministic |
| review_composable_ai_systems_for_t | 67 | 0.0103 | A Survey of Test-Time Compute: From Intuitiv | **Lyapunov Stability and Error Propagation Theorems:** We prove that contract-gated verifi |
| review_composable_ai_systems_for_t | 565 | 0.2492 | MetaGPT: Meta Programming for A Multi-Agent  | Early multi-agent LLM systems—including AutoGPT, BabyAGI, MetaGPT [[crossref_10_48550_arxi |
| review_composable_ai_systems_for_t | 571 | 0.1343 | Direct Preference Optimization: Your Languag | CAS serves as the overarching architectural operating system uniting structured retrieval, |
| review_continual_safety_alignment_ | 169 | 0.0528 | Continual Safety Alignment via Gradient-Base | The harness, all 40 measurements and their artifacts are released so the account can be ch |
| review_enterprise_adoption_of_mult | 52 | 0.1001 | A Blueprint Architecture of Compound AI Syst | Economic Predictability and Unit Economics: Enterprise Total Cost of Ownership (TCO) requi |
| review_enterprise_adoption_of_mult | 68 | 0.1064 | A Survey of Multi-Agent Deep Reinforcement L | The choice of coordination topology fundamentally dictates message overhead, context windo |
| review_enterprise_adoption_of_mult | 168 | 0.2121 | A Blueprint Architecture of Compound AI Syst | Hierarchical decomposition localizes context: worker agents receive only task-relevant ins |
| review_enterprise_adoption_of_mult | 272 | 0.0751 | A Blueprint Architecture of Compound AI Syst | Let $N_{\text{agents}}$ be the count of participating agents, $L_{\text{prompt}}(a, t)$ be |
| review_enterprise_adoption_of_mult | 417 | 0.0236 | A Survey of Test-Time Compute: From Intuitiv | This theoretical derivation explains why hierarchical topologies achieve dramatic economic |
| review_enterprise_adoption_of_mult | 612 | 0.1742 | Designing for Human-Agent Alignment: Underst | Multi-agent deployments introduce unique enterprise attack vectors [[arxiv_2404.04289]]: |
| review_enterprise_adoption_of_mult | 629 | 0.1265 | SWE-agent: Agent-Computer Interfaces Enable  | Modern LLM-based multi-agent frameworks—including MetaGPT [[crossref_10_48550_arxiv_2308_0 |
| review_enterprise_genai_roi | 27 | 0.1328 | A Causal ROI Framework for Life Sciences Bud | A field in which roughly two-thirds of the published record reports no measurement cannot  |
| review_spatio_temporal_grounding_i | 48 | 0.2241 | A Blueprint Architecture of Compound AI Syst | Despite rapid advancements in Vision-Language Models (VLMs), modern architectures exhibit  |
| review_spatio_temporal_grounding_i | 48 | 0.1573 | Direct Preference Optimization: Your Languag | Standard VLM architectures project video streams by flattening sampled frames into a dense |
| review_spatio_temporal_grounding_i | 472 | 0.2222 | Direct Preference Optimization: Your Languag | where $\lambda_T > 0$ is a learnable dynamic velocity scaling factor calibrated during mul |
| review_spatio_temporal_grounding_i | 560 | 0.0122 | Direct Preference Optimization: Your Languag | Our DST-DR framework advances this lineage by replacing monolithic space-time blocks with  |
| review_spatio_temporal_grounding_i | 563 | 0.0815 | A Blueprint Architecture of Compound AI Syst | However, as proven in Theorem 1, uniform sequence scaling induces cross-modal attention co |
| review_spatio_temporal_grounding_i | 588 | 0.0707 | A Survey of Test-Time Compute: From Intuitiv | **Phase 4: World Models and Physical Dynamics Simulation:** Leveraging spatio-temporal vel |
| review_symbol_graph_rag_vs_qlora_s | 25 | 0.0238 | A Survey of Test-Time Compute: From Intuitiv | On this corpus the structural signal adds nothing that lexical matching has not already ca |
| review_symbol_graph_rag_vs_qlora_s | 37 | 0.1596 | A Blueprint Architecture of Compound AI Syst | However, parametric encoding compresses structured repository knowledge into distributed r |
| review_symbol_graph_rag_vs_qlora_s | 41 | 0.2163 | Self-Consistency Improves Chain of Thought R | The central empirical question we address is: *which paradigm better supports autonomous i |
| review_symbol_graph_rag_vs_qlora_s | 49 | 0.2439 | A Blueprint Architecture of Compound AI Syst | An empirical cost analysis quantifying training VRAM, inference latency, amortized per-tas |
| review_symbol_graph_rag_vs_qlora_s | 378 | 0.0606 | Prefix-Tuning: Optimizing Continuous Prompts | Across all PEFT variants, the fundamental limitation is parametric compression of structur |
| review_symbol_graph_rag_vs_qlora_s | 382 | 0.1009 | Foundations of GenIR | Dense retrieval (DPR, BM25) matches issue descriptions against code tokens via embedding s |
| review_symbol_graph_rag_vs_qlora_s | 382 | 0.1712 | CodeBERT: A Pre-Trained Model for Programmin | CodeBERT [[arxiv_2002.08155]] and GraphCodeBERT extend dense retrieval to incorporate stru |
| review_trustworthy_multi_agent_sys | 47 | 0.089 | Deliberative Technology for Alignment | However, current orchestrations remain fundamentally vulnerable to non-deterministic failu |
| review_trustworthy_multi_agent_sys | 50 | 0.0558 | A Blueprint Architecture of Compound AI Syst | Downstream agents uncritically cite these synthetic assertions as ground truth, leading th |
| review_trustworthy_multi_agent_sys | 52 | 0.0617 | Designing for Human-Agent Alignment: Underst | **Ungrounded State Mutations & Action Drift:** Agents executing tool invocations or modify |
| review_trustworthy_multi_agent_sys | 194 | 0.0423 | A Blueprint Architecture of Compound AI Syst | Let up to $f$ agents out of $n$ total council members be Byzantine (i.e., generating hallu |
| review_trustworthy_multi_agent_sys | 489 | 0.0228 | A Blueprint Architecture of Compound AI Syst | However, unconstrained debate is prone to sycophancy, majority-vote bias, and hallucinatio |
