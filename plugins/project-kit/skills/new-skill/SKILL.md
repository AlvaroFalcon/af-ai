---
name: new-skill
description: Turn a procedure the project repeats (a version bump, a migration, a release dry run, screenshots, a new endpoint or command) into a project skill in .claude/skills with its row in CLAUDE.md and the README. Use when the same multi-step work has been done twice, or a step was forgotten once and cost a fix.
---

# new-skill

A project skill is a checklist Claude follows instead of re-deriving the procedure. It pays off
when the procedure has steps that are easy to forget (a test to add, a doc to update, a version
to keep in sync).

## 1. Decide it is worth a skill

- Done at least twice, or a forgotten step already caused a bug or a red CI.
- Not a one-off, and not something a script alone can do. If a script can do all of it, write the
  script and make the skill one line that calls it, or skip the skill.
- Owned by one domain: say which agent uses it.

## 2. Write `.claude/skills/<name>/SKILL.md`

- Frontmatter `name: <name>` (the folder name) and a `description` that says **what** it does and
  **when to use it**, with the words a session would match on.
- Numbered steps, each one checkable: exact commands in their own fenced block, files to touch,
  the test to add, the docs to update.
- Put the rule *why* only where skipping a step would look reasonable ("the server applies new
  migrations on merge, so never edit a merged one").
- End with the verification (`scripts/check_all.sh`) and what to report to the owner.
- Helper scripts go in `scripts/` (tested like other code), not inside the skill folder, unless
  they are only for this skill.

## 3. Register it

- `CLAUDE.md` "Skills for repetitive work": `| \`<name>\` | Use it to … |`.
- README: mention it in backticks in the "Working with Claude Code" section.
- The owning agent's file: "changes of this kind go through the `<name>` skill".

## 4. Check

```bash
python3 scripts/check_docs.py
```
