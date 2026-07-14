# Chapter 4 — Experiment 1: Replication of the GSE263850 AKAP11 Study

The central hypothesis of this thesis asserts that an LLM-based agent can reproduce the principal findings of a peer-reviewed whole-genome bisulphite sequencing study — differentially methylated regions, affected genes, and direction of effect — to a degree comparable with an expert re-analysis of the same data. This chapter subjects that claim to its first empirical test. The experiment takes a single published dataset, GSE263850, and asks three questions: does Mimosa find the same regions, does it assign them the correct biological direction, and does it recover the same downstream biology? A triangulated comparison design — Mimosa versus paper, Mimosa versus an expert baseline, and baseline versus paper — provides the reference frame. The baseline-versus-paper agreement serves as the realistic ceiling against which Mimosa is measured, since even a careful human re-analysis does not reproduce every detail of a published result.

The chapter reports headline concordance metrics, traces each source of divergence to specific parameter choices, catalogues three silent defects that Mimosa's own validation did not catch, and concludes with a scorecard summarising what this first experiment contributes to the overall reliability argument. Findings that span multiple experiments are deferred to the Discussion (Chapter 7).

---

## 4.1 Dataset and biological context

The data for this experiment are drawn from <mark style="background: #FF5582A6;">Farhangdoost et al. (2025),</mark> #update  deposited in the Gene Expression Omnibus as GSE263850. The study investigated genome-wide DNA methylation changes in human induced pluripotent stem cell (iPSC)-derived cortical neurons carrying a heterozygous CRISPR-mediated knockout of _AKAP11_, a gene whose loss-of-function variants are among the strongest known risk factors for both bipolar disorder and schizophrenia. The experimental design is a simple two-group comparison:

|Group|Genotype|Samples|
|---|---|---|
|Knockout (KO)|Het-_AKAP11_-KO|3 clones (Clone 16, 20, 21)|
|Wild-type (WT)|Unedited iPSC-derived neurons|3 replicates (SBP009 ×3)|

The WGBS libraries were sequenced at high depth, aligned with Bismark, and yielded Bismark coverage files deposited in GEO. These six `.cov.gz` files — approximately 24 million CpGs each — are the common starting material for this experiment.

The published analysis used the DSS Bioconductor package with a multi-factor beta-binomial model, smoothing enabled, `p.threshold = 1e-5` (raw per-CpG _p_-value), and no effect-size minimum (`delta = 0`), with adjacent significant CpGs merged at ≤100 bp. The paper reported **813 DMRs** (638 hypermethylated, 175 hypomethylated), **705 associated genes** (±100 kb from TSS via ChIPseeker), and highlighted convergent DMR–H3K27ac–DEG evidence at gold-standard loci including _IRX2_, _CLEC19A_, and _KANK1_.

---

## 4.2 Experimental design — the three analysis arms

The replication is conducted as three independent analyses of the identical six coverage files, differing only in who or what chose the analysis parameters.

**Arm 1 — Published results (paper).** The expected reference: the 813 DMRs, 705 genes, and enriched pathways reported by Farhangdoost et al. (2025). These are taken as the target of replication, not as ground truth — the paper's own analysis is one defensible choice of parameters among several.

**Arm 2 — Expert re-analysis (baseline).** A 531-line monolithic R script written by a human analyst with the explicit goal of replicating the published analysis faithfully. It uses:

- `DMLfit.multiFactor()` + `DMLtest.multiFactor()` (DSS's multi-factor interface),
- the paper's exact parameters: `smoothing = TRUE`, `p.threshold = 1e-5`, `delta = 0`, `dis.merge = 100`, `minlen = 50`, `minCG = 3`, `pct.sig = 0.5`,
- ≥5× per-sample coverage filter (matching the paper),
- ChIPseeker annotation with a ±100 kb TSS window,
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

The single most consequential difference is the `p.threshold` mismatch. DSS's `callDMR()` function expects a raw per-CpG _p_-value threshold; the Mimosa pipeline passes its configured FDR cutoff (0.05) into this slot. This makes the per-CpG inclusion criterion approximately 5,000 times more permissive than the paper's `1e-5`, which is the primary driver of the DMR count inflation. Mimosa's stricter effect-size filter (`delta = 0.25` versus `delta = 0`) partially offsets this by rejecting small-effect CpGs, but clearly does not compensate for the p-value looseness. The `dis.merge = 1000` setting further inflates counts by merging CpGs up to 10× farther apart into single regions.

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

This is not biological discordance but a labelling convention difference. The baseline's `DMLfit.multiFactor()` computes coefficients as _treatment − control_ (KO − WT), so a positive `areaStat` indicates higher methylation in the KO — hypermethylation. Mimosa's `DMLtest()` was called as `DMLtest(group1 = ctrl, group2 = treat)`, so its `diff.Methy` represents _control − treatment_ (WT − KO) — flipping the sign. The 100% inversion confirms that the two pipelines agree on the biology for every shared region; the labels are simply opposite.<mark style="background: #FF5582A6;"> sadece label farklıysa hyper hypo farkı neden inverted değil de mimosada %40-60 gibi bir oran?</mark> #update 

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
- [ ] burayı paper a ve onun results una bakarak doğrula #update task🔼 📅 2026-07-19 

Gene-level concordance is assessed for the paper's gold-standard loci — genes with convergent DMR + H3K27ac + DEG evidence — and for the top hypermethylated hits.

**Table 4.6.** Recovery of key genes across analysis arms.

|Gene|Paper status|Baseline|Mimosa|
|---|---|---|---|
|**IRX2**|Gold standard (DMR + H3K27ac + DEG)|✅ Found (Hyper; 3'UTR/Promoter/Intron)|✅ Found (via enrichment re-overlap)|
|**CLEC19A**|Gold standard|❌ Not found|❌ Not found|
|**KANK1**|Gold standard|❌ Not found|❌ Not found|
|OTX1|Top hypermethylated|✅ Found (Hyper; Exon/Intergenic)|✅ Found (via enrichment)|
|NR2E1|Top hypermethylated|✅ Found (Hyper; 5'UTR)|✅ Found (via enrichment)|
|PAX7|Top hypermethylated|✅ Found (Hyper; Intergenic)|Unknown (gene_name empty)|
|ENPP2|Top hypermethylated|✅ Found (Hyper; Promoter)|Unknown (gene_name empty)|
|CCDC177|Top hypomethylated|✅ Found (Hyper — contradicts paper)|✅ Found (via enrichment)|
|DMRTA2|ORA-enriched|❌ Missing from baseline|✅ Found (via enrichment)|

Two patterns emerge. First, neither the baseline nor Mimosa recovers _CLEC19A_ or _KANK1_ — two of the paper's three gold-standard genes. This likely reflects a real methodological difference: the paper's gene-association strategy (±100 kb from TSS) links distant DMRs to genes that a direct-overlap annotation would not capture, and these two genes may fall in that gap. That neither arm finds them suggests the ceiling for gene recovery under direct-overlap annotation is below 100%, which sets an honest upper bound for the Mimosa comparison. #update <mark style="background: #FF5582A6;">Paper HOMER kullanıyor o yüzden de farklı olabilir ama double check</mark>

Second, Mimosa's enrichment step (`04_enrichment.R`) independently re-computes DMR–gene overlaps and _does_ recover key genes like _IRX2_, _NR2E1_, _CCDC177_, and _DMRTA2_ — but because the `gene_name` column in the annotated DMR output is empty for all 4,812 rows (a confirmed annotation bug — see §4.7), these genes cannot be traced back to specific DMR coordinates without re-running the annotation step. This reduces the utility of Mimosa's output for gene-level biological interpretation. #update <mark style="background: #FF5582A6;">Bu nerden çıkıyor hiçbir fikrim yok double check. en kötü claude konuşmalarından bulmaya çalış bu nerden çıktı</mark>

### 4.4.2 Enrichment concordance — biological pathways
- [ ] bu section not complete ya. paper'daki pathway ve go analizini objektif olarak ekle buraya task⏫ 📅 2026-07-25 #update 
Despite the different enrichment frameworks — Reactome (baseline) versus GO + KEGG (Mimosa) — and the different gene sets (305 symbols from ±100 kb TSS versus 2,444 Entrez IDs from direct overlap), both analyses converge on the same broad biological themes.

**Mimosa's top GO Biological Process terms:**

1. Pattern specification process (_p_~adj~ = 4.37 × 10^-20^)
2. Embryonic organ development (_p_~adj~ = 1.35 × 10^-16^)
3. Regionalization (_p_~adj~ = 1.20 × 10^-15^)
4. Skeletal system development (_p_~adj~ = 7.58 × 10^-15^)

**Mimosa's top KEGG pathways:**

1. Neuroactive ligand–receptor interaction (_p_~adj~ = 3.00 × 10^-7^)
2. Calcium signalling pathway (_p_~adj~ = 1.89 × 10^-5^)
3. Axon guidance (_p_~adj~ = 6.80 × 10^-5^)

Both pipelines highlight neural and developmental pathways, which is biologically consistent with the study's context — _AKAP11_ knockout in iPSC-derived cortical neurons, a model for bipolar disorder and schizophrenia. The enrichment concordance is arguably the most robust form of agreement between the arms, because pathway-level results are buffered against individual gene-level differences by the aggregation inherent in enrichment analysis.

Two caveats apply. First, Mimosa's enrichment used the default gene universe (all annotated genes) rather than an explicit universe of genes tested, which inflates enrichment significance (a known over-representation analysis pitfall). Second, Mimosa's gene set is derived from 19,525 overlapping RefSeq transcripts rather than the 705 genes in the paper, so the denominator is very different; the fact that the top terms still converge on neural/developmental biology is meaningful precisely because it survives this inflation.

---

## 4.5 Genomic context and chromosome distribution
#update <mark style="background: #FF5582A6;">Homer şeysi yine</mark>
The distribution of DMRs across genomic compartments is broadly similar between the arms.

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

**Defect 1: p.threshold / FDR mismatch.** As detailed in §4.3.2, Mimosa feeds an FDR cutoff (0.05) into DSS's `callDMR(p.threshold = ...)`, which expects a raw per-CpG _p_-value. This is the primary cause of the 5.9× DMR inflation.

**Defect 2: Direction inversion.** Mimosa's `DMLtest()` group-order convention produces `diff.Methy` with opposite sign from the baseline (§4.3.3). While internally consistent, any biological conclusion about hyper- versus hypomethylation drawn directly from Mimosa's labels would be backwards.

**Defect 3: Empty gene_name column.** In `03_annotate.R`, the `gene_name` vectors are initialised to empty strings and never assigned gene symbols after annotation. The genomation-based annotation correctly produces genomic-context categories (promoter/exon/intron/intergenic) and CpG-island context, but the gene-symbol column remains blank for all 4,812 DMRs. The pipeline's validation script does not check `gene_name` completeness, so the bug passes silently.

These defects are consequential for the reliability assessment because they instantiate the failure mode that the hypothesis anticipates: plausible, internally consistent outputs that are biologically misleading. They cannot be caught by Mimosa's own verification loop, and their nature — a semantic API mismatch, a convention difference, and a silent initialisation bug — represents the category of errors most resistant to automated detection.

---

## 4.8 Summary

Table 4.8 brings together the comparison across all evaluated dimensions.

**Table 4.8.** Experiment 1 summary scorecard.

|Dimension|Baseline vs. paper|Mimosa vs. paper|Mimosa vs. baseline|
|---|---|---|---|
|**DMR count fidelity**|921 vs. 813 (1.1×)|4,812 vs. 813 (5.9×)|5.2× more|
|**Direction**|Correct convention|Inverted (100%)|Inverted (100%)|
|**Gene recovery**|4/9 key genes found|4/9 via enrichment|86% positional overlap|
|**Pathway themes**|Neural/developmental ✅|Neural/developmental ✅|Convergent|
|**Genomic context**|Proportionally similar|Proportionally similar|Higher intergenic|
|**Silent defects**|None identified|3 (p-threshold, direction, gene_name)|—|

The baseline achieves close fidelity to the paper (within 13% on DMR count, correct direction, same key genes). Mimosa recovers the biological signal — 86% of the baseline's DMRs, the same pathway themes, and the same key genes through its enrichment step — but does so at the cost of a 5.9× inflated call set, inverted direction labels, and a broken gene-annotation column. Its engineering qualities — modular scripts, config-driven parameters, OOM protection, automated validation — are genuine, but the three silent defects demonstrate that engineering quality does not guarantee biological correctness.

What Experiment 1 contributes to the hypothesis is a clear separation of capability from reliability. On the capability side, the evidence is affirmative: Mimosa finds the signal (85.9% positional recall of the baseline), ranks its calls correctly (the strongest are the most corroborated), and converges on the correct biology (neural and developmental pathways, key genes recovered via enrichment). On the reliability side, the evidence is cautionary: three silent defects — a semantic parameter mismatch, a direction-convention error, and an empty annotation column — would each produce misleading biological conclusions if taken at face value, and none would have been detected without the triangulated comparison against the baseline and the published analysis.

This outcome supports the framing introduced in §1.4: that Mimosa can demonstrate statistical and biological competence while still harbouring errors that require external reference points to detect. Whether the same pattern — genuine capability alongside silent defects — recurs in a different dataset, organism, and experimental context is the question addressed in the next experiment (Chapter 5). The cross-experiment synthesis, including whether these defects are systematic or dataset-specific and what they imply for the practical deployment of agentic analysis pipelines, is taken up in the Discussion (Chapter 7).