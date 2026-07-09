
the result of analyse_WGBS.R
```R

The following information can be used to parametrise the simulation of data to match your dataset 
The average difference in methylation proportion:  0.0663982983974777 
The standard deviation in difference in methylation proportion:  0.0803548692511872 
The max difference in methylation proportion:  0.99999999 
The probability of success in a methylated region:  0.928435470021939 
The probability of success in a unmethylated region:  0.135516953414242 
The average coverage in a methylated region:  10 
The average coverage in an unmethylated region:  9 
The fast decay rate for CpGs:  0.09031924348971 
The slow decay rate for CpGs:  0.0031831900256275 

RAW methylated coverage avg: 10.41697 
Further details can be found in: analysis_out/study_C_run2.analysis_of_real_data.pdf 

nb. in Unix: evince analysis_out/study_C_run2.analysis_of_real_data.pdf 
or in OsX: open analysis_out/study_C_run2.analysis_of_real_data.pdf 

To create a binomially simulated dataset with the default settings execute the following:
Rscript simulate_WGBS.R 5000 0.928435470021939 0.135516953414242 0.2 0.2 8.87444791461314 8.87444791461314 3 2 0.05 0.5 0.09031924348971,0.0031831900256275 analysis_out/study_C_run2 binomial
To create a negative binomially simulated dataset with the default settings execute the following:
Rscript simulate_WGBS.R 5000 0.928435470021939 0.135516953414242 0.2 0.2 8.87444791461314 8.87444791461314 3 2 0.05 0.5 0.09031924348971,0.0031831900256275 analysis_out/study_C_run2 truncated

```


the result of simulate_WGBS.R

```R

mlegrand@pivoine:~/Desktop/Deniz/study_C/WGBSSuite$ Rscript simulate_WGBS.R 5000 0.928435470021939 0.135516953414242 0.2 0.2 8.87444791461314 8.87444791461314 3 2 0.05 0.5 0.09031924348971,0.0031831900256275 analysis_out/study_C_run2 binomial Attaching package: ‘zoo’ The following objects are masked from ‘package:base’: as.Date, as.Date.numeric Creating the simulated dateset. |======================================================================| 100% ##########################SIMULATION COMPLETE############################ The simulated data can be found here: analysis_out/study_C_run2_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.135516953414242_0.2_0.2_0_0.05_0.5_.txt A pdf summarising the simulated data can be found here: analysis_out/study_C_run2_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.135516953414242_0.2_0.2_0_0.05_0.5_.txt.pdf To run the benchmarking script on this dataset with the default settings use:

Rscript benchmark_WGBS.R analysis_out/study_C_run2_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.135516953414242_0.2_0.2_0_0.05_0.5_.txt 2 3 1 999999 1 1 15 30 100 1000000 0 0 200 0 0 analysis_out/study_C_run2 0 

mlegrand@pivoine:~/Desktop/Deniz/study_C/WGBSSuite$ Rscript simulate_WGBS.R 5000 0.928435470021939 0.928435470021939 0.2 0.2 8.87444791461314 8.87444791461314 3 2 0.05 0.5 0.09031924348971,0.0031831900256275 analysis_out/study_C_run2_null binomial Attaching package: ‘zoo’ The following objects are masked from ‘package:base’: as.Date, as.Date.numeric Creating the simulated dateset. |======================================================================| 100% ##########################SIMULATION COMPLETE############################ The simulated data can be found here: analysis_out/study_C_run2_null_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.928435470021939_0.2_0.2_0_0.05_0.5_.txt A pdf summarising the simulated data can be found here: analysis_out/study_C_run2_null_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.928435470021939_0.2_0.2_0_0.05_0.5_.txt.pdf To run the benchmarking script on this dataset with the default settings use:

Rscript benchmark_WGBS.R analysis_out/study_C_run2_null_5000_1_0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9_8.87444791461314_8.87444791461314_0.928435470021939_0.928435470021939_0.2_0.2_0_0.05_0.5_.txt 2 3 1 999999 1 1 1530 100 1000000 0 0 200 0 0 analysis_out/study_C_run2_null 0 mlegrand@pivoine:~/Desktop/Deniz/study_C/WGBSSuite$

```

### Quick sanity check on what you got

The output filenames encode the full parameter set the script actually used internally (not just what you passed in — note it also shows `0.65_0.2_0.35_0.8_0.9_0.1_0.1_0.9` etc., which are the script's own internal HMM transition constants, hardcoded in `generate_sim_set()`, not something you controlled). That's expected — ignore that middle chunk, it's constant across your runs.

The one thing worth confirming by eye right now, per the Plan's "start with one dataset you can inspect" instruction:

- **Main run filename** ends in `..._0.928435470021939_0.135516953414242_...` — two _different_ probabilities (methylated vs. unmethylated region), confirming this run has a true group difference.
- **Null run filename** ends in `..._0.928435470021939_0.928435470021939_...` — same probability twice, confirming no true difference. Good — this is exactly the audit trail you want; you can literally tell the two runs apart from the filename alone, which is handy for your reproducibility manifest.

Open both `.pdf` files (`evince` on Linux) and check:

- the main run shows visible separation between the two sample-group traces in the differentially-methylated blocks,
- the null run shows the two traces tracking each other closely (only noise, no systematic offset).

### Before writing any conversion code — inspect the raw column layout (Plan §3, item 1)

Don't assume the column names. Based on the script's own `generate_sim_set()` logic, the `.txt` file should be a flat table with:

```
col 1: locs        (CpG genomic position)
col 2: diff_methed (0/1 — is this CpG truly in a differentially-methylated block)
cols 3+: 4 columns per replicate × (replicates × samples) = 4 × 3 × 2 = 24 columns
         → each block of 4 = [methylated_count (x), coverage (n), coverage (repeated), proportion]
```

So you should see **26 total columns**. Confirm this directly:

bash

```bash
head -n 3 analysis_out/study_C_run2_5000_..._.txt | column -t
wc -l analysis_out/study_C_run2_5000_..._.txt
```

Check that:

1. Column count matches 26 (2 + 24).
2. Column 2 (`diff_methed`) is binary and its 1s cluster in contiguous runs (not scattered) — that's your ground-truth DMR signal.
3. The 4-column repeating pattern per replicate matches `x / n / coverage / proportion` as expected, so you know exactly which raw columns become which BSseq/DSS/Mimosa input columns later.

Once you've confirmed that layout, you're ready for the actual Section 3 conversion work: reshaping into DSS's `(chr, pos, N, X)` format for the expert arm, and into a Bismark-style `.cov` for the Mimosa arm. Want to do that inspection together first (paste `head` output here) before I help draft the conversion script?
