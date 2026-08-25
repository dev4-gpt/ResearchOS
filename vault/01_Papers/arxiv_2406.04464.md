---
title: "On The Importance of Reasoning for Context Retrieval in Repository-Level Code Editing"
authors:
  - "Alexander Kovrigin"
  - "Aleksandra Eliseeva"
  - "Yaroslav Zharov"
  - "Timofey Bryksin"
url: "http://arxiv.org/abs/2406.04464v1"
published: "2024-06-06"
citations: "0"
source: "arXiv"
id: "arxiv:2406.04464"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "review-symbol-graph-rag-vs-qlora-swe-bench-lite"
---
# On The Importance of Reasoning for Context Retrieval in Repository-Level Code Editing

**Authors**: Alexander Kovrigin, Aleksandra Eliseeva, Yaroslav Zharov, Timofey Bryksin
**Published**: 2024-06-06 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2406.04464v1

## Abstract
Recent advancements in code-fluent Large Language Models (LLMs) enabled the research on repository-level code editing. In such tasks, the model navigates and modifies the entire codebase of a project according to request. Hence, such tasks require efficient context retrieval, i.e., navigating vast codebases to gather relevant context. Despite the recognized importance of context retrieval, existing studies tend to approach repository-level coding tasks in an end-to-end manner, rendering the impact of individual components within these complicated systems unclear. In this work, we decouple the task of context retrieval from the other components of the repository-level code editing pipelines. We lay the groundwork to define the strengths and weaknesses of this component and the role that reasoning plays in it by conducting experiments that focus solely on context retrieval. We conclude that while the reasoning helps to improve the precision of the gathered context, it still lacks the ability to identify its sufficiency. We also outline the ultimate role of the specialized tools in the process of context gathering. The code supplementing this paper is available at https://github.com/JetBrains-Research/ai-agents-code-editing.
