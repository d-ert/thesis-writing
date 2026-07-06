---
tags:
  - epykit
  - Todo
---

- add a explore_dataset (find a better name) to look at stuff like 
	- **Coverage distribution** – mean, median, % sites with coverage <5.
	
	- **Methylation level distribution** – particularly the proportion of sites with beta <0.1 or >0.9.
	
	- **Between‑replicate variance** – does Study 2 have higher biological variability?
	
	- **DMR properties** – width, effect size, CpG density.
	to analyze the dataset and see the general landscape

- Look at the fdr improvements in the [[fdr_analysis]] and add the ones that improve the package.

- when i run this code i dont think epykit uses from cache because it takes a long time on the second run too. we need to double check caching mechanism 
```python
ep.tl.dmc(
    md,
    fdr_method="fdr_tsbh",
    neighbour_combine=True,
    neighbour_bp=500,
    sep_fallback=True
)
```

