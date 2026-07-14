# Chapter 3 — System Design & Methods

## 3.1 Introduction

The methodology of this work rests on evaluating this fully specified system. The architectural design choices—namely, the separation of orchestration from execution, the encoding of domain expertise as a declarative _skill_, the dual-server tool surface, and the strict file-on-disk reproducibility contract—constitute the mechanisms intended to ensure reliability. These mechanisms are evaluated empirically in the subsequent validation experiments (Chapters 4–6). Furthermore, where specific components are exercised only partially due to computational constraints (such as the upstream alignment pipeline of Server A, which could not be executed on full-scale real data; see §3.2 and Chapter 4), these constraints are delimited alongside the system specifications.

This chapter establishes the baseline architecture, defining the parameters and operational boundaries of the pre-existing system prior to experimental evaluation. The quantitative behavior of the system—specifically its concordance with published studies, its performance against synthetic ground truth, and its reproducibility across repeated executions—is then assessed sequentially in the following chapters.

The architecture and end-to-end data flow are detailed in §3.1, followed by the specifications of the two MCP servers: the Nextflow/methylseq runner (§3.2) and the containerised R methylKit/DSS environment (§3.3). The domain-specific _skill_ governing the agent's analytical decisions is defined in §3.4. The underlying Mimosa framework—including its workflow-synthesis loop, evolutionary search, verifier, and goal specification—is detailed in §3.5.

**Contributions and Pre-existing Framework.** To delineate the scope of novel contributions, the underlying **Mimosa framework**—including its planner, Quality-Diversity evolution engine, multi-source verifier, and SmolAgents/LangGraph runner (§3.5)—as well as the **Toolomics** control plane, constitute prior work developed by the host laboratory (Legrand et al., 2026). These are employed here as the foundational apparatus under test. The novel engineering contributions developed specifically for this research include: the implementation of **both MCP servers** (the Nextflow/methylseq runner detailed in §3.2 and the containerised R/Bioconductor methylation server with bundled annotations in §3.3); the declarative **methylation skill** (§3.4); the **goal specification and its iterative refinement** (§3.5.5); the **epigenomics claim adapter** (§3.7); and corrective modifications to the Perspicacité literature service (§3.7).

- [ ] epigenomics claim adapter'ı ve perspicacite cümlelerini silmek lazım sanki. yaptığın contribution'a göre karar ver task🔼 📅 2026-07-19 

---

## 3.1 Architecture overview

### 3.1.1 System overview

Mimosa is an autonomous agent built around an LLM that operates in a loop: it reads a goal and the current state of a working directory, selects a next action, executes that action through a tool, observes the result, and repeats until it judges the goal met. Its actions are not free-form text but _tool calls_, and the tools available to it are not generic shell access but a curated set of operations exposed by MCP servers. The selection and sequencing of those operations is performed by the LLM; the operations themselves, and the reproducible environments in which they run, reside in the servers. This division constitutes the central architectural commitment of the system and the one most relevant to reliability: the non-deterministic component (an LLM choosing what to do) is deliberately separated from the components that must behave identically on every invocation (a pinned Bioconductor container, a versioned Nextflow pipeline, a fixed set of typed tools). A clarification of scope is necessary regarding the term _agent_: Mimosa is the laboratory's broader self-evolving, multi-agent framework, which _synthesises_ the analysis workflow it subsequently executes — and, optionally, evolves it across generations — rather than executing a hand-written loop. The read–decide–act loop described here is what its execution agents perform _within_ one synthesised workflow; §3.5 provides the full account. For the purposes of the architectural description in this section, the division stated above is the salient property.

Concretely, the system has four cooperating layers and a shared data substrate:




```
                          ┌───────────────────────────────────────────┐
   natural-language  ──▶  │  AGENT LAYER — Mimosa (LLM loop)           │
   goal + WGBS data       │  goal → plan → tool call → observe → repeat │
                          └───────────────────┬───────────────────────┘
                                              │ reads, on demand
                          ┌───────────────────▼───────────────────────┐
                          │  KNOWLEDGE LAYER — the methylation *skill* │
                          │  engine selection · QC defaults · pitfalls │
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

_(Figure 3.1.)_


![[Thesis_Architecture overview.png]]

### 3.1.2 The end-to-end data flow

The biological pipeline the system automates is the standard WGBS path from raw reads to interpreted regions, and the architecture maps onto it directly:

1. **Reads → coverage (Server A).** Paired-end FASTQ files (local, on S3, or fetched from the SRA) are assembled into an nf-core samplesheet and run through **nf-core/methylseq 2.6.0** with the **Bismark** aligner: adapter trimming, bisulfite alignment, methylation extraction, and per-cytosine reporting, yielding Bismark `.cov(.gz)` coverage files — six columns of chromosome, position, methylation percentage, and methylated/unmethylated counts per CpG.
    
2. **Coverage → differential methylation (Server B).** The `.cov` files are loaded into a methylKit object, filtered on coverage, normalised, and united across samples; differential testing is then performed either per-CpG (**DMCs**, differentially methylated cytosines) or over genomic tiles (**DMRs**, differentially methylated regions), using one of two engines — **methylKit** (per-CpG Fisher/logistic regression) or **DSS** (beta-binomial dispersion-shrinkage with spatial smoothing).
    
3. **Regions → biology (Server B).** Significant DMCs/DMRs are annotated against bundled UCSC RefSeq gene models and CpG-island tracks (hg38 and mm10) and carried into gene-level and ontology-level interpretation.
    

<mark style="background: #FF5582A6;">The **dividing line between the two servers — the `.cov` coverage file — is also the boundary of what this work exercises on real data.** Aligning full real human WGBS from FASTQ with nf-core/methylseq was estimated at roughly six days per sample on the available workstation (64 GB RAM, 24 cores, no cloud access), so the real-data replications in Chapter 4 begin at the coverage-file stage and Server A's alignment half is demonstrated only at small synthetic scale (Chapter 6). Server A is therefore presented as a _capability_ of the system — fully implemented and runnable locally on small data — rather than as a stage benchmarked on real WGBS. This boundary is made explicit here because it shapes how the validation should be read.</mark>

### 3.1.3 How the layers communicate
- [ ] update with info from mimosa paper. because different agents send each other results etc task⏫ 📅 2026-07-19 

The agent and the servers do not pass large objects to one another in messages. They communicate through two narrow channels, both chosen for reproducibility and for keeping the LLM's context small:

- **Typed tool calls over MCP.** Each server is a FastMCP application speaking the streamable-HTTP transport. Within the Toolomics deployment, `deploy.py` auto-discovers each server's `docker-compose.yml`, assigns it a port in the 5000–5200 range, and brings the container up; Mimosa's port scanner then registers the server's tools automatically, so adding a server requires no change to the agent. Tool results returned to the agent are deliberately small — standard output and error are truncated (4000 characters for the R server) and large artefacts are left on disk rather than returned inline.
    
- **A shared workspace directory.** Both servers mount the same workspace as Mimosa's working directory. State that must persist between steps is written there as files: Mimosa authors R analysis scripts to disk and then asks the server to run them; intermediate methylKit objects are serialised as `.rds` files that later steps reload; figures are written to PDF devices; and an append-only `run_report.txt` records what was decided and done. The guiding rule, stated in the skill, is that _the on-disk file is the deliverable_ — the script a human would review is exactly the script that runs, with no hidden inlined code.
    

### 3.1.4 Design principles

Four principles recur across the components and are stated here because the experiment chapters test whether they deliver the reliability they are intended to provide:

1. **Separate orchestration from execution.** The LLM decides; pinned containers and versioned pipelines execute. Non-determinism is confined to the planning layer, where it can be measured, and kept out of the numerical layer, where it would be fatal.
    
2. **Encode expertise as a skill, not as prompt folklore.** The non-obvious decisions of methylation analysis — which engine suits which coverage/replicate regime, what QC thresholds to apply, which failure modes to guard against — are written once as a declarative skill (§3.4) that the agent consults, rather than being re-derived inconsistently on every run.
    
3. **Offer two tool altitudes — and default to the more reviewable one.** The methylation server's primary surface is deliberately minimal: the agent authors a complete R script and runs it (maximally expressive, and auditable as a single on-disk file). An earlier variant additionally exposed a set of typed atomic tools that each perform one canonical pipeline step (maximally constrained); this alternative is retained in the repository as a record of the design space explored. The trade-off between expressivity and constraint is discussed further in §3.3.1.
    
4. **Make the artefact reproducible by construction.** On-disk scripts, serialised intermediates, pinned environments, and an append-only run log mean that a completed run is, in principle, re-executable and auditable independently of the agent that produced it.
    

The remainder of the chapter examines each layer in turn, beginning with the two MCP servers that constitute the tool layer.

---

## 3.2 MCP Server A — the Nextflow / nf-core/methylseq runner

Server A is the system's upstream component: it converts raw sequencing reads into the per-CpG coverage files that the downstream analysis consumes. It is a FastMCP application (speaking the streamable-HTTP transport, like Server B) that wraps the community-standard **nf-core/methylseq** workflow and exposes its operation — input preparation, execution, monitoring, and teardown — as eight typed tools. The agent does not invoke `nextflow` directly; it composes these tools, and the server constructs the pipeline invocation, selects an execution backend, and reports status.

### 3.2.1 The tool surface

The eight tools fall into three groups — preparing inputs, running and managing the pipeline, and inspecting the environment:

| Tool                       | Group | Purpose                                                                                                                                                                     |
| -------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prepare_methylseq_inputs` | input | Build the nf-core samplesheet (`sample, fastq_1, fastq_2`) from local FASTQ globs, an S3 path, or a list of SRA accessions; auto-detects R1/R2 mate pairs and sample names. |
| `fetch_sra_data`           | input | Download SRA/ENA/DDBJ data via **nf-core/fetchngs**, locally or on the cloud, optionally emitting a methylseq samplesheet on completion.                                    |
| `upload_to_cloud`          | input | Push local files to S3 (`s3://`) or Google Cloud Storage (`gs://`) for cloud execution.                                                                                     |
| `run_methylseq_pipeline`   | run   | Launch **nf-core/methylseq** with full control over aligner, library type, trimming, M-bias correction, reference, and resource limits; supports `resume`.                  |
| `get_pipeline_status`      | run   | Query a running/finished workflow; for cloud runs returns the `session_id` needed to resume, for local runs checks the Nextflow/Singularity install and free disk.          |
| `manage_pipeline`          | run   | Cancel a running cloud workflow or clean Nextflow work/cache directories.                                                                                                   |
| `list_available_resources` | env   | Enumerate accessible Seqera organisations, workspaces, and compute environments.                                                                                            |
| `validate_environment`     | env   | Pre-flight check of every dependency and credential (Nextflow, Singularity, disk, Seqera/AWS tokens) with remediation hints.                                                |

The biologically consequential parameters are concentrated in `run_methylseq_pipeline`. It defaults to the **Bismark** aligner (with `bwameth` and `bismark_hisat` also selectable), accepts a library-type switch covering `rrbs`, `pbat`, `em_seq`, `single_cell`, `accel`, and `zymo` protocols, and exposes the trimming and M-bias-correction knobs that most affect call quality — adapter clipping at either end and the `ignore_r1/r2` and `ignore_3prime_r1/r2` options (the last defaulting to ignoring two bases of read 2, a standard correction for the end-repair bias of directional WGBS libraries). The reference genome is supplied either as an iGenomes identifier (e.g. `GRCh38`, `GRCm39`) or as a custom FASTA, and per-cytosine reporting is enabled by default so that the output is directly consumable by Server B.

### 3.2.2 Two execution backends

A single `execution_mode` argument selects between two backends that the server configures differently:

- **Local execution** runs Nextflow against a **Singularity** container engine on the workstation (`workflow.containerEngine = 'singularity'`), with a per-process resource ceiling that defaults to 16 CPUs and 128 GB of memory and a 24-hour time limit, and a Singularity image cache held in the workspace. The server first checks, via helper functions, that Nextflow and Singularity/Apptainer are installed and that sufficient disk is free.
    
- **Cloud execution** submits the run to the **Seqera Platform** (formerly Nextflow Tower), which dispatches the work to an **AWS Batch** compute environment. The server talks to the Seqera REST API (default endpoint `https://api.cloud.seqera.io`) through a small client that launches workflows, polls their status, and cancels them, reading the workspace and compute-environment identifiers and access token from environment variables.
    

### 3.2.3 Scope exercised in this work

Both backends are implemented, but the compute resources available for this thesis constrain which is exercised. The project workstation has **no Seqera or AWS access**, so the cloud backend is described as a designed capability rather than an exercised path. The local backend is functional, but aligning full real human WGBS from FASTQ with nf-core/methylseq was estimated at approximately **six days per sample** on this hardware, which is infeasible for the multi-sample replications of Chapter 4. Consequently:

- the **real-data replications (Chapter 4 and Chapter 5) start from the published `.cov` coverage files** and do not exercise Server A's alignment stage;
- Server A's full FASTQ → `.cov` path is demonstrated only at **small synthetic scale** (Chapter 6), where a reduced reference and short simulated read sets complete quickly, with an existing small-genome Bismark test run as additional evidence that the local Singularity path is correct end-to-end.

This is the system's principal honesty boundary, and it is stated here, at the description of the component, rather than left to the discussion: the end-to-end claim of the thesis covers the _coverage-to-regions_ analysis on real data and the _reads-to-coverage_ alignment only on small synthetic data.

## 3.3 MCP Server B — the Dockerised R methylKit/DSS runner

Server B is the system's downstream engine: it takes Bismark coverage files and carries them through differential-methylation analysis to annotated, interpreted regions. It addresses a concrete deployment constraint: Mimosa's own execution sandbox installs only Python packages, so the R/Bioconductor stack that the canonical methylation pipeline requires — methylKit, DSS, genomation, and their dependencies — cannot be installed in the agent's local environment, and any analysis script the agent writes would fail at `library(methylKit)`. Server B resolves this by shipping that stack as a service: a Docker image built on **`bioconductor/bioconductor_docker:RELEASE_3_19`** (Bioconductor 3.19) with methylKit, DSS, bsseq, genomation, GenomicRanges, matrixStats, `data.table` (pinned to 1.15.4), dplyr, ggplot2, clusterProfiler, the `org.Hs.eg.db`/`org.Mm.eg.db` annotation databases, and supporting packages pre-installed, plus pre-built UCSC annotation tracks for hg38 and mm10. The agent executes its R code inside this container over MCP and thereby inherits a fixed, reproducible analysis environment.

### 3.3.1 Two altitudes of tools — and the one used here

Server B can present its R environment at two markedly different altitudes. The two are not both live at once; they are two server variants, and the one that produced every run analysed in this thesis is the more minimal of the two.

**The primary surface: write a real script, then run it (two tools).** The production methylation server is _execute-only_. It exposes just two tools, and deliberately nothing more:

|Tool|Purpose|
|---|---|
|`execute_r_script_file(filename)`|**Primary tool.** Run an R script that already exists in the workspace via `Rscript`, with the workspace as the working directory; the execution timeout is set server-side (default 7200 s).|
|`list_workspace_files()`|List the workspace contents, to sanity-check which scripts and inputs are visible before running.|

The server's documentation states the rationale: "No code-string execution, no script-writing, no typed atomic pipeline tools are registered here — that's intentional, so Mimosa commits to _write a real R script file, then run it_ rather than reaching for shortcuts." Two conventions ensure reproducibility. The script the server runs is a real file already on disk — authored by Mimosa with its own file-writing tools — so the script a reviewer reads is identical to the script that executed, with no inlined code. The text returned to Mimosa is capped (standard output and error truncated to 4000 characters, with the full logs left on disk), keeping Mimosa's context small and forcing large results to persist as files rather than pass through the conversation. This minimalism is itself a reliability decision: it removes Mimosa's option to run throwaway code that leaves no auditable trace.
- [ ] atomic tool alternativini başka bir şekilde tanıt. önceden vardı gibi değil de ayrıca bu da var task🔼 ⏳ 2026-07-19 
**The alternative surface: typed atomic tools (a retained variant).** An earlier design exposed the same R stack at a far more constrained altitude. Alongside four generic runners (`execute_r_code`, which saves supplied R to a timestamped file and runs it; `write_r_script`; `execute_r_script_file`; and `list_workspace_files`), it registered a set of typed _atomic_ tools that each perform one canonical pipeline step and validate their inputs. Each is a thin wrapper that invokes a corresponding `r_scripts/*.R` helper with a JSON argument blob and parses a structured result the helper prints inside a `<<<RESULT>>>…<<<END>>>` footer — so the agent receives, for example, the number of sites tested and the number significant at q < 0.05, not free text. This variant is retained in the repository (`old_server_with_atomicTools`) as an alternative design that prioritises constraint over expressivity. Its fourteen atomic tools cover the whole methylKit workflow:

|Tool|Pipeline step|Key defaults|
|---|---|---|
|`load_bismark`|read `.cov` into a `methylRawList`|`min_cov=10`, `assembly="hg38"`|
|`qc_per_sample`|per-sample methylation/coverage QC plots|—|
|`filter_coverage`|`filterByCoverage`|`lo_count=10`, `hi_perc=99.9`|
|`normalize_coverage`|`normalizeCoverage`|`method="median"`|
|`unite_samples`|`unite` to a `methylBase`|strict intersect unless `min_per_group` set|
|`sd_filter`|drop low-variance CpGs|`sd_cutoff=2.0` (pts)|
|`qc_sample_structure`|correlation / clustering / PCA|—|
|`calculate_dmc`|per-CpG `calculateDiffMeth` (paired via `covariates`)|`overdispersion="MN"`, `adjust="BH"`|
|`tile_methyl_counts`|`tileMethylCounts` + `unite`|`win=500`, `step=500`, `cov_bases=5`|
|`calculate_dmr`|DMR via tiled `calculateDiffMeth`|`overdispersion="MN"`, `adjust="BH"`|
|`get_methyl_diff`|extract significant + write CSV/bedGraph|`difference=10`, `qvalue=0.05`|
|`annotate_methyl_diff`|gene + CpG-island annotation|`assembly`-resolved BEDs|
|`export_methyl_diff`|flat CSV with per-group mean beta|—|
|`list_methylkit_objects`|inspect `.rds` objects in the workspace|utility|

### 3.3.2 State flow via `.rds` files
- [ ] bu başlığa çok gerek yok gibi task🔽 
The atomic tools do not hold state in memory between calls; they pass it through the filesystem. Each step reads one or more `.rds` files (serialised R objects) from the workspace and writes its output as another `.rds`, so a fallback analysis is an explicit chain of files:

```
load_bismark        → methylkit_raw.rds         (methylRawList)
  filter_coverage   → methylkit_filtered.rds    (methylRawList)
  normalize_coverage→ methylkit_normalized.rds  (methylRawList)
  unite_samples     → methylkit_united.rds      (methylBase)
  calculate_dmc     → methylkit_myDiff.rds      (methylDiff)
  get_methyl_diff   → significant.csv
  annotate_methyl_diff / export_methyl_diff → annotation.pdf, results.csv
```

DMR analysis branches from the normalised object through `tile_methyl_counts` → `calculate_dmr`. Because each intermediate is named and typed, a run that fails partway can be resumed: `list_methylkit_objects` reports the class of every `.rds` already present, letting the agent identify the right input for the next step rather than recomputing the expensive differential test. The same `.rds` discipline reappears in the execute-only design of §3.3.1, by convention rather than enforcement: the agent's own scripts serialise their intermediates.

### 3.3.3 Bundled annotation and its resolution

Biological annotation is the last stage of the pipeline, and the image ships the reference tracks it needs so that annotation runs offline: pre-built UCSC RefSeq gene models and CpG-island BEDs for both assemblies, at `/opt/annotations/` — `hg38_refseq_genes.bed` (BED12 transcripts) and `hg38_cpg_islands.bed` (BED4), with `mm10` equivalents. `annotate_methyl_diff` resolves them in a fixed order: an explicit `refseq_bed`/`cpg_bed` path wins; otherwise an `assembly` of `hg38` or `mm10` selects the bundled file; otherwise the tool errors rather than guessing. Other assemblies (hg19, mm9, custom genomes) require the user to supply BED files in the workspace. The gene databases `org.Hs.eg.db` and `org.Mm.eg.db` are likewise bundled, so gene-ontology enrichment runs without network access, whereas KEGG enrichment, which queries a live service, does not.

### 3.3.4 Deployment

Server B requires no change to the Toolomics control plane to come online. `deploy.py` auto-discovers the server's `docker-compose.yml`, assigns it a free port in the 5000–5200 range, and starts the container; Mimosa's port scanner then finds the server and registers its tools automatically — the two of the execute-only server used throughout this thesis, or the fuller set of the retained atomic-tool variant. The image is comparatively expensive to build the first time — installing the Bioconductor stack and downloading the UCSC annotations takes roughly 15–30 minutes — but the result is cached, so this cost is paid once rather than per run.

## 3.4 The skill as router and guardrail

The two MCP servers provide Mimosa with _capabilities_; the **skill** provides it with _judgement_. It is a declarative document — a structured Markdown file Mimosa reads — that encodes the domain expertise a methylation analyst would otherwise supply by hand on every run: which differential-methylation engine fits the data, what quality-control thresholds to apply, which non-obvious pitfalls to avoid, and how to structure a reproducible project. In the layered architecture of §3.1, the skill constitutes the knowledge layer that sits between Mimosa and the tools, shaping _how_ the tools are used without itself executing anything. Its design rationale corresponds to principle 2 of §3.1.4: expertise written once and consulted consistently, rather than re-derived inconsistently by the LLM on each run. Whether this consistency materially reduces run-to-run variance is a question the experiment chapters are positioned to address.

### 3.4.1 The central decision: engine selection

The skill defines its most consequential function as routing between the two engines before any analysis code is written. methylKit and DSS embody different statistical trade-offs: methylKit performs direct per-CpG tests and is well-powered when coverage and replicate counts are high, whereas DSS borrows information across neighbouring CpGs through spatial smoothing and shrinks dispersion across the genome, recovering signal at low coverage or with few replicates that per-CpG tests miss. The skill encodes this distinction as an explicit decision table keyed on coverage and replication:

|Coverage / replicates|Engine|
|---|---|
|≥10× **and** ≥4 replicates/group (high power)|methylKit (`calculateDiffMeth`, `overdispersion="MN"`); DSS also fine|
|5–10×, **or** 2–3 replicates/group|**DSS** (dispersion shrinkage + smoothing)|
|Sparse WGBS, single-CpG resolution wanted|**DSS** with `smoothing=TRUE`|
|Multifactor / covariate-adjusted / paired design|**DSS `DMLfit.multiFactor`** _or_ methylKit `covariates=`|
|<5× or n=2|DSS `equal.disp=TRUE`, or Fisher's exact (methylKit) — exploratory only|

The skill's guidance at the boundary between engines is to run both and treat the concordant DMRs as the confident calls — a built-in form of the cross-method agreement that the experiment chapters also employ as a concordance axis.

### 3.4.2 Progressive disclosure: the hub and the reference files

The skill is organised so that only a small, always-relevant core is loaded into the agent's context by default, with depth pulled in on demand. The hub document owns the shared, engine-agnostic workflow — the execution model, input and aligner detection, file-format definitions, metadata handling, QC thresholds, annotation, interpretation, visualisation, and project structure — and the engine-selection decision above. The command-level depth for each engine lives in two separate reference files, `references/methylkit.md` and `references/dss.md`, which the skill instructs the agent to read **only after it has chosen an engine**. This keeps the resident context compact and avoids loading, say, the full DSS multifactor-GLM reference during a run that uses methylKit.

### 3.4.3 Failure modes as guardrails

A distinctive feature of the skill is that a substantial portion of it catalogues _failure modes_ — the non-obvious facts that, in the authors' experience, cause the most analyses to fail silently. By stating them where the agent will read them, the skill converts hard-won debugging knowledge into preventive guardrails. The most important are:

- **Derive groups from metadata, never hard-code them.** Treatment/group vectors must come from a `metadata.csv`; if it is missing, the agent is told to halt and ask rather than guess.
- **Cap the core count.** `parallel::detectCores()` reports the host's CPUs, not the container's cgroup limit, so naive parallelism oversubscribes inside Docker; the skill prescribes a capped `mc.cores`/`ncores` and lower still on genome-wide objects whose memory scales with cores.
- **Do not double-smooth DSS.** DSS smooths internally, so the raw `BSseq` must be passed to its test; pre-running `bsseq::BSmooth` is a silent statistical error.
- **Counts are required for count-based tests.** A bedGraph that carries only methylation percentages, without methylated/unmethylated counts, is unusable for DSS or methylKit's logistic/Fisher tests.
- **Use exact annotation filenames, never mix aligners, and always send plots to a file device** — the MCP returns text, not graphics.

The QC thresholds the skill fixes are similarly concrete and engine-agnostic: bisulfite conversion inferred from CHH methylation below ~1%, mapping rate above 70%, at least ~1 million covered CpGs per WGBS sample, replicate correlation above r ≈ 0.95, and the expectation that replicates cluster together in PCA with no batch separation — with the standing instruction to flag and confirm with the user before excluding any sample.

### 3.4.4 Project structure and the run report

Finally, the skill prescribes a fixed project layout — `raw_data/`, `metadata.csv`, `config.yaml` (genome, engine, coverage, effect-size and FDR thresholds, tile size, smoothing), numbered `scripts/`, a `results/` tree, and an **append-only `run_report.txt`** in which each step records the mode and engine chosen, the files found, the steps run or skipped, and any samples excluded. The append-only run report is both a reproducibility aid and a source of evidence about what the agent actually decided on a given run.

## 3.5 The Mimosa agent — framework, loop, goal evolution, and the workspace contract

The previous sections described the _capabilities_ the agent acts through and the _knowledge_ that shapes how it acts. This section describes the actor itself. **Mimosa** is the host laboratory's open-source framework for autonomous scientific research (Legrand et al., 2026); this thesis does not introduce it but adopts it as the agent under test. The methylation-specific components that surround it — enumerated in the contribution note of §3.0 — are this thesis's own work, and the validation of the integrated system on DNA-methylation analysis is its purpose. An accurate description of Mimosa is necessary for the validation that follows, because the system extends beyond the "read goal → call tool → observe → repeat" loop sketched in §3.1.1: that loop is what an _execution agent_ performs within a single workflow, but Mimosa as a whole is a system that **synthesises the workflow itself** and can **evolve it across generations**. Both properties bear directly on reliability and are therefore presented here rather than abstracted away.

### 3.5.1 What Mimosa is: a workflow-synthesising, self-evolving framework

Mimosa's self-description is precise: it "writes a custom multi-agent workflow per task, runs it in a sandbox, checks what the agents actually did against independent vantage points, and evolves the workflow across generations with a Quality-Diversity inspired search." Given a task — here, "analyse this folder of WGBS coverage files and call differential methylation" — it does not execute a fixed program but rather _synthesises_ one. The framework is organised in five layers, connected through small dataclass schemas:

|Layer|Component|Role in a methylation run|
|---|---|---|
|0|**Planner** _(optional; `--goal` mode only)_|Decomposes a high-level objective into discrete tasks. Bypassed for the single-task methylation goal used here.|
|1|**ToolManager + Perspicacité**|Scans the configured address/port range (`0.0.0.0:5000–5100`) and registers every MCP tool it finds — the two Toolomics servers of §3.2–3.3 — and, when the Perspicacité literature service (§3.7) is running, can pull supporting literature.|
|2|**EvolutionEngine**|Synthesises the workflow as Python source and, in `--learn` mode, evolves it across generations (§3.5.3).|
|3|**WorkflowRunner**|Executes the synthesised workflow in a sandbox built on Hugging Face **SmolAgents** (a `LocalPythonExecutor` with an AST allow-list) over shared **LangGraph** state. The execution agents inside this sandbox are what call the MCP tools and write the R scripts of §3.3–3.4.|
|4|**VerifierEvaluator**|After each run, scores the workspace from six independent vantage points (§3.5.4) and feeds the next mutation.|

The design commitment that distinguishes Mimosa from a scripted pipeline — and the one most relevant to a reliability evaluation — is **code-as-genotype**: each synthesised workflow is a complete, standalone Python program emitted to disk (no domain-specific language, no YAML), so "any generation can be inspected, diffed, or re-run standalone." The program is the unit that is stored, mutated, and audited. Its _phenotype_ is whatever it produces in the shared workspace: the `.rds` intermediates, figures, tables, and `run_report.txt` of §3.1–§3.4.

### 3.5.2 Execution modes and the run regime used in this thesis

Mimosa exposes several modes, selected by command-line flag. The two axes that matter here are **planning** (`--task` for a single focused operation versus `--goal` for a multi-step objective that invokes the planner) and **learning** (`--learn` adds evolution across generations; without it, the framework synthesises and runs a single workflow — "one-shot"). A `--single_agent` mode skips multi-agent synthesis entirely for a fast, learning-free baseline.

It is necessary to state which regime produced the artefacts this thesis analyses. The completed methylation runs (`run5`–`run12`) were predominantly **one-shot, single-task runs with evolution disabled** — the prompt harness (`scripts/run_prompt_ablation.sh`) explicitly invokes `main.py … --max_evolve_iterations 1` so that each goal variant is evaluated in isolation. Evolution is therefore not the default operating mode of the system as validated here; an honest account of Mimosa requires describing the full evolutionary machinery while being explicit that the majority of the evidence derives from its single-shot use.

### 3.5.3 The evolution loop (when `--learn` is enabled)

When evolution is enabled, the workflow program is the thing that evolves. The mechanics, drawn from the framework's evolution engine (`sources/core/evolution_engine.py`), are:

- **Selection — a Quality-Diversity archive** (MAP-Elites-style, maximum population 50). Each workflow is scored as `qd_score = (1 − w)·quality + w·novelty`; novelty is a k-nearest-neighbour distance (k = 25) over a _behaviour descriptor_ `[n_agents, n_edges, n_branches, prompt_chars]`, so the archive rewards structurally distinct workflows rather than collapsing onto one design.
- **Variation — stagnation-driven scope.** Mutation boldness is a continuous function of how much the recent "prompt gradients" repeat: when progress stalls the search widens from a prompt-level tweak toward a complete topology rethink; near-winners are protected. About 30 % of generations use **crossover** of two parents.
- **Cold start.** When the archive is empty, a similarity-filtered scan of past runs on disk (MiniLM cosine ≥ 0.5) seeds the search, so useful workflows transfer across tasks.
- **Termination.** A generation budget (`max_learning_evolve_iterations`, default 45) or an early-stop when the verifier score reaches `learned_score_threshold` (0.94).

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

_(Figure 3.3.) In the one-shot regime used for most runs in this thesis (§3.5.2) the loop runs once, top to bottom; the return path on the right is active only under `--learn`._

### 3.5.4 The multi-source verifier — what a "success" actually means

The component most directly aimed at trustworthiness is the verifier, and it represents the point at which Mimosa departs most sharply from agents that grade themselves. After each run, **six independent claim sources** inspect the workspace and emit success-polarity claims, and — critically — each claim is checked by a **Python program the judge writes against the workspace, not by re-querying an LLM about whether it believes the agent**:

|Source|Vantage|
|---|---|
|**A**|Peer-reviewed practice, grounded in the literature via Perspicacité (§3.7).|
|**B**|The literal goal text — whether the agents delivered what was asked.|
|**C**|Agent narration — whether the numbers and artefacts the agent _claims_ can be reproduced from what is on disk.|
|**D**|Mathematical invariants — probabilities in [0, 1], shape consistency, no NaNs.|
|**E**|Computational reproducibility — declared dependencies cover the imports actually used, no absolute paths, seeds set on stochastic operations.|
|**F**|Statistical fingerprint — beats a baseline, no degenerate predictions, no leakage signatures.|


### 3.5.5 The model configuration and the goal specification
- [ ] Bu increasing goal fikri çöp oldu sanki. paper replicationları single shot + learning koyarım paperdaki parametreleri kullan diyerekten fln task⏫ ⏳ 2026-07-19 
**Models.** Mimosa is multi-model by design: distinct LLMs fill distinct roles, each configured in `config.py` and routable through OpenRouter via litellm. At the time of writing, the configured defaults are a GLM-5.1 **planner**, a Claude Opus 4.5 **workflow synthesiser** (the model that writes the pipeline code), a DeepSeek-v4 **execution-agent** model, and a Qwen **judge** that writes the verifier programs; generation uses `reasoning_effort = "medium"` and `max_tokens = 8192`. These are configuration fields, not hard-coded choices — any role can be repointed at another provider — and a controlled experiment should **pin a single, fixed configuration** across its repeated runs so that observed variance is attributable to the agent's non-determinism rather than to a changing model target. (This pinning supersedes the earlier project assumption of a single fixed Sonnet model: the system is genuinely multi-model, and the experiment controls for this rather than the system embodying it.)

**The goal as the task contract.** Within a run, the agent is steered by a single _goal file_ — a plain-text task specification provided alongside the data. The goal is where the methylation task is made concrete, and tightening it in response to observed failures is itself part of the engineering contribution of this thesis. Six versions exist (`tools/goals/goal_v1…goal_v6`), and their progression constitutes a compact record of what an LLM agent requires to be told before it analyses WGBS data reliably:

|Goal|What it adds relative to the previous version|
|---|---|
|**v1** minimal|The bare task: from Bismark `.cov` files, call DMCs and DMRs between two groups; read group labels from a samplesheet.|
|**v2** outputs|An explicit required-output list — DMC/DMR tables, a DMC volcano, per-sample and sample-structure QC, and an append-only `run_report.txt`.|
|**v3** MCP|The hard execution constraint: **all R runs through the methylation MCP server**, never locally; author a real `.R` script and execute it; inspect large files with `head`/`zcat`, never open them whole.|
|**v4** methodology|Concrete statistics: `pipeline="bismarkCoverage"`, 10× coverage filter, trim the top 0.1 %, median normalisation, an SD pre-filter, a **paired** test with the donor as a covariate (`overdispersion="MN"`), and dual reporting thresholds (lenient \|Δβ\|≥10 %, strict ≥25 %, both q<0.05).|
|**v5** repository|A reproducible project contract: `config.yaml`, an input-detection step that emits `input_manifest.json`, numbered scripts `00_detect_inputs.py … 04_enrichment.R`, a `run_pipeline.sh` driver, and a machine-parseable `STEP_SUMMARY …` line on each script's final stdout.|
|**v6** corrected|Corrections of recurring agent errors: affirm that methylKit _does_ support paired designs, fix the DMR tile width at 500 bp (not 1000), enforce the **canonical** bundled BED filenames, and add TSS-distance tables for the strict DMC set.|

The trajectory is from _what to do_ (v1–v2) to _how to run it reproducibly_ (v3, v5) to _exactly which statistics, corrected against observed mistakes_ (v4, v6). The dual-threshold reporting and the paired-design instruction in particular are direct responses to the analysis requirements of the Chapter 4 replications.

_(Table 3.1.) The goal-evolution changelog; the final version cites line ranges in each goal file._

### 3.5.6 The workspace contract and the audit trail

**The workspace contract.** Agent and tools do not exchange large objects in messages; they share a single workspace directory (configured as `workspace_dir`) and communicate through files, as introduced in §3.1.3. A run materialises a predictable tree: the input-detection step writes `input_manifest.json` (one record per sample: `sample_id`, `file_path`, `group`, a `treatment` code, and capability flags), so that no downstream script hard-codes sample names or group membership; the numbered R scripts read the manifest and `config.yaml`, write their `.rds` intermediates and figures, and append to `run_report.txt`. This file-on-disk contract is what makes a completed run independently re-executable and, also what makes its failures externally auditable.

**The audit trail.** Because Mimosa is designed for scientific use, every generation is recoverable after the fact. For each synthesised workflow the framework persists, under `sources/workflows/<uuid>/`: the exact executed Python (`workflow_genotype_<uuid>.py`), the lineage and operator that produced it (`lineage_<uuid>.json`: parents and `seed | mutation | crossover`), the exact LLM prompt that generated it (`evolution_prompt_<uuid>.md` — "same prompt + seed = same code"), per-iteration metrics (`run_metrics.json`: wall time, cost, scores), and the abstracted gradient. Companion tools (`memory_explorer.py`, `memory_timelapse.py`, a RAG-backed `--memory_cli`) allow stepping through a run's full trace. The sandbox executes under explicit resource ceilings set in `config.py` — a per-workflow runner timeout of 10 800 s (3 h), a per-agent execution timeout of 21 600 s (6 h), and a 10 GB memory cap — and an insufficiently set timeout is shown by the run archive to be the operational cause of several earlier run failures.

---

## 3.6 [EDITORIAL NOTE — SECTION CONTENT MISSING FROM SOURCE FILE] #update

> **This section is a placeholder, not finished prose.** §3..6 is described in §3.0's chapter outline and cross-referenced seven times elsewhere in this chapter and in Chapter 2, but no actual section body was present in the file supplied for this edit — the document currently jumps from §3.5.6 straight to §3.7. I have not invented the missing content, since it concerns specific empirical findings (bug reports, failure counts, timeout evidence) that only you can supply accurately; fabricating plausible-sounding specifics here would misrepresent your own results. Below is a reconstruction, from the forward-references scattered through the rest of the thesis, of what this section needs to contain and roughly how it is already being cited — use it as a checklist and drop your actual material into the matching subsection. Once you paste in the real content, I can polish it to match the rest of the chapter in the same pass.

Reconstructed scope, by forward-reference:

- **§3.0 (chapter outline):** "§3..6 collects the reliability-engineering guardrails and instrumentation that the experiment chapters draw upon," described in the contribution note as "this thesis's own methodology for making the agent's trustworthiness measurable."
- **§3.5.4 (verifier, Source C):** "Source C is exactly the check that the run-to-run failures of §3..6 violate: an agent can write '1816 significant DMRs' into a report, but Source C asks whether that number survives contact with the files on disk." This section needs the actual worked example(s) of a self-reported number that did not survive an on-disk check.
- **§3.5.4–3.5.5 boundary:** "the methylation-specific sanity assertions of §3..6 are best understood as a domain-tuned extension of Sources C, D and F… the §3..6 assertions check that _this_ number is biologically and arithmetically possible (a tile count cannot be smaller than the number of significant tiles it contains)." This section needs the actual list of domain-specific sanity assertions coded into the pipeline, of which the tile-count example is one instance.
- **§3.5.6 (workspace contract):** "This file-on-disk contract is what makes a completed run independently re-executable — and, as §3..6 shows, also what makes its failures externally auditable" — and later, in the same subsection, that "an under-set timeout is shown by the run archive to be the operational cause of several earlier run failures." This section needs the concrete audit-trail walkthrough (which failed run, which archived artefact revealed the cause) that substantiates both claims.
- **Chapter 2, §2.5 ("The reliability problem"):** "The concrete failures documented in §3..6 — the same input yielding results that differ by orders of magnitude, an impossible region count carried into a biological conclusion — are precisely this problem in the methylation domain." This section needs the specific run(s) and numbers behind that "orders of magnitude" claim.

A plausible internal structure, following the pattern of the rest of the chapter, would be:

**3.6.1 Domain-specific sanity assertions.** The pipeline-level invariants layered on top of the generic verifier (§3.5.4) — e.g., tile counts, significant-CpG counts, and effect-size ranges checked against what is arithmetically or biologically possible given the input data.

**3.6.2 Run-to-run variance and self-reported claims that do not survive audit.** The worked example(s) behind the "1816 significant DMRs" and "orders of magnitude" references — presented as a table or short case study of claimed vs. disk-verified results.

**3.6.3 Timeout ceilings and the audit trail in practice.** The specific run(s) that exhausted the 10 800 s / 21 600 s ceilings of §3.5.6, and how the archived lineage/prompt/metrics files (`lineage_<uuid>.json`, `run_metrics.json`, etc.) were used to diagnose them.

---

## 3.7 Situating Mimosa in the Holobiomics Lab ecosystem

Mimosa and the two Toolomics servers are not isolated artefacts; they belong to a small family of laboratory tools, two of which are described here because they are wired into the system described above and because they frame the future work developed in Chapter 8 (Conclusions). They are summarised only to the depth required for that purpose; neither is itself under validation in this thesis.

**Perspicacité — literature grounding for the verifier.** Perspicacité is a local-first retrieval-augmented-generation service for academic literature: it ingests papers from sources such as Semantic Scholar, OpenAlex, PubMed and arXiv (via the SciLEx multi-database search layer), indexes them with vector embeddings in a local ChromaDB store alongside BM25, and exposes the result as MCP tools and a REST API. Its role in this work is specific and bounded: it is the service behind **Source A** of Mimosa's verifier (§3.5.4) — the "peer-reviewed practice" vantage — and Mimosa discovers and uses it automatically when it is running. It is named here, rather than folded silently into the verifier, partly because it is part of the same ecosystem and partly because two concrete fixes to it form part of this thesis's engineering contribution: making the LLM-provider selection honour the configuration file rather than a hard-coded default, and repairing the SciLEx adapter to load via path injection rather than assuming an installed package.

**Indicium — the claim-standardisation layer and the multi-omics bridge.** Indicium is a small, versioned vocabulary standard for a _typed scientific claim bound to the evidence that grounds it_, with provenance stamps, from which Pydantic models, JSON-Schema, SHACL and OWL are generated. Around it sits an adapter framework (`indicium-adapters`) whose domain plug-ins enrich raw claims with ontology terms; the **epigenomics** adapter handles exactly the claim types this thesis produces (WGBS, and methylation-array assays — resolving assay names, assemblies, and probe identifiers to controlled vocabularies), while a sibling **metabolomics** adapter does the same for that domain. This epigenomics adapter is itself one of the thesis's contributions (§3.0): it is the concrete point at which the methylation work plugs into the shared claim standard, and so the most tangible piece of the multi-omics bridge that Chapter 8 develops. Indicium is not used to _run_ any analysis here — it explicitly does not call DMRs or align reads — and so it is not part of the system under test. It is described because it is the concrete substrate of the thesis's framing claim: methylation is positioned as the **validated first vertical** of a system designed to extend, through a shared claim standard, toward transcriptomics and metabolomics. The benchmark-construction toolkit AgenticScienceBuilder, which turns published papers into machine-readable evaluation tasks against this same standard, completes the ecosystem but is otherwise out of scope.