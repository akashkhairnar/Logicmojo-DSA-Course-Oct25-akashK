#!/usr/bin/env python3
"""
dashboard.py

Generates a polished DSA dashboard (index.html) from Java files under the `dsa/` folder.
Supports:
 - Filters: Type (subfolder), Level, Revisit
 - Edit Mode: inline editing for Level, Revisit, Notes (only when Edit Mode is ON)
 - Save Changes -> downloads updates.json (browser). Place updates.json next to this script and re-run to apply edits to Java files.
 - README.md generation (clean markdown table + dashboard link)

Usage:
  python dashboard.py
"""

import os
import json
from datetime import datetime

# === Configuration ===
ROOT = "dsa"                  # root folder containing subfolders of java problems
README_PATH = "README.md"
HTML_PATH = "index.html"
UPDATES_JSON = "updates.json"


# -----------------------------
# Helpers: read/write metadata
# -----------------------------
def extract_metadata(file_path):
    """
    Extract metadata from the top comments of a Java file.
    Returns tuple: (problem_name, level, revisit, notes, pattern_link)
    If a field is missing, returns empty string for that field.
    """
    problem = ""
    level = ""
    revisit = ""
    notes = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # read first 50 lines at most to find comment metadata
            for _ in range(50):
                line = f.readline()
                if not line:
                    break
                s = line.strip()
                if s.startswith("// Problem:"):
                    problem = s.replace("// Problem:", "").strip()
                elif s.startswith("// Level:"):
                    level = s.replace("// Level:", "").strip()
                elif s.startswith("// Revisit:"):
                    revisit = s.replace("// Revisit:", "").strip()
                elif s.startswith("// Notes:"):
                    notes = s.replace("// Notes:", "").strip()
                # stop early if we collected most fields
                if problem and level and revisit and notes:
                    break
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    return problem, level, revisit, notes


def ensure_normalized_type(s):
    """Return normalized type string from a folder name"""
    if not s:
        return "general"
    t = str(s).strip().lower()
    # remove leading/trailing ./ or backslashes if present
    t = t.strip("./\\")
    return t or "general"


# -----------------------------
# Generate README markdown table
# -----------------------------
def generate_table():
    rows = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if not file.endswith(".java"):
                continue
            path = os.path.join(root, file)
            problem, level, revisit, notes = extract_metadata(path)
            problem_display = problem or file.replace(".java", "")
            # create a relative link to the file
            rel_path = os.path.relpath(path)
            github_link = f"[Code]({rel_path})"
            # problem link: if a comment Link field existed it would be used; we keep plain text here
            rows.append((count, problem_display, github_link, level, file.replace(".java", ""), revisit, notes))
            count += 1

    if not rows:
        return "No Java files found yet."

    header = (
        "# 🚀 DSA in Java\n\n"
        "📊 **[Open Interactive Dashboard →](index.html)**  \n"
        "_Filter by Type, Level, and Revisit status interactively._\n\n"
        "| # | Problem | Solution | Level | Pattern | Revisit | Notes |\n"
        "|---:|:--------|:--------:|:-----:|:--------|:-------:|:------|\n"
    )

    lines = [header]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")

    return "\n".join(lines)


# -----------------------------
# Apply updates.json to .java files
# -----------------------------
def apply_updates():
    """
    Look for updates.json in current directory. If present, apply changes to matching .java files.
    updates.json format: list of objects { path: "<file path>", level: "...", revisit: "...", notes: "..." }
    """
    if not os.path.exists(UPDATES_JSON):
        print("No updates.json found — skipping apply_updates.")
        return

    try:
        with open(UPDATES_JSON, "r", encoding="utf-8") as f:
            updates = json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to read {UPDATES_JSON}: {e}")
        return

    if not isinstance(updates, list):
        print("⚠️ updates.json format invalid: expected a list of update objects.")
        return

    for upd in updates:
        path = upd.get("path") or upd.get("file") or upd.get("href")
        level = upd.get("level", "").strip()
        revisit = upd.get("revisit", "").strip()
        notes = upd.get("notes", "").strip()

        if not path:
            print("⚠️ Skipping update with no path:", upd)
            continue

        # Normalize path if it is relative
        file_path = os.path.normpath(path)

        # if path isn't absolute and file exists in repo relative: use as-is
        if not os.path.exists(file_path):
            # try relative to current script directory
            alt = os.path.join(os.getcwd(), path)
            if os.path.exists(alt):
                file_path = alt
            else:
                print(f"⚠️ File not found, skipping: {path}")
                continue

        try:
            with open(file_path, "r", encoding="utf-8") as rf:
                lines = rf.readlines()
        except Exception as e:
            print(f"⚠️ Could not read {file_path}: {e}")
            continue

        # We'll attempt to update comment lines in the top area of the file.
        # Strategy:
        # - Search first 50 lines for "// Level:", "// Revisit:", "// Notes:" and replace them.
        # - If not found, try to insert them right after "// Problem:" line if present.
        # - If still not found, prepend the comment block at top.
        updated_lines = []
        replaced_level = replaced_revisit = replaced_notes = False
        insert_index_after_problem = None

        for idx, line in enumerate(lines[:50]):
            s = line.strip()
            if s.startswith("// Problem:"):
                insert_index_after_problem = idx
            if s.startswith("// Level:") and level:
                lines[idx] = f"// Level: {level}\n"
                replaced_level = True
            if s.startswith("// Revisit:") and revisit:
                lines[idx] = f"// Revisit: {revisit}\n"
                replaced_revisit = True
            if s.startswith("// Notes:") and notes:
                lines[idx] = f"// Notes: {notes}\n"
                replaced_notes = True

        # If any field not replaced, try to insert after Problem line
        insertion_block = []
        if not replaced_level and level:
            insertion_block.append(f"// Level: {level}\n")
        if not replaced_revisit and revisit:
            insertion_block.append(f"// Revisit: {revisit}\n")
        if not replaced_notes and notes:
            insertion_block.append(f"// Notes: {notes}\n")

        if insertion_block:
            if insert_index_after_problem is not None:
                insert_at = insert_index_after_problem + 1
                # insert block at that position
                lines[insert_at:insert_at] = insertion_block
                print(f"Inserted missing metadata into {file_path} after Problem line.")
            else:
                # prepend at top
                lines = insertion_block + ["\n"] + lines
                print(f"Prepended metadata to {file_path} (no Problem line found).")

        # Write back
        try:
            with open(file_path, "w", encoding="utf-8") as wf:
                wf.writelines(lines)
            print(f"✅ Applied updates to: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to write {file_path}: {e}")

    # remove updates.json after applying
    try:
        os.remove(UPDATES_JSON)
        print(f"🧹 Removed {UPDATES_JSON} after applying changes.")
    except Exception:
        pass


# -----------------------------
# Generate the polished index.html
# -----------------------------
def generate_html():
    """
    Build a modern, polished index.html dashboard with:
     - filters (Type, Level, Revisit)
     - Edit Mode (toggle) - editing Level, Revisit, Notes only
     - Save button (downloads updates.json)
    """
    rows_html = []
    type_set = set()
    count = 1

    # walk files and build rows (no visible Type column; type is data-attribute)
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if not file.endswith(".java"):
                continue
            file_path = os.path.join(root, file)
            problem, level, revisit, notes = extract_metadata(file_path)
            # pattern (use filepath stem or folder+filename if desired)
            pattern = file.replace(".java", "")
            # derive type from folder under ROOT
            rel_dir = os.path.relpath(root, ROOT)
            if rel_dir == ".":
                problem_type = "general"
            else:
                problem_type = rel_dir.split(os.sep)[0]
            problem_type = ensure_normalized_type(problem_type)
            type_set.add(problem_type)

            # normalize values for data attributes
            data_level = (level or "").strip().lower()
            data_revisit = (revisit or "").strip().lower()
            data_type = problem_type

            # link to the code file (relative path)
            rel_path = os.path.relpath(file_path)
            problem_label = problem or pattern

            # create a row with data attributes; we DO NOT expose Type as a visible column
            rows_html.append(
                f"<tr data-type='{data_type}' data-level='{data_level}' data-revisit='{data_revisit}' data-path='{rel_path}'>"
                f"<td class='col-idx'>{count}</td>"
                f"<td class='col-problem'>{problem_label}</td>"
                f"<td class='col-solution'><a href='{rel_path}' target='_blank'>Code</a></td>"
                f"<td class='col-level editable-cell'>{level}</td>"
                f"<td class='col-pattern'>{pattern}</td>"
                f"<td class='col-revisit editable-cell'>{revisit}</td>"
                f"<td class='col-notes editable-cell'>{notes}</td>"
                f"</tr>"
            )
            count += 1

    if not type_set:
        type_set.add("general")

    # build type options (cap first letter)
    type_options_html = "\n".join([f"<option value='{t}'>{t.title()}</option>" for t in sorted(type_set)])

    # HTML template with modern neutral styling (purple/indigo accent)
    html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>DSA Dashboard</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #f5f6f8;
  --card: #ffffff;
  --muted: #6b7280;
  --text: #111827;
  --accent: #7c3aed; /* purple-indigo */
  --accent-2: #6d28d9;
  --success: #059669;
  --danger: #dc2626;
  --radius: 10px;
  --shadow: 0 6px 18px rgba(17,24,39,0.06);
}}

* {{ box-sizing: border-box; font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }}
body {{
  background: var(--bg);
  color: var(--text);
  margin: 24px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

.container {{
  max-width: 1200px;
  margin: 0 auto;
}}

.header {{
  display:flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}}

.title {{
  display:flex;
  gap: 12px;
  align-items: center;
}}

.logo {{
  width:46px; height:46px; border-radius:10px;
  background: linear-gradient(135deg,var(--accent),var(--accent-2));
  display:flex; align-items:center; justify-content:center;
  color:white; font-weight:700; box-shadow: var(--shadow);
}}

h1 {{
  font-size: 20px; margin:0;
}}

.controls {{
  display:flex; gap:12px; align-items:center;
}}

.select, .btn {{
  border: 0;
  background: var(--card);
  box-shadow: var(--shadow);
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
}

.select {{
  min-width: 140px;
}}

.filter-row {{
  display:flex;
  gap:12px;
  align-items:center;
  margin-bottom: 12px;
  margin-top: 12px;
}}

.card {{
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 16px;
  overflow: auto;
}}

.table-wrap {{
  width:100%;
  overflow:auto;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  min-width: 900px;
}}

thead th {{
  position: sticky;
  top: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.98));
  color: var(--muted);
  font-size: 13px;
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #eef2f6;
  z-index: 2;
}}

tbody td {{
  padding: 12px;
  border-bottom: 1px solid #f1f4f8;
  font-size: 14px;
  color: var(--text);
  vertical-align: top;
  overflow-wrap: break-word;
}

/* column widths (user requested) */
.col-idx {{ width: 5%; }}
.col-problem {{ width: 15%; font-weight:600; }}
.col-solution {{ width: 8%; text-align:center; }}
.col-level {{ width: 8%; }}
.col-pattern {{ width: 20%; color: var(--muted); }}
.col-revisit {{ width: 8%; }}
.col-notes {{ width: 36%; }}

tr:hover td {{ background: rgba(99,102,241,0.03); }}

a {{
  color: var(--accent-2);
  text-decoration: none;
  font-weight:600;
}}

/* editable cells styling */
.editable-cell {{
  background: linear-gradient(90deg, rgba(124,58,237,0.03), rgba(124,58,237,0.02));
  border-radius: 6px;
  transition: box-shadow .12s ease;
}}
.editable-cell[contenteditable="true"] {{
  outline: 2px solid rgba(124,58,237,0.12);
  background: rgba(124,58,237,0.04);
}}

/* Buttons */
.btn-primary {{
  background: linear-gradient(90deg,var(--accent),var(--accent-2));
  color: white;
}}
.btn-ghost {{
  background: transparent;
  box-shadow: none;
  color: var(--muted);
}}

/* small helpers */
.row-actions {{
  display:flex; gap:8px; align-items:center;
}}
.meta {{
  color: var(--muted);
  font-size: 13px;
}}

/* responsive */
@media (max-width: 900px) {{
  .col-problem {{ width: 30%; }}
  .col-notes {{ width: 30%; }}
  table {{ min-width: 800px; }}
}}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="title">
      <div class="logo">DS</div>
      <div>
        <h1>DSA Problems — Dashboard</h1>
        <div class="meta">Interactive view of problems under <strong>{ROOT}</strong></div>
      </div>
    </div>

    <div class="controls">
      <button id="editToggle" class="btn select">Edit Mode</button>
      <button id="saveBtn" class="btn btn-primary" style="display:none;">💾 Save Changes</button>
      <button id="cancelBtn" class="btn btn-ghost" style="display:none;">✖ Cancel</button>
    </div>
  </div>

  <div class="filter-row">
    <select id="typeFilter" class="select">
      <option value="">All Types</option>
      {type_options_html}
    </select>

    <select id="levelFilter" class="select">
      <option value="">All Levels</option>
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard">Hard</option>
    </select>

    <select id="revisitFilter" class="select">
      <option value="">All Revisit</option>
      <option value="yes">Yes</option>
      <option value="no">No</option>
    </select>

    <div style="flex:1"></div>

    <div class="meta">Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</div>
  </div>

  <div class="card">
    <div class="table-wrap">
      <table id="problemsTable" role="table" aria-label="DSA problems table">
        <thead>
          <tr>
            <th>#</th>
            <th>Problem</th>
            <th>Solution</th>
            <th>Level</th>
            <th>Pattern</th>
            <th>Revisit</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows_html)}
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
/* Client-side behavior:
   - edit mode toggle: enables contenteditable for certain cells (.editable-cell)
   - Save: collects current values and downloads updates.json for the backend to apply
   - Filter: Type / Level / Revisit filter using data-* attributes
*/

const editToggle = document.getElementById('editToggle');
const saveBtn = document.getElementById('saveBtn');
const cancelBtn = document.getElementById('cancelBtn');
const typeFilter = document.getElementById('typeFilter');
const levelFilter = document.getElementById('levelFilter');
const revisitFilter = document.getElementById('revisitFilter');
const table = document.getElementById('problemsTable').querySelector('tbody');

let editMode = false;
let originalState = null;

// Helper: capture snapshot of editable content (so Cancel can revert)
function snapshotEditable() {
  const snap = [];
  table.querySelectorAll('tr').forEach(row => {
    const path = row.dataset.path || row.getAttribute('data-path') || row.getAttribute('data-path');
    const levelCell = row.querySelector('.col-level');
    const revisitCell = row.querySelector('.col-revisit');
    const notesCell = row.querySelector('.col-notes');
    snap.push({
      path: path,
      level: levelCell ? (levelCell.textContent || '').trim() : '',
      revisit: revisitCell ? (revisitCell.textContent || '').trim() : '',
      notes: notesCell ? (notesCell.textContent || '').trim() : ''
    });
  });
  return snap;
}

// Revert from snapshot
function revertFromSnapshot(snap) {
  table.querySelectorAll('tr').forEach(row => {
    const path = row.dataset.path;
    const entry = snap.find(e => e.path === path);
    if (entry) {
      const levelCell = row.querySelector('.col-level');
      const revisitCell = row.querySelector('.col-revisit');
      const notesCell = row.querySelector('.col-notes');
      if (levelCell) levelCell.textContent = entry.level;
      if (revisitCell) revisitCell.textContent = entry.revisit;
      if (notesCell) notesCell.textContent = entry.notes;
    }
  });
}

// Toggle edit mode
editToggle.addEventListener('click', () => {
  editMode = !editMode;
  if (editMode) {
    // enter edit mode
    editToggle.textContent = 'Exit Edit';
    saveBtn.style.display = '';
    cancelBtn.style.display = '';
    // snapshot
    originalState = snapshotEditable();
    // make editable cells contenteditable
    document.querySelectorAll('.editable-cell').forEach(cell => {
      cell.setAttribute('contenteditable', 'true');
      cell.classList.add('active-edit');
    });
  } else {
    // exit edit mode (without saving)
    editToggle.textContent = 'Edit Mode';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
    document.querySelectorAll('.editable-cell').forEach(cell => {
      cell.removeAttribute('contenteditable');
      cell.classList.remove('active-edit');
    });
    originalState = null;
  }
});

// Cancel edits -> revert
cancelBtn.addEventListener('click', () => {
  if (originalState) {
    revertFromSnapshot(originalState);
  }
  // exit edit mode
  editMode = false;
  editToggle.textContent = 'Edit Mode';
  saveBtn.style.display = 'none';
  cancelBtn.style.display = 'none';
  document.querySelectorAll('.editable-cell').forEach(cell => {
    cell.removeAttribute('contenteditable');
    cell.classList.remove('active-edit');
  });
});

// Build updates JSON and download
saveBtn.addEventListener('click', () => {
  const updates = [];
  table.querySelectorAll('tr').forEach(row => {
    const path = row.getAttribute('data-path') || row.dataset.path;
    if (!path) return;
    const level = row.querySelector('.col-level')?.textContent.trim() || '';
    const revisit = row.querySelector('.col-revisit')?.textContent.trim() || '';
    const notes = row.querySelector('.col-notes')?.textContent.trim() || '';
    updates.push({ path, level, revisit, notes });
  });

  const blob = new Blob([JSON.stringify(updates, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'updates.json';
  document.body.appendChild(a);
  a.click();
  a.remove();

  // exit edit mode after saving
  editMode = false;
  editToggle.textContent = 'Edit Mode';
  saveBtn.style.display = 'none';
  cancelBtn.style.display = 'none';
  document.querySelectorAll('.editable-cell').forEach(cell => {
    cell.removeAttribute('contenteditable');
    cell.classList.remove('active-edit');
  });

  alert('Updates downloaded as updates.json. Move it next to dashboard.py and re-run the script to apply changes to Java files.');
});

// Filters
function applyFilters() {
  const typeVal = (typeFilter.value || '').toLowerCase();
  const levelVal = (levelFilter.value || '').toLowerCase();
  const revisitVal = (revisitFilter.value || '').toLowerCase();

  table.querySelectorAll('tr').forEach(row => {
    const rowType = (row.getAttribute('data-type') || '').toLowerCase();
    const rowLevel = (row.getAttribute('data-level') || '').toLowerCase();
    const rowRevisit = (row.getAttribute('data-revisit') || '').toLowerCase();

    const matchType = !typeVal || rowType === typeVal;
    const matchLevel = !levelVal || rowLevel === levelVal;
    const matchRevisit = !revisitVal || rowRevisit === revisitVal;

    row.style.display = (matchType && matchLevel && matchRevisit) ? '' : 'none';
  });
}

[typeFilter, levelFilter, revisitFilter].forEach(el => el.addEventListener('change', applyFilters));

</script>
</body>
</html>
"""

    # write HTML
    try:
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ Generated {HTML_PATH}")
    except Exception as e:
        print(f"⚠️ Failed to write {HTML_PATH}: {e}")


# -----------------------------
# Main flow
# -----------------------------
def main():
    # Step 1: Apply updates.json if present (this updates Java files)
    apply_updates()
    # Step 2: Regenerate README
    try:
        table_md = generate_table()
        with open(README_PATH, "w", encoding="utf-8") as rf:
            rf.write(table_md)
        print(f"✅ Updated {README_PATH}")
    except Exception as e:
        print(f"⚠️ Failed to write {README_PATH}: {e}")
    # Step 3: Regenerate HTML dashboard
    generate_html()


if __name__ == "__main__":
    main()
