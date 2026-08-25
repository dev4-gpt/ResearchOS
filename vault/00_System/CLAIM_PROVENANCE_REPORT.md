# Claim Provenance Report

Every quantitative claim in each manuscript, resolved against recorded
evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`
matches the value; `CITATION` means the sentence attributes it to a cited
source; `UNGROUNDED` means the manuscript asserts a measurement it cannot
support.

| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |
|:---|---:|---:|---:|---:|---:|
| autonomous_code_synthesis_and_self_healing_multi_agent_systems | 13 | 13 | 0 | 0 | 100.0% |
| review_architectural_dynamics_long_12_page | 26 | 23 | 3 | 0 | 100.0% |
| review_composable_ai_systems_for_trustworthy_agentic_pipelines | 116 | 0 | 0 | 116 | 0.0% |
| review_continual_safety_alignment_in_vision_language_models | 39 | 0 | 0 | 39 | 0.0% |
| review_enterprise_adoption_of_multi_agent_ai_systems_infr | 25 | 23 | 2 | 0 | 100.0% |
| review_enterprise_genai_roi | 6 | 6 | 0 | 0 | 100.0% |
| review_spatio_temporal_grounding_in_video_question_answering | 85 | 0 | 0 | 85 | 0.0% |
| review_symbol_graph_rag_vs_qlora_swe_bench_lite | 11 | 11 | 0 | 0 | 100.0% |
| review_trustworthy_multi_agent_systems_formal_verification | 6 | 5 | 1 | 0 | 100.0% |

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
- **L370** `N = 8,600` — We evaluate the CAS framework across four distinct enterprise task suites totaling $N = 8,600$ multi-step workflows:
- **L371** `N = 2,400` — **SWE-bench Multi-Repo Repair ($N = 2,400$):** Multi-file issue resolution requiring AST parsing, patch generation, and regression testing [[arxiv_240
- **L372** `N = 2,200` — **Financial Compliance & Regulatory Auditing ($N = 2,200$):** Multi-hop document extraction requiring strict numerical grounding and SEC filing invari
- **L373** `N = 2,000` — **Distributed Clinical Pathway Synthesis ($N = 2,000$):** Electronic health record synthesis requiring strict HIPAA privacy constraints and drug-inter
- **L374** `N = 2,000` — **Autonomous Cloud Infrastructure Remediation ($N = 2,000$):** Live Kubernetes microservice incident triage requiring root-cause diagnosis and non-des
- **L397** `N = 8,600` — **Table 1: Multi-Domain Benchmark Results Across $N = 8,600$ Enterprise Workflows**
- **L401** `61.2%` — 61.2%
- **L401** `54.3%` — 54.3%
- **L401** `28.4%` — 28.4%
- **L401** `24.8s` — 24.8s
- **L402** `68.7%` — 68.7%
- **L402** `49.1%` — 49.1%
- **L402** `34.1%` — 34.1%
- **L402** `31.2s` — 31.2s
- **L403** `77.4%` — 77.4%
- **L403** `79.2%` — 79.2%
- **L403** `12.3%` — 12.3%
- **L403** `18.6s` — 18.6s
- **L404** `92.6%` — **92.6%**
- **L404** `98.4%` — **98.4%**
- **L404** `0.8%` — **0.8%**
- **L404** `6.7s` — **6.7s**
- **L406** `p < 0.001` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L406** `d = 1.08` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L406** `t(8598) = 21.43` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L406** `15.2\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L406** `1.1\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L409** `28.4\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L409** `0.8\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L410** `51.8\%` — **Compute Efficiency:** By terminating invalid reasoning branches at Tier 3 contracts rather than looping through 10+ open-ended LLM reflection passes

## review_continual_safety_alignment_in_vision_language_models — 39 ungrounded

- **L31** `p < 0.001` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `N = 14,850` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `93.4\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L31** `99.2\%` — Through extensive meta-analysis across four standard multimodal safety benchmarks ($N = 14,850$ test probes), we prove that gradient-constrained sampl
- **L179** `N = 1,214` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L179** `N = 486` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L179** `N = 168` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L179** `N = 38` — Following automated deduplication ($N = 1,214$), abstract screening ($N = 486$), and full-text methodological audit ($N = 168$), a final core corpus o
- **L198** `44.2\%` — Unconstrained Full SFT & Low ($1.0\times$) & Baseline ($1.0\times$) & No & 44.2\% & Catastrophic alignment collapse \\
- **L199** `68.5\%` — LoRA / PEFT Adapter & Low ($1.1\times$) & Low ($0.1\times$) & No & 68.5\% & Subspace leakage into shared bases \\
- **L200** `88.7\%` — Dark Experience Replay & High ($2.4\times$) & High ($1.8\times$) & Yes (Replay Buffer) & 88.7\% & Heavy memory \& data privacy burden \\
- **L201** `89.4\%` — Gradient Projection Surgery & Very High ($3.1\times$) & Medium ($1.3\times$) & Yes (Reference Grad) & 89.4\% & Quadratic gradient inner products \\
- **L202** `76.1\%` — Representation Steering & Low ($1.05\times$) & Low ($1.0\times$) & No & 76.1\% & Fails under complex visual jailbreaks \\
- **L203** `93.4\%` — \textbf{Gradient Sample Selection (Ours)} & \textbf{Low ($1.15\times$)} & \textbf{Baseline ($1.0\times$)} & \textbf{No} & \textbf{93.4\%} & Requires s
- **L244** `N = 14,850` — To rigorously evaluate safety retention and task performance, we utilize four primary empirical benchmarks encompassing $N = 14,850$ multimodal test e
- **L254** `10\%` — Dark Experience Replay (DER++): Replaying $10\%$ historical safety alignment batches during task adaptation [[arxiv_2406.04028]].
- **L268** `N = 14,850` — \caption{Comprehensive Main Results across Multimodal Safety Benchmarks and Downstream Task Accuracy ($N = 14,850$)
- **L287** `6.2\%` — As demonstrated in Table \ref{tab:main_results}, unconstrained full fine-tuning causes an alarming collapse in safety performance, with attack vulnera
- **L287** `58.4\%` — As demonstrated in Table \ref{tab:main_results}, unconstrained full fine-tuning causes an alarming collapse in safety performance, with attack vulnera
- **L287** `89.2\%` — While DER++ preserves safety effectively ($89.2\%$), it requires continuous access to proprietary safety alignment data
- **L287** `93.8\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L287** `7.8\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L287** `0.6\%` — In contrast, our gradient-based sample selection achieves $93.8\%$ safety on VLGuard and suppresses AdvVQA ASR to $7.8\%$, while trailing unconstraine
- **L290** `30\%` — To analyze the sensitivity of the gradient filtering cutoff, Table \ref{tab:ablation_alpha} details model performance as the filtering quantile $(1-\a
- **L301** `100\%` — 1.00 (Full Dataset) & 100\% & 46.2 & 58.4 & 84.2 \\
- **L302** `95\%` — 0.95 & 95\% & 68.4 & 34.2 & 84.0 \\
- **L303** `90\%` — 0.90 & 90\% & 86.7 & 16.1 & 83.9 \\
- **L304** `85\%` — \textbf{0.85 (Optimal)} & \textbf{85\%} & \textbf{93.8} & \textbf{7.8} & \textbf{83.6} \\
- **L305** `80\%` — 0.80 & 80\% & 94.1 & 7.2 & 81.8 \\
- **L306** `70\%` — 0.70 & 70\% & 94.6 & 6.5 & 77.4 \\
- **L311** `15\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L311** `95\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L311** `20\%` — The ablation confirms that filtering the top $15\%$ high-gradient instances ($(1-\alpha) = 0.85$) represents the Pareto-optimal operating point, captu
- **L335** `0 GB` — Full Fine-Tuning & 48.2 & 142 & 0 GB \\
- **L336** `12 GB` — Dark Experience Replay & 74.6 & 318 & 12 GB (Replay Buffer) \\
- **L337** `8 GB` — Gradient Projection (GPM) & 82.4 & 485 & 8 GB (Feature Bases) \\
- **L338** `0 GB` — \textbf{Gradient Selection (Ours)} & \textbf{49.1} & \textbf{156} & \textbf{0 GB} \\
- **L369** `93.8\%` — We proved theoretically and verified empirically across $14,850$ multimodal benchmark interactions that data-centric gradient sample selection retains
- **L369** `98.9\%` — We proved theoretically and verified empirically across $14,850$ multimodal benchmark interactions that data-centric gradient sample selection retains

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
- **L392** `N = 42,000` — We evaluate DST-DR across eight standard video reasoning benchmarks totaling $N = 42,000$ test queries:
- **L394** `N = 42,000` — **Table 1: Benchmark Dataset Characteristics Across $N = 42,000$ Probes**
- **L398** `180 s` — 180 s
- **L399** `120 s` — 120 s
- **L400** `44 s` — 44 s
- **L401** `10 s` — 10 s
- **L402** `15 s` — 15 s
- **L403** `3 s` — 3 s
- **L404** `25 s` — 25 s
- **L405** `300 s` — 300 s
- **L437** `p < 0.001` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L437** `d = 0.89` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L437** `t(41998) = 16.84` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L437** `5.2\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L437** `0.6\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L440** `5.2\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L440** `6.4\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L440** `6.1\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L441** `78.7\%` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L441** `38.4\%` — dense**, and **$38.4\%$ reduction vs
- **L442** `54.7\%` — **Egocentric Mastery:** On Ego4D (fine-grained tool manipulation across 5-minute video streams), DST-DR achieves $54.7\%$ accuracy, proving robust spa
- **L450** `N = 6,500` — **Table 3: Next-QA Accuracy Breakdown by Reasoning Category ($N = 6,500$)**
- **L454** `54.2%` — 54.2%
- **L454** `48.1%` — 48.1%
- **L454** `66.9%` — 66.9%
- **L454** `56.4%` — 56.4%
- **L455** `59.8%` — 59.8%
- **L455** `53.4%` — 53.4%
- **L455** `73.1%` — 73.1%
- **L455** `62.1%` — 62.1%
- **L456** `64.1%` — 64.1%
