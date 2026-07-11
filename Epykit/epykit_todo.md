---
tags:
  - epykit
  - Todo
---

- [ ] add a explore_dataset (find a better name) to look at stuff like 
	- **Coverage distribution** – mean, median, % sites with coverage <5.
	
	- **Methylation level distribution** – particularly the proportion of sites with beta <0.1 or >0.9.
	
	- **Between‑replicate variance** – does Study 2 have higher biological variability?
	
	- **DMR properties** – width, effect size, CpG density.
	to analyze the dataset and see the general landscape

- [ ] Look at the fdr improvements in the [[fdr_analysis]] and add the ones that improve the package.

- [ ] when i run this code i dont think epykit uses from cache because it takes a long time on the second run too. we need to double check caching mechanism 
```python
ep.tl.dmc(
    md,
    fdr_method="fdr_tsbh",
    neighbour_combine=True,
    neighbour_bp=500,
    sep_fallback=True
)
```


- [ ] **On WGBS itself first, since you asked directly:** CpG count isn't really a growth axis anymore — 22M is close to the ceiling for any mammalian genome, and you're already streaming it. The axis that _would_ eventually strain the current design is **sample count**, not site count — biobank-scale cohorts (thousands of methylomes) rather than genome-scale sites. Polars' streaming engine is single-node, so at real biobank scale you'd likely want to fan the existing chromosome-partition key out across a cluster (Dask/Ray orchestrating the same per-chromosome units you already have) rather than rewrite the per-site math. The other two genuinely useful extensions are cloud-object-store-native reads (S3/GCS, which pyarrow/polars already support if `store_dir` accepts a URI) for cohorts too large for local disk, and making sure your Parquet row groups are sorted/statistics-rich enough for min/max pruning on `region_beta()`-style locus queries. None of that is a redesign — it's stress-testing the same primitives on a second axis.
- [ ] https://chanzuckerberg.github.io/cellxgene-census/
- [ ] https://github.com/scverse/SnapATAC2
- [ ] **Long-read (nanopore) methylation** — this is close to free. Dorado + modkit already output per-site methylated/unmethylated counts in bedMethyl format, which is structurally almost identical to a Bismark `.cov` file. Modkit itself has a basic built-in DMR command, but there's no real Python statistical ecosystem sitting on top of it the way there is for bisulfite data — meaning you could plausibly add a `read_nanopore_bedmethyl()` ingest function and get the rest of your DMC/DMR/annotation/report pipeline for free. Very high leverage, almost no new architecture.
- [ ] **Methylation arrays (450K/EPIC/EPICv2)** — this one's live right now. A paper just came out this year introducing a new package (Pylluminator) specifically because it says the existing Python options — methylprep/methylize, CpGTools, Mepylome — are either unmaintained or too shallow, while R's minfi is still the backend that half a dozen other Bioconductor packages (ChAMP, DMRcate, missMethyl, and others) build on top of. EPICv2 now covers over 930,000 loci — small enough that it doesn't need your streaming Parquet layer at all, it'd sit happily as an in-memory dataframe reusing your existing `lr`/`glm`/`welch_t` engines directly. It's the same biology you already understand, so the domain-expertise cost is near zero — but note the field isn't empty anymore, so you'd need real differentiation (probably your stats panel + annotation depth) rather than just "Python version of minfi."
- [ ] **Proteomics** — this is the one place your instinct is right. Mass-spec differential abundance is still overwhelmingly R territory — limma, MSstats, PECA, msqrob2, and proDA are all R/Bioconductor packages, each handling missingness differently (imputation vs. hurdle models vs. probabilistic dropout), and Python's answer so far is thinner tools like AlphaPeptStats, which covers normalization, imputation, and standard statistical tests but doesn't yet match the methodological depth of the R panel. This is structurally the same opportunity WGBS was for you: an R-dominated field, small enough matrices that storage isn't the issue, where a maintained _panel_ of engines behind one canonical schema (your actual innovation, more than the Parquet layer) would be genuinely new in Python.