# CLAUDE.md: af-ai

Rules for sessions working on this repo of Claude Code plugins. The [README](README.md) explains
what the plugins do.

## Working agreement with the owner

- Research → plan → implement, in small increments. Present the plan and wait for the owner's OK
  before anything non-trivial. Explain in Spanish.
- Develop on a `claude/...` branch and open PRs to `main`. Never push to `main`.

## Rules

1. **Generic only.** Nothing project-specific (names, paths, services, rules of one project)
   goes into the plugins. Examples in skills use neutral names.
2. **Projects own their copies.** `init-project` copies templates into the project; skills never
   make a project depend on the plugin being installed to pass its CI. Skills never overwrite a
   project's `CLAUDE.md`, knowledge, agents or skills.
3. **Section headings are an interface.** `templates/check_docs.py` reads "Where knowledge lives",
   "Who to ask" and "Skills for repetitive work". Changing them means changing the template
   `CLAUDE.md`, the checker, its tests and `kit-audit` together.
4. **One version.** Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json` and its entry
   in `.claude-plugin/marketplace.json` together (`tests/test_check_docs.py` checks they agree).
   Patch for wording, minor for new skills or checker behaviour.
5. **Checks green before pushing:** the pytest suite and `claude plugin validate .` (CI runs the
   tests).
6. **Language:** everything in the repo is in English.

## Layout

| Path | What |
|---|---|
| `.claude-plugin/marketplace.json` | The marketplace (`af-ai`) listing the plugins. |
| `plugins/project-kit/` | The project-kit plugin: `skills/*/SKILL.md`. |
| `plugins/project-kit/skills/sync-agents/catalog/` | Ready-made agents (marker `project-kit catalog: <name> v<N>`, bump N on change) and the knowledge seeds they need. |
| `plugins/project-kit/skills/init-project/templates/` | Files copied into projects: `CLAUDE.md`, knowledge, agents, `check_docs.py`, `check_all.sh`. |
| `tests/` | Tests of the checker template and the manifests. |
