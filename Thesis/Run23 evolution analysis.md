---
tags:
  - Thesis
  - Mimosa
  - Results
---
# Run23 evolution analysis

## Connections

- [[Thesis MOC|Thesis / Mimosa MOC]]
- [[Thesis/run_comparison_report|Mimosa runs vs baseline]]
- [[Thesis/Thesis_v1/System Design & Methods|Chapter 3 - System Design & Methods]]
- [[Thesis/Thesis_v1/04_validation1_replication|Chapter 4 - Validation I: Replication]]

Now let me check evaluation3 and evaluation5.Here's the full picture across all 6 Mimosa iterations, cross-referencing `run_metrics*.json`, `evaluation*.txt`, and the self-verification data embedded in `state_result*.json`.

## Run-by-run summary

|Iter|UUID|Kind|Parent|Score (capped/raw)|Cost|Wall time|Outcome|
|---|---|---|---|---|---|---|---|
|0|`96420b35`|seed|—|0.0 / 0.0|$0.02|3h02m|**Total execution error** — all 30 verifier claims came back `error` (nothing could even be scored). No `state_result0` was produced.|
|1|`1889fcbb`|seed|—|**0.860 / 0.860**|$1.68|46m|Best run of the whole tree. 22/27 pass, 3 fail, 1 error, 1 unsure.|
|2|`d06857ed`|mutation|1889fcbb|**0.500 / 0.726**|$1.83|47m|Hard-fail capped: high average (0.726) but the _mandatory_deliverable_ claim failed (`DMRs_annotated.txt` missing expected columns), so the score is capped to 0.5 regardless of the rest.|
|3|`a3ae1229`|mutation|d06857ed|0.0 / 0.0|$0.03|3h03m|**Total execution error** again, no evaluation produced.|
|4|`a25cf440`|mutation|d06857ed|0.716 / 0.716|$2.00|3h15m|22/31 pass, 8 fail, 1 unsure.|
|5|`1bc68129`|mutation|a25cf440|0.690 / 0.690|$1.92|1h00m|23/35 pass, 9 fail, 3 unsure.|

Total spend across the whole tree: **~$7.48**. Total wall time: **~12 hours**. And the evolutionary search never beat the first seed (0.86) — everything downstream of it regressed.

## Why each run actually failed

**Iter 0 & 3 (total errors):** These burned the _most_ wall-clock time (3+ hours each) yet cost almost nothing in tokens and produced zero usable output or evaluation. That pattern — long duration, tiny cost, zero result — smells like the agent got stuck retrying an MCP call or hit an execution timeout rather than failing fast on a logic error. Worth checking the raw transcripts/observations for these two specifically if you have them, since they're the biggest waste of wall-clock budget in the tree.

**Iter 1 (0.86, best):** Failed on:

- Hardcoded group/treatment mapping (`'KO'`, `'wt'`) instead of reading dynamically from `samplesheet.csv`.
- Hardcoded annotation BED paths instead of resolving from `/opt/annotations/` via config.
- DMR tile-length inconsistency (see logic critique below).

**Iter 2 (capped to 0.5):** Same recurring hardcoding pattern, plus the annotated DMR table was missing columns entirely — a real, load-bearing bug, correctly triggering the hard-fail cap. Also failed `run_report_integrity` (missing required log sections) and — oddly — `manifest_structural_validity`, even though the same run's own self-check and other runs' checks passed manifest validity fine.

**Iter 4 (0.716):** New/different failures appeared instead of the old ones being fixed: `input_manifest_generation` failed because `sample 0` was missing the `treatment` key; two PDFs (`dendrogram.pdf`, `chromosome_summary.pdf`) were confirmed _actually blank_ by the verifier's pixel-variance check — something the agent's own re-validation script never caught, because it only checked file existence/size, not rendered content. Also failed `engine_selection_and_api` with the reason "Design not 2-group/3-rep," which is almost certainly a downstream casualty of the broken manifest (missing `treatment` key breaks the design-detection logic) rather than an actual wrong engine choice — every other run confirms 3 KO vs 3 wt.

**Iter 5 (0.690):** Reverted back to hardcoded treatment mapping and hardcoded BED paths (regressing behavior iter4 had actually avoided in that area), plus missing R script comment headers and unsafe large-file inspection.

## Persistent, never-fixed issues across nearly every run

- Hardcoded group/treatment labels instead of sourcing from `samplesheet.csv`/manifest (iter1, iter2-partially, iter5)
- Hardcoded annotation BED paths instead of dynamic `/opt/annotations/` resolution (iter1, iter5; iter4 differently broken)
- DMR tile-length/coordinate-consistency failure (iter1, 2, 3-implied, 4, 5 — essentially every scored run)
- "Large file inspection" safety check (grep for `head`/`zcat`/`wc -l`) fails in every single evaluated run

The evolutionary search kept trading one bug for a different one rather than converging — it never fixed the core hardcoding problem and never beat the original seed's score.

## Is the evaluator's logic actually sound for WGBS/methylation analysis?

A few things stand out:

1. **The DMR tile-consistency check looks like it's testing the wrong thing.** It repeatedly fails runs for producing DMRs whose interval lengths aren't a fixed 1000bp window. But when the engine is DSS, `callDMR` doesn't tile the genome into fixed windows — it merges runs of significant, spatially-correlated CpGs into variable-length regions (that's the actual DSS methodology, distinct from `methylKit::tileMethylCounts`'s fixed-window tiling). If the workflow legitimately chose DSS (which the evaluator itself credits as correct engine choice in most runs), penalizing it for _not_ producing fixed 1000bp tiles is arguably penalizing correct DSS behavior rather than a real defect. This looks like a claim written with methylKit's tiling model in mind and applied indiscriminately to DSS output.
    
2. **The blank-PDF pixel-variance check (std > 5) is a genuinely good, hard-to-game test** — it caught real blank plots (iter4) that the agent's own re-verification missed entirely, because the agent only checked file existence/size, never rendered content. That's the evaluator doing something the self-audit structurally can't.
    
3. **Manifest/path-existence failures look inconsistent across runs** in ways that suggest environment mismatch rather than real bugs — e.g., iter4 failed because a manifest path was prefixed `/app/workspace/...` and didn't resolve, while functionally-identical manifests in other runs passed. That's worth treating with some skepticism as an artifact of how the verifier resolves container paths, not necessarily a true agent error.
    
4. **The hard-fail capping mechanism (iter2) is sound design** — a high average score (0.726) got correctly overridden to 0.5 because the literal named deliverable was broken. That prevents an agent from "gaming" the score by acing many low-stakes sanity checks while failing the actual point of the pipeline.
    
5. **Systemic pattern worth flagging**: in all six runs, the agent's own self-verification step reports near-universal "PASS," including for defects the external verifier later caught (hardcoded literals phrased differently than the self-check's grep patterns, blank PDFs, tile-width violations). The self-audits lean on shallow signals (row counts, "not all NA," file size) rather than the deeper semantic checks the external verifier applies — so the self-verification score is not a reliable proxy for actual pass rate, and the QD evolutionary loop may be over-trusting it when deciding what to mutate next.
    

If you want, I can pull the raw actions/observations from `state_result1` and `state_result3` (the two full-error runs) to see whether they timed out on the same MCP call, which would tell you whether that's a systemic infra issue rather than a workflow-design issue.
