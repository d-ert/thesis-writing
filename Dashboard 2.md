
# 🏠 Dashboard

<span class="dash-date">`= dateformat(date(today), "EEEE, MMMM d, yyyy")`</span>

---

## ⚡ Quick Links



> [!grid-2]
> > [!example] 💼 Work
> > - [[Work/Projects MOC|📋 All Projects]]
> > - [[Work/Meeting Notes|🗣️ Meeting Notes]]
> > - [[Work/Action Items|✅ Action Items]]
>
> > [!abstract] 📚 Study
> > - [[Study/Reading List|📖 Reading List]]
> > - [[Study/Course Notes|🎓 Course Notes]]
> > - [[Study/Research|🔬 Research Hub]]
>
> > [!journal] 📓 Journal
> > - [[Daily notes/`= dateformat(date(today), "yyyy-MM-dd")`|📝 Today's Entry]]
> > - [[Journal/Weekly Review|🗓️ Weekly Review]]
>
> > [!success] 🗂️ References
> > - [[References/MOC|🗺️ Map of Content]]
> > - [[Inbox|📥 Inbox / Unsorted]]



---

## ✅ Tasks

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; margin-bottom:8px;">

> [!todo] Due Today
> ```tasks
> not done
> due today
> sort by priority
> ```

> [!warning] Overdue
> ```tasks
> not done
> due before today
> sort by due
> limit 8
> ```

> [!info] No Due Date
> ```tasks
> not done
> no due date
> sort by priority
> limit 8
> ```

</div>

---

## 🕐 Recent & Stats

<div style="display:grid; grid-template-columns:2fr 1fr; gap:14px;">

> [!note] Recently Modified
> ```dataview
> TABLE file.mtime as "Edited", file.folder as "Folder"
> FROM ""
> WHERE file.name != "Dashboard"
> SORT file.mtime DESC
> LIMIT 10
> ```

> [!tip] Vault by Folder
> ```dataview
> TABLE WITHOUT ID length(rows) as "Notes", key as "Folder"
> FROM ""
> WHERE file.folder != ""
> GROUP BY file.folder
> SORT length(rows) DESC
> LIMIT 8
> ```

</div>
