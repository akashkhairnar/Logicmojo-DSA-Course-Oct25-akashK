import os
import json

ROOT = "dsa"
README_PATH = "README.md"
HTML_PATH = "index.html"

# -----------------------------
# 1️⃣ Extract metadata
# -----------------------------
def extract_metadata(file_path):
    """Extract metadata (Problem, Link, Notes, Level, Pattern, Revisit) from Java file comments"""
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

    header = "| # | Problem | Solution | Level | Pattern | Revisit | Quick Notes |\n|---|----------|-----------|--------|----------|----------|--------------|"
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
                path = os.path.join(root, file)
                problem, link, notes, level, pattern, revisit = extract_metadata(path)
                rel_path = os.path.relpath(path, ROOT)
                type_name = rel_path.split(os.sep)[0] if os.sep in rel_path else "General"
                type_set.add(type_name)

                problem_cell = f'<a href="{link}" target="_blank">{problem}</a>' if link else problem
                code_cell = f'<a href="{path}" target="_blank">Code</a>'

                rows_html.append(
                    f"<tr data-level='{level.lower()}' data-revisit='{revisit.lower()}' data-type='{type_name.lower()}'>"
                    f"<td>{count}</td>"
                    f"<td>{problem_cell}</td>"
                    f"<td>{code_cell}</td>"
                    f"<td>{level}</td>"
                    f"<td>{pattern}</td>"
                    f"<td>{revisit}</td>"
                    f"<td>{notes}</td>"
                    f"</tr>"
                )
                count += 1

    type_options_html = "".join(f"<option value='{t.lower()}'>{t.title()}</option>" for t in sorted(type_set))

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DSA Dashboard</title>
<style>
:root {{
  --bg-color: #f5f6fa;
  --card-bg: #ffffff;
  --border-color: #e0e0e0;
  --text-color: #333;
  --accent: #6c63ff;
}}
body {{
  font-family: "Inter", Arial, sans-serif;
  margin: 40px;
  background: var(--bg-color);
  color: var(--text-color);
}}
h1 {{
  text-align: center;
  font-size: 28px;
  margin-bottom: 25px;
}}
.container {{
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  padding: 25px;
}}
.filters {{
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}}
select {{
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  background: white;
}}
button {{
  padding: 8px 16px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}}
button:hover {{
  background: #554ef0;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
}}
th {{
  background: var(--accent);
  color: white;
  text-align: left;
  padding: 10px;
}}
td {{
  border-bottom: 1px solid var(--border-color);
  padding: 10px;
}}
tr:hover {{
  background: #f2f2ff;
}}
.hidden {{
  display: none;
}}
.editable {{
  background: #fdf8d3;
}}
</style>
</head>
<body>

<h1>📘 DSA Problem Dashboard</h1>
<div class="container">
  <div class="filters">
    <label>Level:</label>
    <select id="levelFilter">
      <option value="">All</option>
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard">Hard</option>
    </select>
    <label>Revisit:</label>
    <select id="revisitFilter">
      <option value="">All</option>
      <option value="yes">Yes</option>
      <option value="no">No</option>
    </select>
    <label>Type:</label>
    <select id="typeFilter">
      <option value="">All</option>
      {type_options_html}
    </select>
    <button id="editBtn">✏️ Edit Mode</button>
    <button id="saveBtn" class="hidden">💾 Save</button>
    <button id="cancelBtn" class="hidden">❌ Cancel</button>
  </div>

  <table id="problemsTable">
    <thead>
      <tr>
        <th style="width:5%;">#</th>
        <th style="width:15%;">Problem</th>
        <th style="width:10%;">Solution</th>
        <th style="width:15%;">Level</th>
        <th style="width:20%;">Pattern</th>
        <th style="width:10%;">Revisit</th>
        <th style="width:25%;">Notes</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows_html)}
    </tbody>
  </table>
</div>

<script>
const levelFilter = document.getElementById("levelFilter");
const revisitFilter = document.getElementById("revisitFilter");
const typeFilter = document.getElementById("typeFilter");

function applyFilters() {{
  const levelVal = levelFilter.value;
  const revisitVal = revisitFilter.value;
  const typeVal = typeFilter.value;
  document.querySelectorAll("#problemsTable tbody tr").forEach(row => {{
    const matchesLevel = !levelVal || row.dataset.level === levelVal;
    const matchesRevisit = !revisitVal || row.dataset.revisit === revisitVal;
    const matchesType = !typeVal || row.dataset.type === typeVal;
    row.style.display = (matchesLevel && matchesRevisit && matchesType) ? "" : "none";
  }});
}}

[levelFilter, revisitFilter, typeFilter].forEach(f => f.addEventListener("change", applyFilters));

const editBtn = document.getElementById("editBtn");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");

editBtn.addEventListener("click", () => {{
  document.querySelectorAll("#problemsTable tbody tr").forEach(row => {{
    row.querySelectorAll("td:nth-child(4), td:nth-child(6), td:nth-child(7)").forEach(td => {{
      td.contentEditable = "true";
      td.classList.add("editable");
    }});
  }});
  editBtn.classList.add("hidden");
  saveBtn.classList.remove("hidden");
  cancelBtn.classList.remove("hidden");
}});

cancelBtn.addEventListener("click", () => {{
  window.location.reload();
}});

saveBtn.addEventListener("click", () => {{
  const updates = [];
  document.querySelectorAll("#problemsTable tbody tr").forEach(row => {{
    const codeLink = row.querySelector("td:nth-child(3) a");
    if (!codeLink) return;
    const path = codeLink.getAttribute("href");
    const level = row.querySelector("td:nth-child(4)").textContent.trim();
    const revisit = row.querySelector("td:nth-child(6)").textContent.trim();
    const notes = row.querySelector("td:nth-child(7)").textContent.trim();
    updates.push({{ path, level, revisit, notes }});
  }});
  const blob = new Blob([JSON.stringify(updates, null, 2)], {{type: "application/json"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "updates.json";
  a.click();
}});
</script>

</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html generated successfully!")


# -----------------------------
# 4️⃣ Apply updates from updates.json
# -----------------------------
def apply_updates():
    if not os.path.exists("updates.json"):
        return
    with open("updates.json", "r", encoding="utf-8") as f:
        updates = json.load(f)
    for upd in updates:
        file_path = upd["path"]
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.startswith("// Level:"):
                line = f"// Level: {upd['level']}\n"
            elif line.startswith("// Revisit:"):
                line = f"// Revisit: {upd['revisit']}\n"
            elif line.startswith("// Notes:"):
                line = f"// Notes: {upd['notes']}\n"
            new_lines.append(line)
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Updated {file_path}")
    os.remove("updates.json")
    print("🧹 Removed updates.json")


# -----------------------------
# 5️⃣ Update README
# -----------------------------
def update_readme():
    table = generate_table()
    content = f"""# 🚀 DSA in Java

📊 **[View Interactive Dashboard →](index.html)**  
_Filter by Level, Type, and Revisit interactively!_

---

{table}
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md updated successfully!")


# -----------------------------
# 6️⃣ Main
# -----------------------------
if __name__ == "__main__":
    apply_updates()
    update_readme()
    generate_html()
