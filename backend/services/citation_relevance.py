"""Citation relevance auditor.

A citation key that resolves is not the same as a citation that belongs. The
existing checks verify that every ``[[paper_id]]`` maps to a real note in
``vault/01_Papers``, which is necessary but says nothing about whether the cited
work has anything to do with the sentence citing it. That gap let a manuscript on
AST mutation algebra cite a paper on breast-cancer classification, and a paper on
program repair cite a study of the card game Hanabi.

Relevance is scored by lexical overlap between the citing context and the cited
work's own title and tags, measured against the base rate for that manuscript.
This is deliberately a weak signal used for triage: it flags citations for review
rather than deciding them, because judging whether a citation supports a claim is
not a lexical question. What it reliably catches is the case that matters here --
a citation with no topical connection at all.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


STOPWORDS = frozenset("""
a an the and or of to in is are for with that this it as be on by from at not if
then than which was were will can may use used using we our their its these those
via toward towards into over under between across during through more most such
both each other than when where while about after before both few many some any
""".split())


@dataclass
class CitationUsage:
    """One citation occurrence, with the context that should justify it."""

    key: str
    line_no: int
    context: str
    title: str = ""
    tags: List[str] = field(default_factory=list)
    resolved: bool = False
    overlap: int = 0
    score: float = 0.0
    verdict: str = "unreviewed"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def tokenize(text: str) -> Set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", (text or "").lower())
    out: Set[str] = set()
    for word in words:
        for piece in re.split(r"[-_]", word):
            if len(piece) > 2 and piece not in STOPWORDS:
                out.add(piece)
    return out


class CitationRelevanceService:
    """Scores whether each cited work is topically connected to its citing context."""

    #: Below this, the citation shares essentially no vocabulary with either the
    #: sentence citing it or the manuscript's own subject matter.
    #: Fewer content words than this and the context cannot support a judgement.
    MIN_CONTEXT_TOKENS = 8

    IRRELEVANT_THRESHOLD = 0.10
    WEAK_THRESHOLD = 0.25

    _WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")

    def __init__(self, vault_path: str = "vault") -> None:
        self.vault_path = vault_path
        self._notes: Optional[Dict[str, Dict[str, Any]]] = None
        self._idf: Optional[Dict[str, float]] = None

    # ------------------------------------------------------------------ corpus

    def load_notes(self) -> Dict[str, Dict[str, Any]]:
        """Index vault paper notes by citation key."""
        if self._notes is not None:
            return self._notes

        notes: Dict[str, Dict[str, Any]] = {}
        papers_dir = os.path.join(self.vault_path, "01_Papers")
        if not os.path.isdir(papers_dir):
            self._notes = notes
            return notes

        for name in os.listdir(papers_dir):
            if not name.endswith(".md"):
                continue
            path = os.path.join(papers_dir, name)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue

            title = self._frontmatter(text, "title")
            paper_id = self._frontmatter(text, "id")
            tags = re.findall(r'^\s*-\s*"([^"]+)"', text[:2000], re.MULTILINE)
            body = re.sub(r"^---[\s\S]*?\n---\n", "", text)[:4000]

            # Title and tags alone are too thin: the tag list carries the ingesting
            # topic slug, which matches any manuscript on that topic regardless of
            # what the paper is actually about. The abstract is the real signal.
            entry = {"title": title, "tags": tags, "body": body,
                     "tokens": tokenize(title) | tokenize(body)}
            for key in self._candidate_keys(name, paper_id):
                notes.setdefault(key, entry)

        self._notes = notes
        return notes

    def idf(self) -> Dict[str, float]:
        """Inverse document frequency of each term over the vault corpus.

        Unweighted overlap made "agent", "multi" and "systems" carry the match, so
        a paper on the card game Hanabi scored as relevant to program repair
        because both are about agents. Weighting by specificity is what separates
        a shared subject from shared field vocabulary.
        """
        if self._idf is not None:
            return self._idf

        import math
        notes = self.load_notes()
        documents = {id(e): e for e in notes.values()}.values()
        total = max(len(documents), 1)
        frequency: Dict[str, int] = {}
        for entry in documents:
            for token in entry["tokens"]:
                frequency[token] = frequency.get(token, 0) + 1
        self._idf = {t: math.log(total / (1 + c)) for t, c in frequency.items()}
        return self._idf

    def _weight(self, tokens: Set[str]) -> float:
        idf = self.idf()
        # Unseen terms are maximally specific: they appear in no vault note.
        default = max(idf.values(), default=1.0)
        return sum(idf.get(t, default) for t in tokens)

    @staticmethod
    def _frontmatter(text: str, field_name: str) -> str:
        match = re.search(rf'^{field_name}:\s*"?(.*?)"?\s*$', text[:2000], re.MULTILINE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _candidate_keys(filename: str, paper_id: str) -> List[str]:
        """Citation keys are written several ways; index every form we may see."""
        stem = os.path.splitext(filename)[0]
        keys = {stem, stem.replace(".", "_"), stem.replace("_", ".")}
        if paper_id:
            normalised = paper_id.replace(":", "_").replace("/", "_").replace("-", "_")
            keys |= {paper_id, normalised, normalised.replace(".", "_")}
        return [k for k in keys if k]

    # ------------------------------------------------------------------- audit

    def audit_draft(self, draft_path: str) -> List[CitationUsage]:
        """Score every citation occurrence in one manuscript."""
        with open(draft_path, encoding="utf-8") as handle:
            markdown = handle.read()

        notes = self.load_notes()
        subject = self._subject_tokens(markdown)
        usages: List[CitationUsage] = []

        for line_no, line in enumerate(markdown.split("\n"), start=1):
            for match in self._WIKILINK.finditer(line):
                raw = match.group(1)
                for key in (k.strip() for k in raw.split(",")):
                    if not key:
                        continue
                    entry = self._lookup(notes, key)
                    context = self._sentence_around(line, match.start())
                    usage = CitationUsage(key=key, line_no=line_no, context=context[:300])
                    if entry is None:
                        usage.verdict = "unresolved"
                        usages.append(usage)
                        continue

                    usage.resolved = True
                    usage.title = entry["title"]
                    usage.tags = entry["tags"]
                    cited = entry["tokens"]
                    local = tokenize(context)
                    # Score against the citing sentence first, then the manuscript
                    # as a whole: a citation may support a specific sentence, or be
                    # general background for the paper's subject.
                    # Normalise by the citing context, not by the cited work: the
                    # question is whether the cited paper covers what this sentence
                    # is about, not whether the sentence covers the whole paper.
                    context_tokens = local or subject
                    # Too few content words to judge against. Scoring these would
                    # mark perfectly good citations irrelevant purely because the
                    # sentence around them is short.
                    if len(context_tokens) < self.MIN_CONTEXT_TOKENS:
                        usage.verdict = "unjudged"
                        usages.append(usage)
                        continue
                    matched = cited & context_tokens
                    usage.overlap = len(matched)
                    denominator = self._weight(context_tokens) or 1.0
                    usage.score = round(self._weight(matched) / denominator, 4)
                    usage.verdict = self._verdict(usage.score)
                    usages.append(usage)
        return usages

    @classmethod
    def _verdict(cls, score: float) -> str:
        if score < cls.IRRELEVANT_THRESHOLD:
            return "irrelevant"
        if score < cls.WEAK_THRESHOLD:
            return "weak"
        return "relevant"

    @staticmethod
    def _lookup(notes: Dict[str, Dict[str, Any]], key: str) -> Optional[Dict[str, Any]]:
        for candidate in (key, key.replace(".", "_"), key.replace("_", "."),
                          key.replace("-", "_")):
            if candidate in notes:
                return notes[candidate]
        return None

    def _subject_tokens(self, markdown: str) -> Set[str]:
        """The manuscript's own subject vocabulary, from title and section heads."""
        title = self._frontmatter(markdown, "title")
        heads = re.findall(r"^#{1,3}\s+(.+)$", markdown, re.MULTILINE)
        return tokenize(title + " " + " ".join(heads))

    @staticmethod
    def _sentence_around(line: str, index: int) -> str:
        start = line.rfind(". ", 0, index) + 1
        end = line.find(". ", index)
        end = len(line) if end == -1 else end
        return line[max(start, 0):end].strip()

    # ----------------------------------------------------------------- reports

    def audit_all(self, drafts_dir: str) -> Dict[str, List[CitationUsage]]:
        reports: Dict[str, List[CitationUsage]] = {}
        for name in sorted(os.listdir(drafts_dir)):
            if name.endswith(".md"):
                reports[os.path.splitext(name)[0]] = self.audit_draft(
                    os.path.join(drafts_dir, name)
                )
        return reports

    @staticmethod
    def summarise(usages: Sequence[CitationUsage]) -> Dict[str, int]:
        counts = {"relevant": 0, "weak": 0, "irrelevant": 0, "unresolved": 0,
                  "unjudged": 0}
        for usage in usages:
            counts[usage.verdict] = counts.get(usage.verdict, 0) + 1
        counts["distinct_keys"] = len({u.key for u in usages})
        counts["total"] = len(usages)
        return counts

    def score_pair(self, cited_tokens: Set[str], context_tokens: Set[str]) -> float:
        """The single relevance definition, used by both auditing and suggesting.

        Keeping two scoring formulas meant the replacement threshold was measured
        on a different scale from the verdicts it was supposed to act on, and no
        candidate ever cleared it.
        """
        denominator = self._weight(context_tokens) or 1.0
        return round(self._weight(cited_tokens & context_tokens) / denominator, 4)

    def suggest_replacements(self, usage: CitationUsage, subject: Set[str],
                             limit: int = 5) -> List[Tuple[str, str, float]]:
        """Rank vault papers by relevance to the citing context.

        Returns (key, title, score) on the same scale as the audit verdicts.
        Suggestions only: whether a paper supports a claim is a judgement the
        author has to make.
        """
        notes = self.load_notes()
        context = tokenize(usage.context) or subject
        scored: List[Tuple[str, str, float]] = []
        seen_titles: Set[str] = set()
        for key, entry in notes.items():
            if entry["title"] in seen_titles or not entry["tokens"]:
                continue
            seen_titles.add(entry["title"])
            score = self.score_pair(entry["tokens"], context)
            if score > 0:
                scored.append((key, entry["title"], score))
        scored.sort(key=lambda row: -row[2])
        return scored[:limit]
