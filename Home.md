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
const deadline = dv.date("2026-09-01");

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


```dataviewjs
// ── Action Radar ─────────────────────────────────────────────────
const today = dv.date("today");
const nextWeek = today.plus({days: 7});
const nextMonth = today.plus({days: 30});

const allTasks = dv.pages('-".dashboard-backup" and -".smart-env" and -".obsidian"').file.tasks.where(t => !t.completed && t.due);

const overdueToday = allTasks.where(t => t.due <= today).sort(t => t.due);
const thisWeek = allTasks.where(t => t.due > today && t.due <= nextWeek).sort(t => t.due);
const thisMonth = allTasks.where(t => t.due > nextWeek && t.due <= nextMonth).sort(t => t.due);

function getPriority(text) {
  if (text.includes("🔺")) return { level: 1, label: "Highest", color: "var(--dash-hot)" };
  if (text.includes("⏫")) return { level: 2, label: "High", color: "var(--dash-amber)" };
  if (text.includes("🔼")) return { level: 3, label: "Medium", color: "var(--dash-cold)" };
  if (text.includes("🔽") || text.includes("⏬")) return { level: 5, label: "Low", color: "var(--dash-fog)" };
  return { level: 4, label: "Normal", color: "transparent" };
}

function renderTask(t) {
  const prio = getPriority(t.text);
  // Strip out tasks plugin emojis/dates for a cleaner UI
  let cleanText = t.text.replace(/[\u{1F53A}\u{23EB}\u{1F53C}\u{1F53D}\u{23EC}]/gu, "").replace(/📅\s*\d{4}-\d{2}-\d{2}/, "").trim();
  
  const dueStr = t.due.toFormat("MMM d");
  const prioDot = prio.level < 4 ? `<span class="task-prio-dot" style="background: ${prio.color}; box-shadow: 0 0 6px ${prio.color}"></span>` : "";
  
  return `
    <div class="dash-task">
      <div class="dash-task-check"></div>
      <div class="dash-task-body">
        <div class="dash-task-text"><a class="internal-link" href="${t.path}" data-href="${t.path}">${cleanText}</a></div>
        <div class="dash-task-meta">
          ${prioDot} <span style="color:${prio.level < 4 ? prio.color : 'inherit'}" class="task-prio-label">${prio.label !== 'Normal' ? prio.label + ' &middot; ' : ''}</span>
          <span class="dash-task-due">&#128197; ${dueStr}</span>
        </div>
      </div>
    </div>
  `;
}

function renderCol(title, tasks, icon) {
  const html = tasks.length > 0 
    ? tasks.map(t => renderTask(t)).join("")
    : `<div class="dash-task-empty">No upcoming tasks</div>`;
  
  return `
    <div class="dash-task-col">
      <div class="dash-task-col-head">
        <h4 class="dash-task-col-title">${icon} ${title}</h4>
        <span class="dash-task-count">${tasks.length}</span>
      </div>
      <div class="dash-task-list">${html}</div>
    </div>
  `;
}

dv.container.innerHTML = `
  <div class="panel" style="margin-bottom: 1.75rem;">
    <h3 class="panel-title"><span class="panel-icon">&#9889;</span> Action Radar</h3>
    <div class="dash-task-board">
      ${renderCol("Due & Overdue", overdueToday, "&#128680;")}
      ${renderCol("Next 7 Days", thisWeek, "&#128197;")}
      ${renderCol("Later this Month", thisMonth, "&#128198;")}
    </div>
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

```dataviewjs
// ── Momentum Heatmap ─────────────────────────────────────────────
const daysToTrack = 84; // 12 weeks
const today = dv.date("today");
let activity = {};

for (let i = 0; i < daysToTrack; i++) {
  let d = today.minus({days: i}).toFormat("yyyy-MM-dd");
  activity[d] = 0;
}

dv.pages('-".obsidian" and -".smart-env" and -".dashboard-backup"').forEach(p => {
  if (p.file.mtime) {
    let mDate = p.file.mtime.toFormat("yyyy-MM-dd");
    if (activity[mDate] !== undefined) {
      activity[mDate]++;
    }
  }
});

let orderedDays = [];
for (let i = daysToTrack - 1; i >= 0; i--) {
  orderedDays.push(today.minus({days: i}).toFormat("yyyy-MM-dd"));
}

let html = '<div class="dash-heatmap-container"><div class="dash-heatmap-grid">';

orderedDays.forEach(d => {
  let count = activity[d];
  let level = 0;
  if (count > 0) level = 1;
  if (count > 2) level = 2;
  if (count > 5) level = 3;
  if (count > 10) level = 4;
  
  html += `<div class="dash-heatmap-cell" data-level="${level}" title="${d}: ${count} updates"></div>`;
});

html += '</div>';
html += `<div class="dash-heatmap-meta">
  <span>Last 12 weeks</span>
  <div class="dash-heatmap-legend">
    <span>Less</span>
    <div class="dash-heatmap-cell" data-level="0"></div>
    <div class="dash-heatmap-cell" data-level="1"></div>
    <div class="dash-heatmap-cell" data-level="2"></div>
    <div class="dash-heatmap-cell" data-level="3"></div>
    <div class="dash-heatmap-cell" data-level="4"></div>
    <span style="margin-left:4px">More</span>
  </div>
</div></div>`;

dv.container.innerHTML = `
  <div class="panel" style="margin-top: 1.5rem;">
    <h3 class="panel-title"><span class="panel-icon">&#128293;</span> Writing Momentum</h3>
    ${html}
  </div>
`;
```
</div>



<div class="dash-row">
<div class="dash-col">



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
