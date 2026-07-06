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
