# 01_introduction

# Chapter 1 — Introduction

## 1.1 Introduction

DNA methylation is one of the most extensively characterised epigenetic marks. It regulates gene expression, underlies genomic imprinting and X-chromosome inactivation, and its dysregulation is a hallmark of cancer and other diseases [3]. Whole-genome bisulfite sequencing (WGBS) measures this mark at single-base resolution across the entire genome and is widely regarded as the gold-standard assay for the mark [2, 3]. Because both the underlying biology and the assay itself are so well studied, the downstream computational analysis — quality control, alignment of bisulfite-converted reads, methylation calling, differential testing, and region calling — is correspondingly mature, having been the subject of dozens of competing statistical methods, multiple published benchmarking studies, and well-documented failure modes [2, 5, 6]. Differential methylation analysis is therefore a domain in which the properties an automated analysis system should ideally exhibit — results that are concordant with established findings, consistent across repeated runs and across experimental designs, and transparent about their own errors — can be assessed against a substantial existing body of reference results, rather than merely asserted.

At the same time, large language models (LLMs) capable of planning multi-step analyses and generating executable code have increasingly been applied across computational biology. Autonomous Scientific Research (ASR) frameworks now propose, execute, and iteratively refine multi-step analyses from little more than a stated objective and a set of available tools [1, 9, 10]. Recent surveys identify dozens of such systems in genomics and bioinformatics alone: single-agent tools that plan and execute an entire omics analysis from a data path and a stated goal [11], and multi-agent systems that distribute planning, coding, and quality control across specialised roles [9]. None of the systems catalogued in the most recent surveys of agentic bioinformatics targets differential-methylation calling from WGBS data specifically, and the handful of existing AI applications to DNA methylation are supervised predictors of methylation state rather than autonomous agents that plan and execute an analysis pipeline end to end [12].

This thesis addresses that gap by adapting **Mimosa** [1] — an evolving multi-agent framework for autonomous scientific research, originally developed and benchmarked on data-driven discovery tasks spanning bioinformatics, computational chemistry, geographic information science, and psychology — to the problem of differential methylation analysis from WGBS data. The aim is not simply to establish that such a system can produce a plausible-looking output, but to evaluate it against the standards a working <mark style="background: #D2B3FFA6;">epigenomicist</mark> would apply in practice: whether its results are concordant with established, expert-run analyses of the same data, whether they are consistent across repeated runs and across different organisms and experimental designs, and whether its errors, when they occur, are legible to a human reviewer rather than concealed behind fluent narrative output.

## 1.2 Problem Statement

This work is motivated by two distinct problems. The first is a problem *within* differential-methylation analysis itself, independent of any AI system: differential methylation analysis is a domain in which "correct" is already a statistical, not an absolute, notion. Independent benchmarking studies have shown that established, expert-run tools can disagree substantially even on the same dataset, so evaluating an automated system has to be built around concordance with a defensible range of outcomes rather than a single ground truth.

The second problem is specific to autonomous agents. LLM agents are non-deterministic; they fail in fluent and confident ways; and they can report success on results that do not survive inspection. For a clinically-adjacent assay such as WGBS methylation — where a hyper- or hypo-methylated region may be read as a candidate biomarker or a diagnostic indicator — a plausible wrong answer is worse than an obvious one. The decisive quantities a practitioner would need before trusting such a tool — concordance with published findings, cross-species consistency, and full-pipeline capability from raw sequencing reads — have not, to our knowledge, been reported for an LLM agent performing methylation analysis. Existing AI applications to DNA methylation are, overwhelmingly, supervised predictors of methylation state trained on sequence or array features; none targets autonomous, end-to-end differential-methylation calling from WGBS data, and the small number of general-purpose agentic-bioinformatics systems that do plan and execute whole analyses have not been evaluated against this domain's specific demands — biological-replicate structure, coverage heterogeneity, and a genuine plurality of legitimate statistical approaches.

Tool-using LLM agents have, within a very short span, moved from research demonstrations to systems that conduct chemical and computational research with minimal human intervention [@boiko2023; @bran2024]. The recent standardisation of agent–tool interfaces through the Model Context Protocol [@anthropic2024mcp] has made it routine to connect an agent to real scientific software, and the attraction for biology and medicine is immediate: methylation and other omics analyses demand specialised statistical and computational expertise that most clinicians and many researchers lack, and a conversational agent promises to make that analysis accessible through ordinary language. The same properties that make these systems attractive, however, make them dangerous in a scientific setting, which is precisely why supplying the quantities a practitioner would need — in a domain whose correct answers are knowable even if not unique — is a timely contribution.

## 1.3 Research Questions

The work is organised around a single, falsifiable hypothesis rather than a set of open questions:

> A tool-augmented large language multi-model agent, constrained by a domain-specific skill and typed Model Context Protocol tool servers, can autonomously execute whole-genome bisulfite sequencing differential methylation analyses — replicating published findings across organisms and executing the complete reads-to-results pipeline — with results concordant with expert-conducted analyses.

Each experiment produces a quantitative concordance or capability measure that either supports the hypothesis or does not, and no measure is discarded after the fact because it is inconvenient. A negative or qualified result — for example, that reliability requires the domain skill and bounded autonomy, or that concordance is adequate for gene-level findings but not for individual CpG sites — would itself be a scientifically informative outcome rather than a failure. Three sub-questions structure how the hypothesis is tested:

- **Can the system be specified precisely enough to be measured?** — its architecture, its two MCP tool servers, its domain skill, its agent loop and goal specification, and its reliability guardrails (Chapter 3).
- **Does Mimosa replicate published findings, and does it do so consistently across organisms?** — tested by driving Mimosa, and matched expert-run baselines, over the identical data of two peer-reviewed studies, a human AKAP11 knockout study (GSE263850) and a mouse Dnmt3a conditional knockout study (GSE214232), with concordance scored as a triangle: Mimosa versus published results, Mimosa versus expert re-analysis, and expert versus published (Chapters 4 and 5).
- **Can Mimosa execute the complete reads-to-results pipeline, not just downstream analysis?** — tested from simulated FASTQ files through bisulfite alignment to differentially methylated region (DMR) calling, exercising the complete path that the real-data experiments, by necessity, begin downstream of alignment (Chapter 6).
- **How stable are Mimosa's analytical conclusions** — the workflow topology it designs, the tools it selects, and the regions it calls — across repeated runs on identical inputs, across different organisms and experimental designs, and across different underlying execution models? <mark style="background: #FF5582A6;">Chapter ???</mark>
- **Do Mimosa's execution traces, judge justifications, and archived workflow graphs make Mimosa's errors legible to a human reviewer with domain expertise** — that is, can a methylation biologist inspect a failed or questionable run and identify *why* it failed, rather than being presented only with a plausible-looking final report? <mark style="background: #FF5582A6;">Bu da each run karşılaştırılarak yapılabilir veya run23 sonucu hatalı sunulur sonra sign flip yapılır ve aynı/iyi sonuçlar gözükür burda da hata yapsa bile reviewable ve chanable değişiklikler yapılabilir falan
</mark>


## 1.4 Objectives and Contributions

In pursuit of these questions, the work makes the following contributions:

1. **A WGBS-Mimosa integration.** An extension of Mimosa's tool-discovery layer with a set of containerised MCP servers exposing the standard WGBS analysis toolchain — quality control and adapter trimming, bisulfite-aware read alignment and methylation extraction, differential testing and DMR calling using more than one statistical family, and functional annotation — so that the meta-orchestrator can allocate them to agents exactly as it does with the generic tools evaluated in the original Mimosa paper
2. **A triangulated concordance evaluation.** Scoring Mimosa against both a published study and an independent expert re-analysis of the identical data, using the expert-versus-published agreement as the realistic ceiling for what any re-analysis can achieve. The triangulation is deliberate rather than a convenience: because established, expert-run methods can legitimately disagree with one another and with a re-analysed publication, scoring Mimosa against a single reference point would risk mistaking ordinary methodological variation for agent error, or the reverse.
3. **A cross-species generalisation test.** The same evaluation framework applied to a second organism (mouse, after human), asking whether Mimosa's reliability is a property of the system rather than an artefact of a single dataset.
4. **A full-pipeline end-to-end demonstration.** Simulated FASTQ files with known properties, processed through the complete reads-to-results path — bisulfite alignment via nf-core/methylseq, coverage extraction, and DMR calling — verifying that the full pipeline executes correctly and that the system is not limited to analysis from pre-computed coverage files.


An explicit honesty boundary governs all three experiments. The real-data validation in Experiments 1 and 2 begins at the coverage-file stage: the available compute environment (a single workstation, no cloud infrastructure) made full alignment of production-scale WGBS reads infeasible. The complete reads-to-coverage path is therefore exercised only at simulated scale in Experiment 3. This boundary is stated wherever it bears on a claim, not relegated to a limitations note. Concordance itself is assessed on gene recovery, direction of effect, and qualitative methylation signature rather than on raw count identity, since several defensible statistical methods yield legitimately different counts.

## 1.5 Overview of the Proposed System

Given WGBS data and a natural-language goal, the system synthesises and executes a complete differential-methylation pipeline — quality control, differential testing, region calling, annotation — by writing analysis code and invoking domain tools rather than by following a fixed script. It does so through Mimosa's agent loop, driven by a domain-specific methylation skill and typed MCP tool servers rather than a generic, undirected toolset: a Nextflow-based alignment server and a Dockerised R analysis server, described in full in Chapter 3.

The four sources drawn on to specify and evaluate this system are of distinct kinds. The *primary data* are public: coverage files and supplementary result tables of the two peer-reviewed WGBS studies, GSE263850 [@gse263850] and GSE214232 [@gse214232], obtained from the Gene Expression Omnibus (GEO), together with simulated FASTQ data generated <mark style="background: #FF5582A6;">BY SHERMANN</mark> with controlled parameters for Experiment 3. The *methodological literature* comprises the established science of bisulfite sequencing and differential-methylation analysis — a domain with decades of method development but, notably, no consensus statistical model for detecting differentially methylated cytosines or regions, spanning logistic-regression, smoothing, beta-binomial, hidden-Markov-model, entropy-based, and segmentation-based families, each with different assumptions about biological replication, spatial correlation between neighbouring CpG sites, and sequencing coverage — with methylKit [@akalin2012] and DSS [@park2016; @wu2015] as the principal statistical engines, the Bismark aligner [@krueger2011], and the nf-core/methylseq pipeline [@ewels2020]. The *system under study* is documented from its own source code and from the laboratory's framework description [@legrand2026]. The *agent and protocol literature* — LLM tool use, MCP, autonomous agents for science, and the reliability of such systems — is drawn from primary sources and, being recent and fast-moving, is treated with an explicit knowledge-cutoff caveat and was re-verified at the time of writing.

## 1.6 Thesis Structure

The chapters that follow are organised as follows.

**Chapter 2 (Background & Related Work)** introduces the two literatures joined here — WGBS DNA methylation and its statistics on one side, LLM agents and the Model Context Protocol on the other — and states the gap between them.

**Chapter 3 (System Design & Methods)** specifies the system under test: its four-layer architecture, the two MCP tool servers, the methylation skill that encodes domain knowledge, the Mimosa framework and its goal evolution, and the reliability engineering that underpins Section 1.4's contributions.

**Chapter 4 (Experiment 1: Replication — GSE263850)** presents the replication of a human AKAP11 knockout WGBS study, scored as a concordance triangle against both the published findings and an expert re-analysis.

**Chapter 5 (Experiment 2: Replication — GSE214232)** presents the replication of a mouse Dnmt3a conditional knockout study using the same triangulated evaluation, testing cross-species generalisation.

**Chapter 6 (Experiment 3: End-to-End — Simulated FASTQ)** demonstrates full-pipeline capability from simulated raw reads through alignment to DMR calling, exercising the reads-to-results path the real-data experiments cannot.

**Chapter 7 (Discussion)** returns to the hypothesis, synthesises findings across the three experiments, weighs strengths against honest limitations, and considers threats to validity.

**Chapter 8 (Conclusions & Future Work)** states the contributions, draws the honest scope boundary, and develops the multi-omics extension roadmap for which methylation is the validated first vertical.

A **Bibliography** and **Annexes** — including the methylation skill specification, MCP tool catalogues, representative agent transcripts, and supplementary result tables — close the document.

What is new in this approach, taken as a whole, is evaluating Mimosa not by capability demonstrations — the dominant mode in the agents-for-science literature, where success is shown once and failure is omitted — but by measurement against knowable truth, in a domain chosen precisely because its correct answers, while not unique, are at least bounded and checkable. Treating methylation as a fully validated vertical rather than an isolated demonstration, and building its claims on shared scoring infrastructure that other omics domains can adopt, yields both specific empirical results and an honest template for how tool-augmented LLMs might be validated, domain by domain, before they are trusted in scientific practice.


## References

*(Numbering matches the bracketed citations above; format to your department's required style before submission.)*

1. Legrand, M., Jiang, T., Feraud, M., Navet, B., Taghzouti, Y., Gandon, F., Dumont, E., & Nothias, L.-F. (2026). *Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research*. arXiv:2603.28986 [cs.AI].
2. Shafi, A., Mitrea, C., Nguyen, T., & Draghici, S. (2018). A survey of the approaches for identifying differential methylation using bisulfite sequencing data. *Briefings in Bioinformatics*, 19(5), 737–753. https://doi.org/10.1093/bib/bbx013
3. Dolzhenko, E., & Smith, A. D. [tool: RADMeth] Using beta-binomial regression for high-precision differential methylation analysis in multifactor whole-genome bisulfite sequencing experiments. *BMC Bioinformatics*, 15, 215 (2014). *(verify authorship before citing — retrieved via secondary source; check primary record.)*
4. Benchmarking edgeR and methylKit for the Detection of Differential DNA Methylation: A Methodological Evaluation. *International Journal of Molecular Sciences*, 27(4), 1964 (2026). https://doi.org/10.3390/ijms27041964
5. Calling differentially methylated regions from whole genome bisulphite sequencing with DMRcate. *Nucleic Acids Research*, 49(19), e109 (2021).
6. FAIRification of the DMRichR pipeline: advancing epigenetic research on environmental and evolutionary model organisms. *Bioinformatics Advances*, 5(1), vbaf024 (2025).
7. A comprehensive evaluation of computational tools to identify differential methylation regions using RRBS data. *Genomics* (2020). https://doi.org/10.1016/j.ygeno.2020.07.032
8. Integrative Epigenomics: Bioinformatics (preprint review). *Preprints.org* (2026).
9. Zhou, J., Jiang, J., Han, Z., Wang, Z., & Gao, X. (2025). Streamline automated biomedical discoveries with agentic bioinformatics. *Briefings in Bioinformatics*, 26(5), bbaf505. https://doi.org/10.1093/bib/bbaf505
10. Huang, S., Lang, M., Chen, Z., Yang, C., Huang, X., et al. (2026). From foundation models to autonomous agents in biology. *Genomics Communications*, 3, e006. https://doi.org/10.48130/gcomm-0026-0005
11. Zhou, J., Zhang, B., Li, G., et al. (2024). An AI agent for fully automated multi-omic analyses. *Advanced Science*, 11, e2407094. https://doi.org/10.1002/advs.202407094
12. Artificial intelligence for comprehensive DNA methylation analysis: overview, challenges, and future directions. *Briefings in Bioinformatics*, 26(5), bbaf468 (2025).
13. Wratten, L., Wilm, A., & Göke, J. (2021). Reproducible, scalable, and shareable analysis pipelines with bioinformatics workflow managers. *Nature Methods*, 18, 1161–1168. https://doi.org/10.1038/s41592-021-01254-9
14. ARPEGGIO: Automated Reproducible Polyploid EpiGenetic GuIdance workflOw. *bioRxiv* 2020.07.16.206193 (2020).
15. FAIRification of the DMRichR pipeline [see also ref. 6].
16. Chen, Z., Chen, S., Ning, Y., Zhang, Q., Wang, B., Yu, B., Li, Y., Liao, Z., Wei, C., Lu, Z., Dey, V., Xue, M., Baker, F. N., Burns, B., Adu-Ampratwum, D., Huang, X., Ning, X., Gao, S., Su, Y., & Sun, H. (2025). ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery. *arXiv preprint*.
17. Mitchener, L., Laurent, J. M., Tenmann, B., Narayanan, S., Wellawatte, G. P., White, A., Sani, L., & Rodriques, S. G. (2025). BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology. *arXiv preprint* arXiv:2503.00096.

*Notes for revision: (i) reference 3 needs its primary bibliographic record confirmed directly (author list was not fully visible in the source used during drafting); (ii) references 5, 6, 7, 8, and 12 are given with journal/volume/year only because author bylines were not captured during drafting — pull the full author lists from the DOIs before your bibliography is finalised; (iii) references 16–17 are reproduced from Mimosa's own bibliography and should be independently verified against arXiv/publisher records; (iv) consider whether your department wants numeric (Vancouver/IEEE) or author–date (APA/Harvard) style — this draft uses numeric throughout for consistency with the Mimosa paper, but bioinformatics theses often expect author–date.*

---

# 02_background

# Chapter 2 — Background & Related Work

## 2.1 DNA Methylation and Whole-Genome Bisulfite Sequencing

DNA methylation is the covalent addition of a methyl group to the 5-carbon of cytosine, producing 5-methylcytosine (5mC). In vertebrates it occurs predominantly at cytosine–guanine dinucleotides (CpG sites); although only a small fraction of genomic cytosines are methylated overall, CpG sites are methylated the large majority of the time [2]. Methylation at gene promoters is generally repressive: a methylated CpG site restricts the binding of transcription factors, whereas an unmethylated site permits it, so methylation state is tightly linked to transcriptional regulation, cellular differentiation, genomic imprinting, and X-chromosome inactivation [2, 3]. Aberrant methylation — hypermethylation of tumour-suppressor promoters, hypomethylation of oncogenes — is a well-established feature of cancer, which is part of why differential-methylation analysis is clinically as well as biologically motivated [2, 3].

Whole-genome bisulfite sequencing measures methylation at single-base resolution across an entire genome by exploiting a simple chemical asymmetry: treatment with sodium bisulfite deaminates unmethylated cytosines to uracil, which is read as thymine during sequencing, while methylated cytosines are left unconverted and continue to read as cytosine [2, 3]. Comparing the resulting sequence to an unconverted reference therefore recovers, at each covered CpG site, an estimated methylation level as the ratio of reads retaining a cytosine call to total reads at that site. Because bisulfite conversion introduces a large and systematic mismatch between reads and the reference genome, standard aligners perform poorly on unconverted references; dedicated bisulfite aligners such as Bismark instead align reads against *in-silico* converted versions of the genome (or use "wildcard" aligners that treat unconverted cytosines specially) before recovering per-site methylation calls [2]. A typical WGBS analysis therefore proceeds through six broadly agreed stages: raw-read quality control and adapter trimming; bisulfite-aware alignment to a reference genome; post-alignment quality assessment; per-cytosine methylation extraction; differential methylation testing at the level of individual cytosines and/or aggregated regions; and, finally, annotation of the resulting regions against gene models and regulatory features [2].


WGBS is the most comprehensive methylation assay but not the only one: reduced-representation bisulfite sequencing (RRBS) enriches for CpG-dense regions at lower cost, and methylation microarrays (the Illumina 450K and EPIC platforms) interrogate a fixed panel of pre-selected CpGs. These trade genome-wide coverage for cost or convenience. The experiments of this thesis use WGBS coverage data.



## 2.3 The Differential Methylation Analysis Pipeline

The step that this thesis is centrally concerned with — identifying differentially methylated cytosines (DMCs) and differentially methylated regions (DMRs) between two or more biological conditions — is also the step with the least methodological consensus. A 2018 survey classified twenty-two published approaches into seven conceptual families: logistic-regression methods such as methylKit, which models methylation proportions directly and can operate with or without biological replicates; smoothing-based methods such as BSmooth and BiSeq, which borrow statistical strength from neighbouring CpG sites to reduce required coverage; beta-binomial methods such as DSS, MOABS, and RADMeth, which jointly model sampling variability (via a binomial term) and biological variability across replicates (via a beta term); hidden-Markov-model approaches; Shannon-entropy-based approaches; approaches built on classical hypothesis tests (Fisher's exact test, ANOVA) applied within fixed or variable genomic windows; and binary-segmentation approaches such as metilene [2]. Each family makes different trade-offs among considering biological replication, spatial correlation between neighbouring sites, sequencing coverage, additional covariates, and the ability to call *de novo* regions rather than only testing predefined ones, and — critically — no single method dominates the others across all of these axes [2].

This is not a purely theoretical concern. A benchmarking study comparing seven DMR-calling tools under simulated data found that method ranking by predictive accuracy changed with sequencing depth and with the magnitude of the underlying methylation difference, with some tools performing well only when differences were large and coverage was high [7]. A more recent benchmarking effort introduced an additional tool, DMRcate, and compared it against three established competitors on realistic simulations, again reporting meaningful differences in sensitivity and false-discovery control across methods rather than convergence on a single best approach [5]. Perhaps most directly relevant to the "trustworthiness" question this thesis is built around, a 2026 study applying two long-established, actively maintained pipelines (edgeR- and methylKit-based) to the *same* WGBS dataset found only around 56% concordance between the two tools at the level of individual differentially methylated cytosines, rising to roughly 90% once results were aggregated to genes — a useful reminder that even without any AI system in the loop, the choice of statistical pipeline materially shapes reported findings, and that per-cytosine and gene-level agreement can diverge substantially [4]. Reviews of newer, actively maintained pipelines make the same point explicitly: with methods available ranging from simple hypothesis tests to Bayesian smoothing frameworks, none has been shown to consistently outperform the others across benchmarks [6].

This body of work matters for the present thesis in two ways. First, it means that "the agent got the wrong answer" is frequently not a well-formed statement for WGBS differential-methylation analysis — the more honest question is whether the agent's answer falls within the range that domain-appropriate methods would themselves produce, and whether the agent can justify the specific choices (test family, replicate handling, coverage filtering) that led to its particular answer. Second, it directly motivates the evaluation strategy adopted later in this thesis: rather than scoring an agent purely against a single "gold" DMR set, Chapter 3 defines concordance relative to a small ensemble of established pipelines and, where available, the region set reported in the dataset's original publication, so that an agent's output can be judged for falling within (or outside) the envelope of results that a competent human analyst would consider defensible.

---

## 2.3.2 Tool Multiplicity and the Reliability Problem in Epigenomics
- [ ] başlık numaralarını güncelle/finalize task 🔼 📅 2026-08-10

The lack of statistical consensus described above sits inside a broader reproducibility problem that affects computational epigenomics as a discipline. Bioinformatics pipelines are long chains of interdependent tools and parameter choices, and errors or biases introduced early — in quality trimming, in alignment, in normalisation — propagate through every downstream step; different normalisation and peak- or region-calling strategies applied to the same raw epigenomic data can therefore yield materially different biological interpretations even when every individual tool is used correctly [8]. This is compounded by the short half-life of bioinformatics software, incomplete documentation of workflow parameters, and inconsistent reporting practices, all of which are recognised contributors to a wider reproducibility crisis across computational biology [8]. Workflow-management systems such as Snakemake and Nextflow, and specialised reproducible WGBS pipelines such as ARPEGGIO for polyploid methylome comparisons or the FAIR-oriented DMRichR pipeline, have been developed precisely to fix a workflow's tools, versions, and parameters so that an analysis can be re-executed identically by a different investigator [13, 14, 15]. These systems solve reproducibility in the narrow, mechanical sense of *re-executability*: given the same pipeline definition and the same data, the same numbers come out. They do not, and are not designed to, resolve the deeper methodological disagreement described in Section 2.2 — a perfectly reproducible pipeline can still be reproducibly using a statistical model poorly suited to a given experimental design.

This distinction — reproducibility of *execution* versus reliability of *method choice* — is central to how this thesis frames the risk and the opportunity posed by an autonomous agent. A rigid, version-pinned pipeline is reproducible but cannot adapt its method choice to an experimental design it was not built for (small sample sizes without replicates, unusual coverage profiles, non-CpG methylation contexts relevant to plant genomes). An agent that can read the structure of the input data and select, justify, and if necessary revise its statistical approach could in principle improve on this — but only if that flexibility does not come at the cost of the very reproducibility that fixed pipelines were built to guarantee. Measuring both properties at once, for the same system, is one of the central methodological aims of this thesis.

---

## 2.4 From Static Pipelines to Agentic Science

Large language models capable of planning multi-step actions and executing code have given rise to a distinct research direction generally termed autonomous scientific research (ASR) or, within computational biology specifically, "agentic bioinformatics" [1, 9, 10]. The common thread across this literature is a move away from software that executes a single, human-specified pipeline and toward software that is given a high-level objective and a set of available tools, and that plans, executes, evaluates, and — in the more advanced systems — revises its own strategy.

Early and still widely used systems in this space are single-agent: a standalone LLM-driven agent equipped with a broad tool set handles an entire analysis. AutoBA, for example, requires only a data path, a short data description, and a stated objective, and then autonomously proposes and executes a multi-omics analysis plan, including a self-repair mechanism for failed code [11]. Comparable single-agent tools have been built for single-cell RNA-seq analysis, biomarker discovery, and enzyme engineering, generally by pairing an LLM with a curated set of callable APIs or command-line tools [9, 10]. These systems establish that natural-language-driven, code-generating automation is feasible for real bioinformatics workloads, but recent surveys note recurring limitations: brittle handling of ambiguous instructions, heavy dependence on the quality of third-party tool documentation, inconsistent tool choices for ostensibly identical queries, and a persistent need for manual correction when the agent's single reasoning trajectory commits early to an unproductive analysis strategy [9].

Multi-agent systems attempt to address this by distributing a task across specialised roles — a planner, one or more executor agents, and an evaluator or "critic" agent that checks outputs before they are accepted — an approach reported to improve robustness on tasks such as single-cell RNA-seq analysis (CellAgent), general bioinformatics pipelines with a dedicated debugging role (BioMaster), and protein design (ProtAgents) [9]. The Virtual Lab extends this pattern with an explicit human-in-the-loop principal-investigator agent coordinating a team of specialist agents, and reports a substantial real-world validation (engineered nanobody binders against SARS-CoV-2 variants), while also documenting that the system requires repeated human-guided refinement and is sensitive to prompt ambiguity [9]. Across this literature, a broadly shared conclusion is that specialisation into multiple roles improves handling of complex, multi-step tasks relative to single agents, but that fixed, hand-designed coordination structures still struggle when a task's requirements deviate from what the designer anticipated [1, 9] — precisely the architectural rigidity that motivates *evolving* multi-agent frameworks such as Mimosa (Section 2.5).

Notably absent from this landscape, as far as the present survey of the literature has established, is any agentic system purpose-built for — or systematically evaluated on — differential methylation analysis from WGBS data specifically. Existing AI applications to DNA methylation are overwhelmingly supervised prediction models: deep-learning and machine-learning classifiers trained to predict methylation status, CpG-island behaviour, or disease association from sequence or array features, rather than autonomous agents that plan and execute an analysis pipeline end to end [12]. This absence is one of the concrete gaps this thesis addresses.

---
## 2.5 The Mimosa Framework

Mimosa is an open-source, evolving multi-agent framework for autonomous scientific research introduced by Legrand, Jiang, and colleagues, designed to address two limitations the authors identify in prior ASR systems: degraded long-horizon reasoning as LLM context accumulates ("semantic drift"), and the architectural rigidity of fixed multi-agent coordination protocols that cannot reconfigure when tools change, objectives are revised, or intermediate results suggest a different analytical path [1]. Mimosa is organised into five layers: an optional planning layer that decomposes a high-level research goal into discrete tasks; a tool-discovery layer, built on the Model Context Protocol (MCP) and a companion tool-management platform called Toolomics, which scans for available computational tools exposed as MCP servers; a meta-orchestration layer that either retrieves and mutates a previously archived workflow for a sufficiently similar task, or synthesises a new one from scratch, encoding the result as a directed-acyclic-graph workflow of specialised agents; an execution layer in which each agent is a SmolAgent code-generating agent that writes and runs Python to invoke tools and scientific libraries directly, rather than emitting schema-constrained tool calls; and an evaluation layer in which an LLM-as-a-judge scores each completed execution along four criteria — goal alignment, inter-agent collaboration, output quality, and answer plausibility — and returns structured, evidence-citing feedback that the meta-orchestrator uses to propose the next workflow mutation [1].

The refinement procedure itself is a bounded, single-incumbent local search: at each iteration the best workflow observed so far is mutated by a single structural or prompt-level edit (adding or removing an agent, rewiring which agent receives which predecessor's output, or rewriting a prompt), the mutated workflow is executed and scored, and it replaces the incumbent only if its score improves; the loop terminates after a fixed number of iterations or once the judge score exceeds a preset threshold [1]. Evaluated on ScienceAgentBench — 102 data-driven discovery tasks spanning bioinformatics, computational chemistry, geographic information science, and psychology, each with a programmatic, ground-truth evaluation script independent of the internal judge — Mimosa achieved a 43.1% Success Rate using DeepSeek-V3.2 as the execution model, exceeding both a single-agent baseline (38.2%) and a one-shot (non-iterative) multi-agent configuration (32.4%) with the same underlying model [1]. Critically for the present thesis, the authors report that this benefit is not universal: GPT-4o and Claude Haiku 4.5 showed large single-agent-to-multi-agent gains but only modest or even slightly negative additional gains from iterative refinement, leading the authors to conclude that the value of workflow evolution is contingent on the underlying execution model's instruction-following robustness rather than a guaranteed property of the architecture [1]. They also report that their case-based workflow-retrieval mechanism, though fully implemented, was never actually exercised during the ScienceAgentBench evaluation because no two tasks in that benchmark were similar enough to trigger it — meaning every reported result reflects workflow synthesis *de novo*, with retrieval-and-adaptation left as future work [1].

Two further design choices make Mimosa a suitable starting point for this thesis. First, its tool-agnostic MCP integration means that extending it with a WGBS-specific toolchain (Bismark, methylation extractors, DMR-calling packages, annotation libraries) requires registering new containerised MCP servers rather than modifying Mimosa's core orchestration logic [1]. Second, its emphasis on fully logged, archived execution traces — intended by its authors to support auditability and eventual replication of computational analyses — is directly what RQ5 of this thesis sets out to test empirically: whether that logged trace is, in practice, legible enough for a domain expert to diagnose a wrong or borderline analysis, rather than merely documenting that one occurred [1].


---

## 2.7 Gap and Positioning of This Thesis

Three threads converge into the gap this thesis addresses. First, differential-methylation analysis from WGBS data is a mature, well-benchmarked, but genuinely unsettled statistical problem: published tools disagree with one another even in expert hands, which means any evaluation of an automated system must be built around concordance with a defensible range of outcomes rather than a single ground truth. Second, computational epigenomics already has a documented reproducibility problem driven by pipeline and parameter heterogeneity, which existing workflow-management and pipeline-standardisation tools address only at the level of re-executability, not method appropriateness. Third, agentic AI systems for bioinformatics — including general-purpose ASR frameworks such as Mimosa and domain-specific systems such as AutoBA, CellAgent, and BioMaster — have been built and benchmarked extensively for other data types, but, as far as the literature surveyed here shows, none has been purpose-adapted or systematically evaluated for WGBS differential-methylation analysis, and existing AI-for-methylation work is overwhelmingly supervised prediction rather than autonomous pipeline execution.

This thesis sits at the intersection of these three threads. It adapts Mimosa — chosen specifically for its dynamic tool discovery, its judge-driven iterative refinement, and its emphasis on archived, auditable execution traces — to a domain where "correct" is already a matter of statistical judgement even for human experts, and asks whether an evolving multi-agent system can be shown, empirically and against real benchmarks of concordance and consistency rather than a single internal score, to perform this kind of analysis in a way a domain expert could actually trust.



## References

*(Numbering matches the bracketed citations above; format to your department's required style before submission.)*

1. Legrand, M., Jiang, T., Feraud, M., Navet, B., Taghzouti, Y., Gandon, F., Dumont, E., & Nothias, L.-F. (2026). *Mimosa Framework: Toward Evolving Multi-Agent Systems for Scientific Research*. arXiv:2603.28986 [cs.AI].
2. Shafi, A., Mitrea, C., Nguyen, T., & Draghici, S. (2018). A survey of the approaches for identifying differential methylation using bisulfite sequencing data. *Briefings in Bioinformatics*, 19(5), 737–753. https://doi.org/10.1093/bib/bbx013
3. Dolzhenko, E., & Smith, A. D. [tool: RADMeth] Using beta-binomial regression for high-precision differential methylation analysis in multifactor whole-genome bisulfite sequencing experiments. *BMC Bioinformatics*, 15, 215 (2014). *(verify authorship before citing — retrieved via secondary source; check primary record.)*
4. Benchmarking edgeR and methylKit for the Detection of Differential DNA Methylation: A Methodological Evaluation. *International Journal of Molecular Sciences*, 27(4), 1964 (2026). https://doi.org/10.3390/ijms27041964
5. Calling differentially methylated regions from whole genome bisulphite sequencing with DMRcate. *Nucleic Acids Research*, 49(19), e109 (2021).
6. FAIRification of the DMRichR pipeline: advancing epigenetic research on environmental and evolutionary model organisms. *Bioinformatics Advances*, 5(1), vbaf024 (2025).
7. A comprehensive evaluation of computational tools to identify differential methylation regions using RRBS data. *Genomics* (2020). https://doi.org/10.1016/j.ygeno.2020.07.032
8. Integrative Epigenomics: Bioinformatics (preprint review). *Preprints.org* (2026).
9. Zhou, J., Jiang, J., Han, Z., Wang, Z., & Gao, X. (2025). Streamline automated biomedical discoveries with agentic bioinformatics. *Briefings in Bioinformatics*, 26(5), bbaf505. https://doi.org/10.1093/bib/bbaf505
10. Huang, S., Lang, M., Chen, Z., Yang, C., Huang, X., et al. (2026). From foundation models to autonomous agents in biology. *Genomics Communications*, 3, e006. https://doi.org/10.48130/gcomm-0026-0005
11. Zhou, J., Zhang, B., Li, G., et al. (2024). An AI agent for fully automated multi-omic analyses. *Advanced Science*, 11, e2407094. https://doi.org/10.1002/advs.202407094
12. Artificial intelligence for comprehensive DNA methylation analysis: overview, challenges, and future directions. *Briefings in Bioinformatics*, 26(5), bbaf468 (2025).
13. Wratten, L., Wilm, A., & Göke, J. (2021). Reproducible, scalable, and shareable analysis pipelines with bioinformatics workflow managers. *Nature Methods*, 18, 1161–1168. https://doi.org/10.1038/s41592-021-01254-9
14. ARPEGGIO: Automated Reproducible Polyploid EpiGenetic GuIdance workflOw. *bioRxiv* 2020.07.16.206193 (2020).
15. FAIRification of the DMRichR pipeline [see also ref. 6].
16. Chen, Z., Chen, S., Ning, Y., Zhang, Q., Wang, B., Yu, B., Li, Y., Liao, Z., Wei, C., Lu, Z., Dey, V., Xue, M., Baker, F. N., Burns, B., Adu-Ampratwum, D., Huang, X., Ning, X., Gao, S., Su, Y., & Sun, H. (2025). ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery. *arXiv preprint*.
17. Mitchener, L., Laurent, J. M., Tenmann, B., Narayanan, S., Wellawatte, G. P., White, A., Sani, L., & Rodriques, S. G. (2025). BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology. *arXiv preprint* arXiv:2503.00096.

*Notes for revision: (i) reference 3 needs its primary bibliographic record confirmed directly (author list was not fully visible in the source used during drafting); (ii) references 5, 6, 7, 8, and 12 are given with journal/volume/year only because author bylines were not captured during drafting — pull the full author lists from the DOIs before your bibliography is finalised; (iii) references 16–17 are reproduced from Mimosa's own bibliography and should be independently verified against arXiv/publisher records; (iv) consider whether your department wants numeric (Vancouver/IEEE) or author–date (APA/Harvard) style — this draft uses numeric throughout for consistency with the Mimosa paper, but bioinformatics theses often expect author–date.*


















---

# 03_system_design_and_methods

# Chapter 3 — System Design & Methods

## 3.1 Introduction

The methodology of this work rests on evaluating this fully specified system. The architectural design choices—namely, the separation of orchestration from execution, the encoding of domain expertise as a declarative _skill_, the dual-server tool surface, and the strict file-on-disk reproducibility contract—constitute the mechanisms intended to ensure reliability. These mechanisms are evaluated empirically in the subsequent validation experiments (Chapters 4–6). Furthermore, where specific components are exercised only partially due to computational constraints (such as the upstream alignment pipeline of Server A, which could not be executed on full-scale real data; see §3.2 and Chapter 4), these constraints are delimited alongside the system specifications.

This chapter establishes the baseline architecture, defining the parameters and operational boundaries of the pre-existing system prior to experimental evaluation. The quantitative behavior of the system—specifically its concordance with published studies, its performance against synthetic ground truth, and its reproducibility across repeated executions—is then assessed sequentially in the following chapters.

The architecture and end-to-end data flow are detailed in §3.1, followed by the specifications of the two MCP servers: the Nextflow/methylseq runner (§3.2) and the containerised R methylKit/DSS environment (§3.3). The domain-specific _skill_ governing the agent's analytical decisions is defined in §3.4. The underlying Mimosa framework—including its workflow-synthesis loop, evolutionary search, verifier, and goal specification—is detailed in §3.5.

**Contributions and Pre-existing Framework.** To delineate the scope of novel contributions, the underlying **Mimosa framework**—including its planner, Quality-Diversity evolution engine, multi-source verifier, and SmolAgents/LangGraph runner (§3.5)—as well as the **Toolomics** control plane, constitute prior work developed by the host laboratory (Legrand et al., 2026). These are employed here as the foundational apparatus under test. The novel engineering contributions developed specifically for this research include: the implementation of **both MCP servers** (the Nextflow/methylseq runner detailed in §3.2 and the containerised R/Bioconductor methylation server with bundled annotations in §3.3); the declarative **methylation skill** (§3.4); the **goal specification and its iterative refinement** (§3.5.5); the **epigenomics claim adapter** (§3.7); and corrective modifications to the Perspicacité literature service (§3.7).

- [ ] epigenomics claim adapter'ı ve perspicacite cümlelerini silmek lazım sanki. yaptığın contribution'a göre karar ver task🔼 📅 2026-07-19 



## 3.2 MCP Server A — the Nextflow / nf-core/methylseq runner

Server A is the system's upstream component: it converts raw sequencing reads into the per-CpG coverage files that the downstream analysis consumes. It is a FastMCP application (speaking the streamable-HTTP transport, like Server B) that wraps the community-standard **nf-core/methylseq** workflow and exposes its operation — input preparation, execution, monitoring, and teardown — as eight typed tools. The agent does not invoke `nextflow` directly; it composes these tools, and the server constructs the pipeline invocation, selects an execution backend, and reports status.

### 3.2.1 The tool surface

The eight tools fall into three groups — preparing inputs, running and managing the pipeline, and inspecting the environment:

| Tool                       | Group | Purpose                                                                                                                                                                     |
| -------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prepare_methylseq_inputs` | input | Build the nf-core samplesheet (`sample, fastq_1, fastq_2`) from local FASTQ globs, an S3 path, or a list of SRA accessions; auto-detects R1/R2 mate pairs and sample names. |
| `fetch_sra_data`           | input | Download SRA/ENA/DDBJ data via **nf-core/fetchngs**, locally or on the cloud, optionally emitting a methylseq samplesheet on completion.                                    |
| `upload_to_cloud`          | input | Push local files to S3 (`s3://`) or Google Cloud Storage (`gs://`) for cloud execution.                                                                                     |
| `run_methylseq_pipeline`   | run   | Launch **nf-core/methylseq** with full control over aligner, library type, trimming, M-bias correction, reference, and resource limits; supports `resume`.                  |
| `get_pipeline_status`      | run   | Query a running/finished workflow; for cloud runs returns the `session_id` needed to resume, for local runs checks the Nextflow/Singularity install and free disk.          |
| `manage_pipeline`          | run   | Cancel a running cloud workflow or clean Nextflow work/cache directories.                                                                                                   |
| `list_available_resources` | env   | Enumerate accessible Seqera organisations, workspaces, and compute environments.                                                                                            |
| `validate_environment`     | env   | Pre-flight check of every dependency and credential (Nextflow, Singularity, disk, Seqera/AWS tokens) with remediation hints.                                                |

The biologically consequential parameters are concentrated in `run_methylseq_pipeline`. It defaults to the **Bismark** aligner (with `bwameth` and `bismark_hisat` also selectable), accepts a library-type switch covering `rrbs`, `pbat`, `em_seq`, `single_cell`, `accel`, and `zymo` protocols, and exposes the trimming and M-bias-correction knobs that most affect call quality — adapter clipping at either end and the `ignore_r1/r2` and `ignore_3prime_r1/r2` options (the last defaulting to ignoring two bases of read 2, a standard correction for the end-repair bias of directional WGBS libraries). The reference genome is supplied either as an iGenomes identifier (e.g. `GRCh38`, `GRCm39`) or as a custom FASTA, and per-cytosine reporting is enabled by default so that the output is directly consumable by Server B.

### 3.2.2 Two execution backends

A single `execution_mode` argument selects between two backends that the server configures differently:

- **Local execution** runs Nextflow against a **Singularity** container engine on the workstation (`workflow.containerEngine = 'singularity'`), with a per-process resource ceiling that defaults to 16 CPUs and 128 GB of memory and a 24-hour time limit, and a Singularity image cache held in the workspace. The server first checks, via helper functions, that Nextflow and Singularity/Apptainer are installed and that sufficient disk is free.
    
- **Cloud execution** submits the run to the **Seqera Platform** (formerly Nextflow Tower), which dispatches the work to an **AWS Batch** compute environment. The server talks to the Seqera REST API (default endpoint `https://api.cloud.seqera.io`) through a small client that launches workflows, polls their status, and cancels them, reading the workspace and compute-environment identifiers and access token from environment variables.
    

### 3.2.3 Scope exercised in this work

Both backends are implemented, but the compute resources available for this thesis constrain which is exercised. The project workstation has **no Seqera or AWS access**, so the cloud backend is described as a designed capability rather than an exercised path. The local backend is functional, but aligning full real human WGBS from FASTQ with nf-core/methylseq was estimated at approximately **six days per sample** on this hardware, which is infeasible for the multi-sample replications of Chapter 4. Consequently:

- the **real-data replications (Chapter 4 and Chapter 5) start from the published `.cov` coverage files** and do not exercise Server A's alignment stage;
- Server A's full FASTQ → `.cov` path is demonstrated only at **small synthetic scale** (Chapter 6), where a reduced reference and short simulated read sets complete quickly, with an existing small-genome Bismark test run as additional evidence that the local Singularity path is correct end-to-end.

This is the system's principal honesty boundary, and it is stated here, at the description of the component, rather than left to the discussion: the end-to-end claim of the thesis covers the _coverage-to-regions_ analysis on real data and the _reads-to-coverage_ alignment only on small synthetic data.

## 3.3 MCP Server B — the Dockerised R methylKit/DSS runner

Server B is the system's downstream engine: it takes Bismark coverage files and carries them through differential-methylation analysis to annotated, interpreted regions. It addresses a concrete deployment constraint: Mimosa's own execution sandbox installs only Python packages, so the R/Bioconductor stack that the canonical methylation pipeline requires — methylKit, DSS, genomation, and their dependencies — cannot be installed in the agent's local environment, and any analysis script the agent writes would fail at `library(methylKit)`. Server B resolves this by shipping that stack as a service: a Docker image built on **`bioconductor/bioconductor_docker:RELEASE_3_19`** (Bioconductor 3.19) with methylKit, DSS, bsseq, genomation, GenomicRanges, matrixStats, `data.table` (pinned to 1.15.4), dplyr, ggplot2, clusterProfiler, the `org.Hs.eg.db`/`org.Mm.eg.db` annotation databases, and supporting packages pre-installed, plus pre-built UCSC annotation tracks for hg38 and mm10. The agent executes its R code inside this container over MCP and thereby inherits a fixed, reproducible analysis environment.

### 3.3.1 Two altitudes of tools — and the one used here

Server B can present its R environment at two markedly different altitudes. The two are not both live at once; they are two server variants, and the one that produced every run analysed in this thesis is the more minimal of the two.

**The primary surface: write a real script, then run it (two tools).** The production methylation server is _execute-only_. It exposes just two tools, and deliberately nothing more:

|Tool|Purpose|
|---|---|
|`execute_r_script_file(filename)`|**Primary tool.** Run an R script that already exists in the workspace via `Rscript`, with the workspace as the working directory; the execution timeout is set server-side (default 7200 s).|
|`list_workspace_files()`|List the workspace contents, to sanity-check which scripts and inputs are visible before running.|

The server's documentation states the rationale: "No code-string execution, no script-writing, no typed atomic pipeline tools are registered here — that's intentional, so Mimosa commits to _write a real R script file, then run it_ rather than reaching for shortcuts." Two conventions ensure reproducibility. The script the server runs is a real file already on disk — authored by Mimosa with its own file-writing tools — so the script a reviewer reads is identical to the script that executed, with no inlined code. The text returned to Mimosa is capped (standard output and error truncated to 4000 characters, with the full logs left on disk), keeping Mimosa's context small and forcing large results to persist as files rather than pass through the conversation. This minimalism is itself a reliability decision: it removes Mimosa's option to run throwaway code that leaves no auditable trace.
- [ ] atomic tool alternativini başka bir şekilde tanıt. önceden vardı gibi değil de ayrıca bu da var task🔼 ⏳ 2026-07-19 
**The alternative surface: typed atomic tools (a retained variant).** An earlier design exposed the same R stack at a far more constrained altitude. Alongside four generic runners (`execute_r_code`, which saves supplied R to a timestamped file and runs it; `write_r_script`; `execute_r_script_file`; and `list_workspace_files`), it registered a set of typed _atomic_ tools that each perform one canonical pipeline step and validate their inputs. Each is a thin wrapper that invokes a corresponding `r_scripts/*.R` helper with a JSON argument blob and parses a structured result the helper prints inside a `<<<RESULT>>>…<<<END>>>` footer — so the agent receives, for example, the number of sites tested and the number significant at q < 0.05, not free text. This variant is retained in the repository (`old_server_with_atomicTools`) as an alternative design that prioritises constraint over expressivity. Its fourteen atomic tools cover the whole methylKit workflow:

|Tool|Pipeline step|Key defaults|
|---|---|---|
|`load_bismark`|read `.cov` into a `methylRawList`|`min_cov=10`, `assembly="hg38"`|
|`qc_per_sample`|per-sample methylation/coverage QC plots|—|
|`filter_coverage`|`filterByCoverage`|`lo_count=10`, `hi_perc=99.9`|
|`normalize_coverage`|`normalizeCoverage`|`method="median"`|
|`unite_samples`|`unite` to a `methylBase`|strict intersect unless `min_per_group` set|
|`sd_filter`|drop low-variance CpGs|`sd_cutoff=2.0` (pts)|
|`qc_sample_structure`|correlation / clustering / PCA|—|
|`calculate_dmc`|per-CpG `calculateDiffMeth` (paired via `covariates`)|`overdispersion="MN"`, `adjust="BH"`|
|`tile_methyl_counts`|`tileMethylCounts` + `unite`|`win=500`, `step=500`, `cov_bases=5`|
|`calculate_dmr`|DMR via tiled `calculateDiffMeth`|`overdispersion="MN"`, `adjust="BH"`|
|`get_methyl_diff`|extract significant + write CSV/bedGraph|`difference=10`, `qvalue=0.05`|
|`annotate_methyl_diff`|gene + CpG-island annotation|`assembly`-resolved BEDs|
|`export_methyl_diff`|flat CSV with per-group mean beta|—|
|`list_methylkit_objects`|inspect `.rds` objects in the workspace|utility|

### 3.3.2 State flow via `.rds` files
- [ ] bu başlığa çok gerek yok gibi task🔽 
The atomic tools do not hold state in memory between calls; they pass it through the filesystem. Each step reads one or more `.rds` files (serialised R objects) from the workspace and writes its output as another `.rds`, so a fallback analysis is an explicit chain of files:

```
load_bismark        → methylkit_raw.rds         (methylRawList)
  filter_coverage   → methylkit_filtered.rds    (methylRawList)
  normalize_coverage→ methylkit_normalized.rds  (methylRawList)
  unite_samples     → methylkit_united.rds      (methylBase)
  calculate_dmc     → methylkit_myDiff.rds      (methylDiff)
  get_methyl_diff   → significant.csv
  annotate_methyl_diff / export_methyl_diff → annotation.pdf, results.csv
```

DMR analysis branches from the normalised object through `tile_methyl_counts` → `calculate_dmr`. Because each intermediate is named and typed, a run that fails partway can be resumed: `list_methylkit_objects` reports the class of every `.rds` already present, letting the agent identify the right input for the next step rather than recomputing the expensive differential test. The same `.rds` discipline reappears in the execute-only design of §3.3.1, by convention rather than enforcement: the agent's own scripts serialise their intermediates.

### 3.3.3 Bundled annotation and its resolution

Biological annotation is the last stage of the pipeline, and the image ships the reference tracks it needs so that annotation runs offline: pre-built UCSC RefSeq gene models and CpG-island BEDs for both assemblies, at `/opt/annotations/` — `hg38_refseq_genes.bed` (BED12 transcripts) and `hg38_cpg_islands.bed` (BED4), with `mm10` equivalents. `annotate_methyl_diff` resolves them in a fixed order: an explicit `refseq_bed`/`cpg_bed` path wins; otherwise an `assembly` of `hg38` or `mm10` selects the bundled file; otherwise the tool errors rather than guessing. Other assemblies (hg19, mm9, custom genomes) require the user to supply BED files in the workspace. The gene databases `org.Hs.eg.db` and `org.Mm.eg.db` are likewise bundled, so gene-ontology enrichment runs without network access, whereas KEGG enrichment, which queries a live service, does not.

### 3.3.4 Deployment

Server B requires no change to the Toolomics control plane to come online. `deploy.py` auto-discovers the server's `docker-compose.yml`, assigns it a free port in the 5000–5200 range, and starts the container; Mimosa's port scanner then finds the server and registers its tools automatically — the two of the execute-only server used throughout this thesis, or the fuller set of the retained atomic-tool variant. The image is comparatively expensive to build the first time — installing the Bioconductor stack and downloading the UCSC annotations takes roughly 15–30 minutes — but the result is cached, so this cost is paid once rather than per run.

## 3.4 The skill as router and guardrail

The two MCP servers provide Mimosa with _capabilities_; the **skill** provides it with _judgement_. It is a declarative document — a structured Markdown file Mimosa reads — that encodes the domain expertise a methylation analyst would otherwise supply by hand on every run: which differential-methylation engine fits the data, what quality-control thresholds to apply, which non-obvious pitfalls to avoid, and how to structure a reproducible project. In the layered architecture of §3.1, the skill constitutes the knowledge layer that sits between Mimosa and the tools, shaping _how_ the tools are used without itself executing anything. Its design rationale corresponds to principle 2 of §3.1.4: expertise written once and consulted consistently, rather than re-derived inconsistently by the LLM on each run. Whether this consistency materially reduces run-to-run variance is a question the experiment chapters are positioned to address.

### 3.4.1 The central decision: engine selection

The skill defines its most consequential function as routing between the two engines before any analysis code is written. methylKit and DSS embody different statistical trade-offs: methylKit performs direct per-CpG tests and is well-powered when coverage and replicate counts are high, whereas DSS borrows information across neighbouring CpGs through spatial smoothing and shrinks dispersion across the genome, recovering signal at low coverage or with few replicates that per-CpG tests miss. The skill encodes this distinction as an explicit decision table keyed on coverage and replication:

|Coverage / replicates|Engine|
|---|---|
|≥10× **and** ≥4 replicates/group (high power)|methylKit (`calculateDiffMeth`, `overdispersion="MN"`); DSS also fine|
|5–10×, **or** 2–3 replicates/group|**DSS** (dispersion shrinkage + smoothing)|
|Sparse WGBS, single-CpG resolution wanted|**DSS** with `smoothing=TRUE`|
|Multifactor / covariate-adjusted / paired design|**DSS `DMLfit.multiFactor`** _or_ methylKit `covariates=`|
|<5× or n=2|DSS `equal.disp=TRUE`, or Fisher's exact (methylKit) — exploratory only|

The skill's guidance at the boundary between engines is to run both and treat the concordant DMRs as the confident calls — a built-in form of the cross-method agreement that the experiment chapters also employ as a concordance axis.

### 3.4.2 Progressive disclosure: the hub and the reference files

The skill is organised so that only a small, always-relevant core is loaded into the agent's context by default, with depth pulled in on demand. The hub document owns the shared, engine-agnostic workflow — the execution model, input and aligner detection, file-format definitions, metadata handling, QC thresholds, annotation, interpretation, visualisation, and project structure — and the engine-selection decision above. The command-level depth for each engine lives in two separate reference files, `references/methylkit.md` and `references/dss.md`, which the skill instructs the agent to read **only after it has chosen an engine**. This keeps the resident context compact and avoids loading, say, the full DSS multifactor-GLM reference during a run that uses methylKit.

### 3.4.3 Failure modes as guardrails

A distinctive feature of the skill is that a substantial portion of it catalogues _failure modes_ — the non-obvious facts that, in the authors' experience, cause the most analyses to fail silently. By stating them where the agent will read them, the skill converts hard-won debugging knowledge into preventive guardrails. The most important are:

- **Derive groups from metadata, never hard-code them.** Treatment/group vectors must come from a `metadata.csv`; if it is missing, the agent is told to halt and ask rather than guess.
- **Cap the core count.** `parallel::detectCores()` reports the host's CPUs, not the container's cgroup limit, so naive parallelism oversubscribes inside Docker; the skill prescribes a capped `mc.cores`/`ncores` and lower still on genome-wide objects whose memory scales with cores.
- **Do not double-smooth DSS.** DSS smooths internally, so the raw `BSseq` must be passed to its test; pre-running `bsseq::BSmooth` is a silent statistical error.
- **Counts are required for count-based tests.** A bedGraph that carries only methylation percentages, without methylated/unmethylated counts, is unusable for DSS or methylKit's logistic/Fisher tests.
- **Use exact annotation filenames, never mix aligners, and always send plots to a file device** — the MCP returns text, not graphics.

The QC thresholds the skill fixes are similarly concrete and engine-agnostic: bisulfite conversion inferred from CHH methylation below ~1%, mapping rate above 70%, at least ~1 million covered CpGs per WGBS sample, replicate correlation above r ≈ 0.95, and the expectation that replicates cluster together in PCA with no batch separation — with the standing instruction to flag and confirm with the user before excluding any sample.

### 3.4.4 Project structure and the run report

Finally, the skill prescribes a fixed project layout — `raw_data/`, `metadata.csv`, `config.yaml` (genome, engine, coverage, effect-size and FDR thresholds, tile size, smoothing), numbered `scripts/`, a `results/` tree, and an **append-only `run_report.txt`** in which each step records the mode and engine chosen, the files found, the steps run or skipped, and any samples excluded. The append-only run report is both a reproducibility aid and a source of evidence about what the agent actually decided on a given run.

## 3.5 The Mimosa agent — framework, loop, goal evolution, and the workspace contract

The previous sections described the _capabilities_ the agent acts through and the _knowledge_ that shapes how it acts. This section describes the actor itself. **Mimosa** is the host laboratory's open-source framework for autonomous scientific research (Legrand et al., 2026); this thesis does not introduce it but adopts it as the agent under test. The methylation-specific components that surround it — enumerated in the contribution note of §3.0 — are this thesis's own work, and the validation of the integrated system on DNA-methylation analysis is its purpose. An accurate description of Mimosa is necessary for the validation that follows, because the system extends beyond the "read goal → call tool → observe → repeat" loop sketched in §3.1.1: that loop is what an _execution agent_ performs within a single workflow, but Mimosa as a whole is a system that **synthesises the workflow itself** and can **evolve it across generations**. Both properties bear directly on reliability and are therefore presented here rather than abstracted away.

### 3.5.1 What Mimosa is: a workflow-synthesising, self-evolving framework

Mimosa's self-description is precise: it "writes a custom multi-agent workflow per task, runs it in a sandbox, checks what the agents actually did against independent vantage points, and evolves the workflow across generations with a Quality-Diversity inspired search." Given a task — here, "analyse this folder of WGBS coverage files and call differential methylation" — it does not execute a fixed program but rather _synthesises_ one. The framework is organised in five layers, connected through small dataclass schemas:

|Layer|Component|Role in a methylation run|
|---|---|---|
|0|**Planner** _(optional; `--goal` mode only)_|Decomposes a high-level objective into discrete tasks. Bypassed for the single-task methylation goal used here.|
|1|**ToolManager + Perspicacité**|Scans the configured address/port range (`0.0.0.0:5000–5100`) and registers every MCP tool it finds — the two Toolomics servers of §3.2–3.3 — and, when the Perspicacité literature service (§3.7) is running, can pull supporting literature.|
|2|**EvolutionEngine**|Synthesises the workflow as Python source and, in `--learn` mode, evolves it across generations (§3.5.3).|
|3|**WorkflowRunner**|Executes the synthesised workflow in a sandbox built on Hugging Face **SmolAgents** (a `LocalPythonExecutor` with an AST allow-list) over shared **LangGraph** state. The execution agents inside this sandbox are what call the MCP tools and write the R scripts of §3.3–3.4.|
|4|**VerifierEvaluator**|After each run, scores the workspace from six independent vantage points (§3.5.4) and feeds the next mutation.|

The design commitment that distinguishes Mimosa from a scripted pipeline — and the one most relevant to a reliability evaluation — is **code-as-genotype**: each synthesised workflow is a complete, standalone Python program emitted to disk (no domain-specific language, no YAML), so "any generation can be inspected, diffed, or re-run standalone." The program is the unit that is stored, mutated, and audited. Its _phenotype_ is whatever it produces in the shared workspace: the `.rds` intermediates, figures, tables, and `run_report.txt` of §3.1–§3.4.

### 3.5.2 Execution modes and the run regime used in this thesis

Mimosa exposes several modes, selected by command-line flag. The two axes that matter here are **planning** (`--task` for a single focused operation versus `--goal` for a multi-step objective that invokes the planner) and **learning** (`--learn` adds evolution across generations; without it, the framework synthesises and runs a single workflow — "one-shot"). A `--single_agent` mode skips multi-agent synthesis entirely for a fast, learning-free baseline.

It is necessary to state which regime produced the artefacts this thesis analyses. The completed methylation runs (`run5`–`run12`) were predominantly **one-shot, single-task runs with evolution disabled** — the prompt harness (`scripts/run_prompt_ablation.sh`) explicitly invokes `main.py … --max_evolve_iterations 1` so that each goal variant is evaluated in isolation. Evolution is therefore not the default operating mode of the system as validated here; an honest account of Mimosa requires describing the full evolutionary machinery while being explicit that the majority of the evidence derives from its single-shot use.

### 3.5.3 The evolution loop (when `--learn` is enabled)

When evolution is enabled, the workflow program is the thing that evolves. The mechanics, drawn from the framework's evolution engine (`sources/core/evolution_engine.py`), are:

- **Selection — a Quality-Diversity archive** (MAP-Elites-style, maximum population 50). Each workflow is scored as `qd_score = (1 − w)·quality + w·novelty`; novelty is a k-nearest-neighbour distance (k = 25) over a _behaviour descriptor_ `[n_agents, n_edges, n_branches, prompt_chars]`, so the archive rewards structurally distinct workflows rather than collapsing onto one design.
- **Variation — stagnation-driven scope.** Mutation boldness is a continuous function of how much the recent "prompt gradients" repeat: when progress stalls the search widens from a prompt-level tweak toward a complete topology rethink; near-winners are protected. About 30 % of generations use **crossover** of two parents.
- **Cold start.** When the archive is empty, a similarity-filtered scan of past runs on disk (MiniLM cosine ≥ 0.5) seeds the search, so useful workflows transfer across tasks.
- **Termination.** A generation budget (`max_learning_evolve_iterations`, default 45) or an early-stop when the verifier score reaches `learned_score_threshold` (0.94).

```
  task: "analyse these WGBS .cov files and call differential methylation"
       │
  (0) PLANNER ............. decompose into tasks         (optional, --goal only)
       │
  (1) TOOLMANAGER + Perspicacité
       │  discover MCP tools on 0.0.0.0:5000–5100 (Server A, Server B);
       │  pull supporting literature ─────────────────►  feeds Verifier Source A
       ▼
  (2) EVOLUTION ENGINE ─────────────────────────────────────────────────┐
       │  synthesise the workflow as a standalone Python program          │
       │  (workflow_genotype.py — "code-as-genotype")                     │
       ▼                                                                  │
  (3) WORKFLOW RUNNER   sandbox: SmolAgents LocalPythonExecutor +         │
       │  LangGraph state. Execution agents call the MCP tools, author    │ mutate /
       │  R scripts, run them on Server A / Server B → shared workspace   │ crossover
       ▼                                                                  │ (--learn
  (4) VERIFIER — six deterministic claim sources                         │  only)
       │  A literature   B goal        C disk-vs-claim                    │
       │  D math invariants   E reproducibility   F statistics           │
       │  score + rubric-blind "abstracted gradient"                      │
       ▼                                                                  │
      QD ARCHIVE (MAP-Elites, population ≤ 50) ───────────────────────────┘
      keep structurally-diverse high scorers; draw the next parent
```

_(Figure 3.3.) In the one-shot regime used for most runs in this thesis (§3.5.2) the loop runs once, top to bottom; the return path on the right is active only under `--learn`._

### 3.5.4 The multi-source verifier — what a "success" actually means

The component most directly aimed at trustworthiness is the verifier, and it represents the point at which Mimosa departs most sharply from agents that grade themselves. After each run, **six independent claim sources** inspect the workspace and emit success-polarity claims, and — critically — each claim is checked by a **Python program the judge writes against the workspace, not by re-querying an LLM about whether it believes the agent**:

|Source|Vantage|
|---|---|
|**A**|Peer-reviewed practice, grounded in the literature via Perspicacité (§3.7).|
|**B**|The literal goal text — whether the agents delivered what was asked.|
|**C**|Agent narration — whether the numbers and artefacts the agent _claims_ can be reproduced from what is on disk.|
|**D**|Mathematical invariants — probabilities in [0, 1], shape consistency, no NaNs.|
|**E**|Computational reproducibility — declared dependencies cover the imports actually used, no absolute paths, seeds set on stochastic operations.|
|**F**|Statistical fingerprint — beats a baseline, no degenerate predictions, no leakage signatures.|


### 3.5.5 The model configuration and the goal specification
- [ ] Bu increasing goal fikri çöp oldu sanki. paper replicationları single shot + learning koyarım paperdaki parametreleri kullan diyerekten fln task⏫ ⏳ 2026-07-19 
**Models.** Mimosa is multi-model by design: distinct LLMs fill distinct roles, each configured in `config.py` and routable through OpenRouter via litellm. At the time of writing, the configured defaults are a GLM-5.1 **planner**, a Claude Opus 4.5 **workflow synthesiser** (the model that writes the pipeline code), a DeepSeek-v4 **execution-agent** model, and a Qwen **judge** that writes the verifier programs; generation uses `reasoning_effort = "medium"` and `max_tokens = 8192`. These are configuration fields, not hard-coded choices — any role can be repointed at another provider — and a controlled experiment should **pin a single, fixed configuration** across its repeated runs so that observed variance is attributable to the agent's non-determinism rather than to a changing model target. (This pinning supersedes the earlier project assumption of a single fixed Sonnet model: the system is genuinely multi-model, and the experiment controls for this rather than the system embodying it.)

**The goal as the task contract.** Within a run, the agent is steered by a single _goal file_ — a plain-text task specification provided alongside the data. The goal is where the methylation task is made concrete, and tightening it in response to observed failures is itself part of the engineering contribution of this thesis. Six versions exist (`tools/goals/goal_v1…goal_v6`), and their progression constitutes a compact record of what an LLM agent requires to be told before it analyses WGBS data reliably:

|Goal|What it adds relative to the previous version|
|---|---|
|**v1** minimal|The bare task: from Bismark `.cov` files, call DMCs and DMRs between two groups; read group labels from a samplesheet.|
|**v2** outputs|An explicit required-output list — DMC/DMR tables, a DMC volcano, per-sample and sample-structure QC, and an append-only `run_report.txt`.|
|**v3** MCP|The hard execution constraint: **all R runs through the methylation MCP server**, never locally; author a real `.R` script and execute it; inspect large files with `head`/`zcat`, never open them whole.|
|**v4** methodology|Concrete statistics: `pipeline="bismarkCoverage"`, 10× coverage filter, trim the top 0.1 %, median normalisation, an SD pre-filter, a **paired** test with the donor as a covariate (`overdispersion="MN"`), and dual reporting thresholds (lenient \|Δβ\|≥10 %, strict ≥25 %, both q<0.05).|
|**v5** repository|A reproducible project contract: `config.yaml`, an input-detection step that emits `input_manifest.json`, numbered scripts `00_detect_inputs.py … 04_enrichment.R`, a `run_pipeline.sh` driver, and a machine-parseable `STEP_SUMMARY …` line on each script's final stdout.|
|**v6** corrected|Corrections of recurring agent errors: affirm that methylKit _does_ support paired designs, fix the DMR tile width at 500 bp (not 1000), enforce the **canonical** bundled BED filenames, and add TSS-distance tables for the strict DMC set.|

The trajectory is from _what to do_ (v1–v2) to _how to run it reproducibly_ (v3, v5) to _exactly which statistics, corrected against observed mistakes_ (v4, v6). The dual-threshold reporting and the paired-design instruction in particular are direct responses to the analysis requirements of the Chapter 4 replications.

_(Table 3.1.) The goal-evolution changelog; the final version cites line ranges in each goal file._

### 3.5.6 The workspace contract and the audit trail

**The workspace contract.** Agent and tools do not exchange large objects in messages; they share a single workspace directory (configured as `workspace_dir`) and communicate through files, as introduced in §3.1.3. A run materialises a predictable tree: the input-detection step writes `input_manifest.json` (one record per sample: `sample_id`, `file_path`, `group`, a `treatment` code, and capability flags), so that no downstream script hard-codes sample names or group membership; the numbered R scripts read the manifest and `config.yaml`, write their `.rds` intermediates and figures, and append to `run_report.txt`. This file-on-disk contract is what makes a completed run independently re-executable and, also what makes its failures externally auditable.

**The audit trail.** Because Mimosa is designed for scientific use, every generation is recoverable after the fact. For each synthesised workflow the framework persists, under `sources/workflows/<uuid>/`: the exact executed Python (`workflow_genotype_<uuid>.py`), the lineage and operator that produced it (`lineage_<uuid>.json`: parents and `seed | mutation | crossover`), the exact LLM prompt that generated it (`evolution_prompt_<uuid>.md` — "same prompt + seed = same code"), per-iteration metrics (`run_metrics.json`: wall time, cost, scores), and the abstracted gradient. Companion tools (`memory_explorer.py`, `memory_timelapse.py`, a RAG-backed `--memory_cli`) allow stepping through a run's full trace. The sandbox executes under explicit resource ceilings set in `config.py` — a per-workflow runner timeout of 10 800 s (3 h), a per-agent execution timeout of 21 600 s (6 h), and a 10 GB memory cap — and an insufficiently set timeout is shown by the run archive to be the operational cause of several earlier run failures.

---

## 3.6 [EDITORIAL NOTE — SECTION CONTENT MISSING FROM SOURCE FILE] #update

> **This section is a placeholder, not finished prose.** §3..6 is described in §3.0's chapter outline and cross-referenced seven times elsewhere in this chapter and in Chapter 2, but no actual section body was present in the file supplied for this edit — the document currently jumps from §3.5.6 straight to §3.7. I have not invented the missing content, since it concerns specific empirical findings (bug reports, failure counts, timeout evidence) that only you can supply accurately; fabricating plausible-sounding specifics here would misrepresent your own results. Below is a reconstruction, from the forward-references scattered through the rest of the thesis, of what this section needs to contain and roughly how it is already being cited — use it as a checklist and drop your actual material into the matching subsection. Once you paste in the real content, I can polish it to match the rest of the chapter in the same pass.

Reconstructed scope, by forward-reference:

- **§3.0 (chapter outline):** "§3..6 collects the reliability-engineering guardrails and instrumentation that the experiment chapters draw upon," described in the contribution note as "this thesis's own methodology for making the agent's trustworthiness measurable."
- **§3.5.4 (verifier, Source C):** "Source C is exactly the check that the run-to-run failures of §3..6 violate: an agent can write '1816 significant DMRs' into a report, but Source C asks whether that number survives contact with the files on disk." This section needs the actual worked example(s) of a self-reported number that did not survive an on-disk check.
- **§3.5.4–3.5.5 boundary:** "the methylation-specific sanity assertions of §3..6 are best understood as a domain-tuned extension of Sources C, D and F… the §3..6 assertions check that _this_ number is biologically and arithmetically possible (a tile count cannot be smaller than the number of significant tiles it contains)." This section needs the actual list of domain-specific sanity assertions coded into the pipeline, of which the tile-count example is one instance.
- **§3.5.6 (workspace contract):** "This file-on-disk contract is what makes a completed run independently re-executable — and, as §3..6 shows, also what makes its failures externally auditable" — and later, in the same subsection, that "an under-set timeout is shown by the run archive to be the operational cause of several earlier run failures." This section needs the concrete audit-trail walkthrough (which failed run, which archived artefact revealed the cause) that substantiates both claims.
- **Chapter 2, §2.5 ("The reliability problem"):** "The concrete failures documented in §3..6 — the same input yielding results that differ by orders of magnitude, an impossible region count carried into a biological conclusion — are precisely this problem in the methylation domain." This section needs the specific run(s) and numbers behind that "orders of magnitude" claim.

A plausible internal structure, following the pattern of the rest of the chapter, would be:

**3.6.1 Domain-specific sanity assertions.** The pipeline-level invariants layered on top of the generic verifier (§3.5.4) — e.g., tile counts, significant-CpG counts, and effect-size ranges checked against what is arithmetically or biologically possible given the input data.

**3.6.2 Run-to-run variance and self-reported claims that do not survive audit.** The worked example(s) behind the "1816 significant DMRs" and "orders of magnitude" references — presented as a table or short case study of claimed vs. disk-verified results.

**3.6.3 Timeout ceilings and the audit trail in practice.** The specific run(s) that exhausted the 10 800 s / 21 600 s ceilings of §3.5.6, and how the archived lineage/prompt/metrics files (`lineage_<uuid>.json`, `run_metrics.json`, etc.) were used to diagnose them.

---

## 3.7 Situating Mimosa in the Holobiomics Lab ecosystem

Mimosa and the two Toolomics servers are not isolated artefacts; they belong to a small family of laboratory tools, two of which are described here because they are wired into the system described above and because they frame the future work developed in Chapter 8 (Conclusions). They are summarised only to the depth required for that purpose; neither is itself under validation in this thesis.

**Perspicacité — literature grounding for the verifier.** Perspicacité is a local-first retrieval-augmented-generation service for academic literature: it ingests papers from sources such as Semantic Scholar, OpenAlex, PubMed and arXiv (via the SciLEx multi-database search layer), indexes them with vector embeddings in a local ChromaDB store alongside BM25, and exposes the result as MCP tools and a REST API. Its role in this work is specific and bounded: it is the service behind **Source A** of Mimosa's verifier (§3.5.4) — the "peer-reviewed practice" vantage — and Mimosa discovers and uses it automatically when it is running. It is named here, rather than folded silently into the verifier, partly because it is part of the same ecosystem and partly because two concrete fixes to it form part of this thesis's engineering contribution: making the LLM-provider selection honour the configuration file rather than a hard-coded default, and repairing the SciLEx adapter to load via path injection rather than assuming an installed package.

**Indicium — the claim-standardisation layer and the multi-omics bridge.** Indicium is a small, versioned vocabulary standard for a _typed scientific claim bound to the evidence that grounds it_, with provenance stamps, from which Pydantic models, JSON-Schema, SHACL and OWL are generated. Around it sits an adapter framework (`indicium-adapters`) whose domain plug-ins enrich raw claims with ontology terms; the **epigenomics** adapter handles exactly the claim types this thesis produces (WGBS, and methylation-array assays — resolving assay names, assemblies, and probe identifiers to controlled vocabularies), while a sibling **metabolomics** adapter does the same for that domain. This epigenomics adapter is itself one of the thesis's contributions (§3.0): it is the concrete point at which the methylation work plugs into the shared claim standard, and so the most tangible piece of the multi-omics bridge that Chapter 8 develops. Indicium is not used to _run_ any analysis here — it explicitly does not call DMRs or align reads — and so it is not part of the system under test. It is described because it is the concrete substrate of the thesis's framing claim: methylation is positioned as the **validated first vertical** of a system designed to extend, through a shared claim standard, toward transcriptomics and metabolomics. The benchmark-construction toolkit AgenticScienceBuilder, which turns published papers into machine-readable evaluation tasks against this same standard, completes the ecosystem but is otherwise out of scope.

---

# 04_experiment1_gse263850

# Chapter 4 — Experiment 1: Replication of the GSE263850 AKAP11 Study

The central hypothesis of this thesis asserts that an LLM-based agent can reproduce the principal findings of a peer-reviewed whole-genome bisulphite sequencing study — differentially methylated regions, affected genes, and direction of effect — to a degree comparable with an expert re-analysis of the same data. This chapter subjects that claim to its first empirical test. The experiment takes a single published dataset, GSE263850, and asks three questions: does Mimosa find the same regions, does it assign them the correct biological direction, and does it recover the same downstream biology? A triangulated comparison design — Mimosa versus paper, Mimosa versus an expert baseline, and baseline versus paper — provides the reference frame. The baseline-versus-paper agreement serves as the realistic ceiling against which Mimosa is measured, since even a careful human re-analysis does not reproduce every detail of a published result.

The chapter reports headline concordance metrics, traces each source of divergence to specific parameter choices, catalogues three silent defects that Mimosa's own validation did not catch, and concludes with a scorecard summarising what this first experiment contributes to the overall reliability argument. Findings that span multiple experiments are deferred to the Discussion (Chapter 7).



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

---

# 05_experiment2_gse214232

# Chapter 5 — Experiment 2: Replication of the GSE214232 Dnmt3a Study

<!-- This chapter follows the modular experiment template. Each section mirrors Ch.4. -->

This chapter presents the second test of the hypothesis: whether the agent replicates the
principal findings of a published WGBS study in a different organism. Where Experiment 1
(Chapter 4) demonstrated the agent's behaviour on human data (GSE263850, *AKAP11*
heterozygous knockout), Experiment 2 applies the identical evaluation framework to a mouse
dataset — GSE214232, a conditional knockout of *Dnmt3a*, a DNA methyltransferase — thereby
testing cross-species generalisation of the agent's analytical capability.

The experimental design is the same three-arm triangle used in Chapter 4: the published results
serve as the replication target, an expert re-analysis provides the realistic ceiling, and the
agent's output is scored against both. The mouse genome (mm10) exercises the system's
portability across assemblies and organisms, including the config-driven annotation described
in §3.3.

---

## 5.1 Dataset and biological context

<!-- To be completed when the dataset is fully characterised. -->
<!-- Key information to include:
     - Citation for the original study
     - Biological question (Dnmt3a conditional KO)
     - Experimental design (groups, sample counts)
     - Published analysis parameters and key findings (DMR counts, key genes)
     - Data availability (GEO accession, file format)
-->

## 5.2 Experimental design

The three analysis arms are:

**Arm 1 — Published results.** The DMR counts, associated genes, and enriched pathways
reported in the original publication.

**Arm 2 — Expert re-analysis (baseline).** A human-authored R script replicating the
published analysis parameters as faithfully as possible.

**Arm 3 — Agent pipeline.** The Mimosa agent, given the same coverage files and a
natural-language goal, synthesising and executing its own analysis.

<!-- Detail the specific goal version, agent configuration, and any mm10-specific considerations. -->

## 5.3 Results

<!-- To be completed. Subsections will include:
     - Headline DMR counts across the three arms
     - Parameter analysis (as in §4.3)
     - Direction labelling assessment
     - Overlap and concordance metrics
-->

## 5.4 Gene recovery and biological concordance

<!-- To be completed. -->

## 5.5 Genomic context distribution

<!-- To be completed. -->

## 5.6 Identified defects

<!-- To be completed. Assess whether the defects from Experiment 1 recur. -->

## 5.7 Chapter summary

<!-- To be completed. Address:
     - What Experiment 2 contributes to the hypothesis
     - Whether error modes from Experiment 1 recur or are dataset-specific
     - Whether cross-species generalisation holds
     - Forward reference to Discussion (Ch.7)
-->


---

# 06_experiment3_simulated_fastq

# Chapter 6 — Experiment 3: End-to-End Pipeline with Simulated FASTQ

<!-- This chapter follows the modular experiment template. -->

This chapter presents the third and final test of the hypothesis: whether the agent can execute
the complete WGBS analysis pipeline — from raw sequencing reads through alignment and
methylation extraction to differential methylation calling — without human intervention.
Where Experiments 1 and 2 (Chapters 4 and 5) validated the agent's downstream analytical
capability starting from pre-existing coverage files, Experiment 3 exercises the full system
architecture described in Chapter 3, including MCP Server A (Nextflow / nf-core/methylseq) for
the upstream alignment stage.

The experiment uses simulated FASTQ files rather than real sequencing data. This choice is
driven by two considerations. First, the computational cost of aligning full real human WGBS
data was infeasible on the available hardware (§3.2). Second, simulated data provides a
controlled setting in which the pipeline's end-to-end execution can be verified independently
of biological complexity. The objective is not to benchmark sensitivity or specificity against
ground truth, but to demonstrate that the agent can autonomously orchestrate the entire
pipeline — input preparation, alignment, methylation extraction, differential testing, and
biological interpretation — producing a coherent and complete analysis from raw reads.

---

## 6.1 Simulated data generation

<!-- To be completed. Sections to address:
     - Tool used for FASTQ simulation (e.g., Sherman, ART, or custom)
     - Reference genome used (reduced or full)
     - Number of samples, groups, and simulated read depth
     - Any methylation patterns embedded in the simulation
-->

## 6.2 Experimental design

<!-- To be completed. Sections to address:
     - Agent configuration (goal version, execution mode)
     - Server A configuration (local backend, Singularity, resource limits)
     - Server B configuration (engine choice)
     - Expected pipeline stages and outputs
     - Success criteria: what constitutes a successful end-to-end run?
-->

## 6.3 Pipeline execution

<!-- To be completed. Sections to address:
     - Server A stage: samplesheet preparation, nf-core/methylseq execution
     - Coverage file generation
     - Server B stage: loading, QC, differential testing, annotation
     - Agent's decision trace (what the agent chose at each stage)
     - Wall time, resource usage
-->

## 6.4 Results

<!-- To be completed. Sections to address:
     - Was the pipeline completed end-to-end without manual intervention?
     - Output files produced
     - QC metrics from alignment and methylation extraction
     - DMR/DMC calls produced
     - Any errors, retries, or agent interventions
-->

## 6.5 Identified issues

<!-- To be completed. Sections to address:
     - Any failures or workarounds during execution
     - Parameter choices the agent made for the upstream stage
     - Comparison of agent's alignment choices with best practices
-->

## 6.6 Chapter summary

<!-- To be completed. Address:
     - What Experiment 3 demonstrates about the hypothesis
     - The significance of full-pipeline capability
     - Honest scope: simulated data, reduced scale
     - Forward reference to Discussion (Ch.7)
-->


---

# 07_discussion

# Chapter 7 — Discussion

This chapter synthesises the findings of Experiments 1–3 (Chapters 4–6), evaluates them
against the hypothesis stated in §1.3, and considers the strengths, limitations, and threats
to validity of the work.

---

## 7.1 Summary of experimental findings

<!-- To be completed after Chapters 4–6 are finalised. Synthesise across experiments:
     - Concordance achieved in the two replications
     - Pipeline capability demonstrated in Experiment 3
     - Recurring vs. experiment-specific error modes
     - The role of the skill and tool architecture in observed performance
-->

## 7.2 Evaluation against the hypothesis

<!-- To be completed. Address each facet of the hypothesis:
     - Can the agent replicate published findings? (Exp.1, Exp.2)
     - Does this generalise across organisms? (Exp.1 vs. Exp.2)
     - Can the agent execute the full pipeline? (Exp.3)
     - Are results concordant with expert analyses?
     - State the verdict explicitly: supported, partially supported, or not supported.
-->

## 7.3 The role of silent defects

<!-- To be completed. Discuss:
     - The pattern of silent defects across experiments
     - What external comparison reveals that internal validation misses
     - Implications for trust in agent-produced scientific analyses
     - The gap between capability and reliability
-->

## 7.4 Strengths of the approach

<!-- To be completed. Consider:
     - Triangulated evaluation design
     - Use of a domain with knowable correct answers
     - Sign canonicalisation and post-hoc assertions
     - Modular, reproducible system design
-->

## 7.5 Limitations

<!-- To be completed. Address honestly:
     - Compute constraints (no cloud, coverage-file starting point for Exp.1/2)
     - Simulated vs. real data for Exp.3
     - Single agent framework (Mimosa) — generalisability?
     - No formal false-positive calibration study
     - No formal reliability/reproducibility study (repeated runs)
     - Limited to two datasets and one domain
-->

## 7.6 Threats to validity

<!-- To be completed. Consider:
     - Internal validity: parameter differences between arms
     - External validity: generalisability beyond WGBS, beyond Mimosa
     - Construct validity: what "concordance" measures vs. what practitioners need
-->


---

# 08_conclusions

# Chapter 8 — Conclusions and Future Work

## 8.1 Contributions

<!-- To be completed. List the concrete contributions:
     1. The first rigorous validation of an LLM agent on WGBS differential methylation analysis
     2. Two MCP tool servers (Nextflow/methylseq runner, R/Bioconductor methylation runner)
     3. The methylation skill encoding domain expertise as a declarative document
     4. Goal specification and its six-version evolution
     5. Sign-canonicalisation library and post-hoc sanity assertions
     6. The epigenomics claim adapter for Indicium
     7. Two fixes to the Perspicacité literature service
-->

## 8.2 Conclusions

<!-- To be completed. State the main conclusions:
     - What the experiments demonstrate about the hypothesis
     - The gap between capability and reliability
     - The value of measurement against knowable truth
     - Practical implications: when can (and when should) an LLM agent be trusted?
-->

## 8.3 Future work

<!-- To be completed. Develop:
     - Multi-omics extension: transcriptomics and metabolomics via the same infrastructure
     - Formal reproducibility study: repeated identical runs with controlled ablation
     - Synthetic ground-truth benchmark: calibration of false-discovery rates
     - Cloud-scale alignment: exercising Server A on full real WGBS via Seqera/AWS
     - Agent self-correction: using the post-hoc assertions as feedback during the run
     - Broader agent evaluation: other domains with knowable correct answers
-->


---

# 09_bibliography

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


---

# 10_annexes

# Annexes

## A. Methylation Skill Document

<!-- Include the full skill text here or as a referenced file. -->

## B. MCP Tool Catalogues

<!-- Server A: 8 tools with full signatures and descriptions. -->
<!-- Server B: 2 execute-only tools + 14 atomic tools (retained variant). -->

## C. Agent Transcript

<!-- A complete transcript of a representative agent run (e.g., run23). -->

## D. Supplementary Result Tables

<!-- Additional tables not included in the experiment chapters. -->

## E. Environment Manifest

<!-- Docker image versions, R/Bioconductor package versions, Nextflow version, etc. -->
