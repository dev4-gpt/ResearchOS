---
title: "Cloud-Edge Orchestration for Smart Cities: A Review of Kubernetes-based Orchestration Architectures"
authors:
  - "Sebastian Böhm"
  - "Guido Wirtz"
url: "https://doi.org/10.4108/eetsc.v6i18.1197"
published: "2022"
citations: "42"
source: "Crossref"
id: "10.4108/eetsc.v6i18.1197"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-enterprise-adoption-of-multi-agent-ai-systems-infr"
---
# Cloud-Edge Orchestration for Smart Cities: A Review of Kubernetes-based Orchestration Architectures

**Authors**: Sebastian Böhm, Guido Wirtz
**Published**: 2022 | **Source**: Crossref
**URL**: https://doi.org/10.4108/eetsc.v6i18.1197

## Abstract
Edge computing offers computational resources near data-generating devices to enable low-latency access. Especially for smart city contexts, edge computing becomes inevitable for providing real-time services, like air quality monitoring systems. Kubernetes, a popular container orchestration platform, is often used to efficiently manage containerized applications in smart cities. Although it misses essential requirements of edge computing, like network-related metrics for scheduling decisions, it is still considered. This paper analyzes custom cloud-edge architectures implemented with Kubernetes. Specifically, we analyze how essential requirements of edge orchestration in smart cities are solved. Also, shortcomings are identified in these architectures based on the fundamental requirements of edge orchestration. We conduct a literature review to obtain the general requirements of edge computing and edge orchestration for our analysis. We map these requirements to the capabilities of Kubernetes-based cloud-edge architectures to assess their level of achievement. Issues like using network-related metrics and the missing topology-awareness of networks are partially solved. However, requirements like real-time resource utilization, fault-tolerance, and the placement of container registries are in the early stages. We conclude that Kubernetes is an eligible candidate for cloudedge orchestration. When the formerly mentioned issues are solved, Kubernetes can successfully contribute latency-critical, large-scale, and multi-tenant application deployments for smart cities.
