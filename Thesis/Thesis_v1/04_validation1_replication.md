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

---

## 4.1 Study A — Human *AKAP11* heterozygous knockout (GSE263850)

### 4.1.1 Dataset and biological context

The data for Study A are drawn from Farhangdoost et al. (2025), *Molecular Psychiatry*
30:4543–4557, deposited in the Gene Expression Omnibus as GSE263850. The study investigated
genome-wide DNA methylation changes in human induced pluripotent stem cell (iPSC)-derived
cortical neurons carrying a heterozygous CRISPR-mediated knockout of *AKAP11*, a gene whose
loss-of-function variants are among the strongest known risk factors for both bipolar disorder
and schizophrenia. The experimental design is a simple two-group comparison:

| Group | Genotype | Samples |
|---|---|---|
| Knockout (KO) | Het-*AKAP11*-KO | 3 clones (Clone 16, 20, 21) |
| Wild-type (WT) | Unedited iPSC-derived neurons | 3 replicates (SBP009 ×3) |

The WGBS libraries were sequenced at high depth, aligned with Bismark, and yielded Bismark
coverage files deposited in GEO. These six `.cov.gz` files — approximately 24 million CpGs each
— are the common starting material for all three analysis arms.

The published analysis used the DSS Bioconductor package with a multi-factor beta-binomial
model, smoothing enabled, `p.threshold = 1e-5` (raw per-CpG *p*-value), and no effect-size
minimum (`delta = 0`), with adjacent significant CpGs merged at ≤100 bp. The paper reported
**813 DMRs** (638 hypermethylated, 175 hypomethylated), **705 associated genes** (±100 kb from
TSS via ChIPseeker), and highlighted convergent DMR–H3K27ac–DEG evidence at gold-standard loci
including *IRX2*, *CLEC19A*, and *KANK1*.

### 4.1.2 The three analysis arms

The replication is conducted as three independent analyses of the identical six coverage files,
differing only in who or what chose the analysis parameters:

**Arm 1 — Published results (paper).** The expected reference: the 813 DMRs, 705 genes, and
enriched pathways reported by Farhangdoost et al. (2025). These are taken as the target of
replication, not as ground truth — the paper's own analysis is one defensible choice of
parameters among several.

**Arm 2 — Expert re-analysis (baseline).** A 531-line monolithic R script written by a human
analyst with the explicit goal of replicating the published analysis faithfully. It uses:

- `DMLfit.multiFactor()` + `DMLtest.multiFactor()` (DSS's multi-factor interface),
- the paper's exact parameters: `smoothing = TRUE`, `p.threshold = 1e-5`, `delta = 0`,
  `dis.merge = 100`, `minlen = 50`, `minCG = 3`, `pct.sig = 0.5`,
- ≥5× per-sample coverage filter (matching the paper),
- ChIPseeker annotation with a ±100 kb TSS window,
- ReactomePA pathway enrichment with an explicit gene universe.

**Arm 3 — Mimosa pipeline.** The Mimosa agent, given a natural-language goal, operated with Quality-Diversity evolution. The pipeline it synthesized is a five-script modular design:

- `01_load_and_qc.R` — load, coverage filter (≥10×), QC plots (PCA, heatmap, dendrogram),
- `02_differential_methylation.R` — `DMLtest()` (simple two-group), chromosome-by-chromosome to avoid OOM, with `p.threshold = 0.05`, `delta = 0.25`, `dis.merge = 1000`,
- `03_annotate.R` — genomation-based annotation (promoter/exon/intron/intergenic + CpG island
  overlap),
- `04_enrichment.R` — GO Biological Process + KEGG enrichment via clusterProfiler,
- `validate_pipeline.R` — automated sanity checks (sample counts, p-value range, output file
  existence).

<mark style="background: #FF5582A6;">The agent's pipeline differed from the paper's in several consequential parameters, which are
analysed in §4.1.4. Critically, run23 is the first agentic run in this thesis's experimental
series to complete the full analysis cycle end-to-end without crashes, OOM failures, or
simulated-data fallbacks — a trajectory documented in §3.6 and revisited in §4.1.8.</mark>

### 4.1.3 Headline results

Table 4.1 summarizes the DMR-level output of each arm.

**Table 4.1.** DMR counts and region statistics across the three arms, Study A.

| Metric               |     Paper |  Baseline |            Mimosa |
| -------------------- | --------: | --------: | ----------------: |
| **Total DMRs**       |       813 |       921 |             4,812 |
| **Hypermethylated**  | 638 (78%) | 685 (74%) |       2,182 (45%) |
| **Hypomethylated**   | 175 (22%) | 236 (26%) |       2,630 (55%) |
| **Associated genes** |       705 |       825 | — (gene_name bug) |
| Median region length |         — |    242 bp |            285 bp |
| Mean region length   |         — |    293 bp |            346 bp |
| Median CpGs/region   |         — |         5 |                 6 |
| Total bp covered     |         — |   270,068 |         1,665,686 |

The baseline produces 921 DMRs — a 13% overshoot of the paper's 813, within the range of
variation expected from minor implementation differences (e.g. Bioconductor version, exact
coverage at boundary CpGs). The agent produces 4,812 DMRs — a 5.9× overshoot. This inflation
is the chapter's first major finding and is traced to specific parameter differences in
§4.1.4.

### 4.1.4 Parameter analysis — the sources of divergence

Table 4.2 catalogues the parameter differences between the baseline and the agent, alongside
their impact.

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
function expects a raw per-CpG *p*-value threshold; the agent pipeline passes its configured
FDR cutoff (0.05) into this slot. This makes the per-CpG inclusion criterion approximately
5,000 times more permissive than the paper's `1e-5`, which is the primary driver of the DMR
count inflation. The agent's stricter effect-size filter (`delta = 0.25` versus `delta = 0`)
partially offsets this by rejecting small-effect CpGs, but clearly does not compensate for the
p-value looseness. The `dis.merge = 1000` setting further inflates counts by merging CpGs up to
10× farther apart into single regions.

This is a semantic mismatch — the agent treated a conceptually correct FDR threshold as if it
were a raw *p*-value — and is precisely the kind of "plausible wrong answer" described in §1.4.
Its detection required the triangulated comparison design: within the agent's output alone, the
4,812 DMRs are internally consistent and pass the pipeline's own validation, and only the
juxtaposition with the baseline and the paper reveals the inflation. This observation is
returned to in §6 (Discussion).

### 4.1.5 Direction labeling — a systematic inversion

Among the 791 overlapping DMR pairs between the baseline and agent output, the direction of
effect is **100% inverted**, with zero exceptions:

**Table 4.3.** Direction concordance for overlapping DMR pairs.

| Agent label | Baseline label | Count |
|---|---|---:|
| Hypo | Hyper | 607 |
| Hyper | Hypo | 184 |
| Hyper | Hyper | 0 |
| Hypo | Hypo | 0 |

This is not biological discordance but a labeling convention difference. The baseline's
`DMLfit.multiFactor()` computes coefficients as *treatment − control* (KO − WT), so a positive
`areaStat` indicates higher methylation in the KO — hypermethylation. The agent's `DMLtest()`
was called as `DMLtest(group1 = ctrl, group2 = treat)`, so its `diff.Methy` represents
*control − treatment* (WT − KO) — flipping the sign. The 100% inversion confirms the two
pipelines agree on the biology for every shared region; the labels are simply opposite.

<mark style="background: #FF5582A6;">
This finding motivated the sign-canonicalisation library described in §3.6: without
standardising the direction convention *before* computing any concordance score, an analysis
that agreed perfectly on the biology would appear to disagree perfectly on direction. The
canonicalisation forces all comparison arms onto a single convention (KO − WT = positive →
hypermethylation) before any metric is computed.</mark>

### 4.1.6 Overlap and concordance

Having noted the direction inversion, we now assess positional concordance — whether the two
pipelines identify the same genomic loci as differentially methylated.

**Table 4.4.** Overlap between the baseline and agent DMR call sets.

| Comparison | Result |
|---|---|
| Baseline DMRs recovered by agent | **791 / 921 (85.9%)** |
| Agent DMRs supported by baseline | 764 / 4,812 (15.9%) |
| Agent-only DMRs (no baseline match) | 4,048 (84.1%) |

The asymmetry is the expected consequence of the call-set size difference: the baseline's
smaller, higher-confidence set is almost entirely (86%) recovered within the agent's larger set,
while the reverse is naturally much lower. This pattern — high recall, low precision relative
to the baseline — is the signature of a permissive threshold.

More informatively, the quality of the agent's calls correlates with their corroboration:

**Table 4.5.** Properties of agent DMRs that overlap vs. do not overlap the baseline.

| Property | Overlapping (n = 764) | Non-overlapping (n = 4,048) |
|---|---:|---:|
| Median |areaStat| | 56.8 | 24.7 |
| Median nCG | 7 | 6 |
| Median region length | 372 bp | 274 bp |
| Median baseline overlap | 78% | — |

The agent's **strongest calls** — those with the largest effect sizes, most CpGs, and broadest
regions — are disproportionately the ones confirmed by the baseline. This indicates that the
agent's internal ranking of its calls is sound; the problem is the threshold at which the list
is cut, not the ranking above it.

### 4.1.7 Gene recovery and biological concordance

Gene-level concordance is assessed for the paper's gold-standard loci — genes with convergent
DMR + H3K27ac + DEG evidence — and for the top hypermethylated hits.

**Table 4.6.** Recovery of key genes across analysis arms.

| Gene        | Paper status                        | Baseline                               | Agent                               |
| ----------- | ----------------------------------- | -------------------------------------- | ----------------------------------- |
| **IRX2**    | Gold standard (DMR + H3K27ac + DEG) | ✅ Found (Hyper; 3'UTR/Promoter/Intron) | ✅ Found (via enrichment re-overlap) |
| **CLEC19A** | Gold standard                       | ❌ Not found                            | ❌ Not found                         |
| **KANK1**   | Gold standard                       | ❌ Not found                            | ❌ Not found                         |
| OTX1        | Top hypermethylated                 | ✅ Found (Hyper; Exon/Intergenic)       | ✅ Found (via enrichment)            |
| NR2E1       | Top hypermethylated                 | ✅ Found (Hyper; 5'UTR)                 | ✅ Found (via enrichment)            |
| PAX7        | Top hypermethylated                 | ✅ Found (Hyper; Intergenic)            | Unknown (gene_name empty)           |
| ENPP2       | Top hypermethylated                 | ✅ Found (Hyper; Promoter)              | Unknown (gene_name empty)           |
| CCDC177     | Top hypomethylated                  | ✅ Found (Hyper — contradicts paper)    | ✅ Found (via enrichment)            |
| DMRTA2      | ORA-enriched                        | ❌ Missing from baseline                | ✅ Found (via enrichment)            |

Two patterns emerge. First, neither the baseline nor the agent recovers *CLEC19A* or *KANK1* —
two of the paper's three gold-standard genes. This likely reflects a real methodological
difference: the paper's gene-association strategy (±100 kb from TSS) links distant DMRs to
genes that a direct-overlap annotation would not capture, and these two genes may fall in that
gap. That neither arm finds them suggests the ceiling for gene recovery under direct-overlap
annotation is below 100%, which sets an honest upper bound for the agent comparison.

Second, the agent's enrichment step (`04_enrichment.R`) independently re-computes DMR–gene
overlaps and *does* recover key genes like *IRX2*, *NR2E1*, *CCDC177*, and *DMRTA2* — but
because the `gene_name` column in the annotated DMR output is empty for all 4,812 rows (a
confirmed annotation bug — see §4.1.9), these genes cannot be traced back to specific DMR
coordinates without re-running the annotation step. This reduces the utility of the agent's
output for gene-level biological interpretation.

### 4.1.8 Enrichment concordance — biological pathways

Despite the different enrichment frameworks — Reactome (baseline) versus GO + KEGG (agent) —
and the different gene sets (305 symbols from ±100 kb TSS versus 2,444 Entrez IDs from direct
overlap), both analyses converge on the same broad biological themes:

**Agent's top GO Biological Process terms:**

1. Pattern specification process (*p*~adj~ = 4.37 × 10^-20^)
2. Embryonic organ development (*p*~adj~ = 1.35 × 10^-16^)
3. Regionalization (*p*~adj~ = 1.20 × 10^-15^)
4. Skeletal system development (*p*~adj~ = 7.58 × 10^-15^)

**Agent's top KEGG pathways:**

1. Neuroactive ligand–receptor interaction (*p*~adj~ = 3.00 × 10^-7^)
2. Calcium signalling pathway (*p*~adj~ = 1.89 × 10^-5^)
3. Axon guidance (*p*~adj~ = 6.80 × 10^-5^)

Both pipelines highlight neural and developmental pathways, which is biologically consistent
with the study's context — *AKAP11* knockout in iPSC-derived cortical neurons, a model for
bipolar disorder and schizophrenia. The enrichment concordance is arguably the most robust form
of agreement between the arms, because pathway-level results are buffered against individual
gene-level differences by the aggregation inherent in enrichment analysis.

Two caveats apply. First, the agent's enrichment used the default gene universe (all annotated
genes) rather than an explicit universe of genes tested, which inflates enrichment significance
(a known over-representation analysis pitfall). Second, the agent's gene set is derived from
19,525 overlapping RefSeq transcripts rather than the 705 genes in the paper, so the
denominator is very different; the fact that the top terms still converge on neural/developmental
biology is meaningful precisely because it survives this inflation.

### 4.1.9 Identified agent defects

Three specific defects in the agent's pipeline were identified through the comparison:

**Defect 1: p.threshold / FDR mismatch (severity: high).** As detailed in §4.1.4, the agent
feeds an FDR cutoff (0.05) into DSS's `callDMR(p.threshold = ...)`, which expects a raw
per-CpG *p*-value. This is the primary cause of the 5× DMR inflation.

**Defect 2: Direction inversion (severity: medium).** The agent's `DMLtest()` group-order
convention produces `diff.Methy` with opposite sign from the baseline (§4.1.5). While
internally consistent, any biological conclusion about hyper- versus hypomethylation drawn
directly from the agent's labels would be backwards.

**Defect 3: Empty gene_name column (severity: medium).** In `03_annotate.R`, the `gene_name`
vectors are initialised to empty strings and never assigned gene symbols after annotation.
The genomation-based annotation correctly produces genomic-context categories
(promoter/exon/intron/intergenic) and CpG-island context, but the gene-symbol column remains
blank for all 4,812 DMRs. The pipeline's validation script does not check `gene_name`
completeness, so the bug passes silently.

These defects are consequential for the reliability assessment because all three are *silent* —
the pipeline completes successfully, passes its own validation, and produces outputs that are
internally coherent. Their detection required external comparison. This connects directly to the
thesis's claim that capability is necessary but not sufficient (§1.4) and that triangulated
validation against known references is essential for scientific trust.

### 4.1.10 Genomic context and chromosome distribution

The distribution of DMRs across genomic compartments is broadly similar between the arms:

**Table 4.7.** Genomic context distribution of DMRs.

| Category | Baseline | Agent |
|---|---:|---:|
| Intron | 50.7% | 46.9% |
| Intergenic | 21.9% | 35.6% |
| Exon | 12.6% | 10.7% |
| Promoter | 10.3% | 6.9% |
| 3'UTR | 3.6% | — |
| 5'UTR | 0.9% | — |

The agent's higher intergenic share (35.6% vs. 21.9%) is consistent with permissive calling
picking up weaker signals in regions far from annotated genes. The proportional similarity
across the remaining categories indicates that the extra agent DMRs are spread across all
genomic compartments rather than concentrated in one anomalous category — there is no evidence
of a systematic annotation artefact.

Chromosomal distribution is likewise broadly concordant, with two notable deviations: the agent
calls 2× the relative share of chrX DMRs (3.4% vs. 1.5%) and identifies 8 chrY DMRs where the
baseline finds none. Both are consistent with a permissive threshold lowering the bar
everywhere, including on sex chromosomes where sample size is effectively halved (all samples
are male).

### 4.1.11 The agent's evolutionary trajectory

Run23 was executed under Mimosa's Goal 5 (full cycle with learning), using the Quality-Diversity
(QD) evolutionary algorithm. Six iterations were evaluated:

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
declining success rate (50% → 25%), responding by increasing "boldness" and doubling the agent
budget.

Twenty-one learned patterns were accumulated during the process, covering failure modes from
earlier runs: OOM avoidance (chromosome-by-chromosome processing), DSS p-value validation
(abort if any *p* > 1, guarding against column-swap bugs), and graceful degradation (skip
enrichment rather than crash). That the verifier system nonetheless missed the p.threshold
semantics, direction inversion, and empty gene_name — precisely the defects that required
external comparison to detect — exposes a gap in the automated verification coverage that the
thesis returns to in §6 (Discussion).

### 4.1.12 Study A — Summary scorecard

Table 4.8 brings together the comparison across all evaluated dimensions.

**Table 4.8.** Study A summary scorecard.

| Dimension | Baseline vs. paper | Agent vs. paper | Agent vs. baseline |
|---|---|---|---|
| **DMR count fidelity** | 921 vs. 813 (1.1×) | 4,812 vs. 813 (5.9×) | 5.2× more |
| **Direction** | Correct convention | Inverted (100%) | Inverted (100%) |
| **Gene recovery** | 4/9 key genes found | 4/9 via enrichment | 86% positional overlap |
| **Pathway themes** | Neural/developmental ✅ | Neural/developmental ✅ | Convergent |
| **Genomic context** | Proportionally similar | Proportionally similar | Higher intergenic |
| **Silent defects** | None identified | 3 (p-threshold, direction, gene_name) | — |

The baseline achieves close fidelity to the paper (within 13% on DMR count, correct direction,
same key genes). The agent recovers the biological signal — 86% of the baseline's DMRs, the
same pathway themes, and the same key genes through its enrichment step — but does so at the
cost of a 5.9× inflated call set, inverted direction labels, and a broken gene-annotation
column. Its engineering qualities — modular scripts, config-driven parameters, OOM protection,
automated validation — are genuine, but the three silent defects demonstrate that engineering
quality does not guarantee biological correctness.

---

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
interpretation without expert review. <mark style="background: #FF5582A6;">Whether the skill and tool guardrails described in §3.4
and §3.6 can close this gap</mark>, and whether these defects recur in Study B, are the questions that
the remainder of the validation (§4.2, Chapter 5) addresses.
