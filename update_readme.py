import os
from pathlib import Path

ROOT = "dsa"                     # Folder where all your .java files
README_PATH = "README.md"
HTML_PATH = "index.html"

def extract_metadata(file_path):
    """Extract metadata from Java file comments."""
    problem = "-"
    link = ""
    notes = "-"
    level = "-"
    pattern = "-"
    revisit = "-"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("// Problem:"):
                    problem = line.replace("// Problem:", "").strip()
                elif line.startswith("// Link:"):
                    link = line.replace("// Link:", "").strip()
                elif line.startswith("// Notes:"):
                    notes = line.replace("// Notes:", "").strip()
                elif line.startswith("// Level:"):
                    level = line.replace("// Level:", "").strip()
                elif line.startswith("// Pattern:"):
                    pattern = line.replace("// Pattern:", "").strip()
                elif line.startswith("// Revisit:"):
                    revisit = line.replace("// Revisit:", "").strip()
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    return problem, link, notes, level, pattern, revisit

def escape_md(text: str) -> str:
    """Escape pipes in markdown."""
    return text.replace("|", "\\|")

def collect_files():
    """Collect all Java files and metadata."""
    all_entries = []
    topics_set = set()
    levels_set = set()
    revisits_set = set()
    for root, _, files in os.walk(ROOT):
        if ".git" in root or ".github" in root:
            continue
        topic = os.path.relpath(root, ROOT)
        if topic == ".":
            topic = "General"
        for file in files:
            if not file.endswith(".java"):
                continue
            path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(path)
            except Exception:
                mtime = 0
            problem, link, notes, level, pattern, revisit = extract_metadata(path)
            all_entries.append({
                "topic": topic,
                "problem": problem,
                "link": link,
                "notes": notes,
                "level": level,
                "pattern": pattern,
                "revisit": revisit,
                "path": path.replace("\\", "/"),
                "mtime": mtime
            })
            topics_set.add(topic)
            if level:
                levels_set.add(level)
            if revisit:
                revisits_set.add(revisit)
    return all_entries, sorted(topics_set), sorted(levels_set), sorted(revisits_set)

def generate_html():
    entries, topics, levels, revisits = collect_files()
    # sort entries by mtime descending
    entries.sort(key=lambda x: x["mtime"], reverse=True)

    rows_html = ""
    count = 1
    for e in entries:
        problem_cell = f'<a href="{e["link"]}" target="_blank">{escape_md(e["problem"])}</a>' if e["link"] else escape_md(e["problem"])
        code_cell = f'<a href="{e["path"]}" target="_blank">Code</a>'
        level_lower = (e["level"] or "").lower()
        if level_lower == "easy":
            level_cell = '<span class="level-easy">Easy</span>'
        elif level_lower == "medium":
            level_cell = '<span class="level-medium">Medium</span>'
        elif level_lower == "hard":
            level_cell = '<span class="level-hard">Hard</span>'
        else:
            level_cell = escape_md(e["level"]) if e["level"] else "-"
        rows_html += f"<tr><td>{count}</td><td>{escape_md(e['topic'])}</td><td>{problem_cell}</td><td>{code_cell}</td><td>{level_cell}</td><td>{escape_md(e['pattern'])}</td><td>{escape_md(e['revisit'])}</td><td>{escape_md(e['notes'])}</td></tr>\n"
        count += 1

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DSA Dashboard</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css">
<style>
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background:#f5f7fa; margin:20px;
}}
h1 {{
    text-align:center; color:#222; margin-bottom:20px;
}}
.filter-container {{
    display:flex; flex-wrap:wrap; gap:12px; background:white; padding:16px;
    border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.08); margin-bottom:20px; align-items:center;
}}
.filter-container label {{ font-weight:bold; margin-right:6px; }}
.filter-container select, .filter-container input[type='text'] {{
    padding:6px 10px; border-radius:6px; border:1px solid #ccc; min-width:150px; transition:0.3s;
}}
.filter-container select:hover, .filter-container input[type='text']:hover {{ border-color:#007bff; }}
table {{
    width:100%; border-collapse: collapse; background:white; box-shadow:0 2px 6px rgba(0,0,0,0.06); border-radius:6px;
}}
th {{
    background:#007bff; color:white; padding:12px;
}}
td {{
    padding:10px; border-bottom:1px solid #ddd;
}}
tr:hover {{ background-color:#f1f1f1; }}
.level-easy {{ background:#d4edda; color:#155724; padding:4px 10px; border-radius:4px; font-weight:bold; }}
.level-medium {{ background:#fff3cd; color:#856404; padding:4px 10px; border-radius:4px; font-weight:bold; }}
.level-hard {{ background:#f8d7da; color:#721c24; padding:4px 10px; border-radius:4px; font-weight:bold; }}
@media(max-width:768px) {{
    .filter-container {{ flex-direction:column; align-items:flex-start; }}
}}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>

<div class="filter-container">
<label for="searchInput">Search:</label>
<input type="text" id="searchInput" placeholder="Search problem, pattern, notes..."/>
<label for="topicFilter">Topic:</label>
<select id="topicFilter"><option value="">All</option>{''.join([f"<option value='{escape_md(t)}'>{escape_md(t)}</option>" for t in topics])}</select>
<label for="levelFilter">Level:</label>
<select id="levelFilter"><option value="">All</option>{''.join([f"<option value='{escape_md(l)}'>{escape_md(l)}</option>" for l in levels])}</select>
<label for="revisitFilter">Revisit:</label>
<select id="revisitFilter"><option value="">All</option>{''.join([f"<option value='{escape_md(r)}'>{escape_md(r)}</option>" for r in revisits])}</select>
</div>

<table id="problemsTable">
<thead><tr>
<th>#</th><th>Topic</th><th>Problem</th><th>Solution</th><th>Level</th><th>Pattern</th><th>Revisit</th><th>Quick Notes</th>
</tr></thead>
<tbody>
{rows_html}
</tbody>
</table>

<script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" defer></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const dt = new simpleDatatables.DataTable("#problemsTable");

    const topicFilter = document.getElementById("topicFilter");
    const levelFilter = document.getElementById("levelFilter");
    const revisitFilter = document.getElementById("revisitFilter");
    const searchInput = document.getElementById("searchInput");

    function applyFilters() {{
        const topicVal = topicFilter.value.toLowerCase();
        const levelVal = levelFilter.value.toLowerCase();
        const revisitVal = revisitFilter.value.toLowerCase();
        const searchVal = searchInput.value.toLowerCase();

        dt.rows().forEach(row => {{
            const rowTopic = row.cells[1].textContent.toLowerCase();
            const rowLevel = row.cells[4].textContent.toLowerCase();
            const rowRevisit = row.cells[6].textContent.toLowerCase();
            const rowText = (row.cells[2].textContent + " " + row.cells[5].textContent + " " + row.cells[7].textContent).toLowerCase();
            if ((topicVal === "" || rowTopic.includes(topicVal)) &&
                (levelVal === "" || rowLevel.includes(levelVal)) &&
                (revisitVal === "" || rowRevisit.includes(revisitVal)) &&
                (rowText.includes(searchVal))) {{
                row.show();
            }} else {{
                row.hide();
            }}
        }});
    }}

    topicFilter.addEventListener("change", applyFilters);
    levelFilter.addEventListener("change", applyFilters);
    revisitFilter.addEventListener("change", applyFilters);
    searchInput.addEventListener("input", applyFilters);
}});
</script>

</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ {HTML_PATH} generated successfully!")

def update_readme():
    entries, topics, levels, revisits = collect_files()
    entries.sort(key=lambda x: x["mtime"], reverse=True)
    rows = []
    count = 1
    for e in entries:
        problem_display = f"[{escape_md(e['problem'])}]({e['link']})" if e["link"] else escape_md(e['problem'])
        code_link = f"[Code]({e['path']})"
        rows.append(f"| {count} | {problem_display} | {code_link} | {e['level'] or '-'} | {escape_md(e['pattern'])} | {escape_md(e['revisit'])} | {escape_md(e['notes'])} |")
        count += 1

    table_md = "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n|---|----------|-----------|--------|-----------------|----------|--------------|\n" + "\n".join(rows)
    dashboard_url = "https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/"
    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →]({dashboard_url})**

---

Automatically generated list of solved problems.

{table_md}
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {README_PATH} updated successfully!")

if __name__ == "__main__":
    update_readme()
    generate_html()
