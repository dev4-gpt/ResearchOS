# Claim Provenance Report

Every quantitative claim in each manuscript, resolved against recorded
evidence. `EXPERIMENT` means a measurement artifact in `runs/<run_id>/`
matches the value; `CITATION` means the sentence attributes it to a cited
source; `UNGROUNDED` means the manuscript asserts a measurement it cannot
support.

| Manuscript | Claims | Experiment | Citation | Ungrounded | Grounded % |
|:---|---:|---:|---:|---:|---:|
| autonomous_code_synthesis_and_self_healing_multi_agent_systems | 17 | 5 | 0 | 12 | 29.4% |
| review_architectural_dynamics_long_12_page | 27 | 23 | 4 | 0 | 100.0% |
| review_composable_ai_systems_for_trustworthy_agentic_pipelines | 9 | 9 | 0 | 0 | 100.0% |
| review_continual_safety_alignment_in_vision_language_models | 7 | 7 | 0 | 0 | 100.0% |
| review_enterprise_adoption_of_multi_agent_ai_systems_infr | 30 | 28 | 2 | 0 | 100.0% |
| review_enterprise_genai_roi | 6 | 6 | 0 | 0 | 100.0% |
| review_spatio_temporal_grounding_in_video_question_answering | 0 | 0 | 0 | 0 | 100.0% |
| review_symbol_graph_rag_vs_qlora_swe_bench_lite | 12 | 6 | 1 | 5 | 58.3% |
| review_trustworthy_multi_agent_systems_formal_verification | 8 | 7 | 1 | 0 | 100.0% |

## autonomous_code_synthesis_and_self_healing_multi_agent_systems — 12 ungrounded

- **L22** `97.89\%` — Syntactic validity is high across operators ($97.89\%$ to $100.00\%$), confirming that compilation alone is a weak filter
- **L22** `46.34\%` — A three-stage pre-filter -- compilation, static name binding, then Z3-SMT reachability -- rejects $46.34\%$ of candidates at a mean cost of $4.09$ ms 
- **L677** `97.89%` — **97.89%**
- **L683** `0.64%` — **0.64%** of what it sees.
- **L689** `35.26%` — least-filtered (35.26%) and most-filtered
- **L690** `64.62%` — (64.62%)
- **L775** `4.09 ms` — 4.09 ms/candidate
- **L790** `46.00\%` — Static name binding rejects 46.00\% of the candidates reaching it at negligible cost, while Z3-SMT reachability rejects 0.00\% of the candidates reach
- **L790** `4.09 ms` — On this corpus a two-stage filter is strictly preferable to the three-stage design we began with, and the mean pre-filter cost of 4.09 ms per candidat
- **L874** `46.34\%` — The pipeline rejects 46.34\% of candidates before any sandbox is started, at a mean cost of 4.09 ms each
- **L874** `46.00\%` — That saving is almost entirely attributable to static name binding, which rejects 46.00\% of the candidates reaching it
- **L874** `4.09 ms` — The pipeline rejects 46.34\% of candidates before any sandbox is started, at a mean cost of 4.09 ms each

## review_symbol_graph_rag_vs_qlora_swe_bench_lite — 5 ungrounded

- **L24** `d = -0.0137` — Symbol-graph diffusion is statistically indistinguishable from the BM25 baseline it re-ranks: MRR 0.8701 against 0.8739 ($\Delta = -0.0038$, Cohen's $
- **L24** `80.58\%` — Symbol-graph diffusion is statistically indistinguishable from the BM25 baseline it re-ranks: MRR 0.8701 against 0.8739 ($\Delta = -0.0038$, Cohen's $
- **L24** `81.55\%` — Symbol-graph diffusion is statistically indistinguishable from the BM25 baseline it re-ranks: MRR 0.8701 against 0.8739 ($\Delta = -0.0038$, Cohen's $
- **L313** `d = -0.0137` — Paired difference in MRR: $\Delta = -0.0038$, Cohen's $d = -0.0137$
- **L385** `d = -0.0137` — With hyperparameters selected on a held-out split and reported on 103 unseen queries, Personalized PageRank over a symbol graph scores MRR 0.8701 agai
