---
title: "Deductive Verification of Unmodified Linux Kernel Library Functions"
authors:
  - "Denis Efremov"
  - "Mikhail Mandrykin"
  - "Alexey Khoroshilov"
url: "http://arxiv.org/abs/1809.00626v1"
published: "2018-09-03"
citations: "0"
source: "arXiv"
id: "arxiv:1809.00626"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Deductive Verification of Unmodified Linux Kernel Library Functions

**Authors**: Denis Efremov, Mikhail Mandrykin, Alexey Khoroshilov
**Published**: 2018-09-03 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1809.00626v1

## Abstract
This paper presents results from the development and evaluation of a deductive verification benchmark consisting of 26 unmodified Linux kernel library functions implementing conventional memory and string operations. The formal contract of the functions was extracted from their source code and was represented in the form of preconditions and postconditions. The correctness of 23 functions was completely proved using AstraVer toolset, although success for 11 functions was achieved using 2 new specification language constructs. Another 2 functions were proved after a minor modification of their source code, while the final one cannot be completely proved using the existing memory model. The benchmark can be used for the testing and evaluation of deductive verification tools and as a starting point for verifying other parts of the Linux kernel.
