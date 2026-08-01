import re
from typing import List, Dict, Any

class TopicRecommenderService:
    def __init__(self):
        self.curated_topics = [
            {
                "id": "enterprise-genai-roi",
                "title": "Systematic Review & Meta-Taxonomy of Generative AI in Enterprise Workflows: Empirical Evidence, Economic Limits, Skill Equalization, and Task Boundary Frontiers",
                "domain": "AI & Enterprise Economics",
                "impact_score": "98/100",
                "target_venue": "IEEE TKDE / MIS Quarterly",
                "summary": "Synthesizes empirical RCT field studies (N>5,000), skill equalization across novice/senior workers, task boundary fragility (-19% accuracy drop outside frontier), and TRiSM governance.",
                "core_keywords": ["generative-ai", "enterprise-workflows", "empirical-productivity", "jagged-frontier", "trism-governance"],
                "estimated_corpus_size": "20-30 papers"
            },
            {
                "id": "test-time-compute-reasoning",
                "title": "Test-Time Compute, Inference Scaling Laws, and Search-Guided Reasoning in Large Language Models: A Systematic Survey",
                "domain": "Machine Learning & LLM Systems",
                "impact_score": "96/100",
                "target_venue": "ACM Computing Surveys / NeurIPS",
                "summary": "Investigates inference-time compute scaling (MCTS, Process Reward Models, self-consistency) vs pre-training parameter scaling laws, evaluating accuracy vs latency tradeoffs.",
                "core_keywords": ["test-time-compute", "inference-scaling", "process-reward-models", "mcts", "reasoning-llms"],
                "estimated_corpus_size": "25-35 papers"
            },
            {
                "id": "sparse-autoencoders-interpretability",
                "title": "Mechanistic Interpretability via Sparse Autoencoders: Feature Extraction, Circuit Discovery, and Safety Steering in Frontier Models",
                "domain": "AI Safety & Interpretability",
                "impact_score": "95/100",
                "target_venue": "Nature Machine Intelligence / ICML",
                "summary": "Audits monosemantic feature extraction, polysemanticity disentanglement, circuit discovery, and SAE-based steering vectors for safety guardrails.",
                "core_keywords": ["mechanistic-interpretability", "sparse-autoencoders", "sae", "circuit-discovery", "concept-steering"],
                "estimated_corpus_size": "20-25 papers"
            },
            {
                "id": "multi-agent-orchestration-security",
                "title": "Architectures, Communication Protocols, and Rejection Vulnerabilities of Autonomous Multi-Agent Systems in Regulated Enterprise Domains",
                "domain": "Distributed AI & Agentic Systems",
                "impact_score": "94/100",
                "target_venue": "IEEE Transactions on Autonomous Mental Development",
                "summary": "Evaluates multi-agent role decomposition, consensus protocols, infinite loop deadlocks, indirect prompt injection risks, and EU AI Act compliance.",
                "core_keywords": ["multi-agent-systems", "agentic-workflows", "consensus-protocols", "prompt-injection", "eu-ai-act"],
                "estimated_corpus_size": "25-30 papers"
            },
            {
                "id": "onpremise-slm-privacy-opex",
                "title": "Quantized Small Language Models (SLMs) vs. Proprietary Cloud APIs: A Comparative Empirical Benchmark of Privacy, Latency, and Token OpEx",
                "domain": "HPC Systems & Enterprise Privacy",
                "impact_score": "92/100",
                "target_venue": "ACM Transactions on Computer Systems (TOCS)",
                "summary": "Compares 8B-70B open-weights SLMs (Llama-3.3, Qwen-2.5) on local vLLM / FlashAttention-2 clusters against proprietary frontier API endpoints.",
                "core_keywords": ["slm", "quantization", "vllm", "privacy", "opex-optimization"],
                "estimated_corpus_size": "20-25 papers"
            }
        ]

    def list_curated_topics(self) -> List[Dict[str, Any]]:
        """Returns the list of high-impact research topics."""
        return self.curated_topics

    def get_topic_by_id(self, topic_id: str) -> Dict[str, Any]:
        """Retrieves details for a specific topic."""
        for t in self.curated_topics:
            if t["id"] == topic_id:
                return t
        return self.curated_topics[0]
