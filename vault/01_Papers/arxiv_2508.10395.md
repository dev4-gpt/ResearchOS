---
title: "XQuant: Breaking the Memory Wall for LLM Inference with KV Cache Rematerialization"
authors:
  - "Aditya Tomar"
  - "Coleman Hooper"
  - "Minjae Lee"
  - "Haocheng Xi"
  - "Rishabh Tiwari"
  - "Wonjun Kang"
  - "Luca Manolache"
  - "Michael W. Mahoney"
  - "Kurt Keutzer"
  - "Amir Gholami"
url: "http://arxiv.org/abs/2508.10395v1"
published: "2025-08-14"
citations: "0"
source: "arXiv"
id: "arxiv:2508.10395"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-architectural-dynamics-long-12-page"
---
# XQuant: Breaking the Memory Wall for LLM Inference with KV Cache Rematerialization

**Authors**: Aditya Tomar, Coleman Hooper, Minjae Lee, Haocheng Xi, Rishabh Tiwari, Wonjun Kang, Luca Manolache, Michael W. Mahoney, Kurt Keutzer, Amir Gholami
**Published**: 2025-08-14 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2508.10395v1

## Abstract
Although LLM inference has emerged as a critical workload for many downstream applications, efficiently inferring LLMs is challenging due to the substantial memory footprint and bandwidth requirements. In parallel, compute capabilities have steadily outpaced both memory capacity and bandwidth over the last few decades, a trend that remains evident in modern GPU hardware and exacerbates the challenge of LLM inference. As such, new algorithms are emerging that trade increased computation for reduced memory operations. To that end, we present XQuant, which takes advantage of this trend, enabling an order-of-magnitude reduction in memory consumption through low-bit quantization with substantial accuracy benefits relative to state-of-the-art KV cache quantization methods. We accomplish this by quantizing and caching the layer input activations X, instead of using standard KV caching, and then rematerializing the Keys and Values on-the-fly during inference. This results in an immediate 2$\times$ memory savings compared to KV caching. By applying XQuant, we achieve up to $\sim 7.7\times$ memory savings with $<0.1$ perplexity degradation compared to the FP16 baseline. Furthermore, our approach leverages the fact that X values are similar across layers. Building on this observation, we introduce XQuant-CL, which exploits the cross-layer similarity in the X embeddings for extreme compression. Across different models, XQuant-CL attains up to 10$\times$ memory savings relative to the FP16 baseline with only 0.01 perplexity degradation, and 12.5$\times$ memory savings with only $0.1$ perplexity degradation. XQuant exploits the rapidly increasing compute capabilities of hardware platforms to eliminate the memory bottleneck, while surpassing state-of-the-art KV cache quantization methods and achieving near-FP16 accuracy across a wide range of models.
