---
title: "Guest Editorial: Special Topic on Data-enabled Theoretical Chemistry"
authors:
  - "Matthias Rupp"
  - "O. Anatole von Lilienfeld"
  - "Kieron Burke"
url: "http://arxiv.org/abs/1806.02690v2"
published: "2018-06-07"
citations: "0"
source: "arXiv"
id: "arxiv:1806.02690"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "test-topic"
---
```obsidian
---
title: "Guest Editorial: Special Topic on Data-enabled Theoretical Chemistry"
authors: ["Matthias Rupp", "O. Anatole von Lilienfeld", "Kieron Burke"]
publication_date: "2018-06-07"
doi: "10.1063/1.5043213"
arxiv_id: "1806.02690v2"
journal: "The Journal of Chemical Physics"
volume: "148"
issue: "24"
page: "241401"
citations: 0 # As per provided metadata
tags: ["Editorial", "Theoretical Chemistry", "Machine Learning", "Cheminformatics", "Materials Informatics"]
---

# Guest Editorial: Special Topic on Data-enabled Theoretical Chemistry

## Abstract
This paper provides a survey of the contributions to The Journal of Chemical Physics [[Special Topic on Data-enabled Theoretical Chemistry]], including a glossary of relevant [[Machine Learning]] terms. The editorial aims to guide non-experts in the rapidly evolving field of data-enabled chemistry.

## 1. Introduction and Overview
This editorial welcomes readers to the [[Journal of Chemical Physics]] [[Special Topic on Data-enabled Theoretical Chemistry]], highlighting the rapid growth and impact of data-driven approaches in theoretical and computational chemistry. The scope of "data-enabled chemistry" is interpreted broadly to include [[algorithmic developments]] under the rubric of [[Machine Learning]], applied across areas from small molecule chemistry to materials science and protein behavior.

The editorial provides:
*   A brief glossary of [[Machine Learning]] terms (Section II) with an emphasis on concepts used in physical chemistry and materials science applications.
*   A survey of contributions to the [[Special Topic]] (Section III), grouped by the physical and chemical processes and systems they address.
*   A nomenclature table for abbreviations.
*   An overview table of all articles in the [[Special Topic]], summarizing [[ML Method]], [[QM Method]], [[Systems]], and [[Keywords]].

## 2. Key Concepts and Nomenclature

### 2.1. Glossary of Terms
*   **AI (Artificial Intelligence)**: The study of machines that exhibit intelligent behavior. Traditionally involves (symbolic) knowledge representation and logical reasoning.
*   **B3LYP (Becke, three-parameter, Lee-Yang-Parr)**: A hybrid [[DFT functional]].
*   **CCSD(T) (Coupled Cluster with Single, Double and perturbative Triple excitations)**: An [[electronic structure method]].
*   **Cheminformatics**: Intersection of chemistry and computer science.
*   **Clustering**: A [[Machine Learning]] task to group similar data points.
*   **Data Mining**: Similar to [[Machine Learning]], but more concerned with the extraction of new patterns in large datasets.
*   **Data Science**: Often used to mean applied [[Machine Learning]] and statistics; no consensus definition has emerged yet.
*   **DFT (Density Functional Theory)**: An [[electronic structure method]].
*   **DFTB (Density Functional Theory Tight Binding)**: An [[electronic structure method]].
*   **DNN (Deep Neural Network)**: See [[(A)NN]].
*   **EAM (Embedded Atom Model/Method)**: An [[interatomic potential]].
*   **GAP (Gaussian Approximation Potential)**: A [[Machine Learning potential]].
*   **HOMO (Highest Occupied Molecular Orbital)**.
*   **KRR (Kernel Ridge Regression)**: A [[Machine Learning]] algorithm, often used for regression tasks.
*   **LUMO (Lowest Unoccupied Molecular Orbital)**.
*   **MAE (Mean Absolute Error)**: A measure for error, used in performance evaluation.
*   **Materials Informatics**: A newer field at the intersection of materials science and computer science.
*   **ML (Machine Learning)**: An umbrella term referring to algorithms that improve with data ("learn from experience"), mostly for analysis or prediction. Relies on given data to make statements about new data, rather than explicit programming.
*   **MD (Molecular Dynamics)**: A [[simulation technique]].
*   **MP2 (Møller-Plesset perturbation theory to Second order)**: An [[electronic structure method]].
*   **(A)NN (Artificial Neural Network / Neural Network)**: A [[Machine Learning]] algorithm.
*   **Pattern Recognition**: Essentially a synonym for [[Machine Learning]].
*   **QM/MM (Quantum Mechanics/Molecular Mechanics)**: A [[molecular simulation method]].
*   **QSPR (Quantitative Structure-Property Relationship)**: Relates molecular features or descriptors to, usually experimental, molecular properties.
*   **RMSE (Root Mean Squared Error)**: A measure for error, used in performance evaluation.
*   **SINDy (Sparse Identification of Nonlinear Dynamics)**: A [[Machine Learning]] method.
*   **SNAP (Spectral Neighbor Analysis Potential)**: A [[Machine Learning potential]].
*   **Supervised Learning**: [[Machine Learning]] where examples are pairs of input (x) and label (y), and the task is to predict the label of new examples (e.g., molecules and their energy).
*   **SVM (Support Vector Machine)**: A [[Machine Learning]] algorithm.
*   **tICA (time structure Independent Component Analysis)**: A [[Machine Learning]] method.
*   **Unsupervised Learning**: [[Machine Learning]] where only inputs (x) are given, and the task is to find hidden structures or patterns (e.g., clustering, dimensionality reduction).
*   **Virtual Screening**: Computational screening of large databases for compounds with desired properties.

### 2.2. Problem Types Addressed by ML
*   **Supervised Learning**: Learning a mapping from input *x* to label *y* using examples of *(x, y)* pairs.
    *   **Regression**: Predicting continuous labels (e.g., energy, force).
    *   **Classification**: Predicting discrete labels (e.g., stable/unstable, metal/insulator).
*   **Unsupervised Learning**: Finding structure in data where no labels *y* are provided.
    *   **Dimensionality Reduction**: Reducing the number of features describing each example.
    *   **Clustering**: Grouping similar examples together.
*   **Reinforcement Learning**: Learning an optimal sequence of actions through interaction with an environment to maximize a reward signal.

## 3. Methodologies, Algorithms, and Architectures
The editorial itself does not introduce new methodologies but surveys those presented in the [[Special Topic]].

### 3.1. Machine Learning Methods Surveyed (from Table I)
*   [[Neural Network]] (NN) / [[Deep Neural Network]] (DNN)
*   [[Kernel Ridge Regression]] (KRR)
*   [[Gaussian Process Regression]] (GPR)
*   [[Multilinear regression]]
*   [[Regression trees]]
*   [[Linear regression]]
*   [[Regularized linear regression]]
*   [[Polynomial fit]]
*   [[Support Vector Machine]] (SVM)
*   [[Genetic algorithm]]
*   [[Monte Carlo tree search]]
*   [[Binary classification trees]]
*   [[Subset selection]]
*   [[Outlier detection]]
*   [[Sparse regression]]
*   [[Time-lagged autoencoder]]
*   [[Markov state model]]
*   [[tICA (time structure Independent Component Analysis)]]
*   [[Autoencoder]]
*   [[Graph analysis]]
*   [[Data analysis]]

### 3.2. Quantum Mechanical (QM) and Other Computational Methods Surveyed (from Table I)
*   [[Density Functional Theory]] (DFT)
*   [[Coupled Cluster with Single, Double and perturbative Triple excitations]] (CCSD(T))
*   [[Density Functional Theory Tight Binding]] (DFTB)
*   [[Force field]]
*   [[Embedded Atom Model]] (EAM)
*   [[Harris approximation]]
*   [[Analytic potential]]

## 4. Experimental Results, Datasets, and Quantitative Benchmarks

### 4.1. Publication Trend
*   **Observation**: A search for "machine learning" and "chemistry" or "materials" on Web of Science (taken June 5, 2018) shows a rapid growth in the number of publications over the last three decades. (Visualized in Fig. 1).
*   **Quantitative Benchmark**: The average number of citations per article in this search is **12**.

### 4.2. Systems Studied (from Table I, representative examples from the Special Topic)
*   Hydrocarbon molecules
*   Small organic molecules
*   Water, solids, bulk crystals, C20-fullerene
*   Dimers, hydrogen-bonded complexes
*   Liquid water, Al-Si-Mg alloy
*   Li-C guest-host systems, Li xSi alloys
*   Na+, Cl− ion-water clusters
*   Tantalum
*   Ni nanoclusters
*   Nicotine, water cluster
*   Cu surface grain boundaries
*   Water/ZnO(10 ¯10) interface
*   Formic acid dimer
*   Model systems (e.g., for Hartree-exchange-correlation potential, kinetic energy density functional)
*   AB2C2 ternary intermetallics, Inorganic crystals, Rigid-molecule crystals
*   Ag, Co grain boundaries
*   Boron-doped graphene
*   Main group chemistry
*   Dye-labeled polyproline-20, Villin peptide
*   Donor-acceptor polymers, Organic polymers
*   Perovskite oxides, elpasolite halides
*   Anatase TiO2(001)
*   Tyrosine phosphatase 1E (Proteins)
*   Antimicrobial peptides
*   Various (G3/99 test set)

## 5. Stated Limitations
*   The terms [[Artificial Intelligence]], [[Machine Learning]], [[Big Data]], etc., are acknowledged as "vague but computer-driven terms."
*   For [[Artificial Intelligence]], the scope is noted as "less clear-cut," evidenced by "the lack of a formal definition of intelligence."
*   For the term [[Data Science]], it is stated that "no consensus has emerged yet."
*   The absolute rate of publications shown in Fig. 1 is acknowledged as "rather arbitrary, depending on the precise search terms," though the rapid growth trend is robust.
```