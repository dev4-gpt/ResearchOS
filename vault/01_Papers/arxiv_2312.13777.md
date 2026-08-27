---
title: "Arma: Byzantine Fault Tolerant consensus with Linear Scalability"
authors:
  - "Yacov Manevich"
url: "http://arxiv.org/abs/2312.13777v1"
published: "2023-12-21"
citations: "0"
source: "arXiv"
id: "arxiv:2312.13777"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# Arma: Byzantine Fault Tolerant consensus with Linear Scalability

**Authors**: Yacov Manevich
**Published**: 2023-12-21 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2312.13777v1

## Abstract
Arma is a Byzantine Fault Tolerant (BFT) consensus system designed to achieve linear scalability across all hardware resources: network bandwidth, CPU, and disk I/O. As opposed to preceding BFT protocols, Arma separates the dissemination and validation of client transactions from the consensus process, restricting the latter to totally ordering only metadata of batches of transactions. This separation enables each party to distribute compute and storage resources for transaction validation, dissemination and disk I/O among multiple machines, resulting in linear scalability. Additionally, Arma ensures censorship resistance by imposing a maximum time limit for the inclusion of client transactions. We build a prototype implementation of Arma and evaluate its performance experimentally. Our results show that Arma totally orders over 100,000 transactions per second when deployed in a WAN setting and integrated into Hyperledger Fabric.
