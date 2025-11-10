import os

ROOT = "dsa"  # Folder containing your Java files
README_PATH = "README.md"
HTML_PATH = "index.html"

# -----------------------------
# 1️⃣ Extract metadata
# -----------------------------
def extract_metadata(file_path):
    """Extract metadata (Problem, Link, Notes, Level, Time, Revisit) from Java file comments"""
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


# -----------------------------
# 2️⃣ Generate Markdown Table (for README)
# -----------------------------
def generate_table():
    """Generate Markdown table for README.md"""
    rows = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java") and ".git" not in root and ".github" not in root:
                path = os.path.join(root, file)
                github_link = f"[Code]({path})"
                problem, link, notes, level, pattern, revisit = extract_metadata(path)
                problem_display = f"[{problem}]({link})" if link else problem
                rows.append(
                    f"| {count} | {problem_display} | {github_link} | {level} | {pattern} | {revisit} | {notes} |"
                )
                count += 1

    if not rows:
        return "No Java files found yet."

    header = "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n|---|----------|-----------|--------|-----------------|----------|--------------|"
    return header + "\n" + "\n".join(rows)


# -----------------------------
# 3️⃣ Generate HTML Dashboard
# -----------------------------
def generate_html():
    rows_html = []
    count = 1
    type_set = set()

    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java"):
                relative_path = os.path.relpath(root, ROOT)
                problem_type = relative_path.split(os.sep)[0] if relative_path != "." else "general"
                type_set.add(problem_type)

                path = os.path.join(root, file)
                problem, link, notes, level, pattern, revisit = extract_metadata(path)
                problem_cell = f'<a href="{link}" target="_blank">{problem}</a>' if link else problem
                code_cell = f'<a href="{path}" target="_blank">Code</a>'

                level_class = ""
                if level.lower() == "easy":
                    level_class = "level-easy"
                elif level.lower() == "medium":
                    level_class = "level-medium"
                elif level.lower() == "hard":
                    level_class = "level-hard"

                level_cell = f'<span class="{level_class}">{level}</span>'

                rows_html.append(
                    f"<tr data-type='{problem_type}' data-level='{level.lower()}' data-revisit='{revisit.lower()}'>"
                    f"<td>{count}</td><td>{problem_cell}</td><td>{code_cell}</td>"
                    f"<td>{level_cell}</td><td>{pattern}</td><td>{revisit}</td><td>{notes}</td></tr>"
                )
                count += 1

    if not type_set:
        type_set.add("general")

    type_options_html = "\n".join([f'<option value="{t}">{t.capitalize()}</option>' for t in sorted(type_set)])

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DSA Dashboard</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css">
<style>
body {{
  font-family: Arial, sans-serif;
  margin: 40px;
  background: #f8f9fa;
}}
h1 {{
  text-align: center;
  color: #333;
}}
select {{
  margin: 10px;
  padding: 5px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  border-radius: 6px;
  overflow: hidden;
}}
th:nth-child(1), td:nth-child(1) {{ width: 5%; }}
th:nth-child(2), td:nth-child(2) {{ width: 20%; }}
th:nth-child(3), td:nth-child(3) {{ width: 8%; }}
th:nth-child(4), td:nth-child(4) {{ width: 8%; }}
th:nth-child(5), td:nth-child(5) {{ width: 20%; }}
th:nth-child(6), td:nth-child(6) {{ width: 8%; }}
th:nth-child(7), td:nth-child(7) {{ width: 26%; }}
th, td {{
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  word-wrap: break-word;
}}
th {{
  background: #007bff;
  color: white;
  font-weight: bold;
  position: sticky;
  top: 0;
}}
tbody tr:hover {{
  background-color: #f1f1f1;
}}
.level-easy {{
  background: #d4edda;
  color: #155724;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}}
.level-medium {{
  background: #fff3cd;
  color: #856404;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}}
.level-hard {{
  background: #f8d7da;
  color: #721c24;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>

<div style="text-align:center;">
  <label>Filter by Type:</label>
  <select id="typeFilter">
    <option value="">All</option>
    {type_options_html}
  </select>

  <label>Filter by Level:</label>
  <select id="levelFilter">
    <option value="">All</option>
    <option value="easy">Easy</option>
    <option value="medium">Medium</option>
    <option value="hard">Hard</option>
  </select>

  <label>Filter by Revisit:</label>
  <select id="revisitFilter">
    <option value="">All</option>
    <option value="yes">Yes</option>
    <option value="no">No</option>
  </select>
</div>

<table id="problemsTable" class="datatable">
  <thead>
    <tr>
      <th>#</th>
      <th>Problem</th>
      <th>Solution</th>
      <th>Level</th>
      <th>Pattern</th>
      <th>Revisit</th>
      <th>Quick Notes</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows_html)}
  </tbody>
</table>

<script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" defer></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  const typeFilter = document.getElementById("typeFilter");
  const levelFilter = document.getElementById("levelFilter");
  const revisitFilter = document.getElementById("revisitFilter");
  const table = document.querySelector("#problemsTable");
  const dataTable = new simpleDatatables.DataTable(table);

  function applyFilters() {{
    const typeVal = (typeFilter.value || "").toLowerCase();
    const levelVal = (levelFilter.value || "").toLowerCase();
    const revisitVal = (revisitFilter.value || "").toLowerCase();

    // Loop through all table rows
    table.querySelectorAll("tbody tr").forEach(row => {{
      const rowType = row.getAttribute("data-type") || "";
      const rowLevel = row.getAttribute("data-level") || "";
      const rowRevisit = row.getAttribute("data-revisit") || "";

      const matchType = !typeVal || rowType === typeVal;
      const matchLevel = !levelVal || rowLevel === levelVal;
      const matchRevisit = !revisitVal || rowRevisit === revisitVal;

      row.style.display = (matchType && matchLevel && matchRevisit) ? "" : "none";
    }});
  }}

  [typeFilter, levelFilter, revisitFilter].forEach(f => f.addEventListener("change", applyFilters));
}});
</script>

</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html generated — type, level, and revisit filters all working!")

# -----------------------------
# 4️⃣ Update README
# -----------------------------
def update_readme():
    """Generate README.md with a dashboard link"""
    table = generate_table()
    dashboard_url = "https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/"
    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →]({dashboard_url})**
_Filter by Level, Pattern, and Revisit status interactively!_

---

Automatically generated table of solved problems.

{table}
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md updated successfully!")


# -----------------------------
# 5️⃣ Main
# -----------------------------
if __name__ == "__main__":
    update_readme()
    generate_html()
