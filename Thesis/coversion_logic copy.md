### Conversion of GSE263850 BED Files to Bismark Coverage Format

The publicly available **GSE263850** dataset was originally provided as **12-column BED files**, whereas the downstream analysis pipeline required **6-column Bismark `.cov` files**. To enable compatibility, all samples were converted to the Bismark coverage format using a deterministic mapping based on the structure of the original files. 

Inspection of the BED files showed that each row contained strand-specific methylation counts in addition to combined totals. The columns were organized as:

| Columns | Description                                                                   |
| ------- | ----------------------------------------------------------------------------- |
| 1–3     | Chromosome, start, end coordinates                                            |
| 4–6     | Methylated count, total coverage, methylation percentage (strand 1)           |
| 7–9     | Methylated count, total coverage, methylation percentage (strand 2)           |
| 10–12   | Combined methylated count, combined coverage, combined methylation percentage |

The conversion generated standard Bismark coverage files containing the following six fields:

1. Chromosome
2. Genomic position (BED end coordinate, used as both start and end since BED uses 0-based half-open intervals whereas Bismark `.cov` uses 1-based single-base coordinates)
3. Genomic position
4. Methylation percentage
5. Number of methylated reads
6. Number of unmethylated reads, computed as:

[
\text{Unmethylated Reads} = \text{Total Coverage} - \text{Methylated Reads}
]

To ensure that the inferred column mapping was correct, the conversion was performed using a streaming Python script that processed the compressed files without loading them into memory. During conversion, an invariant check was performed for every CpG site:

* Strand-specific methylated counts summed to the reported total methylated count.
* Strand-specific coverage values summed to the reported total coverage.

Across all processed files, **zero invariant mismatches** were detected, confirming that the BED file structure was interpreted correctly and that the conversion preserved the original methylation information. 

The conversion was applied to all six samples in the GSE263850 dataset:

* GSM8200106_Clone16_untreated
* GSM8200107_Clone20_untreated
* GSM8200108_Clone21_untreated
* GSM8200109_SBP009_Untreated_1
* GSM8200110_SBP009_Untreated_2
* GSM8200111_SBP009_Untreated_3

In total, **over 143 million CpG records** were converted into compressed Bismark-compatible `.cov.gz` files. The resulting files occupied approximately **1 GB**, compared with approximately **1.7 GB** for the original BED files, reflecting the removal of redundant strand-specific information while retaining all information required for downstream methylation analyses. 
