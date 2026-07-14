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
concrete failures documented in  — the same input yielding results that differ by orders of
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
