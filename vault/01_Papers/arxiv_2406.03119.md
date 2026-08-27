---
title: "Automated Verification of Silq Quantum Programs using SMT Solvers"
authors:
  - "Marco Lewis"
  - "Paolo Zuliani"
  - "Sadegh Soudjani"
url: "http://arxiv.org/abs/2406.03119v1"
published: "2024-06-05"
citations: "0"
source: "arXiv"
id: "arxiv:2406.03119"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Automated Verification of Silq Quantum Programs using SMT Solvers

**Authors**: Marco Lewis, Paolo Zuliani, Sadegh Soudjani
**Published**: 2024-06-05 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2406.03119v1

## Abstract
We present SilVer (Silq Verification), an automated tool for verifying behaviors of quantum programs written in Silq, which is a high-level programming language for quantum computing. The goal of the verification is to ensure correctness of the Silq quantum program against user-defined specifications using SMT solvers. We introduce a programming model that is based on a quantum RAM-style computer as an interface between Silq programs and SMT proof obligations, allowing for control of quantum operations using both classical and quantum conditions. Additionally, users can employ measurement flags within the specification to easily specify conditions that measurement results require to satisfy for being a valid behavior. We provide case studies on the verification of generating entangled states and multiple oracle-based algorithms.
