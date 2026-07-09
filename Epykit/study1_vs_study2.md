---
tags:
  - Todo
  - epykit
---
# Study 1 vs Study 2

## Connections

- [[Epykit MOC|epykit MOC]]
- [[Epykit/Benchmark Results|Benchmark results]]
- [[Epykit/fdr_analysis|FDR analysis]]
- [[References MOC|References MOC]]

!!! ONEMLIII
bu comparisona gse verisini de eklicen bunun icin claudish session'i:
claude --resume ddca1c41-35da-4109-a07c-8ccf8bef90a0


| **Metric**                             | **Study 2 (dmrseq WGBS benchmark)**   | **Study 1 (your epykit sim)**            |
| -------------------------------------- | ------------------------------------- | ---------------------------------------- |
| Genome scope                           | whole genome, ~21.8M CpGs/sample      | chr1 only, 100k CpGs                     |
| Design                                 | 3v3 (n3) and 2v2 (n2) dendritic cells | 3v3, parameterised by φ/coverage         |
| Coverage (pooled, per-site)            | mean ≈ 28 (within-group) / 56 (all 6) | mean ≈ 30–120 (depends on cov param)     |
| % sites coverage < 5                   | ~0.2–0.3% (within grp), ~0% pooled    | 0.00% (all cells)                        |
| Beta mean / median                     | 0.78 / 0.92                           | 0.36 / 0.29                              |
| % beta < 0.1                           | ~11.4%                                | ~29–39%                                  |
| % beta > 0.9                           | ~54%                                  | ~6–14%                                   |
| Between-replicate β SD (mean / median) | 0.08 / 0.06                           | 0.13–0.21 / 0.12–0.20                    |
| % sites with rep-SD > 0.2              | ~7%                                   | ~14–53%                                  |
| # true DMRs                            | 3,000 (per design)                    | 200                                      |
| DMR width (mean / median bp)           | 2,850 / 1,676                         | 7,945 / 7,126                            |
| DMR effect size                        | not in truth BED                      | median region_delta 0.20, 88% \|Δ\|>0.25 |
| CpGs per DMR                           | —                                     | ~19                                      |

The dataset comparison you’ve provided makes the problem very clear. **epykit’s default settings are poorly suited to the methylation profile of Study 2**, and this explains both the inflated FDR and why Study 1 (and likely Study 3) worked fine.

## What’s wrong with Study 2 for epykit’s defaults?

| Property | Study 2 (benchmark) | Study 1 (your sim) | Why it matters |
|----------|---------------------|-------------------|----------------|
| **Median beta** | **0.92** | 0.29 | Most CpGs are near fully methylated |
| **% beta > 0.9** | **54%** | 6–14% | Vast majority of sites have very low binomial variance |
| **Between‑replicate SD** | **0.08 / 0.06** | 0.13–0.21 | Study 2 has tighter replication – small absolute changes look “significant” |

When a CpG is already at beta ≈ 0.95, even a single‑read methylation difference between groups can produce a huge effect size (e.g. 9/10 vs 10/10 → Δ = 0.10) while the binomial variance `pi*(1‑pi)` is near zero. The **quasi‑binomial likelihood‑ratio test** divides the observed deviation by this near‑zero variance, inflating the test statistic and deflating p‑values. The dispersion correction (phi) can’t fully compensate because it multiplies the already tiny variance – it would need to be enormous to restore calibration.

In Study 1, beta values are spread across the whole range, variance is higher, and boundary sites are rare. The same test behaves well there.

## Why the q‑values are so miscalibrated

Your benchmark report warns:  
`⚠ q-values overoptimistic by 168986× (mean q=0.0000 vs eFDR=0.6992)`.

This happens because the p‑value histogram for null sites is **heavily skewed toward zero** – the test is anti‑conservative on Study 2. The BH correction then assigns tiny q‑values to many false positives. This is **not a bug** in your code; it’s a consequence of applying a binomial‑based test to boundary‑dominated data without stabilization.

## What to do – immediate fixes

You can make epykit work well on Study 2 by turning on the **DSS‑style smoothing** that you already implemented. Smoothing borrows information from neighboring CpGs and pulls estimated proportions away from the extreme boundaries, greatly improving calibration.

**Recommended parameter set for Study 2‑like data:**

```python
epykit.tl.dmc(
    ...
    test="lr",
    dispersion="eb",      # empirical‑Bayes shrinkage of dispersion
    reference="adaptive", # keep adaptive F/χ² switch
    smoothing=True,        # ← THIS IS CRITICAL for boundary‑beta data
    smoothing_span_bp=500, # DSS default
    ...
)
```

If you also want to be extra conservative, use `reference="F"` to always use an F‑distribution (heavier tailed than χ²) – it will lower FDR at some power cost.

**For the tiling mode:** Tiling pools counts across adjacent CpGs, which **amplifies** the boundary beta problem if the tile consists of many highly‑methylated sites. Avoid tiling for Study 2‑type data until you add spatial‑correlation variance scaling (planned for v0.8). Stick with the per‑CpG DMC step followed by region merging.

## Next steps

1. **Re‑run epykit on Study 2 with `smoothing=True` + `dispersion="eb"`** and re‑benchmark. I predict the FDR will drop dramatically.
2. **Run a null‑label permutation test** on Study 2 with and without smoothing to confirm that smoothing restores uniformity of p‑values under the null.
3. **If smoothing fixes Study 2 but you still want a non‑smoothed option**, consider adding a simple **beta‑clipping guard** (e.g., exclude sites with mean beta outside [0.2, 0.8] or apply a logit‑t test only to those sites) – but that would cost power. Smoothing is the standard solution used by DSS and others for exactly this reason.

The core code is sound; the issue is that the **default parameterisation** was inadvertently optimised for datasets with a more uniform methylation landscape (like your simulation). Now you know the trigger, you can either document the limitation or make `smoothing=True` the default when the median beta is high – but that’s a design decision.

Let me know what FDR you get after re‑running with smoothing.
