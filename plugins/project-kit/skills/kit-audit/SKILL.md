---
name: kit-audit
description: Check a project's Claude Code setup (CLAUDE.md, docs/knowledge, .claude/agents, .claude/skills, scripts/check_docs.py, CI) against the project-kit conventions, update scripts/check_docs.py to the kit's latest version, and propose fixes. Use after updating the plugin, when a project was set up by hand, or when CLAUDE.md, agents and knowledge seem to have drifted apart.
---

# kit-audit

Read-only until the owner agrees. The project's own content (rules, knowledge, agents) is never
replaced by templates; only `scripts/check_docs.py` is a kit file that may be updated as a whole.

## 1. Compare

- `scripts/check_docs.py` vs `templates/check_docs.py` of the `init-project` skill (this plugin):
  diff them. Keep the project's settings block; everything else follows the kit.
- `CLAUDE.md` has the sections "Working agreement", "Non-negotiable rules", "Where knowledge
  lives", "Who to ask", "Skills for repetitive work", with every knowledge file, agent and skill
  in its table.
- Every source path has exactly one owner in "Who to ask"; no two agents claim the same files.
- Each agent reads `CLAUDE.md` and its knowledge file first, has minimum tools, and ends with
  "checks green + knowledge updated".
- Knowledge files: facts have sources; no contradictions; volatile facts marked; nothing that is
  really a rule for every session (that belongs in `CLAUDE.md`).
- `scripts/check_all.sh` runs every CI step and `check_docs.py`; CI runs `check_docs.py`.
- Catalog agents (marked `<!-- project-kit catalog: ... -->`): outdated or edited ones, and
  catalog agents not imported yet. Fix them with `sync-agents`, not by hand.
- `.claude/settings.json` declares the kit (`enabledPlugins` has `project-kit@af-ai`), so cloud
  sessions load its skills; the working agreement in `CLAUDE.md` describes the feature flow.
- Procedures repeated in recent history (`git log`) that deserve a skill (`new-skill`).

## 2. Report and propose

Give the owner, in their language, a short list: what is fine, what drifted, what you propose to
change. Wait for OK.

## 3. Apply and check

Apply what was agreed, then:

```bash
python3 scripts/check_docs.py
```

```bash
scripts/check_all.sh
```
