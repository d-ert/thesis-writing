# Chapter 2 — Background & Related Work

## 2.1 DNA Methylation and Whole-Genome Bisulfite Sequencing

DNA methylation is the covalent addition of a methyl group to the 5-carbon of cytosine, producing 5-methylcytosine (5mC). In vertebrates it occurs predominantly at cytosine–guanine dinucleotides (CpG sites); although only a small fraction of genomic cytosines are methylated overall, CpG sites are methylated the large majority of the time [2]. Methylation at gene promoters is generally repressive: a methylated CpG site restricts the binding of transcription factors, whereas an unmethylated site permits it, so methylation state is tightly linked to transcriptional regulation, cellular differentiation, genomic imprinting, and X-chromosome inactivation [2, 3]. Aberrant methylation — hypermethylation of tumour-suppressor promoters, hypomethylation of oncogenes — is a well-established feature of cancer, which is part of why differential-methylation analysis is clinically as well as biologically motivated [2, 3].

Whole-genome bisulfite sequencing measures methylation at single-base resolution across an entire genome by exploiting a simple chemical asymmetry: treatment with sodium bisulfite deaminates unmethylated cytosines to uracil, which is read as thymine during sequencing, while methylated cytosines are left unconverted and continue to read as cytosine [2, 3]. Comparing the resulting sequence to an unconverted reference therefore recovers, at each covered CpG site, an estimated methylation level as the ratio of reads retaining a cytosine call to total reads at that site. Because bisulfite conversion introduces a large and systematic mismatch between reads and the reference genome, standard aligners perform poorly on unconverted references; dedicated bisulfite aligners such as Bismark instead align reads against *in-silico* converted versions of the genome (or use "wildcard" aligners that treat unconverted cytosines specially) before recovering per-site methylation calls [2]. A typical WGBS analysis therefore proceeds through six broadly agreed stages: raw-read quality control and adapter trimming; bisulfite-aware alignment to a reference genome; post-alignment quality assessment; per-cytosine methylation extraction; differential methylation testing at the level of individual cytosines and/or aggregated regions; and, finally, annotation of the resulting regions against gene models and regulatory features [2].


WGBS is the most comprehensive methylation assay but not the only one: reduced-representation bisulfite sequencing (RRBS) enriches for CpG-dense regions at lower cost, and methylation microarrays (the Illumina 450K and EPIC platforms) interrogate a fixed panel of pre-selected CpGs. These trade genome-wide coverage for cost or convenience. The experiments of this thesis use WGBS coverage data.

---
## 2.2 From reads to coverage: the alignment pipeline 
- [ ] task⏫ 📅 2026-07-19 (BURAYA ALİGNMENT PİPELİNE'YLA VE NEXTFLOWLA İLGİLİ BİŞEY YAP YAP)

Between the sequencer and the statistics sits an alignment-and-extraction pipeline whose job is to
turn millions of short, bisulfite-converted reads into the per-CpG count table of §2.1. This is
the stage automated by **MCP Server A** in Chapter 3, and three properties of it matter for the
thesis.

**Bisulfite-aware alignment is its own problem.** Standard short-read aligners assume the read and
the reference share an alphabet; bisulfite conversion deliberately breaks that assumption by
turning most cytosines into thymines, creating a three-letter genome that conventional alignment
mishandles. Specialised aligners solve this — most prominently **Bismark**, which converts reads
and reference into a common reduced alphabet, aligns, and then restores the original bases to
score methylation [@krueger2011]. Bismark also performs the **methylation-extraction** step that
emits the coverage file consumed downstream: a per-cytosine report of chromosome, position,
strand, methylation percentage, and methylated/unmethylated counts — the Bismark `.cov` format on
which the rest of the analysis depends.

**Reproducibility is delegated to a workflow framework.** Running this multi-step process — quality
trimming, alignment, deduplication, methylation extraction, reporting — reproducibly across
samples and machines is the role of a workflow manager. The community standard is **Nextflow**,
which expresses a pipeline as a dataflow of containerised processes so that the same workflow runs
identically on a laptop, a cluster, or the cloud [@ditommaso2017]. On top of it, the **nf-core**
project curates peer-reviewed, versioned, community-maintained pipelines with standardised inputs,
tests, and software-provenance reporting [@ewels2020], and **nf-core/methylseq** is its WGBS
pipeline — the exact artefact Server A invokes. The significance for this thesis is that
this upstream stage is already engineered for reproducibility through pinned containers and
versioned code; the non-determinism the thesis investigates is introduced not here but by the
agent that orchestrates it.

**The coverage file is the natural boundary.** Because alignment is computationally heavy — full
real-WGBS alignment was infeasible on the available hardware (Chapter 3) — the coverage file is
also the practical boundary at which this thesis's real-data validation begins. The data model of
§2.1 is recovered exactly at this point, so downstream analysis can be validated against published
studies even when the alignment half is exercised only at small synthetic scale.

---

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
















# Eskiden kalanlar
- [ ] background knowledge'da bu altta kalanları oku, ekleyebildiklerini yukarı ekle, gerisini sil task⏫ 📅 2026-07-19 



## 2.4 Large language model agents, tool use, and the Model Context Protocol

The second literature concerns the actor rather than the analysis. Modern LLMs are
transformer-based sequence models [@vaswani2017] which, once scaled, exhibit strong few-shot and
instruction-following behaviour [@brown2020] and can be prompted to externalise intermediate
reasoning before answering [@wei2022]. On their own, however, they are closed systems: they
generate text, cannot execute code or read files, and have no access to ground truth beyond their
training. The step from language model to agent is the addition of **tools** and a **loop**.

**Tool use and the agent loop.** A tool-using agent interleaves reasoning with action: it decides
on a next step, calls an external tool, observes the result, and repeats. The **ReAct** pattern
formalised this interleaving of reasoning traces and tool actions [@yao2023], and **Toolformer**
showed that models can learn when and how to invoke tools through their API signatures
[@schick2023]; retrieval-augmented generation similarly grounds outputs in external documents
rather than parametric memory [@lewis2020]. The recurring theme is that the model supplies
decisions while tools supply capabilities and ground truth — exactly the orchestration/execution
split that Chapter 3 makes its central design commitment.

**The Model Context Protocol.** Connecting an agent to many tools historically meant bespoke
integration code per tool. The **Model Context Protocol (MCP)**, an open standard introduced in
late 2024, defines a uniform client–server interface through which an agent discovers and calls
tools, retrieves resources, and uses prompt templates, so that any MCP-speaking client can use any
MCP server without custom glue [@mcp2024]. MCP is the protocol on which the Toolomics servers of
§3.2–3.3 are built, and the property that makes it valuable for reliability is the same one that
makes it valuable for engineering: tools become typed, versioned, independently testable services
rather than inlined code, which confines the unpredictable component to the agent and keeps the
executing component fixed.

**Encoding domain expertise.** A capability gap remains between having tools and using them
well: an agent equipped with methylKit and DSS still needs to know which to choose, what
thresholds to set, and which pitfalls to avoid. A lightweight answer that has emerged in agent
practice is the **skill** — a declarative, version-controlled document of domain procedure and
guardrails that the agent consults at run time rather than re-deriving on every invocation. The
methylation skill of §3.4 is an instance of this idea, and whether such encoded expertise
improves the quality and consistency of agent-driven analyses is a question the experiments of
Chapters 4–6 address.

---

## 2.5 Autonomous agents for science and the reliability problem

Tool-using agents have been turned toward scientific work with striking demonstrations, and with
equally striking gaps in their evaluation. The promise and the problem together motivate this
thesis.

**Agents that do science.** Recent systems couple LLMs to laboratory and computational tools to
carry out research tasks with limited human intervention: agents that plan and execute chemical
synthesis or computational chemistry by orchestrating domain tools [@boiko2023; @bran2024], and
frameworks that attempt end-to-end research — ideation, experimentation, and write-up — in machine
learning [@lu2024]. The framework this thesis evaluates, Mimosa (Chapter 3), belongs to this
lineage but answers a narrower, more measurable question than full-paper generation: can a
per-task synthesised workflow reproduce a known analysis? [@legrand2026]

**The reliability problem.** What these demonstrations rarely establish is reliability. LLMs are
non-deterministic and prone to fluent, confident errors — including fabricated facts and
unsupported claims [@ji2023] — and an agent that wraps an LLM inherits these failure modes while
adding new ones: silent tool failures, irreproducible run-to-run behaviour, and self-reported
successes that do not survive inspection. In a scientific setting these are disqualifying unless
measured and controlled, because a plausible-looking wrong answer is worse than an obvious one. The
concrete failures documented in §3.6 — the same input yielding results that differ by orders of
magnitude, an impossible region count carried into a biological conclusion — are precisely this
problem in the methylation domain.

**Evaluation is catching up, unevenly.** Benchmarks have begun to measure agent capability on
scientific and data-analysis tasks — for example task suites that score whether an agent's
generated analysis reproduces a reference result [@scienceagentbench; @paperbench]. These measure
capability (does it ever succeed?) more than reliability (does it succeed consistently, and
fail safely?), and they are general rather than tied to a domain with an established ground truth.
For a clinically-adjacent assay such as WGBS methylation, the quantities a practitioner actually
needs — concordance with published findings, calibrated false-positive control, and reproducibility
across repeated runs — have not, to our knowledge, been reported for an LLM agent.

---

## 2.6 The gap and the thesis's position

Bringing the two literatures together exposes a specific, fillable gap.

On one side, **the methods are mature and their correct answers are knowable** (§2.1–2.3): WGBS has
canonical formats, methylKit and DSS are characterised tools, published studies provide concrete
target findings, and synthetic data can supply exact ground truth. On the other side, **agents are
capable but unproven on reliability** (§2.4–2.5): the orchestration/execution split and protocols
like MCP make it architecturally possible to fence non-determinism away from numerical execution,
and skills make it possible to encode expertise — but whether these mechanisms deliver concordant,
well-controlled methylation analysis has not been demonstrated or measured.

That absence is the gap this thesis addresses. Where prior agent-for-science work emphasises
capability demonstrations, this work emphasises **measurement against knowable truth** in a single
well-chosen domain. The hypothesis stated in Chapter 1 proposes that a tool-augmented LLM agent,
constrained by a domain skill and typed MCP tools, can autonomously execute WGBS differential-
methylation analyses — replicating published findings across organisms and executing the full
pipeline from raw reads to called regions — with results concordant with expert analyses. The
system that makes this testable is the subject of Chapter 3; the measurements themselves are
Chapters 4–6, which validate the hypothesis through replication of a human dataset, replication
of a mouse dataset, and an end-to-end run on simulated data respectively. The conclusions are
drawn in Chapter 7.
