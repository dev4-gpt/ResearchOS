# Claim Provenance Report

Every quantitative claim in each manuscript, resolved against recorded
evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`
matches the value; `CITATION` means the sentence attributes it to a cited
source; `UNGROUNDED` means the manuscript asserts a measurement it cannot
support.

| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |
|:---|---:|---:|---:|---:|---:|
| autonomous_code_synthesis_and_self_healing_multi_agent_systems | 17 | 17 | 0 | 0 | 100.0% |
| review_architectural_dynamics_long_12_page | 27 | 23 | 4 | 0 | 100.0% |
| review_composable_ai_systems_for_trustworthy_agentic_pipelines | 116 | 0 | 0 | 116 | 0.0% |
| review_continual_safety_alignment_in_vision_language_models | 7 | 7 | 0 | 0 | 100.0% |
| review_enterprise_adoption_of_multi_agent_ai_systems_infr | 30 | 28 | 2 | 0 | 100.0% |
| review_enterprise_genai_roi | 6 | 6 | 0 | 0 | 100.0% |
| review_spatio_temporal_grounding_in_video_question_answering | 85 | 0 | 0 | 85 | 0.0% |
| review_symbol_graph_rag_vs_qlora_swe_bench_lite | 12 | 11 | 1 | 0 | 100.0% |
| review_trustworthy_multi_agent_systems_formal_verification | 8 | 7 | 1 | 0 | 100.0% |

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
- **L412** `N = 8,600` — We evaluate the CAS framework across four distinct enterprise task suites totaling $N = 8,600$ multi-step workflows:
- **L413** `N = 2,400` — **SWE-bench Multi-Repo Repair ($N = 2,400$):** Multi-file issue resolution requiring AST parsing, patch generation, and regression testing.
- **L414** `N = 2,200` — **Financial Compliance & Regulatory Auditing ($N = 2,200$):** Multi-hop document extraction requiring strict numerical grounding and SEC filing invari
- **L415** `N = 2,000` — **Distributed Clinical Pathway Synthesis ($N = 2,000$):** Electronic health record synthesis requiring strict HIPAA privacy constraints and drug-inter
- **L416** `N = 2,000` — **Autonomous Cloud Infrastructure Remediation ($N = 2,000$):** Live Kubernetes microservice incident triage requiring root-cause diagnosis and non-des
- **L439** `N = 8,600` — **Table 1: Multi-Domain Benchmark Results Across $N = 8,600$ Enterprise Workflows**
- **L443** `61.2%` — 61.2%
- **L443** `54.3%` — 54.3%
- **L443** `28.4%` — 28.4%
- **L443** `24.8s` — 24.8s
- **L444** `68.7%` — 68.7%
- **L444** `49.1%` — 49.1%
- **L444** `34.1%` — 34.1%
- **L444** `31.2s` — 31.2s
- **L445** `77.4%` — 77.4%
- **L445** `79.2%` — 79.2%
- **L445** `12.3%` — 12.3%
- **L445** `18.6s` — 18.6s
- **L446** `92.6%` — **92.6%**
- **L446** `98.4%` — **98.4%**
- **L446** `0.8%` — **0.8%**
- **L446** `6.7s` — **6.7s**
- **L448** `p < 0.001` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L448** `d = 1.08` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L448** `t(8598) = 21.43` — $p < 0.001$ across all metrics; Two-sample $t(8598) = 21.43$; Cohen's $d = 1.08$ (large effect)
- **L448** `15.2\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L448** `1.1\%` — Bootstrap 95% CI on WCR gain over StateGraph: $\Delta = +15.2\% \pm 1.1\%$ [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].
- **L451** `28.4\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L451** `0.8\%` — **Zero Hallucination Cascades:** CAS reduces hallucination cascade rates from $28.4\%$ (ReAct) to $0.8\%$, validating the Lyapunov error containment b
- **L452** `51.8\%` — **Compute Efficiency:** By terminating invalid reasoning branches at Tier 3 contracts rather than looping through 10+ open-ended LLM reflection passes

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
- **L440** `N = 42,000` — We evaluate DST-DR across eight standard video reasoning benchmarks totaling $N = 42,000$ test queries:
- **L442** `N = 42,000` — **Table 1: Benchmark Dataset Characteristics Across $N = 42,000$ Probes**
- **L446** `180 s` — 180 s
- **L447** `120 s` — 120 s
- **L448** `44 s` — 44 s
- **L449** `10 s` — 10 s
- **L450** `15 s` — 15 s
- **L451** `3 s` — 3 s
- **L452** `25 s` — 25 s
- **L453** `300 s` — 300 s
- **L485** `p < 0.001` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L485** `d = 0.89` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L485** `t(41998) = 16.84` — $p < 0.001$ across all benchmarks; Two-sample $t(41998) = 16.84$; Cohen's $d = 0.89$ (large effect)
- **L485** `5.2\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L485** `0.6\%` — Bootstrap 95% CI on ActivityNet-QA gain over PLLaVA: $\Delta = +5.2\% \pm 0.6\%$ [[crossref_10.1201_9788743808145-14], [arxiv_2501.02497]].
- **L488** `5.2\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L488** `6.4\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L488** `6.1\%` — **State-of-the-Art Accuracy:** DST-DR outperforms PLLaVA by **$+5.2\%$ on ActivityNet-QA**, **$+6.4\%$ on Next-QA**, and **$+6.1\%$ on Ego4D**, demons
- **L489** `78.7\%` — **Compute Efficiency:** DST-DR reduces cross-attention FLOPs from $5.58 \times 10^{12}$ (dense concatenation) to $1.19 \times 10^{12}$ (**$78.7\%$ red
- **L489** `38.4\%` — dense**, and **$38.4\%$ reduction vs
- **L490** `54.7\%` — **Egocentric Mastery:** On Ego4D (fine-grained tool manipulation across 5-minute video streams), DST-DR achieves $54.7\%$ accuracy, proving robust spa
- **L498** `N = 6,500` — **Table 3: Next-QA Accuracy Breakdown by Reasoning Category ($N = 6,500$)**
- **L502** `54.2%` — 54.2%
- **L502** `48.1%` — 48.1%
- **L502** `66.9%` — 66.9%
- **L502** `56.4%` — 56.4%
- **L503** `59.8%` — 59.8%
- **L503** `53.4%` — 53.4%
- **L503** `73.1%` — 73.1%
- **L503** `62.1%` — 62.1%
- **L504** `64.1%` — 64.1%
