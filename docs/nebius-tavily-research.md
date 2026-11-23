# Optional Nebius and Tavily Scout discovery

Set `SCOUT_NEBIUS_ENABLED=true` and `NEBIUS_API_KEY` to use Nebius for
planning up to six academic queries for long topics. `NEBIUS_BASE_URL` and
`NEBIUS_MODEL` override the Token Factory endpoint and model shown in
`.env.example`. Nebius supports Scout planning only; a configured existing
Council provider is still required for live runs.

Set `SCOUT_TAVILY_ENABLED=true` and `TAVILY_API_KEY` to add Tavily advanced
search. Both integrations are independently disabled by default and bypassed
in dry runs. Restart the backend after changing its environment. A Scout run
issues at most one Nebius request and six Tavily searches, with at most five
results each; each request has a 20-second timeout. Provider failures fall back
to existing planning or scholarly search. Keys are not logged.

Tavily results are unverified leads. Only arXiv links that resolve through the
arXiv API enter the paper corpus, carrying their discovery URLs as provenance.
Snippets are never used as paper text. Existing PDF ingestion, fact checking,
and publication checks remain responsible for evidence evaluation; arXiv
discovery does not imply peer review or claim verification.

Both services may charge for calls; consult current provider pricing and account
limits before enabling them. The cookbook's example cost is not a guarantee of
the cost of a ResearchingOS run. See the [Nebius cookbook](https://dev.nebius.com/cookbook/deep-research-agent-tavily).
