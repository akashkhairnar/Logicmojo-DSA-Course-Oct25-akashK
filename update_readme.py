import os

ROOT = "dsa"  # folder where all your .java files are
README_PATH = "README.md"
HTML_PATH = "index.html"

def extract_metadata(file_path):
    """Extract metadata (Problem, Link, Notes, Level, Time, Revisit) from Java file comments"""
    problem = "-"
    link = ""
    notes = "-"
    level = "-"
    time_complexity = "-"
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
                elif line.startswith("// TimeComplexity:"):
                    time_complexity = line.replace("// TimeComplexity:", "").strip()
                elif line.startswith("// Revisit:"):
                    revisit = line.replace("// Revisit:", "").strip()
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")

    return problem, link, notes, level, time_complexity, revisit


def generate_table():
    """Generate Markdown table for README.md"""
    rows = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java") and ".git" not in root and ".github" not in root:
                path = os.path.join(root, file)
                github_link = f"[Code]({path})"
                problem, link, notes, level, time_complexity, revisit = extract_metadata(path)
                problem_display = f"[{problem}]({link})" if link else problem
                rows.append(f"| {count} | {problem_display} | {github_link} | {level} | {time_complexity} | {revisit} | {notes} |")
                count += 1

    if not rows:
        return "No Java files found yet."

    header = "| # | Problem | Solution | Level | Time Complexity | Revisit | Quick Notes |\n|---|----------|-----------|--------|-----------------|----------|--------------|"
    return header + "\n" + "\n".join(rows)


def generate_html():
    """Generate interactive HTML dashboard"""
    rows_html = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java"):
                path = os.path.join(root, file)
                problem, link, notes, level, time_complexity, revisit = extract_metadata(path)
                problem_cell = f'<a href="{link}" target="_blank">{problem}</a>' if link else problem
                code_cell = f'<a href="{path}" target="_blank">Code</a>'
                rows_html.append(
                    f"<tr><td>{count}</td><td>{problem_cell}</td><td>{code_cell}</td><td>{level}</td>"
                    f"<td>{time_complexity}</td><td>{revisit}</td><td>{notes}</td></tr>"
                )
                count += 1

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
}}
th, td {{
  text-align: left;
  padding: 8px;
}}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>

<div style="text-align:center;">
  <label>Filter by Level:</label>
  <select id="levelFilter">
    <option value="">All</option>
    <option value="Easy">Easy</option>
    <option value="Medium">Medium</option>
    <option value="Hard">Hard</option>
  </select>

  <label>Filter by Revisit:</label>
  <select id="revisitFilter">
    <option value="">All</option>
    <option value="Yes">Yes</option>
    <option value="No">No</option>
  </select>
</div>

<table id="problemsTable" class="datatable">
  <thead>
    <tr>
      <th>#</th>
      <th>Problem</th>
      <th>Solution</th>
      <th>Level</th>
      <th>Time Complexity</th>
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
  const dataTable = new simpleDatatables.DataTable("#problemsTable");
  const levelFilter = document.getElementById("levelFilter");
  const revisitFilter = document.getElementById("revisitFilter");

  function applyFilters() {{
    dataTable.rows().show();
    const levelVal = levelFilter.value;
    const revisitVal = revisitFilter.value;

    dataTable.rows().each((row) => {{
      const level = row.cells[3].innerText.trim();
      const revisit = row.cells[5].innerText.trim();

      if ((levelVal && level !== levelVal) || (revisitVal && revisit !== revisitVal)) {{
        row.style.display = "none";
      }}
    }});
  }}

  levelFilter.addEventListener("change", applyFilters);
  revisitFilter.addEventListener("change", applyFilters);
}});
</script>

</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html (Dashboard) generated successfully!")


def update_readme():
    """Generate README.md with a dashboard link"""
    table = generate_table()
    dashboard_url = "https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/"
    content = f"""# 🚀 DSA in Java


   📊 **[View Interactive Dashboard →]({dashboard_url})**
   _Filter by Level, Time Complexity, and Revisit status interactively!_

   ---

   Automatically generated table of solved problems.

   {table}
   """
       with open(README_PATH, "w", encoding="utf-8") as f:
           f.write(content)
       print("✅ README.md updated successfully!")


if __name__ == "__main__":
    update_readme()
    generate_html()
