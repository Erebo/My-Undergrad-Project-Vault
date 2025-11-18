#!/usr/bin/env python3
"""
Generate project cards for root-level project folders and replace a section
in README.md between markers:
  <!-- PROJECT_CARDS_START -->
  <!-- PROJECT_CARDS_END -->
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
README_PATH = ROOT / "README.md"
EXCLUDE = {".github", ".git", ".vscode", "__pycache__", "assets"}
MARKER_START = "<!-- PROJECT_CARDS_START -->"
MARKER_END = "<!-- PROJECT_CARDS_END -->"


def read_project_description(proj_path: Path) -> str:
    """
    Read first non-empty line from project's README.md (if exists) to use as short description.
    Fallback: prettified folder name.
    """
    readme = proj_path / "README.md"
    if readme.exists():
        try:
            with readme.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        line = re.sub(r"^#+\s*", "", line)  # strip markdown headings
                        return line if len(line) <= 200 else line[:197] + "..."
        except Exception:
            pass
    name = proj_path.name.replace("-", " ").replace("_", " ").title()
    return f"{name} — project folder. Open for details."


def generate_card_md(proj_name: str, desc: str) -> str:
    """
    Return a markdown snippet for a project.
    """
    link = f"./{proj_name}"
    md = f"""### [{proj_name}]({link})
{desc}

[View project →]({link})

---
"""
    return md


def main():
    # gather root-level directories (projects)
    entries = sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name not in EXCLUDE])
    projects = []
    for p in entries:
        if p.name.startswith("."):
            continue
        desc = read_project_description(p)
        cards = generate_card_md(p.name, desc)
        projects.append(cards)

    cards_section = "\n".join(projects) if projects else "_No projects found in root._\n"

    # ensure README exists
    if not README_PATH.exists():
        print("README.md not found at repo root. Creating a new one with markers.")
        README_PATH.write_text(f"{MARKER_START}\n{cards_section}\n{MARKER_END}\n", encoding="utf-8")
        return

    readme_text = README_PATH.read_text(encoding="utf-8")

    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        # Append markers and section at end if markers not present
        new_text = readme_text.rstrip() + f"\n\n{MARKER_START}\n{cards_section}\n{MARKER_END}\n"
    else:
        pattern = re.compile(re.escape(MARKER_START) + ".*?" + re.escape(MARKER_END), flags=re.DOTALL)
        replacement = f"{MARKER_START}\n{cards_section}\n{MARKER_END}"
        new_text = pattern.sub(replacement, readme_text)

    README_PATH.write_text(new_text, encoding="utf-8")
    print("README.md updated with project cards.")


if __name__ == "__main__":
    main()
