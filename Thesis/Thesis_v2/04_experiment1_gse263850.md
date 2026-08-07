# Chapter 4 — Experiment 1: Replication of the GSE263850 AKAP11 Study
- [ ] bu section'da method ve result arasında net bir çizgi yok gibi ve bunları nasıl ayırsam bilemiyorum. yani methodların ne kadarı zaten methods kısmında yazılmalı ve ne kadarı results kısmında olmalı. bu file normalde bu deneyin resultsu olcaktı son dosyada da o başlıkta birleştircektim. ama bilmiyorum. task🔼 

The central hypothesis of this thesis asserts that an LLM-based agent can reproduce the principal findings of a peer-reviewed whole-genome bisulphite sequencing study — differentially methylated regions, affected genes, and direction of effect — to a degree comparable with an expert re-analysis of the same data. This chapter subjects that claim to its first empirical test. The experiment takes a single published dataset, GSE263850, and asks three questions: does Mimosa find the same regions, does it assign them the correct biological direction, and does it recover the same downstream biology? A triangulated comparison design — Mimosa versus paper, Mimosa versus an expert baseline, and baseline versus paper — provides the reference frame. The baseline-versus-paper agreement serves as the realistic ceiling against which Mimosa is measured, since even a careful human re-analysis does not reproduce every detail of a published result.

The chapter reports headline concordance metrics, traces each source of divergence to specific parameter choices, catalogues three silent defects that Mimosa's own validation did not catch, reports a subsequent debug pass that corrects all three within Mimosa's existing pipeline architecture, and concludes with a scorecard summarising what this first experiment contributes to the overall reliability argument.

---

## 4.1 Dataset and biological context

The data for this experiment are drawn from Farhangdoost et al. (2025), deposited in the Gene Expression Omnibus as GSE263850. The study investigated genome-wide DNA methylation changes in human induced pluripotent stem cell (iPSC)-derived cortical neurons carrying a heterozygous CRISPR-mediated knockout of _AKAP11_, a gene whose loss-of-function variants are among the strongest known risk factors for both bipolar disorder and schizophrenia #review <mark style="background: #FF5582A6;">add citation</mark>. The experimental design is a simple two-group comparison:

|Group|Genotype|Samples|
|---|---|---|
|Knockout (KO)|Het-_AKAP11_-KO|3 clones (Clone 16, 20, 21)|
|Wild-type (WT)|Unedited iPSC-derived neurons|3 replicates (SBP009 ×3)|

The WGBS libraries were sequenced at high depth, aligned with Bismark, and yielded Bismark coverage files deposited in GEO. These six `.bed.gz` files the dataset has 12 column bed files that we transfered to 6 column cov files with this method blabla #review  [[coversion_logic copy]]  <mark style="background: #FF5582A6;">ayrıca neden spesifik olarak bu dataseti seçtiğini açıkla</mark>— approximately 24 million CpGs each — are the common starting material for this experiment. 

The published analysis used the DSS Bioconductor package with a multi-factor beta-binomial model, smoothing enabled, `p.threshold = 1e-5` (raw per-CpG _p_-value), and no effect-size minimum (`delta = 0`), with adjacent significant CpGs merged at ≤100 bp. The paper reported **813 DMRs** (638 hypermethylated, 175 hypomethylated), **705 associated genes** (annotated via Homer and associated within ±100 kb from TSS to DMR midpoint for DMR–DEG correlations), and highlighted convergent DMR–H3K27ac–DEG evidence at gold-standard loci including _IRX2_, _CLEC19A_, and _KANK1_.

---

## 4.2 Experimental design — the three analysis arms

The replication is conducted as three independent analyses of the identical six coverage files, differing only in who or what chose the analysis parameters.

**Arm 1 — Published results (paper).** The expected reference: the 813 DMRs, 705 genes, and enriched pathways reported by Farhangdoost et al. (2025). These are taken as the target of replication, not as ground truth — the paper's own analysis is one defensible choice of parameters among several.

**Arm 2 — Expert re-analysis (baseline).** An R script written by a human analyst with the explicit goal of replicating the published analysis faithfully. It uses:

- `DMLfit.multiFactor()` + `DMLtest.multiFactor()` (DSS's multi-factor interface),
- the paper's exact parameters: `smoothing = TRUE`, `p.threshold = 1e-5`, `delta = 0`, `dis.merge = 100`, `minlen = 50`, `minCG = 3`, `pct.sig = 0.5`,
- ≥5× per-sample coverage filter (matching the paper),
- ChIPseeker annotation with a ±100 kb TSS window, #review <mark style="background: #FF5582A6;">not the same as the paper but we want to simulate the most paperlike script that doesn't use extra tools because thats what mimosa will do</mark>
- ReactomePA pathway enrichment with an explicit gene universe.

**Arm 3 — Mimosa pipeline.** Mimosa was given a natural-language goal and a workspace with the coverage files. The pipeline it synthesised is a five-script modular design:

- `01_load_and_qc.R` — load, coverage filter (≥10×), QC plots (PCA, heatmap, dendrogram),
- `02_differential_methylation.R` — `DMLtest()` (simple two-group), chromosome-by-chromosome to avoid out-of-memory failures, with `p.threshold = 0.05`, `delta = 0.25`, `dis.merge = 1000`,
- `03_annotate.R` — genomation-based annotation (promoter/exon/intron/intergenic + CpG island overlap),
- `04_enrichment.R` — GO Biological Process + KEGG enrichment via clusterProfiler,
- `validate_pipeline.R` — automated sanity checks (sample counts, p-value range, output file existence).

Mimosa's pipeline differed from the paper's in several consequential parameters, which are analysed in §4.3.2.

---

## 4.3 Results

### 4.3.1 Headline DMR counts

Table 4.1 summarises the DMR-level output of each arm.

**Table 4.1.** DMR counts and region statistics across the three arms.

|Metric|Paper|Baseline|Mimosa|
|---|--:|--:|--:|
|**Total DMRs**|813|921|4,812|
|**Hypermethylated**|638 (78%)|685 (74%)|2,182 (45%)|
|**Hypomethylated**|175 (22%)|236 (26%)|2,630 (55%)|
|**Associated genes**|705|825|— (gene_name bug)|
|Median region length|—|242 bp|285 bp|
|Mean region length|—|293 bp|346 bp|
|Median CpGs/region|—|5|6|
|Total bp covered|—|270,068|1,665,686|

The baseline produces 921 DMRs — a 13% overshoot of the paper's 813, within the range of variation expected from minor implementation differences (e.g. Bioconductor version, exact coverage at boundary CpGs). Mimosa produces 4,812 DMRs — a 5.9× overshoot. This inflation is the chapter's first major finding and is traced to specific parameter differences in §4.3.2.

### 4.3.2 Parameter analysis — the sources of divergence

Table 4.2 catalogues the parameter differences between the baseline and Mimosa, alongside their impact.

**Table 4.2.** Critical parameter differences between the baseline and Mimosa pipelines.

|Parameter|Baseline (paper values)|Mimosa|Impact|
|---|---|---|---|
|Coverage filter|≥5× per sample|≥10× in ≥1 sample|Mimosa retains fewer sites but with different per-sample logic|
|Statistical model|`DMLfit.multiFactor()`|`DMLtest()` (simple 2-group)|Equivalent for this single-factor design|
|`delta` (effect-size minimum)|**0**|**0.25**|Mimosa is stricter — requires ≥25% methylation difference|
|`p.threshold` in `callDMR`|**1e-5** (raw _p_)|**0.05** (FDR, misapplied)|**Mimosa is ~5,000× more permissive**|
|`dis.merge`|**100 bp**|**1,000 bp**|Mimosa merges regions 10× farther apart|
|`minlen`|50|50|Identical|
|`minCG`|3|3|Identical|
|`pct.sig`|0.5|0.5|Identical|

The single most consequential difference is the `p.threshold` mismatch. DSS's `callDMR()` function expects a raw per-CpG _p_-value threshold; the Mimosa pipeline passes its configured FDR cutoff (0.05) into this slot, via `q_value_cutoff = 0.05` in `config.yaml`. This makes the per-CpG inclusion criterion approximately 5,000 times more permissive than the paper's `1e-5`, which is the primary driver of the DMR count inflation. Mimosa's stricter effect-size filter (`delta = 0.25` versus the baseline's `delta = 0`) partially offsets this by rejecting small-effect CpGs, but clearly does not compensate for the p-value looseness on its own. The `dis.merge = 1000` setting further inflates counts by merging CpGs up to 10× farther apart into single regions. §4.8 shows that correcting `q_value_cutoff` from `0.05` to `0.00001` — a single configuration value — was the single most effective corrective step once the pipeline was debugged.

This is a semantic mismatch — Mimosa treated a conceptually correct FDR threshold as if it were a raw _p_-value — and is precisely the kind of "plausible wrong answer" described in §1.4. Its detection required the triangulated comparison design: within Mimosa's output alone, the 4,812 DMRs are internally consistent and pass the pipeline's own validation, and only the juxtaposition with the baseline and the paper reveals the inflation.

### 4.3.3 Direction concordance — a systematic inversion

Among the 791 overlapping DMR pairs between the baseline and Mimosa's output, the direction of effect is **100% inverted**, with zero exceptions.

**Table 4.3.** Direction concordance for overlapping DMR pairs.

|Mimosa label|Baseline label|Count|
|---|---|--:|
|Hypo|Hyper|607|
|Hyper|Hypo|184|
|Hyper|Hyper|0|
|Hypo|Hypo|0|

This is not biological discordance but a labelling convention difference. The baseline's `DMLfit.multiFactor()` computes coefficients as _treatment − control_ (KO − WT), so a positive `areaStat` indicates higher methylation in the KO — hypermethylation. Mimosa's `DMLtest()` was called as `DMLtest(group1 = ctrl, group2 = treat)`, so its `diff.Methy` represents _control − treatment_ (WT − KO) — flipping the sign. The 100% inversion confirms that the two pipelines agree on the biology for every shared region; the labels are simply opposite.

A natural question is why Mimosa's overall hyper/hypo ratio (45%/55%) does not mirror the paper's strong hypermethylation skew (78%/22%) if the labels are merely inverted. The answer lies in the composition of the call set. Among the 762 Mimosa DMRs that overlap the baseline, the directional split is 23.9% positive `diff.Methy` / 76.1% negative — which, after accounting for the sign inversion, closely mirrors the baseline's 74.4% Hyper / 25.6% Hypo ratio. The remaining ~4,050 Mimosa-only DMRs — additional low-confidence calls admitted by the permissive threshold — show a near-even split (49.4% / 50.6%), diluting the directional signal in the aggregate statistics. The inversion is thus fully present in the shared, high-confidence regions; the near-even overall ratio is an artefact of the inflated call set. #review

### 4.3.4 Overlap and concordance

Having noted the direction inversion, the analysis turns to positional concordance — whether the two pipelines identify the same genomic loci as differentially methylated.

**Table 4.4.** Overlap between the baseline and Mimosa DMR call sets.

| Comparison                           | Result                |
| ------------------------------------ | --------------------- |
| Baseline DMRs recovered by Mimosa    | **791 / 921 (85.9%)** |
| Mimosa DMRs supported by baseline    | 764 / 4,812 (15.9%)   |
| Mimosa-only DMRs (no baseline match) | 4,048 (84.1%)         |

The asymmetry is the expected consequence of the call-set size difference: the baseline's smaller, higher-confidence set is almost entirely (86%) recovered within Mimosa's larger set, while the reverse is naturally much lower. This pattern — high recall, low precision relative to the baseline — is the signature of a permissive threshold.

More informatively, the quality of Mimosa's calls correlates with their corroboration.

**Table 4.5.** Properties of Mimosa DMRs that overlap vs. do not overlap the baseline.

|Property|Overlapping (n = 764)|Non-overlapping (n = 4,048)|
|---|--:|--:|
|Median|areaStat||
|Median nCG|7|6|
|Median region length|372 bp|274 bp|
|Median baseline overlap|78%|—|

Mimosa's **strongest calls** — those with the largest effect sizes, most CpGs, and broadest regions — are disproportionately the ones confirmed by the baseline. This indicates that Mimosa's internal ranking of its calls is sound; the problem is the threshold at which the list is cut, not the ranking above it.

---

## 4.4 Gene recovery and biological concordance

### 4.4.1 Gene-level recovery

Gene-level concordance is assessed for the paper's gold-standard loci — genes with convergent DMR + H3K27ac + DEG evidence — and for the top hypermethylated hits.

**Table 4.6.** Recovery of key genes across analysis arms.

| Gene        | Paper status                        | Baseline                               | Mimosa                    |
| ----------- | ----------------------------------- | -------------------------------------- | ------------------------- |
| **IRX2**    | Gold standard (DMR + H3K27ac + DEG) | ✅ Found (Hyper; 3'UTR/Promoter/Intron) | ✅ Found (via enrichment)  |
| **CLEC19A** | Gold standard                       | ❌ Not found                            | ❌ Not found               |
| **KANK1**   | Gold standard                       | ❌ Not found                            | ✅ Found (via enrichment)  |
| OTX1        | Top hypermethylated                 | ✅ Found (Hyper; Exon/Intergenic)       | ✅ Found (via enrichment)  |
| NR2E1       | Top hypermethylated                 | ✅ Found (Hyper; 5'UTR)                 | ✅ Found (via enrichment)  |
| PAX7        | Top hypermethylated                 | ✅ Found (Hyper; Intergenic)            | Unknown (gene_name empty) |
| ENPP2       | Top hypermethylated                 | ✅ Found (Hyper; Promoter)              | ✅ Found (via enrichment)  |
| CCDC177     | Top hypomethylated                  | ✅ Found (Hyper — contradicts paper)    | ✅ Found (via enrichment)  |
| DMRTA2      | ORA-enriched                        | ❌ Missing from baseline                | ✅ Found (via enrichment)  |

#review

Two patterns emerge. First, neither the baseline nor Mimosa's annotation step recovers _CLEC19A_ — one of the paper's three gold-standard genes — and the baseline also misses _KANK1_, though Mimosa's enrichment step does recover _KANK1_ in 37 GO terms. This partly reflects a real methodological difference in annotation strategy: the paper used HOMER `annotatePeaks`, which assigns each DMR to its nearest TSS regardless of whether the DMR overlaps the gene body, while the baseline used ChIPseeker (a promoter/genic region hierarchy with nearest-gene fallback) and Mimosa used genomation (direct genomic overlap). For the convergent DMR + H3K27ac + DEG evidence at _IRX2_, _CLEC19A_, and _KANK1_, the paper's multi-omics integration (Fig. 5C) links enhancers to genes by proximity to nearest TSS — so these genes need not have a DMR that overlaps their gene body, only a DMR at a nearby regulatory region. That _CLEC19A_ is not found by any arm suggests the ceiling for gene recovery under R-based annotation strategies is below 100%, which sets an honest upper bound for the Mimosa comparison. #review

Second, Mimosa's enrichment step (`04_enrichment.R`) independently re-computes DMR–gene overlaps — it reads the raw DMR coordinates (`DMRs_tiles.txt`), performs its own `findOverlaps()` against a RefSeq gene BED file, converts RefSeq IDs to Entrez via `org.Hs.eg.db`, and feeds the result into `enrichGO()` and `enrichKEGG()`. This independent pathway _does_ recover key genes including _IRX2_, _NR2E1_, _KANK1_, _CCDC177_, and _DMRTA2_ — but because the `gene_name` column in the annotated DMR output is empty for all 4,812 rows (a confirmed annotation bug in `03_annotate.R` — see §4.7), these gene recoveries cannot be traced back to specific DMR coordinates without re-running the annotation step. This reduces the utility of Mimosa's output for gene-level biological interpretation. #review

### 4.4.2 Enrichment concordance — biological pathways

The three arms used different enrichment frameworks and gene sets, which makes direct comparison informative.

**Paper's ORA — Reactome (all 705 DMR-associated genes via ShinyGO v0.77, FDR < 0.05):** #review

1. Class A/1 Rhodopsin-like receptors
2. Peptide ligand-binding receptors
3. GPCR ligand binding
4. GPCR downstream signalling
5. Signalling by GPCR
6. G alpha (i) signalling events

**Paper's ORA — GO Molecular Function (59 DMR-associated genes with differential expression, ±100 kb, ShinyGO):** #review

1. Sequence-specific DNA binding (GO:0043565)
2. DNA-binding transcription factor activity, RNA Pol II-specific (GO:0000981)
3. Transcription factor binding (GO:0008134)
4. DNA-binding transcription activator activity, RNA Pol II-specific (GO:0001228)
5. RNA polymerase II cis-regulatory region sequence-specific DNA binding

**Mimosa's top GO Biological Process terms:**

1. Pattern specification process (_p_~adj~ = 4.37 × 10^-20^)
2. Embryonic organ development (_p_~adj~ = 1.35 × 10^-16^)
3. Regionalization (_p_~adj~ = 1.20 × 10^-15^)
4. Skeletal system development (_p_~adj~ = 7.58 × 10^-15^)

**Mimosa's top KEGG pathways:**

1. Neuroactive ligand–receptor interaction (_p_~adj~ = 3.00 × 10^-7^)
2. Calcium signalling pathway (_p_~adj~ = 1.89 × 10^-5^)
3. Axon guidance (_p_~adj~ = 6.80 × 10^-5^)

The paper's Reactome ORA of all DMR-associated genes highlighted GPCR-related pathways, while its GO MF analysis of the smaller DMR–DEG overlap set (59 genes) highlighted DNA-binding transcription factor activity. Mimosa's GO BP enrichment emphasised neural development and patterning, and its KEGG results included neuroactive ligand–receptor interaction — thematically related to the paper's GPCR findings, though framed differently due to the different ontology databases. All three arms converge on neural and developmental biology, which is consistent with the study's context — _AKAP11_ knockout in iPSC-derived cortical neurons, a model for bipolar disorder and schizophrenia. The enrichment concordance is arguably the most robust form of agreement between the arms, because pathway-level results are buffered against individual gene-level differences by the aggregation inherent in enrichment analysis. #review

Three caveats apply. First, the paper performed two separate enrichment analyses — one on all DMR-associated genes (Reactome; GPCR-related) and one on the 59-gene DMR–DEG overlap (GO MF; transcription factor activity) — while Mimosa lumped all DMR-overlapping genes into a single enrichment, making the two not directly comparable. Second, the paper used an explicit background universe of 23,590 genes derived from their own RNA-seq data. Because this RNA-seq dataset was not available to us, neither the baseline nor Mimosa could use this exact background; Mimosa instead used the default gene universe (all annotated genes), which inflates enrichment significance (a known ORA pitfall) #review <mark style="background: #FF5582A6;">add reference</mark> and contributes to the divergence from the paper's specific pathway findings. Third, Mimosa's gene set is derived from 1,587 Entrez IDs (converted from RefSeq overlaps) rather than the 705 genes in the paper, so the input size is very different; the fact that the top terms still converge on neural/developmental biology is meaningful precisely because it survives this inflation. #review

**Post-hoc manual standardisation** #review
To determine whether the divergence in pathway themes (GPCR/TF activity vs. neural development) was driven by the analytical framework (ShinyGO vs. clusterProfiler) or the input gene set, a post-hoc manual standardisation was performed. The 1,040 unique gene symbols identified by Mimosa's enrichment step were manually run through ShinyGO v0.77 against the GO Molecular Function database — replicating the tool and database used by the paper. 

**Manual ORA — GO Molecular Function (all 1,040 Mimosa DMR genes, ShinyGO v0.77):**
1. heparan sulfate 6-sulfotransferase activity (GO:0017095)
2. ryanodine-sensitive calcium-release channel activity (GO:0005219)
3. Roundabout binding (GO:0048495)
4. neurotrophin receptor activity (GO:0005030)
5. voltage-gated calcium channel activity (GO:0086007)

The top results did not recover the paper's transcription factor binding signatures. Instead, the top terms align closely with Mimosa's autonomous findings, featuring calcium channel activity, neurotrophin receptor activity, and Roundabout binding (an axon guidance receptor). #review <mark style="background: #FF5582A6;">maybe references here too?</mark>

Standardising the enrichment method and database did not shift the results toward the paper's transcription-factor-activity terms; the top hits remained centred on ion channel and receptor activity (ryanodine-sensitive calcium-release channel, voltage-gated calcium channel, neurotrophin receptor) rather than DNA-binding or transcription factor function. This suggests the divergence observed in Section 4.4.2 is not primarily attributable to the choice of enrichment tool or ontology database (ShinyGO/GO MF vs. clusterProfiler/GO BP/KEGG), since holding these constant did not reproduce the paper's findings. Instead, the discordance more likely originates upstream, in the composition of the DMR-associated gene set itself — consistent with the differences in background universe and gene set size noted above. #review <mark style="background: #FF5582A6;">bununla altındaki overlap ediyo sanki bunları birleştir veya direkt sil birini </mark>

This demonstrates a critical methodological point: the paper's specific GO MF findings (transcription factor binding) were entirely dependent on their decision to filter the DMR genes down to only those that were also differentially expressed (the 59-gene DMR–DEG overlap). When an autonomous pipeline like Mimosa faithfully annotates all significant DMRs and enriches the full set, the resulting pathway profile looks completely different — dominated instead by broader neural development and calcium signalling themes, regardless of the ontology database used. #review <mark style="background: #FF5582A6;">too ai written, especially the start. make it objective, this is a scientific paper</mark>


---

## 4.5 Genomic context and chromosome distribution

The distribution of DMRs across genomic compartments is broadly similar between the arms, though exact percentages are not directly comparable because the paper used Homer for annotation (which assigns each DMR to its nearest TSS feature), the baseline used ChIPseeker (which uses a promoter/genic region hierarchy), and Mimosa used genomation (direct overlap with gene features). #review

**Table 4.7.** Genomic context distribution of DMRs.

|Category|Baseline|Mimosa|
|---|--:|--:|
|Intron|50.7%|46.9%|
|Intergenic|21.9%|35.6%|
|Exon|12.6%|10.7%|
|Promoter|10.3%|6.9%|
|3'UTR|3.6%|—|
|5'UTR|0.9%|—|

Mimosa's higher intergenic share (35.6% vs. 21.9%) is consistent with permissive calling picking up weaker signals in regions far from annotated genes. The proportional similarity across the remaining categories indicates that the extra Mimosa DMRs are spread across all genomic compartments rather than concentrated in one anomalous category — there is no evidence of a systematic annotation artefact.

The chromosomal distribution is likewise broadly concordant, with two notable deviations: Mimosa calls 2× the relative share of chrX DMRs (3.4% vs. 1.5%) and identifies 8 chrY DMRs where the baseline finds none. Both are consistent with a permissive threshold lowering the bar everywhere, including on sex chromosomes where the effective sample size is halved (all samples are male).

---

## 4.6 Mimosa evolutionary trajectory

The workflow generation was executed under Mimosa's Quality-Diversity (QD) evolutionary algorithm. Six iterations were evaluated:

|Iteration|Kind|Quality score|Archive size|Notes|
|---|---|--:|--:|---|
|1|Seed|**0.8601** (best)|1|Produced the final pipeline|
|2|Mutation|0.7259|2|Explored but did not improve|
|3|Mutation|— (not archived)|2||
|4|Mutation|0.7163|3||
|5|Mutation|0.6899|4||
|6|Mutation|—|4|Budget doubled due to plateau|

The seed iteration scored highest, and subsequent mutations explored diversity without improving quality — a classic exploration-without-improvement pattern in which the initial synthesis happened to be the best. The system detected increasing plateau (0% → 50%) and declining success rate (50% → 25%), responding by increasing "boldness" and doubling the Mimosa budget.

Twenty-one learned patterns were accumulated during the process, covering failure modes from earlier runs: OOM avoidance (chromosome-by-chromosome processing), DSS p-value validation (abort if any _p_ > 1, guarding against column-swap bugs), and graceful degradation (skip enrichment rather than crash). That the verifier system nonetheless missed the p.threshold semantics, direction inversion, and empty gene_name — precisely the defects that required external comparison to detect — exposes a gap in the automated verification coverage that the thesis returns to in the Discussion (Chapter 7).

---

## 4.7 Identified defects

Three specific defects in Mimosa's pipeline were identified through the triangulated comparison. All three are _silent_: the pipeline completes successfully, passes its own validation, and produces outputs that are internally coherent. Their detection required external comparison — a fact that connects directly to the thesis's claim that capability is necessary but not sufficient (§1.4) and that triangulated validation against known references is essential for scientific trust.

**Defect 1: p.threshold / FDR mismatch.** As detailed in §4.3.2, Mimosa feeds an FDR cutoff (0.05) into DSS's `callDMR(p.threshold = ...)`, which expects a raw per-CpG _p_-value. This is the primary cause of the 5.9× DMR inflation. §4.8 reports a debug pass that corrects this directly, by changing `q_value_cutoff` in `config.yaml` from `0.05` to `0.00001`, and quantifies the resulting change in DMR count.

**Defect 2: Direction inversion.** Mimosa's `DMLtest()` group-order convention produces `diff.Methy` with opposite sign from the baseline (§4.3.3). While internally consistent, any biological conclusion about hyper- versus hypomethylation drawn directly from Mimosa's labels would be backwards. §4.8 shows this is corrected by a two-line group-order swap.

**Defect 3: Empty gene_name column.** In `03_annotate.R`, the `gene_name` vectors are initialised to empty strings and never assigned gene symbols after annotation. The genomation-based annotation correctly produces genomic-context categories (promoter/exon/intron/intergenic) and CpG-island context, but the gene-symbol column remains blank for all 4,812 DMRs. The pipeline's validation script does not check `gene_name` completeness, so the bug passes silently. §4.8 shows this is corrected by calling the appropriate `genomation` accessor function.

These defects are consequential for the reliability assessment because they instantiate the failure mode that the hypothesis anticipates: plausible, internally consistent outputs that are biologically misleading. They cannot be caught by Mimosa's own verification loop, and their nature — a semantic API mismatch, a convention difference, and a silent initialisation bug — represents the category of errors most resistant to automated detection.

---

## 4.8 Debug rerun: correcting the identified defects

Section 4.7 established that all three defects were silent — invisible to Mimosa's own validation — but says nothing about whether they were *expensive* to fix once found. This section addresses that question directly. A manual debug pass was carried out on the Mimosa-generated pipeline, changing only what was needed to address the three defects identified above, and the resulting outputs are compared against the original (buggy) Mimosa run, the expert baseline, and the paper.

### 4.8.1 What was changed

**Table 4.8.** Configuration and script changes made in the debug pass.

|Change|Location|Original Mimosa|Debug rerun|
|---|---|---|---|
|`p.threshold` value fed to `callDMR()`|`config.yaml`, `q_value_cutoff`|`0.05` (an FDR cutoff, misapplied — Defect 1)|`0.00001` (the raw per-CpG _p_-value `callDMR()` expects)|
|Group order in `DMLtest()`|`02_differential_methylation.R`|`group1 = ctrl_ids, group2 = treat_ids` (computes WT − KO)|`group1 = treat_ids, group2 = ctrl_ids` (computes KO − WT)|
|Gene-name extraction|`03_annotate.R`|`getTargetAnnotationStats()` — returns annotation percentages, not gene identifiers|`getAssociationWithTSS()$feature.name` — returns the nearest RefSeq transcript ID per DMR/DMC|

The effect-size floor (`meth_diff_cutoff = 25`, i.e. `delta = 0.25`) was present in both the original and debugged runs and was not changed; Defect 1 is instead corrected directly, by changing the value assigned to `q_value_cutoff` so that the number passed into `callDMR(p.threshold = ...)` is the intended raw _p_-value rather than an FDR cutoff. The `dis.merge` setting, coverage filter, statistical test (`DMLtest`, simple two-group), annotation tool (`genomation`), and enrichment tool (`clusterProfiler`) were all left unchanged from the version analysed in §4.2–§4.7. In total, the correction comprised one configuration value and two short, localised script edits — a two-line argument swap and a function-call replacement — with no restructuring of the five-script pipeline.

### 4.8.2 Effect on DMR counts and direction

**Table 4.9.** DMR counts and directional split before and after the debug pass.

|Metric|Paper|Baseline|Original Mimosa|Debug rerun|
|---|--:|--:|--:|--:|
|Total DMRs|813|921|4,812 (5.9×)|846 (1.04×)|
|Hypermethylated|638 (78%)|685 (74%)|2,182 (45%, inverted convention)|524 (62%)|
|Hypomethylated|175 (22%)|236 (26%)|2,630 (55%, inverted convention)|322 (38%)|

The single configuration change (`q_value_cutoff: 0.05 → 0.00001`) reduces the DMR count from 4,812 to 846 — within 4% of the paper's 813, against the original 5.9× overshoot. This proximity should be read with one caveat: the `delta = 0.25` effect-size floor was present in both the original and debugged runs, and was already necessary to keep `DMLtest()`'s output in a comparable range to the paper's — without it, `DMLtest()` alone reportedly produces on the order of 24,000 DMRs on this dataset, roughly 30× the baseline's count. We attribute this difference to the different DML tests used in the workflow because the simple two-group test is inherently more permissive than the paper's multi-factor model at a fixed threshold. The count reduction achieved by debugging is attributable specifically to the `q_value_cutoff` fix operating on top of that pre-existing floor; the resulting proximity to the paper's count reflects correction of the FDR/raw-_p_ semantic bug within this two-group-plus-floor approach, not full convergence between `DMLtest` and the paper's multi-factor model.

Direction is corrected without qualification. At the locus with the largest effect size (chr6:108,174,302), the original run reported `meanMethy1 (WT) = 0.119`, `meanMethy2 (KO) = 0.705`, `diff.Methy = −0.586`; the debug rerun reports the same underlying methylation values with `diff.Methy = +0.586` — only the sign convention changed. Across all 357 DMR pairs shared between the debug rerun and the baseline, direction concordance is 100%. The overall hyper/hypo split (62%/38%) is now qualitatively consistent with the paper's hypermethylation-dominant pattern (78%/22%), though the quantitative gap is not fully closed — plausibly reflecting the remaining `DMLtest`-versus-`DMLfit.multiFactor` difference and the `delta` filter's disproportionate removal of smaller-effect hypomethylated calls (§4.8.4).

### 4.8.3 Gene annotation restored

**Table 4.10.** Annotation completeness and key gene recovery, debug rerun.

|Metric|Original Mimosa|Debug rerun|
|---|--:|--:|
|Non-empty `gene_name` rows|0 / 4,812 (0%)|846 / 846 (100%)|
|Gene identifier type|— (empty)|RefSeq accessions (NM_, NR_, XM_, XR_)|

The fix resolves Defect 3 completely at the row level, though the identifiers recovered are RefSeq transcript accessions rather than the gene symbols the paper (via Homer) and baseline (via ChIPseeker) report — a residual, minor divergence in annotation output rather than a defect. At the IRX2 locus, the debug rerun calls four DMRs (three hyper, one hypo), the same qualitative pattern observed in the baseline. Enrichment-derived gene recovery also improves in traceability: IRX2, NR2E1, DMRTA2, OTX1, OTX2, ENPP2, and PAX7 all appear in significant GO terms, and — because `gene_name` is now populated — these recoveries can for the first time be traced back to specific annotated DMR coordinates, resolving the limitation noted in §4.4.1 and §4.7 (Defect 3). _CLEC19A_, _KANK1_, and _CCDC177_ were not re-examined in the debug rerun and so cannot be reported on here.

### 4.8.4 Overlap with the baseline

**Table 4.11.** Overlap between the debug rerun and the expert baseline.

|Metric|Original Mimosa vs. baseline|Debug rerun vs. baseline|
|---|--:|--:|
|Baseline DMRs recovered|791 / 921 (85.9%)|354 / 921 (38.4%)|
|Call set supported by baseline|764 / 4,812 (15.9%)|340 / 846 (40.2%)|
|Jaccard index (bp-level)|—|0.211|
|Top-20 baseline DMRs (by \|areaStat\|) recovered|—|19 / 20 (95%)|
|Directional concordance, overlapping pairs|0% (100% inverted)|100%|

Correcting the count and direction did not translate into higher raw positional overlap with the baseline — recall falls from 85.9% to 38.4%. This is not a regression: the original run's high recall was an artefact of its call set being large enough to contain most of the baseline's regions as a near-superset, at the cost of a 5.9× inflated total. The debugged pipeline instead converges with the baseline on the strongest, most defensible calls — 95% of the baseline's top 20 DMRs by area statistic are recovered — while continuing to disagree on a substantial number of lower-confidence regions on both sides, consistent with the residual difference between `DMLtest` and `DMLfit.multiFactor`. Recovery is also asymmetric by direction: 42% of baseline hypermethylated DMRs are recovered versus 28% of hypomethylated ones, consistent with the `delta` floor disproportionately removing smaller-effect hypomethylated calls.

### 4.8.5 Enrichment after the fix

**Table 4.12.** GO and KEGG enrichment before and after the debug pass.

|Metric|Original Mimosa|Debug rerun|
|---|--:|--:|
|Input genes|1,587|328|
|Significant GO BP terms|469|94|
|Significant KEGG pathways|56|2|
|Top GO BP themes|Neuron projection development, axonogenesis, forebrain development|Synapse organisation, axonogenesis, forebrain development|

The reduction in significant terms tracks the reduction in input genes; p-values also become more moderate (10⁻³–10⁻⁴ rather than 10⁻¹¹–10⁻¹⁴), consistent with the smaller gene list carrying a lower false-discovery burden. The core thematic content — neural development, axon guidance, forebrain development — is unchanged, and *focal adhesion* is the one KEGG term preserved across both runs. As in §4.4.2, the debug rerun still does not recover the paper's GO Molecular Function "transcription factor activity" signature; this is attributable to gene-set composition (all DMR-associated genes versus the paper's 59-gene DMR–DEG overlap set) rather than to the defects addressed here.

### 4.8.6 Synthesis

The three defects catalogued in §4.7 were corrected with one configuration value and two short, localised script edits, with no restructuring of the pipeline. Following correction, Mimosa's DMR count is within 4% of the paper's, its directional labels are unambiguously correct, its gene-annotation output is complete and traceable, and its highest-confidence calls converge closely with the baseline's and with the paper's key genes and pathway themes. Two qualifications keep this short of a straightforward "defects fixed, replication achieved" result. First, the near-match in DMR count reflects correction of a semantic bug (an FDR cutoff fed into a raw-_p_ slot) rather than the two statistical models converging on the same criterion — the pre-existing `delta = 0.25` floor, unchanged by the debug pass, was already necessary to keep `DMLtest`'s count in a range comparable to the multi-factor model's, and the `q_value_cutoff` fix operates on top of it. Second, region-level overlap with the baseline is lower after debugging than before, because the corrected call set is no longer a superset that trivially contains most baseline regions; overlap on the highest-confidence calls is the more informative measure of convergence, and there it is strong.

What this section demonstrates is best read as a statement about the *cost of correction*, not about self-correction: none of the three defects were detected, or could have been detected, by Mimosa's own validation. Diagnosis required the triangulated comparison of §4.3–§4.7; the fixes that followed the diagnosis were small and mechanical precisely because Mimosa's modular, configuration-driven pipeline design kept each defect isolated to a single parameter or function call rather than entangled across scripts. Whether this same separation — hard to detect internally, cheap to correct once diagnosed externally — holds for the defects encountered in later experiments is taken up in Chapter 7. #review <mark style="background: #FF5582A6;">this part not needed?</mark>

---

## 4.9 Summary

Table 4.13 brings together the comparison across all evaluated dimensions.

**Table 4.13.** Experiment 1 summary scorecard.

|Dimension|Baseline vs. paper|Mimosa vs. paper|Mimosa vs. baseline|Debug rerun vs. paper|
|---|---|---|---|---|
|**DMR count fidelity**|921 vs. 813 (1.1×)|4,812 vs. 813 (5.9×)|5.2× more|846 vs. 813 (1.04×), via direct q_value_cutoff fix (§4.8.2)|
|**Direction**|Correct convention|Inverted (100%)|Inverted (100%)|Correct (100%)|
|**Gene recovery**|4/9 key genes found|5/9 via enrichment|86% positional overlap|7 key genes traceable via enrichment (annotation now complete)|
|**Pathway themes**|Neural/developmental ✅|Neural/developmental ✅|Convergent|Neural/developmental ✅ (moderated significance)|
|**Genomic context**|Proportionally similar|Proportionally similar|Higher intergenic|Not re-assessed|
|**Silent defects**|None identified|3 (p-threshold, direction, gene_name)|—|0 outstanding — all three corrected (§4.8)|

The baseline achieves close fidelity to the paper (within 13% on DMR count, correct direction, same key genes). Mimosa's original run recovers the biological signal — 86% of the baseline's DMRs, the same pathway themes, and the same key genes through its enrichment step — but does so at the cost of a 5.9× inflated call set, inverted direction labels, and a broken gene-annotation column. Its engineering qualities — modular scripts, config-driven parameters, OOM protection, automated validation — are genuine, but the three silent defects demonstrate that engineering quality does not guarantee biological correctness. The debug rerun (§4.8) shows that this same modular, configuration-driven design is what kept the cost of correcting those defects low — one parameter and two short script edits, no rewrite — though the correction depended entirely on the external, human-led diagnosis reported in §4.3–§4.7, not on any capability internal to Mimosa itself.

What Experiment 1 contributes to the hypothesis is a clear separation of capability from reliability. On the capability side, the evidence is affirmative: Mimosa finds the signal (85.9% positional recall of the baseline in its original run), ranks its calls correctly (the strongest are the most corroborated), and converges on the correct biology (neural and developmental pathways, key genes recovered via enrichment). On the reliability side, the evidence is cautionary: three silent defects — an FDR-cutoff-fed-as-raw-_p_-value semantic mismatch, a direction-convention error, and an empty annotation column — would each produce misleading biological conclusions if taken at face value, and none would have been detected without the triangulated comparison against the baseline and the published analysis. The debug rerun adds a third dimension to this picture: once diagnosed, all three defects proved cheap to correct, and correction brought DMR count and direction close to the paper's without fully resolving every methodological divergence — region-level overlap with the baseline actually falls after debugging, even as agreement on the highest-confidence calls strengthens. Detection, not correction, is the bottleneck this experiment identifies.

This outcome supports the framing introduced in §1.4: that Mimosa can demonstrate statistical and biological competence while still harbouring errors that require external reference points to detect, and that a modular, configuration-driven architecture can make those errors cheap to fix once found. Whether the same pattern — genuine capability, silent but correctable defects — recurs in a different dataset, organism, and experimental context is the question addressed in the next experiment (Chapter 5). The cross-experiment synthesis, including whether these defects are systematic or dataset-specific, whether detection can be made less dependent on an external baseline, and what all of this implies for the practical deployment of agentic analysis pipelines, is taken up in the Discussion.
