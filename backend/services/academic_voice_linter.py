"""Academic Voice Linter & Humanizer for ResearchingOS.

Implements guidelines from hardikpandya/stop-slop and blader/humanizer:
- Scans draft manuscripts for predictable AI writing patterns, stock clichés,
  formulaic "not X but Y" staging contrasts, and throat-clearing adverbs.
- Generates an Academic Voice Score [0-100%] and severity-ranked remediation directives.
- Produces cleaned, humanized scholarly prose with zero factual hallucinations or dropped citations.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class SlopFinding:
    pattern_type: str  # "CLICHE", "STAGING_CONTRAST", "THROAT_CLEARING", "FILLER_ADVERB"
    matched_text: str
    line_number: int
    context: str
    recommendation: str
    severity: str      # "BLOCKER", "MAJOR", "MINOR"


class AcademicVoiceLinter:
    """Lints academic text to eliminate AI tells and ensure authoritative human scholarly voice."""

    AI_CLICHES = [
        (r"\b(pivotal|pivotally)\b", "pivotal", "Replace with 'essential', 'central', or state the specific mechanism.", "MAJOR"),
        (r"\b(delve[s]?\s+into)\b", "delves into", "Replace with 'analyzes', 'examines', or 'investigates'.", "MAJOR"),
        (r"\b(a\s+testament\s+to)\b", "a testament to", "Cut rhetorical flourish; state empirical proof directly.", "BLOCKER"),
        (r"\b(tapestry)\b", "tapestry", "Delete metaphor; specify precise multidisciplinary interaction.", "BLOCKER"),
        (r"\b(beacon)\b", "beacon", "Delete decorative fluff; state the benchmark reference directly.", "BLOCKER"),
        (r"\b(seamlessly|seamless)\b", "seamlessly", "Remove vague modifier; describe exact algorithmic interface.", "MAJOR"),
        (r"\b(groundbreaking|unprecedented)\b", "groundbreaking", "Cut hype; let statistical effect sizes demonstrate novelty.", "BLOCKER"),
        (r"\b(game-changer|game\s+changing)\b", "game-changer", "Unacceptable in IEEE/ACM manuscripts; state quantitative delta.", "BLOCKER"),
        (r"\b(foster[s]?\b)", "fosters", "Replace with 'enables', 'yields', or 'produces'.", "MINOR"),
        (r"\b(at\s+its\s+core)\b", "at its core", "Throat-clearing opener; state the mathematical foundation directly.", "MAJOR"),
        (r"\b(it\s+is\s+worth\s+noting(\s+that)?)\b", "it is worth noting", "Cut meta-commentary; state the observation as fact.", "MAJOR"),
        (r"\b(make\s+no\s+mistake)\b", "make no mistake", "Conversational crutch; delete entirely.", "BLOCKER"),
        (r"\b(deep\s+dive)\b", "deep dive", "Business jargon; use 'empirical analysis' or 'formal audit'.", "MAJOR"),
        (r"\b(landscape\s+of)\b", "landscape of", "Replace with 'domain of' or 'field of'.", "MINOR"),
        (r"\b(in\s+today's\s+[a-zA-Z]+)\b", "in today's ...", "Generic AI opening cliché; anchor directly in benchmark scope.", "MAJOR"),
    ]

    STAGING_CONTRASTS = [
        (r"\bnot\s+only\b[\s\S]{1,60}?\bbut(\s+also)?\b", "not only X but also Y", "Break binary contrast staging; state both claims directly.", "MAJOR"),
        (r"\bnot\s+just\b[\s\S]{1,60}?\bbut\b", "not just X but Y", "Avoid staging; present the primary contribution plainly.", "MAJOR"),
        (r"\bnot\s+merely\b[\s\S]{1,60}?\bbut\b", "not merely X but Y", "Avoid dramatic artificial contrast; state finding directly.", "MAJOR"),
        (r"\bit\s+is\s+not\b[\s\S]{1,50}?\bit\s+is\b", "it is not X, it is Y", "State the positive claim directly without negating an unmade point.", "MAJOR"),
    ]

    FILLER_ADVERBS = [
        (r"\b(crucially)\b", "crucially", "Delete adverb; emphasize finding with empirical baseline comparisons.", "MINOR"),
        (r"\b(fundamentally)\b", "fundamentally", "Delete adverb or specify the axiomatic level.", "MINOR"),
        (r"\b(inherently)\b", "inherently", "Delete adverb or define exact mathematical invariance.", "MINOR"),
        (r"\b(deeply)\b", "deeply", "Delete hyperbolic intensifier.", "MINOR"),
        (r"\b(genuinely)\b", "genuinely", "Delete conversational hedge.", "MINOR"),
        (r"\b(truly)\b", "truly", "Delete conversational hedge.", "MINOR"),
    ]

    def audit_prose(self, text: str) -> Dict[str, Any]:
        """Audits text and returns academic score, findings list, and statistics."""
        findings: List[SlopFinding] = []
        lines = text.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Skip code blocks or math display blocks
            if stripped.startswith("```") or stripped.startswith("$$"):
                continue

            # 1. Check AI Cliches
            for pat, name, rec, sev in self.AI_CLICHES:
                for match in re.finditer(pat, line, re.IGNORECASE):
                    findings.append(SlopFinding(
                        pattern_type="CLICHE",
                        matched_text=match.group(0),
                        line_number=idx,
                        context=line.strip()[:100],
                        recommendation=rec,
                        severity=sev,
                    ))

            # 2. Check Staging Contrasts
            for pat, name, rec, sev in self.STAGING_CONTRASTS:
                for match in re.finditer(pat, line, re.IGNORECASE):
                    findings.append(SlopFinding(
                        pattern_type="STAGING_CONTRAST",
                        matched_text=match.group(0),
                        line_number=idx,
                        context=line.strip()[:100],
                        recommendation=rec,
                        severity=sev,
                    ))

            # 3. Check Filler Adverbs
            for pat, name, rec, sev in self.FILLER_ADVERBS:
                for match in re.finditer(pat, line, re.IGNORECASE):
                    findings.append(SlopFinding(
                        pattern_type="FILLER_ADVERB",
                        matched_text=match.group(0),
                        line_number=idx,
                        context=line.strip()[:100],
                        recommendation=rec,
                        severity=sev,
                    ))

        # Compute Academic Voice Score [0 - 100%]
        blockers = sum(1 for f in findings if f.severity == "BLOCKER")
        majors = sum(1 for f in findings if f.severity == "MAJOR")
        minors = sum(1 for f in findings if f.severity == "MINOR")

        penalty = (blockers * 10) + (majors * 5) + (minors * 2)
        score = max(0, min(100, 100 - penalty))

        if score >= 90:
            rating = "AUTHENTIC_HUMAN_SCHOLARLY"
        elif score >= 75:
            rating = "ACCEPTABLE_ACADEMIC"
        elif score >= 60:
            rating = "MILD_AI_SLOP_DETECTED"
        else:
            rating = "HEAVY_AI_SLOP_FLAGGED"

        return {
            "academic_voice_score": score,
            "rating": rating,
            "total_findings": len(findings),
            "breakdown": {
                "blockers": blockers,
                "majors": majors,
                "minors": minors,
            },
            "findings": [asdict(f) for f in findings],
        }

    def humanize_text(self, text: str) -> Dict[str, Any]:
        """Removes AI cliches, throat-clearing, and staging contrasts while preserving meaning and citations."""
        audit_before = self.audit_prose(text)
        cleaned = text

        # Automatic replacements for common throat-clearers and cliches
        replacements = [
            (r"\bIt\s+is\s+worth\s+noting\s+that\s+", ""),
            (r"\bit\s+is\s+worth\s+noting\s+that\s+", ""),
            (r"\bAt\s+its\s+core,\s*", ""),
            (r"\bat\s+its\s+core,\s*", ""),
            (r"\bMake\s+no\s+mistake,\s*", ""),
            (r"\bmake\s+no\s+mistake,\s*", ""),
            (r"\bdelves\s+into\b", "analyzes"),
            (r"\bdelve\s+into\b", "examine"),
            (r"\bpivotal\b", "essential"),
            (r"\bseamlessly\b", "directly"),
            (r"\bgroundbreaking\b", "novel"),
            (r"\bunprecedented\b", "significant"),
            (r"\bgame-changer\b", "major advance"),
            (r"\ba\s+testament\s+to\b", "empirical evidence of"),
            (r"\btapestry\s+of\b", "system of"),
            (r"\bdeep\s+dive\s+into\b", "analysis of"),
            (r"\bcrucially,\s*", ""),
            (r"\bfundamentally,\s*", ""),
        ]

        for pat, repl in replacements:
            cleaned = re.sub(pat, repl, cleaned)

        audit_after = self.audit_prose(cleaned)

        return {
            "original_score": audit_before["academic_voice_score"],
            "cleaned_score": audit_after["academic_voice_score"],
            "score_improvement": audit_after["academic_voice_score"] - audit_before["academic_voice_score"],
            "original_findings_count": audit_before["total_findings"],
            "cleaned_findings_count": audit_after["total_findings"],
            "humanized_text": cleaned,
        }
