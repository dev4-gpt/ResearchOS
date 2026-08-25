---
title: "Arma: Byzantine Fault Tolerant Consensus with Horizontal Scalability"
authors:
  - "Yacov Manevich"
  - "Hagar Meir"
  - "Kaoutar Elkhiyaoui"
  - "Yoav Tock"
  - "May Buzaglo"
url: "http://arxiv.org/abs/2405.16575v2"
published: "2024-05-26"
citations: "0"
source: "arXiv"
id: "arxiv:2405.16575"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-trustworthy-multi-agent-systems-formal-verification"
---
# Arma: Byzantine Fault Tolerant Consensus with Horizontal Scalability

**Authors**: Yacov Manevich, Hagar Meir, Kaoutar Elkhiyaoui, Yoav Tock, May Buzaglo
**Published**: 2024-05-26 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2405.16575v2

## Abstract
Arma is a Byzantine Fault Tolerant (BFT) consensus system designed to achieve horizontal scalability across all hardware resources: network bandwidth, CPU, and disk I/O. As opposed to preceding BFT protocols, Arma separates the dissemination and validation of client transactions from the consensus process, restricting the latter to totally ordering only metadata of batches of transactions. This separation enables each party to distribute compute and storage resources for transaction validation, dissemination and disk I/O among multiple machines, resulting in horizontal scalability. Additionally, Arma ensures censorship resistance by imposing a maximum time limit on the inclusion of client transactions. We built and evaluated two Arma prototypes. The first is an independent system handling over 200,000 transactions per second, the second integrated into Hyperledger Fabric, speeding its consensus by an order of magnitude.
