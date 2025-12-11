import os
import html

ROOT = "dsa"  # Folder with all .java files
README_PATH = "README.md"
HTML_PATH = "index.html"
DASHBOARD_URL = "https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/"

# ---- Extract metadata from Java files ----
def extract_metadata(file_path):
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

# ---- Escape helpers ----
def escape_md(text):
    return text.replace("|", "\\|") if text else ""

def escape_html(text):
    return html.escape(text or "")

# ---- Normalize Yes/No for Level and Revisit ----
def normalize_yes_no(value):
    if not value:
        return ""
    value = value.strip().lower()
    if value in ["yes", "y", "true"]:
        return "Yes"
    elif value in ["no", "n", "false"]:
        return "No"
    elif value in ["easy", "medium", "hard"]:
        return value.title()
    else:
        return value.title()

# ---- Collect all files with metadata ----
def collect_files():
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
            problem, link, notes, level, pattern, revisit = extract_metadata(path)

            level_norm = normalize_yes_no(level)
            revisit_norm = normalize_yes_no(revisit)

            all_entries.append({
                "topic": topic,
                "problem": problem,
                "link": link,
                "notes": notes,
                "level": level_norm,
                "pattern": pattern,
                "revisit": revisit_norm,
                "path": path.replace("\\", "/")
            })
            topics_set.add(topic)
            if level_norm:
                levels_set.add(level_norm)
            if revisit_norm:
                revisits_set.add(revisit_norm)

    # Sort by topic, then by problem
    all_entries.sort(key=lambda x: (x['topic'].lower(), x['problem'].lower()))
    return all_entries, sorted(topics_set), sorted(levels_set), sorted(revisits_set)

# ---- Generate README.md ----
def generate_readme():
    entries, _, _, _ = collect_files()
    if not entries:
        table_content = "No Java files found yet."
    else:
        table_content = ""
        current_topic = ""
        count = 1
        for e in entries:
            if e['topic'] != current_topic:
                current_topic = e['topic']
                table_content += f"\n### {escape_md(current_topic)}\n\n"
                table_content += "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n"
                table_content += "|---|---------|---------|-------|---------|---------|-------------|\n"
                count = 1

            problem_md = f"[{escape_md(e['problem'])}]({escape_md(e['link'])})" if e['link'] else escape_md(e['problem'])
            table_content += f"| {count} | {problem_md} | [Code]({escape_md(e['path'])}) | {escape_md(e['level'])} | {escape_md(e['pattern'])} | {escape_md(e['revisit'])} | {escape_md(e['notes'])} |\n"
            count += 1

    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →]({DASHBOARD_URL})**

Automatically generated list of solved problems, grouped by topic.
{table_content}
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {README_PATH} updated successfully!")

# ---- Generate HTML dashboard ----
def generate_html():
    entries, topics, levels, revisits = collect_files()
    rows_html = ""
    for i, e in enumerate(entries, start=1):
        problem_cell = f'<a href="{escape_html(e["link"])}" target="_blank">{escape_html(e["problem"])}</a>' if e["link"] else escape_html(e["problem"])
        code_cell = f'<a href="{escape_html(e["path"])}" target="_blank">Code</a>'
        level_cell = f'<span class="level-badge">{escape_html(e["level"])}</span>' if e["level"] else "-"
        rows_html += f"<tr><td>{i}</td><td>{escape_html(e['topic'])}</td><td>{problem_cell}</td><td>{code_cell}</td><td>{level_cell}</td><td>{escape_html(e['pattern'])}</td><td>{escape_html(e['revisit'])}</td><td>{escape_html(e['notes'])}</td></tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DSA Dashboard</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f5f7fa; margin:20px; }}
h1 {{ text-align:center; color:#222; margin-bottom:20px; }}
.filter-container {{ display:flex; flex-wrap:wrap; gap:12px; background:white; padding:16px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.08); margin-bottom:20px; align-items:center; }}
.filter-container label {{ font-weight:bold; margin-right:6px; }}
.filter-container select, .filter-container input[type='text'] {{ padding:6px 10px; border-radius:6px; border:1px solid #ccc; min-width:150px; transition:0.3s; }}
.filter-container select:hover, .filter-container input[type='text']:hover {{ border-color:#007bff; }}
.table-wrapper {{ overflow-x:auto; }}
table {{ width:100%; border-collapse: collapse; background:white; box-shadow:0 2px 6px rgba(0,0,0,0.06); border-radius:6px; }}
th {{ background:#007bff; color:white; padding:12px; position:sticky; top:0; z-index:1; }}
td {{ padding:10px; border-bottom:1px solid #ddd; }}
tr:hover {{ background-color:#f1f1f1; }}
.level-badge {{ background:#d4edda; color:#155724; padding:4px 10px; border-radius:4px; font-weight:bold; }}
@media(max-width:768px) {{ .filter-container {{ flex-direction:column; align-items:flex-start; }} }}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>

<div class="filter-container">
<label for="searchInput">Search:</label>
<input type="text" id="searchInput" placeholder="Search problem, pattern, notes..."/>
<label for="topicFilter">Topic:</label>
<select id="topicFilter"><option value="">All</option>{"".join([f"<option value='{escape_html(t)}'>{escape_html(t)}</option>" for t in topics])}</select>
<label for="levelFilter">Level:</label>
<select id="levelFilter"><option value="">All</option>{"".join([f"<option value='{escape_html(l)}'>{escape_html(l)}</option>" for l in levels])}</select>
<label for="revisitFilter">Revisit:</label>
<select id="revisitFilter"><option value="">All</option>{"".join([f"<option value='{escape_html(r)}'>{escape_html(r)}</option>" for r in revisits])}</select>
</div>

<div class="table-wrapper">
<table id="problemsTable">
<thead><tr>
<th>#</th><th>Topic</th><th>Problem</th><th>Solution</th><th>Level</th><th>Pattern</th><th>Revisit</th><th>Quick Notes</th>
</tr></thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {{
    const searchInput = document.getElementById("searchInput");
    const topicFilter = document.getElementById("topicFilter");
    const levelFilter = document.getElementById("levelFilter");
    const revisitFilter = document.getElementById("revisitFilter");
    const table = document.getElementById("problemsTable");
    const rows = Array.from(table.tBodies[0].rows).map(r => {{
        return {{
            row: r,
            topic: r.cells[1].textContent.toLowerCase(),
            level: r.cells[4].textContent.toLowerCase(),
            revisit: r.cells[6].textContent.toLowerCase(),
            text: r.textContent.toLowerCase()
        }};
    }});

    function applyFilters() {{
        const searchText = searchInput.value.toLowerCase();
        const topicValue = topicFilter.value.toLowerCase();
        const levelValue = levelFilter.value.toLowerCase();
        const revisitValue = revisitFilter.value.toLowerCase();

        rows.forEach(r => {{
            const match = 
                (!topicValue || r.topic.includes(topicValue)) &&
                (!levelValue || r.level.includes(levelValue)) &&
                (!revisitValue || r.revisit.includes(revisitValue)) &&
                (!searchText || r.text.includes(searchText));

            r.row.style.display = match ? "" : "none";
        }});
    }}

    searchInput.addEventListener("input", applyFilters);
    topicFilter.addEventListener("change", applyFilters);
    levelFilter.addEventListener("change", applyFilters);
    revisitFilter.addEventListener("change", applyFilters);
}});
</script>

</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ {HTML_PATH} generated successfully!")

# ---- Main ----
if __name__ == "__main__":
    generate_readme()
    generate_html()
