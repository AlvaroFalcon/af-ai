# af-ai

Claude Code plugins for working on long projects with Claude as a coordinator of domain agents.

## project-kit

Sets up and maintains the structure that keeps long Claude Code projects coherent across
sessions. It is extracted from a real project where it worked well:

- **`CLAUDE.md`** holds the working agreement (research → spec → plan → implement → verify, with
  the owner's OK on the spec and on the plan), the non-negotiable rules, where each kind of knowledge lives, which agent to ask about
  what, and which skill to use for repeated procedures.
- **`docs/knowledge/<domain>.md`**: facts that are not obvious from the code (measurements, API
  quirks, CI failure causes, owner decisions), one fact per bullet, each with its source.
- **`.claude/agents/<domain>.md`**: one agent per area of the code. Each owns a set of paths, reads
  `CLAUDE.md` and its knowledge file first, and finishes with the checks green and the knowledge
  updated. Read-only advisors cover outside expertise.
- **`.claude/skills/<name>/`**: project checklists for repeated procedures (version bump,
  migrations, release dry runs…).
- **`scripts/check_docs.py`**: fails CI when knowledge files, agents or skills are not linked from
  `CLAUDE.md`, a table names something missing, or a cited path does not exist.
- **`scripts/check_all.sh`**: every CI check locally, with one summary.
- **`docs/specs/NNN-<slug>.md`**: one spec per change (problem, value, research, decisions,
  acceptance criteria, plan, verification), written by the `feature` skill.

### The flow

```
request ─► product: worth it? exists? reuse? quick win?
              │
              ├─ trivial ──────────────► short plan ─► OK ─► implement
              ├─ fits one spec ─► research ─► grilling ─► SPEC ─► OK ─► PLAN ─► OK ─► implement ─► verify
              └─ too big / foggy ─► wayfinder map on GitHub issues ─► one decision per session ─► spec(s) ─┘
```

`feature` runs it; `grilling` asks the owner the open questions in rounds, each with a
recommended answer; `wayfinder` charts big efforts as a map issue with decision tickets as
sub-issues (shown on a GitHub Project board through its auto-add workflow).

### Install

In Claude Code 2.1.275 or later:

```
/plugin install project-kit --marketplace AlvaroFalcon/af-ai
```

Older versions:

```
/plugin marketplace add AlvaroFalcon/af-ai
```

```
/plugin install project-kit@af-ai
```

Restart the session so the skills load.

### Skills

| Skill | Use it to |
|---|---|
| `project-kit:init-project` | Set up a repo: research it, ask the owner's rules, propose the domains, then write `CLAUDE.md`, knowledge files, agents, `check-all`, the docs checker and the CI step. |
| `project-kit:add-knowledge` | Record a non-obvious fact in the right knowledge file, with its source, and propagate it. |
| `project-kit:new-domain` | Add a new area: knowledge file, agent, and their rows in `CLAUDE.md` and the README. |
| `project-kit:new-skill` | Turn a procedure done twice into a project skill. |
| `project-kit:feature` | Take a request through research → spec → plan → implement → verify, with the catalog agents. |
| `project-kit:grilling` | Settle open decisions with the owner: rounds of numbered questions, each with a recommended answer. |
| `project-kit:wayfinder` | Chart work too big for one spec as a map of decision tickets on GitHub issues, then resolve one per session. Started only when the owner asks for it, by name or with `/project-kit:wayfinder`. |
| `project-kit:create-pr` | Open or update the branch's PR with a fixed description (new, changed, to test, acceptance criteria, notes), after merging the base in and running the checks; links the spec. |
| `project-kit:sync-agents` | Add ready-made agents from the kit catalog, or update the ones a project already imported (keeping its "Project notes"). |
| `project-kit:kit-audit` | Compare a project's setup with the kit, update its `scripts/check_docs.py`, propose fixes. |

### Agent catalog

Besides the domain agents written for each project, the kit ships finished agents that are the
same everywhere. `sync-agents` copies them into `.claude/agents/` and later updates them; each one
keeps a `## Project notes` section that belongs to the project.

| Agent | What it does |
|---|---|
| `product` | Read-only advisor: is the request worth it, does it already exist, what can be reused, what is the quick win. Reads `docs/knowledge/product.md` for users and goals. |
| `researcher` | Read-only: the facts a decision waits on, from the code, the docs and the web, with sources. |
| `planner` | Read-only: turns an agreed spec into small steps, each owned by one domain agent. |
| `verifier` | Runs the checks and verifies each acceptance criterion with evidence; never edits. |

`grilling` and `wayfinder` are adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
(MIT); see [THIRD_PARTY.md](plugins/project-kit/THIRD_PARTY.md).

Start a new project with: *"set up this repo with project-kit"* (the `init-project` skill).

The project gets **copies** of the templates, so it keeps working without the plugin, and the kit
never overwrites a project's own rules, knowledge or agents. After updating the plugin
(`/plugin update project-kit`), run `kit-audit` in each project to pick up checker changes and
`sync-agents` to update catalog agents.

## Developing this repo

```bash
uv run --with pytest python -m pytest -q tests
```

```bash
claude plugin validate .
```

See [CLAUDE.md](CLAUDE.md) for the rules.

## License

[GPL-3.0-or-later](LICENSE). Copyright (C) 2026 AlvaroFalcon. Projects set up with the kit keep
their own license for their own content.
