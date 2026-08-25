---
title: "Tigris: a DSL and Framework for Monitoring Software Systems at Runtime"
authors:
  - "Jhonny Mertz"
  - "Ingrid Nunes"
url: "http://arxiv.org/abs/2103.15986v1"
published: "2021-03-29"
citations: "0"
source: "arXiv"
id: "arxiv:2103.15986"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Tigris: a DSL and Framework for Monitoring Software Systems at Runtime

**Authors**: Jhonny Mertz, Ingrid Nunes
**Published**: 2021-03-29 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2103.15986v1

## Abstract
The understanding of the behavioral aspects of a software system is an essential enabler for many software engineering activities, such as adaptation. This involves collecting runtime data from the system so that it is possible to analyze the collected data to guide actions upon the system. Consequently, software monitoring imposes practical challenges because it is often done by intercepting the system execution and recording gathered information. Such monitoring may degrade the performance and disrupt the system execution to unacceptable levels. In this paper, we introduce a two-phase monitoring approach to support the monitoring step in adaptive systems. The first phase collects lightweight coarse-grained information and identifies relevant parts of the software that should be monitored in detail based on a provided domain-specific language. This language is informed by a systematic literature review. The second phase collects relevant and fine-grained information needed for deciding whether and how to adapt the managed system. Our approach is implemented as a framework, called Tigris, that can be seamlessly integrated into existing software systems to support monitoring-based activities. To validate our proposal, we instantiated Tigris to support an application-level caching approach, which adapts caching decisions of a software system at runtime to improve its performance.
