---
title: "Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding"
authors:
  - "Hang Zhang"
  - "Xin Li"
  - "Lidong Bing"
url: "https://doi.org/10.18653/v1/2023.emnlp-demo.49"
published: "2023"
citations: "515"
source: "Crossref"
id: "10.18653/v1/2023.emnlp-demo.49"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-spatio-temporal-grounding-in-video-question-answering"
---
# Video-LLaMA: An Instruction-tuned Audio-Visual Language Model for Video Understanding

**Authors**: Hang Zhang, Xin Li, Lidong Bing
**Published**: 2023 | **Source**: Crossref
**URL**: https://doi.org/10.18653/v1/2023.emnlp-demo.49

## Abstract
We present Video-LLaMA 1 a multi-modal framework that empowers Large Language Models (LLMs) with the capability of understanding both visual and auditory content in the video. Video-LLaMA bootstraps cross-modal training from the frozen pre-trained visual & audio encoders and the frozen LLMs. Unlike previous works that complement LLMs to process the visual or audio signals only To counter the first challenge, we propose a Video Q-former to assemble a pre-trained image encoder into our video encoder and introduce a video-to-text generation task to learn video-language correspondence. For the second challenge, we leverage ImageBind To align the output of both visual & audio encoders with LLM's embedding space, we first train Video-LLaMA on massive video/image-caption pairs and then tune our model with visual-instruction datasets of moderate amount but higher quality. We found Video-LLaMA shows the ability to perceive and comprehend video content and generate meaningful responses grounded in the visual and auditory information presented in the videos.
