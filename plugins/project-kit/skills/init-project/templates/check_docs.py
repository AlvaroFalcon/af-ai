"""Check that the project's docs, knowledge, agents and skills are linked consistently.

  python scripts/check_docs.py

Installed by the project-kit plugin (`project-kit:init-project`). The project owns this copy; run
`project-kit:kit-audit` to compare it with the kit's latest version.

Checks (exit 1 with a list of problems if any fails):
  1. Relative links in Markdown files point to files that exist.
  2. Every file in KNOWLEDGE_DIRS is listed in CLAUDE.md.
  3. Every agent in .claude/agents/ is in CLAUDE.md's "Who to ask" table, and every agent in the
     table exists. The frontmatter `name` matches the file name.
  4. Every skill in .claude/skills/ is in CLAUDE.md's skills table (and mentioned in README.md if
     README_LISTS_SKILLS), and every skill in the table exists. The frontmatter `name` matches the
     folder name. Plugin skills (`plugin:skill`) in the table are not checked.
  5. Repo paths cited in backticks by CLAUDE.md, agents and skills exist. A backticked token is
     treated as a repo path when its first segment is a top-level entry of the repo. Globs,
     placeholders (<x>, NNN, {a,b}) and lines marked "(planned)" are allowed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# --- Project settings ------------------------------------------------------------------------
KNOWLEDGE_DIRS = ("docs/knowledge", "docs/design")
AGENTS_SECTION = "Who to ask"
SKILLS_SECTION = "Skills for repetitive work"
README_LISTS_SKILLS = True
# -------------------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BACKTICK = re.compile(r"`([^`\s]+)`")
FRONTMATTER_NAME = re.compile(r"^---\s*\n(?:.*\n)*?name:\s*([^\n]+)\n(?:.*\n)*?---", re.MULTILINE)
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "__pycache__"}


def markdown_files(root: Path) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
        files = [root / f for f in out]
    except (OSError, subprocess.CalledProcessError):
        files = [p for p in root.rglob("*.md") if not SKIP_DIRS.intersection(p.parts)]
    return sorted({f for f in files if f.is_file()})


def section(text: str, heading: str) -> str:
    """Body of the `## heading` section (until the next `## `)."""
    match = re.search(rf"^## {re.escape(heading)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def first_column_names(table_text: str) -> set[str]:
    """Local names in the first column; `plugin:skill` entries are skipped."""
    return set(re.findall(r"^\|\s*`([a-z0-9-]+)`\s*\|", table_text, re.M))


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_links(root: Path, files: list[Path]) -> list[str]:
    problems = []
    for md in files:
        text = strip_code_blocks(md.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue  # http(s):, mailto:, in-page anchors
            path = target.split("#", 1)[0]
            if not path:
                continue
            resolved = (md.parent / path).resolve()
            if root.resolve() not in resolved.parents and resolved != root.resolve():
                continue  # GitHub web paths such as ../../releases
            if not resolved.exists():
                problems.append(f"{md.relative_to(root)}: broken link -> {target}")
    return problems


def check_knowledge_listed(root: Path, claude: str) -> list[str]:
    problems = []
    for folder in KNOWLEDGE_DIRS:
        for f in sorted((root / folder).glob("*.md")):
            rel = f"{folder}/{f.name}"
            if rel not in claude:
                problems.append(f"CLAUDE.md: {rel} is not listed in 'Where knowledge lives'")
    return problems


def frontmatter_name(path: Path) -> str | None:
    match = FRONTMATTER_NAME.search(path.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else None


def check_agents(root: Path, claude: str) -> list[str]:
    problems = []
    table = first_column_names(section(claude, AGENTS_SECTION))
    files = {p.stem: p for p in (root / ".claude" / "agents").glob("*.md")}
    for name, path in sorted(files.items()):
        if name not in table:
            problems.append(
                f"CLAUDE.md: agent `{name}` is missing from the '{AGENTS_SECTION}' table"
            )
        if frontmatter_name(path) != name:
            problems.append(f"{path.relative_to(root)}: frontmatter name must be '{name}'")
    for name in sorted(table - set(files)):
        problems.append(f"CLAUDE.md: agent `{name}` in the table has no .claude/agents/{name}.md")
    return problems


def check_skills(root: Path, claude: str, readme: str) -> list[str]:
    problems = []
    table = first_column_names(section(claude, SKILLS_SECTION))
    folders = {p.parent.name: p for p in (root / ".claude" / "skills").glob("*/SKILL.md")}
    for name, path in sorted(folders.items()):
        if name not in table:
            problems.append(f"CLAUDE.md: skill `{name}` is missing from the skills table")
        if README_LISTS_SKILLS and f"`{name}`" not in readme:
            problems.append(f"README.md: skill `{name}` is not mentioned")
        if frontmatter_name(path) != name:
            problems.append(f"{path.relative_to(root)}: frontmatter name must be '{name}'")
    for name in sorted(table - set(folders)):
        problems.append(
            f"CLAUDE.md: skill `{name}` in the table has no .claude/skills/{name}/SKILL.md"
        )
    return problems


def top_level(root: Path) -> set[str]:
    return {p.name for p in root.iterdir() if p.name not in SKIP_DIRS}


def cited_path_exists(root: Path, cited: str) -> bool:
    if any(token in cited for token in ("<", ">", "NNN", "{", "}")):
        return True  # placeholder or brace pattern: a documented convention, not a concrete file
    if any(ch in cited for ch in "*?["):
        return any(root.glob(cited))
    return (root / cited).exists()


def check_cited_paths(root: Path) -> list[str]:
    problems = []
    roots = top_level(root)
    sources = [root / "CLAUDE.md"]
    sources += sorted((root / ".claude" / "agents").glob("*.md"))
    sources += sorted((root / ".claude" / "skills").glob("*/SKILL.md"))
    for src in sources:
        for line in strip_code_blocks(src.read_text(encoding="utf-8")).splitlines():
            if "(planned)" in line:
                continue
            for token in BACKTICK.findall(line):
                cited = token.rstrip(".,;:)").removeprefix("./")
                if cited.split("/", 1)[0] not in roots:
                    continue  # not a repo path: a command, an identifier, a value
                if not cited_path_exists(root, cited):
                    problems.append(
                        f"{src.relative_to(root)}: cites `{cited}`, which does not exist"
                    )
    return problems


def run(root: Path = ROOT) -> list[str]:
    claude_md = root / "CLAUDE.md"
    if not claude_md.exists():
        return ["CLAUDE.md is missing"]
    claude = claude_md.read_text(encoding="utf-8")
    readme_md = root / "README.md"
    readme = readme_md.read_text(encoding="utf-8") if readme_md.exists() else ""
    return (
        check_links(root, markdown_files(root))
        + check_knowledge_listed(root, claude)
        + check_agents(root, claude)
        + check_skills(root, claude, readme)
        + check_cited_paths(root)
    )


def main() -> int:
    problems = run()
    if problems:
        print("Documentation links are inconsistent:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("Docs, knowledge, agents and skills are consistently linked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
