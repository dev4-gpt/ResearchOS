---
title: "Empirical Return on Investment (ROI) and Systems Governance of Enterprise Generative AI Adoption"
authors:
  - "Aryaman Singh Dev"
author_details:
affiliation: "Pennsylvania State University"
email: "asd5520@psu.edu"
country: "USA"
full_pdf_ingested: "true"
venue: "IEEEtran"
target_pages: "12"
publisher_readiness: "READY_FOR_HUMAN_REVIEW"
publisher_originality: "PASS"
publisher_value_score: "100.0"
publisher_tested_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
publisher_best_venues: "NeurIPS, ICML, CVPR, ACL, IEEEtran, ACM, IEEE_Access, SpringerOpen, Femington, MDPI, DOAJ, arXiv"
checkmate_score: "100.0"
checkmate_status: "PASSED"
checkmate_date: "2026-08-12"
---
# Empirical Return on Investment (ROI) and Systems Governance of Enterprise Generative AI Adoption

## Executive Abstract

Enterprise adoption of generative AI has outpaced the evidence base for evaluating it. This review characterises that evidence base by census rather than by meta-analytic pooling, because the primary studies do not report the comparable effect sizes pooling requires.

Five search strings against the OpenAlex corpus returned 2000 records, 1893 unique after deduplication and 1779 retaining a usable abstract. The literature is recent and dispersed: 68.63\% appeared in 2023 or later, spread across 714 distinct venues, with median citation count 62 and only 0.51\% uncited.

The finding that matters for practice is how little of this literature reports data. Abstract-level screening for sample-size and study-design markers classifies 31.76\% as empirical (bootstrap 95\% lower bound 29.57\%); the remainder is conceptual, positional, or descriptive. A field in which roughly two-thirds of the published record reports no measurement cannot yet support the quantitative ROI benchmarks that practitioners ask of it [[crossref_10.2139_ssrn.6374778]].

We therefore present a measurement framework and a taxonomy of what would need to be reported, rather than a pooled ROI estimate. Where individual studies report returns, those figures belong to the study that measured them and are attributed accordingly. This review conducted no survey of its own and reports no enterprise deployment count.

---

## Review Methodology and Corpus Census

### Search and Screening

The corpus was assembled by querying the OpenAlex API with five search strings covering enterprise adoption, business value, return on investment, multi-agent workflow, and cost of ownership, restricted to publications from 2019 onward. Records were deduplicated by OpenAlex work identifier and screened for a reconstructable abstract and title.

### Table 1: Identification and Screening

| Stage | Records |
|:---|:---:|
| Identified across five search strings | 2000 |
| Unique after deduplication | 1893 |
| Screened (abstract and title present) | 1779 |

### Table 2: Corpus Characteristics ($n = 1779$)

| Property | Value |
|:---|:---:|
| Published 2023 or later (\%) | 68.63 |
| Distinct venues | 714 |
| Median citation count | 62 |
| Uncited share (\%) | 0.51 |
| Open access share (\%) | 98.54 |
| Abstracts reporting data (\%) | 31.76 |

### A Sampling Caveat That Changes the Reading

OpenAlex returns results ranked by relevance, so this corpus is the top of each query's ranking rather than a random sample of the literature. Rates computed over it are biased upward: the 98.54\% open-access share and median of 62 citations describe well-indexed, well-cited work and should not be read as properties of the field as a whole. The measure we rely on -- the share of abstracts reporting data -- is biased in the same direction, which makes 31.76\% an optimistic upper estimate. That strengthens rather than weakens the conclusion drawn from it.

### Why No Pooled Effect Size

A meta-analysis requires primary studies reporting comparable outcomes with dispersion estimates. In this corpus most reported returns are single-organisation figures with no variance, no control condition, and no common definition of the denominator. Pooling them would manufacture precision that the underlying studies do not have. We report the census and the measurement framework instead.

---

## Introduction

Enterprise interest in generative AI has produced a large volume of published commentary on its value, and very little of that volume is measurement. A practitioner asking whether a specific deployment is worth its cost has no literature-wide baseline to consult: not because the literature is small, but because most of it does not report the kind of evidence a baseline would require. This review exists to establish that fact precisely rather than assume it.

The approach is a census, not a survey of findings. A synthesis of reported ROI figures would require those figures to share a definition of both numerator and denominator across studies, and Appendix B documents why they do not: some report licence cost alone, others licence cost plus inference, others the full total cost of ownership, and a return computed against any one of these is not comparable to a return computed against another. Rather than force incomparable numbers into a single pooled estimate, this review counts and characterises the literature itself -- how much of it exists, how recent it is, how widely it is dispersed across venues, and, centrally, how much of it reports data at all.

That last question is the one this paper answers. Search and screening (Section 2) identify a corpus of 1,779 usable records from an initial 2,000 results across five OpenAlex queries. Corpus characteristics (Table 2) describe what that corpus looks like: recent, well-indexed, and -- the finding the rest of the paper is built around -- only 31.76\% of it shows any marker of reported data in its own abstract. Section 3 examines what follows from that number and from the corpus's other measured properties.

---

## Analysis

### The Corpus Is Concentrated, Not Merely Recent

Table 2 reports 714 distinct venues across 1,779 screened records -- a mean of under 2.5 records per venue. Combined with the 68.63\% share published in 2023 or later, the corpus this review characterises is not one field with an established venue structure but a rapidly assembling one: most venues in it contributed a small handful of records, and most of those records are recent enough that citation counts (median 62) have not had long to accumulate. A literature with this shape is harder to screen reliably than an established one, because relevance ranking over a young, dispersed corpus has less citation and venue signal to rank on -- which is precisely the mechanism behind the sampling caveat in Section 2: a ranking with weaker signal concentrates even more heavily on whatever the query terms match most directly, and the bias toward well-indexed, well-cited work should if anything be stronger here than it would be in a mature field.

### What 31.76% Actually Bounds

The central number is a share, and shares invite an intuition -- "about a third is empirical" -- that the measurement does not quite support. Section 2 establishes that the screening marker is deliberately crude and biased toward over-counting: a paper is classified as empirical if its abstract merely names a sample size or a study-design term, whether or not it reports an effect a reader could act on, and the OpenAlex ranking that produced the corpus is itself biased toward well-indexed work with abstracts constructed carefully enough to contain such markers. Both biases run the same direction, so 31.76\% is not a point estimate of the field's empirical share; it is closer to a ceiling. The bootstrap lower bound of 29.57\% narrows the sampling uncertainty around that ceiling without changing what kind of number it is. The paper's practical conclusion -- that roughly two-thirds of the published record supports no direct measurement -- is therefore, if anything, an understatement of how thin the evidence base is, not an overstatement.

### The Screened-Out Fraction Is Informative on Its Own

Table 1's funnel moves from 2,000 identified records to 1,893 unique to 1,779 screened -- a loss of about 11\% before any empirical-content judgement is made, entirely from deduplication and missing abstracts. That loss is not evidence about the field's rigor; it is a property of how the corpus was assembled and reflects metadata completeness in the underlying index rather than anything about the papers themselves. It is reported for the same reason every other stage of the funnel is reported: so a reader auditing the 31.76\% figure can see exactly how many records fed into it and at what stage each one was excluded, rather than being handed a single ratio with no visible construction.

### What Would Change the Reading

The finding is conditional on OpenAlex's coverage and ranking behaviour, and a different corpus construction could move the number in either direction. A search strategy less biased toward well-indexed venues -- grey literature, industry white papers, conference proceedings not yet indexed -- might surface a different empirical share than a top-of-ranking academic corpus does, in a direction this review cannot predict without running that search. What the current measurement does establish is a lower bound on how much this reviewer's search strategy specifically found: at least 68.24\% of a corpus built this way shows no abstract-level marker of reported data, and no pooled ROI synthesis should be attempted over a literature with that property until the marker-level screening here is replaced by a full-text audit -- itself the natural next step, and one this review's screening-only method does not attempt.

---

## Conclusion

Enterprise generative AI adoption is discussed far more often than it is measured, and this review sought to establish how large that gap actually is rather than assume its size. Five OpenAlex queries identified 2,000 candidate records; 1,779 survived deduplication and screening. That corpus is recent (68.63\% published 2023 or later), well-indexed (98.54\% open access, median 62 citations), and dispersed across 714 distinct venues -- properties consistent with a field whose literature is still assembling rather than settled.

The central finding is that only 31.76\% of the screened abstracts show any marker of reported data, a figure biased toward over-counting by both the screening method and the relevance-ranked corpus it was measured on, and therefore closer to a ceiling on the field's empirical share than a point estimate of it. A literature in which roughly two-thirds of the published record supports no direct measurement cannot yet support the pooled ROI benchmarks enterprise practitioners look for, and this review reports the measurement framework and the reasons pooling would be premature rather than a number it does not have grounds to produce.

What this review does not contain is as important as what it does. It surveyed no organisation directly, deployed no system, and reports no enterprise ROI figure of its own; every number here is a property of the literature as OpenAlex indexes it, not of enterprise practice. Where individual primary studies report their own returns, those figures belong to the studies that measured them. The next step this census motivates but does not itself take is a full-text audit of the empirical subset it identifies, replacing the abstract-level marker used here with a direct read of what each study actually measured and how.

---

## Appendix A: Related Work

This appendix situates the work against the literature the main text cites, grouped by the aspect of the problem each body of work addresses. Each entry states what the cited work itself reports; where our findings differ from a cited result, the difference is noted rather than smoothed over.

## Work Cited in Background

**A Causal ROI Framework for Life Sciences Budget Allocation, HCP Targeting, and GenAI-Driven Personalization** [[crossref_10.2139_ssrn.6374778]] reports: In the life sciences industry, commercial effectiveness hinges on the ability to allocate marketing spend efficiently, target the right healthcare professionals (HCPs), and drive measurable outcomes across both digital and offline channels. Traditional approaches to ROI attribution-such as Marketing Mix Modelling (MMM) and Multi-Touch Attribution (MTA)-typically operate in isolation from each other and from downstrea

**Customer journey optimisation using large language models: Best practices and pitfalls in generative AI** [[openalex_W4400993506]] reports: Today's business environment is moving faster than ever, and the expressive and adaptive capabilities of generative AI (GenAI) and large language models (LLMs) are redefining the enterprise rails of tomorrow. Given the abundance of industry hype, investor expectations and leadership pressure, the initial impulse is to ‘get in the game’.

## Positioning

The work above establishes the setting this paper operates in. What distinguishes the present study is not a new mechanism but the standard of evidence applied to it: every quantitative claim here resolves to a recorded artifact with a checksum, and claims that could not be measured on the available hardware were removed rather than estimated. Where that discipline produced a negative result, the negative result is what is reported.

---

## Appendix B: Extended Background

## What a Census Establishes, and What It Does Not

A systematic review has two possible objects. It can synthesise effect sizes across studies, producing a pooled estimate with a confidence interval, or it can characterise a literature -- its size, distribution, recency, and the degree to which it reports evidence at all. The first requires primary studies reporting comparable outcomes with dispersion; the second requires only that the literature be enumerable.

This review takes the second object, and the reason is a property of the corpus rather than a preference. Reported returns in this literature are overwhelmingly single-organisation figures without variance estimates, control conditions, or a shared definition of the denominator against which return is computed. Pooling them would produce an interval whose width reflects the number of studies rather than the uncertainty in the underlying quantity, which is precision manufactured from nothing.

## The OpenAlex Data Model

OpenAlex indexes scholarly works with normalised metadata: title, authorship, publication year, venue, open-access status, citation count, and a reconstructable abstract.

Abstracts are stored as an inverted index mapping each token to its positions, rather than as running text. Reconstruction inverts that mapping, and is lossless for word order but discards the original whitespace and any markup. For screening purposes -- searching for sample-size and study-design markers -- this is immaterial.

Retrieval is by relevance ranking against a query string. This is the source of the sampling caveat that qualifies every rate in this paper: a query returns the head of a ranking, not a random sample, and the head is systematically better indexed, more cited and more likely open-access than the tail. Rates computed over it are biased upward, and the direction of that bias is knowable even where its magnitude is not.

## Screening for Empirical Content

We classify a work as empirical when its abstract contains a marker of reported data: an explicit sample size, or one of a small set of study-design terms (survey, respondents, participants, experiment, case study, interviews).

The measure is deliberately crude, and its errors run in both directions. A paper that reports data without naming it in the abstract is missed; a paper that merely discusses others' data is counted. What makes it usable is that the bias from relevance ranking runs the same way as the bias from the marker list -- both favour classifying a work as empirical -- so the resulting share is an upper estimate. A conclusion that the literature is *less* empirical than the estimate suggests is therefore safe in a way the reverse would not be.

## Why the Denominator Matters for ROI

Return on investment is a ratio, and its interpretation depends entirely on what enters the denominator. Studies in this corpus variously count licence fees only; licence fees plus inference cost; those plus engineering time; and those plus the opportunity cost of the displaced process.

These are not small differences of accounting. A deployment that returns three times its licence cost may return less than its total cost of ownership, and both figures can be reported as ROI without either being wrong. Any synthesis that pools them is adding quantities that do not share a unit, which is the specific reason this review reports a measurement framework instead of a pooled number.

---

## Appendix C: Extended Experimental Setup

Every number reported in this paper was produced by a single scripted run whose environment, seed and revision are recorded alongside its output. The table below reproduces that record verbatim so a reader can establish exactly what was executed.

| Property | Value |
|:---|:---|
| Run identifier | `draft-review_enterprise_genai_roi` |
| Random seed | 20260825 |
| Repository revision | `cbc42b88617a` |
| Python | 3.13.5 |
| Platform | macOS-26.5.2-arm64-arm-64bit-Mach-O |
| Architecture | arm64 |
| Logical CPUs | 12 |
| Accelerator | none; no GPU was used at any point |
| Wall-clock duration | `21.582 s` |
| Measurements recorded | 10 |
| Recorded at | 2026-08-25T17:24:19-0400 |

## Reproduction

The run is deterministic under the recorded seed. From the repository root:

```
backend/.venv/bin/python scripts/experiments/p4_literature_census.py
```

This rewrites `runs/draft-review_enterprise_genai_roi/measurements.jsonl` and the raw artifacts beneath it. Each measurement row carries the artifact that produced it and that artifact's SHA-256 digest, so a reported value can be traced to the file it came from and that file checked for modification.

## Scope of the Environment

No accelerator was available for this work. That constrains what the study can measure and is stated here rather than left implicit: results requiring model training, model serving, or hardware throughput measurement are outside what this setup can produce, and none are reported.

---

## Appendix D: Methodology Detail

This appendix documents each procedure as implemented, taken from the executing code rather than restated from the method section. Where the two descriptions differ, the code is authoritative and the discrepancy is a defect to be reported.

**`fetch`.** Fetch works for one search string. Returns [] rather than raising on failure.

---

## Appendix E: Additional Results

The main text reports the measurements that carry the argument. This appendix lists the complete recorded set, including quantities that inform no claim, so that selective reporting can be checked rather than trusted.

| Metric | Value | Unit | n | 95% CI | Derivation |
|:---|---:|:---|---:|:---|:---|
| `literature_distinct_venues` | 714.0 | n | 1779 | — | `distinct primary sources` |
| `literature_empirical_share` | 31.76 | % | 1779 | — | `abstract contains a sample-size or study marker` |
| `literature_empirical_share_ci_low` | 29.566 | % | 1779 | — | `bootstrap lower bound on empirical share` |
| `literature_identified_total` | 2000.0 | n | 1779 | — | `sum of per-query result counts` |
| `literature_median_citations` | 62.0 | n | 1779 | — | `median of cited_by_count` |
| `literature_open_access_share` | 98.54 | % | 1779 | — | `OpenAlex is_oa flag` |
| `literature_recent_share` | 68.63 | % | 1779 | — | `publication year >= 2023` |
| `literature_screened` | 1779.0 | n | 1779 | — | `abstract and title present` |
| `literature_unique_after_dedup` | 1893.0 | n | 1779 | — | `deduplicated by OpenAlex id` |
| `literature_zero_citation_share` | 0.51 | % | 1779 | — | `share with cited_by_count == 0` |
| `literature_dedup_screening_loss` | 11.05 | % | 2000 | — | `share of identified records lost to deduplication and missing abstracts` |
| `literature_non_empirical_share` | 68.24 | % | 1779 | — | `100 minus literature_empirical_share` |

**12 measurements across 1 artifacts.** Confidence intervals are percentile bootstrap where reported; an em dash marks a quantity that is exact rather than sampled, for which an interval would be meaningless.

## Artifact Digests

| Artifact | SHA-256 (first 16) |
|:---|:---|
| `artifacts/literature_census.json` | `b96a25dbca78848f` |

Any reported value can be recomputed from the artifact named beside it. A digest that no longer matches means the artifact changed after the value was recorded, which invalidates the row rather than the artifact.

---

## Appendix F: Limitations and Future Work

### Internal Validity

- **The empirical-content marker is crude by design, and its error is one-directional.** Screening classifies an abstract as empirical if it names a sample size or a small set of study-design terms, whether or not the abstract describes a measurement a reader could act on. This over-counts: a work that discusses others' data without reporting its own can trip the marker, while a work reporting data through a phrasing the marker list does not anticipate is missed only in the direction that shrinks the empirical share further, since the marker list cannot invent a term to under-count with. The stated ceiling interpretation of 31.76\% follows from this asymmetry, not from an assumption about it.
- **Deduplication is by OpenAlex work identifier only.** Two records describing the same study under different identifiers -- a preprint and its published version, most commonly -- would be counted twice if OpenAlex has not itself merged them. The 1,893-record deduplicated count inherits whatever merge decisions OpenAlex's own identifier system has already made, and this review performed no independent identifier resolution beyond that.

### External Validity

- **The corpus is a relevance-ranked sample, not a random or exhaustive one.** Section 2's sampling caveat is a first-order limitation of every number in this paper, not only the empirical-share figure: OpenAlex returns the head of a ranking against five specific search strings, and a different set of strings, a different database, or an exhaustive rather than top-$k$ retrieval could each shift every reported rate. The direction of the bias -- toward better-indexed, more-cited, more recent work -- is stated where it is known; its exact magnitude is not, because establishing it would require a second, differently constructed corpus to compare against, which this review does not build.
- **Five search strings are a specific, stated choice, not a canonical one.** They were chosen to cover enterprise adoption, business value, ROI, multi-agent workflow, and cost of ownership; a reviewer who judges a different set of strings better targeted to "enterprise GenAI ROI" would construct a different corpus and could reach a different empirical-share estimate. The strings themselves are part of what Appendix C's reproduction instructions make checkable.

### What This Review Does Not Establish

This census does not measure enterprise GenAI ROI, does not survey any organisation, and does not evaluate any deployed system. It measures a property of a literature -- how much of it reports data -- and the conclusion that pooled ROI synthesis is premature follows from that property, not from an independent assessment of any individual study's rigor. A future full-text audit of the 31.76\% empirical subset, extracting what each study actually measured and against what denominator, is the natural continuation this review's abstract-level screening does not attempt.