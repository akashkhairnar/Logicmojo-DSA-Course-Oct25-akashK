import os

ROOT = "dsa"  # base folder
README_PATH = "README.md"

def extract_metadata(file_path):
    problem = "-"
    link = ""
    level = "-"
    time_complexity = "-"
    notes = "-"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("// Problem:"):
                    problem = line.replace("// Problem:", "").strip()
                elif line.startswith("// Link:"):
                    link = line.replace("// Link:", "").strip()
                elif line.startswith("// Level:"):
                    level = line.replace("// Level:", "").strip()
                elif line.startswith("// Time Complexity:"):
                    time_complexity = line.replace("// Time Complexity:", "").strip()
                elif line.startswith("// Notes:"):
                    notes = line.replace("// Notes:", "").strip()
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    return problem, link, level, time_complexity, notes


def generate_table():
    rows = []
    count = 1
    for root, _, files in os.walk(ROOT):
        for file in sorted(files):
            if file.endswith(".java") and ".git" not in root and ".github" not in root:
                path = os.path.join(root, file)
                github_link = f"[Code]({path})"
                problem, link, level, time_complexity, notes = extract_metadata(path)
                problem_display = f"[{problem}]({link})" if link else problem
                rows.append(
                    f"| {count} | {problem_display} | {github_link} | {level} | {time_complexity} | {notes} |"
                )
                count += 1

    if not rows:
        return "No Java files found yet."

    header = (
        "| # | Problem | Solution | Level | Time Complexity | Quick Notes |\n"
        "|---|----------|-----------|--------|------------------|--------------|"
    )
    return header + "\n" + "\n".join(rows)


def update_readme():
    table = generate_table()
    content = f"# 🚀 DSA in Java\n\nAutomatically generated table of solved problems.\n\n{table}\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README updated successfully!")


if __name__ == "__main__":
    update_readme()