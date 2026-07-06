---
cssclasses:
  - dashboard-home
---

<div class="dash-hero">
<div class="dash-ribbon"></div>

```dataviewjs
const now = new Date();
const h = now.getHours();
const greeting = h < 5 ? "Still up" : h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : h < 22 ? "Good evening" : "Still up";
const dateStr = moment().format("dddd, MMMM D, YYYY");

dv.container.innerHTML = `
  <div class="dash-eyebrow">ACADEMY <span class="dash-eyebrow-dot">·</span> RESEARCH VAULT</div>
  <h1 class="dash-title">${greeting}.</h1>
  <div class="dash-subtitle">${dateStr}</div>
`;
```

</div>

```dataviewjs
// ── Vault stats ────────────────────────────────────────────────
// EDIT ME: set your real submission / milestone date below
const deadline = dv.date("2026-12-01");

const allNotes = dv.pages('-".dashboard-backup" and -".smart-env" and -".obsidian"');
const noteCount = allNotes.length;

const openTasks = dv.pages().file.tasks.where(t => !t.completed);
const dueSoon = openTasks.where(t => t.due && t.due <= dv.date("today").plus({days: 7})).length;
const overdue = openTasks.where(t => t.due && t.due < dv.date("today")).length;

const today = dv.date("today");
const daysLeft = Math.round(deadline.diff(today, "days").days);

const chapterPaths = [
  "Thesis/Thesis_v1/Introduction.md",
  "Thesis/Thesis_v1/Background.md",
  "Thesis/Thesis_v1/System Design & Methods.md",
  "Thesis/Thesis_v1/04_validation1_replication.md",
];
let totalWords = 0;
for (const p of chapterPaths) {
  const text = await dv.io.load(p);
  if (text) totalWords += text.trim().split(/\s+/).filter(Boolean).length;
}

const stats = [
  { label: "Notes in vault", value: noteCount.toLocaleString(), icon: "&#128209;" },
  { label: overdue > 0 ? "Overdue tasks" : "Due within 7 days", value: overdue > 0 ? overdue : dueSoon, icon: "&#9989;", warn: overdue > 0 },
  { label: "Days to submission", value: daysLeft, icon: "&#8987;" },
  { label: "Thesis words drafted", value: totalWords.toLocaleString(), icon: "&#129516;" },
];

dv.container.innerHTML = `
  <div class="stat-grid">
    ${stats.map(s => `
      <div class="stat-card ${s.warn ? "stat-warn" : ""}">
        <div class="stat-icon">${s.icon}</div>
        <div class="stat-value">${s.value}</div>
        <div class="stat-label">${s.label}</div>
      </div>
    `).join("")}
  </div>
`;
```

<div class="dash-row">
<div class="dash-col">

### &#128197; Today

```dataviewjs
const todayStr = dv.date("today").toFormat("yyyy-MM-dd");
const todayPath = `Daily notes/${todayStr}.md`;
const exists = !!dv.page(todayPath);

dv.container.innerHTML = `
  <a class="today-link internal-link" href="${todayPath}" data-href="${todayPath}">
    <span class="today-dot"></span>
    <span class="today-label">${exists ? "Open today&rsquo;s note" : "Create today&rsquo;s note"}</span>
    <span class="today-date">${dv.date("today").toFormat("cccc, LLLL d")}</span>
  </a>
`;
```

```tasks
not done
(due before tomorrow) OR (due today)
sort by due
limit 8
```

</div>
<div class="dash-col">

```dataviewjs
// ── Thesis chapter progress ─────────────────────────────────────
// EDIT ME: adjust target word counts to your own expected chapter length
const chapters = [
  { title: "Introduction", path: "Thesis/Thesis_v1/Introduction.md", target: 6000 },
  { title: "Background", path: "Thesis/Thesis_v1/Background.md", target: 9000 },
  { title: "System Design & Methods", path: "Thesis/Thesis_v1/System Design & Methods.md", target: 14000 },
  { title: "Validation & Replication", path: "Thesis/Thesis_v1/04_validation1_replication.md", target: 9000 },
];

let rows = "";
for (const ch of chapters) {
  const text = await dv.io.load(ch.path);
  const words = text ? text.trim().split(/\s+/).filter(Boolean).length : 0;
  const pct = Math.max(2, Math.min(100, Math.round((words / ch.target) * 100)));
  rows += `
    <div class="progress-item">
      <a class="progress-name internal-link" href="${ch.path}" data-href="${ch.path}">${ch.title}</a>
      <div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>
      <div class="progress-meta">${words.toLocaleString()} / ${ch.target.toLocaleString()} words &middot; ${pct}%</div>
    </div>`;
}

dv.container.innerHTML = `
  <div class="panel">
    <h3 class="panel-title"><span class="panel-icon">&#129516;</span> Thesis progress</h3>
    <div class="progress-list">${rows}</div>
  </div>
`;
```

</div>
</div>

```dataviewjs
// ── Active research ──────────────────────────────────────────────
// EDIT ME: keep status/desc current as work moves along
const projects = [
  {
    name: "Epykit",
    desc: "DMR calling & benchmarking toolkit",
    status: "active",
    links: [
      { label: "README", path: "Epykit/epykit_README.md" },
      { label: "Benchmarks", path: "Epykit/Benchmark Results.md" },
      { label: "FDR analysis", path: "Epykit/fdr_analysis.md" },
      { label: "To-do", path: "Epykit/epykit_todo.md" },
    ],
    touch: "Epykit/epykit_README.md",
  },
  {
    name: "WGBS Benchmarking",
    desc: "Whole-genome bisulfite sequencing pipeline comparison",
    status: "active",
    links: [
      { label: "Notes", path: "WGBS benchmarking.md" },
      { label: "DMR overlap report", path: "dmr_overlap_report.html" },
    ],
    touch: "WGBS benchmarking.md",
  },
  {
    name: "Thesis \u2014 Study C",
    desc: "Replication & validation study",
    status: "in review",
    links: [
      { label: "Method", path: "Thesis/Study C Method.md" },
      { label: "Run comparison", path: "Thesis/run_comparison_report.md" },
      { label: "Run23 evolution", path: "Thesis/Run23 evolution analysis.md" },
    ],
    touch: "Thesis/Study C Method.md",
  },
];

function timeAgo(path) {
  const f = app.vault.getAbstractFileByPath(path);
  return f ? moment(f.stat.mtime).fromNow() : "&mdash;";
}

const cards = projects.map(p => `
  <div class="project-card">
    <div class="project-head">
      <span class="project-name">${p.name}</span>
      <span class="status-pill status-${p.status.replace(/\s+/g, "-")}">${p.status}</span>
    </div>
    <p class="project-desc">${p.desc}</p>
    <div class="project-touched">Last touched ${timeAgo(p.touch)}</div>
    <div class="project-links">
      ${p.links.map(l => `<a class="internal-link" href="${l.path}" data-href="${l.path}">${l.label}</a>`).join("")}
    </div>
  </div>
`).join("");

dv.container.innerHTML = `
  <div class="panel">
    <h3 class="panel-title"><span class="panel-icon">&#129514;</span> Active research</h3>
    <div class="project-grid">${cards}</div>
  </div>
`;
```

<div class="dash-row">
<div class="dash-col">

```dataviewjs
// ── Recent activity ──────────────────────────────────────────────
const pages = dv.pages('-".dashboard-backup" and -".smart-env" and -".obsidian"')
  .where(p => p.file.name !== "Home")
  .sort(p => p.file.mtime, 'desc')
  .limit(6);

const rows = pages.map(p => `
  <a class="activity-item internal-link" href="${p.file.path}" data-href="${p.file.path}">
    <span class="activity-dot"></span>
    <span class="activity-main">
      <span class="activity-name">${p.file.name}</span>
      <span class="activity-folder">${p.file.folder || "Vault root"}</span>
    </span>
    <span class="activity-time">${p.file.mtime.toRelative()}</span>
  </a>
`).join("");

dv.container.innerHTML = `
  <div class="panel">
    <h3 class="panel-title"><span class="panel-icon">&#128336;</span> Recent activity</h3>
    <div class="activity-list">${rows}</div>
  </div>
`;
```

</div>
<div class="dash-col">
<div class="panel">
<h3 class="panel-title"><span class="panel-icon">&#129504;</span> Quick navigation</h3>
<div class="nav-grid">
<a class="nav-card internal-link" href="Thesis/MOC.md" data-href="Thesis/MOC.md"><span class="nav-icon">&#129517;</span><span class="nav-label">Thesis MOC</span></a>
<a class="nav-card internal-link" href="Epykit/MOC.md" data-href="Epykit/MOC.md"><span class="nav-icon">&#129516;</span><span class="nav-label">Epykit MOC</span></a>
<a class="nav-card internal-link" href="References/MOC.md" data-href="References/MOC.md"><span class="nav-icon">&#128218;</span><span class="nav-label">References</span></a>
<a class="nav-card internal-link" href="TODO.md" data-href="TODO.md"><span class="nav-icon">&#9989;</span><span class="nav-label">Master to-do</span></a>
<a class="nav-card internal-link" href="Thesis/Thesis_v1/OUTLINE.md" data-href="Thesis/Thesis_v1/OUTLINE.md"><span class="nav-icon">&#128193;</span><span class="nav-label">Thesis outline</span></a>
<a class="nav-card internal-link" href="Thesis/Whole bunch of skills that Mimosa can use.md" data-href="Thesis/Whole bunch of skills that Mimosa can use.md"><span class="nav-icon">&#129504;</span><span class="nav-label">Skills reference</span></a>
</div>
</div>
</div>
</div>

```dataviewjs
// ── Footer ────────────────────────────────────────────────────────
const tips = [
  "Commit your vault before a big edit \u2014 obsidian-git has your back.",
  "Re-run FDR correction whenever you add new DMR calls before trusting a p-value.",
  "A cluttered outline is a research idea in disguise \u2014 park it in Scratch.md.",
  "Cite as you write. Future you will not remember which paper that number came from.",
  "Benchmark early, benchmark often \u2014 regressions hide quietly in pipelines.",
  "Write the hard paragraph first. Everything after it is easier.",
  "Back up before you refactor Epykit's core functions.",
  "A finished draft beats a perfect outline.",
];
const tip = tips[dv.date("today").ordinal % tips.length];

dv.container.innerHTML = `
  <div class="dash-footer">
    <span class="footer-tip">${tip}</span>
    <span class="footer-meta">Academy &middot; Obsidian research vault</span>
  </div>
`;
```
