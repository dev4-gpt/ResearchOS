---
title: "Do VLMs Share Safety Neurons Across Modalities?"
arxiv_id: "2608.30750"
source_url: "https://arxiv.org/abs/2608.30750"
source_type: "primary_preprint"
project: "vlm-safety"
full_pdf_ingested: false
full_text_obtained: true
retrieval: "OpenResearch paper --full; extracted text stored locally in .tools/vlm-research/literature/arxiv_2608.30750.txt"
visual_review_completed: false
---

The authors examine text and visual safety with neuron ablations and direction-level interventions. Their tested decoder mechanisms show a dominant, more localized text refusal pathway and more distributed visual signals. They explicitly limit inference to the interventions, datasets and backbone components examined; their selected harmful intents emphasize a regime where text refusal is active. Judge dependence and visual-data concentration are acknowledged limitations. Full text inspected: causal comparison, direction analysis, discussion and limitations.

Proposal implication (our interpretation): behavioral text/image correlations alone cannot establish shared causal mechanisms. A common refusal pathway can coexist with modality-specific recognition failures or intervention-specific trade-offs. Direction ablations need random controls and capability checks to distinguish safety effects from model impairment.

Primary source: [arXiv](https://arxiv.org/abs/2608.30750). The abstract page reports EMNLP acceptance; proceedings verification has not been completed in this review.
