---
title: "LoRA-C: Parameter-Efficient Fine-Tuning of Robust CNN for IoT Devices"
authors:
  - "Chuntao Ding"
  - "Xu Cao"
  - "Jianhang Xie"
  - "Linlin Fan"
  - "Shangguang Wang"
  - "Zhichao Lu"
url: "http://arxiv.org/abs/2410.16954v2"
published: "2024-10-22"
citations: "0"
source: "arXiv"
id: "arxiv:2410.16954"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# LoRA-C: Parameter-Efficient Fine-Tuning of Robust CNN for IoT Devices

**Authors**: Chuntao Ding, Xu Cao, Jianhang Xie, Linlin Fan, Shangguang Wang, Zhichao Lu
**Published**: 2024-10-22 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2410.16954v2

## Abstract
Efficient fine-tuning of pre-trained convolutional neural network (CNN) models using local data is essential for providing high-quality services to users using ubiquitous and resource-limited Internet of Things (IoT) devices. Low-Rank Adaptation (LoRA) fine-tuning has attracted widespread attention from industry and academia because it is simple, efficient, and does not incur any additional reasoning burden. However, most of the existing advanced methods use LoRA to fine-tune Transformer, and there are few studies on using LoRA to fine-tune CNN. The CNN model is widely deployed on IoT devices for application due to its advantages in comprehensive resource occupancy and performance. Moreover, IoT devices are widely deployed outdoors and usually process data affected by the environment (such as fog, snow, rain, etc.). The goal of this paper is to use LoRA technology to efficiently improve the robustness of the CNN model. To this end, this paper first proposes a strong, robust CNN fine-tuning method for IoT devices, LoRA-C, which performs low-rank decomposition in convolutional layers rather than kernel units to reduce the number of fine-tuning parameters. Then, this paper analyzes two different rank settings in detail and observes that the best performance is usually achieved when $α/{r}$ is a constant in either standard data or corrupted data. This discovery provides experience for the widespread application of LoRA-C. Finally, this paper conducts many experiments based on pre-trained models. Experimental results on CIFAR-10, CIFAR-100, CIFAR-10-C, and Icons50 datasets show that the proposed LoRA-Cs outperforms standard ResNets. Specifically, on the CIFAR-10-C dataset, the accuracy of LoRA-C-ResNet-101 achieves 83.44% accuracy, surpassing the standard ResNet-101 result by +9.5%.
