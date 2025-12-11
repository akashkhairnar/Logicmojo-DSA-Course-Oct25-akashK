import os
import html

ROOT = "dsa"                     # Folder where all your .java files
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

def escape_html(text):
    return html.escape(text or "")

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
            })
            topics_set.add(topic)
            if level:
                levels_set.add(level)
            if revisit:
                revisits_set.add(revisit)
    return all_entries, sorted(topics_set), sorted(levels_set), sorted(revisits_set)

def generate_html():
    entries, topics, levels, revisits = collect_files()

    rows_html = ""
    for i, e in enumerate(entries, start=1):
        problem_cell = f'<a href="{escape_html(e["link"])}" target="_blank">{escape_html(e["problem"])}</a>' if e["link"] else escape_html(e["problem"])
        code_cell = f'<a href="{escape_html(e["path"])}" target="_blank">Code</a>'
        level_lower = (e["level"] or "").lower()
        if level_lower == "easy":
            level_cell = '<span class="level-easy">Easy</span>'
        elif level_lower == "medium":
            level_cell = '<span class="level-medium">Medium</span>'
        elif level_lower == "hard":
            level_cell = '<span class="level-hard">Hard</span>'
        else:
            level_cell = escape_html(e["level"]) if e["level"] else "-"
        rows_html += f"<tr><td>{i}</td><td>{escape_html(e['topic'])}</td><td>{problem_cell}</td><td>{code_cell}</td><td>{level_cell}</td><td>{escape_html(e['pattern'])}</td><td>{escape_html(e['revisit'])}</td><td>{escape_html(e['notes'])}</td></tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DSA Dashboard</title>
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
<select id="topicFilter"><option value="">All</option>{''.join([f"<option value='{escape_html(t)}'>{escape_html(t)}</option>" for t in topics])}</select>
<label for="levelFilter">Level:</label>
<select id="levelFilter"><option value="">All</option>{''.join([f"<option value='{escape_html(l)}'>{escape_html(l)}</option>" for l in levels])}</select>
<label for="revisitFilter">Revisit:</label>
<select id="revisitFilter"><option value="">All</option>{''.join([f"<option value='{escape_html(r)}'>{escape_html(r)}</option>" for r in revisits])}</select>
</div>

<table id="problemsTable">
<thead><tr>
<th>#</th><th>Topic</th><th>Problem</th><th>Solution</th><th>Level</th><th>Pattern</th><th>Revisit</th><th>Quick Notes</th>
</tr></thead>
<tbody>
{rows_html}
</tbody>
</table>

<script>
document.addEventListener('DOMContentLoaded', function() {{
    const searchInput = document.getElementById("searchInput");
    const topicFilter = document.getElementById("topicFilter");
    const levelFilter = document.getElementById("levelFilter");
    const revisitFilter = document.getElementById("revisitFilter");
    const table = document.getElementById("problemsTable");
    const rows = Array.from(table.tBodies[0].rows);

    function applyFilters() {{
        const searchText = searchInput.value.toLowerCase();
        const topicValue = topicFilter.value.toLowerCase();
        const levelValue = levelFilter.value.toLowerCase();
        const revisitValue = revisitFilter.value.toLowerCase();

        rows.forEach(row => {{
            const topic = row.cells[1].textContent.toLowerCase();
            const level = row.cells[4].textContent.toLowerCase();
            const revisit = row.cells[6].textContent.toLowerCase();
            const text = row.textContent.toLowerCase();

            const match = 
                (!topicValue || topic.includes(topicValue)) &&
                (!levelValue || level.includes(levelValue)) &&
                (!revisitValue || revisit.includes(revisitValue)) &&
                (!searchText || text.includes(searchText));

            row.style.display = match ? "" : "none";
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

if __name__ == "__main__":
    generate_html()
