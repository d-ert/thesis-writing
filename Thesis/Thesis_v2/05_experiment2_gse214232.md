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
