# Research skill collections

ResearchingOS integrates a pinned selection from:

- [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills)
- [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

The versioned manifest at `integrations/research_skills.json` records the precise
revision, selected package, document checksum, license note, role mapping, and
reviewed method guidance for every entry. Fifteen packages are selected: eight
from agent-research-skills, four from academic-research-skills, and three from
Composio. Thirteen have advisory role assignments; two are reference-only.

## Runtime behavior

| Pipeline role | Method guidance |
| --- | --- |
| Scout | Query design, source verification, search eligibility and citation records |
| Analyst | Evidence synthesis, contradictions and material gaps |
| Engineer | Hypotheses, baselines, compute budgets and ablation design |
| Statistician | Statistical assumptions, effect sizes, intervals and multiplicity |
| Reviewer2 / PeerReviewer | Evidence-linked review, limitations and correlated reviewer judgments |
| Chairman | Explicit handoffs and research/draft/review stage tracking |
| Writer | Context-first drafting, citation support and two-pass refinement |
| Tier 2 CitationExpander | Source-grounded references and bibliographic validation |

Council provider calls, DSPy section-writing calls, fallback writer calls, DSPy
red-team/peer-review calls and Tier 2 citation-expansion calls receive the
relevant reviewed guidance. Tier 2's deterministic checks retain their existing
behavior; assigning guidance to a role does not convert those checks to model calls.
The list is bounded to 4,000 characters per role and loaded only from verified
installed package documents. It adds no model calls or execution permissions.

The runtime uses the short reviewed guidance written in the manifest, **not the
full upstream prompt or scripts**. Full upstream `SKILL.md` files are reference
data for inspection in **Feynman Lab → Research Skills**. The panel supports
collection, role and text filters and displays installation and checksum status.
`webapp-testing` and `changelog-generator` are reference-only. No external
messaging connectors, hooks, background jobs or compute tasks are activated.

Existing vault citation rules, source/measurement checks, venue contracts,
fact checker and release gates continue to determine readiness. Skill advice
does not certify a paper or constitute empirical evidence.

## Local installation

```sh
python3 scripts/install_research_skills.py
```

This uses the Codex system skill installer to copy the selection into the ignored
`.tools/research-skills/<source>/<skill>/` directory. The installer helper can be
specified with `--installer /path/to/install-skill-from-github.py`. Packages include
their local scripts/resources where supplied, but ResearchingOS never executes them.
Some upstream references point outside the selected package or to Claude-specific
tools; those references are not resolved as executable dependencies by this adapter.

The operation pins commit revisions, verifies document hashes, skips matching
packages, and refuses to overwrite modified packages. New clones need this local
installation step; missing/modified skills stay visible and supply no runtime guidance.
Set `RESEARCH_SKILLS_ENABLED=false` and restart the backend to disable guidance
while retaining reference inspection. Installed skills are available to the
ResearchingOS pipeline immediately; they are not globally installed Codex skills.

## Source terms

Upstream packages stay local and are not vendored or relicensed under this
repository's MIT license. The academic collection declares CC-BY-NC-4.0,
copyright 2026 Cheng-I Wu; its noncommercial terms continue to apply. No
repository-wide license was found in the pinned lingzhi227 source. Composio
contains mixed per-skill terms: webapp-testing has Apache-2.0 terms, while the
selected writing/changelog folders contain no license file. Proprietary PDF/PPTX
document packages were excluded. Consult the pinned upstream source for terms.

## API and verification

- `GET /api/skills/research?source=agent-research&role=Scout&query=citation`
- `GET /api/skills/research/agent-research:citation-management`

Detail lookup uses exact manifest IDs rather than arbitrary filesystem paths.
Modified instruction files cannot activate guidance or be returned as the pinned
reference. Unit tests verify checksum failure, missing packages, disable behavior,
path containment, role selection, prompt budgets, API filters, actual council
provider calls and DSPy reviewer integration without making network/model calls.
