---
title: "Decentralized Validation for Non-malicious Arbitrary Fault Tolerance in Paxos"
authors:
  - "Rodrigo R. Barbieri"
  - "Enrique S. dos Santos"
  - "Gustavo M. D. Vieira"
url: "http://arxiv.org/abs/2002.07509v1"
published: "2020-02-18"
citations: "0"
source: "arXiv"
id: "arxiv:2002.07509"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Decentralized Validation for Non-malicious Arbitrary Fault Tolerance in Paxos

**Authors**: Rodrigo R. Barbieri, Enrique S. dos Santos, Gustavo M. D. Vieira
**Published**: 2020-02-18 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2002.07509v1

## Abstract
Fault-tolerant distributed systems offer high reliability because even if faults in their components occur, they do not exhibit erroneous behavior. Depending on the fault model adopted, hardware and software errors that do not result in a process crashing are usually not tolerated. To tolerate these rather common failures the usual solution is to adopt a stronger fault model, such as the arbitrary or Byzantine fault model. Algorithms created for this fault model, however, are considerably more complex and require more system resources than the ones developed for less strict fault models. One approach to reach a middle ground is the non-malicious arbitrary fault model. This model assumes it is possible to detect and filter faults with a given probability, if these faults are not created with malicious intent, allowing the isolation and mapping of these faults to benign faults. In this paper we describe how we incremented an implementation of active replication in the non-malicious fault model with a basic type of distributed validation, where a deviation from the expected algorithm behavior will make a process crash. We experimentally evaluate this implementation using a fault injection framework showing that it is feasible to extend the concept of non-malicious failures beyond hardware failures.
