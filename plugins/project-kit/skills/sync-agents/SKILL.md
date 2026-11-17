---
name: sync-agents
description: Add ready-made agents from the project-kit catalog (such as the product advisor) to a project, or update the catalog agents it already imported to the kit's latest version while keeping each one's "Project notes". Use after updating the plugin, when the owner asks which kit agents exist, or to add one. Not for domain agents written for the project (use new-domain).
---

# sync-agents

The catalog is the `catalog/` folder next to this file (the skill's base directory is printed when
the skill loads). Each catalog agent is a finished file, the same in every project. The project
gets a **copy** in `.claude/agents/`, so it keeps working without the plugin.

A catalog agent starts with a marker line right after its frontmatter:

```
<!-- project-kit catalog: <name> v<N>. ... -->
```

Everything above `## Project notes` belongs to the kit. `## Project notes` and everything after
it belongs to the project and is never replaced. Agents without the marker are the project's own
and are never touched.

## 1. Compare (read-only)

For each `catalog/*.md` and each `.claude/agents/*.md`, classify:

| Agent | State | Proposal |
|---|---|---|
| in the catalog, not in the project | not imported | offer to add |
| marker version lower than the catalog's | outdated | update (show the diff of the kit part) |
| marker version equal, kit part differs | edited locally | show the diff; propose moving the local change to "Project notes", or keeping it |
| marker version equal, kit part identical | current | nothing |
| same file name, no marker | the project's own | never touch; if the name clashes with a catalog agent, say so |

Give the owner the table, in their language, with one line per agent saying what it does, and
**wait for their OK** on which agents to add or update.

## 2. Add an agent

1. Copy `catalog/<name>.md` to `.claude/agents/<name>.md` unchanged.
2. Knowledge the agent reads: for every `docs/knowledge/*.md` it cites that the project lacks,
   create it from `catalog/knowledge/<name>.md` if the catalog has one, else from the
   `knowledge.md` template of the `init-project` skill. Fill what the owner already said (with
   the date) and ask for the rest; leave unanswered bullets out rather than inventing them.
3. Register it in `CLAUDE.md`: a row in "Who to ask" (`| \`<name>\` | ask it about … | owns
   nothing (advisor) |` for read-only agents) and, for a new knowledge file, a row in "Where
   knowledge lives". If the project's README lists the agents, add it there too.
4. Ask the owner whether the agent needs project notes (for example, which goals matter most) and
   write them under `## Project notes`.

## 3. Update an agent

1. Replace everything above `## Project notes` with the catalog version, marker included.
2. Keep `## Project notes` and everything after it exactly as it was.
3. If the new version reads a knowledge file the project lacks, create it as in step 2.2.
4. Show the owner the diff and a one-line summary of what changed in the agent's behaviour.

## 4. Check

```bash
python3 scripts/check_docs.py
```

```bash
scripts/check_all.sh
```

Both must pass. Tell the owner that a new session is needed for added or updated agents to load.
Commit on a branch and open a PR only if the project's rules say so.
