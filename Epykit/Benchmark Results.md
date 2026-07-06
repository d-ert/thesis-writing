# Study 1: Fully Synthetic Data & Full Sweeps

**Goal:** Prove the mathematics of `epykit` work under controlled conditions.
*   **What you already have:** Sweeps across coverage ($5x$ to $25x$), sample sizes ($n=2$ to $10$), and overdispersion ($\phi$).
*   **How to improve it:** 
    *   **FDR Control validation:** Make sure you explicitly plot the *Empirical FDR vs. Target FDR* (e.g., if a tool is set to $q < 0.05$, does it actually yield $\le 5\%$ false positives?). Many tools claim an FDR of $0.05$ but actually yield $20\%$. If `epykit` holds the line at exactly $0.05$ across different $\phi$ (dispersion) values, that is a massive selling point.
    *   **Compute resources:** Track RAM and CPU time here. Synthetic data is a great place to show computational scaling ($O(N)$ vs $O(N^2)$) as you increase the number of CpGs or samples.


the latest results: [the folder](D:\Coding\Projeler\methyl_lib\epykit-benchmark3\epykit-benchmark\study1_try3)

![[Pasted image 20260622171615.png]]


## IMPORTANT
The last thing you did was to check the best dmc params and while that was happening you broke lr. the changes are reverted but the study1 pipeline needs to be run one last time to have healthy clean results tables etc. So after study3 finishes running rerun study1 one last time. If you can fix DSS because something is clearly not correct with that but idk


# Study 2: Semi-Synthetic Empirical Simulation

**Goal:** Prove `epykit` handles real-world genome topology, GC bias, and unmodeled background noise.
*   **How to do it correctly:** 
    1. Take real WGBS data of $N$ replicates from the **exact same biological condition** (e.g., 6 healthy control mice). 
    2. Split them randomly into two groups (3 pseudo-treatment vs 3 pseudo-control).
    3. Because they are the same condition, **any DMR found here is a False Positive**. Run your tools here to test strict Null control.
    4. Next, artificially "spike-in" DMRs by modifying the read counts in the pseudo-treatment group for specific genomic windows. 
*   **How to improve it:** Use the *dmrseq* paper’s exact strategy for this step. If `epykit` matches or beats *dmrseq* on *dmrseq’s* own home turf (their simulation style), reviewers cannot argue with your results.


dmrseq paper also have a git repo with scripts and i downloaded their sim data too so i can just plug epykit to that structure i think. 

Only thing is that their paper is not that informative and only has 1-2 figures





# Study 3: Real WGBS Data: GSE263850
**Goal:** Prove `epykit` finds biologically meaningful results that biologists actually care about.
*   **The Problem:** In real data, you have no ground truth. You don't know which CpGs are actually DMCs/DMRs.
*   **How to improve it (Orthogonal Validation):**
    *   **RNA-seq Concordance:** Do what the *dmrseq* paper did (Figure 4). Find a public dataset that has *both* WGBS and RNA-seq for the same samples (e.g., healthy vs. cancer). A good DMR caller should find DMRs in the promoters of genes that are Differentially Expressed (DE). Usually, promoter hypermethylation = gene downregulation. 
    *   **Concordance / UpSet Plots:** Plot an intersection of the DMRs found by `epykit`, `methylKit`, `DSS`, and `dmrseq`. You want to show that `epykit` finds the consensus DMRs, plus maybe some highly plausible novel ones that the others missed.
    *   **Runtime on real data:** Real whole-genome data is massive (~28 million CpGs). Show that `epykit` finishes in minutes/hours while others might crash or take days.


First results are in and they are exciting:
![[Combined DMR Benchmarking & Runtime Report.pdf]]

i think im going to replace the DSS data here with the baseline pipeline from the mimosa paper as its more true to the paper and i think it would be more fair.

























# Refining Your Release Strategy (The "Go-to-Market")


1. **Benchmark & Fix:** Run Studies 1, 2, and 3. Iterate until `epykit` is undeniably competitive or better (in speed, accuracy, or memory).
2. **Draft a Preprint & Publish the Package:** Write a short, punchy paper with your 3 studies as the main figures. Upload the package to GitHub/PyPI/Bioconda, and simultaneously upload the paper to **bioRxiv**.
3. **Community Feedback (Reddit/Twitter/Biostars):** *Now* you post to Bioinformatics subreddits, Twitter, and Biostars saying: *"We just released `epykit`, a new Python WGBS caller that is X times faster than DSS/dmrseq. Check out the GitHub and our bioRxiv preprint."* Linking a bioRxiv preprint gives your tool instant legitimacy.
4. **Peer Review:** Submit the manuscript to a journal (e.g., *Bioinformatics*, *NAR Genomics and Bioinformatics*, or *Genome Biology*). You can implement the feedback you got from Reddit/Twitter users during the peer-review revision process.

**Summary:** Your scientific plan is flawless and follows the exact trajectory of a high-impact bioinformatics methods paper. Start crunching the Study 1 data!


