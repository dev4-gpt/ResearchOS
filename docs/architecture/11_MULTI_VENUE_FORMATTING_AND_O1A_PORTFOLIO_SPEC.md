# Architectural Specification: Multi-Venue Formatting & O-1A Academic Portfolio Engine

## 1. Overview & Vision

To prove extraordinary ability for O-1A visa portfolios and secure rapid citations, ResearchingOS supports **Multi-Path Publishing** across gold-standard AI/CS conferences and journals:

- **General ML & Deep Learning**: NeurIPS, ICML, ICLR
- **Computer Vision & Multimodal**: CVPR
- **Natural Language Processing & LLMs**: ACL / ARR (ACL Rolling Review)
- **High-Impact Systems & Enterprise Journals**: IEEE Transactions (IEEE TKDE, TPAMI), ACM CSUR / SIGKDD

ResearchingOS allows co-authors and researchers to select a specific target venue OR export **Multi-Path Bundles** containing submission-ready LaTeX files formatted for all premier venues simultaneously.

---

## 2. Venue Format Specifications & Page Limits

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PREMIER VENUE FORMATTING SPECIFICATIONS                         │
├───────────────┬───────────────────────────────┬───────────────────────┬────────────────┤
│ Venue         │ Page Limit & Rules            │ Column / Layout       │ Style Package  │
├───────────────┼───────────────────────────────┼───────────────────────┼────────────────┤
│ NeurIPS       │ 9 pages main text + refs/check│ Single-column 10pt    │ neurips_2026   │
│ ICML          │ 8 pages main body + refs      │ Two-column US Letter  │ icml2026       │
│ CVPR          │ 8 pages main text + refs      │ Two-column US Letter  │ cvpr           │
│ ACL / ARR     │ 8 pages (long paper) + refs   │ Two-column A4/Letter  │ acl            │
│ IEEEtran      │ 10 to 25+ pages (journal)     │ Two-column 10pt       │ IEEEtran.cls   │
│ ACM           │ 12 to 20+ pages (CSUR)        │ Two-column acmart     │ acmart.cls     │
└───────────────┴───────────────────────────────┴───────────────────────┴────────────────┘
```

### 2.1 NeurIPS (Neural Information Processing Systems)
- **Format**: Single-column layout using 10pt Times font (`neurips_2026.sty`).
- **Page Limit**: 9 pages main text (excluding references and mandatory NeurIPS Paper Checklist).

### 2.2 ICML (International Conference on Machine Learning)
- **Format**: Two-column layout, US Letter size (`icml2026.sty`).
- **Page Limit**: 8 pages main body + unlimited additional pages for references and appendices.

### 2.3 CVPR (Conference on Computer Vision and Pattern Recognition)
- **Format**: Two-column layout (`cvpr.sty`).
- **Page Limit**: 8 pages main body (excluding references).

### 2.4 ACL / ARR (Association for Computational Linguistics)
- **Format**: Two-column layout, ACL Rolling Review track (`acl.sty`).
- **Page Limit**: 8 pages long paper + unlimited references.

### 2.5 IEEEtran & ACM
- **Format**: Two-column journal format (`IEEEtran.cls` / `acmart.cls`).
- **Page Limit**: 10 to 25+ pages for systematic literature reviews and meta-taxonomies.

---

## 3. Automated Venue Selection & Multi-Path Export

1. **Automated Topic-Domain Mapping**: When no venue is explicitly specified, `TopicRecommenderService` maps keywords to the optimal gold-standard venue.
2. **Multi-Path Publishing Endpoint (`/api/vault/export-venue-latex?venue=ALL`)**: Generates LaTeX files for NeurIPS, ICML, CVPR, ACL, IEEEtran, and ACM in a single 1-click download.
