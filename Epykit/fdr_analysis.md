---
tags:
  - Todo
  - review
---
# FDR analysis

## Connections

- [[Epykit/MOC|epykit MOC]]
- [[Epykit/epykit_todo|epykit TODO]]
- [[Epykit/study1_vs_study2|Study 1 vs Study 2]]
- [[References/MOC|References MOC]]

After reviewing the provided source code in detail, I identified several statistical choices that can inflate the false-discovery rate (FDR) or reduce power. The most critical issue is an arbitrary degrees‑of‑freedom floor in the quasi‑likelihood F‑test, which can make p‑values far too liberal. Below I walk through each component you asked about, point out the problems, and suggest targeted improvements.

---

## 1. **Dispersion models and the `DF_PHI_FLOOR` (critical FDR inflation)**

### What the code does
All quasi‑likelihood tests (`lr`, `glm`, `glm_contrast`) estimate a dispersion parameter *ϕ* (overdispersion relative to binomial) and then compute an F‑statistic or a scaled χ².  
When the overdispersion is larger than 1, the code switches from a χ²(1) reference to an *F*(1, df) distribution, where *df* is the (possibly shrunken) degrees of freedom used to estimate *ϕ*.

### The problem
`_score_finalize` and `_glm.reference_pvalues` both apply a hard floor to the denominator degrees of freedom:

```python
DF_PHI_FLOOR = 50.0
...
df_phi_floored = np.maximum(df_phi, DF_PHI_FLOOR)
```

This means: **no matter how few replicates you have, the denominator df will never drop below 50**.  

#### Why this inflates FDR
For small or moderately replicated experiments, the true residual df (and thus the df of the dispersion estimate) is often much smaller than 50.  
- With *n* = 3 vs 3, the per‑site residual df is roughly (3+3–2) = 4.  
- Shrinkage may add a few pseudo‑df (default 4), giving e.g. *df* ≈ 8.  

An *F*(1, 8) distribution has a much heavier tail than an *F*(1, 50) distribution (which is essentially χ²(1)).  
By flooring to 50, you are **artificially making the reference distribution lighter‑tailed**, thereby assigning smaller p‑values to the same test statistic. This directly inflates the false‑positive rate.

*Example*: a LR statistic of 5 gives p ≈ 0.025 under χ²(1) (or F(1,50)), but p ≈ 0.06 under F(1,8). The floor eliminates the conservativeness that the F‑test is supposed to provide when *ϕ* > 1.

### How to fix
- Remove the floor entirely, or set it to a very small value (e.g. 2.0) only to avoid numerical division by zero.
- The degrees of freedom should be allowed to fall to their actual estimated values.  
  - For the chromosome‑wide dispersion, *df* is often large anyway; for site‑wise or shrunken dispersions, the low *df* is exactly what makes the F‑test appropriately conservative.
- If the goal was to avoid unstable p‑values, a better approach is to use **empirical Bayes moderation of the dispersion** (see recommendation below), not a fixed floor.

---

## 2. **Smoothing implementation (`_smooth_sample_counts_box`)**

### What it does
When `smoothing=True`, each sample’s meth and coverage counts are smoothed *before* aggregating across replicates, using a moving‑average box kernel of width `smoothing_span_bp`.

```python
meth_sm[i] = (cum_meth[hi] - cum_meth[lo]) / n_window
cov_sm[i]  = (cum_cov[hi]  - cum_cov[lo])  / n_window
```

The smoothed counts (now floats) are then passed to the likelihood‑ratio test.

### Statistical concerns
- **No adjustment for induced correlation** – Smoothing creates strong local correlations among CpGs. The LR test treats every site as independent. Even with a dispersion correction, the effective number of independent observations is reduced, which can lead to **p‑values that are too small** (anti‑conservative).  
- **Effect on dispersion estimation** – Smoothing reduces within‑group variance, which may artificially lower the estimated overdispersion *ϕ*, further shrinking p‑values.

### Recommendation
- If smoothing is kept, consider using a **variance‑stabilising transformation** or a **correlation‑aware model** (e.g., a generalised estimating equation or a mixed model).  
- At minimum, warn users that smoothing increases the risk of false positives, especially for broad peaks.  
- A safer alternative is to smooth only for visualisation, not for inference.

---

## 3. **Reference distribution (`reference='adaptive'` and the F‑test switch)**

### Logic
```python
if reference == "adaptive":
    p_F    = sp_stats.f.sf(chi2_stat, dfn=1, dfd=df_phi_floored)
    p_chi2 = sp_stats.chi2.sf(chi2_stat, df=1)
    pvals  = np.where(phi_eff > 1.0, p_F, p_chi2)
```
This is a reasonable quasi‑likelihood approach: use the heavier‑tailed F when overdispersion is present, otherwise the χ².

### Problem
The switch condition is `phi_eff > 1.0`. Because `phi_eff` is always forced ≥ 1 (via `max(min_dispersion, …)`), the F‑test is used *whenever any overdispersion is detected* (ϕ > 1). Combined with the df floor, this becomes the default for all real data.  

The choice of threshold is sensible, but the real damage comes from the df floor discussed above.

---

## 4. **LR engine (`_score_finalize` for `test='lr'`)**

### The test statistic
```python
lr_terms = (
    u_case * np.log(pc_safe / pi_pool_safe) + v_case * np.log((1-pc_safe) / (1-pi_pool_safe))
    + u_ctrl * np.log(pk_safe / pi_pool_safe) + v_ctrl * np.log((1-pk_safe) / (1-pi_pool_safe))
)
stat_raw = 2.0 * lr_terms
```
This is the correct likelihood‑ratio statistic for a 2×2 table (G‑test), using the total meth/unmeth counts across replicates.  

The division by `phi_eff` to obtain a quasi‑χ² statistic is standard.

### Small bias from clipping
Proportions are clipped to `[_BETA_EPSILON, 1-_BETA_EPSILON]` (ε ≈ 1e‑6). This avoids log(0) but can introduce slight bias for very low coverage sites. It is not a major FDR driver.

---

## 5. **Separation fallback (`sep_fallback=True`)**

### What it does
For sites with |meth_diff| ≥ `sep_threshold` (default 0.9) and LR‑p > 0.05, it recomputes a Fisher exact test on the aggregated 2×2 table and keeps the smaller p‑value.

```python
if p_fb < pvals[idx[k]]:
    pvals[idx[improved]] = p_fb[improved]
```

### Statistical concern
This is **a one‑way adjustment**: it can only *lower* p‑values, never increase them. While motivated by the LR test being conservative for extreme differences, it introduces a **post‑hoc selection bias** that can inflate the FDR, especially if the threshold is not rigorously calibrated. It also uses the same data to both select and re‑test.

### Recommendation
- Avoid enabling `sep_fallback` by default.  
- If used, the fallback p‑values should be corrected for selection (e.g., by adjusting for the number of tested sites), or better, the LR test itself should be replaced by a more robust model (e.g., a beta‑binomial regression) that handles extremes natively.

---

## 6. **Dispersion estimation details**

The site‑wise dispersion `phi_site = (chi_case + chi_ctrl) / df_i` is computed from the Pearson χ² contributions.  
Shrinkage towards a chromosome‑wide estimate is done via:
- **Shrinkage (simple):** `phi_eff = (df_i*phi_site + w*phi_hat) / (df_i + w)` with `w=4`.
- **Empirical Bayes (eb):** estimates `w_eb` from the variance of site‑wise ϕ’s using a moment estimator.

These are reasonable first‑order approximations, but the EB estimator (`a_mom = m^2 / v + 2`) can be unstable with few sites. A more principled approach would be to use the **edgeR/limma squeezeVar** style with a prior degrees of freedom, but the current method is not a major FDR inflator *per se*.

---

## 7. **Other potential improvements**

- **Small sample sizes:** The `welch_t` test is known to be underpowered; the warnings are appropriate. The `lr` test with dispersion estimation is a better choice, but for *n* < 3 it still has low power. The package could incorporate a **moderated t‑test** (e.g., using a prior variance) to stabilise small‑n experiments.
- **Combined neighbour p‑values (`combine_neighbour_pvalues`):** This uses Stouffer’s method with a sign‑agreement filter. Without correcting for the multiple‑testing of neighbouring windows, it can create artificially significant regions. It should be used with caution and ideally followed by a DMR‑level FDR correction (which the sliding‑window/chain‑merge callers do).
- **Multiple testing:** The BH and Storey procedures are correctly implemented and applied after DMR aggregation.

---

## Summary of top recommendations to improve power and control FDR

1. **Remove or drastically reduce `DF_PHI_FLOOR`** – This is the single most impactful change. Set it to `2.0` (just to avoid zero) or eliminate it entirely.
2. **Rethink `sep_fallback`** – Either drop it or convert it into a proper model selection (e.g., always use a beta‑binomial test for high‑difference sites without double‑dipping).
3. **Smoothing** – Add a clear warning that smoothing inflates false positives; consider offering a correlation‑adjusted test or recommending it only for visualisation.
4. **Dispersion shrinkage** – Replace the ad‑hoc EB shrinkage with a robust moderated dispersion estimator (similar to `limma::squeezeVar`) to stabilise ϕ when the number of sites per chromosome is small.
5. **For very small samples** – Integrate a moderated t‑statistic (e.g., using a prior on the logit scale) as a fallback when `test='lr'` has few residual df.

Implementing these changes would make the package substantially more powerful without sacrificing FDR control.
