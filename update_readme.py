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

def extract_topic(root):
    rel = os.path.relpath(root, ROOT)
    if rel == ".":
        return "General"
    return "/".join(rel.split(os.sep))

def escape_md(text: str) -> str:
    return text.replace("|", "\\|")

def collect_files_by_topic():
    topics = {}
    for root, _, files in os.walk(ROOT):
        if ".git" in root or ".github" in root:
            continue
        topic = extract_topic(root)
        for file in files:
            if not file.endswith(".java"):
                continue
            path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(path)
            except Exception:
                mtime = 0
            problem, link, notes, level, pattern, revisit = extract_metadata(path)
            entry = {
                "path": path,
                "problem": problem,
                "link": link,
                "notes": notes,
                "level": level,
                "pattern": pattern,
                "revisit": revisit,
                "mtime": mtime,
                "topic": topic
            }
            topics.setdefault(topic, []).append(entry)
    return topics

def generate_table():
    """Generate markdown table for README."""
    topics = collect_files_by_topic()
    if not topics:
        return "No Java files found yet."
    sorted_topics = sorted(topics.keys())
    rows = []
    count = 1

    header = (
        "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n"
        "|---|----------|-----------|--------|-----------------|----------|--------------|"
    )

    for topic in sorted_topics:
        entries = topics[topic]
        entries_sorted = sorted(entries, key=lambda e: e["mtime"], reverse=True)
        rows.append(f"| **{escape_md(topic)} ({len(entries_sorted)})** |  |  |  |  |  |  |")
        for e in entries_sorted:
            path = e["path"].replace('\\', '/')
            github_link = f"[Code]({path})"
            problem_display = f"[{escape_md(e['problem'])}]({e['link']})" if e["link"] else escape_md(e["problem"])
            level_text = e["level"] if e["level"] else "-"
            rows.append(f"| {count} | {problem_display} | {github_link} | {level_text} | {escape_md(e['pattern'])} | {escape_md(e['revisit'])} | {escape_md(e['notes'])} |")
            count += 1
        rows.append("|  |  |  |  |  |  |  |")
    return header + "\n" + "\n".join(rows)

def generate_html():
    topics = collect_files_by_topic()
    sorted_topics = sorted(topics.keys())
    count = 1
    levels_set = set()
    revisits_set = set()

    all_rows_data = []

    for topic in sorted_topics:
        entries = topics[topic]
        entries_sorted = sorted(entries, key=lambda e: e["mtime"], reverse=True)
        for e in entries_sorted:
            path = e["path"].replace('\\', '/')
            problem_cell = f'<a href="{e["link"]}" target="_blank">{escape_md(e["problem"])}</a>' if e["link"] else escape_md(e["problem"])
            code_cell = f'<a href="{path}" target="_blank">Code</a>'
            level = (e["level"] or "").strip()
            levels_set.add(level)
            revisits_set.add(e["revisit"])
            if level.lower() == "easy":
                level_cell = '<span class="level-easy">Easy</span>'
            elif level.lower() == "medium":
                level_cell = '<span class="level-medium">Medium</span>'
            elif level.lower() == "hard":
                level_cell = '<span class="level-hard">Hard</span>'
            else:
                level_cell = escape_md(level) if level else "-"

            all_rows_data.append([
                str(count),
                escape_md(topic),
                problem_cell,
                code_cell,
                level_cell,
                escape_md(e["pattern"]),
                escape_md(e["revisit"]),
                escape_md(e["notes"])
            ])
            count += 1

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>DSA Dashboard</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css'>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 24px; background: #f0f2f5; }}
h1 {{ text-align:center; margin-bottom: 20px; color:#222; }}
.filter-container {{
    display:flex; flex-wrap:wrap; gap:12px; background:white; padding:16px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); margin-bottom:20px;
    align-items:center;
}}
.filter-container label {{ font-weight:bold; margin-right:6px; }}
.filter-container select, .filter-container input[type='text'] {{
    padding:6px 10px; border-radius:6px; border:1px solid #ccc; min-width:150px; transition:0.3s;
}}
.filter-container select:hover, .filter-container input[type='text']:hover {{ border-color:#007bff; }}
table {{ width:100%; border-collapse: collapse; background:white; box-shadow:0 2px 6px rgba(0,0,0,0.1); border-radius:6px; }}
th {{ background:#007bff; color:white; padding:12px; }}
td {{ padding:10px; border-bottom:1px solid #ddd; }}
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

<div class='filter-container'>
<label for='searchInput'>Search:</label>
<input type='text' id='searchInput' placeholder='Search problem, pattern, notes...'/>
<label for='topicFilter'>Topic:</label>
<select id='topicFilter'><option value='All'>All</option>{''.join([f"<option value='{escape_md(t)}'>{escape_md(t)}</option>" for t in sorted_topics])}</select>
<label for='levelFilter'>Level:</label>
<select id='levelFilter'><option value='All'>All</option>{''.join([f"<option value='{escape_md(l)}'>{escape_md(l)}</option>" for l in sorted(levels_set) if l])}</select>
<label for='revisitFilter'>Revisit:</label>
<select id='revisitFilter'><option value='All'>All</option>{''.join([f"<option value='{escape_md(r)}'>{escape_md(r)}</option>" for r in sorted(revisits_set) if r])}</select>
</div>

<table id='problemsTable'>
<thead><tr><th>#</th><th>Topic</th><th>Problem</th><th>Solution</th><th>Level</th><th>Pattern</th><th>Revisit</th><th>Quick Notes</th></tr></thead>
<tbody>
{''.join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td>{r[7]}</td></tr>" for r in all_rows_data])}
</tbody>
</table>

<script src='https://cdn.jsdelivr.net/npm/simple-datatables@latest' defer></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const dt = new simpleDatatables.DataTable("#problemsTable");
    const topicFilter = document.getElementById('topicFilter');
    const levelFilter = document.getElementById('levelFilter');
    const revisitFilter = document.getElementById('revisitFilter');
    const searchInput = document.getElementById('searchInput');

    function applyFilters() {{
        const topicVal = topicFilter.value.toLowerCase();
        const levelVal = levelFilter.value.toLowerCase();
        const revisitVal = revisitFilter.value.toLowerCase();
        const searchVal = searchInput.value.toLowerCase();

        const filteredRows = [];
        dt.data.forEach(row => {{
            const topic = row[1].toLowerCase();
            const level = row[4].toLowerCase();
            const revisit = row[6].toLowerCase();
            const searchText = (row[2] + " " + row[5] + " " + row[7]).toLowerCase();

            if ((topicVal === 'all' || topic.includes(topicVal)) &&
                (levelVal === 'all' || level.includes(levelVal)) &&
                (revisitVal === 'all' || revisit.includes(revisitVal)) &&
                (searchText.includes(searchVal))) {{
                filteredRows.push(row);
            }}
        }});

        dt.rows().remove();
        dt.rows().add(filteredRows);
    }}

    topicFilter.addEventListener('change', applyFilters);
    levelFilter.addEventListener('change', applyFilters);
    revisitFilter.addEventListener('change', applyFilters);
    searchInput.addEventListener('input', applyFilters);
}});
</script>

</body>
</html>"""

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ {HTML_PATH} generated successfully!")

def update_readme():
    table = generate_table()
    dashboard_url = 'https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/'
    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →]({dashboard_url})**

---

Automatically generated list of solved problems (grouped by topic).

{table}
"""
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {README_PATH} updated successfully!")

if __name__ == '__main__':
    update_readme()
    generate_html()
