"""
VenueAdvisorAgent — Multi-sub-agent system that recommends the best publication
venue for a confirmed research paper, based on paper content + user profile.

Agent Architecture:
  1. ProfileMatcherAgent  — reads user portfolio, expertise, O-1A goals
  2. VenueScorerAgent     — scores all venues on 5 axes per paper
  3. StrategyGeneratorAgent — writes personalized rationale for top venues

Produces a ranked venue list with scores, difficulty, O-1A value, and strategy.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv()


# ──────────────────────────────────────────────────────────────────────────────
# Static venue knowledge base
# ──────────────────────────────────────────────────────────────────────────────

VENUE_KNOWLEDGE = {
    "NeurIPS": {
        "full_name": "Conference on Neural Information Processing Systems",
        "type": "conference",
        "acceptance_rate": 0.26,
        "difficulty": "Very Hard",
        "page_limit": 9,
        "format": "Single-column, 10pt",
        "anonymized": True,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 5,
        "o1a_rationale": "Top-tier ML venue. Acceptance is primary evidence for 8 CFR §204.5(h)(3)(vi) Scholarly Articles.",
        "best_for": ["Deep Learning", "Reinforcement Learning", "Probabilistic Models", "Optimization", "ML Theory"],
        "citation_velocity": "very_high",
        "review_cycle": "Annual (May deadline)",
        "workshop_track": True,
        "strategic_tip": "Strong empirical results + theoretical foundations. Must beat SOTA baselines significantly.",
    },
    "ICML": {
        "full_name": "International Conference on Machine Learning",
        "type": "conference",
        "acceptance_rate": 0.32,
        "difficulty": "Hard",
        "page_limit": 8,
        "format": "Two-column, 10pt",
        "anonymized": True,
        "o1a_criterion": "original_contributions",
        "o1a_value": 4,
        "o1a_rationale": "Evidence for 8 CFR §204.5(h)(3)(v) Original Contributions of Major Significance.",
        "best_for": ["Optimization", "ML Theory", "Scalable Algorithms", "Statistical Learning"],
        "citation_velocity": "very_high",
        "review_cycle": "Annual (Jan deadline)",
        "workshop_track": True,
        "strategic_tip": "Theoretical rigor is prized. Proofs, convergence guarantees, and algorithmic novelty are expected.",
    },
    "CVPR": {
        "full_name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
        "type": "conference",
        "acceptance_rate": 0.25,
        "difficulty": "Very Hard",
        "page_limit": 8,
        "format": "Two-column, 10pt, line-numbered",
        "anonymized": True,
        "o1a_criterion": "published_media",
        "o1a_value": 4,
        "o1a_rationale": "High media coverage drives 8 CFR §204.5(h)(3)(iii) Published Material About the Alien criterion.",
        "best_for": ["Computer Vision", "Multimodal Learning", "Image Generation", "Video Understanding", "3D Vision"],
        "citation_velocity": "very_high",
        "review_cycle": "Annual (Nov deadline)",
        "workshop_track": True,
        "strategic_tip": "Strong visualizations essential. Hugging Face demo + GitHub release maximizes citations.",
    },
    "ACL": {
        "full_name": "Association for Computational Linguistics (ACL / ARR)",
        "type": "conference",
        "acceptance_rate": 0.28,
        "difficulty": "Hard",
        "page_limit": 8,
        "format": "Two-column ACL style",
        "anonymized": True,
        "o1a_criterion": "judging_work_of_others",
        "o1a_value": 4,
        "o1a_rationale": "NLP venue membership leads to reviewer invitations for 8 CFR §204.5(h)(3)(iv) Judging Work of Others.",
        "best_for": ["Natural Language Processing", "Language Models", "Machine Translation", "Text Generation", "Dialogue"],
        "citation_velocity": "high",
        "review_cycle": "Rolling (ARR every 2 months)",
        "workshop_track": True,
        "strategic_tip": "Language-specific benchmarks are mandatory. Reproducibility checklist must be fully completed.",
    },
    "IEEEtran": {
        "full_name": "IEEE Transactions (TKDE / TPAMI / Access)",
        "type": "journal",
        "acceptance_rate": 0.65,
        "difficulty": "Moderate",
        "page_limit": None,
        "format": "Two-column IEEE journal, 10-25+ pages",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 3,
        "o1a_rationale": "IEEE journal publication is primary evidence for 8 CFR §204.5(h)(3)(vi) Scholarly Articles in Major Journals.",
        "best_for": ["Systematic Reviews", "Survey Papers", "Applied Systems", "All AI Topics"],
        "citation_velocity": "medium",
        "review_cycle": "Continuous submission",
        "workshop_track": False,
        "strategic_tip": "Ideal for 15-25 page comprehensive literature reviews. No page limit — depth is an asset.",
    },
    "ACM": {
        "full_name": "ACM Computing Surveys / SIGKDD / SIGMOD",
        "type": "journal",
        "acceptance_rate": 0.60,
        "difficulty": "Moderate",
        "page_limit": None,
        "format": "ACM two-column journal or proceedings",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 3,
        "o1a_rationale": "ACM journal publication is primary evidence for 8 CFR §204.5(h)(3)(vi) Scholarly Articles.",
        "best_for": ["Survey Papers", "Databases", "Systems", "HCI", "Broad AI Topics"],
        "citation_velocity": "medium",
        "review_cycle": "Continuous submission",
        "workshop_track": False,
        "strategic_tip": "ACM Computing Surveys is ideal for exhaustive literature reviews — 20+ pages with full taxonomy.",
    },
    "IEEE_Access": {
        "full_name": "IEEE Access (Multidisciplinary Open Access Journal)",
        "type": "journal",
        "acceptance_rate": 0.70,
        "difficulty": "Moderate",
        "page_limit": 12,
        "format": "IEEE two-column Open Access, 10pt",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 4,
        "o1a_rationale": "Indexed in IEEE Xplore (30% of world CS/EE literature). Fast 10-week peer review for high-impact AI/EE papers.",
        "best_for": ["Computer Science", "Electrical Engineering", "Applied AI", "Robotics", "Telecommunications"],
        "citation_velocity": "very_high",
        "review_cycle": "Rapid ~10 weeks",
        "workshop_track": False,
        "strategic_tip": "High citation velocity via IEEE Xplore. Excellent for rapid publishing of applied AI systems ($2,245 APC).",
    },
    "SpringerOpen": {
        "full_name": "SpringerOpen (Springer Nature Open Access Journals)",
        "type": "journal",
        "acceptance_rate": 0.65,
        "difficulty": "Moderate",
        "page_limit": 14,
        "format": "Springer Nature Open Access single/two-column",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 4,
        "o1a_rationale": "Backed by Springer Nature with Web of Science and Scopus indexing under Creative Commons (CC BY).",
        "best_for": ["Applied CS", "Data Science", "Interdisciplinary AI", "Biomedical Informatics"],
        "citation_velocity": "high",
        "review_cycle": "Continuous (2-3 months)",
        "workshop_track": False,
        "strategic_tip": "Check institutional agreements for APC coverage. Strong indexing ensures widespread academic readership.",
    },
    "Femington": {
        "full_name": "Femington Academic Press (IJISDS / IJAMBI / IJCRMS)",
        "type": "journal",
        "acceptance_rate": 0.75,
        "difficulty": "Moderate",
        "page_limit": 12,
        "format": "Femington Open Access IEEE/ACM style",
        "anonymized": False,
        "o1a_criterion": "original_contributions",
        "o1a_value": 3,
        "o1a_rationale": "Specialized open access focusing on AI, data science, and business intelligence with COPE ethics & CrossRef DOIs.",
        "best_for": ["Intelligent Systems", "Data Science", "Business Intelligence", "Clinical AI", "Applied ML"],
        "citation_velocity": "high",
        "review_cycle": "Predictable 4-6 weeks",
        "workshop_track": False,
        "strategic_tip": "Ideal for applied AI research bridging theory and enterprise practice with transparent status tracking.",
    },
    "MDPI": {
        "full_name": "MDPI (Multidisciplinary Digital Publishing Institute)",
        "type": "journal",
        "acceptance_rate": 0.72,
        "difficulty": "Easy to Moderate",
        "page_limit": 12,
        "format": "MDPI Open Access two-column",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 3,
        "o1a_rationale": "Fast-turnaround open access with immediate indexing across Web of Science & Scopus.",
        "best_for": ["Applied Sciences", "Sensors", "Electronics", "Systems Engineering", "AI Operations"],
        "citation_velocity": "high",
        "review_cycle": "Fast 2-4 weeks first decision",
        "workshop_track": False,
        "strategic_tip": "Use when speed-to-publish is urgent for grant deadlines or graduation requirements ($1,000-$2,600 APC).",
    },
    "DOAJ": {
        "full_name": "DOAJ (Directory of Open Access Journals - Verified Seal)",
        "type": "directory",
        "acceptance_rate": 0.80,
        "difficulty": "Moderate",
        "page_limit": 12,
        "format": "Verified Open Access standard layout",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 3,
        "o1a_rationale": "DOAJ Seal guarantees non-predatory, peer-reviewed open access standards for scholarly citation indexing.",
        "best_for": ["Open Science", "Computer Science", "Multi-Agent Systems", "Applied ML"],
        "citation_velocity": "high",
        "review_cycle": "Varies by journal (4-8 weeks)",
        "workshop_track": False,
        "strategic_tip": "Filter DOAJ index for zero-APC or low-fee society-run journals to maximize open-access visibility.",
    },
    "arXiv": {
        "full_name": "arXiv (cs.SE / cs.AI Open Access Preprint Repository)",
        "type": "preprint",
        "acceptance_rate": 0.95,
        "difficulty": "Fast Open Access",
        "page_limit": 14,
        "format": "Two-column CS preprint format",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 4,
        "o1a_rationale": "Primary open-access repository for AI and CS preprints, providing instant global citation indexing on Google Scholar.",
        "best_for": ["Computer Science", "Software Engineering", "Artificial Intelligence", "Multi-Agent Systems"],
        "citation_velocity": "instant_very_high",
        "review_cycle": "Immediate (24-48 hours)",
        "workshop_track": False,
        "strategic_tip": "Establishes immediate priority and timestamped public evidence for scholarly articles and citations.",
    },
    "arXiv_Workshop": {
        "full_name": "arXiv Preprint + Conference Workshop Track",
        "type": "preprint_workshop",
        "acceptance_rate": 0.90,
        "difficulty": "Easy",
        "page_limit": 4,
        "format": "Workshop 4-page extended abstract or full NeurIPS/CVPR workshop paper",
        "anonymized": False,
        "o1a_criterion": "scholarly_articles",
        "o1a_value": 2,
        "o1a_rationale": "arXiv preprints build citation velocity and portfolio evidence. Workshop acceptance adds conference affiliation.",
        "best_for": ["All Topics — Portfolio Building", "Fast Idea Dissemination", "Preliminary Results"],
        "citation_velocity": "variable",
        "review_cycle": "Any time (arXiv), Workshop deadlines vary",
        "workshop_track": True,
        "strategic_tip": "Best starting point. arXiv ID + NeurIPS/CVPR workshop acceptance is strong early O-1A evidence.",
    },
}

DIFFICULTY_ORDER = {"Easy": 1, "Moderate": 2, "Hard": 3, "Very Hard": 4}


# ──────────────────────────────────────────────────────────────────────────────
# Paper-to-venue topic affinity mapping
# ──────────────────────────────────────────────────────────────────────────────

TOPIC_VENUE_AFFINITY = {
    # Vision / Multimodal → CVPR > NeurIPS > ICML > IEEEtran
    "vision": ["CVPR", "NeurIPS", "ICML", "IEEEtran"],
    "multimodal": ["CVPR", "NeurIPS", "ACL", "IEEEtran"],
    "image": ["CVPR", "NeurIPS", "IEEEtran", "ACM"],
    "video": ["CVPR", "NeurIPS", "IEEEtran"],
    "3d": ["CVPR", "NeurIPS", "IEEEtran"],
    "contrastive": ["CVPR", "NeurIPS", "ICML", "IEEEtran"],
    "clip": ["CVPR", "NeurIPS", "IEEEtran"],
    "diffusion": ["CVPR", "NeurIPS", "IEEEtran"],
    "generation": ["CVPR", "NeurIPS", "ACL", "IEEEtran"],
    # Language / NLP → ACL > NeurIPS > ICML > IEEEtran
    "language": ["ACL", "NeurIPS", "ICML", "IEEEtran"],
    "nlp": ["ACL", "NeurIPS", "IEEEtran"],
    "text": ["ACL", "NeurIPS", "IEEEtran"],
    "llm": ["ACL", "NeurIPS", "CVPR", "IEEEtran"],
    "transformer": ["ACL", "NeurIPS", "ICML", "CVPR", "IEEEtran"],
    "alignment": ["NeurIPS", "ICML", "ACL", "CVPR", "IEEEtran"],
    "rlhf": ["NeurIPS", "ICML", "ACL"],
    "translation": ["ACL", "NeurIPS"],
    # ML theory / optimization → NeurIPS > ICML > IEEEtran
    "optimization": ["NeurIPS", "ICML", "IEEEtran"],
    "convergence": ["ICML", "NeurIPS", "IEEEtran"],
    "generalization": ["NeurIPS", "ICML", "IEEEtran"],
    "reinforcement": ["NeurIPS", "ICML", "IEEEtran"],
    # Survey / systematic review → IEEEtran > ACM > arXiv_Workshop
    "survey": ["IEEEtran", "ACM", "NeurIPS", "arXiv_Workshop"],
    "systematic review": ["IEEEtran", "ACM", "arXiv_Workshop"],
    "literature review": ["IEEEtran", "ACM", "arXiv_Workshop"],
    "taxonomy": ["IEEEtran", "ACM", "NeurIPS"],
    "comparative": ["IEEEtran", "ACM", "NeurIPS", "CVPR"],
    "meta-analysis": ["IEEEtran", "ACM", "NeurIPS"],
}


# ──────────────────────────────────────────────────────────────────────────────
# VenueAdvisorAgent
# ──────────────────────────────────────────────────────────────────────────────

class VenueAdvisorAgent:
    """
    Multi-sub-agent system that recommends publication venues for confirmed papers.

    Sub-agents:
      1. ProfileMatcher — assesses user readiness for each venue tier
      2. VenueScorer    — scores venues on 5 axes: topic fit, acceptance, difficulty,
                          O-1A value, profile match
      3. StrategyGen    — writes AI-powered rationale using Gemini
    """

    def __init__(self, vault_path: str = ""):
        self.vault_path = vault_path

    def _compute_topic_affinity(self, title: str, abstract: str, topic_keywords: List[str]) -> Dict[str, float]:
        """Score each venue's topic affinity based on paper content keywords."""
        text = " ".join([title, abstract] + topic_keywords).lower()
        scores: Dict[str, float] = {v: 0.0 for v in VENUE_KNOWLEDGE}

        for keyword, preferred_venues in TOPIC_VENUE_AFFINITY.items():
            if keyword in text:
                for rank, venue in enumerate(preferred_venues):
                    if venue in scores:
                        # First venue in list gets +3, second +2, third +1
                        scores[venue] += max(3 - rank, 0.5)

        # Normalize to 0-10
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1.0
        return {v: round((s / max_score) * 10, 2) for v, s in scores.items()}

    def _compute_profile_match(self, venue_key: str, portfolio: Dict[str, Any]) -> float:
        """Score how well the user's profile matches venue tier requirements."""
        venue = VENUE_KNOWLEDGE[venue_key]
        difficulty_num = DIFFICULTY_ORDER.get(venue["difficulty"], 2)
        score = 10.0

        # Penalize hard/very-hard venues for users with no top-venue history
        top_pub_count = len(portfolio.get("accepted_top_venues", []))
        if difficulty_num >= 3 and top_pub_count == 0:
            score -= 3.0
        elif difficulty_num == 4 and top_pub_count < 2:
            score -= 2.0

        # Bonus for matching submission goals
        goals = portfolio.get("submission_goals", "balanced")
        if goals == "top_conference" and venue["type"] == "conference":
            score += 2.0
        elif goals == "safe_accept" and venue["acceptance_rate"] > 0.5:
            score += 3.0
        elif goals == "journal_impact" and venue["type"] == "journal":
            score += 3.0

        # Timeline: urgent users should prefer fast tracks
        timeline = portfolio.get("target_timeline", "normal")
        if timeline == "urgent" and venue["type"] == "journal":
            score -= 2.0  # Journals are slow
        if timeline == "urgent" and venue_key == "arXiv_Workshop":
            score += 3.0

        # O-1A alignment bonus
        o1a_goals = portfolio.get("o1a_criteria_met", [])
        if "scholarly_articles" not in o1a_goals and venue["o1a_criterion"] == "scholarly_articles":
            score += 1.5
        if "judging_work_of_others" not in o1a_goals and venue["o1a_criterion"] == "judging_work_of_others":
            score += 2.0

        return max(0.0, min(10.0, round(score, 2)))

    def _call_llm_for_rationale(self, title: str, abstract: str, top_venues: List[Dict[str, Any]], portfolio: Dict[str, Any]) -> Dict[str, str]:
        """Call LLMRouter to generate personalized submission rationale for top 3 venues."""
        try:
            from services.llm_router import llm_router

            venues_text = "\n".join([
                f"- {v['venue_key']} (score={v['overall_score']:.1f}/10, acceptance={int(v['acceptance_rate']*100)}%): {', '.join(VENUE_KNOWLEDGE[v['venue_key']]['best_for'][:3])}"
                for v in top_venues[:3]
            ])
            portfolio_text = f"Publications: {portfolio.get('total_publications', 0)}, Citations: {portfolio.get('citation_count', 0)}, Past top venues: {portfolio.get('accepted_top_venues', [])}"

            prompt = f"""You are an elite academic publishing strategist and O-1A visa evidence architect.

Paper Title: {title}
Abstract: {abstract[:800]}
User Portfolio: {portfolio_text}
Submission Goals: {portfolio.get('submission_goals', 'balanced')}
Target Timeline: {portfolio.get('target_timeline', 'normal')}

Top Venue Candidates:
{venues_text}

For EACH of the top 3 venues, write a 2-3 sentence personalized submission rationale explaining:
1. Why this paper fits this venue specifically
2. What O-1A immigration criterion this acceptance would satisfy
3. One specific thing the author should emphasize in the submission

Return ONLY a valid JSON object: {{"venue_key": "rationale text", ...}}"""

            raw = llm_router.generate_content(prompt, provider="GROQ", model="llama-3.1-8b-instant")
            if raw:
                json_match = re.search(r'\{[\s\S]*\}', raw)
                if json_match:
                    return json.loads(json_match.group(0))
        except Exception as e:
            print(f"VenueAdvisor LLM rationale error: {e}")

        # Fallback: use static templates
        return {
            v["venue_key"]: (
                f"{title} is a strong fit for {v['venue_key']} given the topic alignment "
                f"and {int(v['acceptance_rate']*100)}% acceptance rate. "
                f"Acceptance would satisfy the O-1A '{VENUE_KNOWLEDGE[v['venue_key']]['o1a_criterion']}' criterion. "
                f"{VENUE_KNOWLEDGE[v['venue_key']]['strategic_tip']}"
            )
            for v in top_venues[:3]
        }

    def recommend(
        self,
        title: str,
        abstract: str,
        topic_keywords: List[str],
        portfolio: Dict[str, Any],
        n_recommendations: int = 6,
    ) -> Dict[str, Any]:
        """
        Run the full venue recommendation pipeline.
        Returns ranked venue list with composite scores and AI rationale.
        """
        # Sub-agent 1: Topic affinity scoring
        topic_scores = self._compute_topic_affinity(title, abstract, topic_keywords)

        # Sub-agent 2: Profile matching
        ranked = []
        for venue_key, info in VENUE_KNOWLEDGE.items():
            topic_score = topic_scores.get(venue_key, 5.0)
            profile_score = self._compute_profile_match(venue_key, portfolio)
            acceptance_score = round(info["acceptance_rate"] * 10, 2)
            o1a_score = info["o1a_value"] * 2  # scale to 10

            # Weighted composite: topic fit 35%, profile match 25%, O-1A value 25%, acceptance 15%
            overall = (
                topic_score * 0.35 +
                profile_score * 0.25 +
                o1a_score * 0.25 +
                acceptance_score * 0.15
            )

            ranked.append({
                "venue_key": venue_key,
                "full_name": info["full_name"],
                "type": info["type"],
                "overall_score": round(overall, 2),
                "topic_score": topic_score,
                "profile_score": profile_score,
                "o1a_score": o1a_score,
                "acceptance_score": acceptance_score,
                "acceptance_rate": info["acceptance_rate"],
                "difficulty": info["difficulty"],
                "o1a_criterion": info["o1a_criterion"],
                "o1a_value": info["o1a_value"],
                "o1a_rationale": info["o1a_rationale"],
                "page_limit": info["page_limit"],
                "format": info["format"],
                "anonymized": info["anonymized"],
                "best_for": info["best_for"],
                "review_cycle": info["review_cycle"],
                "strategic_tip": info["strategic_tip"],
                "workshop_track": info["workshop_track"],
            })

        ranked.sort(key=lambda x: x["overall_score"], reverse=True)

        # Sub-agent 3: AI rationale generation for top venues
        top_venues = ranked[:3]
        rationales = self._call_llm_for_rationale(title, abstract, top_venues, portfolio)

        for rec in ranked:
            rec["ai_rationale"] = rationales.get(rec["venue_key"], rec.get("strategic_tip", ""))

        return {
            "ranked_venues": ranked[:n_recommendations],
            "top_recommendation": ranked[0]["venue_key"] if ranked else "IEEEtran",
            "total_scored": len(ranked),
            "paper_title": title,
            "scoring_axes": {
                "topic_weight": "35%",
                "profile_weight": "25%",
                "o1a_weight": "25%",
                "acceptance_weight": "15%",
            }
        }
