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
