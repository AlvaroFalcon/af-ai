---
name: add-knowledge
description: Record something learned that is not obvious from the code - a measurement, an API or service quirk, the root cause of a CI failure, an owner decision - in the right docs/knowledge (or docs/design) file, with its source, and keep every reference to it consistent. Use whenever such a fact appears, in the same PR as the change it relates to.
---

# add-knowledge

Knowledge that only lives in chat is lost at the next session. Write it down the moment it is
established.

## 1. Choose the file

Read the "Where knowledge lives" table in `CLAUDE.md` and pick the most specific file.
- An agreed design or owner decision about how a feature works → the matching `docs/design/*.md`
  if the project has them.
- A fact that fits no domain → a new domain (`new-domain` skill), not a miscellaneous file.

## 2. Look before you write

Search the file and the rest of the docs for the same topic
(`grep -rn "<keyword>" docs CLAUDE.md .claude`).
- **It already exists:** edit it in place. Correct numbers, add the new source, remove what is no
  longer true.
- **It contradicts an earlier fact:** replace the old fact. Say briefly what changed and when,
  e.g. "was 4 workers until 2026-06".
- **It is new:** add it under the most specific heading, or a new heading if none fits.

## 3. Write it in the house format (English)

- One fact per bullet, stated plainly, with concrete numbers or identifiers.
- **Source in the same bullet:** *measured on YYYY-MM-DD* (what the owner sent or what was run) ·
  *official docs* (link) · *verified in local tests / CI run* · *owner decision on YYYY-MM-DD*.
- **Volatile facts** (prices, free-tier limits, third-party behaviour) get "re-check before
  relying on it".
- Paths and identifiers in backticks, so the docs checker can verify them.
- Short. The code holds the details; knowledge holds the *why* and the non-obvious.

## 4. Propagate it

When the fact changes how work must be done, update where people and agents act on it:
- a rule for every session → `CLAUDE.md`;
- how a domain agent must work → its file in `.claude/agents/`;
- a step of a procedure → the matching project skill;
- user-visible behaviour → the README and, if shipped, the changelog.

A new file in `docs/knowledge/` or `docs/design/` gets a row in the "Where knowledge lives" table.

## 5. Check the links

```bash
python3 scripts/check_docs.py
```
