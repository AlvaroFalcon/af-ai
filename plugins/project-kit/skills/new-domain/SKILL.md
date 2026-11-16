---
name: new-domain
description: Add a new area of expertise to a project set up with the kit - its knowledge file, its domain agent, and its rows in CLAUDE.md and the README - without overlapping existing agents. Use when work starts on something no existing agent owns. Not for a single fact (add-knowledge) or a sub-feature of an existing domain.
---

# new-domain

## 1. Check that it really is new

Read the "Who to ask" table in `CLAUDE.md` and the scope of every agent in `.claude/agents/`.
- If an existing agent already owns most of the files and questions, extend that agent instead
  (its scope and its knowledge file).
- Otherwise write down the boundary: which files and questions move to the new domain and what
  stays with the neighbours.

**Present the proposal to the owner before creating anything.** A new agent changes how work is
routed.

## 2. Create the knowledge file

`docs/knowledge/<domain>.md`, from the `knowledge.md` template of the `init-project` skill
(in this plugin, `skills/init-project/templates/`). Seed it with what is already known, with
sources, and the reasons behind any decision taken.

## 3. Create the agent

`.claude/agents/<domain>.md`, from `agent.md` (or `advisor-agent.md` for advice only), using an
existing agent of the project as a model for tone and depth.
- `name` equals the file name; `description` is one dense sentence the coordinator matches on.
- Minimum tools. Advisors get no Edit, Write or Bash.
- "Before doing anything, read": `CLAUDE.md`, its knowledge file, neighbour knowledge it needs.
- Scope with explicit hand-over points; how it works; what it verifies before finishing.

## 4. Register it

- `CLAUDE.md` "Where knowledge lives": a row for the knowledge file.
- `CLAUDE.md` "Who to ask": `| \`<domain>\` | ask it about … | owns … |`. Adjust neighbours'
  "Owns" if files moved. Files that don't exist yet are marked "(planned)".
- README "Working with Claude Code": the agent in the list.

## 5. Check

```bash
python3 scripts/check_docs.py
```

```bash
scripts/check_all.sh
```

Then tell the owner, in their language, what the new agent does and what it doesn't, and that a
new session is needed for it to load.
