# Chapter 8 — Bibliography

> **Working bibliography seed.** This file holds the BibTeX entries backing the `[@key]` citations
> used in the Markdown chapters; at Pandoc time it is exported to a `references.bib` and rendered
> by `citeproc`. **Every entry must be verified against the primary source before submission** —
> author lists, years, venues, volume/pages and DOIs were drafted from working knowledge and are
> not yet checked. Each entry carries a `note` with its status:
>
> - `STATUS: confident` — a well-known landmark paper; verify exact volume/pages/DOI only.
> - `STATUS: VERIFY` — recent or fast-moving source (agent / MCP / benchmark literature); confirm
>   it exists, get the canonical citation, and replace if superseded. **Do not cite as final.**
>
> Run a dedicated literature-verification pass (web search / reference manager) over §2.4–2.5
> citations especially — they are the knowledge-cutoff-sensitive ones flagged in the plan.

## Methylation biology & WGBS (§2.1)

```bibtex
@article{bird2002,
  author  = {Bird, Adrian},
  title   = {{DNA} methylation patterns and epigenetic memory},
  journal = {Genes \& Development},
  year    = {2002},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{jones2012,
  author  = {Jones, Peter A.},
  title   = {Functions of {DNA} methylation: islands, start sites, gene bodies and beyond},
  journal = {Nature Reviews Genetics},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{frommer1992,
  author  = {Frommer, Marianne and McDonald, Louise E. and Millar, Douglas S. and others},
  title   = {A genomic sequencing protocol that yields a positive display of 5-methylcytosine residues in individual {DNA} strands},
  journal = {Proceedings of the National Academy of Sciences (PNAS)},
  year    = {1992},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{lister2009,
  author  = {Lister, Ryan and Pelizzola, Mattia and Dowen, Robert H. and others},
  title   = {Human {DNA} methylomes at base resolution show widespread epigenomic differences},
  journal = {Nature},
  year    = {2009},
  note    = {STATUS: confident — verify author list/vol/pages/DOI}
}
@article{cokus2008,
  author  = {Cokus, Shawn J. and Feng, Suhua and Zhang, Xiaoyu and others},
  title   = {Shotgun bisulphite sequencing of the {Arabidopsis} genome reveals {DNA} methylation patterning},
  journal = {Nature},
  year    = {2008},
  note    = {STATUS: VERIFY — confirm this is the intended WGBS-origin cite; verify details}
}
```

## Alignment & pipelines (§2.2)

```bibtex
@article{krueger2011,
  author  = {Krueger, Felix and Andrews, Simon R.},
  title   = {Bismark: a flexible aligner and methylation caller for {Bisulfite-Seq} applications},
  journal = {Bioinformatics},
  year    = {2011},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ditommaso2017,
  author  = {Di Tommaso, Paolo and Chatzou, Maria and Floden, Evan W. and others},
  title   = {Nextflow enables reproducible computational workflows},
  journal = {Nature Biotechnology},
  year    = {2017},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{ewels2020,
  author  = {Ewels, Philip A. and Peltzer, Alexander and Fillinger, Sven and others},
  title   = {The {nf-core} framework for community-curated bioinformatics pipelines},
  journal = {Nature Biotechnology},
  year    = {2020},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
```

## Differential methylation (§2.3)

```bibtex
@article{akalin2012,
  author  = {Akalin, Altuna and Kormaksson, Matthias and Li, Sheng and others},
  title   = {methylKit: a comprehensive {R} package for the analysis of genome-wide {DNA} methylation profiles},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{feng2014,
  author  = {Feng, Hao and Conneely, Karen N. and Wu, Hao},
  title   = {A {Bayesian} hierarchical model to detect differentially methylated loci from single nucleotide resolution sequencing data},
  journal = {Nucleic Acids Research},
  year    = {2014},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{wu2015,
  author  = {Wu, Hao and Xu, Tianlei and Feng, Hao and others},
  title   = {Detection of differentially methylated regions from whole-genome bisulfite sequencing data without replicates},
  journal = {Nucleic Acids Research},
  year    = {2015},
  note    = {STATUS: VERIFY — confirm author list/vol/pages/DOI}
}
@article{park2016,
  author  = {Park, Yongseok and Wu, Hao},
  title   = {Differential methylation analysis for {BS-seq} data under general experimental design},
  journal = {Bioinformatics},
  year    = {2016},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{hansen2012,
  author  = {Hansen, Kasper D. and Langmead, Benjamin and Irizarry, Rafael A.},
  title   = {{BSmooth}: from whole genome bisulfite sequencing reads to differentially methylated regions},
  journal = {Genome Biology},
  year    = {2012},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{benjamini1995,
  author  = {Benjamini, Yoav and Hochberg, Yosef},
  title   = {Controlling the false discovery rate: a practical and powerful approach to multiple testing},
  journal = {Journal of the Royal Statistical Society: Series B},
  year    = {1995},
  note    = {STATUS: confident — verify vol/pages/DOI}
}
@article{robinson2014,
  author  = {Robinson, Mark D. and Kahraman, Abdullah and Law, Charity W. and others},
  title   = {Statistical methods for detecting differentially methylated loci and regions},
  journal = {Frontiers in Genetics},
  year    = {2014},
  note    = {STATUS: VERIFY — confirm venue/author list/details}
}
```

## LLMs, agents, tool use & MCP (§2.4)

```bibtex
@inproceedings{vaswani2017,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title     = {Attention is all you need},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2017},
  note      = {STATUS: confident — verify}
}
@inproceedings{brown2020,
  author    = {Brown, Tom B. and Mann, Benjamin and Ryder, Nick and others},
  title     = {Language models are few-shot learners},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@inproceedings{wei2022,
  author    = {Wei, Jason and Wang, Xuezhi and Schuurmans, Dale and others},
  title     = {Chain-of-thought prompting elicits reasoning in large language models},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2022},
  note      = {STATUS: confident — verify}
}
@inproceedings{yao2023,
  author    = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and others},
  title     = {{ReAct}: Synergizing reasoning and acting in language models},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{schick2023,
  author    = {Schick, Timo and Dwivedi-Yu, Jane and Dess{\`i}, Roberto and others},
  title     = {{Toolformer}: Language models can teach themselves to use tools},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023},
  note      = {STATUS: confident — verify}
}
@inproceedings{lewis2020,
  author    = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and others},
  title     = {Retrieval-augmented generation for knowledge-intensive {NLP} tasks},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2020},
  note      = {STATUS: confident — verify}
}
@misc{mcp2024,
  author       = {{Anthropic}},
  title        = {Introducing the {Model Context Protocol}},
  year         = {2024},
  howpublished = {\url{https://www.anthropic.com/news/model-context-protocol}},
  note         = {STATUS: VERIFY — confirm canonical citation/spec URL and access date}
}
```

## Agents for science & reliability (§2.5)

```bibtex
@article{boiko2023,
  author  = {Boiko, Daniil A. and MacKnight, Robert and Kline, Ben and Gomes, Gabe},
  title   = {Autonomous chemical research with large language models},
  journal = {Nature},
  year    = {2023},
  note    = {STATUS: VERIFY — (Coscientist) confirm author list/vol/pages/DOI}
}
@article{bran2024,
  author  = {M. Bran, Andres and Cox, Sam and Schilter, Oliver and others},
  title   = {Augmenting large language models with chemistry tools},
  journal = {Nature Machine Intelligence},
  year    = {2024},
  note    = {STATUS: VERIFY — (ChemCrow) confirm author list/year/vol/pages/DOI}
}
@misc{lu2024,
  author = {Lu, Chris and Lu, Cong and Lange, Robert Tjarko and others},
  title  = {The {AI} {Scientist}: Towards fully automated open-ended scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — (Sakana AI) confirm arXiv id/author list}
}
@article{ji2023,
  author  = {Ji, Ziwei and Lee, Nayeon and Frieske, Rita and others},
  title   = {Survey of hallucination in natural language generation},
  journal = {ACM Computing Surveys},
  year    = {2023},
  note    = {STATUS: VERIFY — confirm vol/pages/DOI}
}
@misc{scienceagentbench,
  author = {Chen, Ziru and others},
  title  = {{ScienceAgentBench}: Toward rigorous assessment of language agents for data-driven scientific discovery},
  year   = {2024},
  note   = {STATUS: VERIFY — confirm authors/arXiv id/year (referenced by the Mimosa benchmark suite)}
}
@misc{paperbench,
  author = {{OpenAI}},
  title  = {{PaperBench}: Evaluating {AI}'s ability to replicate {AI} research},
  year   = {2025},
  note   = {STATUS: VERIFY — confirm authors/canonical citation}
}
```

## The system under study

```bibtex
@article{legrand2026,
  author  = {Legrand, Martin and Jiang, Tao and Feraud, Matthieu and Navet, Benjamin
             and Taghzouti, Yousouf and Gandon, Fabien and Dumont, Elise and Nothias, Louis-F{\'e}lix},
  title   = {Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research},
  journal = {arXiv preprint arXiv:2603.28986},
  year    = {2026},
  note    = {STATUS: VERIFY — citation taken from the Mimosa README; confirm arXiv id once public}
}
```



# refs from Consensus

the csv = [the csv](D:\Akademi\14_Donem_MSc_Internship\%23Thesis\thesis_writing\references.csv)
also added this to zotero

I have analyzed your  references.csv  file and cross-referenced it with the topics outlined in your thesis ( OUTLINE.md ), specifically looking for relevance to your chapters on DNA methylation,
  bioinformatics pipelines, and LLM agents.

  Here is my verdict on the applicability of these papers to your thesis:

  ### 1. What's Missing: LLM & Agent Literature (Sections 2.4 & 2.5)

  The LLM that generated this CSV focused entirely on the biological and methodological side of your thesis. There are zero papers in this list related to LLMs, autonomous agents, or the Model Context
  Protocol (MCP). For Sections 2.4 and 2.5 of your Background chapter, you will need to do a separate literature search to find papers like ChemCrow, Coscientist, ScienceAgentBench, and Toolformer.

  ### 2. Highly Applicable: DNA Methylation & Bioinformatics (Sections 2.1 – 2.3)

  The CSV is a goldmine for the first half of your Background chapter and for justifying the design choices of your  Mimosa  agent. I found 57 papers that are relevant to your bioinformatics stack.

  Here are the most useful ones perfectly mapped to your thesis structure:

  #### For Section 2.2: Reads → Coverage (Bismark, Nextflow, pipelines)

  These papers are perfect for discussing mapping software, pipeline architectures, and reproducibility:

  • "Variable performance of widely used bisulfite sequencing methods and read mapping software for DNA methylation" (2025) — Very recent; explicitly discusses the performance of Bismark and how tool choice
  influences data reliability.
  • "Evaluation of preprocessing, mapping and postprocessing algorithms for analyzing whole genome bisulfite sequencing data" (2015) — Great for reviewing historical baseline comparisons of Bismark and WGBS
  pipelines.
  • "BiocMAP: a Bioconductor-friendly, GPU-accelerated pipeline for bisulfite-sequencing data" (2022) — Excellent for referencing modern, containerized pipeline orchestration (mentions Nextflow-like
  paradigms and reproducible workflows).
  • "Comparison of whole-genome bisulfite sequencing library preparation strategies identifies sources of biases affecting DNA methylation data" (2017) — Important for your theme of "reliability and
  reproducibility" in WGBS data.

  #### For Section 2.3: DMCs/DMRs & Two Engines (methylKit vs DSS)

  These papers cover the specific differential methylation engines you're using (Server B in your architecture):

  • "Detection of differentially methylated regions from whole-genome bisulfite sequencing data without replicates" (2015) — Directly focuses on DSS (Dispersion Shrinkage for Sequencing data), covering how
  it models overdispersion and spatial correlation for DMR detection.
  • "A Bayesian hierarchical model to detect differentially methylated loci from single nucleotide resolution sequencing data" (2014) — Another foundational paper detailing the statistical modeling behind
  DSS.
  • "Identification of Differentially Methylated Sites with Weak Methylation Effects" (2018) — Explicitly discusses the use of methylKit and compares statistical methodologies for finding biologically
  meaningful DMCs/DMRs.

  ### Summary Recommendation

  You can absolutely use this  references.csv  to heavily source Sections 2.1, 2.2, and 2.3 of your thesis. The papers provide strong evidence for why robust pipelines (like  nf-core/methylseq ) and
  reliable engines (like  methylKit / DSS ) are necessary—which perfectly sets up the "gap statement" for why an agent like  Mimosa  is needed to orchestrate them reliably.

  Would you like me to help you perform a web search to gather the missing LLM/Agent papers (e.g., Coscientist, Toolformer) to complete the bibliography for the second half of your Background chapter?





# **WGBS** Reviews and Methods for **NovaSeq** Methylation Analysis

For a literature search on **WGBS data analysis** from NovaSeq X or NovaSeq 6000, the most useful papers split into three facets: end-to-end analysis workflows, NovaSeq/platform-specific performance, and differential methylation and bias handling (Gong et al., 2022; Liu et al., 2024).

## Workflow Reviews

Several papers provide **step-by-step WGBS analysis workflows** from raw reads through DMR calling and interpretation (Gong et al., 2022; Stuart et al., 2024; Stuart et al., 2018).

- Gong et al. is a practical review covering library preparation, alignment, QC, and DMR detection with tool comparisons and code examples (Gong et al., 2022).
- Adusumalli et al. lays out the classic analysis chain: WGBS-specific QC, bisulfite-aware alignment, methylation scoring, heterogeneity assessment, annotation, visualization, and DMC/DMR testing (Adusumalli et al., 2015).
- Recent protocol papers also give end-to-end methods, including public bioinformatics workflows and reusable pipelines such as DMAP2 (Derbala et al., 2024; Stockwell et al., 2024).

## NovaSeq Performance

For **NovaSeq 6000-specific WGBS**, the evidence says platform choice affects duplication, coverage uniformity, and cost more than the core interpretability of methylation data (Zhou et al., 2019; Liu et al., 2024).

- In a systematic comparison, NovaSeq and HiSeq X showed little overall performance difference, except **higher duplication on NovaSeq** (Zhou et al., 2019).
- NovaSeq 6000 remained reproducible for WGBS and performed better than DNBSEQ-T7 for WGBS, especially in depth and GC-rich coverage uniformity (Liu et al., 2024).
- Earlier Illumina-platform work found WGBS libraries are low-diversity and that software versions can affect base quality, including known issues carried into NovaSeq comparisons (Raine et al., 2017).

## Bias and Differential Analysis

For **methylation calling and differential analysis**, the main message is that library protocol, amplification, replicate count, and depth all shape results, and no single DMR method dominates (Piao et al., 2021; Olova et al., 2017).

- Library preparation can change both absolute and relative methylation estimates, and amplification-free approaches are the least biased (Olova et al., 2017).
- Across DMR tools, **no single method** ranked first in all benchmarks, and few replicates cause more difficulty than low depth (Piao et al., 2021).
- Coverage planning remains central because WGBS cost-depth tradeoffs are still substantial, and formal recommendations exist for minimum depth versus replicate number (Ziller et al., 2014; Zhou et al., 2019).

## Key Papers

|Paper|Type|Why It Matters|Best Use|
|---|---|---|---|
|Gong 2022|Review/practical guide|Broad WGBS workflow and tool comparison|Start your search (Gong et al., 2022)|
|Stuart et al. 2024|Methods chapter|Step-by-step analysis and interpretation|Pipeline design (Stuart et al., 2024)|
|Zhou et al. 2019|Benchmarking study|Library prep plus NovaSeq vs HiSeq X|Platform decisions (Zhou et al., 2019)|
|Liu et al. 2024|Platform comparison|NovaSeq 6000 vs DNBSEQ-T7 for WGBS/RRBS|Sequencer evaluation (Liu et al., 2024)|
|Piao et al. 2021|DMR methods benchmark|Compares differential methylation methods|Statistical analysis choice (Piao et al., 2021)|

**Figure 1:** Recommended starting papers for WGBS data analysis literature search with emphasis on NovaSeq-relevant workflows, benchmarking, and differential methylation methods.

A focused search set for your project would start with the workflow reviews, then add NovaSeq benchmarking and DMR-method comparison papers, because **WGBS-specific methylation analysis** depends as much on platform and library bias as on the downstream software.

_These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at [https://consensus.app](https://consensus.app). © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent._

## References

Adusumalli, S., Omar, M. F. M., Soong, R., & Benoukraf, T. (2015). Methodological aspects of whole-genome bisulfite sequencing analysis. _Briefings in bioinformatics, 16 3_, 369-79. [https://doi.org/10.1093/bib/bbu016](https://doi.org/10.1093/bib/bbu016)

Derbala, D., Garnier, A., Bonnet, É., Deleuze, J., & Tost, J. (2024). Whole-Genome Bisulfite Sequencing Protocol for the Analysis of Genome-Wide DNA Methylation and Hydroxymethylation Patterns at Single-Nucleotide Resolution.. _Methods in molecular biology, 2842_, 353-382. [https://doi.org/10.1007/978-1-0716-4051-7_18](https://doi.org/10.1007/978-1-0716-4051-7_18)

Gong, T., Borgard, H., Zhang, Z., Chen, S., Gao, Z., & Deng, Y. (2022). Analysis and performance assessment of the whole genome bisulfite sequencing data workflow: currently available tools and a practical guide to advance DNA methylation studies. _Small methods, 6_, e2101251 - e2101251. [https://doi.org/10.1002/smtd.202101251](https://doi.org/10.1002/smtd.202101251)

Liu, X., Pang, Y., Shan, J., Wang, Y., Zheng, Y., Xue, Y., Zhou, X., Wang, W., Sun, Y., Yan, X., Shi, J., Wang, X., Gu, H., & Zhang, F. (2024). Beyond the base pairs: comparative genome-wide DNA methylation profiling across sequencing technologies. _Briefings in Bioinformatics, 25_. [https://doi.org/10.1093/bib/bbae440](https://doi.org/10.1093/bib/bbae440)

Olova, N. N., Krueger, F., Andrews, S., Oxley, D., Berrens, R. V., Branco, M., & Reik, W. (2017). Comparison of whole-genome bisulfite sequencing library preparation strategies identifies sources of biases affecting DNA methylation data. _Genome Biology, 19_. [https://doi.org/10.1186/s13059-018-1408-2](https://doi.org/10.1186/s13059-018-1408-2)

Piao, Y., Xu, W., Park, K., Ryu, K., & Xiang, R. (2021). Comprehensive Evaluation of Differential Methylation Analysis Methods for Bisulfite Sequencing Data. _International Journal of Environmental Research and Public Health, 18_. [https://doi.org/10.3390/ijerph18157975](https://doi.org/10.3390/ijerph18157975)

Raine, A., Liljedahl, U., & Nordlund, J. (2017). Data quality of whole genome bisulfite sequencing on Illumina platforms. _PLoS ONE, 13_. [https://doi.org/10.1371/journal.pone.0195972](https://doi.org/10.1371/journal.pone.0195972)

Stockwell, P., Rodger, E., Gimenez, G., Morison, I., & Chatterjee, A. (2024). DMAP2: A Pipeline for Analysis of Whole‐Genome‐Scale DNA Methylation Sequencing Data. _Current Protocols, 4_. [https://doi.org/10.1002/cpz1.70003](https://doi.org/10.1002/cpz1.70003)

Stuart, T., Buckberry, S., Nguyen, T., & Lister, R. (2024). Approaches for the Analysis and Interpretation of Whole-Genome Bisulfite Sequencing Data.. _Methods in molecular biology, 2842_, 391-403. [https://doi.org/10.1007/978-1-0716-4051-7_20](https://doi.org/10.1007/978-1-0716-4051-7_20)

Stuart, T., Buckberry, S., & Lister, R. (2018). Approaches for the Analysis and Interpretation of Whole Genome Bisulfite Sequencing Data.. _Methods in molecular biology, 1767_, 299-310. [https://doi.org/10.1007/978-1-4939-7774-1_17](https://doi.org/10.1007/978-1-4939-7774-1_17)

Zhou, L., Ng, H., Drautz-Moses, D. I., Schuster, S., Beck, S., Kim, C., Chambers, J., & Loh, M. (2019). Systematic evaluation of library preparation methods and sequencing platforms for high-throughput whole genome bisulfite sequencing. _Scientific Reports, 9_. [https://doi.org/10.1038/s41598-019-46875-5](https://doi.org/10.1038/s41598-019-46875-5)

Ziller, M. J., Hansen, K. D., Meissner, A., & Aryee, M. J. (2014). Coverage recommendations for methylation analysis by whole genome bisulfite sequencing. _Nature methods, 12_, 230 - 232. [https://doi.org/10.1038/nmeth.3152](https://doi.org/10.1038/nmeth.3152)


# Papers for **WGBS** Processing and **DMR** Analysis

For your literature search, the two main facets are **raw-data processing through methylation calling** and **statistical analysis with QC, DMC/DMR calling, and annotation**.

## Processing and Calling

These papers cover the front half of a WGBS workflow: pre-alignment QC, trimming, bisulfite-aware alignment, post-alignment checks, and methylation calling. Reviews and protocol papers are best for building your pipeline, while benchmarking papers help choose aligners and platform-specific settings.

- Gong 2022 is the clearest **workflow review**, laying out pre-alignment QC, trimming, bisulfite-aware alignment, post-alignment QC, M-bias inspection, methylation calling, and downstream annotation (Gong et al., 2022).
- DMAP2 2024 gives a practical **end-to-end protocol** with genome prep, adapter trimming, Bismark or bsmapz mapping, BAM output, and downstream scripts (Stockwell et al., 2024).
- CpG_Me in a NovaSeq-6000 comparison used Trim Galore, Bismark, Bowtie2, SAMtools, and MultiQC, with trimming for adapters and end bias before CpG count generation (Liu et al., 2024).

## QC and Benchmarking

QC papers matter because WGBS results shift with library prep, trimming, mapper choice, depth, and platform. Several studies show that technical bias can materially alter methylation estimates.

- Library protocol can create **purely technical methylation differences** of up to 20%, and Olova 2017 added Bismark’s bam2nuc QC module to diagnose bias (Olova et al., 2017).
- Benchmarking on novel and Illumina platforms found trimming improved mapping efficiency, and PBAT-style libraries often needed end trimming because of low-quality read segments (Lin et al., 2023).
- A 192-combination evaluation found Mott trimming or quality filtering each improved mapping and methylation estimation, while paired-end sequencing improved sensitivity and reduced errors (Tsuji & Weng, 2015).

## Statistical Analysis

These papers cover DMC/DMR identification, statistical modeling, and region-level inference. The field does not have one universally best caller, so method choice should match replicate structure, coverage, and study design.

- Alignment choice can change the number and methylation levels of called CpGs, DMCs, DMRs, related genes, and pathway results (Gong et al., 2022).
- DMRcate 2021 benchmarked genome-wide methods and found **DMRcate and RADmeth** were the best DMR predictors, with DMRcate the fastest (Peters et al., 2021).
- DSS-single 2015 is specifically useful when you have **no biological replicates**, modeling spatial correlation, depth, and biological variation for Wald-test DMR detection (Wu et al., 2015).

## Suggested Starting Set

|Paper|Best Role|Why Start Here|
|---|---|---|
|Gong 2022|Review|Broad WGBS workflow and tool guide (Gong et al., 2022)|
|Tsuji & Weng 2015|Benchmark|Preprocessing, mapping, postprocessing comparison (Tsuji & Weng, 2015)|
|Olova 2017|QC/bias|Library-prep bias and bam2nuc QC (Olova et al., 2017)|
|DMAP2 2024|Protocol|Practical pipeline from trimming to differential analysis (Stockwell et al., 2024)|
|Peters 2021|DMR methods|DMR caller benchmarking and DMRcate (Peters et al., 2021)|

**Figure 1:** Recommended starter papers for WGBS literature search across preprocessing, QC, methylation calling, and differential methylation analysis.

If your project is specifically **NovaSeq X or NovaSeq 6000 WGBS**, start with Gong 2022 for workflow, then add NovaSeq benchmarking and QC papers, and then move to DMRcate, DSS, or related DMR-method papers for the downstream statistics.

_These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at [https://consensus.app](https://consensus.app). © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent._

## References

Gong, T., Borgard, H., Zhang, Z., Chen, S., Gao, Z., & Deng, Y. (2022). Analysis and performance assessment of the whole genome bisulfite sequencing data workflow: currently available tools and a practical guide to advance DNA methylation studies. _Small methods, 6_, e2101251 - e2101251. [https://doi.org/10.1002/smtd.202101251](https://doi.org/10.1002/smtd.202101251)

Gong, W., Pan, X., Xu, D., Ji, G., Wang, Y., Tian, Y., Cai, J., Li, J., Zhang, Z., & Yuan, X. (2022). Benchmarking DNA methylation analysis of 14 alignment algorithms for whole genome bisulfite sequencing in mammals. _Computational and Structural Biotechnology Journal, 20_, 4704 - 4716. [https://doi.org/10.1016/j.csbj.2022.08.051](https://doi.org/10.1016/j.csbj.2022.08.051)

Lin, Q.-T., Yang, W., Zhang, X., Li, Q.-G., Liu, Y.-F., Yan, Q., & Sun, L. (2023). Systematic and benchmarking studies of pipelines for mammal WGBS data in the novel NGS platform. _BMC Bioinformatics, 24_. [https://doi.org/10.1186/s12859-023-05163-w](https://doi.org/10.1186/s12859-023-05163-w)

Liu, X., Pang, Y., Shan, J., Wang, Y., Zheng, Y., Xue, Y., Zhou, X., Wang, W., Sun, Y., Yan, X., Shi, J., Wang, X., Gu, H., & Zhang, F. (2024). Beyond the base pairs: comparative genome-wide DNA methylation profiling across sequencing technologies. _Briefings in Bioinformatics, 25_. [https://doi.org/10.1093/bib/bbae440](https://doi.org/10.1093/bib/bbae440)

Olova, N. N., Krueger, F., Andrews, S., Oxley, D., Berrens, R. V., Branco, M., & Reik, W. (2017). Comparison of whole-genome bisulfite sequencing library preparation strategies identifies sources of biases affecting DNA methylation data. _Genome Biology, 19_. [https://doi.org/10.1186/s13059-018-1408-2](https://doi.org/10.1186/s13059-018-1408-2)

Peters, T. J., Buckley, M., Chen, Y., Smyth, G., Goodnow, C., & Clark, S. (2021). Calling differentially methylated regions from whole genome bisulphite sequencing with DMRcate. _Nucleic Acids Research, 49_, e109 - e109. [https://doi.org/10.1093/nar/gkab637](https://doi.org/10.1093/nar/gkab637)

Stockwell, P., Rodger, E., Gimenez, G., Morison, I., & Chatterjee, A. (2024). DMAP2: A Pipeline for Analysis of Whole‐Genome‐Scale DNA Methylation Sequencing Data. _Current Protocols, 4_. [https://doi.org/10.1002/cpz1.70003](https://doi.org/10.1002/cpz1.70003)

Tsuji, J., & Weng, Z. (2015). Evaluation of preprocessing, mapping and postprocessing algorithms for analyzing whole genome bisulfite sequencing data. _Briefings in bioinformatics, 17 6_, 938-952. [https://doi.org/10.1093/bib/bbv103](https://doi.org/10.1093/bib/bbv103)

Wu, H., Xu, T., Feng, H., Chen, L., Li, B., Yao, B., Qin, Z. S., Jin, P., & Conneely, K. (2015). Detection of differentially methylated regions from whole-genome bisulfite sequencing data without replicates. _Nucleic Acids Research, 43_, e141 - e141. [https://doi.org/10.1093/nar/gkv715](https://doi.org/10.1093/nar/gkv715)



