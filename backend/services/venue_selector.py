"""Venue Selector.

Picks one venue per manuscript instead of building all twelve. Submitting a single
paper to IEEE, NeurIPS, ICML, CVPR and ACL concurrently is duplicate submission and
is prohibited by every one of them, so the 12-venue matrix is a formatting
capability, not a submission plan.

Scoring combines four things, in decreasing authority:

1. **Provenance eligibility** — a hard gate. A manuscript carrying claims with no
   recorded artifact cannot be routed to a venue that reviews reported numbers as
   the authors' own measurements (see :mod:`services.claim_provenance`).
2. **Scope fit** — vocabulary overlap between the manuscript and the venue's field.
3. **Length fit** — estimated typeset pages against the venue's limit. A 3,200-word
   draft aimed at a 9-page conference is under-built, not ready.
4. **Portfolio shape** — spread across venues, and honour the configured strategy
   rather than stacking every paper on the same target.

Venue standing is recorded honestly: ``UNVERIFIED`` venues are surfaced with a
warning rather than silently scored, because a publication in a venue that cannot
be independently confirmed is weak evidence in any portfolio.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence

from services.claim_provenance import certifies_measurement


TIER_COMPETITIVE = "competitive"
TIER_JOURNAL = "reputable_journal"
TIER_OPEN_ACCESS = "open_access"
TIER_PREPRINT = "preprint"
TIER_INDEX = "index_only"
TIER_UNVERIFIED = "unverified"


@dataclass(frozen=True)
class VenueScope:
    """What a venue publishes, and how it should count toward a portfolio."""

    tier: str
    page_limit: int
    keywords: frozenset
    #: Rough public acceptance rate. Used only for ordering within a tier.
    acceptance: float
    note: str = ""


# Acceptance rates are approximate public figures for ordering, not predictions.
VENUE_SCOPES: Dict[str, VenueScope] = {
    "NeurIPS": VenueScope(TIER_COMPETITIVE, 9, frozenset({
        "learning", "neural", "model", "representation", "optimization", "agent",
        "benchmark", "training", "generalization", "bound", "theorem"}), 0.26),
    "ICML": VenueScope(TIER_COMPETITIVE, 8, frozenset({
        "learning", "training", "scaling", "optimization", "model", "gradient",
        "parameter", "efficiency", "convergence", "theorem"}), 0.27),
    "CVPR": VenueScope(TIER_COMPETITIVE, 8, frozenset({
        "vision", "visual", "image", "video", "multimodal", "spatial", "temporal",
        "grounding", "detection", "segmentation"}), 0.23),
    "ACL": VenueScope(TIER_COMPETITIVE, 8, frozenset({
        "language", "text", "nlp", "semantic", "dialogue", "token", "linguistic",
        "prompt", "reasoning", "corpus"}), 0.21),
    "IEEEtran": VenueScope(TIER_JOURNAL, 14, frozenset({
        "system", "architecture", "engineering", "reliability", "infrastructure",
        "protocol", "verification", "fault", "distributed", "governance"}), 0.30,
        "IEEE Transactions; check the specific transaction's scope before submitting."),
    "IEEE_Access": VenueScope(TIER_JOURNAL, 12, frozenset({
        "system", "applied", "engineering", "enterprise", "framework", "evaluation",
        "architecture", "deployment", "infrastructure"}), 0.30),
    "ACM": VenueScope(TIER_JOURNAL, 10, frozenset({
        "software", "system", "computing", "engineering", "program", "code",
        "repair", "synthesis", "compiler", "runtime"}), 0.25),
    "SpringerOpen": VenueScope(TIER_JOURNAL, 14, frozenset({
        "applied", "review", "framework", "enterprise", "analysis", "survey",
        "taxonomy", "adoption", "economics"}), 0.45),
    "MDPI": VenueScope(TIER_OPEN_ACCESS, 12, frozenset({
        "applied", "review", "survey", "evaluation", "framework", "enterprise",
        "analysis", "adoption"}), 0.50,
        "Rapid open access; article processing charges apply."),
    "DOAJ": VenueScope(TIER_INDEX, 12, frozenset(), 0.0,
        "DOAJ is a directory of open-access journals, not a venue you submit to."),
    "arXiv": VenueScope(TIER_PREPRINT, 20, frozenset(), 1.0,
        "Preprint server; no peer review, so it never counts as a publication."),
    "Femington": VenueScope(TIER_UNVERIFIED, 12, frozenset(), 0.0,
        "Could not be independently verified as an indexed venue. Confirm it is "
        "real, indexed and not predatory before submitting anything to it."),
}

#: Words per typeset page, two-column camera-ready. Used for the length estimate.
WORDS_PER_PAGE = 750


@dataclass
class PaperFeatures:
    stem: str
    title: str
    word_count: int
    table_count: int
    citation_count: int
    ungrounded_claims: int
    total_claims: int
    keywords: List[str] = field(default_factory=list)

    @property
    def estimated_pages(self) -> float:
        return round(self.word_count / WORDS_PER_PAGE, 1)


@dataclass
class VenueScore:
    venue: str
    tier: str
    score: float
    eligible: bool
    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VenueSelectorService:
    """Scores venues per manuscript and allocates one target across the portfolio."""

    _STOPWORDS = frozenset({
        "the", "and", "for", "with", "that", "this", "from", "into", "under", "over",
        "are", "was", "were", "have", "has", "not", "but", "all", "our", "its", "can",
        "which", "these", "their", "than", "then", "when", "each", "such", "also",
    })

    def __init__(self, strategy: str = "balanced") -> None:
        self.strategy = strategy

    # --------------------------------------------------------------- features

    def extract_features(
        self,
        stem: str,
        markdown: str,
        ungrounded_claims: int = 0,
        total_claims: int = 0,
    ) -> PaperFeatures:
        title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
        words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", markdown.lower())
        frequency: Dict[str, int] = {}
        for word in words:
            if word in self._STOPWORDS:
                continue
            frequency[word] = frequency.get(word, 0) + 1
        top = sorted(frequency.items(), key=lambda kv: kv[1], reverse=True)[:40]

        return PaperFeatures(
            stem=stem,
            title=(title_match.group(1).strip() if title_match else stem),
            word_count=len(markdown.split()),
            table_count=markdown.count("\n|"),
            citation_count=len(set(re.findall(r"\[\[([^\]]+)\]\]", markdown))),
            ungrounded_claims=ungrounded_claims,
            total_claims=total_claims,
            keywords=[w for w, _ in top],
        )

    # ---------------------------------------------------------------- scoring

    def score_venue(
        self,
        paper: PaperFeatures,
        venue_key: str,
        used_venues: Optional[Sequence[str]] = None,
    ) -> VenueScore:
        scope = VENUE_SCOPES.get(venue_key)
        if scope is None:
            return VenueScore(venue_key, "unknown", 0.0, False, ["Unknown venue."])

        reasons: List[str] = []
        warnings: List[str] = []
        eligible = True
        score = 0.0

        # 1. Provenance gate — hard, and it outranks every other signal.
        if paper.ungrounded_claims and certifies_measurement(venue_key):
            eligible = False
            reasons.append(
                f"BLOCKED: {paper.ungrounded_claims} claim(s) with no recorded artifact; "
                f"{venue_key} reviews reported numbers as measured by the authors."
            )
        elif not paper.ungrounded_claims:
            score += 30.0
            reasons.append("All quantitative claims trace to evidence (+30).")

        # 2. Venue standing.
        if scope.tier == TIER_UNVERIFIED:
            eligible = False
            warnings.append(scope.note)
            reasons.append("BLOCKED: venue standing could not be verified.")
        elif scope.tier == TIER_INDEX:
            eligible = False
            reasons.append("BLOCKED: an index, not a submission target.")
        elif scope.tier == TIER_PREPRINT:
            warnings.append(scope.note)

        # 3. Scope fit. A competitive venue needs real topical overlap: three
        # incidental words ("prompt", "text", "token") routed a systems simulation
        # paper to a computational-linguistics conference before this gate existed.
        overlap = scope.keywords.intersection(paper.keywords) if scope.keywords else set()
        if scope.keywords:
            fit = min(len(overlap) / 6.0, 1.0) * 25.0
            score += fit
            reasons.append(
                f"Scope fit {fit:.0f}/25 (matched: {', '.join(sorted(overlap)[:5]) or 'none'})."
            )
        if scope.tier == TIER_COMPETITIVE and len(overlap) < 4:
            eligible = False
            reasons.append(
                f"BLOCKED: only {len(overlap)} scope term(s) overlap; too weak a topical "
                f"match for {venue_key}."
            )

        # 4. Length fit against the venue's limit.
        pages = paper.estimated_pages
        if pages < scope.page_limit * 0.6:
            deficit = scope.page_limit - pages
            score += 5.0
            reasons.append(
                f"Under-built: ~{pages} pages against a {scope.page_limit}-page venue "
                f"({deficit:.1f} pages short) (+5)."
            )
            # A half-length submission to a competitive venue is a desk reject, not a
            # long shot. Recommending one wastes a submission cycle.
            if scope.tier == TIER_COMPETITIVE:
                eligible = False
                reasons.append(
                    f"BLOCKED: ~{pages} pages is under 60% of {venue_key}'s "
                    f"{scope.page_limit}-page format; expand before submitting."
                )
        elif pages <= scope.page_limit:
            score += 20.0
            reasons.append(f"Length fits: ~{pages} of {scope.page_limit} pages (+20).")
        else:
            score += 8.0
            reasons.append(f"Over limit: ~{pages} against {scope.page_limit} pages (+8).")

        # 5. Acceptance likelihood, ordering within a tier. A preprint accepts
        # everything, but posting one is not a publication, so it must never
        # outscore a reviewed venue the manuscript is actually eligible for.
        if scope.tier == TIER_PREPRINT:
            reasons.append("Preprint: no acceptance weight; fallback only.")
        else:
            score += scope.acceptance * 15.0
            reasons.append(f"Acceptance weight +{scope.acceptance * 15.0:.1f}.")

        # 6. Portfolio spread.
        if used_venues and venue_key in used_venues:
            score -= 18.0
            reasons.append("Already used by another manuscript in this batch (-18).")

        return VenueScore(venue_key, scope.tier, round(max(score, 0.0), 2), eligible, reasons, warnings)

    def rank_venues(
        self, paper: PaperFeatures, used_venues: Optional[Sequence[str]] = None
    ) -> List[VenueScore]:
        scores = [self.score_venue(paper, key, used_venues) for key in VENUE_SCOPES]
        return sorted(scores, key=lambda s: (s.eligible, s.score), reverse=True)

    # ------------------------------------------------------------- allocation

    def allocate_portfolio(
        self, papers: Sequence[PaperFeatures], max_competitive: int = 2
    ) -> Dict[str, Dict[str, Any]]:
        """Assign one venue per manuscript across the whole batch.

        Under the balanced strategy the best-evidenced manuscripts get the limited
        competitive slots and everything else routes to a credible reviewed journal,
        so the portfolio is not a wall of desk-rejects nor a wall of low-selectivity
        open access.
        """
        # Strongest evidence first: those manuscripts have earned the scarce slots.
        ordered = sorted(
            papers,
            key=lambda p: (p.ungrounded_claims, -p.word_count),
        )

        allocation: Dict[str, Dict[str, Any]] = {}
        used: List[str] = []
        competitive_used = 0

        for paper in ordered:
            ranked = [s for s in self.rank_venues(paper, used) if s.eligible]

            if self.strategy == "balanced" and competitive_used >= max_competitive:
                ranked = [s for s in ranked if s.tier != TIER_COMPETITIVE]

            if not ranked:
                allocation[paper.stem] = {
                    "venue": None,
                    "tier": None,
                    "score": 0.0,
                    "rationale": [
                        "No eligible venue. Every reviewed venue is gated by the "
                        f"{paper.ungrounded_claims} unbacked claim(s); ground or strip "
                        "them, then re-run selection."
                    ],
                    "warnings": [],
                    "runner_up": None,
                    "estimated_pages": paper.estimated_pages,
                }
                continue

            best = ranked[0]
            if best.tier == TIER_COMPETITIVE:
                competitive_used += 1
            used.append(best.venue)

            allocation[paper.stem] = {
                "venue": best.venue,
                "tier": best.tier,
                "score": best.score,
                "rationale": best.reasons,
                "warnings": best.warnings,
                "runner_up": ranked[1].venue if len(ranked) > 1 else None,
                "estimated_pages": paper.estimated_pages,
            }
        return allocation

    # ---------------------------------------------------------------- reports

    @staticmethod
    def render_markdown(
        allocation: Dict[str, Dict[str, Any]], papers: Sequence[PaperFeatures]
    ) -> str:
        by_stem = {p.stem: p for p in papers}
        lines = [
            "# Venue Allocation",
            "",
            "One venue per manuscript. Concurrent submission of the same paper to "
            "multiple venues is prohibited by all of them, so the 12-venue build "
            "matrix is for formatting only.",
            "",
            "| Manuscript | Venue | Tier | Pages | Ungrounded | Score |",
            "|:---|:---|:---|---:|---:|---:|",
        ]
        for stem, entry in sorted(allocation.items()):
            paper = by_stem.get(stem)
            lines.append(
                f"| {stem[:44]} | {entry['venue'] or '**none**'} | {entry['tier'] or '—'} | "
                f"{entry['estimated_pages']} | "
                f"{paper.ungrounded_claims if paper else '?'} | {entry['score']} |"
            )

        lines += ["", "## Rationale", ""]
        for stem, entry in sorted(allocation.items()):
            lines.append(f"### {stem}")
            lines.append(f"**Target:** {entry['venue'] or 'none — blocked'}")
            for reason in entry["rationale"]:
                lines.append(f"- {reason}")
            for warning in entry["warnings"]:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")
        return "\n".join(lines) + "\n"
