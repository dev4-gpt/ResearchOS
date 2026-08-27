---
title: "Scheduling and Checkpointing optimization algorithm for Byzantine fault tolerance in Cloud Clusters"
authors:
  - "Sathya Chinnathambi"
  - "Agilan Santhanam"
url: "http://arxiv.org/abs/1802.00951v1"
published: "2018-02-03"
citations: "0"
source: "arXiv"
id: "arxiv:1802.00951"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Scheduling and Checkpointing optimization algorithm for Byzantine fault tolerance in Cloud Clusters

**Authors**: Sathya Chinnathambi, Agilan Santhanam
**Published**: 2018-02-03 | **Source**: arXiv
**URL**: http://arxiv.org/abs/1802.00951v1

## Abstract
Among those faults Byzantine faults offers serious challenge to fault tolerance mechanism, because it often go undetected at the initial stage and it can easily propagate to other VMs before a detection is made. Consequently some of the mission critical application such as air traffic control, online baking etc still staying away from the cloud for such reasons. However if a Byzantine faults is not detected and tolerated at initial stage then applications such as big data analytics can go completely wrong in spite of hours of computations performed by the entire cloud. Therefore in the previous work a fool-proof Byzantine fault detection has been proposed, as a continuation this work designs a scheduling algorithm (WSSS) and checkpoint optimization algorithm (TCC) to tolerate and eliminate the Byzantine faults before it makes any impact. The WSSS algorithm keeps track of server performance which is part of Virtual Clusters to help allocate best performing server to mission critical application. WSSS therefore ranks the servers based on a counter which monitors every Virtual Nodes (VN) for time and performance failures. The TCC algorithm works to generalize the possible Byzantine error prone region through monitoring delay variation to start new VNs with previous checkpointing. Moreover it can stretch the state interval for performing and error free VNs in an effect to minimize the space, time and cost overheads caused by checkpointing. The analysis is performed with plotting state transition and CloudSim based simulation. The result shows TCC reduces fault tolerance overhead exponentially and the WSSS allots virtual resources effectively
