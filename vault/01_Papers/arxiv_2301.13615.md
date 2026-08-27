---
title: "Property-Based Mutation Testing"
authors:
  - "Ezio Bartocci"
  - "Leonardo Mariani"
  - "Dejan Nickovic"
  - "Drishti Yadav"
url: "http://arxiv.org/abs/2301.13615v1"
published: "2023-01-31"
citations: "0"
source: "arXiv"
id: "arxiv:2301.13615"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Property-Based Mutation Testing

**Authors**: Ezio Bartocci, Leonardo Mariani, Dejan Nickovic, Drishti Yadav
**Published**: 2023-01-31 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2301.13615v1

## Abstract
Mutation testing is an established software quality assurance technique for the assessment of test suites. While it is well-suited to estimate the general fault-revealing capability of a test suite, it is not practical and informative when the software under test must be validated against specific requirements. This is often the case for embedded software, where the software is typically validated against rigorously-specified safety properties. In such a scenario (i) a mutant is relevant only if it can impact the satisfaction of the tested properties, and (ii) a mutant is meaningfully-killed with respect to a property only if it causes the violation of that property. To address these limitations of mutation testing, we introduce property-based mutation testing, a method for assessing the capability of a test suite to exercise the software with respect to a given property. We evaluate our property-based mutation testing framework on Simulink models of safety-critical Cyber-Physical Systems (CPS) from the automotive and avionic domains and demonstrate how property-based mutation testing is more informative than regular mutation testing. These results open new perspectives in both mutation testing and test case generation of CPS.
