# Claim Provenance Report

Every quantitative claim in each manuscript, resolved against recorded
evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`
matches the value; `CITATION` means the sentence attributes it to a cited
source; `UNGROUNDED` means the manuscript asserts a measurement it cannot
support.

| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |
|:---|---:|---:|---:|---:|---:|
| autonomous_code_synthesis_and_self_healing_multi_agent_systems | 12 | 12 | 0 | 0 | 100.0% |
| review_architectural_dynamics_long_12_page | 48 | 1 | 0 | 47 | 2.1% |
| review_composable_ai_systems_for_trustworthy_agentic_pipelines | 116 | 0 | 0 | 116 | 0.0% |
| review_continual_safety_alignment_in_vision_language_models | 39 | 0 | 0 | 39 | 0.0% |
| review_enterprise_adoption_of_multi_agent_ai_systems_infr | 25 | 23 | 2 | 0 | 100.0% |
| review_enterprise_genai_roi | 3 | 0 | 0 | 3 | 0.0% |
| review_spatio_temporal_grounding_in_video_question_answering | 85 | 0 | 0 | 85 | 0.0% |
| review_symbol_graph_rag_vs_qlora_swe_bench_lite | 79 | 3 | 2 | 74 | 6.3% |
| review_trustworthy_multi_agent_systems_formal_verification | 90 | 0 | 0 | 90 | 0.0% |

## review_architectural_dynamics_long_12_page — 47 ungrounded

- **L20** `N = 892` — This paper presents a comprehensive formal investigation of architectural dynamics, parameter efficiency, and compute scaling laws across modern trans
- **L22** `p < 0.001` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `d = 0.91` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `N = 892` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `68.2\%` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `98.4\%` — Our empirical findings demonstrate that structured parameter factorization reduces active memory footprint by $68.2\%$ while preserving $98.4\%$ of de
- **L22** `22.9\%` — The hybrid Symbol-RAG compound architecture achieves $3.1\times$ throughput improvement over dense baselines at $22.9\%$ of the VRAM cost [[crossref_1
- **L66** `N = 892` — An empirical scaling benchmark across $N = 892$ multi-node GPU cluster configurations evaluating FLOPs efficiency, KV cache memory scaling, and infere
- **L254** `0.39\%` — For $d = k = 8192$ and $r = 16$: $\mathcal{M}_{\text{cap}} = 0.39\%$ — confirming that LoRA explores only $0.39\%$ of the full parameter space.
- **L254** `0.39\%` — For $d = k = 8192$ and $r = 16$: $\mathcal{M}_{\text{cap}} = 0.39\%$ — confirming that LoRA explores only $0.39\%$ of the full parameter space.
- **L466** `8×` — For Mixtral 8×7B ($E = 8$, $k = 2$): active params $\approx 12.8$B out of 46.7B total — a $3.65\times$ parameter efficiency gain at inference time [[a
- **L505** `80 GB` — % of 80 GB H100
- **L507** `13.1%` — 13.1%
- **L507** `10.5 GB` — 10.5 GB
- **L508** `52.4%` — 52.4%
- **L508** `41.9 GB` — 41.9 GB
- **L509** `83.9 GB` — 83.9 GB
- **L510** `167.7 GB` — 167.7 GB
- **L511** `335.5 GB` — 335.5 GB
- **L551** `N = 892` — **Table 2: Architectural Comparison Across $N = 892$ Configurations**
- **L555** `14.0 GB` — 14.0 GB
- **L556** `26.0 GB` — 26.0 GB
- **L557** `140.0 GB` — 140.0 GB
- **L558** `42.0 GB` — 42.0 GB†
- **L559** `8×` — MoE 8×7B (top-2)
- **L559** `86.0 GB` — 86.0 GB
- **L560** `8×` — MoE 8×22B (top-2)
- **L560** `162.0 GB` — 162.0 GB
- **L561** `32.0 GB` — **32.0 GB**
- **L563** `p < 0.001` — $p < 0.001$ for Symbol-RAG vs Dense 70B on all benchmarks; Cohen's $d = 0.91$; $N = 892$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L563** `d = 0.91` — $p < 0.001$ for Symbol-RAG vs Dense 70B on all benchmarks; Cohen's $d = 0.91$; $N = 892$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L563** `N = 892` — $p < 0.001$ for Symbol-RAG vs Dense 70B on all benchmarks; Cohen's $d = 0.91$; $N = 892$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L565** `68.2\%` — **Key Finding:** Symbol-RAG achieves $68.2\%$ VRAM reduction vs Dense 70B, $3.1\times$ throughput improvement, while exceeding Dense 70B on all three 
- **L584** `N = 892` — **Table 4: Pareto Frontier — FLOPs vs MMLU vs VRAM ($N = 892$)**
- **L589** `8×` — MoE 8×7B
- **L593** `8×` — MoE 8×22B
- **L595** `90 GB` — Symbol-RAG dominates the Dense 70B and QLoRA 70B configurations — achieving higher MMLU at lower FLOPs and lower VRAM simultaneously, establishing it 
- **L599** `N=50,000` — **Table 5: MoE Expert Utilization Statistics (Token Distribution, $N=50,000$ tokens)**
- **L613** `41.2%` — Without auxiliary loss, Expert 1 captures 41.2% of all tokens (severe collapse)
- **L657** `0.01\%` — IA³ (Few-Shot Parameter-Efficient Fine-Tuning) achieves PEFT with as few as $0.01\%$ of parameters.

## review_composable_ai_systems_for_trustworthy_agentic_pipelines — 116 ungrounded

- **L33** `p < 0.001` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `d = 1.08` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `N = 8,600` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `N = 412` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `98.4\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `64.2\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L33** `41.8\%` — Across rigorous empirical benchmarks comprising $N = 8,600$ multi-hop enterprise reasoning workflows and $N = 412$ enterprise microservice deployments
- **L59** `p < 0.001` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L59** `N = 8,600` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L59** `N = 412` — **Large-Scale Multi-Domain Empirical Benchmark:** We evaluate CAS across $N = 8,600$ enterprise workflows and $N = 412$ production deployments, demons
- **L328** `N = 8,600` — We evaluate the CAS framework across four distinct enterprise task suites totaling $N = 8,600$ multi-step workflows:
- **L329** `N = 2,400` — **SWE-bench Multi-Repo Repair ($N = 2,400$):** Multi-file issue resolution requiring AST parsing, patch generation, and regression testing [[arxiv_240
- **L330** `N = 2,200` — **Financial Compliance & Regulatory Auditing ($N = 2,200$):** Multi-hop document extraction requiring strict numerical grounding and SEC filing invari
- **L331** `N = 2,000` — **Distributed Clinical Pathway Synthesis ($N = 2,000$):** Electronic health record synthesis requiring strict HIPAA privacy constraints and drug-inter
- **L332** `N = 2,000` — **Autonomous Cloud Infrastructure Remediation ($N = 2,000$):** Live Kubernetes microservice incident triage requiring root-cause diagnosis and non-des
- **L355** `N = 8,600` — **Table 1: Multi-Domain Benchmark Results Across $N = 8,600$ Enterprise Workflows**
- **L359** `61.2%` — 61.2%
- **L359** `54.3%` — 54.3%
- **L359** `28.4%` — 28.4%
- **L359** `24.8s` — 24.8s
- **L360** `68.7%` — 68.7%
- **L360** `49.1%` — 49.1%
- **L360** `34.1%` — 34.1%
- **L360** `31.2s` — 31.2s
- **L361** `77.4%` — 77.4%
- **L361** `79.2%` — 79.2%
- **L361** `12.3%` — 12.3%
- **L361** `18.6s` — 18.6s
- **L362** `92.6%` — **92.6%**
- **L362** `98.4%` — **98.4%**
- **L362** `0.8%` — **0.8%**
- **L362** `6.7s` — **6.7s**
- **L364** `p < 0.001` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L364** `d = 1.08` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L364** `t(8598) = 21.43` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L364** `15.2\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L364** `1.1\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L367** `28.4\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L367** `0.8\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L368** `51.8\%` — **Compute Efficiency:** By terminating invalid reasoning branches at Tier 3 contracts rather than looping through 10+ open-ended LLM reflection passes

## review_continual_safety_alignment_in_vision_language_models — 39 ungrounded

- **L31** `p < 0.001` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `N = 14,850` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `93.4\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `99.2\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L167** `N = 1,214` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L167** `N = 486` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L167** `N = 168` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L167** `N = 38` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L186** `44.2\%` — Unconstrained Full SFT & Low ($1.0\times$) & Baseline ($1.0\times$) & No & 44.2\% & Catastrophic alignment collapse \\
- **L187** `68.5\%` — LoRA / PEFT Adapter & Low ($1.1\times$) & Low ($0.1\times$) & No & 68.5\% & Subspace leakage into shared bases \\
- **L188** `88.7\%` — Dark Experience Replay & High ($2.4\times$) & High ($1.8\times$) & Yes (Replay Buffer) & 88.7\% & Heavy memory \& data privacy burden \\
- **L189** `89.4\%` — Gradient Projection Surgery & Very High ($3.1\times$) & Medium ($1.3\times$) & Yes (Reference Grad) & 89.4\% & Quadratic gradient inner products \\
- **L190** `76.1\%` — Representation Steering & Low ($1.05\times$) & Low ($1.0\times$) & No & 76.1\% & Fails under complex visual jailbreaks \\
- **L191** `93.4\%` — \textbf{Gradient Sample Selection (Ours)} & \textbf{Low ($1.15\times$)} & \textbf{Baseline ($1.0\times$)} & \textbf{No} & \textbf{93.4\%} & Requires s
- **L232** `N = 14,850` — To rigorously evaluate safety retention and task performance, we utilize four primary empirical benchmarks encompassing $N = 14,850$ multimodal test e
- **L242** `10\%` — Dark Experience Replay (DER++): Replaying $10\%$ historical safety alignment batches during task adaptation [[arxiv_2406.04028]].
- **L256** `N = 14,850` — \caption{Comprehensive Main Results across Multimodal Safety Benchmarks and Downstream Task Accuracy ($N = 14,850$)
- **L275** `6.2\%` — As demonstrated in Table \ref{tab:main_results}, unconstrained full fine-tuning causes an alarming collapse in safety performance, with attack vulnera
- **L275** `58.4\%` — As demonstrated in Table \ref{tab:main_results}, unconstrained full fine-tuning causes an alarming collapse in safety performance, with attack vulnera
- **L275** `89.2\%` — While DER++ preserves safety effectively ($89.2\%$), it requires continuous access to proprietary safety alignment data
- **L275** `93.8\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L275** `7.8\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L275** `0.6\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L278** `30\%` — To analyze the sensitivity of the gradient filtering cutoff, Table \ref{tab:ablation_alpha} details model performance as the filtering quantile $(1-\a
- **L289** `100\%` — 1.00 (Full Dataset) & 100\% & 46.2 & 58.4 & 84.2 \\
- **L290** `95\%` — 0.95 & 95\% & 68.4 & 34.2 & 84.0 \\
- **L291** `90\%` — 0.90 & 90\% & 86.7 & 16.1 & 83.9 \\
- **L292** `85\%` — \textbf{0.85 (Optimal)} & \textbf{85\%} & \textbf{93.8} & \textbf{7.8} & \textbf{83.6} \\
- **L293** `80\%` — 0.80 & 80\% & 94.1 & 7.2 & 81.8 \\
- **L294** `70\%` — 0.70 & 70\% & 94.6 & 6.5 & 77.4 \\
- **L299** `15\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L299** `95\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L299** `20\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L323** `0 GB` — Full Fine-Tuning & 48.2 & 142 & 0 GB \\
- **L324** `12 GB` — Dark Experience Replay & 74.6 & 318 & 12 GB (Replay Buffer) \\
- **L325** `8 GB` — Gradient Projection (GPM) & 82.4 & 485 & 8 GB (Feature Bases) \\
- **L326** `0 GB` — \textbf{Gradient Selection (Ours)} & \textbf{49.1} & \textbf{156} & \textbf{0 GB} \\
- **L357** `93.8\%` — We proved theoretically and verified empirically across $14,850$ multimodal benchmark interactions that data-centric gradient sample selection retains
- **L357** `98.9\%` — We proved theoretically and verified empirically across $14,850$ multimodal benchmark interactions that data-centric gradient sample selection retains

## review_enterprise_genai_roi — 3 ungrounded

- **L54** `922x` — This framework moves beyond simple correlation, striving for a causal understanding of GenAI's impact [[crossref_10.2139_ssrn.6374778]], [[crossref_10
- **L93** `100\%` — \text{ROI} = \frac{\text{Net Profit attributable to GenAI}}{\text{Cost of GenAI Investment}} \times 100\%
- **L159** `100\%` — \text{ROI} = \frac{(\Delta R + \Delta C) - I}{I} \times 100\%

## review_spatio_temporal_grounding_in_video_question_answering — 85 ungrounded

- **L31** `N = 42,000` — In this paper, we conduct an exhaustive theoretical and empirical evaluation of spatio-temporal cross-modal grounding across $N = 42,000$ video-questi
- **L33** `p < 0.001` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L33** `d = 0.89` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L33** `7.8\%` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L33** `38.4\%` — Across extensive evaluations on ActivityNet-QA, Video-ChatGPT, Next-QA, and Ego4D, DST-DR achieves a **$+7.8\%$ absolute gain in top-1 accuracy** over
- **L43** `75\%` — However, in natural video sequences, static background pixels (e.g., room walls, outdoor terrain, invariant background furniture) account for over $75
- **L53** `p < 0.001` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L53** `N = 42,000` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L53** `38.4\%` — **Large-Scale Multi-Benchmark Empirical Synthesis ($N = 42,000$):** We evaluate DST-DR across eight standard VideoQA benchmarks, demonstrating consist
- **L344** `N = 42,000` — We evaluate DST-DR across eight standard video reasoning benchmarks totaling $N = 42,000$ test queries:
- **L346** `N = 42,000` — **Table 1: Benchmark Dataset Characteristics Across $N = 42,000$ Probes**
- **L350** `180 s` — 180 s
- **L351** `120 s` — 120 s
- **L352** `44 s` — 44 s
- **L353** `10 s` — 10 s
- **L354** `15 s` — 15 s
- **L355** `3 s` — 3 s
- **L356** `25 s` — 25 s
- **L357** `300 s` — 300 s
- **L389** `p < 0.001` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L389** `d = 0.89` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L389** `t(41998) = 16.84` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L389** `5.2\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L389** `0.6\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L392** `5.2\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L392** `6.4\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L392** `6.1\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L393** `78.7\%` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L393** `38.4\%` — dense**, and **$38.4\%$ reduction vs
- **L394** `54.7\%` — **Egocentric Mastery:** On Ego4D (fine-grained tool manipulation across 5-minute video streams), DST-DR achieves $54.7\%$ accuracy, proving robust spa
- **L402** `N = 6,500` — **Table 3: Next-QA Accuracy Breakdown by Reasoning Category ($N = 6,500$)**
- **L406** `54.2%` — 54.2%
- **L406** `48.1%` — 48.1%
- **L406** `66.9%` — 66.9%
- **L406** `56.4%` — 56.4%
- **L407** `59.8%` — 59.8%
- **L407** `53.4%` — 53.4%
- **L407** `73.1%` — 73.1%
- **L407** `62.1%` — 62.1%
- **L408** `64.1%` — 64.1%

## review_symbol_graph_rag_vs_qlora_swe_bench_lite — 74 ungrounded

- **L20** `p < 0.001` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `d = 0.83` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `38.7%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `27.3%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `11.4\%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L20** `1.8\%` — Symbol-Graph RAG achieves a resolved-issue rate of **38.7%** versus **27.3%** for QLoRA fine-tuned 70B models ($p < 0.001$, Cohen's $d = 0.83$, 95% CI
- **L22** `N = 347` — Our ablation across $N = 347$ controlled task variants decomposes performance attributable to graph topology ($+5.5$ pp), call-graph edges ($+3.4$ pp)
- **L41** `N = 347` — A decomposed ablation study ($N = 347$ variants) isolating the independent contributions of graph topology, call-graph edges, and embedding quality to
- **L123** `38.7\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L123** `27.6\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L123** `95%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L123** `27.3\%` — Since our empirical resolved rate is $38.7\%$, the true population rate is at least $27.6\%$ with 95% probability — strictly exceeding QLoRA's $27.3\%
- **L200** `80 GB` — Training: 3 epochs, AdamW ($\eta = 2 \times 10^{-4}$, $\lambda_{\text{wd}} = 0.01$, cosine decay), batch size 32, 2× NVIDIA H100 80 GB (160 GB VRAM pe
- **L200** `160 GB` — Training: 3 epochs, AdamW ($\eta = 2 \times 10^{-4}$, $\lambda_{\text{wd}} = 0.01$, cosine decay), batch size 32, 2× NVIDIA H100 80 GB (160 GB VRAM pe
- **L224** `+11.4 pp` — **+11.4 pp** ★★★
- **L225** `+12.8 pp` — **+12.8 pp** ★★★
- **L228** `11.3s` — **−11.3s** (2.5×)
- **L229** `160 GB` — **−160 GB**
- **L230** `\$0.18` — \$0.18
- **L230** `\$0.42` — \$0.42
- **L230** `\$0.10` — **\$0.10**
- **L230** `\$0.32` — **−\$0.32 (4.2×)**
- **L231** `38.4 kg` — **−38.4 kg**
- **L233** `p < 0.001` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L233** `d = 0.83` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L233** `t(298) = 8.41` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L233** `95%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L233** `11.4\%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L233** `1.8\%` — ★★★ $p < 0.001$; Two-sample $t(298) = 8.41$; Mann-Whitney $U = 31{,}842$; Bootstrap CI at 95%: $\Delta = 11.4\% \pm 1.8\%$; Cohen's $d = 0.83$ (large 
- **L241** `+13.4 pp` — +13.4 pp
- **L242** `+14.9 pp` — +14.9 pp
- **L243** `+10.4 pp` — +10.4 pp
- **L244** `+4.9 pp` — +4.9 pp
- **L245** `+4.6 pp` — +4.6 pp
- **L269** `N = 347` — **Table 4: Symbol-Graph RAG Ablation ($N = 347$ controlled variants)**
- **L274** `5.5 pp` — −5.5 pp ★★★
- **L275** `8.9 pp` — −8.9 pp ★★★
- **L276** `2.6 pp` — −2.6 pp ★★
- **L277** `1.3 pp` — −1.3 pp ★
- **L278** `14.2 pp` — −14.2 pp ★★★

## review_trustworthy_multi_agent_systems_formal_verification — 90 ungrounded

- **L34** `p < 0.001` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L34** `d = 1.21` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L34** `N = 10,200` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L34** `N = 521` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L34** `100\%` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L34** `89.4\%` — Across extensive empirical evaluations comprising $N = 10,200$ adversarial multi-agent interaction traces and $N = 521$ production enterprise agent co
- **L59** `N = 10,200` — **Comprehensive Adversarial Empirical Benchmark ($N = 10,200$):** We evaluate T-MAS against heavy adversarial injection, sybil attacks, and hallucinat
- **L59** `N = 521` — **Comprehensive Adversarial Empirical Benchmark ($N = 10,200$):** We evaluate T-MAS against heavy adversarial injection, sybil attacks, and hallucinat
- **L257** `N = 10,200` — We evaluate T-MAS across $N = 10,200$ rigorous adversarial multi-agent interaction traces:
- **L258** `N = 3,200` — **Adversarial Prompt Injection Traces ($N = 3,200$):** Sybil agent nodes attempting to inject malicious code snippets, bypass sandbox permissions, or 
- **L259** `p < 0.001` — **Hallucination Contagion Traces ($N = 3,000$):** Injected synthetic citations, false numerical claims ($N = \dots, p < 0.001$), and distorted benchma
- **L259** `N = 3,000` — **Hallucination Contagion Traces ($N = 3,000$):** Injected synthetic citations, false numerical claims ($N = \dots, p < 0.001$), and distorted benchma
- **L260** `N = 2,000` — **Circular Deadlock & Livelock Stress Tests ($N = 2,000$):** Contradictory optimization constraints designed to trigger non-terminating rebuttal loops
- **L261** `N = 2,000` — **Production Enterprise Contract Audits ($N = 2,000$):** Multi-hop document synthesis, contract generation, and software repair workflows drawn from l
- **L280** `N = 10,200` — **Table 1: Comparative Evaluation Across $N = 10,200$ Adversarial Multi-Agent Traces**
- **L284** `48.2%` — 48.2%
- **L284** `0.0%` — 0.0% (Compromised)
- **L284** `34.2%` — 34.2%
- **L284** `14.8%` — 14.8%
- **L284** `0 ms` — **1.00×** (0 ms)
- **L285** `76.4%` — 76.4%
- **L285** `18.2%` — 18.2%
- **L285** `18.6%` — 18.6%
- **L285** `8.4%` — 8.4%
- **L285** `42 ms` — 1.12× (+42 ms)
- **L286** `71.8%` — 71.8%
- **L286** `12.4%` — 12.4%
- **L286** `22.4%` — 22.4%
- **L286** `19.2%` — 19.2%
- **L286** `1.2s` — 2.40× (+1.2s)
- **L287** `88.6%` — 88.6%
- **L287** `89.2%` — 89.2%
- **L287** `7.8%` — 7.8%
- **L287** `4.2%` — 4.2%
- **L287** `180 ms` — 1.45× (+180 ms)
- **L288** `100.0%` — **100.0%**
- **L288** `99.8%` — **99.8%**
- **L288** `0.0%` — **0.0%**
- **L288** `0.0%` — **0.0%**
- **L288** `94 ms` — **1.25×** (**+94 ms**)
