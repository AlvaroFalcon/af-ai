---
name: init-project
description: Set up a repository for coordinated Claude Code work - CLAUDE.md with working rules and routing, docs/knowledge files per domain, one agent per domain in .claude/agents, project skills for repetitive work, scripts/check_docs.py and scripts/check_all.sh wired into CI. Use when the user asks to initialise, bootstrap or "set up the kit / agents / knowledge" in a project. Not for adding one domain to a project already set up (use new-domain).
---

# init-project

Sets up the structure that makes long Claude Code projects work: rules every session reads,
knowledge that survives sessions, one agent per area of the code, skills for repeated procedures,
and a check that keeps them all linked.

The templates are in the `templates/` folder next to this file (the skill's base directory is
printed when the skill loads). Copy them; never link to the plugin from the project, because the
project must work without the plugin installed.

**Never overwrite** an existing `CLAUDE.md`, `.claude/agents/*`, `.claude/skills/*` or
`docs/knowledge/*`. If any exists, switch to `kit-audit` and merge instead.

## 1. Research the repo (read-only)

- Languages, frameworks, top-level folders, entry points.
- How it is tested and linted locally, and what CI runs (`.github/workflows/`, other CI files).
- How it is built, versioned and released (version files, CHANGELOG, tags, packaging).
- Existing docs: README, design notes, ADRs, comments that record decisions.
- External services and their constraints (APIs, databases, rate limits, secrets handling).

## 2. Ask the owner what only they know

Ask briefly, in one message, in the language they write in:
- Which language they want explanations in, and the language of user-facing text.
- Branch and PR rules (e.g. "develop on a branch, PR to main, never push to main").
- How they test changes (manually, staging, a device) and what they can send back.
- Rules that must never be broken (data that must not be lost, actions never to automate,
  secrets, production systems).

## 3. Propose the domains and wait for OK

A domain is an area with its own files, rules and knowledge. Propose a table:

| Agent | Owns (paths) | Ask it about |
|---|---|---|

Guidelines:
- 3–6 domains. Every source path belongs to exactly one owner. Split by what changes together and
  needs the same expertise, not by folder alone.
- A release/CI/packaging domain is almost always one.
- Add a **read-only advisor** (template `advisor-agent.md`) when the project depends on outside
  expertise that is not code (a market, a regulation, a game's mechanics).
- Offer the ready-made agents of the kit catalog (the `sync-agents` skill lists them). The flow
  of `feature` uses `product`, `researcher`, `planner` and `verifier`; recommend all four. Add the
  chosen ones in step 4 with `sync-agents`, which also seeds `docs/knowledge/product.md`.
- Propose the first project skills: always `check-all`; others only for procedures that already
  exist and are error-prone (version bump, migration, release dry run, screenshots).

**Present this to the owner and wait for their OK.** Adjust and present again if they change it.

## 4. Write the files

1. `CLAUDE.md` from `templates/CLAUDE.md`: fill every `{{…}}`; number the rules; one row per
   knowledge file, agent and skill. Keep the section headings exactly as in the template: the
   docs checker reads "Where knowledge lives", "Who to ask" and "Skills for repetitive work".
2. `docs/knowledge/<domain>.md` per domain from `templates/knowledge.md`, seeded with real facts
   found in step 1 (with their sources) and the owner's answers as decisions with today's date.
   No invented facts; an almost empty file is fine.
3. `.claude/agents/<domain>.md` per domain from `templates/agent.md` (or `advisor-agent.md`).
   `name` must equal the file name. The description is one dense sentence the coordinator matches
   on. Tools: the minimum; advisors get no Edit, Write or Bash.
4. `.claude/skills/check-all/SKILL.md` from `templates/check-all-skill.md`, plus any agreed
   project skill (use `new-skill` for each).
5. `scripts/check_docs.py` from `templates/check_docs.py` (adjust the settings block only, e.g.
   `README_LISTS_SKILLS = False` if the README should not list skills) and `scripts/check_all.sh`
   from `templates/check_all.sh`, with one `check` line per CI step. `chmod +x` it.
6. CI: add `python3 scripts/check_docs.py` to the existing workflow (or a minimal one if there is
   none). Don't restructure the owner's CI.
7. README: a short "Working with Claude Code" section listing the agents and project skills
   (the checker expects each project skill name in backticks there).
8. Catalog agents chosen in step 3: run `sync-agents` to add them.
9. `.claude/settings.json`: declare the kit so cloud and teammates' sessions load it (merge into
   the file if it exists; never drop existing keys):

   ```json
   {
     "extraKnownMarketplaces": {
       "af-ai": { "source": { "source": "github", "repo": "AlvaroFalcon/af-ai" } }
     },
     "enabledPlugins": { "project-kit@af-ai": true }
   }
   ```

   The project still passes its CI without the plugin; this only makes the kit skills available.

## 5. Verify

```bash
python3 scripts/check_docs.py
```

```bash
scripts/check_all.sh
```

Both must pass. Then tell the owner, in their language:
- what each agent does and doesn't;
- the rule "something learned that is not obvious from the code goes into knowledge, with its
  source, in the same PR";
- that they should restart the session (or start a new one) so the agents load.

Commit on a branch and open a PR only if the owner's rules say so.
