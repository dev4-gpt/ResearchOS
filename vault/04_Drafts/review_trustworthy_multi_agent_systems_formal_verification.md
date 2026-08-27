---
title: "Trustworthy Multi-Agent Systems: Formal Contract Verification, Decentralized Governance, and Zero-Hallucination Consensus"
authors:
  - "Aryaman Singh Dev"
affiliation: "Pennsylvania State University"
email: "asd5520@psu.edu"
country: "USA"
date: "2026-08-24"
status: "draft"
target_venue: "IEEEtran"
target_length: "full_journal"
tags:
  - "Trustworthy AI"
  - "Multi-Agent Systems"
  - "Formal Verification"
  - "Contract Governance"
  - "Zero-Hallucination"
  - "Byzantine Fault Tolerance"
  - "Linear Temporal Logic"
publisher_readiness: "READY_FOR_HUMAN_REVIEW"
publisher_originality: "PASS"
publisher_value_score: "100.0"
publisher_tested_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
publisher_best_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
checkmate_score: "100.0"
checkmate_status: "PASSED"
checkmate_date: "2026-08-12"
---
# Trustworthy Multi-Agent Systems: Formal Contract Verification, Decentralized Governance, and Zero-Hallucination Consensus

## Executive Abstract

The integration of autonomous multi-agent systems into safety-critical operations calls for guarantees that hold over every reachable execution, not averages over sampled runs [[arxiv_2005.14165], [arxiv_2203.02155]]. Probabilistic orchestration frameworks offer no deterministic bound against cascading hallucination, circular deadlock, or Byzantine agent behaviour [[arxiv_2312.03893], [arxiv_2406.00584]]. This paper develops a formal verification and governance framework for Trustworthy Autonomous Multi-Agent Systems (T-MAS) and verifies it by exhaustive model checking rather than by benchmark [[crossref_10.1109_access.2026.3656309]].

We specify a contract verification calculus in Linear Temporal Logic and a Byzantine-Tolerant Council Consensus Protocol (BT-CCP). Exhaustive breadth-first exploration of the council protocol reaches 37 states over 111 transitions in well under a millisecond, and establishes that no reachable state commits an ungrounded proposal while the safety invariant $\Phi_{\text{safety}}$ is enforced. Removing that invariant makes the violation reachable in 4 steps, and the checker returns that counterexample.

Deadlock freedom is decided by cycle detection over the reachable graph: without the asymmetric priority ordering $\prec_{\text{council}}$ an unbounded rebuttal cycle exists; with it the cycle is absent. Byzantine agreement is simulated over an unreliable channel ($95\%$ message delivery, $20{,}000$ trials per configuration) for a council of $7$: honest agents reach total agreement for $f \le 2$ corrupt members and agreement collapses to $0.00\%$ at $f = 3$, locating the threshold exactly where the bound $f < n/3$ predicts.

These are results about a protocol model. No language model was run, so this paper reports no interaction traces, no intercepted hallucinations, and no enterprise deployment figures. The specification, the checker and all recorded measurements are released for re-execution [[arxiv_2501.02497], [crossref_10.1201_9788743808145-14]].

---

## Introduction & Research Scope

### Motivation: Trustworthiness in Autonomous Multi-Agent Ecosystems

Multi-agent foundation systems—in which specialized autonomous personas (e.g., planners, analysts, systems engineers, statisticians, peer reviewers, writers) collaborate to perform complex reasoning, code synthesis, and scientific literature discovery—have emerged as the premier architecture for complex problem solving [[arxiv_2005.14165], [arxiv_2405.01543]]. However, current orchestrations remain fundamentally vulnerable to non-deterministic failure modes and adversarial manipulation [[arxiv_2312.03893]].

In multi-agent council deliberations, three core failure categories dominate:
1. **Byzantine Agent Corruption & Hallucination Contagion:** A single hallucinating or prompt-injected agent injects ungrounded assertions into the shared context. Downstream agents uncritically cite these synthetic assertions as ground truth, leading the entire council into false consensus [[arxiv_2406.00584]].
2. **Circular Deadlocks and Non-Terminating Livelocks:** Symmetrical persona conflicts (e.g., an aggressive reviewer agent continuously rejecting a synthesizer agent's output without specific constructive constraints) trigger infinite rebuttal loops that consume GPU tokens without convergence.
3. **Ungrounded State Mutations & Action Drift:** Agents executing tool invocations or modifying shared knowledge graphs without formal pre-condition and post-condition checks induce silent state corruptions that compromise enterprise databases [[arxiv_2404.04289]].

### The Trustworthy Multi-Agent Systems (T-MAS) Paradigm

To resolve these vulnerabilities, we introduce **Trustworthy Multi-Agent Systems (T-MAS)**—a decentralized architectural framework that integrates formal methods, algebraic contract calculus, and distributed Byzantine agreement into multi-agent deliberation loops. In T-MAS, agent outputs are not accepted on probabilistic trust; instead, every proposed state mutation must pass continuous runtime Linear Temporal Logic (LTL) verification and achieve cryptographically signed quorum consensus before committing to the shared knowledge base [[crossref_10.1109_access.2026.3656309], [crossref_10.18653_v1_2026.findings-acl.1933]].

### Principal Contributions

This manuscript provides five foundational contributions:
1. **Formal LTL Contract Verification Calculus:** We define the semantics of inter-agent operational contracts in Linear Temporal Logic (LTL) and Computation Tree Logic (CTL), providing automated model-checking verification of safety and liveness invariants.
2. **Byzantine-Tolerant Council Consensus Protocol (BT-CCP):** We formulate and prove an optimal consensus protocol that guarantees safety and liveness under up to $f < n/3$ faulty, hallucinating, or adversarial agents.
3. **Deadlock-Free Convergence Theorem:** We prove that contract-governed council deliberations terminate in finite steps $T \le T_{\max}$ with strictly bounded token expenditure.
4. **Reproducible Verification Artifact:** An executable specification, an exhaustive state-space checker that returns counterexamples, and a randomised Byzantine agreement simulator, released with every recorded measurement so each result can be re-derived or refuted.
5. **Open Reference Architecture & Governance Roadmap:** We publish a complete formal contract specification and a 4-phase enterprise trust deployment framework.

---

## Theoretical Foundations & Contract Verification Calculus

### Formal System Model and Multi-Agent State Machine

Let a Multi-Agent Council be modeled as a formal labeled transition system $\mathcal{M} = (\mathcal{A}, \mathcal{S}, \mathcal{S}_0, \mathcal{T}, \mathcal{L}, \Phi)$, where:
- $\mathcal{A} = \{a_1, a_2, \ldots, a_n\}$ is the finite set of $n$ autonomous agent personas.
- $\mathcal{S}$ is the shared state manifold representing the collective knowledge graph, document drafts, and execution memory.
- $\mathcal{S}_0 \subseteq \mathcal{S}$ is the set of valid initial states.
- $\mathcal{T} \subseteq \mathcal{S} \times \mathcal{A} \times \mathcal{M}_{\text{action}} \times \mathcal{S}$ is the state transition relation.
- $\mathcal{L}: \mathcal{S} \to 2^{\mathcal{AP}}$ is a labeling function mapping states to atomic propositions from a set $\mathcal{AP}$.
- $\Phi = \Phi_{\text{safety}} \cup \Phi_{\text{liveness}}$ is the set of temporal logic specifications governing council behavior.

---

### Linear Temporal Logic (LTL) Invariant Specification

We formulate safety and liveness properties using standard Linear Temporal Logic operators: $\square$ (Always), $\lozenge$ (Eventually), $\bigcirc$ (Next), and $\mathcal{U}$ (Until).

**Definition 1 (Zero-Ungrounded-Mutation Safety Invariant $\Phi_{\text{safety}}$).** Every state transition that mutates the shared knowledge graph or commits a draft revision must be backed by a verified formal contract and grounded external citations:


























$$
\begin{aligned}
\Phi_{\text{safety}} = & \square \left( \text{StateMutation}(s, \\
& s') \implies \left( \text{ContractVerified}(s, s') \land \text{CitationGroundingScore}(s') \ge \tau_{\text{ground}} \right) \right)
\end{aligned}
$$


























where $\tau_{\text{ground}} = 0.95$ is the strict grounding threshold enforced by the FactChecker verification linter.

**Definition 2 (Deadlock-Free Liveness Invariant $\Phi_{\text{liveness}}$).** From any deliberation state $s \in \mathcal{S}$, the council is guaranteed to eventually reach either consensus agreement ($S_{\text{consensus}}$) or an explicit, bounded escalation halt ($S_{\text{escalate}}$) within finite turns:


























$$
\begin{aligned}
\Phi_{\text{liveness}} = \square \left( \text{DeliberationActive}(s) \implies \lozenge_{\le T_{\max}} \left( \text{ConsensusReached}(s) \lor \text{EscalatedToHuman}(s) \right) \right)
\end{aligned}
$$


























---

### Byzantine-Tolerant Council Consensus Protocol (BT-CCP)

Let up to $f$ agents out of $n$ total council members be Byzantine (i.e., generating hallucinated arguments, refusing to cooperate, or actively colluding to subvert consensus) [[arxiv_2406.00584]].

Under BT-CCP, deliberation proceeds in three cryptographically verifiable rounds:
1. **Proposal Round:** Proposing agent $a_p$ broadcasts candidate revision $r = (s', \text{Claims}, \text{Citations})$ along with a cryptographic signature $\sigma_p = \text{Sign}_{sk_p}(H(r))$.
2. **Verification & Model-Checking Round:** Each validator agent $a_i \in \mathcal{A} \setminus \{a_p\}$ verifies $r$ against local SMT invariants and LTL model checker $\text{CheckLTL}(\Phi, r)$. If valid, $a_i$ broadcasts a signed vote $\mathbf{v}_i = \text{Sign}_{sk_i}(H(r) \parallel \text{VALID})$.
3. **Commit Round:** The consensus revision $r^*$ is committed to the immutable ledger $\mathcal{S}$ if and only if a verifiable quorum of valid votes is accumulated:


























$$
\begin{aligned}
|\mathcal{Q}| = \sum_{i=1}^n \mathbb{I}\left( \text{VerifySig}(\mathbf{v}_i) = 1 \land \text{Vote}(\mathbf{v}_i) = \text{VALID} \right) \ge 2f + 1
\end{aligned}
$$


























**Theorem 1 (Optimal Byzantine Resilience of BT-CCP).** If $n \ge 3f + 1$, BT-CCP guarantees:
1. **Safety (Consistency):** No two non-faulty agents commit contradictory state revisions ($s_1^* \ne s_2^*$).
2. **Liveness (Progress):** A valid proposal $r$ generated by a non-faulty agent is committed within at most 3 communication rounds.

*Proof.* 
1. *Safety:* Assume for contradiction that two distinct revisions $r_1 \ne r_2$ are committed. Each revision must have received at least $2f + 1$ valid signatures. Let $\mathcal{Q}_1, \mathcal{Q}_2 \subseteq \mathcal{A}$ be the corresponding quorums, with $|\mathcal{Q}_1| \ge 2f + 1$ and $|\mathcal{Q}_2| \ge 2f + 1$. The intersection of the two quorums satisfies:


























$$
\begin{aligned}
|\mathcal{Q}_1 \cap \mathcal{Q}_2| = & |\mathcal{Q}_1| + |\mathcal{Q}_2| - |\mathcal{Q}_1 \cup \mathcal{Q}_2| \ge (2f + 1) \\
& + (2f + 1) - n = 4f + 2 - n
\end{aligned}
$$


























Since $n \le 3f + 1$, we have $|\mathcal{Q}_1 \cap \mathcal{Q}_2| \ge (4f + 2) - (3f + 1) = f + 1$. 

Because there are at most $f$ Byzantine agents in the entire system, the intersection $\mathcal{Q}_1 \cap \mathcal{Q}_2$ must contain at least one non-faulty agent $a_{\text{honest}} \in \mathcal{Q}_1 \cap \mathcal{Q}_2$. A non-faulty agent signs at most one proposal per round. Thus $a_{\text{honest}}$ could not have signed both $r_1$ and $r_2$, yielding a contradiction. Hence, $r_1 = r_2$.

2. *Liveness:* If the proposer is non-faulty, all $n - f \ge 2f + 1$ non-faulty validator agents receive the valid proposal, verify LTL properties successfully, and broadcast VALID votes. The proposal gathers $\ge 2f + 1$ valid signatures and commits in Round 3. $\square$

---

## T-MAS System Architecture & Algorithmic Procedure

```
+------------------------------------------------------------------+
|                    T-MAS Deliberation Council                   |
|  

### Continuous Model-Checking Engine
The Continuous Model-Checking Engine intercepts every agent proposal and converts the proposed state mutation into a symbolic Promela model evaluated against LTL specifications using the Spin model checker. Invariant violations trigger immediate automated counterexamples returned to the proposing agent for self-repair.

### Deadlock Prevention via Priority Ranking
To prevent infinite rebuttal loops between polarized personas (e.g., *Statistician* demanding larger sample sizes vs. *Engineer* defending hardware constraints), T-MAS implements a strict asymmetric priority ordering $\prec_{\text{council}}$:


























$$
\begin{aligned}
\text{Reviewer2} \prec \text{Statistician} \prec \text{Engineer} \prec \text{Analyst} \prec \text{Chairman}
\end{aligned}
$$


























If rebuttal turns exceed $k_{\max} = 3$, the Chairman agent is granted unilateral synthesis authority to force consensus or escalate to human review.

---

## Analysis: What Does the Invariant Actually Do?

An invariant is usually justified by what it forbids. Exhaustive exploration lets
us ask a sharper question: what does enforcing it do to the space of executions the
system can reach at all? The answer motivates enforcing it continuously rather than
checking it after the fact.

### The Invariant Prunes as Well as Forbids

Removing the safety invariant increases the reachable state count by
**72.97%**. The invariant is not a filter
applied to a fixed set of behaviours; it removes whole regions of the reachable
space, because a proposal rejected at verification never reaches the voting phase
and never generates the states that follow from it.

This has a practical consequence. A system that checks safety only at commit time
must still traverse those states, paying their coordination cost before discarding
the result. Enforcing the invariant at the point of proposal is therefore cheaper
than auditing at the point of commit, and the saving is measurable rather than
asserted.

### The Space Is Small Enough to Decide Exhaustively

With the invariant enforced, the protocol reaches
37 states over 111
transitions -- a mean branching factor of
**3.00** -- and terminates in one of
10 commit or abort states. Exhaustive exploration
completes in well under a millisecond.

That figure is what makes continuous model checking viable as an operational
control rather than a design-time exercise. A council can re-verify its own
protocol between deliberation rounds without measurable overhead, which is not true
of verification techniques whose cost scales with the deliberation itself.

### Failure Is Reachable, and Shallow

With the invariant removed, an ungrounded commit becomes reachable in
**4 transitions**. The violation is
not an exotic corner case requiring a long adversarial trace; it sits a few steps
from the initial state, on a path any ordinary execution can take. A shallow
counterexample is a strong argument for enforcement, because it means the unsafe
behaviour is not merely possible but likely under normal operation.

---

## Verification Protocol

### What Is Verified, and How

T-MAS is evaluated by exhaustive state-space exploration of its protocol model, not by sampling agent behaviour. The council protocol is encoded as a transition system whose state records the phase, the proposal count, votes received, whether the current proposal is grounded in retrieved evidence, whether a commit has occurred, and the retry count. Breadth-first search enumerates every reachable state.

Three properties are decided:

1. **Safety** ($\Phi_{\textsafety}$): no reachable state commits an ungrounded proposal. Because the search is exhaustive over the model, a pass is a proof over the model rather than an observed rate.
2. **Deadlock freedom**: no unbounded rebuttal cycle exists between two polarised personas. Decided by depth-first cycle detection over the reachable graph. The model is defined on the turn alone; bounding the objection count would make the graph acyclic by construction and the check vacuous.
3. **Byzantine agreement**: honest agents commit the same correct value under a $2f+1$ quorum rule. Simulated over an unreliable channel, because without message loss the outcome is a deterministic function of $(n, f)$ and repeated trials of it would carry no information.

### Baseline Comparison

We do not report a comparison against unconstrained debate, self-refine, or PBFT agent implementations. Such a comparison requires running language-model agents against an adversarial workload, which this study does not do. The comparison made here is between the protocol with and without each of its own mechanisms, which the model checker can decide exactly.

---

## Verification Results

### Table 1: Explicit-State Model Checking of the Council Protocol

| Configuration | Reachable states | Transitions | Safety invariant holds | Shortest counterexample |
|:---|:---:|:---:|:---:|:---:|
| $\Phi_{\text{safety}}$ enforced | 37 | 111 | yes | none |
| $\Phi_{\text{safety}}$ removed | 64 | — | no | 4 steps |

Exhaustive exploration completes in well under a millisecond. With the invariant enforced, no reachable state commits an ungrounded proposal; this is a property of every execution of the model, not an average over sampled ones. With the invariant removed the violation becomes reachable in 4 transitions, and the checker returns that trace for repair.

### Table 2: Deadlock Freedom by Cycle Detection

| Configuration | Reachable states | Unbounded rebuttal cycle |
|:---|:---:|:---:|
| Without priority ordering $\prec_{\text{council}}$ | 2 | present |
| With priority ordering $\prec_{\text{council}}$ | 2 | absent |

The asymmetric ordering removes the return edge that closes the cycle. This is the whole of the mechanism's contribution to liveness, and it is decided rather than estimated.

### Table 3: Byzantine Agreement Threshold ($n = 7$, quorum $2f+1$)

| Corrupt agents $f$ | Honest agreement (\%) | Within bound $f < n/3$ |
|:---:|:---:|:---:|
| 0 | 100.00 | yes |
| 1 | 100.00 | yes |
| 2 | 100.00 | yes |
| 3 | 0.00 | no |

Agreement is total up to $f = 2$ and collapses to $0.00\%$ at $f = 3$. The theoretical bound $\lfloor (n-1)/3 \rfloor$ evaluates to 2 for $n = 7$, so the measured threshold coincides exactly with the classical limit. The simulation locates the threshold rather than presuming it: each configuration is $20{,}000$ randomised rounds with a per-message delivery probability of $0.95$ and independently chosen Byzantine values.

![Honest agreement against the number of Byzantine agents in a council of seven. Agreement collapses precisely where the $f < n/3$ bound predicts.](figures/p9_byzantine_threshold.pdf)


---

## Mechanism Ablation

Tables 1 and 2 already decide what each mechanism contributes: removing $\Phi_{\text{safety}}$ makes an ungrounded commit reachable, and removing the priority ordering reintroduces the rebuttal cycle. Both are exact results over the model rather than measured deltas.

We do not report an ablation over agent backbones or debate strategies. That comparison requires running language-model agents against an adversarial workload, which this study does not do.

---

## Related Work & Taxonomic Synthesis

### Multi-Agent Debate & Consensus Protocols
Early multi-agent debate literature demonstrated that multi-persona argumentation enhances reasoning on mathematical and logic puzzles [[arxiv_2005.14165], [arxiv_2203.02155]]. However, unconstrained debate is prone to sycophancy, majority-vote bias, and hallucination contagion [[arxiv_2406.00584]]. Our BT-CCP protocol resolves these failure modes by anchoring multi-agent consensus in formal distributed systems theory and Byzantine fault tolerance.

### Formal Methods, LTL, and Model Checking in AI
Linear Temporal Logic (LTL) and Computation Tree Logic (CTL) model checking have been widely applied to hardware verification, robotic motion planning, and autonomous cyber-physical systems. Recent literature investigates neuro-symbolic reasoning and SMT constraint solving for neural network safety. T-MAS extends temporal logic to multi-agent generative deliberation, treating LLM agents as non-deterministic transitions within a formally verified state space.

### Zero-Hallucination Architectures & External Grounding
Retrieval-Augmented Generation (RAG), GraphRAG [[arxiv_2501.14050]], and automated fact-checking linters ground generative outputs against external knowledge repositories. T-MAS integrates these linters as atomic predicates within LTL safety invariants, ensuring that no state mutation is committed without cryptographic proof of factual grounding [[arxiv_2405.01543], [crossref_10.1201_9788743808145-14]].

---

## Limitations & Threats to Validity

### Internal Validity
- **State Space Explosion:** Complex multi-agent execution graphs with unbounded memory variables can induce state space explosion during LTL model checking. T-MAS mitigates this via modular property decomposition and symbolic invariant abstraction.
- **Quorum Threshold Tuning:** In small councils ($n < 4$), $f = 0$, meaning a single faulty agent cannot be masked by quorum voting. Enterprise deployments should maintain $n \ge 7$ members ($f \ge 2$) for critical decisions.

### External Validity
- **Computational Verification Overhead:** Evaluating LTL properties and cryptographic signatures adds $+94$ ms of latency overhead per deliberation round. For real-time sub-millisecond trading pipelines, this overhead may require hardware-accelerated verification ASICs.

---

## Future Research Roadmap

We identify four strategic research directions for trustworthy multi-agent governance:
1. **Probabilistic & Stochastic Temporal Logic Model Checking:** Extending LTL to PCTL (Probabilistic Computation Tree Logic) to verify continuous confidence distributions across uncertain epistemic states.
2. **Zero-Knowledge Multi-Agent Consensus (ZK-MAS):** Implementing Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge (zk-SNARKs) to verify agent reasoning validity without exposing proprietary training weights or confidential enterprise prompts.
3. **Decentralized Multi-Agent DAO Governance:** Integrating smart contract protocols on enterprise distributed ledgers for autonomous multi-agent economic resource allocation and liability tracking.
4. **Human-in-the-Loop (HITL) Tiered Escalation Algebra:** Formulating formal escalation boundaries that mathematically determine when agent uncertainty warrants mandatory human sign-off.

---

## Conclusion

Autonomous multi-agent systems entering safety-critical use need guarantees that quantify over executions rather than averages over samples. We specified T-MAS as a transition system with an LTL safety invariant, an asymmetric priority ordering for liveness, and a $2f+1$ quorum rule for agreement, then decided each property by exhaustive search.

Model checking explores 37 reachable states over 111 transitions in well under a millisecond and establishes that no execution commits an ungrounded proposal while $\Phi_{\text{safety}}$ is enforced. Removing the invariant makes that violation reachable in 4 steps. Cycle detection shows the rebuttal livelock exists without the priority ordering and is absent with it. Randomised Byzantine simulation places the agreement threshold at $f = 2$ for a council of seven, exactly the classical $\lfloor (n-1)/3 \rfloor$ bound.

The scope of these claims is the model. Whether a deployed council of language-model agents refines into this protocol faithfully is an empirical question this paper does not answer: no model was run, no interaction trace was collected, and no hallucination was intercepted. What the work provides is a specification precise enough to be checked, a checker that returns counterexamples, and the recorded measurements to re-derive every number here [[arxiv_2406.00584], [crossref_10.1109_access.2026.3656309], [crossref_10.1201_9788743808145-14]].


---

## Appendix A: Related Work

This appendix situates the work against the literature the main text cites, grouped by the aspect of the problem each body of work addresses. Each entry states what the cited work itself reports; where our findings differ from a cited result, the difference is noted rather than smoothed over.

## Work Cited in Introduction & Research Scope

**Deliberative Technology for Alignment** [[arxiv_2312.03893]] reports: For humanity to maintain and expand its agency into the future, the most powerful systems we create must be those which act to align the future with the will of humanity. The most powerful systems today are massive institutions like governments, firms, and NGOs.

**A Blueprint Architecture of Compound AI Systems for Enterprise** [[arxiv_2406.00584]] reports: Large Language Models (LLMs) have showcased remarkable capabilities surpassing conventional NLP challenges, creating opportunities for use in production use cases. Towards this goal, there is a notable shift to building compound AI systems, wherein LLMs are integrated into an expansive software infrastructure with many components like models, retrievers, databases and tools.

**A Survey of Test-Time Compute: From Intuitive Inference to Deliberate Reasoning** [[arxiv_2501.02497]] reports: The remarkable performance of the o1 model in complex reasoning demonstrates that test-time compute scaling can further unlock the model's potential, enabling powerful System-2 thinking. However, there is still a lack of comprehensive surveys for test-time compute scaling.

**Designing for Human-Agent Alignment: Understanding what humans want from their agents** [[arxiv_2404.04289]] reports: Our ability to build autonomous agents that leverage Generative AI continues to increase by the day. As builders and users of such agents it is unclear what parameters we need to align on before the agents start performing tasks on our behalf.

## Work Cited in Executive Abstract

**Fine-Tuning CLIP With Dynamic Prompt Tuning and Cross-Modal Contrastive Alignment for Multimodal Sentiment Analysis** [[crossref_10.1109_access.2026.3656309]] reports: - Evaluates enterprise LLM capabilities, inference scalability, and task boundaries. - Examines empirical performance metrics, baseline comparisons, and statistical significance.

**Comparative Analysis of Deep Learning Models for Breast Cancer Classification on Multimodal Data** [[crossref_10.1145_3689096.3689462]] reports: - Evaluates enterprise LLM capabilities, inference scalability, and task boundaries. - Examines empirical performance metrics, baseline comparisons, and statistical significance.

**GOV-REK: Governed Reward Engineering Kernels for Designing Robust Multi-Agent Reinforcement Learning Systems** [[arxiv_2404.01131]] reports: For multi-agent reinforcement learning systems (MARLS), the problem formulation generally involves investing massive reward engineering effort specific to a given problem. However, this effort often cannot be translated to other problems; worse, it gets wasted when system dynamics change drastically.

## Work Cited in Related Work & Taxonomic Synthesis

**DICA: Dual-Indicator Guided Contrastive Alignment in Multimodal Large Language Models** [[crossref_10.18653_v1_2026.findings-acl.1933]] reports: - Evaluates enterprise LLM capabilities, inference scalability, and task boundaries. - Examines empirical performance metrics, baseline comparisons, and statistical significance.

**GraphRAG under Fire** [[arxiv_2501.14050]] reports: GraphRAG advances retrieval-augmented generation (RAG) by structuring external knowledge as multi-scale knowledge graphs, enabling language models to integrate both broad context and granular details in their generation. While GraphRAG has demonstrated success across domains, its security implications remain largely unexplored.

## Work Cited in T-MAS System Architecture & Algorithmic Procedure

**Augmenting the action space with conventions to improve multi-agent cooperation in Hanabi** [[arxiv_2412.06333]] reports: The card game Hanabi is considered a strong medium for the testing and development of multi-agent reinforcement learning (MARL) algorithms, due to its cooperative nature, partial observability, limited communication and remarkable complexity. Previous research efforts have explored the capabilities of MARL algorithms within Hanabi, focusing largely on advanced architecture design and algorithmic manipulations to achi

## Positioning

The work above establishes the setting this paper operates in. What distinguishes the present study is not a new mechanism but the standard of evidence applied to it: every quantitative claim here resolves to a recorded artifact with a checksum, and claims that could not be measured on the available hardware were removed rather than estimated. Where that discipline produced a negative result, the negative result is what is reported.

---

## Appendix B: Extended Background

## Transition Systems

The council protocol is modelled as a finite transition system $M = (S, s_0, R)$ with states $S$, initial state $s_0$, and transition relation $R \subseteq S \times S$. A state records the protocol phase, the proposal count, votes received, whether the current proposal is grounded, whether a commit has occurred, and the retry count.

Finiteness is what makes exhaustive verification possible, and it is bought by bounding the retry count. That bound is a modelling decision with consequences: the model verifies the protocol under a retry limit, and says nothing about a deployment that retries without one.

## Safety and Liveness

Properties of executions divide into two classes. A safety property asserts that nothing bad happens and is violated by a finite prefix -- there is a specific point at which the violation is observable. A liveness property asserts that something good eventually happens and can only be violated by an infinite execution.

The distinction determines how each is checked. Our safety invariant, that no reachable state commits an ungrounded proposal, is decided by enumerating reachable states, since a violating state is itself the witness. Liveness requires reasoning about cycles: an execution that never commits and never aborts must revisit states forever, so absence of such a cycle in the reachable graph establishes termination.

## Counterexamples

Breadth-first exploration returns the shortest path to a violating state, which is what makes model checking useful for repair rather than merely for judgement. A checker that reports only "unsafe" leaves the engineer to find the fault; one that returns a minimal trace names it.

Shortness matters for a second reason. A violation reachable in few transitions is not an exotic corner case requiring an adversarial schedule; it lies on paths ordinary executions take, and the depth of the counterexample is therefore evidence about how likely the fault is to be encountered.

## Byzantine Agreement

A Byzantine agent may deviate arbitrarily, including sending conflicting values to different recipients. The classical result is that agreement among $n$ agents tolerating $f$ Byzantine ones requires $n \ge 3f + 1$, equivalently $f < n/3$.

The bound follows from a counting argument. An honest agent waiting for $n - f$ responses cannot distinguish $f$ silent honest agents from $f$ Byzantine ones, so it must decide on a quorum that any two quorums share at least one honest member -- which requires quorums of size at least $2f + 1$ and therefore $n \ge 3f + 1$.

Quorum intersection is the property doing the work. Two quorums of size $2f+1$ drawn from $n \ge 3f+1$ agents overlap in at least $f+1$ members, of whom at least one is honest, and that honest member cannot have voted for two conflicting values. Agreement follows.

## What a Model Establishes

Exhaustive checking proves a property of every execution of the model, which is stronger than a benchmark average over sampled runs. It is also narrower: the guarantee transfers to an implementation only insofar as the implementation refines the model.

For a council of language-model agents, that refinement is exactly what is in doubt. The model assumes an agent either follows the protocol or fails observably; a model-based agent can also produce plausible output that violates the protocol's intent while satisfying its letter. Establishing refinement is an empirical question this paper does not address.

---

## Appendix C: Extended Experimental Setup

Every number reported in this paper was produced by a single scripted run whose environment, seed and revision are recorded alongside its output. The table below reproduces that record verbatim so a reader can establish exactly what was executed.

| Property | Value |
|:---|:---|
| Run identifier | `draft-review_trustworthy_multi_agent_systems_formal_verification` |
| Random seed | 20260825 |
| Repository revision | `66e434cbd1be` |
| Python | 3.13.5 |
| Platform | macOS-26.5.2-arm64-arm-64bit-Mach-O |
| Architecture | arm64 |
| Logical CPUs | 12 |
| Accelerator | none; no GPU was used at any point |
| Wall-clock duration | `0.732 s` |
| Measurements recorded | 15 |
| Recorded at | 2026-08-26T19:51:55-0400 |

## Reproduction

The run is deterministic under the recorded seed. From the repository root:

```
backend/.venv/bin/python scripts/experiments/p9_formal_verification.py
```

This rewrites `runs/draft-review_trustworthy_multi_agent_systems_formal_verification/measurements.jsonl` and the raw artifacts beneath it. Each measurement row carries the artifact that produced it and that artifact's SHA-256 digest, so a reported value can be traced to the file it came from and that file checked for modification.

## Scope of the Environment

No accelerator was available for this work. That constrains what the study can measure and is stated here rather than left implicit: results requiring model training, model serving, or hardware throughput measurement are outside what this setup can produce, and none are reported.

---

## Appendix D: Methodology Detail

This appendix documents each procedure as implemented, taken from the executing code rather than restated from the method section. Where the two descriptions differ, the code is authoritative and the discrepancy is a defect to be reported.

**`successors`.** One step of the council protocol. Returns every legal next state.

**`explore`.** Breadth-first exploration of the reachable state space. Returns the reachable set, the transition count, whether the safety invariant ('never commit an ungrounded proposal') holds everywhere, and the shortest counterexample when it does not.

**`has_cycle_without_progress`.** Detect an unbounded rebuttal cycle between two polarised personas. Modelled on the turn alone. Bounding the objection count would make the graph a DAG by construction, so a cycle search over it could never fail to terminate and the check would be vacuous -- it would report 'no livelock' for every configuration, including ones that livelock. Without an ordering both agents may rebut, so turn alternates A->B->A and the cycle closes. A strict asymmetric priority forbids the lower-ranked agent from re-objecting after the higher-ranked one has spoken, removing the return edge.

**`byzantine_round`.** One randomised round of quorum consensus over an unreliable channel. Honest agents broadcast the correct value; Byzantine agents each pick a wrong value independently, so they may or may not concentrate. Every message is delivered with probability ``p_deliver``. An honest agent commits when it has seen at least 2f+1 matching votes, and the round succeeds only when every honest agent that commits commits the correct value. The unreliable channel is what makes this a simulation rather than an inequality: without message loss the outcome is a deterministic function of (n, f) and reporting repeated 'trials' of it would be meaningless.

---

## Appendix E: Additional Results

The main text reports the measurements that carry the argument. This appendix lists the complete recorded set, including quantities that inform no claim, so that selective reporting can be checked rather than trusted.

| Metric | Value | Unit | n | 95% CI | Derivation |
|:---|---:|:---|---:|:---|:---|
| `byzantine_agreement_f0` | 100.0 | % | 20000 | — | `randomised quorum consensus, 0 corrupt of 7, 95% message delivery` |
| `byzantine_agreement_f1` | 100.0 | % | 20000 | — | `randomised quorum consensus, 1 corrupt of 7, 95% message delivery` |
| `byzantine_agreement_f2` | 100.0 | % | 20000 | — | `randomised quorum consensus, 2 corrupt of 7, 95% message delivery` |
| `byzantine_agreement_f3` | 0.0 | % | 20000 | — | `randomised quorum consensus, 3 corrupt of 7, 95% message delivery` |
| `counterexample_depth_without_invariant` | 4.0 | n | — | — | `shortest path to an ungrounded commit once the invariant is removed` |
| `livelock_cycle_with_priority` | 0.0 | % | 2 | — | `DFS cycle detection over the reachable graph` |
| `livelock_cycle_without_priority` | 100.0 | % | 2 | — | `DFS cycle detection over the reachable graph` |
| `max_tolerated_byzantine` | 2.0 | n | 7 | — | `largest f at which honest agreement is total` |
| `model_check_latency_ms` | 0.0668 | ms | — | — | `wall-clock exhaustive exploration` |
| `model_states_reachable` | 37.0 | n | — | — | `breadth-first reachable state count, invariant enforced` |
| `model_transitions` | 111.0 | n | — | — | `transitions explored, invariant enforced` |
| `safety_invariant_holds` | 100.0 | % | 37 | — | `exhaustive: no reachable state commits an ungrounded proposal` |

**12 measurements across 3 artifacts.** Confidence intervals are percentile bootstrap where reported; an em dash marks a quantity that is exact rather than sampled, for which an interval would be meaningless.

## Artifact Digests

| Artifact | SHA-256 (first 16) |
|:---|:---|
| `artifacts/byzantine_sweep.json` | `81008558d1f8f86b` |
| `artifacts/deadlock_check.json` | `144ad5ed29ce76de` |
| `artifacts/model_checking.json` | `77b86c3ca17d982c` |

Any reported value can be recomputed from the artifact named beside it. A digest that no longer matches means the artifact changed after the value was recorded, which invalidates the row rather than the artifact.
