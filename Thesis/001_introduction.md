# Chapter 1 — Introduction

This thesis asks whether an artificial-intelligence agent can be trusted to perform a real piece of epigenomics. Large language models have made it possible to direct software to carry out an analysis in plain language, and to have it write and execute the code itself; the open question — the one that determines whether such systems belong anywhere near science — is not whether they can occasionally produce a correct answer, but whether they produce it reliably: concordantly with established findings, consistently across organisms and experimental designs, and with their errors visible rather than concealed behind fluent prose. The work that follows takes a single, well-understood analytical domain — differential DNA-methylation analysis from whole-genome bisulfite sequencing (WGBS) — and uses it as a proving ground on which that question can be given numbers instead of adjectives.z

## 1.1 Object

The object of this thesis is the reliability of a tool-augmented large language model (LLM) agent applied to WGBS differential methylation analysis. The specific system under study is Mimosa, a self-evolving multi-agent framework developed in the host laboratory (Université Côte d'Azur, Holobiomics / MetaboLinkAI) and described by [@legrand2026], operating through the laboratory's Toolomics infrastructure of Model Context Protocol (MCP) tool servers. Given WGBS data and a natural-language goal, the system synthesises and executes a complete differential-methylation pipeline — quality control, differential testing, region calling, annotation, and interpretation — by writing analysis code and invoking domain tools rather than by following a fixed script.

<mark style="background: #FF5582A6;">The thesis does not introduce Mimosa; it adopts the framework as the apparatus under test and provides its first rigorously validated application to a biological domain. The work is, deliberately, a refocusing of a broader registered project. The internship from which it arises was registered under a clinical multi-omics title; the thesis delivers and validates the methylation vertical of that vision in depth, and frames it as the validated foundation from which a multi-omics system — transcriptomics, then metabolomics — can be extended, rather than claiming the full integration that remains future work.</mark>

## 1.2 Tasks

To make the object tractable, the thesis pursues three principal tasks, each corresponding to an experiment:

1. **Specify the system under test** precisely enough that its behaviour can be measured — its architecture, its two MCP tool servers, its domain skill, its agent loop and goal specification, and its reliability guardrails (Chapter 3).
2. **Replicate published WGBS findings** by driving the agent, and matched expert-run baselines, over the identical data of two peer-reviewed studies — a human AKAP11 knockout study (GSE263850) and a mouse Dnmt3a conditional knockout study (GSE214232) — and scoring concordance as a triangle: agent versus published results, agent versus expert re-analysis, and expert versus published (Chapters 4 and 5).
3. **Demonstrate full-pipeline capability** from simulated FASTQ files through bisulfite alignment to differentially methylated region (DMR) calling, exercising the complete reads-to-results path that the real-data experiments, by necessity, begin downstream of alignment (Chapter 6).

## 1.3 Hypothesis

The thesis tests a single hypothesis:

> A tool-augmented large language multi-model agent, constrained by a domain-specific skill and typed Model Context Protocol tool servers, can autonomously execute whole-genome bisulfite sequencing differential methylation analyses — replicating published findings across organisms and executing the complete reads-to-results pipeline — with results concordant with expert-conducted analyses.

The hypothesis is falsifiable. Each experiment produces quantitative concordance or capability measures that either support it or do not. A negative or qualified result — for example, that reliability requires the domain skill and bounded autonomy, or that concordance is adequate for gene-level findings but not for individual CpG sites — would itself be a scientifically informative outcome, not a failure of the thesis.

## 1.4 Actuality

The timeliness of the question is sharp. Tool-using LLM agents have, within a very short span, moved from research demonstrations to systems that conduct chemical and computational research with minimal human intervention [@boiko2023; @bran2024]. The recent standardisation of agent–tool interfaces through the Model Context Protocol [@anthropic2024mcp] has made it routine to connect an agent to real scientific software, and the attraction for biology and medicine is immediate: methylation and other omics analyses demand specialised statistical and computational expertise that most clinicians and many researchers lack, and a conversational agent promises to make that analysis accessible through ordinary language.

The same properties that make these systems attractive, however, make them dangerous in a scientific setting. LLM agents are non-deterministic; they fail in fluent and confident ways; and they can report success on results that do not survive inspection. For a clinically-adjacent assay such as WGBS methylation — where a hyper- or hypo-methylated region may be read as a candidate biomarker or a diagnostic indicator — a plausible wrong answer is worse than an obvious one. The decisive quantities a practitioner would need before trusting such a tool — concordance with published findings, cross-species consistency, and full-pipeline capability from raw sequencing reads — have not, to our knowledge, been reported for an LLM agent performing methylation analysis. Supplying those quantities, in a domain whose correct answers are knowable, is the timely contribution this thesis makes.

## 1.5 Research methodology

The research methodology is a system-plus-validation design in which an engineered artefact and an empirical evaluation of it carry equal weight. The system is specified as a fully described apparatus (Chapter 3); its behaviour is then measured by three experiments that address the hypothesis from complementary angles.

**Experiments 1 and 2** are real-data replications. In Experiment 1, the agent analyses the human AKAP11 knockout WGBS dataset GSE263850; in Experiment 2, it analyses the mouse Dnmt3a conditional knockout dataset GSE214232. Each experiment is scored as a triangle: the agent's results are compared with the published findings, the agent's results are compared with an expert re-analysis conducted independently on the same data, and the expert re-analysis is compared with the published findings to establish a realistic ceiling for concordance. This triangulated design prevents the evaluation from depending on a single, possibly idiosyncratic, reference point. Concordance is assessed on gene recovery, direction of effect, and qualitative methylation signature rather than on raw count identity, since several defensible statistical methods yield legitimately different counts.

**Experiment 3** is an end-to-end pipeline demonstration. Simulated FASTQ files with known properties are processed by the agent through the complete reads-to-results path — bisulfite alignment via nf-core/methylseq, coverage extraction, and DMR calling — to verify that the full pipeline executes correctly and that the system is not limited to analysis from pre-computed coverage files.

An explicit honesty boundary governs the methodology. The real-data validation in Experiments 1 and 2 begins at the coverage-file stage: the available compute environment (a single workstation, no cloud infrastructure) made full alignment of production-scale WGBS reads infeasible. The complete reads-to-coverage path is therefore exercised only at simulated scale in Experiment 3. This boundary is stated wherever it bears on a claim, not relegated to a limitations note.

## 1.6 Sources

The sources of the thesis are of four kinds.

The *primary data* are public. Coverage files and supplementary result tables of two peer-reviewed WGBS studies — GSE263850 [@gse263850] and GSE214232 [@gse214232] — were obtained from the Gene Expression Omnibus (GEO). Simulated FASTQ data for Experiment 3 were generated with controlled parameters to provide known ground-truth properties.

The *methodological literature* comprises the established science of bisulfite sequencing and differential-methylation analysis. The principal references are the methylKit [@akalin2012] and DSS [@park2016; @wu2015] statistical engines, the Bismark aligner [@krueger2011], and the nf-core/methylseq pipeline [@ewels2020], each cited to its primary publication.

The *system under study* is documented from its own source code and from the laboratory's framework description [@legrand2026]. Toolomics MCP server implementations, the methylation skill, and the agent configuration are described in Chapter 3 from direct inspection.

The *agent and protocol literature* — LLM tool use, MCP, autonomous agents for science, and the reliability of such systems — is drawn from primary sources. Because this literature is recent and fast-moving, it is treated with an explicit knowledge-cutoff caveat and was re-verified at the time of writing. The full apparatus of sources is given in the Bibliography, and the background they support is developed in Chapter 2.

## 1.7 Structure of the thesis

The thesis is organised as follows.

**Chapter 2 (Background & Related Work)** introduces the two literatures the thesis joins — WGBS DNA methylation and its statistics on one side, LLM agents and the Model Context Protocol on the other — and states the gap between them.

**Chapter 3 (System Design & Methods)** specifies the system under test: its four-layer architecture, the two MCP tool servers (Nextflow-based alignment and Dockerised R analysis), the methylation skill that encodes domain knowledge, the Mimosa agent framework and its goal evolution, and the reliability engineering — sign canonicalisation, post-hoc assertions, and instrumentation.

**Chapter 4 (Experiment 1: Replication — GSE263850)** presents the replication of a human AKAP11 knockout WGBS study, scored as a concordance triangle against both the published findings and an expert re-analysis.

**Chapter 5 (Experiment 2: Replication — GSE214232)** presents the replication of a mouse Dnmt3a conditional knockout study using the same triangulated evaluation, testing cross-species generalisation.

**Chapter 6 (Experiment 3: End-to-End — Simulated FASTQ)** demonstrates full-pipeline capability from simulated raw reads through alignment to DMR calling, exercising the reads-to-results path that the real-data experiments cannot.

**Chapter 7 (Discussion)** returns to the hypothesis, synthesises findings across the three experiments, weighs strengths against honest limitations, and considers threats to validity.

**Chapter 8 (Conclusions & Future Work)** states the contributions, draws the honest scope boundary, and develops the multi-omics extension roadmap for which methylation is the validated first vertical.

A **Bibliography** and **Annexes** — including the methylation skill specification, MCP tool catalogues, representative agent transcripts, and supplementary result tables — close the thesis.

## 1.8 New approach

The new approach of this thesis is to evaluate an autonomous scientific agent not by capability demonstrations — the dominant mode in the agents-for-science literature, where success is shown once and failure is omitted — but by measurement against knowable truth in a domain chosen precisely because its correct answers exist.

Three elements are, to our knowledge, novel in combination. First, a **triangulated concordance evaluation** scores the agent against both a published study and an independent expert re-analysis of the identical data, using the expert-versus-published agreement as the realistic ceiling for what any re-analysis can achieve. This prevents the evaluation from rewarding or penalising the agent for differences that arise from legitimate methodological variation rather than from error. Second, a **cross-species generalisation test** applies the same evaluation framework to a second organism (mouse, after human), asking whether the agent's reliability is a property of the system rather than an artefact of a single dataset. Third, a **full-pipeline end-to-end demonstration** exercises the complete path from raw FASTQ reads through bisulfite alignment to DMR calling, verifying that the agent is not limited to downstream analysis alone.

Underpinning all three experiments are two pieces of methodological engineering. A sign-canonicalising scoring library enforces a single convention for the direction of methylation change before any concordance is computed, removing a class of direction-of-effect errors that are invisible within any single run but corrupt cross-run comparisons. A set of post-hoc assertions transforms an agent's impossible-but-confident result — a methylation percentage outside [0, 100], a sample count that contradicts the input — into a hard stop rather than a silently wrong answer.

By treating methylation as a fully validated vertical rather than an isolated demonstration, and by building its claims on shared scoring infrastructure that other omics domains can adopt, the thesis offers both specific empirical results and an honest template for how tool-augmented LLM agents might be validated, domain by domain, before they are trusted in scientific practice.
