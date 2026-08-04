---
type: reference
aliases: []
tags:
  - literature
  - research
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
authors: "Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao"
year: 2023
journal: ""
doi: ""
read: false
related: []
---

# ReAct: Synergizing Reasoning and Acting in Language Models

> **Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
> **Year:** 2023
> **Journal:** 
> **Links:** [Full Text PDF](zotero://select/library/items/TVY7QT6P) | [DOI](https://doi.org/)

---


## 📝 Abstract

> While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. Project site with code: https://react-lm.github.io


## 🎯 TL;DR / Core Claim
The authors introduce ReAct, a paradigm that allows large language models to seamlessly interleave verbal reasoning (chain-of-thought) with task-specific actions (tool use/environment interaction). For this thesis, ReAct is the foundational execution loop that transforms static LLMs into autonomous scientific agents capable of iterative experimentation, observation, and strategy revision.

## 🧠 Synthesis & Thoughts
This paper establishes the baseline architecture for modern agentic systems. In the context of Chapter 2.4 (_From Static Pipelines to Agentic Science_), ReAct represents the critical bridge between a traditional, human-specified computational pipeline and an autonomous, goal-directed researcher. By allowing the model to gather real-world feedback (e.g., using a Wikipedia API, or in our case, computational biology tools) before its next reasoning step, ReAct directly mitigates hallucinations and flawed assumptions. However, as noted by more recent frameworks (like Mimosa), a single ReAct loop has limitations over long scientific horizons due to context window saturation, meaning ReAct serves best as the "micro-engine" within a larger, multi-agent macro-architecture.

- **Relevance**:: Chapter 2.4 From Static Pipelines to Agentic Science
- **Methodology**:: 
- **Key Findings**::  



---

### Notes
- This is essentially the "origin story" of the modern AI agent.

- The core takeaway is the synergistic loop: _Reasoning_ helps the model induce and update plans, while _Acting_ allows it to pull in factual, external data to ground that reasoning