---
title: "A supervised topic embedding model and its application"
authors:
  - "Weiran Xu"
  - "Koji Eguchi"
url: "https://doi.org/10.1371/journal.pone.0277104"
published: "2022-11-04"
citations: "0"
source: "PLOS"
id: "plos:10.1371/journal.pone.0277104"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "test-topic"
---
```obsidian

year: 2022
publication_date: 2022-11-04
doi: 10.1371/journal.pone.0277104
journal: PLOS ONE
keywords: [topic embedding, supervised learning, regression, natural language processing, text analysis]

# A supervised topic embedding model and its application

## 📄 Abstract

This paper introduces [[rTopicVec]], a [[supervised topic embedding model]] designed to predict response variables associated with documents by analyzing text data. It builds upon the concepts of [[topic modeling]] and [[word embedding]], combining them to model latent topics within a [[word embedding space]]. The core innovation is the incorporation of [[regression]] into the topic embedding framework, allowing for joint modeling of each document and its paired numerical label. The model, including a regularized variant, is capable of yielding topics predictive of response variables and predicting these variables for unlabeled documents. Experimental evaluation on two [[regression tasks]]—predicting stock return rates from news articles and movie ratings from reviews—demonstrated that [[rTopicVec]] achieved more accurate prediction performance compared to three baselines, with a statistically significant difference.

## 🎯 Claims and Hypotheses

*   **Claim 1**: We propose [[rTopicVec]], a [[supervised topic embedding model]] that predicts response variables associated with documents by analyzing the text data.
*   **Claim 2**: [[rTopicVec]] and its regularized variant incorporate [[regression]] into the [[topic embedding model]] to model each document and a numerical label paired with the document jointly.
*   **Claim 3**: Our models yield topics predictive of the response variables as well as predict response variables for unlabeled documents.
*   **Hypothesis**: The prediction performance of [[rTopicVec]] will be more accurate than baseline models on [[regression tasks]].

## 📝 Methodologies, Algorithms, and System Architecture

### Proposed Model: [[rTopicVec]]

*   **Type**: A [[supervised topic embedding model]].
*   **Core Idea**: Combines principles from [[topic modeling]] and [[word embedding]].
    *   **Topic Modeling**: Leverages document-level word co-occurrence patterns to learn latent topics for each document.
    *   **Word Embedding**: Maps words into a low-dimensional continuous semantic space by exploiting local word co-occurrence patterns within a small context window.
    *   **Topic Embedding**: Benefits from combining the above two approaches by modeling latent topics in a [[word embedding space]].
*   **Supervision**: Incorporates [[regression]] into the [[topic embedding model]].
*   **Objective**: Models each document and a numerical label paired with the document jointly.
*   **Variants**: Includes a regularized variant.
*   **Capabilities**:
    *   Yields topics that are predictive of response variables.
    *   Predicts response variables for unlabeled documents.

## 📊 Experimental Results, Datasets, and Quantitative Benchmarks

### Evaluation Tasks

The models were evaluated on two distinct [[regression tasks]]:

1.  **Task**: Predicting [[stock return rates]].
    *   **Dataset**: [[News articles]] provided by [[Thomson Reuters]].
2.  **Task**: Predicting [[movie ratings]].
    *   **Dataset**: [[Movie reviews]].

### Performance Benchmarks

*   **Result**: The prediction performance of [[rTopicVec]] models was found to be "more accurate" compared to three unspecified baselines.
*   **Significance**: The observed difference in performance was statistically significant.
*   *Note: Specific quantitative metrics (e.g., RMSE, MAE, R-squared values) or exact performance improvements are not provided in the abstract/full text extract.*

## 🚧 Limitations

The provided text (abstract and full text being identical) does not explicitly state any limitations acknowledged by the authors.
```