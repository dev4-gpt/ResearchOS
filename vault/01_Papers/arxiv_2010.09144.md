---
title: "Using mutation testing to measure behavioural test diversity"
authors:
  - "Francisco Gomes de Oliveira Neto"
  - "Felix Dobslaw"
  - "Robert Feldt"
url: "http://arxiv.org/abs/2010.09144v1"
published: "2020-10-19"
citations: "0"
source: "arXiv"
id: "arxiv:2010.09144"
full_pdf_ingested: "False"
tags:
  - "research-paper"
  - "autonomous-code-synthesis-and-self-healing-multi-agent-systems"
---
# Using mutation testing to measure behavioural test diversity

**Authors**: Francisco Gomes de Oliveira Neto, Felix Dobslaw, Robert Feldt
**Published**: 2020-10-19 | **Source**: arXiv
**URL**: http://arxiv.org/abs/2010.09144v1

## Abstract
Diversity has been proposed as a key criterion to improve testing effectiveness and efficiency.It can be used to optimise large test repositories but also to visualise test maintenance issues and raise practitioners' awareness about waste in test artefacts and processes. Even though these diversity-based testing techniques aim to exercise diverse behavior in the system under test (SUT), the diversity has mainly been measured on and between artefacts (e.g., inputs, outputs or test scripts). Here, we introduce a family of measures to capture behavioural diversity (b-div) of test cases by comparing their executions and failure outcomes. Using failure information to capture the SUT behaviour has been shown to improve effectiveness of history-based test prioritisation approaches. However, history-based techniques require reliable test execution logs which are often not available or can be difficult to obtain due to flaky tests, scarcity of test executions, etc. To be generally applicable we instead propose to use mutation testing to measure behavioral diversity by running the set of test cases on various mutated versions of the SUT. Concretely, we propose two specific b-div measures (based on accuracy and Matthew's correlation coefficient, respectively) and compare them with artefact-based diversity (a-div) for prioritising the test suites of 6 different open-source projects. Our results show that our b-div measures outperform a-div and random selection in all of the studied projects. The improvement is substantial with an average increase in average percentage of faults detected (APFD) of between 19% to 31% depending on the size of the subset of prioritised tests.
