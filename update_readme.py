import os

ROOT = "dsa"                     # Folder where all your .java files are
README_PATH = "README.md"
HTML_PATH = "index.html"


def extract_metadata(file_path):
    """Extract metadata (Problem, Link, Notes, Level, Time, Revisit) from Java file comments."""
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


def generate_table():
    """Generate Markdown table for README.md."""
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
                    f"| {count} | {problem_display} | {github_link} |"
                    f" {level} | {pattern} | {revisit} | {notes} |"
                )
                count += 1

    if not rows:
        return "No Java files found yet."

    header = (
        "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n"
        "|---|----------|-----------|--------|-----------------|----------|--------------|"
    )

    return header + "\n" + "\n".join(rows)


def generate_html():
    """Generate interactive HTML dashboard with color-coded difficulty."""
    rows_html = []
    count = 1

    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java"):
                path = os.path.join(root, file)

                problem, link, notes, level, pattern, revisit = extract_metadata(path)

                problem_cell = (
                    f'<a href="{link}" target="_blank">{problem}</a>' if link else problem
                )
                code_cell = f'<a href="{path}" target="_blank">Code</a>'

                # Level color badge
                level_class = ""
                if level.lower() == "easy":
                    level_class = "level-easy"
                elif level.lower() == "medium":
                    level_class = "level-medium"
                elif level.lower() == "hard":
                    level_class = "level-hard"

                level_cell = f'<span class="{level_class}">{level}</span>'

                rows_html.append(
                    f"<tr><td>{count}</td>"
                    f"<td>{problem_cell}</td>"
                    f"<td>{code_cell}</td>"
                    f"<td>{level_cell}</td>"
                    f"<td>{pattern}</td>"
                    f"<td>{revisit}</td>"
                    f"<td>{notes}</td></tr>"
                )
                count += 1

    # ---------- HTML CONTENT ----------
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
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
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  border-radius: 6px;
}}
th {{
  background: #007bff;
  color: white;
  padding: 10px;
}}
td {{
  padding: 8px;
  border-bottom: 1px solid #ddd;
}}
tr:hover {{
  background-color: #f1f1f1;
}}
.level-easy {{
  background: #d4edda;
  color: #155724;
  padding: 4px 8px;
  border-radius: 4px;
}}
.level-medium {{
  background: #fff3cd;
  color: #856404;
  padding: 4px 8px;
  border-radius: 4px;
}}
.level-hard {{
  background: #f8d7da;
  color: #721c24;
  padding: 4px 8px;
  border-radius: 4px;
}}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>

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
  const table = document.querySelector("#problemsTable");
  new simpleDatatables.DataTable(table);
}});
</script>

</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ index.html (Dashboard) generated successfully!")


def update_readme():
    """Generate README.md with table and dashboard link."""
    table = generate_table()
    dashboard_url = "https://akashkhairnar.github.io/Logicmojo-DSA-Course-Oct25-akashK/"

    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →]({dashboard_url})**

---

Automatically generated list of solved problems.

{table}
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README.md updated successfully!")


if __name__ == "__main__":
    update_readme()
    generate_html()
