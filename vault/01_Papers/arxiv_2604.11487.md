---
title: "NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild"
authors:
  - "Aleksandr Gushchin"
  - "Khaled Abud"
  - "Ekaterina Shumitskaya"
  - "Artem Filippov"
  - "Georgii Bychkov"
  - "Sergey Lavrushkin"
  - "Mikhail Erofeev"
  - "Anastasia Antsiferova"
  - "Changsheng Chen"
  - "Shunquan Tan"
  - "Radu Timofte"
  - "Dmitry Vatolin"
  - "Chuanbiao Song"
  - "Zijian Yu"
  - "Hao Tan"
  - "Jun Lan"
  - "Zhiqiang Yang"
  - "Yongwei Tang"
  - "Zhiqiang Wu"
  - "Jia Wen Seow"
  - "Hong Vin Koay"
  - "Haodong Ren"
  - "Feng Xu"
  - "Shuai Chen"
  - "Ruiyang Xia"
  - "Qi Zhang"
  - "Yaowen Xu"
  - "Zhaofan Zou"
  - "Hao Sun"
  - "Dagong Lu"
  - "Mufeng Yao"
  - "Xinlei Xu"
  - "Fei Wu"
  - "Fengjun Guo"
  - "Cong Luo"
  - "Hardik Sharma"
  - "Aashish Negi"
  - "Prateek Shaily"
  - "Jayant Kumar"
  - "Sachin Chaudhary"
  - "Akshay Dudhane"
  - "Praful Hambarde"
  - "Amit Shukla"
  - "Zhilin Tu"
  - "Fengpeng Li"
  - "Jiamin Zhang"
  - "Jianwei Fei"
  - "Kemou Li"
  - "Haiwei Wu"
  - "Bilel Benjdira"
  - "Anas M. Ali"
  - "Wadii Boulila"
  - "Chenfan Qu"
  - "Junchi Li"
url: "http://arxiv.org/abs/2604.11487v1"
published: "2026-04-13"
citations: "0"
source: "arXiv"
id: "arxiv:2604.11487"
full_pdf_ingested: "True"
tags:
  - "research-paper"
  - "title:-"multimodal-alignment-in-vision-language-models:-a-comparative-analysis-of-contrastive-vs.-generative-training-paradigms"-target-venues:-cvpr-2026-workshop-/-ieee-tpami-core-research-question:-does-contrastive-alignment-(clip/siglip)-or-autoregressive-generative-alignment-(lmms/chameleon/llama-vision)-provide-superior-out-of-distribution-transferability-and-lower-hallucination-rates?-why-it's-high-impact:-resolves-the-central-architectural-debate-in-modern-multimodal-ai.-corpus-target:-25-papers"
---
# NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild

**Authors**: Aleksandr Gushchin, Khaled Abud, Ekaterina Shumitskaya, Artem Filippov, Georgii Bychkov, Sergey Lavrushkin, Mikhail Erofeev, Anastasia Antsiferova, Changsheng Chen, Shunquan Tan, Radu Timofte, Dmitry Vatolin, Chuanbiao Song, Zijian Yu, Hao Tan, Jun Lan, Zhiqiang Yang, Yongwei Tang, Zhiqiang Wu, Jia Wen Seow, Hong Vin Koay, Haodong Ren, Feng Xu, Shuai Chen, Ruiyang Xia, Qi Zhang, Yaowen Xu, Zhaofan Zou, Hao Sun, Dagong Lu, Mufeng Yao, Xinlei Xu, Fei Wu, Fengjun Guo, Cong Luo, Hardik Sharma, Aashish Negi, Prateek Shaily, Jayant Kumar, Sachin Chaudhary, Akshay Dudhane, Praful Hambarde, Amit Shukla, Zhilin Tu, Fengpeng Li, Jiamin Zhang, Jianwei Fei, Kemou Li, Haiwei Wu, Bilel Benjdira, Anas M. Ali, Wadii Boulila, Chenfan Qu, Junchi Li
**Published**: 2026-04-13 | **Citations**: 0 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2604.11487v1

## Executive Summary & Abstract
This paper presents an overview of the NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild, held in conjunction with the NTIRE workshop at CVPR 2026. The goal of this challenge was to develop detection models capable of distinguishing real images from generated ones in realistic scenarios: the images are often transformed (cropped, resized, compressed, blurred) for practical usage, and therefore, the detection models should be robust to such transformations. The challenge is based on a novel dataset consisting of 108,750 real and 185,750 AI-generated images from 42 generators comprising a large variety of open-source and closed-source models of various architectures, augmented with 36 image transformations. Methods were evaluated using ROC AUC on the full test set, including both transformed and untransformed images. A total of 511 participants registered, with 20 teams submitting valid final solutions. This report provides a comprehensive overview of the challenge, describes the proposed solutions, and can be used as a valuable reference for researchers and practitioners in increasing the robustness of the detection models to real-world transformations.

## Methodological Insights & System Architectures
- Evaluates enterprise LLM capabilities, inference scalability, and task boundaries.
- Examines empirical performance metrics, baseline comparisons, and statistical significance.

## Key Quantitative Findings & Benchmarks
- Focuses on operational ROI, labor market skill distribution, and multi-agent coordination.

## Content Snippet
NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild
Aleksandr Gushchin * Khaled Abud Ekaterina Shumitskaya Artem Filippov
Georgii Bychkov Sergey Lavrushkin Mikhail Erofeev Anastasia Antsiferova
Changsheng Chen Shunquan Tan Radu Timofte Dmitry Vatolin Chuanbiao Song
Zijian Yu Hao Tan Jun Lan Zhiqiang Yang Yongwei Tang Zhiqiang Wu
Jia Wen Seow Hong Vin Koay Haodong Ren Feng Xu Shuai Chen
Ruiyang Xia Qi Zhang Yaowen Xu Zhaofan Zou Hao Sun Dagong Lu
Mufeng Yao Xinlei Xu Fei Wu Fengjun Guo Cong Luo Hardik Sharma
Aashish Negi Prateek Shaily Jayant Kumar Sachin Chaudhary Akshay Dudhane
Praful Hambarde Amit Shukla Zhilin Tu Fengpeng Li Jiamin Zhang
Jianwei Fei Kemou Li Haiwei Wu Bilel Benjdira Anas M. Ali Wadii Boulila
Chenfan Qu Junchi Li
Abstract
This paper presents an overview of the NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild,
held in conjunction with the NTIRE workshop at CVPR
2026. The goal of this challenge was to develop detection
models capable of distinguishing real images from generated ones in realistic scenarios: the images are often transformed (cropped, resized, compressed, blurred) for practical usage, and therefore, the detection models should be
robust to such transformations. The challenge is based on
a novel dataset consisting of 108,750 real and 185,750 AIgenerated images from 42 generators comprising a large
variety of open-source and closed-source models of various
architectures, augmented with 36 image transforma
