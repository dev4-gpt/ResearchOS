---
title: "Improving Code Summarization with Block-wise Abstract Syntax Tree Splitting"
authors:
  - "Chen Lin"
  - "Zhichao Ouyang"
  - "Junqing Zhuang"
  - "Jianqiang Chen"
  - "Hui Li"
  - "Rongxin Wu"
url: "http://arxiv.org/abs/2103.07845v2"
published: "2021-03-14"
citations: "0"
source: "arXiv"
id: "arxiv:2103.07845"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Improving Code Summarization with Block-wise Abstract Syntax Tree Splitting

**Authors**: Chen Lin, Zhichao Ouyang, Junqing Zhuang, Jianqiang Chen, Hui Li, Rongxin Wu
**Published**: 2021-03-14 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2103.07845v2

## Abstract
Automatic code summarization frees software developers from the heavy burden of manual commenting and benefits software development and maintenance. Abstract Syntax Tree (AST), which depicts the source code's syntactic structure, has been incorporated to guide the generation of code summaries. However, existing AST based methods suffer from the difficulty of training and generate inadequate code summaries. In this paper, we present the Block-wise Abstract Syntax Tree Splitting method (BASTS for short), which fully utilizes the rich tree-form syntax structure in ASTs, for improving code summarization. BASTS splits the code of a method based on the blocks in the dominator tree of the Control Flow Graph, and generates a split AST for each code split. Each split AST is then modeled by a Tree-LSTM using a pre-training strategy to capture local non-linear syntax encoding. The learned syntax encoding is combined with code encoding, and fed into Transformer to generate high-quality code summaries. Comprehensive experiments on benchmarks have demonstrated that BASTS significantly outperforms state-of-the-art approaches in terms of various evaluation metrics. To facilitate reproducibility, our implementation is available at https://github.com/XMUDM/BASTS.
