"""Tests for the kit's scripts/check_docs.py template, run against small fake projects."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parent.parent
PLUGIN = KIT / "plugins" / "project-kit"
TEMPLATES = PLUGIN / "skills" / "init-project" / "templates"
CATALOG = PLUGIN / "skills" / "sync-agents" / "catalog"
MARKER = re.compile(r"^<!-- project-kit catalog: ([a-z0-9-]+) v(\d+)\. .* -->$", re.M)


def load_checker():
    spec = importlib.util.spec_from_file_location("check_docs", TEMPLATES / "check_docs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLAUDE = """# CLAUDE.md: demo

## Where knowledge lives

| Topic | File |
|---|---|
| API | `docs/knowledge/api.md` |

## Who to ask

| Agent | Ask it about | Owns |
|---|---|---|
| `api` | the HTTP API | `src/api/` |

## Skills for repetitive work

| Skill | Use it to |
|---|---|
| `check-all` | Run every check. |
| `project-kit:add-knowledge` | Record a fact. |

## Commands

```bash
scripts/check_all.sh
```
"""

AGENT = """---
name: api
description: Expert on the API.
tools: Read
---

Read `CLAUDE.md` and `docs/knowledge/api.md`. Run `npm test` and `make lint`.
"""

SKILL = """---
name: check-all
description: Run every check.
---

Run `scripts/check_all.sh`.
"""


@pytest.fixture
def project(tmp_path: Path) -> Path:
    (tmp_path / "docs" / "knowledge").mkdir(parents=True)
    (tmp_path / "docs" / "knowledge" / "api.md").write_text("# Knowledge: api\n")
    (tmp_path / "src" / "api").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "check_all.sh").write_text("#!/bin/sh\n")
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    (tmp_path / ".claude" / "agents" / "api.md").write_text(AGENT)
    (tmp_path / ".claude" / "skills" / "check-all").mkdir(parents=True)
    (tmp_path / ".claude" / "skills" / "check-all" / "SKILL.md").write_text(SKILL)
    (tmp_path / "CLAUDE.md").write_text(CLAUDE)
    (tmp_path / "README.md").write_text("Skills: `check-all`. See [CLAUDE](CLAUDE.md).\n")
    return tmp_path


def test_consistent_project_passes(project: Path):
    assert load_checker().run(project) == []


def test_unlisted_knowledge_file(project: Path):
    (project / "docs" / "knowledge" / "db.md").write_text("# Knowledge: db\n")
    assert load_checker().run(project) == [
        "CLAUDE.md: docs/knowledge/db.md is not listed in 'Where knowledge lives'"
    ]


def test_agent_missing_from_table_and_wrong_name(project: Path):
    (project / ".claude" / "agents" / "db.md").write_text("---\nname: database\n---\n")
    problems = load_checker().run(project)
    assert "CLAUDE.md: agent `db` is missing from the 'Who to ask' table" in problems
    assert ".claude/agents/db.md: frontmatter name must be 'db'" in problems


def test_table_names_missing_agent_and_skill(project: Path):
    claude = (project / "CLAUDE.md").read_text()
    claude = claude.replace("| `api` |", "| `api` |", 1).replace(
        "| `check-all` |", "| `release` | Release. |\n| `check-all` |"
    )
    claude = claude.replace("|---|---|---|\n", "|---|---|---|\n| `ghost` | x | y |\n")
    (project / "CLAUDE.md").write_text(claude)
    problems = load_checker().run(project)
    assert "CLAUDE.md: agent `ghost` in the table has no .claude/agents/ghost.md" in problems
    assert "CLAUDE.md: skill `release` in the table has no .claude/skills/release/SKILL.md" in problems


def test_plugin_skills_in_table_are_not_checked(project: Path):
    assert not [p for p in load_checker().run(project) if "project-kit" in p]


def test_skill_must_be_in_readme(project: Path):
    (project / "README.md").write_text("Nothing here.\n")
    assert load_checker().run(project) == ["README.md: skill `check-all` is not mentioned"]


def test_readme_check_can_be_disabled(project: Path):
    (project / "README.md").write_text("Nothing here.\n")
    checker = load_checker()
    checker.README_LISTS_SKILLS = False
    assert checker.run(project) == []


def test_broken_relative_link(project: Path):
    (project / "README.md").write_text("`check-all` [x](docs/missing.md) [web](https://a.b)\n")
    assert load_checker().run(project) == ["README.md: broken link -> docs/missing.md"]


def test_cited_paths(project: Path):
    agent = (project / ".claude" / "agents" / "api.md").read_text()
    agent += (
        "Also `src/api/routes.py`, `src/*.py` (none), `docs/knowledge/<x>.md`, "
        "`src/{a,b}.py`, `lib/other.py`, `--flag`.\n"
        "Later `src/planned.py` (planned).\n"
    )
    (project / ".claude" / "agents" / "api.md").write_text(agent)
    problems = load_checker().run(project)
    assert problems == [
        ".claude/agents/api.md: cites `src/api/routes.py`, which does not exist",
        ".claude/agents/api.md: cites `src/*.py`, which does not exist",
    ]


def test_paths_inside_code_blocks_are_ignored(project: Path):
    skill = project / ".claude" / "skills" / "check-all" / "SKILL.md"
    skill.write_text(SKILL + "\n```bash\ncat `src/nope.py`\n```\n")
    assert load_checker().run(project) == []


def test_missing_claude_md(tmp_path: Path):
    assert load_checker().run(tmp_path) == ["CLAUDE.md is missing"]


def frontmatter(path: Path) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    assert match, f"{path} has no frontmatter"
    return dict(line.split(": ", 1) for line in match.group(1).splitlines() if ": " in line)


def test_plugin_skills_have_matching_names_and_descriptions():
    skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
    assert {s.parent.name for s in skills} == {
        "init-project",
        "add-knowledge",
        "new-domain",
        "new-skill",
        "kit-audit",
        "sync-agents",
    }
    for skill in skills:
        meta = frontmatter(skill)
        assert meta["name"] == skill.parent.name
        assert len(meta["description"]) > 80


def test_manifests_agree():
    plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    market = json.loads((KIT / ".claude-plugin" / "marketplace.json").read_text())
    entry = {p["name"]: p for p in market["plugins"]}["project-kit"]
    assert entry["version"] == plugin["version"]
    assert (KIT / entry["source"]).resolve() == PLUGIN.resolve()


def test_templates_referenced_by_init_exist():
    init = (PLUGIN / "skills" / "init-project" / "SKILL.md").read_text()
    for name in re.findall(r"`templates/([^`]+)`", init):
        assert (TEMPLATES / name).is_file(), name


CATALOG_AGENTS = sorted(CATALOG.glob("*.md"))


def test_catalog_is_not_empty():
    assert CATALOG_AGENTS


@pytest.mark.parametrize("agent", CATALOG_AGENTS, ids=lambda p: p.stem)
def test_catalog_agent_format(agent: Path):
    text = agent.read_text(encoding="utf-8")
    meta = frontmatter(agent)
    assert meta["name"] == agent.stem
    assert len(meta["description"]) > 80
    assert meta["tools"]
    after_frontmatter = text.split("\n---\n", 1)[1]
    marker = MARKER.match(after_frontmatter)
    assert marker, "the marker must be the first line after the frontmatter"
    assert marker.group(1) == agent.stem
    assert text.count("\n## Project notes\n") == 1
    assert "{{" not in text, "catalog agents are finished files, not templates"


@pytest.mark.parametrize("agent", CATALOG_AGENTS, ids=lambda p: p.stem)
def test_imported_catalog_agent_passes_checker(project: Path, agent: Path):
    """Importing as sync-agents describes (copy + knowledge + rows) leaves the project consistent."""
    name = agent.stem
    (project / ".claude" / "agents" / f"{name}.md").write_text(agent.read_text())
    claude = (project / "CLAUDE.md").read_text()
    rows = ""
    for cited in sorted(set(re.findall(r"`(docs/knowledge/[a-z0-9-]+\.md)`", agent.read_text()))):
        seed = CATALOG / "knowledge" / Path(cited).name
        assert seed.is_file() or (project / cited).exists(), f"{name} cites {cited} with no seed"
        (project / cited).write_text(seed.read_text())
        rows += f"| {name} | `{cited}` |\n"
    claude = claude.replace("| API | `docs/knowledge/api.md` |\n", "| API | `docs/knowledge/api.md` |\n" + rows)
    claude = claude.replace("| `api` | the HTTP API |", f"| `{name}` | advice | nothing |\n| `api` | the HTTP API |")
    (project / "CLAUDE.md").write_text(claude)
    assert load_checker().run(project) == []
