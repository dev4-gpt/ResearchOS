---
title: "SWE-Lego: Pushing the Limits of Supervised Fine-tuning for Software Issue Resolving"
authors:
  - "Chaofan Tao"
  - "Jierun Chen"
  - "Yuxin Jiang"
  - "Kaiqi Kou"
  - "Shaowei Wang"
  - "Ruoyu Wang"
  - "Xiaohui Li"
  - "Sidi Yang"
  - "Yiming Du"
  - "Jianbo Dai"
  - "Zhiming Mao"
  - "Xinyu Wang"
  - "Lifeng Shang"
  - "Haoli Bai"
url: "http://arxiv.org/abs/2601.01426v2"
published: "2026-01-04"
citations: "0"
source: "arXiv"
id: "arxiv:2601.01426"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# SWE-Lego: Pushing the Limits of Supervised Fine-tuning for Software Issue Resolving

**Authors**: Chaofan Tao, Jierun Chen, Yuxin Jiang, Kaiqi Kou, Shaowei Wang, Ruoyu Wang, Xiaohui Li, Sidi Yang, Yiming Du, Jianbo Dai, Zhiming Mao, Xinyu Wang, Lifeng Shang, Haoli Bai
**Published**: 2026-01-04 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2601.01426v2

## Abstract
We present SWE-Lego, a supervised fine-tuning (SFT) recipe designed to achieve state-ofthe-art performance in software engineering (SWE) issue resolving. In contrast to prevalent methods that rely on complex training paradigms (e.g., mid-training, SFT, reinforcement learning, and their combinations), we explore how to push the limits of a lightweight SFT-only approach for SWE tasks. SWE-Lego comprises three core building blocks, with key findings summarized as follows: 1) the SWE-Lego dataset, a collection of 32k highquality task instances and 18k validated trajectories, combining real and synthetic data to complement each other in both quality and quantity; 2) a refined SFT procedure with error masking and a difficulty-based curriculum, which demonstrably improves action quality and overall performance. Empirical results show that with these two building bricks alone,the SFT can push SWE-Lego models to state-of-the-art performance among open-source models of comparable size on SWE-bench Verified: SWE-Lego-Qwen3-8B reaches 42.2%, and SWE-Lego-Qwen3-32B attains 52.6%. 3) We further evaluate and improve test-time scaling (TTS) built upon the SFT foundation. Based on a well-trained verifier, SWE-Lego models can be significantly boosted--for example, 42.2% to 49.6% and 52.6% to 58.8% under TTS@16 for the 8B and 32B models, respectively.
