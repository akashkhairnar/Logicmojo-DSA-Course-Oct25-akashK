#!/usr/bin/env python3
"""
dashboard.py

DSA Dashboard with:
- Local Flask server
- Admin token protection
- Inline edit for Level, Revisit, Notes
- Auto update .java files
- Auto regenerate README.md and index.html
- Optional GitHub commit & push using GITHUB_TOKEN
- Filters: Type, Level, Revisit
"""

import os
import json
import subprocess
from datetime import datetime
from flask import Flask, request, send_from_directory, jsonify, render_template_string
from pathlib import Path

# ---------------- Configuration ----------------
ROOT = "dsa"
README_PATH = "README.md"
HTML_PATH = "index.html"
BRANCH = "master"  # git branch to push

ADMIN_TOKEN_ENV = os.getenv("ADMIN_TOKEN")
GITHUB_TOKEN_ENV = os.getenv("GITHUB_TOKEN")

# ---------------- Flask App ----------------
app = Flask(__name__)

# ---------------- Helper functions ----------------
def extract_metadata(file_path):
    problem = ""
    level = ""
    revisit = ""
    notes = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
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
                if problem and level and revisit and notes:
                    break
    except:
        pass
    return problem, level, revisit, notes

def ensure_type(s):
    if not s:
        return "general"
    return s.strip().lower().strip("./\\")

def generate_table_md():
    rows = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java"):
                path = os.path.join(root, file)
                problem, level, revisit, notes = extract_metadata(path)
                problem_display = problem or file.replace(".java", "")
                rel_path = os.path.relpath(path)
                github_link = f"[Code]({rel_path})"
                rows.append((count, problem_display, github_link, level, file.replace(".java",""), revisit, notes))
                count +=1

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

def apply_updates(updates):
    for upd in updates:
        path = upd.get("path")
        level = upd.get("level","").strip()
        revisit = upd.get("revisit","").strip()
        notes = upd.get("notes","").strip()
        if not path:
            continue
        file_path = Path(path)
        if not file_path.exists():
            continue
        try:
            with open(file_path,"r",encoding="utf-8") as f:
                lines = f.readlines()
            replaced_level = replaced_revisit = replaced_notes = False
            insert_index_after_problem = None
            for idx,line in enumerate(lines[:50]):
                s=line.strip()
                if s.startswith("// Problem:"):
                    insert_index_after_problem=idx
                if s.startswith("// Level:") and level:
                    lines[idx]=f"// Level: {level}\n"; replaced_level=True
                if s.startswith("// Revisit:") and revisit:
                    lines[idx]=f"// Revisit: {revisit}\n"; replaced_revisit=True
                if s.startswith("// Notes:") and notes:
                    lines[idx]=f"// Notes: {notes}\n"; replaced_notes=True
            insertion=[]
            if not replaced_level and level:
                insertion.append(f"// Level: {level}\n")
            if not replaced_revisit and revisit:
                insertion.append(f"// Revisit: {revisit}\n")
            if not replaced_notes and notes:
                insertion.append(f"// Notes: {notes}\n")
            if insertion:
                if insert_index_after_problem is not None:
                    lines[insert_index_after_problem+1:insert_index_after_problem+1]=insertion
                else:
                    lines=insertion+["\n"]+lines
            with open(file_path,"w",encoding="utf-8") as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Failed to update {file_path}: {e}")

def git_commit_push(message="auto: dashboard update"):
    if not GITHUB_TOKEN_ENV:
        print("No GITHUB_TOKEN set, skipping git push")
        return
    try:
        subprocess.run(["git","add","."],check=True)
        subprocess.run(["git","commit","-m",message],check=True)
        repo_url=subprocess.check_output(["git","config","--get","remote.origin.url"],encoding="utf-8").strip()
        # convert https url to token url
        if repo_url.startswith("https://"):
            parts=repo_url.split("https://")
            token_url=f"https://{GITHUB_TOKEN_ENV}@{parts[1]}"
        else:
            token_url=repo_url
        subprocess.run(["git","push",token_url,BRANCH],check=True)
        print("✅ Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")

# ---------------- Flask routes ----------------
@app.route("/")
def index():
    # Serve dashboard HTML
    return render_dashboard_html()

@app.route("/save",methods=["POST"])
def save():
    data=request.get_json()
    token=data.get("admin_token","")
    if token != ADMIN_TOKEN_ENV:
        return jsonify({"status":"error","msg":"Invalid admin token"}),403
    updates=data.get("updates",[])
    apply_updates(updates)
    # regenerate README
    try:
        with open(README_PATH,"w",encoding="utf-8") as f:
            f.write(generate_table_md())
    except Exception as e:
        print("Failed to write README.md",e)
    # regenerate HTML
    render_dashboard_html(write=True)
    # git push
    git_commit_push()
    return jsonify({"status":"success","msg":"Updates applied successfully"})

# ---------------- Dashboard HTML ----------------
def render_dashboard_html(write=False):
    # Generate table rows
    rows_html=[]
    type_set=set()
    count=1
    for root,_,files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java"):
                file_path=os.path.join(root,file)
                problem,level,revisit,notes=extract_metadata(file_path)
                pattern=file.replace(".java","")
                rel_dir=os.path.relpath(root,ROOT)
                problem_type="general" if rel_dir=="." else rel_dir.split(os.sep)[0]
                problem_type=ensure_type(problem_type)
                type_set.add(problem_type)
                data_level=(level or "").strip().lower()
                data_revisit=(revisit or "").strip().lower()
                data_type=problem_type
                rel_path=os.path.relpath(file_path)
                problem_label=problem or pattern
                rows_html.append(
                    f"<tr data-type='{data_type}' data-level='{data_level}' data-revisit='{data_revisit}' data-path='{rel_path}'>"
                    f"<td>{count}</td>"
                    f"<td>{problem_label}</td>"
                    f"<td><a href='{rel_path}' target='_blank'>Code</a></td>"
                    f"<td class='editable-cell'>{level}</td>"
                    f"<td>{pattern}</td>"
                    f"<td class='editable-cell'>{revisit}</td>"
                    f"<td class='editable-cell'>{notes}</td>"
                    f"</tr>"
                )
                count+=1
    type_options_html="\n".join([f"<option value='{t}'>{t.title()}</option>" for t in sorted(type_set)])

    html_template=f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DSA Dashboard</title>
<style>
body{{font-family:sans-serif;background:#f5f6f8;margin:20px;}}
table{{width:100%;border-collapse:collapse;table-layout:fixed;}}
th,td{{padding:8px;border-bottom:1px solid #ddd;overflow-wrap:break-word;}}
th{{background:#eee;text-align:left;}}
.editable-cell{{background:#f9f7ff;border-radius:4px;}}
.editable-cell[contenteditable="true"]{{outline:2px solid #7c3aed;background:#f2ebff;}}
select,button{{padding:6px 10px;margin:4px;border-radius:4px;}}
</style>
</head>
<body>
<h1>DSA Dashboard</h1>
<div>
Type: <select id="typeFilter"><option value="">All Types</option>{type_options_html}</select>
Level: <select id="levelFilter"><option value="">All</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select>
Revisit: <select id="revisitFilter"><option value="">All</option><option value="yes">Yes</option><option value="no">No</option></select>
<button id="editToggle">Edit Mode</button>
<button id="saveBtn" style="display:none;">💾 Save</button>
</div>
<table id="problemsTable"><thead><tr>
<th>#</th><th>Problem</th><th>Solution</th><th>Level</th><th>Pattern</th><th>Revisit</th><th>Notes</th>
</tr></thead><tbody>
{''.join(rows_html)}
</tbody></table>
<script>
let editMode=false;
const table=document.getElementById('problemsTable').querySelector('tbody');
const editToggle=document.getElementById('editToggle');
const saveBtn=document.getElementById('saveBtn');

function applyFilters(){{
let typeVal=document.getElementById('typeFilter').value.toLowerCase();
let levelVal=document.getElementById('levelFilter').value.toLowerCase();
let revisitVal=document.getElementById('revisitFilter').value.toLowerCase();
table.querySelectorAll('tr').forEach(row=>{
let rowType=row.getAttribute('data-type')||'';
let rowLevel=row.getAttribute('data-level')||'';
let rowRevisit=row.getAttribute('data-revisit')||'';
row.style.display=( (!typeVal||rowType===typeVal)&&(!levelVal||rowLevel===levelVal)&&(!revisitVal||rowRevisit===revisitVal) )?'':'none';
}});
}}

['typeFilter','levelFilter','revisitFilter'].forEach(id=>document.getElementById(id).addEventListener('change',applyFilters));

editToggle.addEventListener('click',()=>{
editMode=!editMode;
document.querySelectorAll('.editable-cell').forEach(cell=>cell.contentEditable=editMode?"true":"false");
saveBtn.style.display=editMode?'':'none';
});

saveBtn.addEventListener('click',async()=>{
let token=prompt("Enter Admin Token");
if(!token)return alert("Admin token required");
let updates=[];
table.querySelectorAll('tr').forEach(row=>{
updates.push({path:row.dataset.path,level:row.querySelector('td:nth-child(4)').textContent.trim(),revisit:row.querySelector('td:nth-child(6)').textContent.trim(),notes:row.querySelector('td:nth-child(7)').textContent.trim()});
});
let res=await fetch('/save',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({admin_token:token,updates:updates})});
let result=await res.json();
alert(result.msg);
if(result.status==="success") location.reload();
});
</script>
</body></html>
"""
    if write:
        with open(HTML_PATH,"w",encoding="utf-8") as f:
            f.write(html_template)
    return html_template

# ---------------- Main ----------------
if __name__=="__main__":
    # ensure README exists
    with open(README_PATH,"w",encoding="utf-8") as f:
        f.write(generate_table_md())
    # generate dashboard HTML
    render_dashboard_html(write=True)
    print("✅ Dashboard ready at http://localhost:5000")
    app.run(host="0.0.0.0",port=5000,debug=False)
