# Thesis — Master Outline & Writing Tracker

**Working title:** *Mimosa: A Reliable, Tool-Augmented LLM Agent for Reproducible DNA-Methylation Analysis — a Validated Foundation for Multi-Omics*

> Source of truth for scope/decisions/timeline: `../THESIS_PLAN.md`.
> This file is the **writing map**: what each chapter contains, what's drafted, and what's blocked on experiments.
> Format: **Markdown-first** (write content here), Pandoc → LaTeX for UniBO formatting in W10 (late Aug).

## Status legend
- ✅ drafted (v1)  · ✍️ in progress  · ⛏️ blocked on an experiment  · ⬜ not started

---

## Chapter map

| # | File | Chapter | Depends on | Status |
|---|------|---------|-----------|--------|
| 1 | `01_introduction.md` | Introduction (8 UniBO sub-elements) | whole thesis | ✅ v1 — §§1.1–1.8 name the 8 UniBO elements explicitly; result-verdict wording to finalize post-experiment |
| 2 | `02_background.md` | Background & Related Work | literature pass | ✅ v1 — §§2.0–2.6 drafted; ⚠ citations need a verification pass (esp. §2.4–2.5) |
| 3 | `03_system_design_and_methods.md` | **System Design & Methods** | **nothing — built work** | ✅ v1 — §§3.0–3.7 drafted (figures pending) |
| 4 | `04_validation1_replication.md` | Validation I — Replication (Study A human, Study B mouse) | Studies A/B results | ✍️ v1 — Study A (GSE263850) drafted from run23; Study B placeholdered; §4.3–4.4 await Study B |
| 5 | `05_validation2_synthetic_reliability.md` | Validation II — Synthetic (Study C) & Reliability (Study D) | Studies C/D results | ⛏️ |
| 6 | `06_discussion.md` | Discussion | Ch.4–5 | ⛏️ |
| 7 | `07_conclusions_future_work.md` | Conclusions & Future Work (multi-omics bridge) | Ch.6 | ⬜ |
| 8 | `08_bibliography.md` | Bibliography (BibTeX seed) | — | ✍️ seeded — ~28 working entries, **all marked STATUS: confident/VERIFY** (none final) |
| 9 | `09_annexes.md` | Annexes (skill, MCP tool tables, transcripts, env manifest) | — | ⬜ |

**Why Chapter 3 first:** it documents work that already exists (the two MCP servers, the
skill, the Mimosa agent) and needs zero experimental results. It is also the body of the
first UniBO progress report due this week. Everything else has a dependency; this does not.

---

## Chapter 3 — section plan (DRAFT v1 COMPLETE)

- **3.0** Chapter intro — what the system is, what this chapter claims/defers. ✅
- **3.1** Architecture overview — the four layers, end-to-end data flow, design principles. ✅ (revised: *agent* = self-evolving framework; Server B box = execute-only)
- **3.2** MCP Server A — Nextflow / nf-core/methylseq runner (FASTQ → `.cov`). ✅
- **3.3** MCP Server B — Dockerized R methylKit/DSS runner. ✅ (revised: **execute-only (2 tools) is the production surface**; the 4+14 atomic-tool design is a retained variant = the Ch.5 constrained ablation arm)
- **3.4** The skill as router & guardrail — engine selection, QC defaults, gotchas. ✅
- **3.5** The Mimosa agent — framework (5 layers, QD evolution, 6-source verifier, multi-model config), goal evolution (v1→v6), workspace contract, audit trail. ✅
- **3.6** Reliability guardrails — run10/11/12 same-input divergence + run11 silent failure; F1 polarity (KO−WT) canonicalisation; F2 silent-failure assertions; trace/param-vector/peak-RSS instrumentation. ✅
- **3.7** Situating Mimosa in the Toolomics ecosystem (brief) — Perspicacité (verifier Source A; Deniz's two fixes); Indicium claim-standardisation adapters (the multi-omics bridge); ASB one line. ✅

Open items for Ch.3:
- **Attribution to confirm with Deniz/supervisor:** Mimosa is the lab's framework (Legrand et al., 2026); be explicit about which methylation-specific pieces (skill, goal evolution, Toolomics methylation server, reliability instrumentation) are Deniz's own contribution. Draft currently attributes Mimosa to the lab and frames the methylation vertical + reliability work as the thesis contribution.
- Figures still to produce.

Figures/tables to produce for this chapter (placeholders in text + `figures/`):
- Fig 3.1 — flagship architecture diagram (greyed-out future multi-omics modules).
- Fig 3.2 — nf-core/methylseq pipeline DAG.
- Fig 3.3 — atomic-tool `.rds` state-flow diagram.
- Fig 3.4 — Mimosa five-layer / evolution-loop figure (goal → synth → sandbox → 6-source verifier → QD archive).
- Fig 3.5 — boxed `run11` report excerpt (5 retried QC failures + "22 tiles → 1816 DMRs"), beside clean `run10`.
- Tab 3.1 — MCP tool catalogue (Server A: 8 tools; Server B: 2 execute-only / 4+14 atomic variant).
- Tab 3.2 — skill engine-selection decision table.
- Tab 3.3 — goal-evolution changelog (v1→v6).

---

## Chapter 2 — section plan (DRAFT v1 COMPLETE)

- **2.0** Chapter intro — two literatures (settled methods + young agents); the seam this thesis works. ✅
- **2.1** DNA methylation & WGBS — 5mC/CpG biology, bisulfite conversion, the count/coverage data model. ✅
- **2.2** Reads → coverage — Bismark, Nextflow, nf-core/methylseq; reproducibility lives upstream. ✅
- **2.3** DMCs/DMRs & two engines — units, overdispersion/FDR, methylKit vs DSS trade-off. ✅
- **2.4** LLM agents, tool use & MCP — ReAct/Toolformer, the agent loop, MCP, skills. ✅
- **2.5** Agents for science & the reliability problem — Coscientist/ChemCrow/AI-Scientist; capability ≠ reliability; benchmarks. ✅
- **2.6** Gap statement → ties to the Ch.1 hypothesis (reproduce / control FP / reproducible). ✅

**⚠ Ch.2 open item — CITATION VERIFICATION PASS (do before any submission):** the bib seed in
`08_bibliography.md` is drafted from working knowledge, not checked. §2.1–2.3 are landmark papers
(verify vol/pages/DOI). **§2.4–2.5 are the knowledge-cutoff-sensitive ones** (MCP spec, Coscientist,
ChemCrow, AI-Scientist, ScienceAgentBench, PaperBench, Mimosa arXiv id) — confirm each exists and get
the canonical citation via web search / a reference manager. Best done with the `deep-research` skill
or a targeted web pass.
