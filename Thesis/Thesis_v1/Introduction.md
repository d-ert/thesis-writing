
# Chapter 1 — Introduction

> **Draft note (remove before submission).** This introduction is written ahead of the experiments
> (Chapters 4–5). Statements of *intent, hypothesis, tasks, and methodology* are stable; any
> sentence that anticipates a *result* is phrased as something the thesis sets out to measure, and
> the final verdict wording is to be settled once the studies are complete. Also: per UniBO rules,
> **the title on the front page must match the title registered on Studenti Online exactly** — the
> registered title is to be updated to the one below when the graduation application opens (9 July
> 2026). The eight subsections of this chapter correspond, in order, to the eight elements UniBO
> requires of a thesis introduction (object, tasks, hypothesis, actuality, research methodology,
> sources, structure, new approach).

This thesis is about whether an artificial-intelligence agent can be *trusted* to do a real
piece of genomics. Large language models have made it possible to ask software to carry out an
analysis in plain language, and to have it write and run the code itself; the open question — the
one that decides whether such systems belong anywhere near science — is not whether they can
occasionally produce a correct answer, but whether they produce it *reliably*: concordantly with
established findings, with their false positives under control, and reproducibly from one run to
the next. The work that follows takes a single, well-understood analytical domain — differential
DNA-methylation analysis from whole-genome bisulfite sequencing (WGBS) — and uses it as a
proving ground on which that question can be given numbers instead of adjectives.

## 1.1 Object

The **object** of this thesis is the reliability of a tool-augmented large language model (LLM)
agent applied to WGBS DNA-methylation analysis. Concretely, the object of study is **Mimosa**, a
self-evolving multi-agent framework developed in the host laboratory (Université Côte d'Azur,
Holobiomics / MetaboLinkAI; Legrand et al., 2026), operating through the laboratory's **Toolomics**
infrastructure of Model Context Protocol (MCP) tool servers. Given a folder of WGBS coverage files
and a natural-language goal, this system synthesises and runs a complete differential-methylation
pipeline — quality control, differential testing, region calling, annotation, and interpretation —
by writing analysis code and invoking domain tools rather than by following a fixed script. The
thesis does not introduce that framework; it adopts it as the apparatus under test and supplies its
first rigorously validated application to a single biological domain.

The work is, deliberately, a *refocusing* of a broader registered project. The internship from
which it arises was registered under a clinical multi-omics title; the thesis delivers and
validates the **methylation vertical** of that vision in depth, and frames it honestly as the
validated foundation from which a multi-omics system (transcriptomics, then metabolomics) can be
extended — rather than claiming the full integration, which is reserved for Future Work
(Chapter 7).

## 1.2 Tasks

To make the object tractable, the thesis pursues a connected set of **tasks**:

1. **Specify the system under test** precisely enough that its behaviour can be measured — its
   architecture, its two MCP tool servers, its domain *skill*, its agent loop and goal
   specification, and its reliability guardrails (Chapter 3).
2. **Replicate published WGBS findings** by driving the agent, and matched expert-run baselines,
   over the identical data of two peer-reviewed studies — a human knockout study and a mouse
   knockout study — and scoring concordance (Chapter 4).
3. **Measure false-positive control and sensitivity against known ground truth**, by generating
   synthetic methylation data with injected, known differentially methylated regions and asking
   whether the agent's calls are calibrated (Chapter 5).
4. **Quantify run-to-run reliability** — reproducibility across repeated identical runs, error
   recovery, and the rate of *silent* failures — under a controlled ablation of the system's
   components (Chapter 5).
5. **Build the measurement infrastructure** these require: a shared, sign-canonicalised scoring and
   concordance library, post-hoc sanity assertions that catch impossible results, and the
   instrumentation that records what each run decided and produced (Chapter 3, §3.6).

Tasks 1 and 5, together with the two Toolomics MCP servers, the methylation skill, the goal
specification and its evolution, and the epigenomics claim adapter, constitute the thesis's own
engineering contribution; tasks 2–4 are its scientific core.

## 1.3 Hypothesis

The central **hypothesis** is that *a tool-augmented LLM agent, constrained by a domain skill and
typed MCP tool servers, can reproduce published WGBS findings and control false positives
comparably to expert-run methylKit/DSS analyses, while remaining reproducible from one run to the
next.* It decomposes into three testable claims, each tied to a study:

- **H1 (concordance).** Driven over the identical data of a published study, the agent recovers the
  study's principal findings — its differentially methylated regions, affected genes, and direction
  of effect — to a degree comparable with an expert re-analysis of the same data (Chapter 4).
- **H2 (calibration).** Against synthetic data with known truth, the agent's false-discovery rate
  sits at or below the nominal level it reports, and its sensitivity is comparable to expert-run
  methylKit/DSS over the same data (Chapter 5).
- **H3 (reproducibility).** Repeated identical runs yield results whose run-to-run variance, and
  whose rate of silent failure, are low — and are demonstrably reduced by the skill and tool
  guardrails relative to an unguarded agent (Chapter 5).

The hypothesis is falsifiable in each part, and the thesis reports the verdict honestly whichever
way the evidence falls; a negative or qualified result (for example, "reliability requires the
skill and bounded autonomy") is a defensible and informative scientific outcome.

## 1.4 Actuality

The **actuality** — the timeliness and relevance — of the question is sharp. Tool-using LLM agents
have, within a very short span, moved from research demonstrations to systems that conduct
chemical and computational research with little human intervention, and the recent standardisation
of agent–tool interfaces (the Model Context Protocol) has made it routine to connect an agent to
real scientific software. The attraction for biology and medicine is obvious: methylation and
other omics analyses demand specialised expertise that most clinicians and many researchers lack,
and a conversational agent promises to make that analysis accessible through ordinary language.

But the same properties that make these systems attractive make them dangerous in a scientific
setting: they are non-deterministic, they fail in fluent and confident ways, and they can report
success on results that do not survive inspection. For a clinically-adjacent assay such as WGBS
methylation — where a hyper- or hypo-methylated region may be read as a candidate biomarker — a
plausible wrong answer is worse than an obvious one. The decisive quantities a practitioner would
need before trusting such a tool — concordance with published findings, calibrated false-positive
control, and run-to-run reproducibility — have not, to our knowledge, been reported for an LLM
agent performing methylation analysis. Supplying them, in a domain whose correct answers are
knowable, is the timely contribution this thesis makes.

## 1.5 Research methodology

The **research methodology** is a *system-plus-validation* design in which an engineered artefact
and an empirical evaluation of it carry equal weight. The system is specified as a fully described
apparatus (Chapter 3); its behaviour is then measured by four studies that triangulate the
hypothesis from complementary angles:

- two **real-data replications** (Study A, human GSE263850; Study B, mouse GSE214232), scored as a
  triangle — agent versus published results, agent versus an expert re-analysis we run ourselves,
  and expert versus published (the realistic ceiling) — on gene recovery, direction, and
  qualitative signature rather than on raw count identity, since several defensible methods give
  different counts;
- one **synthetic ground-truth benchmark** (Study C), in which methylation data with injected,
  known regions tests sensitivity and, crucially, the *calibration* of the reported false-discovery
  rate;
- one **reliability study** (Study D), in which repeated runs under a controlled, one-variable-at-a-
  time ablation quantify reproducibility, error recovery, and silent-failure rate.

Two methodological commitments run throughout. First, **every reported number traces to a committed
script and input**, and all pipelines are forced onto one canonical effect-direction before any
concordance is computed. Second, the methodology is bounded by an explicit **honesty boundary**
imposed by the available compute (a single workstation, no cloud): full alignment of real WGBS from
raw reads was infeasible, so the real-data validation begins at the coverage-file stage and the
full reads-to-coverage path is exercised only at small synthetic scale. This boundary is stated
wherever it bears on a claim, not relegated to a limitations note.

## 1.6 Sources

The **sources** of the thesis are of four kinds. The *primary data* are public: the coverage files
and supplementary result tables of two peer-reviewed WGBS studies, obtained from the Gene
Expression Omnibus (GEO), together with synthetic data generated for Study C. The *methodological
literature* is the established science of bisulfite sequencing and differential-methylation
analysis — the methylKit and DSS engines, the Bismark aligner, and the nf-core/methylseq pipeline —
cited to its primary papers. The *system under study* is documented from its own source code and
from the laboratory's framework description (Legrand et al., 2026). The *agent and protocol
literature* — LLM tool use, MCP, autonomous agents for science, and the reliability of such agents
— is drawn from primary sources; because this literature is recent and fast-moving, it is treated
with an explicit knowledge-cutoff caveat and re-verified at the time of writing. The full apparatus
of sources is given in the Bibliography, and the background they support is set out in Chapter 2.

## 1.7 Structure of the thesis

The **structure** follows the methodology. **Chapter 2 (Background & Related Work)** introduces the
two literatures the thesis joins — WGBS methylation and its statistics on one side, LLM agents and
MCP on the other — and states the gap between them. **Chapter 3 (System Design & Methods)** specifies
the system under test: its architecture, the two MCP servers, the methylation skill, the Mimosa
agent and its goal evolution, and the reliability guardrails. **Chapter 4 (Validation I —
Replication)** presents the two real-data replications and their cross-study discussion. **Chapter 5
(Validation II — Synthetic & Reliability)** presents the synthetic-ground-truth benchmark and the
reproducibility/error-recovery study. **Chapter 6 (Discussion)** returns to the hypothesis, weighs
strengths against honest limitations, and considers threats to validity. **Chapter 7 (Conclusions &
Future Work)** states the contributions and develops the multi-omics bridge for which methylation is
the validated first vertical. A **Bibliography** and **Annexes** (the skill, MCP tool catalogues, a
complete agent transcript, and supplementary result tables) close the thesis.

## 1.8 New approach

The **new approach** of this thesis is to evaluate an autonomous scientific agent not by *capability
demonstrations* — the dominant mode in the agents-for-science literature, where success is shown
once — but by **measurement against knowable truth** in a domain chosen precisely because its
correct answers exist. Three elements are, to our knowledge, novel in combination. First, a
**triangulated concordance evaluation** that scores the agent against both a published study and an
expert re-analysis of the identical data, using the expert-versus-published agreement as the
realistic ceiling. Second, a **calibration-centred synthetic benchmark** that asks not merely
whether the agent finds signal but whether its reported false-discovery rate is honest. Third, a
**quantified reliability study** that treats run-to-run variance, error recovery, and *silent
failure* as first-class measured quantities, and isolates the contribution of a domain skill and
typed tools to reliability through a controlled ablation. Underpinning all three are two small but
consequential pieces of methodological engineering — a sign-canonicalising scoring library that
removes a direction-of-effect bug invisible within any single run, and a set of post-hoc assertions
that turn an agent's impossible-but-confident result into a hard stop. By treating methylation as a
fully validated vertical rather than an isolated demonstration, and by building its claims on a
shared standard that other omics domains can adopt, the thesis also offers an honest template for
how such agents might be validated, domain by domain, before they are trusted.
