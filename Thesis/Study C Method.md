# Study C — Synthetic Ground-Truth Benchmark with WGBSSuite

## Connections

- [[Thesis MOC|Thesis / Mimosa MOC]]
- [[Thesis/Thesis_v1/04_validation1_replication|Chapter 4 - Validation I: Replication]]
- [[References MOC|References MOC]]
- [[WGBS benchmarking|WGBS benchmarking]]

**Purpose:** operationalise H2 (calibration) — measure whether Mimosa's reported false-discovery rate is honest, and whether its sensitivity is comparable to an expert-run DSS analysis, against data where the true DMRs are known exactly.

**Source:** `git clone https://github.com/SystemsGeneticsSG/WGBSSuite.git` (the old `wgbssuite.org.uk` site is dead; the GitHub mirror is the actual code from Rackham et al. 2015, _Bioinformatics_ 31(13):2223–2225). Cite the paper, link the GitHub repo, and note the dead-link substitution once in your Methods text — reviewers will hit the same dead link if they try to verify it.

---

## 0. Environment setup — do this first, before touching the simulator

WGBSSuite is 2016-era R code, last updated for a Linux/Mac HPC environment. Two things will bite you immediately if you're on the Windows workstation:

- `benchmark_WGBS.R` calls `registerDoMC(16)` from the `doMC` package. **`doMC` does not exist on native Windows R** (it's fork-based, POSIX-only). Either: (a) run this whole study inside WSL2 with a Linux R install, or (b) patch `registerDoMC(16)` → `registerDoParallel(makeCluster(N))` using `doParallel` instead, which works cross-platform. (a) is less work and is consistent with the rest of your pipeline likely running through Docker/WSL already for the MCP servers — check what Server B already assumes.
- The benchmark script auto-runs **BSmooth** and **MethylSig** in addition to MethylKit. Confirm these R packages actually install cleanly before you depend on the auto-benchmark path — if either fails, you can still run `methylkit_for_bench()` alone and skip straight to scoring your own DSS/Mimosa calls against the ground truth (Section 4), which is the part you actually need.
- Pin versions: record the exact commit hash of WGBSSuite you clone, your R version, and package versions in your reproducibility manifest (same place you're already tracking env manifests for Annex 9). This code hasn't been touched since 2016 and isn't on CRAN/Bioconductor, so "which version" is a real methodological detail, not boilerplate.

---

## 1. Derive simulation parameters from your own real data (don't use paper defaults blindly)

WGBSSuite's whole pitch is that its parameters can be estimated from a real dataset so the simulation resembles your actual study rather than an arbitrary toy case. Use **Study A (GSE263850, human)** for this, since you already have it processed and baselined.

Run the suite's analysis/estimation script (`analyse_WGBS.R` or equivalent — confirm the exact filename once you have the repo checked out; the paper describes an "analysis of real data" step that produces a summary PDF and a parameter set) against your Study A coverage files. This should give you back-estimated:

- probability of methylated read at a "methylated-state" CpG,
- probability of methylated read at a "demethylated-state" CpG,
- error/variance around each,
- CpG spacing distribution parameters (the exponential-decay values used to drive the two-state HMM for CpG placement).

**Why this matters for your thesis, not just convenience:** it lets you write in Chapter 5 that the synthetic benchmark's background methylation landscape was calibrated to your own real replication dataset rather than an arbitrary default — this directly strengthens the "knowable truth, not an artificial toy" framing from your Introduction §1.8.

If the estimation script turns out to be broken or too fragile to trust (real risk with unmaintained code), fall back to the paper's own reported example values (`0.9203` / `0.076` methylated/demethylated success probabilities were used in their own example run) and state explicitly in the thesis that parameters are paper-derived defaults rather than data-derived — that's an honest, defensible fallback, just a weaker claim than the data-derived version.

---

## 2. Generate the ground-truth synthetic dataset

Run `simulate_WGBS.R` in **single-run mode** (not `multi`, which is for repeated ROC/AUC sweeps — useful later for a robustness curve, but start with one dataset you can inspect by eye). At minimum you need to decide, and record in your methods text:

|Parameter|What it controls|Suggested starting point|
|---|---|---|
|number of CpGs|scale of the simulated genome|large enough to get a meaningful number of DMRs at your chosen % differential (thousands, not hundreds)|
|P(methylated read \| methylated state)|background signal strength|data-derived from Step 1|
|P(methylated read \| demethylated state)|background signal strength|data-derived from Step 1|
|error terms|noise around each state|data-derived from Step 1|
|number of samples / replicates per group|matches your real design|**match Study A's 3 vs 3 design** so the two studies are comparable|
|phase difference / hyper-hypo balance|how DMRs distribute|pick something and justify it, e.g. 0.5 = unbiased hyper/hypo, matching a null expectation|
|CpG-distance decay parameters|spatial clustering realism|data-derived from Step 1|
|distribution type|binomial vs truncated|binomial is the simpler, better-tested path — start there|

The output is a table of simulated CpGs with **two critical truth columns**: genomic location and true methylation _state_ (methylated-region vs demethylated-region label per CpG) — this state vector is what `extract_DMR_phase()` later turns into your ground-truth "which bases are truly differentially methylated" array and the true DMR boundary list. Everything downstream depends on preserving this truth vector unmodified and unscored until Section 4.

**Also generate a null dataset**, using the _same_ methylated-state probability for both simulated groups (no true group difference, only sampling noise). This is your dedicated FPR-under-null benchmark — every call any method makes on this dataset is a false positive by construction, no truth-array logic required. Keep it as a separate run from the main effect-bearing dataset.

---

## 3. Feed the simulated data through your actual pipelines

This is the step that determines whether Study C is testing "DSS in the abstract" or "Mimosa specifically" — make sure it's the latter.

1. **Inspect WGBSSuite's raw output format first**, before writing any conversion code — don't assume column names. It's a flat count table (position, state, counts), not a Bismark `.cov`/cytosine report. You will need a short conversion script that reshapes it into whatever format your two arms below expect.
2. **Expert-run arm:** convert to DSS's native `(chr, pos, N, X)` input format and run your existing baseline DSS script (the same `DMLfit.multiFactor` + `DMLtest.multiFactor` + `callDMR` pipeline you used for Study A/B) directly on the simulated counts. This is your "expert ceiling" arm, exactly analogous to the baseline column in your run23 comparison.
3. **Mimosa arm:** this is the one that actually needs the coverage-file convention Mimosa/Server B expects (likely a Bismark-style `.cov`: chr, start, end, %meth, count_meth, count_unmeth). Convert WGBSSuite's simulated counts into that format, then hand the folder to Mimosa exactly as you did for real data, with the same goal specification you used for run23. Do not hand-hold it toward the right parameters — the whole point is to see whether it reproduces the same `p.threshold`/direction/annotation behaviour you already caught, on data where you now know the right answer.
4. Optionally, a **methylKit-only reference arm** via WGBSSuite's own `methylkit_for_bench()` gives you a documented third point of comparison consistent with the original paper's benchmark, useful context in your Discussion chapter even if it's not one of your three core arms.

---

## 4. Score against ground truth — this is where H2 gets its numbers

WGBSSuite ships scoring functions you can reuse or reimplement inside your own shared scoring library:

- `extract_DMR_phase()` — turns the true per-CpG state vector into (a) a presence/absence array (`0011100...`, 1 = truly differentially methylated) and (b) a list of true DMR boundary intervals.
- `score_overlap()` — per-base confusion matrix (TP/FP/FN/TN) against a predicted call vector at a given cutoff, returning sensitivity and specificity directly.
- `score_overlap_DMR()` — region-level scoring: does each true DMR overlap at least one predicted DMR, and vice versa, giving region-level precision/recall rather than per-base.

**Apply both functions to each arm's calls (expert-DSS, Mimosa, methylKit) at your chosen significance threshold**, and also **sweep across a range of thresholds** to get a full sensitivity/specificity curve per arm — this is what lets you report calibration, not just a single confusion matrix. The `FDR_cutoffs` construction already in `benchmark_WGBS.R` (log-spaced cutoffs across orders of magnitude) is a reasonable template to reuse.

The specific H2 numbers you want out of this section:

- **Sensitivity** of Mimosa vs. expert-DSS at matched nominal FDR — is Mimosa "comparable," worse, or better at finding true DMRs?
- **Empirical FDR vs. reported/nominal FDR** for Mimosa specifically — plot reported cutoff on the x-axis, actual (ground-truth-verified) false discovery proportion on the y-axis. A well-calibrated method sits near the diagonal; a method like your run23 pipeline, which fed a q-value into a raw-p-value slot, would show empirical FDR far above nominal at every cutoff — this is the chart that would have caught that bug immediately, and it's the single most useful figure Study C can produce.
- **FPR under the null dataset** from Section 2 — a direct, ground-truth-free cross-check of the FDR-calibration curve above, and your only real end-to-end check that includes the FASTQ/alignment layer if you additionally push the null dataset through Sherman-simulated reads and nf-core/methylseq first (see the earlier discussion — that's a smaller, complementary side-check, not a replacement for this section).

---

## 5. What to actually report in Chapter 5

- One calibration figure (reported vs. empirical FDR) per method (expert-DSS, Mimosa, optionally methylKit).
- One sensitivity-at-matched-FDR table, same three columns.
- The null-dataset FPR number, reported alongside, as a sanity anchor.
- A short methods paragraph citing Rackham et al. 2015 and the GitHub source, stating your parameter-derivation approach (Step 1), your design choices (Step 2 table), and your exact WGBSSuite commit hash / R environment.
- If Mimosa reproduces a p-threshold-style miscalibration here the same way it did in run23, that is a genuine, citable finding — not a failure of the thesis. Report it as your H2 verdict honestly, exactly as your Introduction §1.3 commits you to.

---

## Open items to resolve once you have the repo checked out

- Confirm the exact filename of the parameter-estimation script (Step 1) — referred to generically in the paper's abstract/docs but not confirmed here by exact name.
- Confirm WGBSSuite's raw simulated-data column layout before writing the conversion script in Step 3.
- Decide binomial vs. truncated-binomial distribution mode and justify the choice in text (binomial is the safer, better-precedented default).
- Decide whether BSmooth/MethylSig dependencies are worth fighting with, or whether you skip the auto-benchmark harness entirely and call `extract_DMR_phase()` / `score_overlap()` / `score_overlap_DMR()` directly against your own DSS and Mimosa outputs (the leaner, more targeted path).
