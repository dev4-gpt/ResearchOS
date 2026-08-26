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

## Resolved automatically: 22 false attributions removed

These were not weak citations. In each, the prose named a paper, a system or
an author, and the key resolved to a different work entirely -- 'Adapter
layers' citing GPT-3, 'Paged attention' citing a sparse-autoencoder paper,
'Byzantine fault tolerance' citing one on fine-tuning CLIP. The citation was
deleted and the sentence left standing without attribution, which is the
honest state; supplying the correct source is authorship.

| Manuscript | Named in prose | Key | Resolved to |
|:---|:---|:---|:---|
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

## Open: 83 occurrences needing an author decision

Keep, remove, or replace. To retire one without changing the draft, add a
`"decision": "keep"` entry for it in `citation_decisions.json`.

| Manuscript | Line | Score | Cited work | Citing context |
|:---|---:|---:|:---|:---|
| autonomous_code_synthesis_and_self | 26 | 0.082 | A Survey of Test-Time Compute: From Intuitiv | Repair convergence is measured over 300 seeded defects: the node-multiset distance to the  |
| autonomous_code_synthesis_and_self | 32 | 0.0732 | A Decentralised Self-Healing Approach for Ne | Traditional Automated Program Repair (APR) methodologies operate via heuristic search over |
| autonomous_code_synthesis_and_self | 32 | 0.1095 | GOV-REK: Governed Reward Engineering Kernels | Symbolic solvers provide formal correctness guarantees but are constrained by state-space  |
| autonomous_code_synthesis_and_self | 32 | 0.0812 | Language Models are Few-Shot Learners | Probabilistic generative models exhibit strong semantic reasoning but suffer hallucination |
| autonomous_code_synthesis_and_self | 460 | 0.0713 | DICA: Dual-Indicator Guided Contrastive Alig | In our mutation study this grammatical and binding stage carries essentially the whole fil |
| autonomous_code_synthesis_and_self | 643 | 0.1012 | Augmenting the action space with conventions | **Orchestrator Agent**: Manages the repair loop, tracks energy $V(T)$, selects repair acti |
| autonomous_code_synthesis_and_self | 652 | 0.1586 | Augmenting the action space with conventions | - **Hierarchical MAS (H-MAS)**: Two-tier architecture with a high-level Planner agent deco |
| autonomous_code_synthesis_and_self | 858 | 0.2293 | GOV-REK: Governed Reward Engineering Kernels | SMT solver integration (Z3, CVC5) enables path-sensitive program analysis for loop invaria |
| autonomous_code_synthesis_and_self | 858 | 0.2408 | DICA: Dual-Indicator Guided Contrastive Alig | Neural-guided formal synthesis [[crossref_10.18653_v1_2026.findings-acl.1933]] combines LL |
| review_architectural_dynamics_long | 22 | 0.0557 | GOV-REK: Governed Reward Engineering Kernels | We give exact closed-form KV-cache arithmetic and evaluate it across attention variants: a |
| review_architectural_dynamics_long | 85 | 0.0602 | Augmenting the action space with conventions | To reconcile high-capacity reasoning with hardware constraints, modern architectures incor |
| review_architectural_dynamics_long | 85 | 0.1201 | A Blueprint Architecture of Compound AI Syst | To reconcile high-capacity reasoning with hardware constraints, modern architectures incor |
| review_architectural_dynamics_long | 299 | 0.0856 | Self-Consistency Improves Chain of Thought R | The marginal benefit of additional test-time compute follows $\partial\text{Pass@}k/\parti |
| review_architectural_dynamics_long | 547 | 0.1936 | Direct Preference Optimization: Your Languag | Since $B$ is initialized to zero and $A$ is initialized with Gaussian noise, the early tra |
| review_architectural_dynamics_long | 752 | 0.0821 | Augmenting the action space with conventions | For Mixtral 8×7B ($E = 8$, $k = 2$): active params $\approx 12.8$B out of 46.7B total — a  |
| review_architectural_dynamics_long | 869 | 0.018 | A Blueprint Architecture of Compound AI Syst | This fundamentally motivates parameter sparsity and quantization as efficiency levers — re |
| review_architectural_dynamics_long | 999 | 0.1567 | Language Models are Few-Shot Learners | scaling laws [[arxiv_2005.14165]] established the foundational power-law framework |
| review_architectural_dynamics_long | 999 | 0.2115 | Self-Consistency Improves Chain of Thought R | Subsequent work on test-time compute scaling [[arxiv_2203.11171]] established that inferen |
| review_architectural_dynamics_long | 999 | 0.0544 | A Survey of Test-Time Compute: From Intuitiv | Recent analyses of emergent capabilities [[arxiv_2501.02497]] demonstrate discontinuous ju |
| review_architectural_dynamics_long | 1011 | 0.1992 | Retro-fallback: retrosynthetic planning in a | RETRO [[arxiv_2310.09270]] demonstrates that retrieval-augmented training can reduce model |
| review_architectural_dynamics_long | 1019 | 0.0933 | Research Ethics Committees (RECs) perspectiv | Vendor specifications report HBM bandwidth of 2.4 TB/s for TPU v5e against 3.35 TB/s for H |
| review_architectural_dynamics_long | 1023 | 0.1338 | Raman Spectroscopy Pre-Trained Encoder: A Se | Production workload distributions differ significantly in sequence length distribution, do |
| review_architectural_dynamics_long | 1027 | 0.0169 | A Survey of Test-Time Compute: From Intuitiv | Extrapolation to frontier-scale training ($>10^{26}$ FLOPs) may encounter emergent capabil |
| review_composable_ai_systems_for_t | 49 | 0.0188 | Deliberative Technology for Alignment | However, prevailing industry deployments rely predominantly on monolithic prompt-chaining  |
| review_composable_ai_systems_for_t | 52 | 0.0128 | A Blueprint Architecture of Compound AI Syst | **Compounding Hallucination Cascades:** Unverified reasoning errors in early pipeline stag |
| review_composable_ai_systems_for_t | 53 | 0.0503 | A Survey of Test-Time Compute: From Intuitiv | **State Divergence & Race Conditions:** Unstructured shared scratchpads lack deterministic |
| review_composable_ai_systems_for_t | 66 | 0.0103 | A Survey of Test-Time Compute: From Intuitiv | **Lyapunov Stability and Error Propagation Theorems:** We prove that contract-gated verifi |
| review_composable_ai_systems_for_t | 233 | 0.0865 | DICA: Dual-Indicator Guided Contrastive Alig | If this condition holds, the composite contract guarantees end-to-end type safety and sema |
| review_composable_ai_systems_for_t | 465 | 0.1317 | GOV-REK: Governed Reward Engineering Kernels | Invalid messages trigger immediate deterministic recovery actions (e.g., fallback routing  |
| review_composable_ai_systems_for_t | 468 | 0.1655 | Fine-Tuning CLIP With Dynamic Prompt Tuning  | A proposal $P$ is approved if and only if $\sum_{i=1}^N w_i \cdot \mathbb{I}(\text{Verify} |
| review_composable_ai_systems_for_t | 536 | 0.2492 | MetaGPT: Meta Programming for A Multi-Agent  | Early multi-agent LLM systems—including AutoGPT, BabyAGI, MetaGPT [[crossref_10_48550_arxi |
| review_composable_ai_systems_for_t | 539 | 0.1226 | DICA: Dual-Indicator Guided Contrastive Alig | The integration of SMT solvers (Z3, CVC5) with neural architectures has a rich history in  |
| review_composable_ai_systems_for_t | 539 | 0.0767 | GOV-REK: Governed Reward Engineering Kernels | Our CAS framework extends formal methods to agent orchestration graphs, using SMT solvers  |
| review_composable_ai_systems_for_t | 542 | 0.1343 | Direct Preference Optimization: Your Languag | CAS serves as the overarching architectural operating system uniting structured retrieval, |
| review_composable_ai_systems_for_t | 562 | 0.1898 | Fine-Tuning CLIP With Dynamic Prompt Tuning  | **Asynchronous Byzantine Pipeline Consensus:** Scaling Tier 4 consensus algorithms to supp |
| review_continual_safety_alignment_ | 168 | 0.0528 | Continual Safety Alignment via Gradient-Base | The harness, all 40 measurements and their artifacts are released so the account can be ch |
| review_enterprise_adoption_of_mult | 51 | 0.1001 | A Blueprint Architecture of Compound AI Syst | Economic Predictability and Unit Economics: Enterprise Total Cost of Ownership (TCO) requi |
| review_enterprise_adoption_of_mult | 67 | 0.1064 | A Survey of Multi-Agent Deep Reinforcement L | The choice of coordination topology fundamentally dictates message overhead, context windo |
| review_enterprise_adoption_of_mult | 111 | 0.08 | Augmenting the action space with conventions | As $N$ scales beyond 6 agents, context windows become rapidly saturated with redundant int |
| review_enterprise_adoption_of_mult | 155 | 0.2121 | A Blueprint Architecture of Compound AI Syst | Hierarchical decomposition localizes context: worker agents receive only task-relevant ins |
| review_enterprise_adoption_of_mult | 199 | 0 | Comparative Analysis of Deep Learning Models | where $|K|$ is the cardinality of the knowledge base [[crossref_10.1145_3689096.3689462]]. |
| review_enterprise_adoption_of_mult | 247 | 0.0751 | A Blueprint Architecture of Compound AI Syst | Let $N_{\text{agents}}$ be the count of participating agents, $L_{\text{prompt}}(a, t)$ be |
| review_enterprise_adoption_of_mult | 374 | 0.0236 | A Survey of Test-Time Compute: From Intuitiv | This theoretical derivation explains why hierarchical topologies achieve dramatic economic |
| review_enterprise_adoption_of_mult | 555 | 0.0736 | Comparative Analysis of Deep Learning Models | Establishing that this translates into lower wall-clock recovery requires a deployed syste |
| review_enterprise_adoption_of_mult | 563 | 0.1742 | Designing for Human-Agent Alignment: Underst | Multi-agent deployments introduce unique enterprise attack vectors [[arxiv_2404.04289]]: |
| review_enterprise_adoption_of_mult | 571 | 0.0665 | Raman Spectroscopy Pre-Trained Encoder: A Se | - Layer 1 (Ephemeral Namespace Sandboxing): All tool-executing agents run in isolated gVis |
| review_enterprise_adoption_of_mult | 572 | 0.0676 | Research Ethics Committees (RECs) perspectiv | - Layer 2 (Cryptographic JWT RBAC Tokens): Inter-agent requests must carry short-lived (60 |
| review_enterprise_adoption_of_mult | 580 | 0.1265 | SWE-agent: Agent-Computer Interfaces Enable  | Modern LLM-based multi-agent frameworks—including MetaGPT [[crossref_10_48550_arxiv_2308_0 |
| review_enterprise_adoption_of_mult | 612 | 0.2206 | Fine-Tuning CLIP With Dynamic Prompt Tuning  | Federated Cross-Enterprise Agent Swarms: Secure multi-party computation (SMPC) protocols e |
| review_enterprise_genai_roi | 26 | 0.1328 | A Causal ROI Framework for Life Sciences Bud | A field in which roughly two-thirds of the published record reports no measurement cannot  |
| review_enterprise_genai_roi | 28 | 0.2375 | Customer journey optimisation using large la | This review conducted no survey of its own and reports no enterprise deployment count [[op |
| review_enterprise_genai_roi | 234 | 0 | Customer journey optimisation using large la | [[openalex_W4400993506]] |
| review_spatio_temporal_grounding_i | 47 | 0.2241 | A Blueprint Architecture of Compound AI Syst | Despite rapid advancements in Vision-Language Models (VLMs), modern architectures exhibit  |
| review_spatio_temporal_grounding_i | 47 | 0.1573 | Direct Preference Optimization: Your Languag | Standard VLM architectures project video streams by flattening sampled frames into a dense |
| review_spatio_temporal_grounding_i | 443 | 0.2222 | Direct Preference Optimization: Your Languag | where $\lambda_T > 0$ is a learnable dynamic velocity scaling factor calibrated during mul |
| review_spatio_temporal_grounding_i | 527 | 0.0122 | Direct Preference Optimization: Your Languag | Our DST-DR framework advances this lineage by replacing monolithic space-time blocks with  |
| review_spatio_temporal_grounding_i | 530 | 0.0815 | A Blueprint Architecture of Compound AI Syst | However, as proven in Theorem 1, uniform sequence scaling induces cross-modal attention co |
| review_spatio_temporal_grounding_i | 544 | 0.2118 | Comparative Analysis of Deep Learning Models | Full-length feature films ($>90$ minutes) require hierarchical long-term memory synthesis  |
| review_spatio_temporal_grounding_i | 552 | 0.0415 | A Decentralised Self-Healing Approach for Ne | **Phase 1: Native Continuous Spatio-Temporal Tokenizers:** Replacing discrete frame sampli |
| review_spatio_temporal_grounding_i | 554 | 0.079 | Raman Spectroscopy Pre-Trained Encoder: A Se | **Phase 3: Real-Time Streaming Video Reasoning:** Adapting DST-DR for zero-latency online  |
| review_spatio_temporal_grounding_i | 555 | 0.0707 | A Survey of Test-Time Compute: From Intuitiv | **Phase 4: World Models and Physical Dynamics Simulation:** Leveraging spatio-temporal vel |
| review_symbol_graph_rag_vs_qlora_s | 24 | 0.0238 | A Survey of Test-Time Compute: From Intuitiv | On this corpus the structural signal adds nothing that lexical matching has not already ca |
| review_symbol_graph_rag_vs_qlora_s | 36 | 0.1596 | A Blueprint Architecture of Compound AI Syst | However, parametric encoding compresses structured repository knowledge into distributed r |
| review_symbol_graph_rag_vs_qlora_s | 40 | 0.2163 | Self-Consistency Improves Chain of Thought R | The central empirical question we address is: *which paradigm better supports autonomous i |
| review_symbol_graph_rag_vs_qlora_s | 47 | 0.0968 | Can Linguistic Knowledge Improve Multimodal  | A hyperparameter study over the diffusion's damping factor and seed breadth, selected on a |
| review_symbol_graph_rag_vs_qlora_s | 48 | 0.2439 | A Blueprint Architecture of Compound AI Syst | An empirical cost analysis quantifying training VRAM, inference latency, amortized per-tas |
| review_symbol_graph_rag_vs_qlora_s | 347 | 0.0606 | Prefix-Tuning: Optimizing Continuous Prompts | Across all PEFT variants, the fundamental limitation is parametric compression of structur |
| review_symbol_graph_rag_vs_qlora_s | 351 | 0.1009 | Foundations of GenIR | Dense retrieval (DPR, BM25) matches issue descriptions against code tokens via embedding s |
| review_symbol_graph_rag_vs_qlora_s | 351 | 0.1712 | CodeBERT: A Pre-Trained Model for Programmin | CodeBERT [[arxiv_2002.08155]] and GraphCodeBERT extend dense retrieval to incorporate stru |
| review_symbol_graph_rag_vs_qlora_s | 359 | 0.1665 | DICA: Dual-Indicator Guided Contrastive Alig | Symbol-Graph RAG provides a natural retrieval backbone for such multi-agent architectures, |
| review_symbol_graph_rag_vs_qlora_s | 367 | 0.2038 | Training language models to follow instructi | Cross-validation on the 300 test tasks was not performed to avoid overfitting [[arxiv_2203 |
| review_symbol_graph_rag_vs_qlora_s | 371 | 0.0974 | Raman Spectroscopy Pre-Trained Encoder: A Se | Generalizability to statically-typed languages (C++, Java, Rust) with more complex module  |
| review_symbol_graph_rag_vs_qlora_s | 371 | 0.0908 | A Survey on LLM-as-a-Judge | Ultra-large monorepos ($>10^6$ LOC) may require hierarchical graph partitioning strategies |
| review_trustworthy_multi_agent_sys | 36 | 0.0569 | GOV-REK: Governed Reward Engineering Kernels | Byzantine agreement is simulated over an unreliable channel ($95\%$ message delivery, $20{ |
| review_trustworthy_multi_agent_sys | 46 | 0.089 | Deliberative Technology for Alignment | However, current orchestrations remain fundamentally vulnerable to non-deterministic failu |
| review_trustworthy_multi_agent_sys | 49 | 0.0558 | A Blueprint Architecture of Compound AI Syst | Downstream agents uncritically cite these synthetic assertions as ground truth, leading th |
| review_trustworthy_multi_agent_sys | 51 | 0.0617 | Designing for Human-Agent Alignment: Underst | **Ungrounded State Mutations & Action Drift:** Agents executing tool invocations or modify |
| review_trustworthy_multi_agent_sys | 185 | 0.0423 | A Blueprint Architecture of Compound AI Syst | Let up to $f$ agents out of $n$ total council members be Byzantine (i.e., generating hallu |
| review_trustworthy_multi_agent_sys | 353 | 0.0559 | Augmenting the action space with conventions | If rebuttal turns exceed $k_{\max} = 3$, the Chairman agent is granted unilateral synthesi |
| review_trustworthy_multi_agent_sys | 468 | 0.0228 | A Blueprint Architecture of Compound AI Syst | However, unconstrained debate is prone to sycophancy, majority-vote bias, and hallucinatio |
| review_trustworthy_multi_agent_sys | 471 | 0.0744 | DICA: Dual-Indicator Guided Contrastive Alig | Linear Temporal Logic (LTL) and Computation Tree Logic (CTL) model checking have been wide |
| review_trustworthy_multi_agent_sys | 471 | 0.1252 | GOV-REK: Governed Reward Engineering Kernels | Recent literature investigates neuro-symbolic reasoning and SMT constraint solving for neu |
| review_trustworthy_multi_agent_sys | 494 | 0.2001 | Fine-Tuning CLIP With Dynamic Prompt Tuning  | **Decentralized Multi-Agent DAO Governance:** Integrating smart contract protocols on ente |
