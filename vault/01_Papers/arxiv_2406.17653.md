---
title: "Low-Overhead Transversal Fault Tolerance for Universal Quantum Computation"
authors:
  - "Hengyun Zhou"
  - "Chen Zhao"
  - "Madelyn Cain"
  - "Dolev Bluvstein"
  - "Nishad Maskara"
  - "Casey Duckering"
  - "Hong-Ye Hu"
  - "Sheng-Tao Wang"
  - "Aleksander Kubica"
  - "Mikhail D. Lukin"
url: "http://arxiv.org/abs/2406.17653v2"
published: "2024-06-25"
citations: "0"
source: "arXiv"
id: "arxiv:2406.17653"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Low-Overhead Transversal Fault Tolerance for Universal Quantum Computation

**Authors**: Hengyun Zhou, Chen Zhao, Madelyn Cain, Dolev Bluvstein, Nishad Maskara, Casey Duckering, Hong-Ye Hu, Sheng-Tao Wang, Aleksander Kubica, Mikhail D. Lukin
**Published**: 2024-06-25 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2406.17653v2

## Abstract
Fast, reliable logical operations are essential for realizing useful quantum computers. By redundantly encoding logical qubits into many physical qubits and using syndrome measurements to detect and correct errors, one can achieve low logical error rates. However, for many practical quantum error correcting (QEC) codes such as the surface code, due to syndrome measurement errors, standard constructions require multiple extraction rounds -- on the order of the code distance $d$ -- for fault-tolerant computation, particularly considering fault-tolerant state preparation. Here, we show that logical operations can be performed fault-tolerantly with only a constant number of extraction rounds for a broad class of QEC codes, including the surface code with magic state inputs and feed-forward, to achieve ``transversal algorithmic fault tolerance". Through the combination of transversal operations and novel strategies for correlated decoding, despite only having access to partial syndrome information, we prove that the deviation from the ideal logical measurement distribution can be made exponentially small in the distance, even if the instantaneous quantum state cannot be made close to a logical codeword due to measurement errors. We supplement this proof with circuit-level simulations in a range of relevant settings, demonstrating the fault tolerance and competitive performance of our approach. Our work sheds new light on the theory of quantum fault tolerance and has the potential to reduce the space-time cost of practical fault-tolerant quantum computation by over an order of magnitude.
