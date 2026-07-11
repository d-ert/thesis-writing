# 01_introduction

# Chapter 1 — Introduction

This thesis asks whether an artificial-intelligence agent can be trusted to perform a real piece of epigenomics. Large language models have made it possible to direct software to carry out an analysis in plain language, and to have it write and execute the code itself; the open question — the one that determines whether such systems belong anywhere near science — is not whether they can occasionally produce a correct answer, but whether they produce it reliably: concordantly with established findings, consistently across organisms and experimental designs, and with their errors visible rather than concealed behind fluent prose. The work that follows takes a single, well-understood analytical domain — differential DNA-methylation analysis from whole-genome bisulfite sequencing (WGBS) — and uses it as a proving ground on which that question can be given numbers instead of adjectives.

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


---

# 02_background

# Chapter 2 — Background & Related Work

## 2.0 Introduction to the chapter

This chapter assembles the background needed to read the rest of the thesis and locates the work
within two literatures that rarely meet. The first is the established science of **whole-genome
bisulfite sequencing (WGBS)** and **differential DNA-methylation analysis**: a mature field with
canonical data formats, statistical models, and software whose behaviour is well characterised.
The second is the fast-moving field of **tool-augmented large language model (LLM) agents** —
systems that plan, call external tools, and act on their results — and the still-young question
of whether such agents can be trusted with scientific analysis. The thesis sits exactly at the
seam between them: it takes a domain whose correct answers are knowable (§2.1–2.3) and asks
whether an agent (§2.4–2.5) can reach them autonomously.

The chapter proceeds accordingly. §2.1 introduces DNA methylation and the WGBS assay that
measures it. §2.2 follows the data from raw reads to per-cytosine coverage through the alignment
pipeline the system of Chapter 3 wraps. §2.3 defines differentially methylated cytosines and
regions (DMCs and DMRs) and contrasts the two statistical engines — methylKit and DSS — that the
agent routes between. §2.4 turns to LLM agents, tool use, and the Model Context Protocol (MCP)
that connects an agent to scientific software. §2.5 surveys autonomous agents for science and the
reliability problem that motivates the experimental programme. §2.6 states the gap these
literatures leave open, which the hypothesis of Chapter 1 sets out to close.

A note on sources is warranted at the outset. The methodological literature of §2.1–2.3 is
settled and is cited to its primary papers. The agent literature of §2.4–2.5 is recent and moves
faster than any single snapshot; claims there are tied to primary sources where available, and the
reader should be aware that findings in this area may evolve between writing and publication.



## 2.2 From reads to coverage: the alignment pipeline

Between the sequencer and the statistics sits an alignment-and-extraction pipeline whose job is to
turn millions of short, bisulfite-converted reads into the per-CpG count table of §2.1. This is
the stage automated by **MCP Server A** in Chapter 3, and three properties of it matter for the
thesis.

**Bisulfite-aware alignment is its own problem.** Standard short-read aligners assume the read and
the reference share an alphabet; bisulfite conversion deliberately breaks that assumption by
turning most cytosines into thymines, creating a three-letter genome that conventional alignment
mishandles. Specialised aligners solve this — most prominently **Bismark**, which converts reads
and reference into a common reduced alphabet, aligns, and then restores the original bases to
score methylation [@krueger2011]. Bismark also performs the **methylation-extraction** step that
emits the coverage file consumed downstream: a per-cytosine report of chromosome, position,
strand, methylation percentage, and methylated/unmethylated counts — the Bismark `.cov` format on
which the rest of the analysis depends.

**Reproducibility is delegated to a workflow framework.** Running this multi-step process — quality
trimming, alignment, deduplication, methylation extraction, reporting — reproducibly across
samples and machines is the role of a workflow manager. The community standard is **Nextflow**,
which expresses a pipeline as a dataflow of containerised processes so that the same workflow runs
identically on a laptop, a cluster, or the cloud [@ditommaso2017]. On top of it, the **nf-core**
project curates peer-reviewed, versioned, community-maintained pipelines with standardised inputs,
tests, and software-provenance reporting [@ewels2020], and **nf-core/methylseq** is its WGBS
pipeline — the exact artefact Server A invokes. The significance for this thesis is that
this upstream stage is already engineered for reproducibility through pinned containers and
versioned code; the non-determinism the thesis investigates is introduced not here but by the
agent that orchestrates it.

**The coverage file is the natural boundary.** Because alignment is computationally heavy — full
real-WGBS alignment was infeasible on the available hardware (Chapter 3) — the coverage file is
also the practical boundary at which this thesis's real-data validation begins. The data model of
§2.1 is recovered exactly at this point, so downstream analysis can be validated against published
studies even when the alignment half is exercised only at small synthetic scale.

---

## 2.3 Differential methylation: DMCs, DMRs, and two statistical engines

The scientific question WGBS is used to answer is comparative: where does methylation differ
between two groups, and in which direction? Answering it well is a non-trivial statistical
problem, and the choice of method materially affects the result — which is precisely why the
agent needs the engine-selection skill of §3.4, and why the validation of Chapters 4–6 must score
against more than one baseline.

**DMCs versus DMRs.** Two units of analysis are standard. A **differentially methylated cytosine
(DMC)** is a single CpG whose methylation level differs significantly between groups. A
**differentially methylated region (DMR)** is a contiguous genomic interval — often a fixed-width
tile or a run of adjacent DMCs — that differs as a unit. DMRs are usually the more biologically
interpretable object, because regulatory effects act over regions rather than isolated bases and
because aggregating neighbouring CpGs improves statistical power and reduces the multiple-testing
burden; DMCs offer finer resolution at the cost of many more tests. A region is summarised by an
effect size, typically the **difference in mean methylation** between groups (often written Δβ or
`meth.diff`), and a significance value; the sign of that difference encodes direction
(hyper- versus hypo-methylation), a detail whose mishandling is the polarity bug of §3.6.

**Why the statistics are hard.** Three features of WGBS counts complicate naïve testing. Coverage
varies by orders of magnitude across sites, so equal weighting is wrong. Biological replicates are
**overdispersed** — the variance between replicates exceeds what a simple binomial model predicts —
so tests that ignore overdispersion produce anti-conservative p-values and inflated false-positive
rates. And the sheer number of CpGs (tens of millions genome-wide) makes **multiple-testing
correction** essential; methods control the false discovery rate (FDR) via Benjamini–Hochberg
[@benjamini1995] or related procedures, reported as q-values. Calibrated control of false
positives under these conditions remains a general concern whenever automated systems select
analysis parameters, and it motivates the careful threshold documentation across the experimental
chapters.

**Two engines, two philosophies.** The field offers several tools [@robinson2014]; this work uses
the two the agent routes between, which make opposite trade-offs.

- **methylKit** performs direct, per-CpG tests — Fisher's exact test for two samples, or logistic
  regression with optional overdispersion correction and covariates for replicated and paired
  designs — and calls DMRs by tiling the genome into windows and testing each tile [@akalin2012].
  It is fast, transparent, and well-powered when coverage and replicate counts are high.
- **DSS** models the counts with a Bayesian beta-binomial hierarchy: it shrinks the dispersion
  estimate across the genome and, for WGBS, **spatially smooths** methylation levels by borrowing
  information from neighbouring CpGs, then tests for differential methylation and assembles DMRs
  from the result [@feng2014; @wu2015; @park2016]. This recovers signal at low coverage or with few
  replicates that per-CpG tests miss, at the cost of speed and of a smoothing assumption that must
  not be double-applied (a guardrail noted in §3.4).

The two are complementary rather than strictly ranked: methylKit is the natural choice in the
high-power regime and DSS in the low-power regime, and at the boundary the defensible practice —
encoded directly in the skill of §3.4 — is to run both and treat concordant calls as the confident
ones. A spatial-smoothing alternative, **BSmooth**/`bsseq`, occupies the same low-power niche as
DSS and supplies the smoothed-methylation tracks used for visualisation [@hansen2012]. The
existence of several defensible methods, each with tunable thresholds, is the reason a single
"ground truth" DMR count does not exist for a real dataset, and why the validation in Chapter 4
scores gene-level recovery, direction, and qualitative signature rather than count identity.

---

## 2.4 Large language model agents, tool use, and the Model Context Protocol

The second literature concerns the actor rather than the analysis. Modern LLMs are
transformer-based sequence models [@vaswani2017] which, once scaled, exhibit strong few-shot and
instruction-following behaviour [@brown2020] and can be prompted to externalise intermediate
reasoning before answering [@wei2022]. On their own, however, they are closed systems: they
generate text, cannot execute code or read files, and have no access to ground truth beyond their
training. The step from language model to agent is the addition of **tools** and a **loop**.

**Tool use and the agent loop.** A tool-using agent interleaves reasoning with action: it decides
on a next step, calls an external tool, observes the result, and repeats. The **ReAct** pattern
formalised this interleaving of reasoning traces and tool actions [@yao2023], and **Toolformer**
showed that models can learn when and how to invoke tools through their API signatures
[@schick2023]; retrieval-augmented generation similarly grounds outputs in external documents
rather than parametric memory [@lewis2020]. The recurring theme is that the model supplies
decisions while tools supply capabilities and ground truth — exactly the orchestration/execution
split that Chapter 3 makes its central design commitment.

**The Model Context Protocol.** Connecting an agent to many tools historically meant bespoke
integration code per tool. The **Model Context Protocol (MCP)**, an open standard introduced in
late 2024, defines a uniform client–server interface through which an agent discovers and calls
tools, retrieves resources, and uses prompt templates, so that any MCP-speaking client can use any
MCP server without custom glue [@mcp2024]. MCP is the protocol on which the Toolomics servers of
§3.2–3.3 are built, and the property that makes it valuable for reliability is the same one that
makes it valuable for engineering: tools become typed, versioned, independently testable services
rather than inlined code, which confines the unpredictable component to the agent and keeps the
executing component fixed.

**Encoding domain expertise.** A capability gap remains between having tools and using them
well: an agent equipped with methylKit and DSS still needs to know which to choose, what
thresholds to set, and which pitfalls to avoid. A lightweight answer that has emerged in agent
practice is the **skill** — a declarative, version-controlled document of domain procedure and
guardrails that the agent consults at run time rather than re-deriving on every invocation. The
methylation skill of §3.4 is an instance of this idea, and whether such encoded expertise
improves the quality and consistency of agent-driven analyses is a question the experiments of
Chapters 4–6 address.

---

## 2.5 Autonomous agents for science and the reliability problem

Tool-using agents have been turned toward scientific work with striking demonstrations, and with
equally striking gaps in their evaluation. The promise and the problem together motivate this
thesis.

**Agents that do science.** Recent systems couple LLMs to laboratory and computational tools to
carry out research tasks with limited human intervention: agents that plan and execute chemical
synthesis or computational chemistry by orchestrating domain tools [@boiko2023; @bran2024], and
frameworks that attempt end-to-end research — ideation, experimentation, and write-up — in machine
learning [@lu2024]. The framework this thesis evaluates, Mimosa (Chapter 3), belongs to this
lineage but answers a narrower, more measurable question than full-paper generation: can a
per-task synthesised workflow reproduce a known analysis? [@legrand2026]

**The reliability problem.** What these demonstrations rarely establish is reliability. LLMs are
non-deterministic and prone to fluent, confident errors — including fabricated facts and
unsupported claims [@ji2023] — and an agent that wraps an LLM inherits these failure modes while
adding new ones: silent tool failures, irreproducible run-to-run behaviour, and self-reported
successes that do not survive inspection. In a scientific setting these are disqualifying unless
measured and controlled, because a plausible-looking wrong answer is worse than an obvious one. The
concrete failures documented in §3.6 — the same input yielding results that differ by orders of
magnitude, an impossible region count carried into a biological conclusion — are precisely this
problem in the methylation domain.

**Evaluation is catching up, unevenly.** Benchmarks have begun to measure agent capability on
scientific and data-analysis tasks — for example task suites that score whether an agent's
generated analysis reproduces a reference result [@scienceagentbench; @paperbench]. These measure
capability (does it ever succeed?) more than reliability (does it succeed consistently, and
fail safely?), and they are general rather than tied to a domain with an established ground truth.
For a clinically-adjacent assay such as WGBS methylation, the quantities a practitioner actually
needs — concordance with published findings, calibrated false-positive control, and reproducibility
across repeated runs — have not, to our knowledge, been reported for an LLM agent.

---

## 2.6 The gap and the thesis's position

Bringing the two literatures together exposes a specific, fillable gap.

On one side, **the methods are mature and their correct answers are knowable** (§2.1–2.3): WGBS has
canonical formats, methylKit and DSS are characterised tools, published studies provide concrete
target findings, and synthetic data can supply exact ground truth. On the other side, **agents are
capable but unproven on reliability** (§2.4–2.5): the orchestration/execution split and protocols
like MCP make it architecturally possible to fence non-determinism away from numerical execution,
and skills make it possible to encode expertise — but whether these mechanisms deliver concordant,
well-controlled methylation analysis has not been demonstrated or measured.

That absence is the gap this thesis addresses. Where prior agent-for-science work emphasises
capability demonstrations, this work emphasises **measurement against knowable truth** in a single
well-chosen domain. The hypothesis stated in Chapter 1 proposes that a tool-augmented LLM agent,
constrained by a domain skill and typed MCP tools, can autonomously execute WGBS differential-
methylation analyses — replicating published findings across organisms and executing the full
pipeline from raw reads to called regions — with results concordant with expert analyses. The
system that makes this testable is the subject of Chapter 3; the measurements themselves are
Chapters 4–6, which validate the hypothesis through replication of a human dataset, replication
of a mouse dataset, and an end-to-end run on simulated data respectively. The conclusions are
drawn in Chapter 7.


---

# 03_system_design_and_methods

# Chapter 3 — System Design & Methods

## 3.0 Introduction to the chapter

This chapter describes the system whose behaviour the rest of the thesis sets out to
measure. The system is **Mimosa**, a tool-augmented Large Language Model (LLM) agent, together
with the **Toolomics** infrastructure of Model Context Protocol (MCP) servers through which it
acts. The object of study is concrete and pre-existing: a conversational agent that, given a
folder of whole-genome bisulfite-sequencing (WGBS) data and a natural-language goal, drives a
complete differential-methylation analysis — coverage filtering, normalisation, differential
testing, region calling, annotation, and biological interpretation — by writing analysis code
and invoking domain-specific tools, rather than by following a fixed script.

The chapter is presented as *Methods* in two senses. First, it documents the engineered
artefact under test, so that the experiment chapters (Chapters 4, 5, and 6) can be read as
measurements of a fully specified system. Second, the design choices described here — the
separation of orchestration from execution, the encoding of domain expertise as a *skill*, the
two-layer tool surface, and the file-on-disk reproducibility contract — are themselves the
mechanisms by which the system is intended to be reliable, and so each is later examined
empirically. Where a component is exercised only partially in this work (most importantly, the
upstream alignment pipeline of Server A, which the available compute could not run on full
real data — see §3.2 and Chapter 4), this is stated explicitly at the point of description and
not deferred to the limitations section.

Nothing in this chapter depends on experimental results; it describes work already built. The
quantitative behaviour of the system — how concordant its output is with published studies,
how it performs against synthetic ground truth, and how reproducible it is across repeated runs
— is the subject of the chapters that follow.

The chapter proceeds from the whole to the parts. §3.1 gives the architecture and the
end-to-end data flow. §3.2 and §3.3 describe the two MCP servers — the Nextflow/methylseq
runner and the Dockerized R methylKit/DSS runner. §3.4 describes the *skill* that supplies the
agent's domain knowledge and routes its decisions. §3.5 describes the Mimosa framework — its
workflow-synthesis loop, its evolutionary search and verifier, and the evolution of its goal
specification. §3.6 collects the reliability-engineering guardrails and instrumentation that
the experiment chapters draw upon, and §3.7 situates the system within the wider Toolomics
ecosystem.

**A note on contribution.** Because a thesis is assessed on its author's own work, the boundary
is drawn explicitly here and assumed throughout. The **Mimosa framework** — its planner, the
Quality-Diversity evolution engine, the multi-source verifier, and the SmolAgents/LangGraph
runner (§3.5) — and the **Toolomics** control plane that deploys and isolates the tool servers
are the host laboratory's prior work (Legrand et al., 2026), used here as the apparatus under
test. The components specific to this thesis are: **both MCP servers** — the Nextflow/methylseq
runner of §3.2 and the execute-only R/Bioconductor methylation server of §3.3, with its bundled
annotation — the **methylation skill** of §3.4, the **goal specification and its six-version
evolution** of §3.5.5, the **epigenomics claim adapter** of §3.7, and two fixes to the
Perspicacité literature service (§3.7). On top of these sits the scientific core of the work: the
**reliability guardrails and instrumentation** of §3.6 — this thesis's own methodology for making
the agent's trustworthiness measurable — and the **validation experiments** of Chapters 4–6, by
which the laboratory's agent is, for the first time, measured on DNA-methylation analysis.



## 3.2 MCP Server A — the Nextflow / nf-core/methylseq runner

Server A is the system's upstream component: it turns raw sequencing reads into the per-CpG
coverage files that the downstream analysis consumes. It is a FastMCP application (speaking the
streamable-HTTP transport, like Server B) that wraps the community-standard
**nf-core/methylseq** workflow and exposes its operation — input preparation, execution,
monitoring, and teardown — as eight typed tools. The agent never calls `nextflow` directly;
it composes these tools, and the server is responsible for constructing the pipeline
invocation, selecting an execution backend, and reporting status.

### 3.2.1 The tool surface

The eight tools fall into three groups — preparing inputs, running and managing the pipeline,
and inspecting the environment:

| Tool | Group | Purpose |
|---|---|---|
| `prepare_methylseq_inputs` | input | Build the nf-core samplesheet (`sample, fastq_1, fastq_2`) from local FASTQ globs, an S3 path, or a list of SRA accessions; auto-detects R1/R2 mate pairs and sample names. |
| `fetch_sra_data` | input | Download SRA/ENA/DDBJ data via **nf-core/fetchngs 1.12.0**, locally or on the cloud, optionally emitting a methylseq samplesheet on completion. |
| `upload_to_cloud` | input | Push local files to S3 (`s3://`) or Google Cloud Storage (`gs://`) for cloud execution. |
| `run_methylseq_pipeline` | run | Launch **nf-core/methylseq 2.6.0** with full control over aligner, library type, trimming, M-bias correction, reference, and resource limits; supports `resume`. |
| `get_pipeline_status` | run | Query a running/finished workflow; for cloud runs returns the `session_id` needed to resume, for local runs checks the Nextflow/Singularity install and free disk. |
| `manage_pipeline` | run | Cancel a running cloud workflow or clean Nextflow work/cache directories. |
| `list_available_resources` | env | Enumerate accessible Seqera organisations, workspaces, and compute environments. |
| `validate_environment` | env | Pre-flight check of every dependency and credential (Nextflow, Singularity, disk, Seqera/AWS tokens) with remediation hints. |

The biologically consequential parameters are concentrated in `run_methylseq_pipeline`. It
defaults to the **Bismark** aligner (with `bwameth` and `bismark_hisat` also selectable),
accepts a library-type switch covering `rrbs`, `pbat`, `em_seq`, `single_cell`, `accel`, and
`zymo` protocols, and exposes the trimming and M-bias-correction knobs that most affect call
quality — adapter clipping at either end and the `ignore_r1/r2` and `ignore_3prime_r1/r2`
options (the last defaulting to ignoring two bases of read 2, a standard correction for the
end-repair bias of directional WGBS libraries). The reference genome is supplied either as an
iGenomes identifier (e.g. `GRCh38`, `GRCm39`) or as a custom FASTA, and per-cytosine reporting
is enabled by default so that the output is directly consumable by Server B.

### 3.2.2 Two execution backends

A single `execution_mode` argument selects between two backends that the server configures
differently:

- **Local execution** runs Nextflow against a **Singularity** container engine on the
  workstation (`workflow.containerEngine = 'singularity'`), with a per-process resource ceiling
  that defaults to 16 CPUs and 128 GB of memory and a 24-hour time limit, and a Singularity
  image cache held in the workspace. The server first checks, via helper functions, that
  Nextflow and Singularity/Apptainer are installed and that sufficient disk is free.

- **Cloud execution** submits the run to the **Seqera Platform** (formerly Nextflow Tower),
  which dispatches the work to an **AWS Batch** compute environment. The server talks to the
  Seqera REST API (default endpoint `https://api.cloud.seqera.io`) through a small client that
  launches workflows, polls their status, and cancels them, reading the workspace and
  compute-environment identifiers and access token from environment variables.

### 3.2.3 Scope exercised in this work

Both backends are implemented, but the compute available for this thesis constrains which is
exercised. There is **no Seqera or AWS access** on the project workstation, so the cloud backend
is described as a designed capability rather than a path run here. The local backend is
functional, but aligning full real human WGBS from FASTQ with nf-core/methylseq was estimated
at roughly **six days per sample** on this hardware, which is not feasible for the multi-sample
replications of Chapter 4. Consequently:

- the **real-data replications (Chapter 4 and Chapter 5) start from the published `.cov`
  coverage files** and do not exercise Server A's alignment stage;
- Server A's full FASTQ → `.cov` path is demonstrated only at **small synthetic scale**
  (Chapter 6), where a reduced reference and short simulated read sets complete quickly, with an
  existing small-genome Bismark test run as additional evidence that the local Singularity path
  is correct end-to-end.

This is the system's principal honesty boundary, and it is stated here, at the description of
the component, rather than left to the discussion: the end-to-end claim of the thesis covers the
*coverage-to-regions* analysis on real data and the *reads-to-coverage* alignment only on
small synthetic data.

## 3.3 MCP Server B — the Dockerized R methylKit/DSS runner

Server B is the system's downstream engine: it takes the Bismark coverage files and carries them
through differential-methylation analysis to annotated, interpreted regions. It exists to solve
a concrete deployment problem. Mimosa's own execution sandbox installs only Python packages, so
the R/Bioconductor stack that the canonical methylation pipeline requires — methylKit, DSS,
genomation, and their dependencies — can never be installed in the agent's local environment,
and any analysis script the agent writes would fail at `library(methylKit)`. Server B removes
this obstacle by shipping that stack as a service: a Docker image built on
**`bioconductor/bioconductor_docker:RELEASE_3_19`** (Bioconductor 3.19) with methylKit, DSS,
bsseq, genomation, GenomicRanges, matrixStats, `data.table` (pinned to 1.15.4), dplyr, ggplot2,
clusterProfiler, the `org.Hs.eg.db`/`org.Mm.eg.db` annotation databases, and supporting packages
pre-installed, plus pre-built UCSC annotation tracks for hg38 and mm10. The agent runs its R
inside this container over MCP and so inherits a fixed, reproducible analysis environment.

### 3.3.1 Two altitudes of tools — and the one used here

Server B can present its R environment at two very different altitudes. The two are not both
live at once; they are two server variants, and the one that produced every run analysed in
this thesis is the more minimal of the two.

**The primary surface: write a real script, then run it (two tools).** The production methylation
server is *execute-only*. It exposes just two tools, and deliberately nothing more:

| Tool | Purpose |
|---|---|
| `execute_r_script_file(filename)` | **Primary tool.** Run an R script that already exists in the workspace via `Rscript`, with the workspace as the working directory; the execution timeout is set server-side (default 7200 s). |
| `list_workspace_files()` | List the workspace contents, to sanity-check which scripts and inputs are visible before running. |

The server's own documentation states the rationale plainly: "No code-string execution, no
script-writing, no typed atomic pipeline tools are registered here — that's intentional, so the
agent commits to *write a real R script file, then run it* rather than reaching for shortcuts."
Two conventions make the surface reproducible. The script the server runs is a real file already
on disk — authored by the agent with its own file-writing tools — so the script a reviewer reads
is exactly the script that executed, with no inlined code; and the text returned to the agent is
capped (standard output and error truncated to 4000 characters, with the full logs left on disk),
keeping the agent's context small and forcing large results to persist as files rather than pass
through the conversation. The minimalism is itself a reliability choice: it removes the agent's
option to run throwaway code that leaves no auditable trace.

**The alternative surface: typed atomic tools (a retained variant).** An earlier design exposed
the same R stack at a far more constrained altitude. Alongside four generic runners
(`execute_r_code`, which saves supplied R to a timestamped file and runs it; `write_r_script`;
`execute_r_script_file`; and `list_workspace_files`), it registered a set of typed *atomic*
tools that each perform one canonical pipeline step and validate their inputs. Each is a thin
wrapper that invokes a corresponding `r_scripts/*.R` helper with a JSON argument blob and parses
a structured result the helper prints inside a `<<<RESULT>>>…<<<END>>>` footer — so the agent
receives, for example, the number of sites tested and the number significant at q < 0.05, not
free text. This variant is retained in the repository (`old_server_with_atomicTools`) as an
alternative design that prioritises constraint over expressivity. Its fourteen atomic tools cover
the whole methylKit workflow:

| Tool | Pipeline step | Key defaults |
|---|---|---|
| `load_bismark` | read `.cov` into a `methylRawList` | `min_cov=10`, `assembly="hg38"` |
| `qc_per_sample` | per-sample methylation/coverage QC plots | — |
| `filter_coverage` | `filterByCoverage` | `lo_count=10`, `hi_perc=99.9` |
| `normalize_coverage` | `normalizeCoverage` | `method="median"` |
| `unite_samples` | `unite` to a `methylBase` | strict intersect unless `min_per_group` set |
| `sd_filter` | drop low-variance CpGs | `sd_cutoff=2.0` (pts) |
| `qc_sample_structure` | correlation / clustering / PCA | — |
| `calculate_dmc` | per-CpG `calculateDiffMeth` (paired via `covariates`) | `overdispersion="MN"`, `adjust="BH"` |
| `tile_methyl_counts` | `tileMethylCounts` + `unite` | `win=500`, `step=500`, `cov_bases=5` |
| `calculate_dmr` | DMR via tiled `calculateDiffMeth` | `overdispersion="MN"`, `adjust="BH"` |
| `get_methyl_diff` | extract significant + write CSV/bedGraph | `difference=10`, `qvalue=0.05` |
| `annotate_methyl_diff` | gene + CpG-island annotation | `assembly`-resolved BEDs |
| `export_methyl_diff` | flat CSV with per-group mean beta | — |
| `list_methylkit_objects` | inspect `.rds` objects in the workspace | utility |

### 3.3.2 State flow via `.rds` files

The atomic tools do not hold state in memory between calls; they pass it through the filesystem.
Each step reads one or more `.rds` files (serialised R objects) from the workspace and writes its
output as another `.rds`, so a fallback analysis is an explicit chain of files:

```
load_bismark        → methylkit_raw.rds         (methylRawList)
  filter_coverage   → methylkit_filtered.rds    (methylRawList)
  normalize_coverage→ methylkit_normalized.rds  (methylRawList)
  unite_samples     → methylkit_united.rds      (methylBase)
  calculate_dmc     → methylkit_myDiff.rds      (methylDiff)
  get_methyl_diff   → significant.csv
  annotate_methyl_diff / export_methyl_diff → annotation.pdf, results.csv
```

DMR analysis branches from the normalised object through `tile_methyl_counts` →
`calculate_dmr`. Because each intermediate is named and typed, a run that fails partway can be
resumed: `list_methylkit_objects` reports the class of every `.rds` already present, letting the
agent identify the right input for the next step rather than recomputing the expensive
differential test. The same `.rds` discipline reappears in the execute-only design of §3.3.1, by
convention rather than enforcement: the agent's own scripts serialise their intermediates — the
run reports of §3.6 show a `methylBase_filtered_united.rds` handed from the QC step to the
differential test — so the file-on-disk state model is a property of the pipeline, not only of the
atomic tools. *(Figure 3.3.)*

### 3.3.3 Bundled annotation and its resolution

Biological annotation is the last stage of the pipeline, and the image ships the reference
tracks it needs so that annotation runs offline: pre-built UCSC RefSeq gene models and
CpG-island BEDs for both assemblies, at `/opt/annotations/` —
`hg38_refseq_genes.bed` (BED12 transcripts) and `hg38_cpg_islands.bed` (BED4), with `mm10`
equivalents. `annotate_methyl_diff` resolves them in a fixed order: an explicit
`refseq_bed`/`cpg_bed` path wins; otherwise an `assembly` of `hg38` or `mm10` selects the
bundled file; otherwise the tool errors rather than guessing. Other assemblies (hg19, mm9,
custom genomes) require the user to supply BED files in the workspace. The gene databases
`org.Hs.eg.db` and `org.Mm.eg.db` are likewise bundled, so gene-ontology enrichment runs without
network access, whereas KEGG enrichment, which queries a live service, does not.

### 3.3.4 Deployment

Server B requires no change to the Toolomics control plane to come online. `deploy.py`
auto-discovers the server's `docker-compose.yml`, assigns it a free port in the 5000–5200 range,
and starts the container; Mimosa's port scanner then finds the server and registers its tools
automatically — the two of the execute-only server used throughout this thesis, or the fuller set
of the retained atomic-tool variant. The image is comparatively expensive to build the first time —
installing the Bioconductor stack and downloading the UCSC annotations takes roughly 15–30
minutes — but the result is cached, so this cost is paid once rather than per run.

## 3.4 The skill as router and guardrail

The two MCP servers give the agent *capabilities*; the **skill** gives it *judgement*. It is a
declarative document — a structured Markdown file the agent reads — that encodes the
domain expertise a methylation analyst would otherwise have to supply by hand on every run:
which differential-methylation engine fits the data, what quality-control thresholds to apply,
which non-obvious pitfalls to avoid, and how to lay out a reproducible project. In the layered
architecture of §3.1 it is the knowledge layer that sits between the agent and the tools,
shaping *how* the tools are used without itself executing anything. Its design rationale is
principle 2 of §3.1.4: expertise written once, consulted consistently, rather than re-derived —
inconsistently — by the LLM on each run. Whether this consistency materially reduces run-to-run
variance is a question the experiment chapters are positioned to address.

### 3.4.1 The central decision: engine selection

The skill describes its single most consequential job as routing between the two engines before
any analysis code is written. methylKit and DSS make different statistical trade-offs —
methylKit performs direct per-CpG tests and is fast and well-powered when coverage and replicate
counts are high, whereas DSS borrows information across neighbouring CpGs by spatial smoothing
and shrinks dispersion across the genome, recovering signal at low coverage or with few
replicates that per-CpG tests miss. The skill turns this into an explicit decision table keyed
on coverage and replication:

| Coverage / replicates | Engine |
|---|---|
| ≥10× **and** ≥4 replicates/group (high power) | methylKit (`calculateDiffMeth`, `overdispersion="MN"`); DSS also fine |
| 5–10×, **or** 2–3 replicates/group | **DSS** (dispersion shrinkage + smoothing) |
| Sparse WGBS, single-CpG resolution wanted | **DSS** with `smoothing=TRUE` |
| Multifactor / covariate-adjusted / paired design | **DSS `DMLfit.multiFactor`** *or* methylKit `covariates=` |
| <5× or n=2 | DSS `equal.disp=TRUE`, or Fisher's exact (methylKit) — exploratory only |

The skill's guidance at the boundary is to run both engines and treat the concordant DMRs as the
confident calls — a built-in form of the cross-method agreement that the experiment chapters
also use as a concordance axis.

### 3.4.2 Progressive disclosure: the hub and the reference files

The skill is organised so that only a small, always-relevant core is loaded into the agent's
context by default, with depth pulled in on demand. The hub document owns the shared,
engine-agnostic workflow — the execution model, input and aligner detection, file-format
definitions, metadata handling, QC thresholds, annotation, interpretation, visualisation, and
project structure — and the engine-selection decision above. The command-level depth for each
engine lives in two separate reference files, `references/methylkit.md` and `references/dss.md`,
which the skill instructs the agent to read **only after it has chosen an engine**. This keeps
the resident context compact and avoids loading, say, the full DSS multifactor-GLM reference
during a run that uses methylKit.

### 3.4.3 Gotchas as guardrails

A distinctive feature of the skill is that a substantial part of it is a catalogue of
*failure modes* — the non-obvious facts that, in the authors' experience, cause the most
analyses to go silently wrong. By stating them where the agent will read them, the skill turns
hard-won debugging knowledge into preventive guardrails. The most important are:

- **Derive groups from metadata, never hardcode them.** Treatment/group vectors must come from
  a `metadata.csv`; if it is missing, the agent is told to halt and ask rather than guess — a
  rule directly relevant to the polarity bug discussed in §3.6.
- **Cap the core count.** `parallel::detectCores()` reports the host's CPUs, not the container's
  cgroup limit, so naive parallelism oversubscribes inside Docker; the skill prescribes a capped
  `mc.cores`/`ncores` and lower still on genome-wide objects whose memory scales with cores.
- **Do not double-smooth DSS.** DSS smooths internally, so the raw `BSseq` must be passed to its
  test; pre-running `bsseq::BSmooth` is a silent statistical error.
- **Counts are required for count-based tests.** A bedGraph that carries only methylation
  percentages, without methylated/unmethylated counts, is unusable for DSS or methylKit's
  logistic/Fisher tests.
- **Use exact annotation filenames, never mix aligners, and always send plots to a file
  device** — the MCP returns text, not graphics.

The QC thresholds the skill fixes are similarly concrete and engine-agnostic: bisulfite
conversion inferred from CHH methylation below ~1%, mapping rate above 70%, at least ~1 million
covered CpGs per WGBS sample, replicate correlation above r ≈ 0.95, and the expectation that
replicates cluster together in PCA with no batch separation — with the standing instruction to
flag and confirm with the user before excluding any sample.

### 3.4.4 Project structure and the run report

Finally, the skill prescribes a fixed project layout — `raw_data/`, `metadata.csv`,
`config.yaml` (genome, engine, coverage, effect-size and FDR thresholds, tile size, smoothing),
numbered `scripts/`, a `results/` tree, and an **append-only `run_report.txt`** in which each
step records the mode and engine chosen, the files found, the steps run or skipped, and any
samples excluded. The append-only run report is both a reproducibility aid and a source of
evidence about what the agent actually decided on a given run.

## 3.5 The Mimosa agent — framework, loop, goal evolution, and the workspace contract

The previous sections described the *capabilities* the agent acts through and the *knowledge*
that shapes how it acts. This section describes the actor itself. **Mimosa** is the host
laboratory's open-source framework for autonomous scientific research (Legrand et al., 2026);
this thesis does not introduce it but adopts it as the agent under test; the
methylation-specific components that surround it — enumerated in the contribution note of §3.0 —
are the thesis's own work, and the validation of the whole on DNA-methylation analysis is its
purpose. Describing Mimosa accurately matters for the validation
that follows, because the system is more than the "read goal → call tool → observe → repeat"
loop sketched in §3.1.1: that loop is what an *execution agent* does within a single workflow,
but Mimosa as a whole is a system that **writes the workflow itself** and can **evolve it across
generations**. Both facts bear directly on reliability and are therefore set out here rather
than abstracted away.

### 3.5.1 What Mimosa is: a workflow-synthesising, self-evolving framework

Mimosa's self-description is precise: it "writes a custom multi-agent workflow per task, runs it
in a sandbox, checks what the agents actually did against independent vantage points, and evolves
the workflow across generations with a Quality-Diversity inspired search." Given a task — here,
"analyse this folder of WGBS coverage files and call differential methylation" — it does not run a
fixed program. It *synthesises* one. The framework is organised in five layers, wired through
small dataclass schemas:

| Layer | Component | Role in a methylation run |
|---|---|---|
| 0 | **Planner** *(optional; `--goal` mode only)* | Decomposes a high-level objective into discrete tasks. Bypassed for the single-task methylation goal used here. |
| 1 | **ToolManager + Perspicacité** | Scans the configured address/port range (`0.0.0.0:5000–5100`) and registers every MCP tool it finds — the two Toolomics servers of §3.2–3.3 — and, when the Perspicacité literature service (§3.7) is running, can pull supporting literature. |
| 2 | **EvolutionEngine** | Synthesises the workflow as Python source and, in `--learn` mode, evolves it across generations (§3.5.3). |
| 3 | **WorkflowRunner** | Executes the synthesised workflow in a sandbox built on Hugging Face **SmolAgents** (a `LocalPythonExecutor` with an AST allow-list) over shared **LangGraph** state. The execution agents inside this sandbox are what call the MCP tools and write the R scripts of §3.3–3.4. |
| 4 | **VerifierEvaluator** | After each run, scores the workspace from six independent vantage points (§3.5.4) and feeds the next mutation. |

The design commitment that distinguishes Mimosa from a scripted pipeline — and the one most
relevant to a reliability thesis — is **code-as-genotype**: each synthesised workflow is a
complete, standalone Python program emitted to disk (no domain-specific language, no YAML), so
"any generation can be inspected, diffed, or re-run standalone." The program is the unit that is
stored, mutated, and audited. Its *phenotype* is whatever it produces in the shared workspace:
the `.rds` intermediates, figures, tables, and `run_report.txt` of §3.1–3.4.

### 3.5.2 Execution modes and the run regime used in this thesis

Mimosa exposes several modes, selected by command-line flag. The two axes that matter here are
**planning** (`--task` for a single focused operation versus `--goal` for a multi-step objective
that invokes the planner) and **learning** (`--learn` adds evolution across generations; without
it, the framework synthesises and runs a single workflow — "one-shot"). A `--single_agent` mode
skips multi-agent synthesis entirely for a fast, learning-free baseline.

It is important to state plainly which regime produced the artefacts this thesis analyses. The
completed methylation runs (`run5`–`run12`) were predominantly **one-shot, single-task runs with
evolution disabled** — the prompt harness (`scripts/run_prompt_ablation.sh`) explicitly invokes
`main.py … --max_evolve_iterations 1` so that each goal variant is evaluated in isolation.
Evolution is therefore not the default operating mode of the system as validated here; presenting
Mimosa honestly means describing the full evolutionary machine while being clear that most of the
evidence comes from its single-shot use.

### 3.5.3 The evolution loop (when `--learn` is enabled)

When evolution is enabled, the workflow program is the thing that evolves. The mechanics, drawn
from the framework's evolution engine (`sources/core/evolution_engine.py`), are:

- **Selection — a Quality-Diversity archive** (MAP-Elites-style, maximum population 50). Each
  workflow is scored as `qd_score = (1 − w)·quality + w·novelty`; novelty is a k-nearest-neighbour
  distance (k = 25) over a *behaviour descriptor* `[n_agents, n_edges, n_branches, prompt_chars]`,
  so the archive rewards structurally distinct workflows rather than collapsing onto one design.
- **Variation — stagnation-driven scope.** Mutation boldness is a continuous function of how much
  the recent "prompt gradients" repeat: when progress stalls the search widens from a prompt-level
  tweak toward a complete topology rethink; near-winners are protected. About 30 % of generations
  use **crossover** of two parents.
- **Cold start.** When the archive is empty, a similarity-filtered scan of past runs on disk
  (MiniLM cosine ≥ 0.5) seeds the search, so useful workflows transfer across tasks.
- **Termination.** A generation budget (`max_learning_evolve_iterations`, default 45) or an
  early-stop when the verifier score reaches `learned_score_threshold` (0.94).

```
  task: "analyse these WGBS .cov files and call differential methylation"
       │
  (0) PLANNER ............. decompose into tasks         (optional, --goal only)
       │
  (1) TOOLMANAGER + Perspicacité
       │  discover MCP tools on 0.0.0.0:5000–5100 (Server A, Server B);
       │  pull supporting literature ─────────────────►  feeds Verifier Source A
       ▼
  (2) EVOLUTION ENGINE ─────────────────────────────────────────────────┐
       │  synthesise the workflow as a standalone Python program          │
       │  (workflow_genotype.py — "code-as-genotype")                     │
       ▼                                                                  │
  (3) WORKFLOW RUNNER   sandbox: SmolAgents LocalPythonExecutor +         │
       │  LangGraph state. Execution agents call the MCP tools, author    │ mutate /
       │  R scripts, run them on Server A / Server B → shared workspace   │ crossover
       ▼                                                                  │ (--learn
  (4) VERIFIER — six deterministic claim sources                         │  only)
       │  A literature   B goal        C disk-vs-claim                    │
       │  D math invariants   E reproducibility   F statistics           │
       │  score + rubric-blind "abstracted gradient"                      │
       ▼                                                                  │
      QD ARCHIVE (MAP-Elites, population ≤ 50) ───────────────────────────┘
      keep structurally-diverse high scorers; draw the next parent
```

*(Figure 3.4.) In the one-shot regime used for most runs in this thesis (§3.5.2) the loop runs
once, top to bottom; the return path on the right is active only under `--learn`.*

### 3.5.4 The multi-source verifier — what a "success" actually means

The component most directly aimed at trustworthiness is the verifier, and it is where Mimosa
departs most sharply from agents that grade themselves. After each run, **six independent claim
sources** inspect the workspace and emit success-polarity claims, and — crucially — each claim is
checked by a **Python program the judge writes against the workspace, not by re-asking an LLM
whether it believes the agent**:

| Source | Vantage |
|---|---|
| **A** | Peer-reviewed practice, grounded in the literature via Perspicacité (§3.7). |
| **B** | The literal goal text — did the agents deliver what was asked? |
| **C** | Agent narration — can the numbers and artefacts the agent *claims* be reproduced from what is on disk? |
| **D** | Mathematical invariants — probabilities in [0, 1], shape consistency, no NaNs. |
| **E** | Computational reproducibility — declared dependencies cover the imports actually used, no absolute paths, seeds set on stochastic operations. |
| **F** | Statistical fingerprint — beats a baseline, no degenerate predictions, no leakage signatures. |

Two properties of this design recur in the validation. First, **Source C is exactly the check
that the run-to-run failures of §3.6 violate**: an agent can write "1816 significant DMRs" into a
report, but Source C asks whether that number survives contact with the files on disk. Second,
mutation is **rubric-blind** — the only signal fed back to the mutator is an
`abstracted_prompt_gradient`, a code-named diagnosis that never names a claim, score, or source —
so the search cannot over-fit to a rubric vocabulary it never sees. The methylation-specific
sanity assertions of §3.6 are best understood as a domain-tuned extension of Sources C, D and F:
where the generic verifier checks that *a* number is reproducible, the §3.6 assertions check that
*this* number is biologically and arithmetically possible (a tile count cannot be smaller than the
number of significant tiles it contains).

### 3.5.5 The model configuration and the goal specification

**Models.** Mimosa is multi-model by design: distinct LLMs fill distinct roles, each set in
`config.py` and routable through OpenRouter via litellm. At the time of writing the configured
defaults are a GLM-5.1 **planner**, a Claude Opus 4.5 **workflow synthesiser** (the model that
writes the pipeline code), a DeepSeek-v4 **execution-agent** model, and a Qwen **judge** that
writes the verifier programs; generation uses `reasoning_effort = "medium"` and `max_tokens =
8192`. These are configuration fields, not hard-coded choices — any role can be repointed at
another provider — and a controlled experiment should **pin a single, fixed configuration**
across its repeated runs so that observed variance is attributable to the agent's
non-determinism rather than to a moving model target. (This pinning supersedes the earlier project
assumption of a single fixed Sonnet model: the system is genuinely multi-model, and the
experiment controls for it rather than the system embodying it.)

**The goal as the task contract.** Within a run the agent is steered by a single *goal file* — a
plain-text task specification handed in alongside the data. The goal is where the methylation task
is made concrete, and tightening it in response to observed failures is itself part of the
engineering of this thesis. Six versions exist (`tools/goals/goal_v1…goal_v6`), and their
progression is a compact record of what an LLM agent needs to be told before it analyses WGBS
data reliably:

| Goal | What it adds relative to the previous version |
|---|---|
| **v1** minimal | The bare task: from Bismark `.cov` files, call DMCs and DMRs between two groups; read group labels from a samplesheet. |
| **v2** outputs | An explicit required-output list — DMC/DMR tables, a DMC volcano, per-sample and sample-structure QC, and an append-only `run_report.txt`. |
| **v3** MCP | The hard execution constraint: **all R runs through the methylation MCP server**, never locally; author a real `.R` script and execute it; inspect large files with `head`/`zcat`, never open them whole. |
| **v4** methodology | Concrete statistics: `pipeline="bismarkCoverage"`, 10× coverage filter, trim the top 0.1 %, median normalisation, an SD pre-filter, a **paired** test with the donor as a covariate (`overdispersion="MN"`), and dual reporting thresholds (lenient \|Δβ\|≥10 %, strict ≥25 %, both q<0.05). |
| **v5** repository | A reproducible project contract: `config.yaml`, an input-detection step that emits `input_manifest.json`, numbered scripts `00_detect_inputs.py … 04_enrichment.R`, a `run_pipeline.sh` driver, and a machine-parseable `STEP_SUMMARY …` line on each script's final stdout. |
| **v6** corrected | Corrections of recurring agent errors: affirm that methylKit *does* support paired designs, fix the DMR tile width at 500 bp (not 1000), enforce the **canonical** bundled BED filenames, and add TSS-distance tables for the strict DMC set. |

The trajectory is from *what to do* (v1–v2) to *how to run it reproducibly* (v3, v5) to *exactly
which statistics, corrected against observed mistakes* (v4, v6). The dual-threshold reporting and
the paired-design instruction in particular are direct responses to the analysis requirements of
the Chapter 4 replications.

*(Table 3.3.) The goal-evolution changelog; the final version cites line ranges in each goal file.*

### 3.5.6 The workspace contract and the audit trail

**The workspace contract.** Agent and tools never exchange large objects in messages; they share
one workspace directory (configured as `workspace_dir`) and communicate through files, as
introduced in §3.1.3. A run materialises a predictable tree: the input-detection step writes
`input_manifest.json` (one record per sample: `sample_id`, `file_path`, `group`, a `treatment`
code, and capability flags), so that no downstream script hard-codes sample names or group
membership; the numbered R scripts read the manifest and `config.yaml`, write their `.rds`
intermediates and figures, and append to `run_report.txt`. This file-on-disk contract is what
makes a completed run independently re-executable — and, as §3.6 shows, also what makes its
failures externally auditable.

**The audit trail.** Because Mimosa is built for scientific use, every generation is recoverable
after the fact. For each synthesised workflow the framework persists, under
`sources/workflows/<uuid>/`: the exact executed Python (`workflow_genotype_<uuid>.py`), the
lineage and operator that produced it (`lineage_<uuid>.json`: parents and `seed | mutation |
crossover`), the exact LLM prompt that generated it (`evolution_prompt_<uuid>.md` — "same prompt +
seed = same code"), per-iteration metrics (`run_metrics.json`: wall time, cost, scores), and the
abstracted gradient. Companion tools (`memory_explorer.py`, `memory_timelapse.py`, a RAG-backed
`--memory_cli`) step through a run's full trace. The sandbox runs under explicit resource ceilings
set in `config.py` — a per-workflow runner timeout of 10 800 s (3 h), a per-agent execution
timeout of 21 600 s (6 h), and a 10 GB memory cap — and an under-set timeout is shown by the run
archive to be the operational cause of several earlier run failures.

---

## 3.6 Reliability engineering

The design choices of §§3.1–3.5 are *intended* to produce reliability: orchestration is fenced
off from execution, expertise is encoded once, artefacts are reproducible by construction, and a
deterministic verifier grades each run. This section is about the gap between intended and
observed. It does two things: it presents the concrete evidence, already sitting in the run
archive, that the unguarded system is **not** reliable run-to-run; and it specifies the
domain-specific guardrails and instrumentation this thesis introduces to close that gap.
These are the thesis's own reliability-engineering layer (§3.0), not pre-existing lab machinery.
The run-archive evidence motivates the guardrails; the guardrails are applied in the experiment
chapters; the instrumentation captures the per-run records those chapters analyse.

### 3.6.1 The motivating evidence: the same data, three different answers

The clearest motivation is in three runs that analyse the **same six input files** — the
knockout clones `clone16/20/21` against the wild-type `sbp009_1/2/3` — and each self-report
success, yet disagree at every level:

| Run | Goal / engine | Sites united | Headline call | Reported result |
|---|---|---|---|---|
| `run10` | v6 / methylKit, paired, 500 bp tiles | 15 600 476 | DMCs + DMRs | 13 212 strict DMCs (5 840 hyper / 7 372 hypo); 245 strict DMRs from 159 132 tiles |
| `run11` | v5 / methylKit, 1000 bp tiles | 22 288 905 | DMRs only | **1 816** strict DMRs (540 hyper / 1 276 hypo) |
| `run12` | v5 / DSS, smoothing | — | DML + DMR | 164 629 DMLs; 22 338 DMRs |

The divergence is not subtle: the number of "united" CpG sites differs by 6.7 million between
`run10` and `run11` (a silent consequence of the agent choosing a permissive `min.per.group = 1`
unite in one run and a strict intersect in the other), and the chosen engine, tile width, and
output granularity differ across all three. These runs are **not controlled replicates** — they
differ in goal version and method, and so they measure *method-selection instability*, not
pure run-to-run variance. But they already establish the thesis's central problem: nominally
identical instructions, executed by the same system on the same data, produce results that
differ by orders of magnitude, and the system reports all of them as successes.[^run9]

[^run9]: A naïve "5 vs 13 212 strict DMCs" comparison sometimes drawn from the folder names is
    misleading: the run reporting 5 DMCs (`run9`) analysed a *different* dataset (the CD55
    contrast), not the clone/sbp009 data. The run archive itself, in other words, needs the same
    canonicalisation discipline applied to the analyses — a small but telling lesson.

`run11` is worse than merely divergent; it is **silently wrong**, and it is the prototype for the
assertions below. Its `run_report.txt` records five consecutive failed attempts at the load/QC
step (`undefined columns selected`; `no base were united`; `ignoring SIGPIPE signal`) before one
finally "succeeds" — the agent retried with quietly different parameters and reported only the
survivor. It then states, in adjacent lines, "**Tiles tested: 22**" and "**Significant DMRs (q <
0.050, |diff| > 25.0 %): 1816**", and proceeds to annotate 1 816 regions and extract 8 593 genes
from them. Twenty-two tested tiles cannot contain 1 816 significant tiles; the number is an
artefact of a broken step, yet nothing in the run stopped, and a contradictory "STEP 2 … STATUS:
FAILED" is appended *after* the "successful" results. A reader trusting the report would carry an
impossible figure into a biological conclusion.

```
run10  (goal v6 · methylKit, paired · 500 bp tiles) — report: SUCCESS
  STAGE 1  common CpG sites after unite ........... 15 600 476
  STAGE 2  strict DMCs (|Δβ|≥25%, q<0.05) ......... 13 212   (5 840 hyper / 7 372 hypo)
           strict DMRs ............................ 245      (of 159 132 tiles tested)

run11  (goal v5 · methylKit · 1000 bp tiles) — report: SUCCESS
  STEP 1  FAILED — undefined columns selected         ┐
  STEP 1  FAILED — no base were united                │  five silent retries;
  STEP 1  FAILED — ignoring SIGPIPE signal            │  only the survivor
  STEP 1  FAILED — no base were united                │  is reported
  STEP 1  (succeeds) CpG sites after unite 22 288 905 ┘
  STEP 2  tiles tested ............................. 22         ◄─┐ 1 816 ⊄ 22:
  STEP 2  significant DMRs (q<0.05, |diff|>25%) ..... 1 816     ◄─┘ impossible
  STEP 3  DMRs annotated 1 816 · unique genes 8 593   → carried into the biology
  STEP 2  FAILED — ignoring SIGPIPE signal            → appended AFTER "success"
```

*(Figure 3.5.) Excerpts of the on-disk `run_report.txt` for two runs on the **same six input
files**. `run10` is internally coherent; `run11` hides five failed load/QC attempts, then reports
1 816 significant DMRs from 22 tested tiles — an impossibility (F2, §3.6.3) — and appends a
contradictory `FAILED` after its own "success". Both self-report success.*

### 3.6.2 Guardrail F1 — polarity / sign canonicalisation

The first guardrail addresses a defect that is invisible in any single run and corrupts every
direction-dependent comparison. The input manifest codes the knockout clones as `treatment = 0`
and the wild-type SBP009 samples as `treatment = 1`. methylKit, by convention, computes
`meth.diff` as *(group 1 − group 0)* — here **WT − KO**, the exact negation of the KO − WT
convention used by the reference study. The coding is internally consistent, so no error is
raised; but every hyper-/hypo-methylation label is flipped relative to the literature, and any
concordance metric computed naïvely against the paper would be measuring agreement with the sign
reversed. The guardrail is a single **shared scoring module** that forces all pipelines —
Mimosa's, the expert baselines, the synthetic oracle — onto one canonical KO − WT sign and
**asserts that sign against a known-direction locus** before any concordance number is computed.
This both removes the bug from the validation and supplies the experiment chapters with a
concrete example of a failure that only cross-run, externally-held ground truth can catch.

### 3.6.3 Guardrail F2 — silent-failure sanity assertions

The second guardrail turns the kind of incoherence that `run11` exhibits from an undetectable
narrative into a hard stop. After any run, a small set of post-hoc assertions is checked against
the artefacts on disk:

- `n_significant ≤ n_tested` at every level (the assertion `run11` violates: 1 816 ⊄ 22);
- `n_tiles_tested ≥ n_DMRs`;
- the count of united CpGs falls within a plausible band for the assay and genome (catching the
  permissive-versus-strict unite drift that separates `run10` from `run11`);
- all emitted coordinates lie within the chromosomes of the declared assembly.

These are deliberately the checks a domain expert performs by reflex and an over-eager agent skips.
They are the methylation-specific complement to the generic verifier's Source C/D (§3.5.4): the
verifier asks whether a claimed number is *reproducible from disk*; F2 asks whether it is
*arithmetically and biologically possible at all*. Each assertion is also a measured datapoint:
the silent-failure rate is one of the quantities the experiment chapters report.

### 3.6.4 Instrumentation

Measuring reliability requires that every run leave the same comparable record, so a thin
instrumentation layer is standardised on top of the audit trail of §3.5.6. For each run it
captures: a normalised `trace.jsonl` (the ordered sequence of tool calls and their exit codes); an
extracted **parameter vector** (the coverage filter, normalisation, engine, tile width, thresholds
the agent actually chose), so that two runs can be compared on *what they decided* and not only on
*what they produced*; **canonicalised `DMC.bed` / `DMR.bed`** files per run (sign-corrected per
F1, gene IDs mapped to stable symbols) so that DMR-interval and gene-set overlap are computed on a
common footing; **peak resident-set memory**, sampled by a process-tree poller, for the resource
profile; and a record of each run's concordance to the expert baseline. The per-run record reuses
the skeleton already present in `tools/Mimosa-AI/scripts/score_ablation.py`. Together these feed
the variance metrics used in the experiment chapters — coefficient of variation of counts, mean
pairwise Jaccard of DMR/DMC and gene sets, parameter-vector agreement, F1 against the synthetic
oracle, and the error-recovery and silent-failure rates — by which the question "is this agent
reliable?" is given numbers rather than adjectives.

---

## 3.7 Situating Mimosa in the Toolomics ecosystem

Mimosa and the two Toolomics servers are not isolated artefacts; they are part of a small family
of laboratory tools, two of which the reader should know exist because they are wired into the
system described above and because they frame the Future Work of Chapter 8 (Conclusions). They are
summarised here only to the depth needed for that purpose; neither is itself under validation in
this thesis.

**Perspicacité — literature grounding for the verifier.** Perspicacité is a local-first
retrieval-augmented-generation service for academic literature: it ingests papers from sources
such as Semantic Scholar, OpenAlex, PubMed and arXiv (via the SciLEx multi-database search layer),
indexes them with vector embeddings in a local ChromaDB store alongside BM25, and exposes the
result as MCP tools and a REST API. Its role in this work is specific and bounded: it is the
service behind **Source A** of Mimosa's verifier (§3.5.4) — the "peer-reviewed practice" vantage —
and Mimosa discovers and uses it automatically when it is running. It is named here, rather than
folded silently into the verifier, partly because it is part of the same ecosystem and partly
because two concrete fixes to it form part of this thesis's engineering contribution: making the
LLM-provider selection honour the configuration file rather than a hard-coded default, and
repairing the SciLEx adapter to load via path injection rather than assuming an installed package.

**Indicium — the claim-standardisation layer and the multi-omics bridge.** Indicium is a small,
versioned vocabulary standard for a *typed scientific claim bound to the evidence that grounds it*,
with provenance stamps, from which Pydantic models, JSON-Schema, SHACL and OWL are generated.
Around it sits an adapter framework (`indicium-adapters`) whose domain plug-ins enrich raw claims
with ontology terms; the **epigenomics** adapter handles exactly the claim types this thesis
produces (WGBS, and methylation-array assays — resolving assay names, assemblies, and probe
identifiers to controlled vocabularies), while a sibling **metabolomics** adapter does the same for
that domain. This epigenomics adapter is itself one of the thesis's contributions (§3.0): it is the
concrete point at which the methylation work plugs into the shared claim standard, and so the most
tangible piece of the multi-omics bridge that Chapter 8 develops. Indicium is not used to *run* any
analysis here — it explicitly does not call DMRs or
align reads — and so it is not part of the system under test. It is described because it is the
concrete substrate of the thesis's framing claim: methylation is positioned as the **validated
first vertical** of a system designed to extend, through a shared claim standard, toward
transcriptomics and metabolomics. The benchmark-construction toolkit AgenticScienceBuilder, which
turns published papers into machine-readable evaluation tasks against this same standard, completes
the ecosystem but is otherwise out of scope.


---

# 04_experiment1_gse263850

# Chapter 4 — Experiment 1: Replication of the GSE263850 AKAP11 Study

The central hypothesis of this thesis (§1.3) asserts that an LLM-based agent can
reproduce the principal findings of a peer-reviewed whole-genome bisulphite sequencing
study — differentially methylated regions, affected genes, and direction of effect — to a
degree comparable with an expert re-analysis of the same data. This chapter subjects that
claim to its first empirical test. The experiment takes a single published dataset,
GSE263850, and asks three questions: does the agent find the same regions, does it assign
them the correct biological direction, and does it recover the same downstream biology? A
triangulated comparison design — agent versus paper, agent versus an expert baseline, and
baseline versus paper — provides the reference frame. The baseline-versus-paper agreement
serves as the realistic ceiling against which the agent is measured, since even a careful
human re-analysis does not reproduce every detail of a published result.

The chapter reports headline concordance metrics, traces each source of divergence to
specific parameter choices, catalogues three silent defects that the agent's own validation
did not catch, and concludes with a scorecard summarising what this first experiment
contributes to the overall reliability argument. Findings that span multiple experiments
are deferred to the Discussion (Chapter 7).



## 4.2 Experimental design — the three analysis arms

The replication is conducted as three independent analyses of the identical six coverage
files, differing only in who or what chose the analysis parameters.

**Arm 1 — Published results (paper).** The expected reference: the 813 DMRs, 705 genes,
and enriched pathways reported by Farhangdoost et al. (2025). These are taken as the
target of replication, not as ground truth — the paper's own analysis is one defensible
choice of parameters among several.

**Arm 2 — Expert re-analysis (baseline).** A 531-line monolithic R script written by a
human analyst with the explicit goal of replicating the published analysis faithfully. It
uses:

- `DMLfit.multiFactor()` + `DMLtest.multiFactor()` (DSS's multi-factor interface),
- the paper's exact parameters: `smoothing = TRUE`, `p.threshold = 1e-5`, `delta = 0`,
  `dis.merge = 100`, `minlen = 50`, `minCG = 3`, `pct.sig = 0.5`,
- ≥5× per-sample coverage filter (matching the paper),
- ChIPseeker annotation with a ±100 kb TSS window,
- ReactomePA pathway enrichment with an explicit gene universe.

**Arm 3 — Agent pipeline (run23).** The Mimosa agent, given a natural-language
goal ("run a complete DSS differential methylation analysis of the AKAP11 KO dataset,
annotate and enrich, then compare to the baseline and report") and a config-driven
workspace. It operated under Goal 5 (full cycle with learning) with Quality-Diversity
evolution. The pipeline it synthesised is a five-script modular design:

- `01_load_and_qc.R` — load, coverage filter (≥10×), QC plots (PCA, heatmap, dendrogram),
- `02_differential_methylation.R` — `DMLtest()` (simple two-group), chromosome-by-chromosome
  to avoid out-of-memory failures, with `p.threshold = 0.05`, `delta = 0.25`,
  `dis.merge = 1000`,
- `03_annotate.R` — genomation-based annotation (promoter/exon/intron/intergenic + CpG
  island overlap),
- `04_enrichment.R` — GO Biological Process + KEGG enrichment via clusterProfiler,
- `validate_pipeline.R` — automated sanity checks (sample counts, p-value range, output
  file existence).

The agent's pipeline differed from the paper's in several consequential parameters, which
are analysed in §4.3. Run23 is the first agentic run in this thesis's experimental series
to complete the full analysis cycle end-to-end without crashes, OOM failures, or
simulated-data fallbacks — a trajectory documented in §3.6 and revisited in §4.6.

---

## 4.3 Results

### 4.3.1 Headline DMR counts

Table 4.1 summarises the DMR-level output of each arm.

**Table 4.1.** DMR counts and region statistics across the three arms.

| Metric | Paper | Baseline | Agent (run23) |
|---|---:|---:|---:|
| **Total DMRs** | 813 | 921 | 4,812 |
| **Hypermethylated** | 638 (78%) | 685 (74%) | 2,182 (45%) |
| **Hypomethylated** | 175 (22%) | 236 (26%) | 2,630 (55%) |
| **Associated genes** | 705 | 825 | — (gene_name bug) |
| Median region length | — | 242 bp | 285 bp |
| Mean region length | — | 293 bp | 346 bp |
| Median CpGs/region | — | 5 | 6 |
| Total bp covered | — | 270,068 | 1,665,686 |

The baseline produces 921 DMRs — a 13% overshoot of the paper's 813, within the range of
variation expected from minor implementation differences (e.g. Bioconductor version, exact
coverage at boundary CpGs). The agent produces 4,812 DMRs — a 5.9× overshoot. This
inflation is the chapter's first major finding and is traced to specific parameter
differences in §4.3.2.

### 4.3.2 Parameter analysis — the sources of divergence

Table 4.2 catalogues the parameter differences between the baseline and the agent,
alongside their impact.

**Table 4.2.** Critical parameter differences between the baseline and agent pipelines.

| Parameter | Baseline (paper values) | Agent (run23) | Impact |
|---|---|---|---|
| Coverage filter | ≥5× per sample | ≥10× in ≥1 sample | Agent retains fewer sites but with different per-sample logic |
| Statistical model | `DMLfit.multiFactor()` | `DMLtest()` (simple 2-group) | Equivalent for this single-factor design |
| `delta` (effect-size minimum) | **0** | **0.25** | Agent is stricter — requires ≥25% methylation difference |
| `p.threshold` in `callDMR` | **1e-5** (raw *p*) | **0.05** (FDR, misapplied) | **Agent is ~5,000× more permissive** |
| `dis.merge` | **100 bp** | **1,000 bp** | Agent merges regions 10× farther apart |
| `minlen` | 50 | 50 | Identical |
| `minCG` | 3 | 3 | Identical |
| `pct.sig` | 0.5 | 0.5 | Identical |

The single most consequential difference is the `p.threshold` mismatch. DSS's `callDMR()`
function expects a raw per-CpG *p*-value threshold; the agent pipeline passes its
configured FDR cutoff (0.05) into this slot. This makes the per-CpG inclusion criterion
approximately 5,000 times more permissive than the paper's `1e-5`, which is the primary
driver of the DMR count inflation. The agent's stricter effect-size filter
(`delta = 0.25` versus `delta = 0`) partially offsets this by rejecting small-effect CpGs,
but clearly does not compensate for the p-value looseness. The `dis.merge = 1000` setting
further inflates counts by merging CpGs up to 10× farther apart into single regions.

This is a semantic mismatch — the agent treated a conceptually correct FDR threshold as if
it were a raw *p*-value — and is precisely the kind of "plausible wrong answer" described
in §1.4. Its detection required the triangulated comparison design: within the agent's
output alone, the 4,812 DMRs are internally consistent and pass the pipeline's own
validation, and only the juxtaposition with the baseline and the paper reveals the
inflation.

### 4.3.3 Direction concordance — a systematic inversion

Among the 791 overlapping DMR pairs between the baseline and agent output, the direction of
effect is **100% inverted**, with zero exceptions.

**Table 4.3.** Direction concordance for overlapping DMR pairs.

| Agent label | Baseline label | Count |
|---|---|---:|
| Hypo | Hyper | 607 |
| Hyper | Hypo | 184 |
| Hyper | Hyper | 0 |
| Hypo | Hypo | 0 |

This is not biological discordance but a labelling convention difference. The baseline's
`DMLfit.multiFactor()` computes coefficients as *treatment − control* (KO − WT), so a
positive `areaStat` indicates higher methylation in the KO — hypermethylation. The agent's
`DMLtest()` was called as `DMLtest(group1 = ctrl, group2 = treat)`, so its `diff.Methy`
represents *control − treatment* (WT − KO) — flipping the sign. The 100% inversion
confirms that the two pipelines agree on the biology for every shared region; the labels
are simply opposite.

This finding motivated the sign-canonicalisation library described in §3.6: without
standardising the direction convention *before* computing any concordance score, an
analysis that agreed perfectly on the biology would appear to disagree perfectly on
direction. The canonicalisation forces all comparison arms onto a single convention
(KO − WT = positive → hypermethylation) before any metric is computed.

### 4.3.4 Overlap and concordance

Having noted the direction inversion, the analysis turns to positional concordance —
whether the two pipelines identify the same genomic loci as differentially methylated.

**Table 4.4.** Overlap between the baseline and agent DMR call sets.

| Comparison | Result |
|---|---|
| Baseline DMRs recovered by agent | **791 / 921 (85.9%)** |
| Agent DMRs supported by baseline | 764 / 4,812 (15.9%) |
| Agent-only DMRs (no baseline match) | 4,048 (84.1%) |

The asymmetry is the expected consequence of the call-set size difference: the baseline's
smaller, higher-confidence set is almost entirely (86%) recovered within the agent's larger
set, while the reverse is naturally much lower. This pattern — high recall, low precision
relative to the baseline — is the signature of a permissive threshold.

More informatively, the quality of the agent's calls correlates with their corroboration.

**Table 4.5.** Properties of agent DMRs that overlap vs. do not overlap the baseline.

| Property | Overlapping (n = 764) | Non-overlapping (n = 4,048) |
|---|---:|---:|
| Median |areaStat| | 56.8 | 24.7 |
| Median nCG | 7 | 6 |
| Median region length | 372 bp | 274 bp |
| Median baseline overlap | 78% | — |

The agent's **strongest calls** — those with the largest effect sizes, most CpGs, and
broadest regions — are disproportionately the ones confirmed by the baseline. This
indicates that the agent's internal ranking of its calls is sound; the problem is the
threshold at which the list is cut, not the ranking above it.

---

## 4.4 Gene recovery and biological concordance

### 4.4.1 Gene-level recovery

Gene-level concordance is assessed for the paper's gold-standard loci — genes with
convergent DMR + H3K27ac + DEG evidence — and for the top hypermethylated hits.

**Table 4.6.** Recovery of key genes across analysis arms.

| Gene | Paper status | Baseline | Agent (run23) |
|---|---|---|---|
| **IRX2** | Gold standard (DMR + H3K27ac + DEG) | ✅ Found (Hyper; 3'UTR/Promoter/Intron) | ✅ Found (via enrichment re-overlap) |
| **CLEC19A** | Gold standard | ❌ Not found | ❌ Not found |
| **KANK1** | Gold standard | ❌ Not found | ❌ Not found |
| OTX1 | Top hypermethylated | ✅ Found (Hyper; Exon/Intergenic) | ✅ Found (via enrichment) |
| NR2E1 | Top hypermethylated | ✅ Found (Hyper; 5'UTR) | ✅ Found (via enrichment) |
| PAX7 | Top hypermethylated | ✅ Found (Hyper; Intergenic) | Unknown (gene_name empty) |
| ENPP2 | Top hypermethylated | ✅ Found (Hyper; Promoter) | Unknown (gene_name empty) |
| CCDC177 | Top hypomethylated | ✅ Found (Hyper — contradicts paper) | ✅ Found (via enrichment) |
| DMRTA2 | ORA-enriched | ❌ Missing from baseline | ✅ Found (via enrichment) |

Two patterns emerge. First, neither the baseline nor the agent recovers *CLEC19A* or
*KANK1* — two of the paper's three gold-standard genes. This likely reflects a real
methodological difference: the paper's gene-association strategy (±100 kb from TSS) links
distant DMRs to genes that a direct-overlap annotation would not capture, and these two
genes may fall in that gap. That neither arm finds them suggests the ceiling for gene
recovery under direct-overlap annotation is below 100%, which sets an honest upper bound
for the agent comparison.

Second, the agent's enrichment step (`04_enrichment.R`) independently re-computes DMR–gene
overlaps and *does* recover key genes like *IRX2*, *NR2E1*, *CCDC177*, and *DMRTA2* — but
because the `gene_name` column in the annotated DMR output is empty for all 4,812 rows (a
confirmed annotation bug — see §4.7), these genes cannot be traced back to specific DMR
coordinates without re-running the annotation step. This reduces the utility of the
agent's output for gene-level biological interpretation.

### 4.4.2 Enrichment concordance — biological pathways

Despite the different enrichment frameworks — Reactome (baseline) versus GO + KEGG
(agent) — and the different gene sets (305 symbols from ±100 kb TSS versus 2,444 Entrez
IDs from direct overlap), both analyses converge on the same broad biological themes.

**Agent's top GO Biological Process terms:**

1. Pattern specification process (*p*~adj~ = 4.37 × 10^-20^)
2. Embryonic organ development (*p*~adj~ = 1.35 × 10^-16^)
3. Regionalization (*p*~adj~ = 1.20 × 10^-15^)
4. Skeletal system development (*p*~adj~ = 7.58 × 10^-15^)

**Agent's top KEGG pathways:**

1. Neuroactive ligand–receptor interaction (*p*~adj~ = 3.00 × 10^-7^)
2. Calcium signalling pathway (*p*~adj~ = 1.89 × 10^-5^)
3. Axon guidance (*p*~adj~ = 6.80 × 10^-5^)

Both pipelines highlight neural and developmental pathways, which is biologically
consistent with the study's context — *AKAP11* knockout in iPSC-derived cortical neurons,
a model for bipolar disorder and schizophrenia. The enrichment concordance is arguably the
most robust form of agreement between the arms, because pathway-level results are buffered
against individual gene-level differences by the aggregation inherent in enrichment
analysis.

Two caveats apply. First, the agent's enrichment used the default gene universe (all
annotated genes) rather than an explicit universe of genes tested, which inflates
enrichment significance (a known over-representation analysis pitfall). Second, the agent's
gene set is derived from 19,525 overlapping RefSeq transcripts rather than the 705 genes
in the paper, so the denominator is very different; the fact that the top terms still
converge on neural/developmental biology is meaningful precisely because it survives this
inflation.

---

## 4.5 Genomic context and chromosome distribution

The distribution of DMRs across genomic compartments is broadly similar between the arms.

**Table 4.7.** Genomic context distribution of DMRs.

| Category | Baseline | Agent |
|---|---:|---:|
| Intron | 50.7% | 46.9% |
| Intergenic | 21.9% | 35.6% |
| Exon | 12.6% | 10.7% |
| Promoter | 10.3% | 6.9% |
| 3'UTR | 3.6% | — |
| 5'UTR | 0.9% | — |

The agent's higher intergenic share (35.6% vs. 21.9%) is consistent with permissive
calling picking up weaker signals in regions far from annotated genes. The proportional
similarity across the remaining categories indicates that the extra agent DMRs are spread
across all genomic compartments rather than concentrated in one anomalous category — there
is no evidence of a systematic annotation artefact.

Chromosomal distribution is likewise broadly concordant, with two notable deviations: the
agent calls 2× the relative share of chrX DMRs (3.4% vs. 1.5%) and identifies 8 chrY DMRs
where the baseline finds none. Both are consistent with a permissive threshold lowering the
bar everywhere, including on sex chromosomes where the effective sample size is halved (all
samples are male).

---

## 4.6 Agent evolutionary trajectory

Run23 was executed under Mimosa's Goal 5 (full cycle with learning), using the
Quality-Diversity (QD) evolutionary algorithm. Six iterations were evaluated:

| Iteration | Kind | Quality score | Archive size | Notes |
|---|---|---:|---:|---|
| 1 | Seed | **0.8601** (best) | 1 | Produced the final pipeline |
| 2 | Mutation | 0.7259 | 2 | Explored but did not improve |
| 3 | Mutation | — (not archived) | 2 | |
| 4 | Mutation | 0.7163 | 3 | |
| 5 | Mutation | 0.6899 | 4 | |
| 6 | Mutation | — | 4 | Budget doubled due to plateau |

The seed iteration scored highest, and subsequent mutations explored diversity without
improving quality — a classic exploration-without-improvement pattern in which the initial
synthesis happened to be the best. The system detected increasing plateau (0% → 50%) and
declining success rate (50% → 25%), responding by increasing "boldness" and doubling the
agent budget.

Twenty-one learned patterns were accumulated during the process, covering failure modes
from earlier runs: OOM avoidance (chromosome-by-chromosome processing), DSS p-value
validation (abort if any *p* > 1, guarding against column-swap bugs), and graceful
degradation (skip enrichment rather than crash). That the verifier system nonetheless
missed the p.threshold semantics, direction inversion, and empty gene_name — precisely the
defects that required external comparison to detect — exposes a gap in the automated
verification coverage that the thesis returns to in the Discussion (Chapter 7).

---

## 4.7 Identified defects

Three specific defects in the agent's pipeline were identified through the triangulated
comparison. All three are *silent*: the pipeline completes successfully, passes its own
validation, and produces outputs that are internally coherent. Their detection required
external comparison — a fact that connects directly to the thesis's claim that capability
is necessary but not sufficient (§1.4) and that triangulated validation against known
references is essential for scientific trust.

**Defect 1: p.threshold / FDR mismatch (severity: high).** As detailed in §4.3.2, the
agent feeds an FDR cutoff (0.05) into DSS's `callDMR(p.threshold = ...)`, which expects a
raw per-CpG *p*-value. This is the primary cause of the 5.9× DMR inflation.

**Defect 2: Direction inversion (severity: medium).** The agent's `DMLtest()` group-order
convention produces `diff.Methy` with opposite sign from the baseline (§4.3.3). While
internally consistent, any biological conclusion about hyper- versus hypomethylation drawn
directly from the agent's labels would be backwards.

**Defect 3: Empty gene_name column (severity: medium).** In `03_annotate.R`, the
`gene_name` vectors are initialised to empty strings and never assigned gene symbols after
annotation. The genomation-based annotation correctly produces genomic-context categories
(promoter/exon/intron/intergenic) and CpG-island context, but the gene-symbol column
remains blank for all 4,812 DMRs. The pipeline's validation script does not check
`gene_name` completeness, so the bug passes silently.

These defects are consequential for the reliability assessment because they instantiate the
failure mode that the hypothesis anticipates: plausible, internally consistent outputs that
are biologically misleading. They cannot be caught by the agent's own verification loop,
and their nature — a semantic API mismatch, a convention difference, and a silent
initialisation bug — represents the category of errors most resistant to automated
detection.

---

## 4.8 Chapter summary

Table 4.8 brings together the comparison across all evaluated dimensions.

**Table 4.8.** Experiment 1 summary scorecard.

| Dimension | Baseline vs. paper | Agent vs. paper | Agent vs. baseline |
|---|---|---|---|
| **DMR count fidelity** | 921 vs. 813 (1.1×) | 4,812 vs. 813 (5.9×) | 5.2× more |
| **Direction** | Correct convention | Inverted (100%) | Inverted (100%) |
| **Gene recovery** | 4/9 key genes found | 4/9 via enrichment | 86% positional overlap |
| **Pathway themes** | Neural/developmental ✅ | Neural/developmental ✅ | Convergent |
| **Genomic context** | Proportionally similar | Proportionally similar | Higher intergenic |
| **Silent defects** | None identified | 3 (p-threshold, direction, gene_name) | — |

The baseline achieves close fidelity to the paper (within 13% on DMR count, correct
direction, same key genes). The agent recovers the biological signal — 86% of the
baseline's DMRs, the same pathway themes, and the same key genes through its enrichment
step — but does so at the cost of a 5.9× inflated call set, inverted direction labels, and
a broken gene-annotation column. Its engineering qualities — modular scripts, config-driven
parameters, OOM protection, automated validation — are genuine, but the three silent
defects demonstrate that engineering quality does not guarantee biological correctness.

What Experiment 1 contributes to the hypothesis is a clear separation of capability from
reliability. On the capability side, the evidence is affirmative: the agent finds the
signal (85.9% positional recall of the baseline), ranks its calls correctly (the strongest
are the most corroborated), and converges on the correct biology (neural and developmental
pathways, key genes recovered via enrichment). On the reliability side, the evidence is
cautionary: three silent defects — a semantic parameter mismatch, a direction-convention
error, and an empty annotation column — would each produce misleading biological
conclusions if taken at face value, and none would have been detected without the
triangulated comparison against the baseline and the published analysis.

This outcome supports the framing introduced in §1.4: that an agent can demonstrate
statistical and biological competence while still harbouring errors that require external
reference points to detect. Whether the same pattern — genuine capability alongside silent
defects — recurs in a different dataset, organism, and experimental context is the question
addressed in the next experiment (Chapter 5). The cross-experiment synthesis, including
whether these defects are systematic or dataset-specific and what they imply for the
practical deployment of agentic analysis pipelines, is taken up in the Discussion
(Chapter 7).


---

# 04_validation1_replication

# Chapter 4 — Validation I: Replication

> **Draft note (remove before submission).** This chapter presents the real-data replication
> studies. Study A (GSE263850, human) is drafted from completed run23 results. Study B
> (GSE214232, mouse) is outlined but awaits experimental completion. Wording that anticipates
> an overall verdict is held open until both studies and the synthetic/reliability results of
> Chapter 5 are in hand.

This chapter presents the first test of the hypothesis stated in §1.3: whether the agent, given
the identical input data of a peer-reviewed WGBS study, recovers its principal findings —
differentially methylated regions, affected genes, and direction of effect — to a degree
comparable with an expert re-analysis of the same data. Two studies are reported: **Study A**,
a human heterozygous *AKAP11* knockout, and **Study B**, a mouse *Dnmt3a* conditional
knockout. Each is scored as a triangle — agent versus published results, agent versus an expert
re-analysis run ourselves (the *baseline*), and baseline versus published — so that the
expert-versus-published agreement serves as the realistic ceiling against which the agent is
measured.

The chapter is structured per study. For each, we describe the dataset, the three arms (paper,
baseline, agent), and the concordance metrics. §4.3 draws cross-study observations, and §4.4
summarises where the agent's replication stands relative to the hypothesis.



## 4.2 Study B — Mouse *Dnmt3a* conditional knockout (GSE214232)

> **Placeholder.** Study B is outlined here and will be drafted when the experimental run is
> complete.

### 4.2.1 Dataset and biological context

The data for Study B are drawn from [citation to be confirmed], deposited as GSE214232. The
study investigated methylation changes in a mouse conditional knockout of *Dnmt3a*, a DNA
methyltransferase. The experimental design, expected DMR counts, and key genes will be stated
here once the dataset is fully characterised.

### 4.2.2 Experimental design

The same three-arm triangle (paper, baseline, agent) will be applied. The mouse genome (mm10)
tests the agent's portability to a different assembly and organism, exercising the config-driven
design described in §3.3 and §3.4.

### 4.2.3–4.2.12 Results

To be completed.

---

## 4.3 Cross-study observations

> **Placeholder.** This section will be drafted once both Studies A and B are complete. It will
> address:
>
> - Whether the agent's error modes (p-threshold mismatch, direction inversion, annotation
>   bugs) recur across datasets or are dataset-specific.
> - Whether the 85–90% positional recall of the baseline's DMRs is consistent across species
>   and assemblies.
> - Whether the agent's pathway-level convergence with published results is robust across
>   different biological contexts.
> - The role of the skill's engine-selection logic (§3.4) in Study B, where the replicate
>   count may differ.

---

## 4.4 Chapter summary — where does replication stand?

Study A provides a mixed but informative answer to **H1 (concordance)**. On the positive side:

- The agent pipeline recovers **86% of the baseline's DMR set** positionally, and its
  strongest calls are the ones most corroborated by the expert analysis — the ranking is sound.
- The agent converges on the **same neural/developmental biological pathways** as both the
  paper and the baseline, even through different enrichment frameworks and gene sets.
- Key published genes (*IRX2*, *OTX1*, *NR2E1*, *DMRTA2*) are independently rediscovered by
  the agent's enrichment step.
- Run23 is a **substantial improvement** over all prior agentic runs (15–20), being the first
  to complete the full cycle without crashes, OOM failures, or simulated-data fallbacks.

On the negative side:

- The agent produces a **5.9× inflated DMR call set**, driven by a semantic parameter mismatch
  that would not have been caught without external comparison.
- Three **silent defects** — all internally consistent, all passing the pipeline's own
  validation — would produce misleading biological conclusions if taken at face value.
- Gene-level annotation is **broken**, reducing the output's utility for downstream
  interpretation.

The honest conclusion for Study A is that the agent demonstrates genuine *capability* — it
finds the signal, ranks it correctly, and converges on the right biology — but not yet
*reliability*: the three silent defects mean the output cannot be used directly for biological
interpretation without expert review. Whether the skill and tool guardrails described in §3.4
and §3.6 can close this gap, and whether these defects recur in Study B, are the questions that
the remainder of the validation (§4.2, Chapter 5) addresses.


---

# 05_experiment2_gse214232

# Chapter 5 — Experiment 2: Replication of the GSE214232 Dnmt3a Study

<!-- This chapter follows the modular experiment template. Each section mirrors Ch.4. -->

This chapter presents the second test of the hypothesis: whether the agent replicates the
principal findings of a published WGBS study in a different organism. Where Experiment 1
(Chapter 4) demonstrated the agent's behaviour on human data (GSE263850, *AKAP11*
heterozygous knockout), Experiment 2 applies the identical evaluation framework to a mouse
dataset — GSE214232, a conditional knockout of *Dnmt3a*, a DNA methyltransferase — thereby
testing cross-species generalisation of the agent's analytical capability.

The experimental design is the same three-arm triangle used in Chapter 4: the published results
serve as the replication target, an expert re-analysis provides the realistic ceiling, and the
agent's output is scored against both. The mouse genome (mm10) exercises the system's
portability across assemblies and organisms, including the config-driven annotation described
in §3.3.

---

## 5.1 Dataset and biological context

<!-- To be completed when the dataset is fully characterised. -->
<!-- Key information to include:
     - Citation for the original study
     - Biological question (Dnmt3a conditional KO)
     - Experimental design (groups, sample counts)
     - Published analysis parameters and key findings (DMR counts, key genes)
     - Data availability (GEO accession, file format)
-->

## 5.2 Experimental design

The three analysis arms are:

**Arm 1 — Published results.** The DMR counts, associated genes, and enriched pathways
reported in the original publication.

**Arm 2 — Expert re-analysis (baseline).** A human-authored R script replicating the
published analysis parameters as faithfully as possible.

**Arm 3 — Agent pipeline.** The Mimosa agent, given the same coverage files and a
natural-language goal, synthesising and executing its own analysis.

<!-- Detail the specific goal version, agent configuration, and any mm10-specific considerations. -->

## 5.3 Results

<!-- To be completed. Subsections will include:
     - Headline DMR counts across the three arms
     - Parameter analysis (as in §4.3)
     - Direction labelling assessment
     - Overlap and concordance metrics
-->

## 5.4 Gene recovery and biological concordance

<!-- To be completed. -->

## 5.5 Genomic context distribution

<!-- To be completed. -->

## 5.6 Identified defects

<!-- To be completed. Assess whether the defects from Experiment 1 recur. -->

## 5.7 Chapter summary

<!-- To be completed. Address:
     - What Experiment 2 contributes to the hypothesis
     - Whether error modes from Experiment 1 recur or are dataset-specific
     - Whether cross-species generalisation holds
     - Forward reference to Discussion (Ch.7)
-->


---

# 06_experiment3_simulated_fastq

# Chapter 6 — Experiment 3: End-to-End Pipeline with Simulated FASTQ

<!-- This chapter follows the modular experiment template. -->

This chapter presents the third and final test of the hypothesis: whether the agent can execute
the complete WGBS analysis pipeline — from raw sequencing reads through alignment and
methylation extraction to differential methylation calling — without human intervention.
Where Experiments 1 and 2 (Chapters 4 and 5) validated the agent's downstream analytical
capability starting from pre-existing coverage files, Experiment 3 exercises the full system
architecture described in Chapter 3, including MCP Server A (Nextflow / nf-core/methylseq) for
the upstream alignment stage.

The experiment uses simulated FASTQ files rather than real sequencing data. This choice is
driven by two considerations. First, the computational cost of aligning full real human WGBS
data was infeasible on the available hardware (§3.2). Second, simulated data provides a
controlled setting in which the pipeline's end-to-end execution can be verified independently
of biological complexity. The objective is not to benchmark sensitivity or specificity against
ground truth, but to demonstrate that the agent can autonomously orchestrate the entire
pipeline — input preparation, alignment, methylation extraction, differential testing, and
biological interpretation — producing a coherent and complete analysis from raw reads.

---

## 6.1 Simulated data generation

<!-- To be completed. Sections to address:
     - Tool used for FASTQ simulation (e.g., Sherman, ART, or custom)
     - Reference genome used (reduced or full)
     - Number of samples, groups, and simulated read depth
     - Any methylation patterns embedded in the simulation
-->

## 6.2 Experimental design

<!-- To be completed. Sections to address:
     - Agent configuration (goal version, execution mode)
     - Server A configuration (local backend, Singularity, resource limits)
     - Server B configuration (engine choice)
     - Expected pipeline stages and outputs
     - Success criteria: what constitutes a successful end-to-end run?
-->

## 6.3 Pipeline execution

<!-- To be completed. Sections to address:
     - Server A stage: samplesheet preparation, nf-core/methylseq execution
     - Coverage file generation
     - Server B stage: loading, QC, differential testing, annotation
     - Agent's decision trace (what the agent chose at each stage)
     - Wall time, resource usage
-->

## 6.4 Results

<!-- To be completed. Sections to address:
     - Was the pipeline completed end-to-end without manual intervention?
     - Output files produced
     - QC metrics from alignment and methylation extraction
     - DMR/DMC calls produced
     - Any errors, retries, or agent interventions
-->

## 6.5 Identified issues

<!-- To be completed. Sections to address:
     - Any failures or workarounds during execution
     - Parameter choices the agent made for the upstream stage
     - Comparison of agent's alignment choices with best practices
-->

## 6.6 Chapter summary

<!-- To be completed. Address:
     - What Experiment 3 demonstrates about the hypothesis
     - The significance of full-pipeline capability
     - Honest scope: simulated data, reduced scale
     - Forward reference to Discussion (Ch.7)
-->


---

# 07_discussion

# Chapter 7 — Discussion

This chapter synthesises the findings of Experiments 1–3 (Chapters 4–6), evaluates them
against the hypothesis stated in §1.3, and considers the strengths, limitations, and threats
to validity of the work.

---

## 7.1 Summary of experimental findings

<!-- To be completed after Chapters 4–6 are finalised. Synthesise across experiments:
     - Concordance achieved in the two replications
     - Pipeline capability demonstrated in Experiment 3
     - Recurring vs. experiment-specific error modes
     - The role of the skill and tool architecture in observed performance
-->

## 7.2 Evaluation against the hypothesis

<!-- To be completed. Address each facet of the hypothesis:
     - Can the agent replicate published findings? (Exp.1, Exp.2)
     - Does this generalise across organisms? (Exp.1 vs. Exp.2)
     - Can the agent execute the full pipeline? (Exp.3)
     - Are results concordant with expert analyses?
     - State the verdict explicitly: supported, partially supported, or not supported.
-->

## 7.3 The role of silent defects

<!-- To be completed. Discuss:
     - The pattern of silent defects across experiments
     - What external comparison reveals that internal validation misses
     - Implications for trust in agent-produced scientific analyses
     - The gap between capability and reliability
-->

## 7.4 Strengths of the approach

<!-- To be completed. Consider:
     - Triangulated evaluation design
     - Use of a domain with knowable correct answers
     - Sign canonicalisation and post-hoc assertions
     - Modular, reproducible system design
-->

## 7.5 Limitations

<!-- To be completed. Address honestly:
     - Compute constraints (no cloud, coverage-file starting point for Exp.1/2)
     - Simulated vs. real data for Exp.3
     - Single agent framework (Mimosa) — generalisability?
     - No formal false-positive calibration study
     - No formal reliability/reproducibility study (repeated runs)
     - Limited to two datasets and one domain
-->

## 7.6 Threats to validity

<!-- To be completed. Consider:
     - Internal validity: parameter differences between arms
     - External validity: generalisability beyond WGBS, beyond Mimosa
     - Construct validity: what "concordance" measures vs. what practitioners need
-->


---

# 08_bibliography

# Chapter 8 — Bibliography

> **Working bibliography seed.** This file holds the BibTeX entries backing the `[@key]` citations
> used in the Markdown chapters; at Pandoc time it is exported to a `references.bib` and rendered
> by `citeproc`. **Every entry must be verified against the primary source before submission** —
> author lists, years, venues, volume/pages and DOIs were drafted from working knowledge and are
> not yet checked. Each entry carries a `note` with its status:
>
> - `STATUS: confident` — a well-known landmark paper; verify exact volume/pages/DOI only.
> - `STATUS: VERIFY` — recent or fast-moving source (agent / MCP / benchmark literature); confirm
>   it exists, get the canonical citation, and replace if superseded. **Do not cite as final.**
>
> Run a dedicated literature-verification pass (web search / reference manager) over §2.4–2.5
> citations especially — they are the knowledge-cutoff-sensitive ones flagged in the plan.

## Methylation biology & WGBS (§2.1)

```bibtex
@article{bird2002,
  author  = {Bird, Adrian},
  title   = {{DNA} methylation patterns and epigenetic memory},
  journal = {Genes \& Development},
  year    = {2002},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{jones2012,
  author  = {Jones, Peter A.},
  title   = {Functions of {DNA} methylation: islands, start sites, gene bodies and beyond},
  journal = {Nature Reviews Genetics},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{frommer1992,
  author  = {Frommer, Marianne and McDonald, Louise E. and Millar, Douglas S. and others},
  title   = {A genomic sequencing protocol that yields a positive display of 5-methylcytosine residues in individual {DNA} strands},
  journal = {Proceedings of the National Academy of Sciences (PNAS)},
  year    = {1992},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{lister2009,
  author  = {Lister, Ryan and Pelizzola, Mattia and Dowen, Robert H. and others},
  title   = {Human {DNA} methylomes at base resolution show widespread epigenomic differences},
  journal = {Nature},
  year    = {2009},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{cokus2008,
  author  = {Cokus, Shawn J. and Feng, Suhua and Zhang, Xiaoyu and others},
  title   = {Shotgun bisulphite sequencing of the {Arabidopsis} genome reveals {DNA} methylation patterning},
  journal = {Nature},
  year    = {2008},
  note    = {STATUS: VERIFY — confirm this is the intended WGBS-origin cite; verify details}
}
```

## Alignment & pipelines (§2.2)

```bibtex
@article{krueger2011,
  author  = {Krueger, Felix and Andrews, Simon R.},
  title   = {Bismark: a flexible aligner and methylation caller for {Bisulfite-Seq} applications},
  journal = {Bioinformatics},
  year    = {2011},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ditommaso2017,
  author  = {Di Tommaso, Paolo and Chatzou, Maria and Floden, Evan W. and others},
  title   = {Nextflow enables reproducible computational workflows},
  journal = {Nature Biotechnology},
  year    = {2017},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ewels2020,
  author  = {Ewels, Philip A. and Peltzer, Alexander and Fillinger, Sven and others},
  title   = {The {nf-core} framework for community-curated bioinformatics pipelines},
  journal = {Nature Biotechnology},
  year    = {2020},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
```

## Differential methylation (§2.3)

```bibtex
@article{akalin2012,
  author  = {Akalin, Altuna and Kormaksson, Matthias and Li, Sheng and others},
  title   = {methylKit: a comprehensive {R} package for the analysis of genome-wide {DNA} methylation profiles},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{feng2014,
  author  = {Feng, Hao and Conneely, Karen N. and Wu, Hao},
  title   = {A {Bayesian} hierarchical model to detect differentially methylated loci from single nucleotide resolution sequencing data},
  journal = {Nucleic Acids Research},
  year    = {2014},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{wu2015,
  author  = {Wu, Hao and Xu, Tianlei and Feng, Hao and others},
  title   = {Detection of differentially methylated regions from whole-genome bisulfite sequencing data without replicates},
  journal = {Nucleic Acids Research},
  year    = {2015},
  note    = {STATUS: VERIFY — confirm author list/vol/pages/DOI}
}
@article{park2016,
  author  = {Park, Yongseok and Wu, Hao},
  title   = {Differential methylation analysis for {BS-seq} data under general experimental design},
  journal = {Bioinformatics},
  year    = {2016},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{hansen2012,
  author  = {Hansen, Kasper D. and Langmead, Benjamin and Irizarry, Rafael A.},
  title   = {{BSmooth}: from whole genome bisulfite sequencing reads to differentially methylated regions},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{benjamini1995,
  author  = {Benjamini, Yoav and Hochberg, Yosef},
  title   = {Controlling the false discovery rate: a practical and powerful approach to multiple testing},
  journal = {Journal of the Royal Statistical Society: Series B},
  year    = {1995},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{robinson2014,
  author  = {Robinson, Mark D. and Kahraman, Abdullah and Law, Charity W. and others},
  title   = {Statistical methods for detecting differentially methylated loci and regions},
  journal = {Frontiers in Genetics},
  year    = {2014},
  note    = {STATUS: VERIFY — confirm venue/author list/details}
}
```

## LLMs, agents, tool use & MCP (§2.4)

```bibtex
@inproceedings{vaswani2017,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title     = {Attention is all you need},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2017},
  note      = {STATUS: confident — verify}
}
@inproceedings{brown2020,
  author    = {Brown, Tom B. and Mann, Benjamin and Ryder, Nick and others},
  title     = {Language models are few-shot learners},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@inproceedings{wei2022,
  author    = {Wei, Jason and Wang, Xuezhi and Schuurmans, Dale and others},
  title     = {Chain-of-thought prompting elicits reasoning in large language models},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2022},
  note      = {STATUS: confident — verify}
}
@inproceedings{yao2023,
  author    = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and others},
  title     = {{ReAct}: Synergizing reasoning and acting in language models},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{schick2023,
  author    = {Schick, Timo and Dwivedi-Yu, Jane and Dess{\`i}, Roberto and others},
  title     = {{Toolformer}: Language models can teach themselves to use tools},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{lewis2020,
  author    = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and others},
  title     = {Retrieval-augmented generation for knowledge-intensive {NLP} tasks},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@misc{mcp2024,
  author       = {{Anthropic}},
  title        = {Introducing the {Model Context Protocol}},
  year         = {2024},
  howpublished = {\url{https://www.anthropic.com/news/model-context-protocol}},
  note         = {STATUS: VERIFY — confirm canonical citation/spec URL and access date}
}
```

## Agents for science & reliability (§2.5)

```bibtex
@article{boiko2023,
  author  = {Boiko, Daniil A. and MacKnight, Robert and Kline, Ben and Gomes, Gabe},
  title   = {Autonomous chemical research with large language models},
  journal = {Nature},
  year    = {2023},
  note    = {STATUS: VERIFY — (Coscientist) confirm author list/vol/pages/DOI}
}
@article{bran2024,
  author  = {M. Bran, Andres and Cox, Sam and Schilter, Oliver and others},
  title   = {Augmenting large language models with chemistry tools},
  journal = {Nature Machine Intelligence},
  year    = {2024},
  note    = {STATUS: VERIFY — (ChemCrow) confirm author list/year/vol/pages/DOI}
}
@misc{lu2024,
  author = {Lu, Chris and Lu, Cong and Lange, Robert Tjarko and others},
  title  = {The {AI} {Scientist}: Towards fully automated open-ended scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — (Sakana AI) confirm arXiv id/author list}
}
@article{ji2023,
  author  = {Ji, Ziwei and Lee, Nayeon and Frieske, Rita and others},
  title   = {Survey of hallucination in natural language generation},
  journal = {ACM Computing Surveys},
  year    = {2023},
  note    = {STATUS: VERIFY — confirm vol/pages/DOI}
}
@misc{scienceagentbench,
  author = {Chen, Ziru and others},
  title  = {{ScienceAgentBench}: Toward rigorous assessment of language agents for data-driven scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — confirm authors/arXiv id/year (referenced by the Mimosa benchmark suite)}
}
@misc{paperbench,
  author = {{OpenAI}},
  title  = {{PaperBench}: Evaluating {AI}'s ability to replicate {AI} research},
  year   = {2025},
  note   = {STATUS: VERIFY — confirm authors/canonical citation}
}
```

## The system under study

```bibtex
@article{legrand2026,
  author  = {Legrand, Martin and Jiang, Tao and Feraud, Matthieu and Navet, Benjamin
             and Taghzouti, Yousouf and Gandon, Fabien and Dumont, Elise and Nothias, Louis-F{\'e}lix},
  title   = {Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research},
  journal = {arXiv preprint arXiv:2603.28986},
  year    = {2026},
  note    = {STATUS: VERIFY — citation taken from the Mimosa README; confirm arXiv id once public}
}
```


---

# 08_conclusions

# Chapter 8 — Conclusions and Future Work

## 8.1 Contributions

<!-- To be completed. List the concrete contributions:
     1. The first rigorous validation of an LLM agent on WGBS differential methylation analysis
     2. Two MCP tool servers (Nextflow/methylseq runner, R/Bioconductor methylation runner)
     3. The methylation skill encoding domain expertise as a declarative document
     4. Goal specification and its six-version evolution
     5. Sign-canonicalisation library and post-hoc sanity assertions
     6. The epigenomics claim adapter for Indicium
     7. Two fixes to the Perspicacité literature service
-->

## 8.2 Conclusions

<!-- To be completed. State the main conclusions:
     - What the experiments demonstrate about the hypothesis
     - The gap between capability and reliability
     - The value of measurement against knowable truth
     - Practical implications: when can (and when should) an LLM agent be trusted?
-->

## 8.3 Future work

<!-- To be completed. Develop:
     - Multi-omics extension: transcriptomics and metabolomics via the same infrastructure
     - Formal reproducibility study: repeated identical runs with controlled ablation
     - Synthetic ground-truth benchmark: calibration of false-discovery rates
     - Cloud-scale alignment: exercising Server A on full real WGBS via Seqera/AWS
     - Agent self-correction: using the post-hoc assertions as feedback during the run
     - Broader agent evaluation: other domains with knowable correct answers
-->


---

# 09_bibliography

# Chapter 8 — Bibliography

> **Working bibliography seed.** This file holds the BibTeX entries backing the `[@key]` citations
> used in the Markdown chapters; at Pandoc time it is exported to a `references.bib` and rendered
> by `citeproc`. **Every entry must be verified against the primary source before submission** —
> author lists, years, venues, volume/pages and DOIs were drafted from working knowledge and are
> not yet checked. Each entry carries a `note` with its status:
>
> - `STATUS: confident` — a well-known landmark paper; verify exact volume/pages/DOI only.
> - `STATUS: VERIFY` — recent or fast-moving source (agent / MCP / benchmark literature); confirm
>   it exists, get the canonical citation, and replace if superseded. **Do not cite as final.**
>
> Run a dedicated literature-verification pass (web search / reference manager) over §2.4–2.5
> citations especially — they are the knowledge-cutoff-sensitive ones flagged in the plan.

## Methylation biology & WGBS (§2.1)

```bibtex
@article{bird2002,
  author  = {Bird, Adrian},
  title   = {{DNA} methylation patterns and epigenetic memory},
  journal = {Genes \& Development},
  year    = {2002},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{jones2012,
  author  = {Jones, Peter A.},
  title   = {Functions of {DNA} methylation: islands, start sites, gene bodies and beyond},
  journal = {Nature Reviews Genetics},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{frommer1992,
  author  = {Frommer, Marianne and McDonald, Louise E. and Millar, Douglas S. and others},
  title   = {A genomic sequencing protocol that yields a positive display of 5-methylcytosine residues in individual {DNA} strands},
  journal = {Proceedings of the National Academy of Sciences (PNAS)},
  year    = {1992},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{lister2009,
  author  = {Lister, Ryan and Pelizzola, Mattia and Dowen, Robert H. and others},
  title   = {Human {DNA} methylomes at base resolution show widespread epigenomic differences},
  journal = {Nature},
  year    = {2009},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{cokus2008,
  author  = {Cokus, Shawn J. and Feng, Suhua and Zhang, Xiaoyu and others},
  title   = {Shotgun bisulphite sequencing of the {Arabidopsis} genome reveals {DNA} methylation patterning},
  journal = {Nature},
  year    = {2008},
  note    = {STATUS: VERIFY — confirm this is the intended WGBS-origin cite; verify details}
}
```

## Alignment & pipelines (§2.2)

```bibtex
@article{krueger2011,
  author  = {Krueger, Felix and Andrews, Simon R.},
  title   = {Bismark: a flexible aligner and methylation caller for {Bisulfite-Seq} applications},
  journal = {Bioinformatics},
  year    = {2011},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ditommaso2017,
  author  = {Di Tommaso, Paolo and Chatzou, Maria and Floden, Evan W. and others},
  title   = {Nextflow enables reproducible computational workflows},
  journal = {Nature Biotechnology},
  year    = {2017},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ewels2020,
  author  = {Ewels, Philip A. and Peltzer, Alexander and Fillinger, Sven and others},
  title   = {The {nf-core} framework for community-curated bioinformatics pipelines},
  journal = {Nature Biotechnology},
  year    = {2020},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
```

## Differential methylation (§2.3)

```bibtex
@article{akalin2012,
  author  = {Akalin, Altuna and Kormaksson, Matthias and Li, Sheng and others},
  title   = {methylKit: a comprehensive {R} package for the analysis of genome-wide {DNA} methylation profiles},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{feng2014,
  author  = {Feng, Hao and Conneely, Karen N. and Wu, Hao},
  title   = {A {Bayesian} hierarchical model to detect differentially methylated loci from single nucleotide resolution sequencing data},
  journal = {Nucleic Acids Research},
  year    = {2014},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{wu2015,
  author  = {Wu, Hao and Xu, Tianlei and Feng, Hao and others},
  title   = {Detection of differentially methylated regions from whole-genome bisulfite sequencing data without replicates},
  journal = {Nucleic Acids Research},
  year    = {2015},
  note    = {STATUS: VERIFY — confirm author list/vol/pages/DOI}
}
@article{park2016,
  author  = {Park, Yongseok and Wu, Hao},
  title   = {Differential methylation analysis for {BS-seq} data under general experimental design},
  journal = {Bioinformatics},
  year    = {2016},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{hansen2012,
  author  = {Hansen, Kasper D. and Langmead, Benjamin and Irizarry, Rafael A.},
  title   = {{BSmooth}: from whole genome bisulfite sequencing reads to differentially methylated regions},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{benjamini1995,
  author  = {Benjamini, Yoav and Hochberg, Yosef},
  title   = {Controlling the false discovery rate: a practical and powerful approach to multiple testing},
  journal = {Journal of the Royal Statistical Society: Series B},
  year    = {1995},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{robinson2014,
  author  = {Robinson, Mark D. and Kahraman, Abdullah and Law, Charity W. and others},
  title   = {Statistical methods for detecting differentially methylated loci and regions},
  journal = {Frontiers in Genetics},
  year    = {2014},
  note    = {STATUS: VERIFY — confirm venue/author list/details}
}
```

## LLMs, agents, tool use & MCP (§2.4)

```bibtex
@inproceedings{vaswani2017,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title     = {Attention is all you need},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2017},
  note      = {STATUS: confident — verify}
}
@inproceedings{brown2020,
  author    = {Brown, Tom B. and Mann, Benjamin and Ryder, Nick and others},
  title     = {Language models are few-shot learners},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@inproceedings{wei2022,
  author    = {Wei, Jason and Wang, Xuezhi and Schuurmans, Dale and others},
  title     = {Chain-of-thought prompting elicits reasoning in large language models},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2022},
  note      = {STATUS: confident — verify}
}
@inproceedings{yao2023,
  author    = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and others},
  title     = {{ReAct}: Synergizing reasoning and acting in language models},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{schick2023,
  author    = {Schick, Timo and Dwivedi-Yu, Jane and Dess{\`i}, Roberto and others},
  title     = {{Toolformer}: Language models can teach themselves to use tools},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{lewis2020,
  author    = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and others},
  title     = {Retrieval-augmented generation for knowledge-intensive {NLP} tasks},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@misc{mcp2024,
  author       = {{Anthropic}},
  title        = {Introducing the {Model Context Protocol}},
  year         = {2024},
  howpublished = {\url{https://www.anthropic.com/news/model-context-protocol}},
  note         = {STATUS: VERIFY — confirm canonical citation/spec URL and access date}
}
```

## Agents for science & reliability (§2.5)

```bibtex
@article{boiko2023,
  author  = {Boiko, Daniil A. and MacKnight, Robert and Kline, Ben and Gomes, Gabe},
  title   = {Autonomous chemical research with large language models},
  journal = {Nature},
  year    = {2023},
  note    = {STATUS: VERIFY — (Coscientist) confirm author list/vol/pages/DOI}
}
@article{bran2024,
  author  = {M. Bran, Andres and Cox, Sam and Schilter, Oliver and others},
  title   = {Augmenting large language models with chemistry tools},
  journal = {Nature Machine Intelligence},
  year    = {2024},
  note    = {STATUS: VERIFY — (ChemCrow) confirm author list/year/vol/pages/DOI}
}
@misc{lu2024,
  author = {Lu, Chris and Lu, Cong and Lange, Robert Tjarko and others},
  title  = {The {AI} {Scientist}: Towards fully automated open-ended scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — (Sakana AI) confirm arXiv id/author list}
}
@article{ji2023,
  author  = {Ji, Ziwei and Lee, Nayeon and Frieske, Rita and others},
  title   = {Survey of hallucination in natural language generation},
  journal = {ACM Computing Surveys},
  year    = {2023},
  note    = {STATUS: VERIFY — confirm vol/pages/DOI}
}
@misc{scienceagentbench,
  author = {Chen, Ziru and others},
  title  = {{ScienceAgentBench}: Toward rigorous assessment of language agents for data-driven scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — confirm authors/arXiv id/year (referenced by the Mimosa benchmark suite)}
}
@misc{paperbench,
  author = {{OpenAI}},
  title  = {{PaperBench}: Evaluating {AI}'s ability to replicate {AI} research},
  year   = {2025},
  note   = {STATUS: VERIFY — confirm authors/canonical citation}
}
```

## The system under study

```bibtex
@article{legrand2026,
  author  = {Legrand, Martin and Jiang, Tao and Feraud, Matthieu and Navet, Benjamin
             and Taghzouti, Yousouf and Gandon, Fabien and Dumont, Elise and Nothias, Louis-F{\'e}lix},
  title   = {Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research},
  journal = {arXiv preprint arXiv:2603.28986},
  year    = {2026},
  note    = {STATUS: VERIFY — citation taken from the Mimosa README; confirm arXiv id once public}
}
```


---

# 10_annexes

# Annexes

## A. Methylation Skill Document

<!-- Include the full skill text here or as a referenced file. -->

## B. MCP Tool Catalogues

<!-- Server A: 8 tools with full signatures and descriptions. -->
<!-- Server B: 2 execute-only tools + 14 atomic tools (retained variant). -->

## C. Agent Transcript

<!-- A complete transcript of a representative agent run (e.g., run23). -->

## D. Supplementary Result Tables

<!-- Additional tables not included in the experiment chapters. -->

## E. Environment Manifest

<!-- Docker image versions, R/Bioconductor package versions, Nextflow version, etc. -->


---

# OUTLINE

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
