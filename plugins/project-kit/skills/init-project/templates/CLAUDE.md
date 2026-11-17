# CLAUDE.md: {{PROJECT_NAME}}

Shared context for every Claude session and subagent working in this repo. Read it first. The
[README](README.md) describes the project; this file holds the working rules and tells you
**where knowledge lives and who to ask**.

## Working agreement with the owner

- Flow: **research → plan → implement**, in small increments. **Present the plan and wait for the
  owner's OK before implementing anything non-trivial.** Explain in {{OWNER_LANGUAGE}}; say what
  something means, not just its name.
- {{BRANCH_AND_PR_RULES}}
- {{HOW_THE_OWNER_TESTS}}

## Non-negotiable rules

{{NON_NEGOTIABLE_RULES}}
N. **All checks green before pushing:** `scripts/check_all.sh` (skill `check-all`).
N. **Language:** code, comments, README, CLAUDE.md, agents, skills and knowledge files are in
   English. {{USER_FACING_LANGUAGE_RULE}}

## Where knowledge lives

| Topic | File |
|---|---|
| Architecture, install, contributing | `README.md` |
{{KNOWLEDGE_ROWS}}

**Keep knowledge current.** When you learn something not obvious from the code, such as a
measurement, an API quirk, a CI failure cause or an owner decision, add it to the matching
`docs/knowledge/*.md` in the same PR, using the `project-kit:add-knowledge` skill. A new area of
work gets its own file and agent via `project-kit:new-domain`. `python scripts/check_docs.py`
(part of `scripts/check_all.sh` and CI) fails when knowledge, agents or skills are not linked
where they should be.

## Who to ask

The main session is the coordinator. Subagents cannot start other subagents. Delegate to the
domain agent in `.claude/agents/` whose area owns the files or the question. Ask several in
sequence when a feature crosses domains.

| Agent | Ask it about | Owns |
|---|---|---|
{{AGENT_ROWS}}

## Skills for repetitive work

Project skills live in `.claude/skills/`. Kit skills come from the `project-kit` plugin.

| Skill | Use it to |
|---|---|
| `check-all` | Run every CI check locally with one summary. |
{{SKILL_ROWS}}
| `project-kit:add-knowledge` | Record a non-obvious fact in the right knowledge file, with its source. |
| `project-kit:new-domain` | Add a new area of expertise: knowledge file, agent and their rows here. |
| `project-kit:new-skill` | Turn work done twice into a project skill. |
| `project-kit:sync-agents` | Add kit catalog agents (e.g. `product`) or update the ones already imported. |
| `project-kit:kit-audit` | Check this setup against the kit's conventions and update `scripts/check_docs.py`. |

## Commands

```bash
scripts/check_all.sh
```

```bash
python scripts/check_docs.py
```
{{EXTRA_COMMANDS}}
