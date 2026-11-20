---
name: grilling
description: Interview the owner in rounds until every decision of a plan, spec or idea is settled - numbered questions, each with a recommended answer, worded so "yes" accepts it, while subagents look up the facts. Use when a request has open questions, before writing a spec, for a wayfinder grilling ticket, or when the owner asks to be grilled or to stress-test an idea.
---

# grilling

Adapted from Matt Pocock's `grilling` skill (MIT, see `THIRD_PARTY.md` at the plugin root).

Interview the owner relentlessly until you reach a shared understanding. Map the work as a
**design tree**: every decision branches into the decisions that hang off it.

## Rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you can
ask now without guessing at answers you haven't heard yet. Ask the whole frontier in one round,
in the owner's language (see `CLAUDE.md`), then wait for the answers.

```
❓ **Q1 - <question title>**: <the question, with the options if there are several>

➡️ <your recommended answer and why, in one or two lines>

---

❓ **Q2 - <question title>**: ...

➡️ ...
```

- Word each question so that "yes" accepts your recommendation. The owner may be answering from a
  phone: keep each question short, and at most about six per round; the rest wait for the next.
- A question whose answer depends on another question still open in this round belongs to a later
  round.
- Each round reshapes the tree: settled decisions unblock the questions that hung on them.
  Recompute the frontier and ask the next round.

## Facts are yours, decisions are the owner's

Never ask the owner for something you can look up. When a question needs a fact (the code, the
docs, a third-party API, the web), send a subagent with a fresh context to find it: the project's
`researcher` agent if it has one, otherwise a general-purpose subagent with a precise brief. Don't
block on it: only the questions downstream of that fact wait; ask the rest of the frontier now.

The decisions are the owner's: put each one to them. Never answer your own questions, and never
turn a recommendation into a decision without the owner's yes.

## Done

The grilling is done when the frontier is empty: every branch visited, nothing left silently
assumed. Then:

1. Summarise the decisions in a short list and ask the owner to confirm the shared understanding.
2. Write them where they belong: the spec being written (`feature`), the ticket's resolution
   comment (`wayfinder`), or the project's knowledge with `project-kit:add-knowledge` (owner
   decisions, with today's date).

Do not act on the decisions before the owner confirms.
