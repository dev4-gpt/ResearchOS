---
title: "Mull it over: mutation testing based on LLVM"
authors:
  - "Alex Denisov"
  - "Stanislav Pankevich"
url: "http://arxiv.org/abs/1908.01540v1"
published: "2019-08-05"
citations: "0"
source: "arXiv"
id: "arxiv:1908.01540"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Mull it over: mutation testing based on LLVM

**Authors**: Alex Denisov, Stanislav Pankevich
**Published**: 2019-08-05 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1908.01540v1

## Abstract
This paper describes Mull, an open-source tool for mutation testing based on the LLVM framework. Mull works with LLVM IR, a low-level intermediate representation, to perform mutations, and uses LLVM JIT for just-in-time compilation. This design choice enables the following two capabilities of Mull: language independence and fine-grained control over compilation and execution of a tested program and its mutations. Mull can work with code written in any programming language that supports compilation to LLVM IR, such as C, C++, Rust, or Swift. Direct manipulation of LLVM IR allows Mull to do less work to generate mutations: only modified fragments of IR code are recompiled, and this results in faster processing of mutated programs. To our knowledge, no existing mutation testing tool provides these capabilities for compiled programming languages. We describe the algorithm and implementation details of Mull, highlight current limitations of Mull, and present the results of our evaluation of Mull on real-world projects such as RODOS, OpenSSL, LLVM.
