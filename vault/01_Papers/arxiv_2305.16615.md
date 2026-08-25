---
title: "AIBugHunter: A Practical Tool for Predicting, Classifying and Repairing Software Vulnerabilities"
authors:
  - "Michael Fu"
  - "Chakkrit Tantithamthavorn"
  - "Trung Le"
  - "Yuki Kume"
  - "Van Nguyen"
  - "Dinh Phung"
  - "John Grundy"
url: "http://arxiv.org/abs/2305.16615v1"
published: "2023-05-26"
citations: "0"
source: "arXiv"
id: "arxiv:2305.16615"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# AIBugHunter: A Practical Tool for Predicting, Classifying and Repairing Software Vulnerabilities

**Authors**: Michael Fu, Chakkrit Tantithamthavorn, Trung Le, Yuki Kume, Van Nguyen, Dinh Phung, John Grundy
**Published**: 2023-05-26 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2305.16615v1

## Abstract
Many ML-based approaches have been proposed to automatically detect, localize, and repair software vulnerabilities. While ML-based methods are more effective than program analysis-based vulnerability analysis tools, few have been integrated into modern IDEs, hindering practical adoption. To bridge this critical gap, we propose AIBugHunter, a novel ML-based software vulnerability analysis tool for C/C++ languages that is integrated into Visual Studio Code. AIBugHunter helps software developers to achieve real-time vulnerability detection, explanation, and repairs during programming. In particular, AIBugHunter scans through developers' source code to (1) locate vulnerabilities, (2) identify vulnerability types, (3) estimate vulnerability severity, and (4) suggest vulnerability repairs. In this article, we propose a novel multi-objective optimization (MOO)-based vulnerability classification approach and a transformer-based estimation approach to help AIBugHunter accurately identify vulnerability types and estimate severity. Our empirical experiments on a large dataset consisting of 188K+ C/C++ functions confirm that our proposed approaches are more accurate than other state-of-the-art baseline methods for vulnerability classification and estimation. Furthermore, we conduct qualitative evaluations including a survey study and a user study to obtain software practitioners' perceptions of our AIBugHunter tool and assess the impact that AIBugHunter may have on developers' productivity in security aspects. Our survey study shows that our AIBugHunter is perceived as useful where 90% of the participants consider adopting our AIBugHunter. Last but not least, our user study shows that our AIBugHunter could possibly enhance developers' productivity in combating cybersecurity issues during software development.
