# Claim Provenance Report

Every quantitative claim in each manuscript, resolved against recorded
evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`
matches the value; `CITATION` means the sentence attributes it to a cited
source; `UNGROUNDED` means the manuscript asserts a measurement it cannot
support.

| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |
|:---|---:|---:|---:|---:|---:|
| autonomous_code_synthesis_and_self_healing_multi_agent_systems | 81 | 0 | 0 | 81 | 0.0% |
| review_architectural_dynamics_long_12_page | 64 | 0 | 0 | 64 | 0.0% |
| review_composable_ai_systems_for_trustworthy_agentic_pipelines | 122 | 0 | 0 | 122 | 0.0% |
| review_continual_safety_alignment_in_vision_language_models | 85 | 0 | 0 | 85 | 0.0% |
| review_enterprise_adoption_of_multi_agent_ai_systems_infr | 90 | 0 | 0 | 90 | 0.0% |
| review_enterprise_genai_roi | 3 | 0 | 0 | 3 | 0.0% |
| review_spatio_temporal_grounding_in_video_question_answering | 95 | 0 | 0 | 95 | 0.0% |
| review_symbol_graph_rag_vs_qlora_swe_bench_lite | 89 | 0 | 2 | 87 | 2.2% |
| review_trustworthy_multi_agent_systems_formal_verification | 99 | 0 | 0 | 99 | 0.0% |

## autonomous_code_synthesis_and_self_healing_multi_agent_systems — 81 ungrounded

- **L20** `N = 500` — We benchmark four distinct multi-agent orchestration topologies across $N = 500$ enterprise software defects drawn from production microservice codeba
- **L20** `74\%` — We benchmark four distinct multi-agent orchestration topologies across $N = 500$ enterprise software defects drawn from production microservice codeba
- **L22** `p < 0.001` — We define a context-free grammar production algebra over AST mutation operators, prove that Z3-SMT pre-filtering with path-sensitive invariant checkin
- **L22** `d = 1.14` — We define a context-free grammar production algebra over AST mutation operators, prove that Z3-SMT pre-filtering with path-sensitive invariant checkin
- **L22** `89.3\%` — We define a context-free grammar production algebra over AST mutation operators, prove that Z3-SMT pre-filtering with path-sensitive invariant checkin
- **L22** `47.2\%` — We define a context-free grammar production algebra over AST mutation operators, prove that Z3-SMT pre-filtering with path-sensitive invariant checkin
- **L22** `28.1\%` — We define a context-free grammar production algebra over AST mutation operators, prove that Z3-SMT pre-filtering with path-sensitive invariant checkin
- **L37** `N = 500` — **Multi-Topology Empirical Benchmark**: Controlled evaluation of 4 orchestration topologies across $N = 500$ production defects across 7 code generati
- **L238** `32%` — This pre-filter eliminates $\sim$32% of all LLM proposals at zero execution cost [[crossref_10.18653_v1_2026.findings-acl.1933]].
- **L309** `N = 500` — **Corollary 1.** For production defects with average tree-edit distance $\bar{V} = 12.4$ (measured empirically across $N = 500$ defects) and $c_{\min}
- **L377** `N = 500` — Our benchmark corpus comprises $N = 500$ production defects drawn from:
- **L381** `N = 500` — **Table 0: Benchmark Defect Distribution Across Categories ($N = 500$)**
- **L385** `47.2%` — 47.2%
- **L386** `28.4%` — 28.4%
- **L387** `14.6%` — 14.6%
- **L388** `9.8%` — 9.8%
- **L416** `p < 0.001` — $p < 0.001$ for H-MAS vs Single Agent; $t(498) = 12.74$; Cohen's $d = 1.14$; Bootstrap CI ($B = 10{,}000$): $\Delta = 19.1\% \pm 2.4\%$ [[arxiv_2501.0
- **L416** `d = 1.14` — $p < 0.001$ for H-MAS vs Single Agent; $t(498) = 12.74$; Cohen's $d = 1.14$; Bootstrap CI ($B = 10{,}000$): $\Delta = 19.1\% \pm 2.4\%$ [[arxiv_2501.0
- **L416** `t(498) = 12.74` — $p < 0.001$ for H-MAS vs Single Agent; $t(498) = 12.74$; Cohen's $d = 1.14$; Bootstrap CI ($B = 10{,}000$): $\Delta = 19.1\% \pm 2.4\%$ [[arxiv_2501.0
- **L416** `19.1\%` — $p < 0.001$ for H-MAS vs Single Agent; $t(498) = 12.74$; Cohen's $d = 1.14$; Bootstrap CI ($B = 10{,}000$): $\Delta = 19.1\% \pm 2.4\%$ [[arxiv_2501.0
- **L416** `2.4\%` — $p < 0.001$ for H-MAS vs Single Agent; $t(498) = 12.74$; Cohen's $d = 1.14$; Bootstrap CI ($B = 10{,}000$): $\Delta = 19.1\% \pm 2.4\%$ [[arxiv_2501.0
- **L418** `74\%` — The H-MAS topology achieves $74\%$ latency reduction and $89.3\%$ SMT pre-filter rate — meaning only $10.7\%$ of LLM proposals require expensive sandb
- **L418** `89.3\%` — The H-MAS topology achieves $74\%$ latency reduction and $89.3\%$ SMT pre-filter rate — meaning only $10.7\%$ of LLM proposals require expensive sandb
- **L418** `10.7\%` — The H-MAS topology achieves $74\%$ latency reduction and $89.3\%$ SMT pre-filter rate — meaning only $10.7\%$ of LLM proposals require expensive sandb
- **L418** `$2.53` — This drives the $2.53\times$ reduction in container-seconds/task.
- **L422** `N = 500` — **Table 2: SHACS H-MAS Performance Across Code Benchmarks ($N = 500$ per benchmark)**
- **L438** `N = 500` — **Table 3: Z3-SMT Pre-Filter Performance ($N = 500$, H-MAS topology)**
- **L442** `38.2%` — 38.2%
- **L442** `97.3%` — 97.3%
- **L442** `2.7%` — 2.7%
- **L443** `21.4%` — 21.4%
- **L443** `94.8%` — 94.8%
- **L443** `5.2%` — 5.2%
- **L444** `18.7%` — 18.7%
- **L444** `96.1%` — 96.1%
- **L444** `3.9%` — 3.9%
- **L445** `11.0%` — 11.0%
- **L445** `99.2%` — 99.2%
- **L445** `0.8%` — 0.8%
- **L446** `89.3%` — **89.3%**

## review_architectural_dynamics_long_12_page — 64 ungrounded

- **L20** `N = 892` — This paper presents a comprehensive formal investigation of architectural dynamics, parameter efficiency, and compute scaling laws across modern trans
- **L22** `p < 0.001` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `d = 0.91` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `N = 892` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `68.2\%` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `98.4\%` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `22.9\%` — The hybrid Symbol-RAG compound architecture achieves $3.1\times$ throughput improvement over dense baselines at $22.9\%$ of the VRAM cost [[crossref_1
- **L22** `$3.1` — The hybrid Symbol-RAG compound architecture achieves $3.1\times$ throughput improvement over dense baselines at $22.9\%$ of the VRAM cost [[crossref_1
- **L51** `$10` — with fitted constants $E = 1.69$, $A = 406.4$, $B = 410.7$, $\alpha = 0.34$, $\beta = 0.28$ across models from $10^7$ to $10^{10}$ parameters
- **L51** `$10` — with fitted constants $E = 1.69$, $A = 406.4$, $B = 410.7$, $\alpha = 0.34$, $\beta = 0.28$ across models from $10^7$ to $10^{10}$ parameters
- **L62** `N = 892` — An empirical scaling benchmark across $N = 892$ multi-node GPU cluster configurations evaluating FLOPs efficiency, KV cache memory scaling, and infere
- **L215** `100\%` — \mathcal{M}_{\text{cap}}(r, d, k) = \frac{r(d + k)}{d \cdot k} \times 100\%
- **L226** `0.39\%` — For $d = k = 8192$ and $r = 16$: $\mathcal{M}_{\text{cap}} = 0.39\%$ — confirming that LoRA explores only $0.39\%$ of the full parameter space.
- **L226** `0.39\%` — For $d = k = 8192$ and $r = 16$: $\mathcal{M}_{\text{cap}} = 0.39\%$ — confirming that LoRA explores only $0.39\%$ of the full parameter space.
- **L410** `8×` — For Mixtral 8×7B ($E = 8$, $k = 2$): active params $\approx 12.8$B out of 46.7B total — a $3.65\times$ parameter efficiency gain at inference time [[a
- **L410** `$3.65` — For Mixtral 8×7B ($E = 8$, $k = 2$): active params $\approx 12.8$B out of 46.7B total — a $3.65\times$ parameter efficiency gain at inference time [[a
- **L445** `80 GB` — % of 80 GB H100
- **L447** `13.1%` — 13.1%
- **L447** `10.5 GB` — 10.5 GB
- **L448** `52.4%` — 52.4%
- **L448** `$4` — $4\times$
- **L448** `41.9 GB` — 41.9 GB
- **L449** `$8` — $8\times$
- **L449** `83.9 GB` — 83.9 GB
- **L450** `$16` — $16\times$
- **L450** `167.7 GB` — 167.7 GB
- **L451** `$32` — $32\times$
- **L451** `335.5 GB` — 335.5 GB
- **L487** `N = 892` — **Table 2: Architectural Comparison Across $N = 892$ Configurations**
- **L491** `14.0 GB` — 14.0 GB
- **L492** `26.0 GB` — 26.0 GB
- **L493** `140.0 GB` — 140.0 GB
- **L494** `42.0 GB` — 42.0 GB†
- **L495** `8×` — MoE 8×7B (top-2)
- **L495** `86.0 GB` — 86.0 GB
- **L496** `8×` — MoE 8×22B (top-2)
- **L496** `162.0 GB` — 162.0 GB
- **L497** `32.0 GB` — **32.0 GB**
- **L499** `p < 0.001` — $p < 0.001$ for Symbol-RAG vs Dense 70B on all benchmarks; Cohen's $d = 0.91$; $N = 892$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L499** `d = 0.91` — $p < 0.001$ for Symbol-RAG vs Dense 70B on all benchmarks; Cohen's $d = 0.91$; $N = 892$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].

## review_composable_ai_systems_for_trustworthy_agentic_pipelines — 122 ungrounded

- **L35** `p < 0.001` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `d = 1.08` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `N = 8,600` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `N = 412` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `98.4\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `64.2\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `41.8\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `$18.6` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L35** `$6.7` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L61** `p < 0.001` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L61** `N = 8,600` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L61** `N = 412` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L302** `N = 8,600` — We evaluate the CAS framework across four distinct enterprise task suites totaling $N = 8,600$ multi-step workflows:
- **L303** `N = 2,400` — **SWE-bench Multi-Repo Repair ($N = 2,400$):** Multi-file issue resolution requiring AST parsing, patch generation, and regression testing [[arxiv_240
- **L304** `N = 2,200` — **Financial Compliance & Regulatory Auditing ($N = 2,200$):** Multi-hop document extraction requiring strict numerical grounding and SEC filing invari
- **L305** `N = 2,000` — **Distributed Clinical Pathway Synthesis ($N = 2,000$):** Electronic health record synthesis requiring strict HIPAA privacy constraints and drug-inter
- **L306** `N = 2,000` — **Autonomous Cloud Infrastructure Remediation ($N = 2,000$):** Live Kubernetes microservice incident triage requiring root-cause diagnosis and non-des
- **L329** `N = 8,600` — **Table 1: Multi-Domain Benchmark Results Across $N = 8,600$ Enterprise Workflows**
- **L333** `61.2%` — 61.2%
- **L333** `54.3%` — 54.3%
- **L333** `28.4%` — 28.4%
- **L333** `24.8s` — 24.8s
- **L334** `68.7%` — 68.7%
- **L334** `49.1%` — 49.1%
- **L334** `34.1%` — 34.1%
- **L334** `31.2s` — 31.2s
- **L335** `77.4%` — 77.4%
- **L335** `79.2%` — 79.2%
- **L335** `12.3%` — 12.3%
- **L335** `18.6s` — 18.6s
- **L336** `92.6%` — **92.6%**
- **L336** `98.4%` — **98.4%**
- **L336** `0.8%` — **0.8%**
- **L336** `6.7s` — **6.7s**
- **L338** `p < 0.001` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L338** `d = 1.08` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L338** `t(8598) = 21.43` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L338** `95%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L338** `15.2\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L338** `1.1\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].

## review_continual_safety_alignment_in_vision_language_models — 85 ungrounded

- **L30** `p < 0.001` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L30** `N = 14,850` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L30** `93.4\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L30** `99.2\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L52** `$14` — We conduct an extensive quantitative meta-analysis, aggregating empirical evaluations across $14,850$ multimodal benchmark interactions to rigorously 
- **L158** `N = 1,214` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L158** `N = 486` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L158** `N = 168` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L158** `N = 38` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L158** `$1` — A total of $1,842$ candidate records were identified
- **L177** `44.2\%` — Unconstrained Full SFT & Low ($1.0\times$) & Baseline ($1.0\times$) & No & 44.2\% & Catastrophic alignment collapse \\
- **L177** `$1.0` — Unconstrained Full SFT & Low ($1.0\times$) & Baseline ($1.0\times$) & No & 44.2\% & Catastrophic alignment collapse \\
- **L177** `$1.0` — Unconstrained Full SFT & Low ($1.0\times$) & Baseline ($1.0\times$) & No & 44.2\% & Catastrophic alignment collapse \\
- **L178** `68.5\%` — LoRA / PEFT Adapter & Low ($1.1\times$) & Low ($0.1\times$) & No & 68.5\% & Subspace leakage into shared bases \\
- **L178** `$1.1` — LoRA / PEFT Adapter & Low ($1.1\times$) & Low ($0.1\times$) & No & 68.5\% & Subspace leakage into shared bases \\
- **L178** `$0.1` — LoRA / PEFT Adapter & Low ($1.1\times$) & Low ($0.1\times$) & No & 68.5\% & Subspace leakage into shared bases \\
- **L179** `88.7\%` — Dark Experience Replay & High ($2.4\times$) & High ($1.8\times$) & Yes (Replay Buffer) & 88.7\% & Heavy memory \& data privacy burden \\
- **L179** `$2.4` — Dark Experience Replay & High ($2.4\times$) & High ($1.8\times$) & Yes (Replay Buffer) & 88.7\% & Heavy memory \& data privacy burden \\
- **L179** `$1.8` — Dark Experience Replay & High ($2.4\times$) & High ($1.8\times$) & Yes (Replay Buffer) & 88.7\% & Heavy memory \& data privacy burden \\
- **L180** `89.4\%` — Gradient Projection Surgery & Very High ($3.1\times$) & Medium ($1.3\times$) & Yes (Reference Grad) & 89.4\% & Quadratic gradient inner products \\
- **L180** `$3.1` — Gradient Projection Surgery & Very High ($3.1\times$) & Medium ($1.3\times$) & Yes (Reference Grad) & 89.4\% & Quadratic gradient inner products \\
- **L180** `$1.3` — Gradient Projection Surgery & Very High ($3.1\times$) & Medium ($1.3\times$) & Yes (Reference Grad) & 89.4\% & Quadratic gradient inner products \\
- **L181** `76.1\%` — Representation Steering & Low ($1.05\times$) & Low ($1.0\times$) & No & 76.1\% & Fails under complex visual jailbreaks \\
- **L181** `$1.05` — Representation Steering & Low ($1.05\times$) & Low ($1.0\times$) & No & 76.1\% & Fails under complex visual jailbreaks \\
- **L181** `$1.0` — Representation Steering & Low ($1.05\times$) & Low ($1.0\times$) & No & 76.1\% & Fails under complex visual jailbreaks \\
- **L182** `93.4\%` — \textbf{Gradient Sample Selection (Ours)} & \textbf{Low ($1.15\times$)} & \textbf{Baseline ($1.0\times$)} & \textbf{No} & \textbf{93.4\%} & Requires s
- **L182** `$1.15` — \textbf{Gradient Sample Selection (Ours)} & \textbf{Low ($1.15\times$)} & \textbf{Baseline ($1.0\times$)} & \textbf{No} & \textbf{93.4\%} & Requires s
- **L182** `$1.0` — \textbf{Gradient Sample Selection (Ours)} & \textbf{Low ($1.15\times$)} & \textbf{Baseline ($1.0\times$)} & \textbf{No} & \textbf{93.4\%} & Requires s
- **L223** `N = 14,850` — To rigorously evaluate safety retention and task performance, we utilize four primary empirical benchmarks encompassing $N = 14,850$ multimodal test e
- **L233** `10\%` — Dark Experience Replay (DER++): Replaying $10\%$ historical safety alignment batches during task adaptation [[arxiv_2406.04028]].
- **L247** `N = 14,850` — \caption{Comprehensive Main Results across Multimodal Safety Benchmarks and Downstream Task Accuracy ($N = 14,850$)
- **L254** `$ 0.3` — Zero-Shot Aligned Baseline & 94.8 $\pm$ 0.3 & 92.1 $\pm$ 0.4 & 6.2 $\pm$ 0.2 & 71.4 $\pm$ 0.5 & 100.0 \\
- **L254** `$ 0.4` — Zero-Shot Aligned Baseline & 94.8 $\pm$ 0.3 & 92.1 $\pm$ 0.4 & 6.2 $\pm$ 0.2 & 71.4 $\pm$ 0.5 & 100.0 \\
- **L254** `$ 0.2` — Zero-Shot Aligned Baseline & 94.8 $\pm$ 0.3 & 92.1 $\pm$ 0.4 & 6.2 $\pm$ 0.2 & 71.4 $\pm$ 0.5 & 100.0 \\
- **L254** `$ 0.5` — Zero-Shot Aligned Baseline & 94.8 $\pm$ 0.3 & 92.1 $\pm$ 0.4 & 6.2 $\pm$ 0.2 & 71.4 $\pm$ 0.5 & 100.0 \\
- **L255** `$ 1.2` — Unconstrained Full-FT & 46.2 $\pm$ 1.2 & 41.8 $\pm$ 1.4 & 58.4 $\pm$ 1.8 & \textbf{84.2 $\pm$ 0.4} & 46.8 \\
- **L255** `$ 1.4` — Unconstrained Full-FT & 46.2 $\pm$ 1.2 & 41.8 $\pm$ 1.4 & 58.4 $\pm$ 1.8 & \textbf{84.2 $\pm$ 0.4} & 46.8 \\
- **L255** `$ 1.8` — Unconstrained Full-FT & 46.2 $\pm$ 1.2 & 41.8 $\pm$ 1.4 & 58.4 $\pm$ 1.8 & \textbf{84.2 $\pm$ 0.4} & 46.8 \\
- **L255** `$ 0.4` — Unconstrained Full-FT & 46.2 $\pm$ 1.2 & 41.8 $\pm$ 1.4 & 58.4 $\pm$ 1.8 & \textbf{84.2 $\pm$ 0.4} & 46.8 \\
- **L256** `$ 0.8` — LoRA Fine-Tuning ($r=16$) & 71.3 $\pm$ 0.8 & 67.5 $\pm$ 0.9 & 32.1 $\pm$ 1.1 & 81.6 $\pm$ 0.5 & 73.1 \\

## review_enterprise_adoption_of_multi_agent_ai_systems_infr — 90 ungrounded

- **L33** `N = 318` — In this paper, we conduct an exhaustive, multi-organizational empirical study across $N = 318$ production enterprise deployments and 45 in-depth organ
- **L35** `p < 0.001` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L35** `d = 0.94` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L35** `99.4\%` — We prove an availability theorem for hierarchical supervisor tree topologies using Discrete-Time Markov Chains (DTMC), establishing that hierarchical 
- **L35** `18.4\%` — In contrast, unconstrained peer-to-peer mesh networks exhibit super-linear token growth $\mathcal{O}(N^2)$ and an $18.4\%$ cascade failure rate due to
- **L35** `41.2\%` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L35** `$120` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L35** `$64.2` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L35** `$18.2` — Across our 90-day observation window tracking over $120$ million production agent interactions, hierarchical federated architectures achieve a $41.2\%
- **L46** `99.9\%` — Strict Service Level Agreements (SLAs): Multi-agent execution pipelines must provide bounded latency distributions ($p99 < 30\text{ s}$) and guarantee
- **L54** `N = 318` — Large-Scale Multi-Enterprise Telemetry Benchmark: An empirical investigation across $N = 318$ production multi-agent systems and 45 comprehensive ente
- **L230** `$1` — *Proof.* For stage $k$, the worker fails with probability $1 - p_k$
- **L230** `$1` — Thus, stage $k$ succeeds with probability $1 - (1 - p_k)(1 - r_k)^M$
- **L233** `44.37\%` — - Monolithic uncoordinated pipeline reliability: $\mathcal{R}_{\text{mono}} = 0.85^5 = 44.37\%$ (unacceptable for enterprise).
- **L234** `99.25\%` — - Hierarchical supervised pipeline reliability: $\mathcal{R}_{\text{hier}} = [1 - (0.15)(0.10)^2]^5 = [1 - 0.0015]^5 = 99.25\%$ (meets enterprise SLA)
- **L242** `N = 318` — Our study synthesizes telemetry data from $N = 318$ production multi-agent systems operating across 45 enterprise organizations over a 90-day observat
- **L273** `81.2%` — 81.2%
- **L273** `18.4%` — 18.4%
- **L273** `\$84.20` — \$84.20
- **L273** `64.2s` — 64.2s
- **L274** `92.4%` — 92.4%
- **L274** `7.2%` — 7.2%
- **L274** `\$46.80` — \$46.80
- **L274** `41.5s` — 41.5s
- **L275** `96.1%` — 96.1%
- **L275** `3.8%` — 3.8%
- **L275** `\$38.40` — \$38.40
- **L275** `29.8s` — 29.8s
- **L276** `99.4%` — 99.4%
- **L276** `0.6%` — 0.6%
- **L276** `\$24.60` — \$24.60
- **L276** `18.2s` — 18.2s
- **L278** `p < 0.001` — $p < 0.001$ across all pairwise comparisons; Two-sample $t(316) = 18.92$; Cohen's $d = 0.94$ (large effect)
- **L278** `d = 0.94` — $p < 0.001$ across all pairwise comparisons; Two-sample $t(316) = 18.92$; Cohen's $d = 0.94$ (large effect)
- **L278** `t(316) = 18.92` — $p < 0.001$ across all pairwise comparisons; Two-sample $t(316) = 18.92$; Cohen's $d = 0.94$ (large effect)
- **L278** `95%` — Bootstrap 95% CI on cost reduction: $\Delta = -\$59.60 \pm \$3.80$ per 1k tasks [[arxiv_2404.01131], [crossref_10.1201_9788743808145-14]].
- **L278** `\$59.60` — Bootstrap 95% CI on cost reduction: $\Delta = -\$59.60 \pm \$3.80$ per 1k tasks [[arxiv_2404.01131], [crossref_10.1201_9788743808145-14]].
- **L278** `\$3.80` — Bootstrap 95% CI on cost reduction: $\Delta = -\$59.60 \pm \$3.80$ per 1k tasks [[arxiv_2404.01131], [crossref_10.1201_9788743808145-14]].
- **L281** `70.8\%` — Token Efficiency: Hierarchical Federated architectures cut token consumption by $70.8\%$ compared to Mesh and $35.9\%$ compared to Blackboard, directl
- **L281** `35.9\%` — Token Efficiency: Hierarchical Federated architectures cut token consumption by $70.8\%$ compared to Mesh and $35.9\%$ compared to Blackboard, directl

## review_enterprise_genai_roi — 3 ungrounded

- **L54** `922x` — This framework moves beyond simple correlation, striving for a causal understanding of GenAI's impact [[crossref_10.2139_ssrn.6374778]], [[crossref_10
- **L91** `100\%` — \text{ROI} = \frac{\text{Net Profit attributable to GenAI}}{\text{Cost of GenAI Investment}} \times 100\%
- **L153** `100\%` — \text{ROI} = \frac{(\Delta R + \Delta C) - I}{I} \times 100\%

## review_spatio_temporal_grounding_in_video_question_answering — 95 ungrounded

- **L33** `N = 42,000` — In this paper, we conduct an exhaustive theoretical and empirical evaluation of spatio-temporal cross-modal grounding across $N = 42,000$ video-questi
- **L35** `p < 0.001` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L35** `d = 0.89` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L35** `7.8\%` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L35** `38.4\%` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L45** `75\%` — However, in natural video sequences, static background pixels (e.g., room walls, outdoor terrain, invariant background furniture) account for over $75
- **L55** `p < 0.001` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L55** `N = 42,000` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L55** `38.4\%` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L314** `N = 42,000` — We evaluate DST-DR across eight standard video reasoning benchmarks totaling $N = 42,000$ test queries:
- **L316** `N = 42,000` — **Table 1: Benchmark Dataset Characteristics Across $N = 42,000$ Probes**
- **L320** `180 s` — 180 s
- **L321** `120 s` — 120 s
- **L322** `44 s` — 44 s
- **L323** `10 s` — 10 s
- **L324** `15 s` — 15 s
- **L325** `3 s` — 3 s
- **L326** `25 s` — 25 s
- **L327** `300 s` — 300 s
- **L352** `$1.0` — **0.82** ($1.0\times$)
- **L353** `$6.8` — 5.58 ($6.8\times$)
- **L354** `$2.4` — 1.97 ($2.4\times$)
- **L355** `$2.2` — 1.84 ($2.2\times$)
- **L356** `$2.1` — 1.72 ($2.1\times$)
- **L357** `$1.45` — **1.19** (**$1.45\times$**)
- **L359** `p < 0.001` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L359** `d = 0.89` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L359** `t(41998) = 16.84` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L359** `95%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L359** `5.2\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L359** `0.6\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L362** `5.2\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L362** `6.4\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L362** `6.1\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L363** `78.7\%` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L363** `38.4\%` — dense**, and **$38.4\%$ reduction vs
- **L363** `$5.58` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L363** `$1.19` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L364** `54.7\%` — **Egocentric Mastery:** On Ego4D (fine-grained tool manipulation across 5-minute video streams), DST-DR achieves $54.7\%$ accuracy, proving robust spa
- **L372** `N = 6,500` — **Table 3: Next-QA Accuracy Breakdown by Reasoning Category ($N = 6,500$)**

## review_symbol_graph_rag_vs_qlora_swe_bench_lite — 87 ungrounded

- **L20** `p < 0.001` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `d = 0.83` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `38.7%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `27.3%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `95%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `11.4\%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `1.8\%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `$4.2` — Symbol-Graph RAG reduces inference compute costs by $4.2\times$ and eliminates training VRAM overhead entirely (QLoRA requires 160 GB across dual H100
- **L20** `160 GB` — Symbol-Graph RAG reduces inference compute costs by $4.2\times$ and eliminates training VRAM overhead entirely (QLoRA requires 160 GB across dual H100
- **L22** `N = 347` — Our ablation across $N = 347$ controlled task variants decomposes performance attributable to graph topology ($+5.5$ pp), call-graph edges ($+3.4$ pp)
- **L41** `N = 347` — A decomposed ablation study ($N = 347$ variants) isolating the independent contributions of graph topology, call-graph edges, and embedding quality to
- **L89** `$1` — By the Banach fixed-point theorem, the affine map $T(\pi) = \mathbf{M}\pi + \beta\mathbf{s}$ is a contraction on $(\mathbb{R}^{|V|}, \|\cdot\|_1)$ wit
- **L93** `$1` — With probability $1-\delta$ over $n = 300$ i.i.d
- **L115** `38.7\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L115** `27.6\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L115** `95%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L115** `27.3\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L143** `$16` — \sim 5{,}000$ nodes, $r = 16$), this bound is approximately $16 \times \log(1 + 312.5) = 82.6$ bits — representing severe structural information loss 
- **L184** `80 GB` — Training: 3 epochs, AdamW ($\eta = 2 \times 10^{-4}$, $\lambda_{\text{wd}} = 0.01$, cosine decay), batch size 32, 2× NVIDIA H100 80 GB (160 GB VRAM pe
- **L184** `160 GB` — Training: 3 epochs, AdamW ($\eta = 2 \times 10^{-4}$, $\lambda_{\text{wd}} = 0.01$, cosine decay), batch size 32, 2× NVIDIA H100 80 GB (160 GB VRAM pe
- **L204** `N = 300` — **Table 1: Primary Performance Comparison on SWE-bench Lite ($N = 300$ tasks)**
- **L208** `+11.4 pp` — **+11.4 pp** ★★★
- **L209** `+12.8 pp` — **+12.8 pp** ★★★
- **L212** `11.3s` — **−11.3s** (2.5×)
- **L213** `160 GB` — **−160 GB**
- **L214** `\$0.18` — \$0.18
- **L214** `\$0.42` — \$0.42
- **L214** `\$0.10` — **\$0.10**
- **L214** `\$0.32` — **−\$0.32 (4.2×)**
- **L215** `38.4 kg` — **−38.4 kg**
- **L217** `p < 0.001` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L217** `d = 0.83` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L217** `t(298) = 8.41` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L217** `95%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L217** `11.4\%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L217** `1.8\%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L225** `+13.4 pp` — +13.4 pp
- **L226** `+14.9 pp` — +14.9 pp
- **L227** `+10.4 pp` — +10.4 pp
- **L227** `$0.003` — $0.003$

## review_trustworthy_multi_agent_systems_formal_verification — 99 ungrounded

- **L36** `p < 0.001` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L36** `d = 1.21` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L36** `N = 10,200` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L36** `N = 521` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L36** `100\%` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L36** `89.4\%` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L61** `N = 10,200` — **Comprehensive Adversarial Empirical Benchmark ($N = 10,200$):** We evaluate T-MAS against heavy adversarial injection, sybil attacks, and hallucinat
- **L61** `N = 521` — **Comprehensive Adversarial Empirical Benchmark ($N = 10,200$):** We evaluate T-MAS against heavy adversarial injection, sybil attacks, and hallucinat
- **L61** `$10` — **Comprehensive Adversarial Empirical Benchmark ($N = 10,200$):** We evaluate T-MAS against heavy adversarial injection, sybil attacks, and hallucinat
- **L167** `$2` — Each revision must have received at least $2f + 1$ valid signatures
- **L239** `N = 10,200` — We evaluate T-MAS across $N = 10,200$ rigorous adversarial multi-agent interaction traces:
- **L240** `N = 3,200` — **Adversarial Prompt Injection Traces ($N = 3,200$):** Sybil agent nodes attempting to inject malicious code snippets, bypass sandbox permissions, or 
- **L241** `p < 0.001` — **Hallucination Contagion Traces ($N = 3,000$):** Injected synthetic citations, false numerical claims ($N = \dots, p < 0.001$), and distorted benchma
- **L241** `N = 3,000` — **Hallucination Contagion Traces ($N = 3,000$):** Injected synthetic citations, false numerical claims ($N = \dots, p < 0.001$), and distorted benchma
- **L242** `N = 2,000` — **Circular Deadlock & Livelock Stress Tests ($N = 2,000$):** Contradictory optimization constraints designed to trigger non-terminating rebuttal loops
- **L243** `N = 2,000` — **Production Enterprise Contract Audits ($N = 2,000$):** Multi-hop document synthesis, contract generation, and software repair workflows drawn from l
- **L262** `N = 10,200` — **Table 1: Comparative Evaluation Across $N = 10,200$ Adversarial Multi-Agent Traces**
- **L266** `48.2%` — 48.2%
- **L266** `0.0%` — 0.0% (Compromised)
- **L266** `34.2%` — 34.2%
- **L266** `14.8%` — 14.8%
- **L266** `0 ms` — **1.00×** (0 ms)
- **L267** `76.4%` — 76.4%
- **L267** `18.2%` — 18.2%
- **L267** `18.6%` — 18.6%
- **L267** `8.4%` — 8.4%
- **L267** `42 ms` — 1.12× (+42 ms)
- **L268** `71.8%` — 71.8%
- **L268** `12.4%` — 12.4%
- **L268** `22.4%` — 22.4%
- **L268** `19.2%` — 19.2%
- **L268** `1.2s` — 2.40× (+1.2s)
- **L269** `88.6%` — 88.6%
- **L269** `89.2%` — 89.2%
- **L269** `7.8%` — 7.8%
- **L269** `4.2%` — 4.2%
- **L269** `180 ms` — 1.45× (+180 ms)
- **L270** `100.0%` — **100.0%**
- **L270** `99.8%` — **99.8%**
- **L270** `0.0%` — **0.0%**
