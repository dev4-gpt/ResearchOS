# Layer Specification: Fact-Checker & Zero-Hallucination Linter

## 1. Overview

The **Fact-Checker Service** (`backend/services/fact_checker.py`) is an automated verification linter that audits draft manuscripts against hallucination errors. It verifies inline citations and checks whether quantitative claims ($N=...$, $\%$, $p$-values) are grounded in source paper text.

---

## 2. Audit Sub-Engines

### 2.1 Citation Link Linter Sub-Engine
- **Extraction**: Parses all `[[WikiLink]]` tags using regex `r'\[\[(.*?)\]\]'`.
- **Target Verification**: Checks if the referenced paper filename (e.g. `crossref_10.2139_ssrn.5260645`) exists within `vault/01_Papers/`.
- **Classification**:
  - `verified_links`: Target file exists in vault.
  - `broken_links`: Target file missing or link formatted incorrectly.

### 2.2 Metric Grounding Linter Sub-Engine
- **Claim Extraction**: Extracts numeric metrics, sample sizes, and p-values using regex:
  `r'(\b\d+(?:\.\d+)?%|\bN\s*=\s*\d+|\bp\s*<[=\s]*0\.\d+|\b\d+\.\d+\b|\b\d{4,}\b)'`
- **Grounding Cross-Reference**: Scans all source text contents in `vault/01_Papers/` to check if the exact metric appears in ingested evidence.
- **Classification**:
  - `grounded_claims`: Metric confirmed present in source corpus.
  - `unverified_claims`: Metric missing from source corpus.

---

## 3. Fact-Check Scoring Formulations

The composite fact-check score is calculated as a weighted average:

$$S_{\text{cite}} = \frac{|\text{verified\_links}|}{|\text{total\_citations}|} \times 100$$

$$S_{\text{metric}} = \frac{|\text{grounded\_claims}|}{|\text{total\_metrics}|} \times 100$$

$$\text{Fact-Check Score} = 0.6 \times S_{\text{cite}} + 0.4 \times S_{\text{metric}}$$

- **Pass Threshold**: $\text{Fact-Check Score} \ge 70.0\%$ (`verification_status: "passed"`).
