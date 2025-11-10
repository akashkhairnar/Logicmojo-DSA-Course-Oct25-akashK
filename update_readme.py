import os
import json
from datetime import datetime

ROOT = "dsa"  # root folder for your DSA problems


def extract_metadata(file_path):
    """Extract Problem, Level, Revisit, Notes from the first few comment lines."""
    problem = level = revisit = notes = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("// Problem:"):
                    problem = line.replace("// Problem:", "").strip()
                elif line.startswith("// Level:"):
                    level = line.replace("// Level:", "").strip()
                elif line.startswith("// Revisit:"):
                    revisit = line.replace("// Revisit:", "").strip()
                elif line.startswith("// Notes:"):
                    notes = line.replace("// Notes:", "").strip()
                if problem and level and revisit and notes:
                    break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return problem, level, revisit, notes


def generate_html():
    """Generate interactive HTML dashboard with filtering and editing support."""
    rows_html = []
    count = 1
    type_set = set()

    for root, _, files in os.walk(ROOT):
        for file in files:
            if not file.endswith(".java"):
                continue
            file_path = os.path.join(root, file)
            problem, level, revisit, notes = extract_metadata(file_path)

            # infer type from folder (like dsa/array/, dsa/linkedlist/, etc.)
            rel_path = os.path.relpath(file_path, ROOT)
            type_name = rel_path.split(os.sep)[0] if os.sep in rel_path else "General"
            type_set.add(type_name)

            pattern = file.replace(".java", "")
            code_link = f"{file_path}"

            rows_html.append(
                f"<tr data-level='{level.lower()}' data-revisit='{revisit.lower()}' data-type='{type_name.lower()}'>"
                f"<td>{count}</td>"
                f"<td>{type_name}</td>"
                f"<td><a href='{code_link}' target='_blank'>{problem or pattern}</a></td>"
                f"<td contenteditable='true' class='editable level'>{level}</td>"
                f"<td>{pattern}</td>"
                f"<td contenteditable='true' class='editable revisit'>{revisit}</td>"
                f"<td contenteditable='true' class='editable notes'>{notes}</td>"
                f"</tr>"
            )
            count += 1

    type_options_html = "".join(f"<option value='{t}'>{t.title()}</option>" for t in sorted(type_set))

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>DSA Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f8f9fa;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
                border-radius: 8px;
                overflow: hidden;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }}
            th {{
                background: #343a40;
                color: white;
            }}
            tr:nth-child(even) {{ background: #f2f2f2; }}
            tr:hover {{ background-color: #e8f0fe; }}
            select {{
                padding: 5px;
                margin-right: 10px;
            }}
            .editable {{
                background-color: #fff9c4;
                cursor: text;
            }}
            #saveChanges {{
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }}
            #saveChanges:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <h2>📘 DSA Dashboard</h2>
        <div>
            <label>Filter by Level:</label>
            <select id="levelFilter">
                <option value="all">All</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>

            <label>Filter by Revisit:</label>
            <select id="revisitFilter">
                <option value="all">All</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select>

            <label>Filter by Type:</label>
            <select id="typeFilter">
                <option value="all">All</option>
                {type_options_html}
            </select>
        </div>

        <table id="problemsTable">
            <thead>
                <tr>
                    <th style="width:5%;">#</th>
                    <th style="width:10%;">Type</th>
                    <th style="width:25%;">Problem</th>
                    <th style="width:15%;">Level</th>
                    <th style="width:15%;">Pattern</th>
                    <th style="width:10%;">Revisit</th>
                    <th style="width:20%;">Notes</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>

        <div style="text-align:center; margin-top:20px;">
            <button id="saveChanges">💾 Save Changes</button>
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
                const matchesLevel = (levelVal === "all" || row.dataset.level === levelVal);
                const matchesRevisit = (revisitVal === "all" || row.dataset.revisit === revisitVal);
                const matchesType = (typeVal === "all" || row.dataset.type === typeVal);
                row.style.display = (matchesLevel && matchesRevisit && matchesType) ? "" : "none";
            }});
        }}

        [levelFilter, revisitFilter, typeFilter].forEach(f => f.addEventListener("change", applyFilters));

        document.getElementById("saveChanges").addEventListener("click", () => {{
            const updates = [];
            document.querySelectorAll("#problemsTable tbody tr").forEach(row => {{
                const link = row.querySelector("td:nth-child(3) a");
                if (!link) return;
                const path = link.getAttribute("href");
                const level = row.querySelector(".level").textContent.trim();
                const revisit = row.querySelector(".revisit").textContent.trim();
                const notes = row.querySelector(".notes").textContent.trim();

                updates.push({{ path, level, revisit, notes }});
            }});

            const blob = new Blob([JSON.stringify(updates, null, 2)], {{ type: "application/json" }});
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "updates.json";
            a.click();
        }});
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ HTML dashboard generated successfully: index.html")


def apply_updates():
    """Apply updates from updates.json to Java files (comment headers)."""
    if not os.path.exists("updates.json"):
        print("No updates.json found — skipping.")
        return

    with open("updates.json", "r", encoding="utf-8") as f:
        updates = json.load(f)

    for update in updates:
        file_path = update["path"]
        level = update["level"]
        revisit = update["revisit"]
        notes = update["notes"]

        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("// Level:"):
                    line = f"// Level: {level}\n"
                elif line.startswith("// Revisit:"):
                    line = f"// Revisit: {revisit}\n"
                elif line.startswith("// Notes:"):
                    line = f"// Notes: {notes}\n"
                lines.append(line)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✅ Updated: {file_path}")

    os.remove("updates.json")
    print("🧹 Removed updates.json after applying changes.")


if __name__ == "__main__":
    apply_updates()
    generate_html()
