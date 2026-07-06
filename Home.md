---
cssclass: dashboard
tags:
  - MOC
  - dashboard
---
# 🏠 Academy

<span class="dash-date">`= dateformat(date(today), "EEEE, MMMM d, yyyy")`</span>

---

## ⚡ Quick Nav

> [!grid-4]
>
> > [!example]+ 📝 Thesis
> > [[Thesis/MOC|Thesis / Mimosa →]]
> > Validation, Mimosa runs, chapters
>
> > [!example]+ 📦 epykit
> > [[Epykit/MOC|epykit →]]
> > Benchmarks, FDR, releases
>
> > [!example]+ 📚 References
> > [[References/MOC|References →]]
> > WGBS methods, callers, literature
>
> > [!example]+ 📋 Tasks
> > [[TODO|Active TODO →]]
> > Cross-project tasks

---

## 📊 Thesis Progress

> [!grid-2]
>
> > [!info]+ Chapter Status
> > | Ch | Title | Status |
> > |---|-------|--------|
> > | 1 | Introduction | ✅ v1 |
> > | 2 | Background & Related Work | ✅ v1 |
> > | 3 | System Design & Methods | ✅ v1 |
> > | 4 | Validation I: Replication | ✍️ WIP |
> > | 5 | Validation II: Synthetic | ⛏️ Blocked |
> > | 6 | Discussion | ⛏️ Blocked |
> > | 7 | Conclusions & Future Work | ⬜ TODO |
> > | 8 | Bibliography | ✍️ WIP |
> > | 9 | Annexes | ⬜ TODO |
> >
> > **3 / 9** chapters drafted — **open items:** citation verification (Ch.2), Study B data (Ch.4), figures (Ch.3)
>
> > [!tip]+ Working On
> > **Thesis**
> > - [[Thesis/Thesis_v1/OUTLINE|Master outline →]]
> > - [[Thesis/Thesis_v1/04_validation1_replication|Ch.4 — Validation I ✍️]]
> > - [[Thesis/Study C Method|Study C — run on workstation]]
> > - [[Thesis/run_comparison_report|Run comparison report]]
> > - [[Thesis/Run23 evolution analysis|Run23 evolution]]
> >
> > **epykit**
> > - [[Epykit/fdr_analysis|FDR analysis — fine-tune on dmrseq sim]]
> > - [[Epykit/study1_vs_study2|Study 1 vs Study 2]]
> > - [[Epykit/epykit_todo|epykit TODO →]]

---

## 🔬 Workstream Details

> [!grid-2]
>
> > [!abstract]+ Thesis / Mimosa
> > ### Thesis Draft
> > - [[Thesis/Thesis_v1/Index|Thesis v1 index]]
> > - [[Thesis/Thesis_v1/Introduction|Ch.1 — Introduction]]
> > - [[Thesis/Thesis_v1/Background|Ch.2 — Background]]
> > - [[Thesis/Thesis_v1/System Design & Methods|Ch.3 — System Design]]
> > - [[Thesis/Thesis_v1/04_validation1_replication|Ch.4 — Validation I]]
> > - [[Thesis/Thesis_v1/Bibliography|Bibliography]]
> >
> > ### Mimosa & Runs
> > - [[Thesis/Run23 evolution analysis|Run23 — best F1 but evolution degrades]]
> > - [[Thesis/run_comparison_report|Runs vs baseline]]
> > - [[Thesis/Study C Method|Study C method]]
> > - [[Thesis/Whole bunch of skills that Mimosa can use|Mimosa skill ideas]]
>
> > [!abstract]+ epykit
> > ### Core
> > - [[Epykit/epykit_README|README & API reference]]
> > - [[Epykit/epykit_todo|TODO list]]
> > - [[Epykit/Benchmark Results|Benchmark results]]
> >
> > ### Diagnostics
> > - [[Epykit/fdr_analysis|FDR calibration & improvements]]
> > - [[Epykit/study1_vs_study2|Study 1 vs Study 2 comparison]]
> >
> > ### Open Issues
> > - dmrseq sim data performance gap
> > - Caching mechanism — double-check `dmc()` cache
> > - `explore_dataset` function design

---

## 🗓️ Recent Activity

> [!grid-bottom]
>
> > [!note]+ Daily Notes
> > ```dataview
> > TABLE WITHOUT ID
> >   link(file.path, dateformat(file.day, "ccc, MMM d")) AS "Date",
> >   truncate(join(filter(file.lists.text, (t) => t != null), " · "), 80) AS "Notes"
> > FROM "Daily notes"
> > SORT file.day DESC
> > LIMIT 7
> > ```
>
> > [!note]+ Recently Modified
> > ```dataview
> > TABLE WITHOUT ID
> >   file.link AS "Note",
> >   dateformat(file.mtime, "MMM d, HH:mm") AS "Modified"
> > FROM "" AND -"Daily notes" AND -".obsidian"
> > WHERE file.name != "Home"
> > SORT file.mtime DESC
> > LIMIT 8
> > ```

---

## 📚 Shared References

> [!info]+
> The reference layer connects both workstreams without merging them.
>
> - [[References/MOC|References MOC →]]
> - [[WGBS benchmarking|WGBS benchmarking — callers, metrics, datasets]]
> - DMC/DMR calling methods (DSS, methylKit, dmrseq, BSmooth)
> - Empirical FDR calibration
> - WGBS QC, coverage filters, annotation context

---

## 🧭 Vault Rules

> [!warning]- Architecture (click to expand)
> - **Thesis/Mimosa** and **epykit** are separate workstreams
> - Connect them *only* through shared references, WGBS concepts, statistics, methods, or daily notes
> - Keep project-specific notes inside their own folders
> - Daily notes are the glue — use them for cross-project journaling
