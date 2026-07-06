# Chapter 2 — Background & Related Work

## 2.0 Introduction to the chapter

This chapter assembles the background needed to read the rest of the thesis and locates the work
within two literatures that rarely meet. The first is the established science of **whole-genome
bisulfite sequencing (WGBS)** and **differential DNA-methylation analysis**: a mature field with
canonical data formats, statistical models, and software whose behaviour is well characterised.
The second is the fast-moving field of **tool-augmented large language model (LLM) agents** —
systems that plan, call external tools, and act on their results — and the still-young question
of whether such agents can be made *reliable* enough to be trusted with scientific analysis. The
thesis sits exactly at the seam between them: it takes a domain whose correct answers are knowable
(§2.1–2.3) and asks whether an agent (§2.4–2.5) can reach them reproducibly.

The chapter proceeds accordingly. §2.1 introduces DNA methylation and the WGBS assay that
measures it. §2.2 follows the data from raw reads to per-cytosine coverage through the alignment
pipeline the system of Chapter 3 wraps. §2.3 defines differentially methylated cytosines and
regions (DMCs and DMRs) and contrasts the two statistical engines — methylKit and DSS — that the
agent routes between. §2.4 turns to LLM agents, tool use, and the Model Context Protocol (MCP)
that connects an agent to scientific software. §2.5 surveys autonomous agents for science and the
reliability problem that motivates the whole thesis. §2.6 states the gap these literatures leave
open, which the hypothesis of Chapter 1 sets out to close.

A caveat on sources is owed at the outset. The methodological literature of §2.1–2.3 is settled
and is cited to its primary papers. The agent literature of §2.4–2.5 is recent and moves faster
than any single snapshot; claims there are tied to primary sources where possible and flagged for
re-verification at the time of writing, consistent with the knowledge-cutoff discipline this work
adopts.

---

## 2.1 DNA methylation and whole-genome bisulfite sequencing

**The modification.** DNA methylation is a covalent epigenetic mark in which a methyl group is
added to the fifth carbon of a cytosine base, producing 5-methylcytosine (5mC). In mammalian
genomes it occurs predominantly at cytosines immediately followed by a guanine — the **CpG
dinucleotide** — and it is one of the most stable and best-studied carriers of epigenetic
information, shaping gene regulation without altering the underlying sequence [@bird2002;
@jones2012]. Its distribution is non-random and biologically consequential: short CpG-dense
stretches called **CpG islands**, often overlapping gene promoters, are typically unmethylated in
active genes, whereas methylation of a promoter island is generally associated with
transcriptional silencing; gene bodies, repetitive elements, and intergenic regions follow their
own characteristic patterns [@jones2012]. Because these patterns are laid down and maintained in
response to developmental and environmental signals, differences in methylation between
conditions — a knockout versus its wild type, a disease cohort versus controls — are read as
candidate regulatory events.

**Measuring it: bisulfite conversion.** The foundational technique for reading methylation at
single-base resolution is **bisulfite conversion** [@frommer1992]. Treating DNA with sodium
bisulfite deaminates unmethylated cytosines to uracil (read as thymine after amplification), while
5-methylcytosine is protected and remains a cytosine. After sequencing, the methylation state of
each cytosine is therefore inferred from a simple contrast: positions that read as C were
methylated, positions that read as T were not, and the **methylation level** of a site is the
fraction of reads still showing C. Applying this genome-wide and at base resolution yields a
**whole-genome bisulfite sequencing (WGBS)** methylome [@lister2009; @cokus2008], the assay this
thesis works with.

**The data model.** For the analysis that follows, the salient point is that WGBS reduces, per
CpG site, to two integer counts: the number of methylated reads and the number of unmethylated
reads covering that position. The methylation level is the ratio of the first to their sum, and
the reliability of that ratio depends on the **coverage** (the total read count) at the site —
a CpG seen by three reads carries far less information than one seen by thirty. This count-based,
coverage-weighted structure is what the downstream statistics of §2.3 are built around, and it is
why coverage filtering is the first quality-control step of every pipeline in this work.

**Alternatives and scope.** WGBS is the most comprehensive methylation assay but not the only one:
reduced-representation bisulfite sequencing (RRBS) enriches for CpG-dense regions at lower cost,
and methylation microarrays (the Illumina 450K and EPIC platforms) interrogate a fixed panel of
pre-selected CpGs. These trade genome-wide coverage for cost or convenience, and the claim-level
metadata that distinguishes them is exactly what the epigenomics adapter of §3.7 standardises. The
experiments of this thesis use WGBS coverage data throughout.

---

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
pipeline — the exact artefact Server A invokes. The significance for a reliability thesis is that
this upstream stage is *already* engineered for reproducibility through pinned containers and
versioned code; the non-determinism the thesis investigates is introduced not here but by the
agent that orchestrates it.

**The coverage file is the natural boundary.** Because alignment is computationally heavy — full
real-WGBS alignment was infeasible on the available hardware (Chapter 3) — the coverage file is
also the practical boundary at which this thesis's real-data validation begins. The data model of
§2.1 is recovered exactly at this point, so downstream analysis can be validated against published
studies even when the alignment half is exercised only at small synthetic scale.

---

## 2.3 Differential methylation: DMCs, DMRs, and two statistical engines

The scientific question WGBS is used to answer is comparative: *where does methylation differ
between two groups, and in which direction?* Answering it well is a non-trivial statistical
problem, and the choice of method materially affects the result — which is precisely why the
agent needs the engine-selection skill of §3.4, and why the validation of Chapters 4–5 must score
against more than one baseline.

**DMCs versus DMRs.** Two units of analysis are standard. A **differentially methylated cytosine
(DMC)** is a single CpG whose methylation level differs significantly between groups. A
**differentially methylated region (DMR)** is a contiguous genomic interval — often a fixed-width
*tile* or a run of adjacent DMCs — that differs as a unit. DMRs are usually the more biologically
interpretable object, because regulatory effects act over regions rather than isolated bases and
because aggregating neighbouring CpGs improves statistical power and reduces the multiple-testing
burden; DMCs offer finer resolution at the cost of many more tests. A region is summarised by an
effect size, typically the **difference in mean methylation** between groups (often written Δβ or
`meth.diff`), and a significance value; the *sign* of that difference encodes direction
(hyper- versus hypo-methylation), a detail whose mishandling is the polarity bug of §3.6.

**Why the statistics are hard.** Three features of WGBS counts complicate naïve testing. Coverage
varies by orders of magnitude across sites, so equal weighting is wrong. Biological replicates are
**overdispersed** — the variance between replicates exceeds what a simple binomial model predicts —
so tests that ignore overdispersion produce anti-conservative p-values and inflated false-positive
rates. And the sheer number of CpGs (tens of millions genome-wide) makes **multiple-testing
correction** essential; methods control the false discovery rate (FDR) via Benjamini–Hochberg
[@benjamini1995] or related procedures, reported as q-values. Calibrated control of false
positives under exactly these conditions is what the synthetic benchmark of Chapter 5 is designed
to measure.

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
training. The step from *language model* to *agent* is the addition of **tools** and a **loop**.

**Tool use and the agent loop.** A tool-using agent interleaves reasoning with action: it decides
on a next step, calls an external tool, observes the result, and repeats. The **ReAct** pattern
formalised this interleaving of reasoning traces and tool actions [@yao2023], and **Toolformer**
showed that models can learn when and how to invoke tools through their API signatures
[@schick2023]; retrieval-augmented generation similarly grounds outputs in external documents
rather than parametric memory [@lewis2020]. The recurring theme is that the model supplies
*decisions* while tools supply *capabilities and ground truth* — exactly the orchestration/
execution split that Chapter 3 makes its central design commitment.

**The Model Context Protocol.** Connecting an agent to many tools historically meant bespoke
integration code per tool. The **Model Context Protocol (MCP)**, an open standard introduced in
late 2024, defines a uniform client–server interface through which an agent discovers and calls
tools, retrieves resources, and uses prompt templates, so that any MCP-speaking client can use any
MCP server without custom glue [@mcp2024]. MCP is the protocol on which the Toolomics servers of
§3.2–3.3 are built, and the property that makes it valuable for reliability is the same one that
makes it valuable for engineering: tools become typed, versioned, independently testable services
rather than inlined code, which confines the unpredictable component to the agent and keeps the
executing component fixed.

**Encoding domain expertise.** A capability gap remains between *having* tools and *using them
well*: an agent equipped with methylKit and DSS still needs to know which to choose, what
thresholds to set, and which pitfalls to avoid. A lightweight answer that has emerged in agent
practice is the **skill** — a declarative, version-controlled document of domain procedure and
guardrails that the agent consults at run time rather than re-deriving on every invocation. The
methylation skill of §3.4 is an instance of this idea, and whether such encoded expertise actually
improves run-to-run consistency is one of the questions the reliability study of Chapter 5
measures directly.

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

**The reliability problem.** What these demonstrations rarely establish is *reliability*. LLMs are
non-deterministic and prone to fluent, confident errors — including fabricated facts and
unsupported claims [@ji2023] — and an agent that wraps an LLM inherits these failure modes while
adding new ones: silent tool failures, irreproducible run-to-run behaviour, and self-reported
"successes" that do not survive inspection. In a scientific setting these are disqualifying unless
measured and controlled, because a plausible-looking wrong answer is worse than an obvious one. The
concrete failures documented in §3.6 — the same input yielding results that differ by orders of
magnitude, an impossible region count carried into a biological conclusion — are precisely this
problem in the methylation domain.

**Evaluation is catching up, unevenly.** Benchmarks have begun to measure agent capability on
scientific and data-analysis tasks — for example task suites that score whether an agent's
generated analysis reproduces a reference result [@scienceagentbench; @paperbench]. These measure
*capability* (does it ever succeed?) more than *reliability* (does it succeed consistently, and
fail safely?), and they are general rather than tied to a domain with an established ground truth.
For a clinically-adjacent assay such as WGBS methylation, the quantities a practitioner actually
needs — concordance with published findings, calibrated false-positive control against known
truth, and reproducibility across repeated runs — have not, to our knowledge, been reported for an
LLM agent. *(This paragraph in particular depends on recent, fast-moving literature and is to be
re-checked against primary sources at writing time.)*

---

## 2.6 The gap and the thesis's position

Bringing the two literatures together exposes a specific, fillable gap.

On one side, **the methods are mature and their correct answers are knowable** (§2.1–2.3): WGBS has
canonical formats, methylKit and DSS are characterised tools, published studies provide concrete
target findings, and synthetic data can supply exact ground truth. On the other side, **agents are
capable but unproven on reliability** (§2.4–2.5): the orchestration/execution split and protocols
like MCP make it architecturally possible to fence non-determinism away from numerical execution,
and skills make it possible to encode expertise — but whether these mechanisms deliver
*reproducible, concordant, false-positive-controlled* methylation analysis has not been
demonstrated or measured.

That absence is the gap this thesis addresses. Where prior agent-for-science work emphasises
capability demonstrations, this work emphasises **measurement against knowable truth** in a single
well-chosen domain. It asks whether a tool-augmented LLM agent, constrained by a domain skill and
typed MCP tools, can (i) reproduce published WGBS findings, (ii) control false positives
comparably to expert-run methylKit/DSS against synthetic ground truth, and (iii) remain
reproducible run-to-run — the three axes of the hypothesis stated in Chapter 1. The system that
makes this measurable is the subject of Chapter 3; the measurements themselves are Chapters 4
and 5. By treating methylation as a fully validated first vertical rather than an isolated demo,
the thesis also lays the honest groundwork for the multi-omics extension of Chapter 7, in which
the same claim-standardisation substrate (§3.7) carries the approach toward transcriptomics and
metabolomics.
