---
description: Workflow for running citation link verification, numeric claim grounding, and composite score calculation.
---

# Workflow: Fact-Check & Verification Audit

Follow this workflow to audit any drafted manuscript or paper note against hallucination errors.

## Step 1: Citation Link Audit
1. Extract all `[[WikiLink]]` tags from target document content using regex `r'\[\[(.*?)\]\]'`.
2. Check if target filename exists in `vault/01_Papers/`, `vault/02_Concepts/`, `vault/03_Debates/`, or `vault/04_Drafts/`.
3. Categorize into `verified_links` vs `broken_links`.

## Step 2: Numeric Claim Grounding Audit
1. Extract numeric metrics, sample sizes, and p-values using regex:
   `r'(\b\d+(?:\.\d+)?%|\bN\s*=\s*\d+|\bp\s*<[=\s]*0\.\d+|\b\d+\.\d+\b|\b\d{4,}\b)'`
2. Cross-reference extracted claims against source paper texts in `vault/01_Papers/`.
3. Categorize into `grounded_claims` vs `unverified_claims`.

## Step 3: Composite Score Calculation & Metadata Update
1. Compute citation score: $S_{\text{cite}} = \frac{|\text{verified}|}{|\text{total}|} \times 100$
2. Compute metric score: $S_{\text{metric}} = \frac{|\text{grounded}|}{|\text{total}|} \times 100$
3. Compute composite fact-check score:
   $$\text{Score} = 0.6 \times S_{\text{cite}} + 0.4 \times S_{\text{metric}}$$
4. Update document YAML frontmatter:
   - `fact_check_score`: string representation of score (e.g. `"88.5"`)
   - `verification_status`: `"passed"` (if Score $\ge 70.0$) else `"failed"`
   - `verification_matrix`: detailed dictionary string of verified/broken citations and claims.
