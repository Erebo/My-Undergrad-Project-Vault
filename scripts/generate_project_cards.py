# #!/usr/bin/env python3
# """
# Generate project cards for root-level project folders and replace a section
# in README.md between markers:
#   <!-- PROJECT_CARDS_START -->
#   <!-- PROJECT_CARDS_END -->
# """

# import os
# import re
# from pathlib import Path

# ROOT = Path(__file__).resolve().parents[1]  # repo root
# README_PATH = ROOT / "README.md"
# EXCLUDE = {".github", ".git", ".vscode", "__pycache__", "assets"}
# MARKER_START = "<!-- PROJECT_CARDS_START -->"
# MARKER_END = "<!-- PROJECT_CARDS_END -->"


# def read_project_description(proj_path: Path) -> str:
#     """
#     Read first non-empty line from project's README.md (if exists) to use as short description.
#     Fallback: prettified folder name.
#     """
#     readme = proj_path / "README.md"
#     if readme.exists():
#         try:
#             with readme.open("r", encoding="utf-8") as f:
#                 for line in f:
#                     line = line.strip()
#                     if line:
#                         line = re.sub(r"^#+\s*", "", line)  # strip markdown headings
#                         return line if len(line) <= 200 else line[:197] + "..."
#         except Exception:
#             pass
#     name = proj_path.name.replace("-", " ").replace("_", " ").title()
#     return f"{name} — project folder. Open for details."


# def generate_card_md(proj_name: str, desc: str) -> str:
#     """
#     Return a markdown snippet for a project.
#     """
#     link = f"./{proj_name}"
#     md = f"""### [{proj_name}]({link})
# {desc}

# [View project →]({link})

# ---
# """
#     return md


# def main():
#     # gather root-level directories (projects)
#     entries = sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name not in EXCLUDE])
#     projects = []
#     for p in entries:
#         if p.name.startswith("."):
#             continue
#         desc = read_project_description(p)
#         cards = generate_card_md(p.name, desc)
#         projects.append(cards)

#     cards_section = "\n".join(projects) if projects else "_No projects found in root._\n"

#     # ensure README exists
#     if not README_PATH.exists():
#         print("README.md not found at repo root. Creating a new one with markers.")
#         README_PATH.write_text(f"{MARKER_START}\n{cards_section}\n{MARKER_END}\n", encoding="utf-8")
#         return

#     readme_text = README_PATH.read_text(encoding="utf-8")

#     if MARKER_START not in readme_text or MARKER_END not in readme_text:
#         # Append markers and section at end if markers not present
#         new_text = readme_text.rstrip() + f"\n\n{MARKER_START}\n{cards_section}\n{MARKER_END}\n"
#     else:
#         pattern = re.compile(re.escape(MARKER_START) + ".*?" + re.escape(MARKER_END), flags=re.DOTALL)
#         replacement = f"{MARKER_START}\n{cards_section}\n{MARKER_END}"
#         new_text = pattern.sub(replacement, readme_text)

#     README_PATH.write_text(new_text, encoding="utf-8")
#     print("README.md updated with project cards.")


# if __name__ == "__main__":
#     main()
#!/usr/bin/env python3
"""
Generate project cards for root-level project folders and replace a section
in README.md between markers:
  <!-- PROJECT_CARDS_START -->
  <!-- PROJECT_CARDS_END -->

This version adds support for git submodules by reading .gitmodules and
producing links to the submodule repos.
"""

import os
import re
import configparser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
README_PATH = ROOT / "README.md"
GITMODULES_PATH = ROOT / ".gitmodules"
EXCLUDE = {".github", ".git", ".vscode", "__pycache__", "assets"}
MARKER_START = "<!-- PROJECT_CARDS_START -->"
MARKER_END = "<!-- PROJECT_CARDS_END -->"


def read_submodules(repo_root: Path = ROOT):
    """
    Parse .gitmodules and return a dict mapping submodule path -> url.
    Example return:
      { "Amusement-Park-Management-System_CSE124": "https://github.com/owner/repo" }
    """
    gitmodules = repo_root / ".gitmodules"
    subs = {}
    if not gitmodules.exists():
        return subs

    cfg = configparser.ConfigParser()
    try:
        # configparser can read the .gitmodules format
        cfg.read(gitmodules)
    except Exception:
        # fallback: manual parse (very simple)
        text = gitmodules.read_text(encoding="utf-8")
        # naive fallback parser (should be rare)
        cur_path = None
        cur_url = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("[submodule"):
                cur_path = cur_url = None
            elif line.startswith("path"):
                cur_path = line.split("=", 1)[1].strip()
            elif line.startswith("url"):
                cur_url = line.split("=", 1)[1].strip().strip('"')
            if cur_path and cur_url:
                subs[cur_path] = cur_url
                cur_path = cur_url = None
        return subs

    # cfg.sections() will look like: submodule "name"
    for section in cfg.sections():
        if section.startswith("submodule"):
            try:
                path = cfg.get(section, "path")
                url = cfg.get(section, "url")
                if path and url:
                    subs[path] = url
            except Exception:
                continue
    return subs


def normalize_git_url_to_https(url: str) -> str:
    """
    Convert git remote URL to a browsable https GitHub URL if possible.
    Examples:
      git@github.com:owner/repo.git -> https://github.com/owner/repo
      https://github.com/owner/repo.git -> https://github.com/owner/repo
    If conversion isn't possible, return the original URL.
    """
    if not url:
        return url
    url = url.strip()
    # git@github.com:owner/repo.git -> https://github.com/owner/repo
    if url.startswith("git@github.com:"):
        https = url.replace("git@github.com:", "https://github.com/")
        if https.endswith(".git"):
            https = https[:-4]
        return https
    # https://github.com/owner/repo.git -> https://github.com/owner/repo
    if url.startswith("https://github.com/") or url.startswith("http://github.com/"):
        if url.endswith(".git"):
            return url[:-4]
        return url
    # fallback: strip .git if present
    if url.endswith(".git"):
        return url[:-4]
    return url


def read_project_description(proj_path: Path, is_submodule: bool = False) -> str:
    """
    Read first non-empty line from project's README.md (if exists) to use as short description.
    Fallback: prettified folder name or a submodule message.
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
    # fallback messages
    name = proj_path.name.replace("-", " ").replace("_", " ").title()
    if is_submodule:
        return f"{name} — submodule at `{proj_path.name}`. Click to open the project repository."
    return f"{name} — project folder. Open for details."


def generate_card_md(proj_name: str, desc: str, link: str) -> str:
    """
    Return a markdown snippet for a project. `link` should be a URL or relative path.
    """
    md = f"""### [{proj_name}]({link})
{desc}

[View project →]({link})

---
"""
    return md


def main():
    # read submodules mapping path -> url
    submodules = read_submodules(ROOT)

    # gather root-level directories (projects)
    entries = sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name not in EXCLUDE])
    projects_md = []

    for p in entries:
        if p.name.startswith("."):
            continue

        if p.name in submodules:
            # treat as submodule
            remote_url = normalize_git_url_to_https(submodules[p.name])
            # If local README exists, prefer that description (submodule may be initialized)
            desc = read_project_description(p, is_submodule=True)
            link = remote_url if remote_url else f"./{p.name}"
            projects_md.append(generate_card_md(p.name, desc, link))
        else:
            # normal project folder
            desc = read_project_description(p, is_submodule=False)
            link = f"./{p.name}"
            projects_md.append(generate_card_md(p.name, desc, link))

    cards_section = "\n".join(projects_md) if projects_md else "_No projects found in root._\n"

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
    print("README.md updated with project cards (including submodules).")


if __name__ == "__main__":
    main()

