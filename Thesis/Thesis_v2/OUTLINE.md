# Thesis — Master Outline & Writing Tracker

**Title:** *Mimosa: A Reliable, Tool-Augmented LLM Agent for Reproducible DNA-Methylation Analysis — a Validated Foundation for Multi-Omics*

> **Format:** Markdown-first (Pandoc → LaTeX for UniBO formatting).
> Each experiment chapter is self-contained and can be added, removed, or reordered without breaking other chapters.

## Style Guide

- **Register:** Formal academic English. Third person or first-person plural ("we").
- **No draft notes** in the body text. Keep TODOs as `<!-- TODO: ... -->` HTML comments only.
- **No conversational asides.** Every sentence earns its place.
- **Passive voice** where the actor is unimportant; active voice where agency matters.
- **Signposting** via topic sentences at paragraph starts, not meta-commentary ("This section will discuss...").
- **Citations:** `[@key]` Pandoc format. Every factual claim backed by a source.
- **Tables and figures:** numbered per chapter (Table 4.1, Fig. 3.2). Captions are complete sentences.
- **Numbers:** spell out below ten except in technical contexts (3 samples, 6 coverage files).

## Hypothesis

> **H:** A tool-augmented large language model agent, constrained by a domain-specific skill and
> typed Model Context Protocol tool servers, can autonomously execute whole-genome bisulfite
> sequencing differential methylation analyses — replicating published findings across organisms
> and executing the complete reads-to-results pipeline — with results concordant with
> expert-conducted analyses.

The hypothesis is tested by three experiments, each addressing a distinct facet:

| Experiment | Dataset | Facet tested |
|---|---|---|
| 1 | GSE263850 (human *AKAP11* KO) | Concordance with published results and an expert re-analysis |
| 2 | GSE214232 (mouse *Dnmt3a* KO) | Cross-species generalisation of the same concordance |
| 3 | Simulated FASTQ files | Full-pipeline capability: raw reads → coverage → DMRs |

---

## Chapter Map

| # | File | Chapter | Depends on | Status |
|---|------|---------|-----------|--------|
| 1 | `01_introduction.md` | Introduction | whole thesis | ⬜ rewrite |
| 2 | `02_background.md` | Background & Related Work | literature | ⬜ rewrite |
| 3 | `03_system_design_and_methods.md` | System Design & Methods | built work | ⬜ rewrite |
| 4 | `04_experiment1_gse263850.md` | Experiment 1: Replication — GSE263850 | run23 data | ⬜ rewrite |
| 5 | `05_experiment2_gse214232.md` | Experiment 2: Replication — GSE214232 | experiment | ⛏️ skeleton |
| 6 | `06_experiment3_simulated_fastq.md` | Experiment 3: End-to-End — Simulated FASTQ | experiment | ⬜ skeleton |
| 7 | `07_discussion.md` | Discussion | Ch.4–6 | ⬜ skeleton |
| 8 | `08_conclusions.md` | Conclusions & Future Work | Ch.7 | ⬜ skeleton |
| — | `09_bibliography.md` | Bibliography | — | ✍️ carry forward |
| — | `10_annexes.md` | Annexes | — | ⬜ skeleton |

**Modularity rule:** Each experiment chapter (4, 5, 6) follows an identical internal structure:
1. Dataset & biological context
2. Experimental design (arms, parameters)
3. Results
4. Analysis & identified defects
5. Chapter summary

This makes it trivial to insert Experiment N+1 or remove one without touching other chapters.

---

## Chapter 1 — Introduction

Follows the eight UniBO-required elements. Each maps to a subsection:

- **§1.1 Object** — the reliability of Mimosa applied to WGBS methylation analysis.
- **§1.2 Tasks** — three tasks mapping to the three experiments.
- **§1.3 Hypothesis** — single hypothesis (see above).
- **§1.4 Actuality** — timeliness: LLM agents in science, MCP standardisation, the trust gap.
- **§1.5 Research methodology** — system-plus-validation: specify apparatus (Ch.3), then measure (Ch.4–6).
- **§1.6 Sources** — public GEO data, methodological literature, system source code, agent/MCP literature.
- **§1.7 Structure** — chapter-by-chapter summary.
- **§1.8 New approach** — measurement against knowable truth instead of capability demonstrations.

## Chapter 2 — Background & Related Work

- **§2.1** DNA methylation & WGBS — 5mC, CpG, bisulfite conversion, coverage data model.
- **§2.2** Reads → coverage — Bismark, Nextflow, nf-core/methylseq.
- **§2.3** DMCs/DMRs & two engines — methylKit vs. DSS statistics.
- **§2.4** LLM agents, tool use & MCP — ReAct, tool-augmented LLMs, MCP protocol.
- **§2.5** Agents for science & the reliability problem — prior work, capability ≠ reliability.
- **§2.6** Gap statement — ties the two literatures to the hypothesis.

## Chapter 3 — System Design & Methods

- **§3.1** Architecture overview — four layers, data flow, design principles.
- **§3.2** MCP Server A — Nextflow / nf-core/methylseq runner (FASTQ → `.cov`).
- **§3.3** MCP Server B — Dockerised R methylKit/DSS runner (execute-only surface).
- **§3.4** The methylation skill — engine selection, QC defaults, domain knowledge encoding.
- **§3.5** The Mimosa agent — framework, QD evolution, multi-source verifier, goal evolution.
- **§3.6** Reliability engineering — sign canonicalisation, post-hoc assertions, instrumentation.
- **§3.7** Toolomics ecosystem — Perspicacité, Indicium, the multi-omics bridge.

## Chapter 4 — Experiment 1: Replication of the GSE263850 AKAP11 Study

Self-contained. All Study A content from old Ch.4, rewritten.

## Chapter 5 — Experiment 2: Replication of the GSE214232 Dnmt3a Study

Self-contained. Skeleton awaiting experimental results.

## Chapter 6 — Experiment 3: End-to-End with Simulated FASTQ

Self-contained. Tests full pipeline (Server A + Server B) from simulated raw reads.

## Chapter 7 — Discussion

Cross-experiment synthesis, strengths, limitations, threats to validity.

## Chapter 8 — Conclusions & Future Work

Contributions, honest scope boundary, multi-omics extension roadmap.
