# Citation Review List

Citations flagged by `CitationRelevanceService` as having little or no topical
overlap with the sentence citing them. This is a triage signal, not a verdict:
the scorer measures vocabulary, not whether a source supports a claim, and it
flags foundational citations (InstructGPT, GPT-3) whose relevance is contextual.

Mis-keyed citations -- where the prose names one paper and the key resolved to
another -- have already been repointed automatically; those were unambiguous
errors. What remains here needs an author decision: keep, replace, or remove.

| Manuscript | Line | Score | Cited work | Citing context |
|:---|---:|---:|:---|:---|
| autonomous_code_synthesis_and_self | 26 | 0.082 | A Survey of Test-Time Compute: From Intuitive  | Repair convergence is measured over 300 seeded defects: the node-multiset distance to the  |
| autonomous_code_synthesis_and_self | 32 | 0.0732 | A Decentralised Self-Healing Approach for Netw | Traditional Automated Program Repair (APR) methodologies operate via heuristic search over |
| autonomous_code_synthesis_and_self | 32 | 0.0812 | Language Models are Few-Shot Learners | Probabilistic generative models exhibit strong semantic reasoning but suffer hallucination |
| autonomous_code_synthesis_and_self | 316 | 0.0713 | DICA: Dual-Indicator Guided Contrastive Alignm | In our mutation study this grammatical and binding stage carries essentially the whole fil |
| autonomous_code_synthesis_and_self | 595 | 0.0217 | A Decentralised Self-Healing Approach for Netw | Classical APR [[arxiv_2010.11146]] applies heuristic search over syntax tree mutation oper |
| review_architectural_dynamics_long | 22 | 0.0556 | GOV-REK: Governed Reward Engineering Kernels f | We give exact closed-form KV-cache arithmetic and evaluate it across attention variants: a |
| review_architectural_dynamics_long | 28 | 0.0 | Generative AI for Enterprise AI | No accelerator was used, no model was trained, and no throughput or realised-VRAM measurem |
| review_architectural_dynamics_long | 69 | 0.0602 | Augmenting the action space with conventions t | To reconcile high-capacity reasoning with hardware constraints, modern architectures incor |
| review_architectural_dynamics_long | 219 | 0.0856 | Self-Consistency Improves Chain of Thought Rea | The marginal benefit of additional test-time compute follows $\partial\text{Pass@}k/\parti |
| review_architectural_dynamics_long | 323 | 0.0553 | CLUDA : Contrastive Learning in Unsupervised D | [[arxiv_2208.14227]] empirically demonstrate $\rho \leq 8$ for most NLP fine-tuning tasks, |
| review_architectural_dynamics_long | 528 | 0.0821 | Augmenting the action space with conventions t | For Mixtral 8×7B ($E = 8$, $k = 2$): active params $\approx 12.8$B out of 46.7B total — a  |
| review_architectural_dynamics_long | 579 | 0.031 | Contrastive Sparse Autoencoders for Interpreti | Paged attention [[arxiv_2406.04028]] addresses fragmentation but does not reduce the asymp |
| review_architectural_dynamics_long | 613 | 0.018 | A Blueprint Architecture of Compound AI System | This fundamentally motivates parameter sparsity and quantization as efficiency levers — re |
| review_architectural_dynamics_long | 727 | 0.0544 | A Survey of Test-Time Compute: From Intuitive  | Recent analyses of emergent capabilities [[arxiv_2501.02497]] demonstrate discontinuous ju |
| review_architectural_dynamics_long | 735 | 0.0852 | Augmenting the action space with conventions t | Switch Transformer [[arxiv_2412.06333]] demonstrated that MoE scaling enables $4\times$ pa |
| review_architectural_dynamics_long | 735 | 0.0511 | Augmenting the action space with conventions t | Mixtral 8×7B [[arxiv_2412.06333]] validated MoE efficiency at open-source scale, achieving |
| review_architectural_dynamics_long | 735 | 0.0561 | GOV-REK: Governed Reward Engineering Kernels f | Expert choice routing [[arxiv_2404.01131]] reverses the routing direction (experts select  |
| review_architectural_dynamics_long | 747 | 0.0933 | Research Ethics Committees (RECs) perspectives | Vendor specifications report HBM bandwidth of 2.4 TB/s for TPU v5e against 3.35 TB/s for H |
| review_architectural_dynamics_long | 755 | 0.0169 | A Survey of Test-Time Compute: From Intuitive  | Extrapolation to frontier-scale training ($>10^{26}$ FLOPs) may encounter emergent capabil |
| review_composable_ai_systems_for_t | 33 | 0.0518 | A Survey of Test-Time Compute: From Intuitive  | We formalize an algebraic contract calculus $\langle \mathcal{I}, \mathcal{O}, \Phi_{\text |
| review_composable_ai_systems_for_t | 41 | 0.0188 | Deliberative Technology for Alignment | However, prevailing industry deployments rely predominantly on monolithic prompt-chaining  |
| review_composable_ai_systems_for_t | 44 | 0.0128 | A Blueprint Architecture of Compound AI System | **Compounding Hallucination Cascades:** Unverified reasoning errors in early pipeline stag |
| review_composable_ai_systems_for_t | 45 | 0.0503 | A Survey of Test-Time Compute: From Intuitive  | **State Divergence & Race Conditions:** Unstructured shared scratchpads lack deterministic |
| review_composable_ai_systems_for_t | 58 | 0.0103 | A Survey of Test-Time Compute: From Intuitive  | **Lyapunov Stability and Error Propagation Theorems:** We prove that contract-gated verifi |
| review_composable_ai_systems_for_t | 177 | 0.0865 | DICA: Dual-Indicator Guided Contrastive Alignm | If this condition holds, the composite contract guarantees end-to-end type safety and sema |
| review_composable_ai_systems_for_t | 358 | 0.0274 | A Survey of Test-Time Compute: From Intuitive  | **Financial Compliance & Regulatory Auditing ($N = 2,200$):** Multi-hop document extractio |
| review_composable_ai_systems_for_t | 359 | 0.0 | Generative AI for Enterprise AI | **Distributed Clinical Pathway Synthesis ($N = 2,000$):** Electronic health record synthes |
| review_composable_ai_systems_for_t | 360 | 0.0566 | A Blueprint Architecture of Compound AI System | **Autonomous Cloud Infrastructure Remediation ($N = 2,000$):** Live Kubernetes microservic |
| review_composable_ai_systems_for_t | 366 | 0.0777 | Augmenting the action space with conventions t | - **Unconstrained Multi-Agent (Baseline 2):** Standard AutoGPT-style peer-to-peer agent ne |
| review_composable_ai_systems_for_t | 458 | 0.0767 | GOV-REK: Governed Reward Engineering Kernels f | Our CAS framework extends formal methods to agent orchestration graphs, using SMT solvers  |
| review_continual_safety_alignment_ | 38 | 0.0768 | Training language models to follow instruction | Vision-Language Models (VLMs) combining high-capacity vision encoders (e.g., Vision Transf |
| review_continual_safety_alignment_ | 38 | 0.0438 | Deliberative Technology for Alignment | As these foundation models transition into regulated real-world environments—such as clini |
| review_continual_safety_alignment_ | 43 | 0.0133 | A Blueprint Architecture of Compound AI System | Safety Alignment ($\mathcal{D}_{\text{safe}}$): Reinforcement Learning from Human Feedback |
| review_continual_safety_alignment_ | 46 | 0.0807 | A Survey of Test-Time Compute: From Intuitive  | When a safety-aligned model is adapted to new task distributions, the acquired safety beha |
| review_continual_safety_alignment_ | 127 | 0.0237 | A Blueprint Architecture of Compound AI System | - Assumption 1 (Subspace Orthogonality Deficit): Safety representations and task-specific  |
| review_continual_safety_alignment_ | 129 | 0.0426 | Transforming Software Development with Generat | - Assumption 3 (Cross-Modal Vulnerability Amplification): Visual conditioning vectors $W_{ |
| review_continual_safety_alignment_ | 180 | 0.0773 | Can Linguistic Knowledge Improve Multimodal Al | Parameter-Isolated Adaptation (PEFT): Confining downstream updates to low-rank adapters (L |
| review_continual_safety_alignment_ | 181 | 0.0337 | GOV-REK: Governed Reward Engineering Kernels f | Regularization & Gradient Surgery: Projecting downstream task gradients orthogonally to sa |
| review_continual_safety_alignment_ | 182 | 0.033 | Contrastive Sparse Autoencoders for Interpreti | Experience Replay & Memory Buffers: Interleaving downstream task batches with historical s |
| review_continual_safety_alignment_ | 241 | 0.0467 | A Blueprint Architecture of Compound AI System | - VLGuard [[arxiv_2406.00584]]: 2,000 safe and unsafe image-text instruction pairs evaluat |
| review_continual_safety_alignment_ | 243 | 0.0179 | Can Linguistic Knowledge Improve Multimodal Al | - AdvVQA [[arxiv_2308.12898]]: 3,500 visually perturbed question-answering probes designed |
| review_continual_safety_alignment_ | 250 | 0.04 | Contrastive Sparse Autoencoders for Interpreti | Dark Experience Replay (DER++): Replaying $10\%$ historical safety alignment batches durin |
| review_continual_safety_alignment_ | 251 | 0.0349 | GOV-REK: Governed Reward Engineering Kernels f | Gradient Projection Memory (GPM): Projecting task gradients orthogonally to principal safe |
| review_continual_safety_alignment_ | 317 | 0.0153 | A Blueprint Architecture of Compound AI System | A persistent controversy in generative AI deployment is the so-called "safety tax"—the obs |
| review_enterprise_adoption_of_mult | 49 | 0.0343 | A Survey on LLM-as-a-Judge | Deterministic Governance and Auditing: Every agent decision, intermediate tool invocation, |
| review_enterprise_adoption_of_mult | 56 | 0.0506 | Generative AI for Enterprise AI | Reproducible Topology Benchmark: A simulation harness measuring message complexity, cascad |
| review_enterprise_adoption_of_mult | 95 | 0.08 | Augmenting the action space with conventions t | As $N$ scales beyond 6 agents, context windows become rapidly saturated with redundant int |
| review_enterprise_adoption_of_mult | 183 | 0.0752 | A Blueprint Architecture of Compound AI System | Let $N_{\text{agents}}$ be the count of participating agents, $L_{\text{prompt}}(a, t)$ be |
| review_enterprise_adoption_of_mult | 262 | 0.0236 | A Survey of Test-Time Compute: From Intuitive  | This theoretical derivation explains why hierarchical topologies achieve dramatic economic |
| review_enterprise_adoption_of_mult | 389 | 0.0736 | Comparative Analysis of Deep Learning Models f | Establishing that this translates into lower wall-clock recovery requires a deployed syste |
| review_enterprise_adoption_of_mult | 405 | 0.0665 | Raman Spectroscopy Pre-Trained Encoder: A Self | - Layer 1 (Ephemeral Namespace Sandboxing): All tool-executing agents run in isolated gVis |
| review_enterprise_adoption_of_mult | 406 | 0.0709 | Research Ethics Committees (RECs) perspectives | - Layer 2 (Cryptographic JWT RBAC Tokens): Inter-agent requests must carry short-lived (60 |
| review_spatio_temporal_grounding_i | 33 | 0.0368 | A Survey of Test-Time Compute: From Intuitive  | We mathematically formalize the cross-modal attention collapse theorem, proving that high  |
| review_spatio_temporal_grounding_i | 33 | 0.0274 | Generative AI for Enterprise AI | Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR  |
| review_spatio_temporal_grounding_i | 43 | 0.0577 | A Survey of Test-Time Compute: From Intuitive  | Consequently, standard softmax attention distributions assign overwhelming mass to static  |
| review_spatio_temporal_grounding_i | 62 | 0.0135 | A Decentralised Self-Healing Approach for Netw | Let a video stream $V$ be represented as a sequence of $T$ uniformly sampled frames $X_v = |
| review_spatio_temporal_grounding_i | 385 | 0.0334 | A Decentralised Self-Healing Approach for Netw | \| **MSVD-QA** [[arxiv_2010.11146]] \| Short action clips \| 4,200 \| 10 s \| Action recognitio |
| review_spatio_temporal_grounding_i | 397 | 0.0261 | Direct Preference Optimization: Your Language  | **Frame-Averaging VLM:** LLaVA-1.5 applied to temporal mean-pooled visual features [[arxiv |
| review_spatio_temporal_grounding_i | 399 | 0.092 | A Decentralised Self-Healing Approach for Netw | **TimeSformer Factorized:** Divided space-time attention blocks [[arxiv_2010.11146]]. |
| review_spatio_temporal_grounding_i | 444 | 0.0272 | Training language models to follow instruction | This confirms that DST-DR directly rectifies the temporal attention collapse identified in |
| review_spatio_temporal_grounding_i | 485 | 0.0122 | Direct Preference Optimization: Your Language  | Our DST-DR framework advances this lineage by replacing monolithic space-time blocks with  |
| review_spatio_temporal_grounding_i | 488 | 0.0815 | A Blueprint Architecture of Compound AI System | However, as proven in Theorem 1, uniform sequence scaling induces cross-modal attention co |
| review_spatio_temporal_grounding_i | 491 | 0.0 | Generative AI for Enterprise AI | Our orthogonal projection algebra applies dynamic routing principles to multimodal video t |
| review_spatio_temporal_grounding_i | 510 | 0.0415 | A Decentralised Self-Healing Approach for Netw | **Phase 1: Native Continuous Spatio-Temporal Tokenizers:** Replacing discrete frame sampli |
| review_spatio_temporal_grounding_i | 512 | 0.079 | Raman Spectroscopy Pre-Trained Encoder: A Self | **Phase 3: Real-Time Streaming Video Reasoning:** Adapting DST-DR for zero-latency online  |
| review_spatio_temporal_grounding_i | 513 | 0.0707 | A Survey of Test-Time Compute: From Intuitive  | **Phase 4: World Models and Physical Dynamics Simulation:** Leveraging spatio-temporal vel |
| review_symbol_graph_rag_vs_qlora_s | 24 | 0.0238 | A Survey of Test-Time Compute: From Intuitive  | On this corpus the structural signal adds nothing that lexical matching has not already ca |
| review_symbol_graph_rag_vs_qlora_s | 26 | 0.0782 | Generative AI for Enterprise AI | Retrieval difficulty on that benchmark is therefore lower than a repository-scale framing  |
| review_symbol_graph_rag_vs_qlora_s | 47 | 0.0968 | Can Linguistic Knowledge Improve Multimodal Al | A hyperparameter study over the diffusion's damping factor and seed breadth, selected on a |
| review_symbol_graph_rag_vs_qlora_s | 241 | 0.0371 | Language Models are Few-Shot Learners | Adapter layers [[arxiv_2005.14165]] insert small bottleneck modules between transformer la |
| review_symbol_graph_rag_vs_qlora_s | 241 | 0.0606 | Prefix-Tuning: Optimizing Continuous Prompts f | Across all PEFT variants, the fundamental limitation is parametric compression of structur |
| review_symbol_graph_rag_vs_qlora_s | 265 | 0.0974 | Raman Spectroscopy Pre-Trained Encoder: A Self | Generalizability to statically-typed languages (C++, Java, Rust) with more complex module  |
| review_symbol_graph_rag_vs_qlora_s | 265 | 0.0908 | A Survey on LLM-as-a-Judge | Ultra-large monorepos ($>10^6$ LOC) may require hierarchical graph partitioning strategies |
| review_trustworthy_multi_agent_sys | 36 | 0.0569 | GOV-REK: Governed Reward Engineering Kernels f | Byzantine agreement is simulated over an unreliable channel ($95\%$ message delivery, $20{ |
| review_trustworthy_multi_agent_sys | 46 | 0.089 | Deliberative Technology for Alignment | However, current orchestrations remain fundamentally vulnerable to non-deterministic failu |
| review_trustworthy_multi_agent_sys | 49 | 0.0558 | A Blueprint Architecture of Compound AI System | Downstream agents uncritically cite these synthetic assertions as ground truth, leading th |
| review_trustworthy_multi_agent_sys | 50 | 0.0586 | A Survey of Test-Time Compute: From Intuitive  | **Circular Deadlocks and Non-Terminating Livelocks:** Symmetrical persona conflicts (e.g., |
| review_trustworthy_multi_agent_sys | 51 | 0.0617 | Designing for Human-Agent Alignment: Understan | **Ungrounded State Mutations & Action Drift:** Agents executing tool invocations or modify |
| review_trustworthy_multi_agent_sys | 63 | 0.0 | Generative AI for Enterprise AI | **Reproducible Verification Artifact:** An executable specification, an exhaustive state-s |
| review_trustworthy_multi_agent_sys | 117 | 0.0863 | GOV-REK: Governed Reward Engineering Kernels f | where $\tau_{\text{ground}} = 0.95$ is the strict grounding threshold enforced by the Fact |
| review_trustworthy_multi_agent_sys | 153 | 0.0423 | A Blueprint Architecture of Compound AI System | Let up to $f$ agents out of $n$ total council members be Byzantine (i.e., generating hallu |
| review_trustworthy_multi_agent_sys | 273 | 0.0559 | Augmenting the action space with conventions t | If rebuttal turns exceed $k_{\max} = 3$, the Chairman agent is granted unilateral synthesi |
| review_trustworthy_multi_agent_sys | 342 | 0.0228 | A Blueprint Architecture of Compound AI System | However, unconstrained debate is prone to sycophancy, majority-vote bias, and hallucinatio |
| review_trustworthy_multi_agent_sys | 345 | 0.0744 | DICA: Dual-Indicator Guided Contrastive Alignm | Linear Temporal Logic (LTL) and Computation Tree Logic (CTL) model checking have been wide |

**84 occurrences flagged.**

## Suggested replacements from the vault

### autonomous_code_synthesis_and_self_healing_multi_agent_systems
- **L26** replacing _A Survey of Test-Time Compute: From Intuitiv_:
    - `crossref_10.1016_j.aei.2026.104392` (0.1976) — Socio-technical assessment of generative AI integration in archi
    - `openalex_W7131475559` (0.1705) — SoK: Agentic Skills -- Beyond Tool Use in LLM Agents
    - `crossref:10.1145/3689096.3689462` (0.1566) — Comparative Analysis of Deep Learning Models for Breast Cancer C
- **L32** replacing _A Decentralised Self-Healing Approach for Ne_:
    - `arxiv_2405.20519` (0.4048) — Diffusion On Syntax Trees For Program Synthesis
    - `10.1145/3611643.3616271` (0.3042) — Copiloting the Copilots: Fusing Large Language Models with Compl
    - `arxiv_1311_3414` (0.3002) — Mining Software Repair Models for Reasoning on the Search Space 
- **L32** replacing _Language Models are Few-Shot Learners_:
    - `10_1038_s41586_023_06924_6` (0.3157) — Mathematical discoveries from program search with large language
    - `arxiv:1806.02690` (0.281) — Guest Editorial: Special Topic on Data-enabled Theoretical Chemi
    - `openalex:W4412620583` (0.2577) — A Comprehensive Introspection on AI Risks: Taxonomy, Challenges 

### review_architectural_dynamics_long_12_page
- **L22** replacing _GOV-REK: Governed Reward Engineering Kernels_:
    - `arxiv_2607.07144` (0.4111) — Fractal KV-Cache Archives: Lossless Symbolic Storage with In-Pla
    - `arxiv_2203.11171` (0.2965) — Self-Consistency Improves Chain of Thought Reasoning in Language
    - `arxiv_2605_09649` (0.2565) — Make Each Token Count: Towards Improving Long-Context Performanc
- **L28** replacing _Generative AI for Enterprise AI_:
    - `crossref_10.1016_j.aei.2026.104392` (0.3064) — Socio-technical assessment of generative AI integration in archi
    - `crossref:10.1109/access.2026.3656309` (0.3064) — Fine-Tuning CLIP With Dynamic Prompt Tuning and Cross-Modal Cont
    - `10.1109/hpca61900.2025.00113` (0.3064) — InstAttention: In-Storage Attention Offloading for Cost-Effectiv
- **L69** replacing _Augmenting the action space with conventions_:
    - `crossref.10.48550.arxiv.2402.09353` (0.3679) — DoRA: Weight-Decomposed Low-Rank Adaptation
    - `arxiv.2604.17215` (0.3484) — Continual Safety Alignment via Gradient-Based Sample Selection
    - `crossref_10_1609_aaai_v39i20_35509` (0.3386) — MTL-LoRA: Low-Rank Adaptation for Multi-Task Learning

### review_composable_ai_systems_for_trustworthy_agentic_pipelines
- **L33** replacing _A Survey of Test-Time Compute: From Intuitiv_:
    - `crossref_10.2139_ssrn.6233618` (0.1638) — AGEC and Graph-Based Systemic Risk Governance: A Deterministic G
    - `crossref:10.1145/3689096.3689462` (0.1187) — Comparative Analysis of Deep Learning Models for Breast Cancer C
    - `arxiv.2604.17215` (0.1165) — Continual Safety Alignment via Gradient-Based Sample Selection
- **L41** replacing _Deliberative Technology for Alignment_:
    - `crossref_10_1201_9788743808145_14` (0.247) — Generative AI for Enterprise AI
    - `10_1145_3544548_3581225` (0.2041) — Co-Writing Screenplays and Theatre Scripts with Language Models:
    - `10_70777_si_v2i3_15161` (0.1952) — AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications an
- **L44** replacing _A Blueprint Architecture of Compound AI Syst_:
    - `doaj.0dd42d861d1d46e8b9e27a88b02ca7d7` (0.171) — Mechanistic interpretability of reinforcement learning in Medica
    - `arxiv_1802_00951` (0.1684) — Scheduling and Checkpointing optimization algorithm for Byzantin
    - `arxiv_2604_12129` (0.1506) — Aethon: A Reference-Based Replication Primitive for Constant-Tim

### review_continual_safety_alignment_in_vision_language_models
- **L38** replacing _Training language models to follow instructi_:
    - `crossref:10.21203/rs.3.rs-10331065/v1` (0.4641) — Automated Fracture Image Captioning Using Multimodal Vision-Lang
    - `hal.5651880` (0.4187) — Efficient and scalable multimodal learning
    - `10_48550_arxiv_2502_14786` (0.3437) — SigLIP 2: Multilingual Vision-Language Encoders with Improved Se
- **L38** replacing _Deliberative Technology for Alignment_:
    - `10_1109_icscn67106_2025_11308520` (0.214) — AI Driven Self Healing Software Architectures for Automated Code
    - `europepmc.PMC13068123` (0.1987) — Cardiology-Chat: A Multi-LLMs Powered System for Cardiac Diagnos
    - `arxiv_2603_14332` (0.1696) — Governing Dynamic Capabilities: Cryptographic Binding and Reprod
- **L43** replacing _A Blueprint Architecture of Compound AI Syst_:
    - `arxiv.2604.17215` (0.7941) — Continual Safety Alignment via Gradient-Based Sample Selection
    - `arxiv.2602.00426` (0.4467) — LLMs as High-Dimensional Nonlinear Autoregressive Models with At
    - `arxiv_2305_18290` (0.415) — Direct Preference Optimization: Your Language Model is Secretly 

### review_enterprise_adoption_of_multi_agent_ai_systems_infr
- **L49** replacing _A Survey on LLM-as-a-Judge_:
    - `arxiv_2604.00186` (0.238) — Agentic AI and Occupational Displacement: A Multi-Regional Task 
    - `arxiv_2606_06545` (0.212) — Queen-Bee Agents: A BeeSpec-Centered Architecture for Governed E
    - `crossref_10.2139_ssrn.6233618` (0.2007) — AGEC and Graph-Based Systemic Risk Governance: A Deterministic G
- **L56** replacing _Generative AI for Enterprise AI_:
    - `arxiv_2602.17675` (0.1986) — Mind the Boundary: Stabilizing Gemini Enterprise A2A via a Cloud
    - `europepmc_PPR1283341` (0.1901) — Findings from Sparse Autoencoders for DNA Sequence Models: Motif
    - `crossref_10.2139_ssrn.6233618` (0.1726) — AGEC and Graph-Based Systemic Risk Governance: A Deterministic G
- **L95** replacing _Augmenting the action space with conventions_:
    - `arxiv.2605.08840` (0.2224) — ReST-KV: Robust KV Cache Eviction with Layer-wise Output Reconst
    - `arxiv.2510.14973` (0.2215) — Attention Is All You Need for KV Cache in Diffusion LLMs
    - `arxiv_2603.04428` (0.188) — Agent Memory Below the Prompt: Persistent Q4 KV Cache for Multi-

### review_spatio_temporal_grounding_in_video_question_answering
- **L33** replacing _A Survey of Test-Time Compute: From Intuitiv_:
    - `arxiv:2605.24470` (0.1817) — TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2
    - `openalex_W4380353763` (0.1716) — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
    - `plos_10_1371_journal_pone_0349024` (0.1691) — TDGN: A text-guided dual-gated network for multimodal sentiment 
- **L33** replacing _Generative AI for Enterprise AI_:
    - `arxiv_2602.08329` (0.2739) — Near-Oracle KV Selection via Pre-hoc Sparsity for Long-Context I
    - `arxiv:2509.01947` (0.2369) — Automated Repair of C Programs Using Large Language Models
    - `crossref.10.18653.v1.2020.emnlp.main.161` (0.2318) — HERO: Hierarchical Encoder for Video+Language Omni-representatio
- **L43** replacing _A Survey of Test-Time Compute: From Intuitiv_:
    - `arxiv:2406.04710` (0.1304) — Morescient GAI for Software Engineering (Extended Version)
    - `arxiv.2512.04356` (0.1273) — Mitigating Object and Action Hallucinations in Multimodal LLMs v
    - `arxiv_2605_09649` (0.125) — Make Each Token Count: Towards Improving Long-Context Performanc

### review_symbol_graph_rag_vs_qlora_swe_bench_lite
- **L24** replacing _A Survey of Test-Time Compute: From Intuitiv_:
    - `arxiv_2607_08691` (0.31) — ProjAgent: Procedural Similarity Retrieval for Repository-Level 
    - `arxiv:2607.24882` (0.2606) — Agent Retrieval Bench: Evaluating Repository Context Retrieval f
    - `arxiv:2605.24470` (0.2593) — TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2
- **L26** replacing _Generative AI for Enterprise AI_:
    - `crossref:10.2139/ssrn.7176278` (0.1988) — Enterprise Trust Gaps in Generative AI Why Accuracy is not Enoug
    - `arxiv:2605.24470` (0.1956) — TempRet: Temporal Enhancement and Two-Stage Reranking for CVPR 2
    - `openalex:W1982461819` (0.1839) — The Economics of Two-Sided Markets
- **L47** replacing _Can Linguistic Knowledge Improve Multimodal _:
    - `arxiv:2602.04998` (0.1632) — Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tun
    - `doaj:00b7bd46aae14917ab6a6542bacad985` (0.1616) — An Explainable Multimodal Vision&#x2013;Language Framework With 
    - `dblp.1673083` (0.1571) — Self-Consistency Improves Chain of Thought Reasoning in Language

### review_trustworthy_multi_agent_systems_formal_verification
- **L36** replacing _GOV-REK: Governed Reward Engineering Kernels_:
    - `10_1109_twc_2023_3293709` (0.2868) — An Efficient and Reliable Byzantine Fault Tolerant Blockchain Co
    - `arxiv:1810.05256` (0.1613) — Aleph: A Leaderless, Asynchronous, Byzantine Fault Tolerant Cons
    - `arxiv:2511.21779` (0.1448) — Aligning Artificial Superintelligence via a Multi-Box Protocol
- **L46** replacing _Deliberative Technology for Alignment_:
    - `openalex_W4304195432` (0.2865) — Distributing Accountability, Not Capability: Phase Separation an
    - `openalex:W4412620583` (0.2858) — A Comprehensive Introspection on AI Risks: Taxonomy, Challenges 
    - `crossref_10.2139_ssrn.6233618` (0.2522) — AGEC and Graph-Based Systemic Risk Governance: A Deterministic G
- **L49** replacing _A Blueprint Architecture of Compound AI Syst_:
    - `arxiv:2411.15594` (0.2243) — A Survey on LLM-as-a-Judge
    - `crossref:10.2139/ssrn.6955478` (0.2195) — Opening the Black Box of Scientific Foundation Models: A Review 
    - `arxiv_2603_14332` (0.1879) — Governing Dynamic Capabilities: Cryptographic Binding and Reprod

