---
tags:
  - MOC
  - references
---
# References MOC

Shared literature and methods notes live here. This layer can connect thesis/Mimosa and epykit when they rely on the same WGBS, DMR, annotation, or FDR concepts, without merging the two workstreams.

## Core WGBS References

- [[WGBS benchmarking|WGBS benchmarking]]


## Methods And Concepts

- DMC and DMR calling
- DSS, methylKit, dmrseq, BSmooth, and related callers
- False-discovery-rate calibration and empirical FDR
- WGBS QC metrics, coverage filters, and annotation context

## Used By

- [[Thesis MOC|Thesis / Mimosa]]
- [[Epykit MOC|epykit]]

## Literature (`papers/`)

```dataview
TABLE 
  title as "Title",
  year as "Year",
  choice(read, "✅", "❌") as "Read",
  Relevance as "Relevance to Thesis"
FROM "References/papers"
SORT year DESC
```
