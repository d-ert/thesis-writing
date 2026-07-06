
# Chapter 3 — System Design & Methods

## 3.0 Introduction to the chapter

This chapter describes the system whose reliability the rest of the thesis sets out to
measure. The system is **Mimosa**, a tool-augmented Large Language Model (LLM) agent, together
with the **Toolomics** infrastructure of Model Context Protocol (MCP) servers through which it
acts. The object of study is concrete and pre-existing: a conversational agent that, given a
folder of whole-genome bisulfite-sequencing (WGBS) data and a natural-language goal, drives a
complete differential-methylation analysis — coverage filtering, normalisation, differential
testing, region calling, annotation, and biological interpretation — by writing analysis code
and invoking domain-specific tools, rather than by following a fixed script.

The chapter is presented as *Methods* in two senses. First, it documents the engineered
artefact under test, so that the validation chapters (Chapters 4 and 5) can be read as
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
specification. §3.6 collects the reliability guardrails that the validation chapters revisit as
measured quantities, and §3.7 situates the system within the wider Toolomics ecosystem.

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
the agent's trustworthiness measurable — and the **validation studies** of Chapters 4–5, by which
the laboratory's agent is, for the first time, measured on DNA-methylation analysis.

---

## 3.1 Architecture overview

### 3.1.1 What the system is

Mimosa is an autonomous agent built around an LLM that operates in a loop: it reads a goal and
the current state of a working directory, decides on a next action, executes that action
through a tool, observes the result, and repeats until it judges the goal met. Its actions are
not free-form text but *tool calls* — and the tools available to it are not generic shell
access but a curated set of operations exposed by MCP servers. The intelligence that selects
and sequences those operations lives in the LLM; the operations themselves, and the
reproducible environments in which they run, live in the servers. This division is the central
architectural commitment of the system and the one most relevant to a thesis about reliability:
the unpredictable component (an LLM choosing what to do) is deliberately fenced off from the
components that must behave identically every time (a pinned Bioconductor container, a versioned
Nextflow pipeline, a fixed set of typed tools). A clarification of scope is owed on the word
*agent*: Mimosa is in fact the laboratory's broader self-evolving, multi-agent framework, which
*synthesises* the analysis workflow it then runs — and, optionally, evolves it across generations
— rather than executing a hand-written loop. The read–decide–act loop described here is what its
execution agents do *within* one synthesised workflow; §3.5 gives the full account. For the
architecture of this section, the division just stated is what matters.

Concretely, the system has four cooperating layers and a shared data substrate:

```
                          ┌───────────────────────────────────────────┐
   natural-language  ──▶  │  AGENT LAYER — Mimosa (LLM loop)           │
   goal + WGBS data       │  goal → plan → tool call → observe → repeat │
                          └───────────────────┬───────────────────────┘
                                              │ reads, on demand
                          ┌───────────────────▼───────────────────────┐
                          │  KNOWLEDGE LAYER — the methylation *skill* │
                          │  engine selection · QC defaults · gotchas  │
                          │  file-format facts · annotation conventions│
                          └───────────────────┬───────────────────────┘
                                              │ shapes how tools are used
              ┌───────────────────────────────▼──────────────────────────────┐
              │  TOOL LAYER — two MCP servers (FastMCP, streamable-HTTP)        │
              │                                                                │
              │   Server A: Nextflow / nf-core/methylseq   Server B: R engine  │
              │   8 tools — FASTQ → trim → Bismark → .cov   execute-only: 2 tools│
              │                                            methylKit / DSS      │
              └───────────────┬───────────────────────────────────┬───────────┘
                              │ executes in                        │ executes in
              ┌───────────────▼─────────────┐       ┌──────────────▼───────────────┐
              │ EXECUTION — Nextflow +        │       │ EXECUTION — Bioconductor 3.19 │
              │ Singularity (local) or        │       │ Docker image (methylKit, DSS, │
              │ Seqera Platform / AWS (cloud) │       │ genomation, …) pinned         │
              └───────────────┬─────────────┘       └──────────────┬───────────────┘
                              └──────────────┬───────────────────────┘
                          ┌──────────────────▼────────────────────────┐
                          │  DATA / STATE — shared workspace directory  │
                          │  .cov inputs · on-disk R scripts · .rds     │
                          │  intermediates · figures · run_report.txt   │
                          └─────────────────────────────────────────────┘
```

*(Figure 3.1 placeholder — this box diagram is the working sketch for the flagship architecture
figure; the final version greys out the future transcriptomics/metabolomics modules to convey
the multi-omics bridge of Chapter 7.)*

### 3.1.2 The end-to-end data flow

The biological pipeline the system automates is the standard WGBS path from raw reads to
interpreted regions, and the architecture maps onto it directly:

1. **Reads → coverage (Server A).** Paired-end FASTQ files (local, on S3, or fetched from the
   SRA) are assembled into an nf-core samplesheet and run through **nf-core/methylseq 2.6.0**
   with the **Bismark** aligner: adapter trimming, bisulfite alignment, methylation extraction,
   and per-cytosine reporting, yielding Bismark `.cov(.gz)` coverage files — six columns of
   chromosome, position, methylation percentage, and methylated/unmethylated counts per CpG.

2. **Coverage → differential methylation (Server B).** The `.cov` files are loaded into a
   methylKit object, filtered on coverage, normalised, and united across samples; differential
   testing is then performed either per-CpG (**DMCs**, differentially methylated cytosines) or
   over genomic tiles (**DMRs**, differentially methylated regions), using one of two engines —
   **methylKit** (per-CpG Fisher/logistic regression) or **DSS** (beta-binomial
   dispersion-shrinkage with spatial smoothing).

3. **Regions → biology (Server B).** Significant DMCs/DMRs are annotated against bundled UCSC
   RefSeq gene models and CpG-island tracks (hg38 and mm10) and carried into gene-level and
   ontology-level interpretation.

The **dividing line between the two servers — the `.cov` coverage file — is also the boundary
of what this work exercises on real data.** Aligning full real human WGBS from FASTQ with
nf-core/methylseq was estimated at roughly six days per sample on the available workstation
(64 GB RAM, 24 cores, no cloud access), so the real-data replications in Chapter 4 begin at the
coverage-file stage and Server A's alignment half is demonstrated only at small synthetic scale
(Chapter 5). Server A is therefore presented as a *capability* of the system — fully
implemented and runnable locally on small data — rather than as a stage benchmarked on real
WGBS. This boundary is made explicit here because it shapes how the validation should be read.

### 3.1.3 How the layers communicate

The agent and the servers do not pass large objects to one another in messages. They
communicate through two narrow channels, both chosen for reproducibility and for keeping the
LLM's context small:

- **Typed tool calls over MCP.** Each server is a FastMCP application speaking the
  streamable-HTTP transport. Within the Toolomics deployment, `deploy.py` auto-discovers each
  server's `docker-compose.yml`, assigns it a port in the 5000–5200 range, and brings the
  container up; Mimosa's port scanner then registers the server's tools automatically, so
  adding a server requires no change to the agent. Tool results returned to the agent are
  deliberately small — standard output and error are truncated (4000 characters for the R
  server) and large artefacts are left on disk rather than returned inline.

- **A shared workspace directory.** Both servers mount the same workspace as the agent's
  working directory. State that must persist between steps is written there as files: the agent
  authors R analysis scripts to disk and then asks the server to run them; intermediate
  methylKit objects are serialised as `.rds` files that later steps reload; figures are written
  to PDF devices; and an append-only `run_report.txt` records what was decided and done. The
  guiding rule, stated in the skill, is that *the on-disk file is the deliverable* — the script
  a human would review is exactly the script that runs, with no hidden inlined code.

### 3.1.4 Design principles

Four principles recur across the components and are worth naming up front, because the
validation chapters test whether they deliver the reliability they promise:

1. **Separate orchestration from execution.** The LLM decides; pinned containers and versioned
   pipelines execute. Non-determinism is confined to the planning layer, where it can be
   measured (Chapter 5), and kept out of the numerical layer, where it would be fatal.

2. **Encode expertise as a skill, not as prompt folklore.** The non-obvious decisions of
   methylation analysis — which engine suits which coverage/replicate regime, what QC
   thresholds to apply, which failure modes to guard against — are written once as a declarative
   skill (§3.4) that the agent consults, rather than being re-derived, inconsistently, on every
   run.

3. **Offer two tool altitudes — and default to the more reviewable one.** The methylation
   server's primary surface is deliberately minimal: the agent authors a complete R script and
   runs it (maximally expressive, and auditable as a single on-disk file). An earlier variant
   additionally exposed a set of typed atomic tools that each perform one canonical pipeline step
   (maximally constrained); it is retained as the constrained arm of the Chapter 5 reliability
   ablation. The trade-off between expressivity and constraint is thus treated as an experimental
   variable, not fixed by fiat — see §3.3.1.

4. **Make the artefact reproducible by construction.** On-disk scripts, serialised
   intermediates, pinned environments, and an append-only run log mean that a completed run is,
   in principle, re-executable and auditable independently of the agent that produced it.

The remainder of the chapter examines each layer in turn, beginning with the two MCP servers
that constitute the tool layer.

---

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

- the **real-data replications (Chapter 4) start from the published `.cov` coverage files** and
  do not exercise Server A's alignment stage;
- Server A's full FASTQ → `.cov` path is demonstrated only at **small synthetic scale**
  (Chapter 5), where a reduced reference and short read sets complete quickly, with an existing
  small-genome Bismark test run as additional evidence that the local Singularity path is
  correct end-to-end.

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

Server B can present its R environment at two very different altitudes, and the difference between
them is itself one of the experimental variables of the reliability study (Chapter 5). The two are
not both live at once; they are two server variants, and the one that produced every run analysed
in this thesis is the more minimal of the two.

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

**The alternative surface: typed atomic tools (a retained variant, used for the ablation).** An
earlier design exposed the same R stack at a far more constrained altitude. Alongside four generic
runners (`execute_r_code`, which saves supplied R to a timestamped file and runs it;
`write_r_script`; `execute_r_script_file`; and `list_workspace_files`), it registered a set of
typed *atomic* tools that each perform one canonical pipeline step and validate their inputs. Each
is a thin wrapper that invokes a corresponding `r_scripts/*.R` helper with a JSON argument blob and
parses a structured result the helper prints inside a `<<<RESULT>>>…<<<END>>>` footer — so the
agent receives, for example, the number of sites tested and the number significant at q < 0.05,
not free text. This variant is retained in the repository (`old_server_with_atomicTools`) and
serves as the **constrained arm of the Chapter 5 ablation**, set against the free-form
write-a-script arm above. Its fourteen atomic tools cover the whole methylKit workflow:

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
atomic tools. *(Figure 3.3 placeholder — this chain is the working sketch for the atomic-tool
state-flow diagram.)*

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
inconsistently — by the LLM on each run. Whether this consistency materially reduces
run-to-run variance is exactly what the no-skill-versus-skill arm of the reliability ablation
(Chapter 5) is built to measure.

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
confident calls — a built-in form of the cross-method agreement that the validation chapters
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
samples excluded. The append-only run report is both a reproducibility aid and, in the
reliability study, a source of evidence about what the agent actually decided on a given run.

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
evolution disabled** — the prompt-ablation harness (`scripts/run_prompt_ablation.sh`) explicitly
invokes `main.py … --max_evolve_iterations 1` so that each goal variant is evaluated in
isolation. Evolution is therefore not the default operating mode of the system as validated here;
it is **one studied axis**, exercised as the `--learn` arm of the Chapter 5 reliability ablation
(plan cell C5), where the question is precisely whether bounded autonomy preserves or degrades
run-to-run reliability. Presenting Mimosa honestly means describing the full evolutionary machine
while being clear that most of the evidence comes from its single-shot use.

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

*(Figure 3.4 — working sketch of the Mimosa five-layer pipeline and its evolutionary feedback
loop. In the one-shot regime used for most runs in this thesis (§3.5.2) the loop runs once, top
to bottom; the dashed return path on the right is active only under `--learn`.)*

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
another provider — and the reliability study of Chapter 5 deliberately **pins a single, fixed
configuration** across its repeated runs so that observed variance is attributable to the agent's
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

*(Table 3.3 placeholder — the goal-evolution changelog above is the working version of the goal
table; the final version cites line ranges in each goal file.)*

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
timeout of 21 600 s (6 h), and a 10 GB memory cap — values that matter for Chapter 5, where an
under-set timeout is shown to be the operational cause of several earlier run failures.

---

## 3.6 Reliability guardrails

The design choices of §§3.1–3.5 are *intended* to produce reliability: orchestration is fenced
off from execution, expertise is encoded once, artefacts are reproducible by construction, and a
deterministic verifier grades each run. This section is about the gap between intended and
observed. It does two things: it presents the concrete evidence, already sitting in the run
archive, that the unguarded system is **not** reliable run-to-run; and it specifies the
domain-specific guardrails and instrumentation this thesis introduces to close and to *measure*
that gap. These are the thesis's own reliability layer (§3.0), not pre-existing lab machinery:
some are already prototyped against the existing runs, and all are applied and quantified across
the Chapter 5 studies (Study D), where each becomes a measured quantity rather than a claim.

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
differ in goal version and method, and so they measure *method-selection instability*, not the
pure run-to-run variance that Chapter 5 isolates by fixing every input. But they already establish
the thesis's central problem: nominally identical instructions, executed by the same system on the
same data, produce results that differ by orders of magnitude, and the system reports all of them
as successes.[^run9]

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

*(Figure 3.5 — excerpts of the on-disk `run_report.txt` for two runs on the **same six input
files**. `run10` is internally coherent; `run11` hides five failed load/QC attempts, then reports
1 816 significant DMRs from 22 tested tiles — an impossibility (F2, §3.6.3) — and appends a
contradictory `FAILED` after its own "success". Both self-report success.)*

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
This both removes the bug from the validation and supplies Chapter 5 with its first concrete
example of a failure that only cross-run, externally-held ground truth can catch.

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
*arithmetically and biologically possible at all*. Each assertion is also a measured datapoint —
the **silent-failure rate** is one of the reliability dimensions Chapter 5 reports.

### 3.6.4 Instrumentation for the reliability study

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
the Chapter 5 variance metrics — coefficient of variation of counts, mean pairwise Jaccard of
DMR/DMC and gene sets, parameter-vector agreement, F1 against the synthetic oracle, and the
error-recovery and silent-failure rates — by which the question "is this agent reliable?" is given
numbers rather than adjectives.

---

## 3.7 Situating Mimosa in the Toolomics ecosystem

Mimosa and the two Toolomics servers are not isolated artefacts; they are part of a small family
of laboratory tools, two of which the reader should know exist because they are wired into the
system described above and because they frame the Future Work of Chapter 7. They are summarised
here only to the depth needed for that purpose; neither is itself under validation in this thesis.

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
tangible piece of the multi-omics bridge that Chapter 7 develops. Indicium is not used to *run* any
analysis here — it explicitly does not call DMRs or
align reads — and so it is not part of the system under test. It is described because it is the
concrete substrate of the thesis's framing claim: methylation is positioned as the **validated
first vertical** of a system designed to extend, through a shared claim standard, toward
transcriptomics and metabolomics. The benchmark-construction toolkit AgenticScienceBuilder, which
turns published papers into machine-readable evaluation tasks against this same standard, completes
the ecosystem but is otherwise out of scope.
