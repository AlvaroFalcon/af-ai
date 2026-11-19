---
name: feature
description: Take a request from idea to verified change with the Research → Spec → Plan → Implement → Verify flow - product check, research, grilling of open questions, a spec in docs/specs with acceptance criteria, a plan in small steps, implementation by the domain agents and verification against the spec, with the owner's OK after the spec and after the plan. Use for any new feature or non-trivial change; it routes work too big for one spec to wayfinder.
---

# feature

The coordinator (the main session) runs this flow. Subagents cannot talk to the owner and cannot
start other subagents, so every question to the owner and every delegation happens here.

Agents named below are the kit's catalog agents (`product`, `researcher`, `planner`,
`verifier`, added with `project-kit:sync-agents`). If the project lacks one, do that step yourself
or with a general-purpose subagent given the agent's brief, and tell the owner it is missing.

## 0. Triage

- **Trivial** (a typo, a one-line fix, a rename, a config value; nothing to decide): skip the
  spec. Give a two-line plan, wait for OK, implement, run the checks. Done.
- **Too big or too foggy for one spec** (several sessions, many open decisions, unclear
  destination): propose `project-kit:wayfinder` to the owner and stop here. The map's
  destination is the spec(s) that come back to step 3.
- Otherwise continue.

## 1. Is it worth it? (`product`)

Ask `product` about the request. Bring its verdict to the owner in a few lines.
- **Don't build it / Reuse X / Build a smaller version:** the owner decides whether to accept the
  verdict. A dropped request ends here; record the reason with `project-kit:add-knowledge` if it
  is a product decision worth keeping.
- Its **open questions** go to step 3.

## 2. Research (`researcher`)

Brief `researcher` with the request, the scope agreed in step 1 and the questions only facts can
answer: what exists in the code, what the knowledge files say, how third parties behave. Run
independent questions as parallel subagents. Keep the findings with their sources and paths.

## 3. Spec (grilling + `docs/specs/`)

1. Grill the owner on the open questions from steps 1 and 2 with `project-kit:grilling`, until the
   frontier is empty.
2. Write `docs/specs/NNN-<slug>.md` from the `spec.md` next to this file (the skill's base
   directory is printed when it loads). `NNN` is the next free number; create `docs/specs/` if
   needed. Fill Problem, Value, Research, Decisions, Acceptance criteria and Out of scope; leave
   Plan and Verification for later. Acceptance criteria are observable and checkable: what a
   user or a test can see, not how it is built.
3. Status `draft`. Show the owner the spec (or its link) with a three-line summary.

**⛔ Wait for the owner's OK on the spec.** Change it and ask again if they change anything. Then
set Status `agreed` and write the date.

## 4. Plan (`planner`)

Give `planner` the spec. It returns small steps, each with its owning domain agent (from "Who to
ask" in `CLAUDE.md`), the files it touches and how it is checked. Write them into the spec's Plan
table and show it to the owner, with anything the planner flagged as a risk.

**⛔ Wait for the owner's OK on the plan.** Then Status `planned` and the date.

## 5. Implement (domain agents)

Status `in progress`. For each step, in order:
- delegate it to its owning agent with the spec's path and the step number;
- one step at a time, unless steps are independent and own different files;
- after each step, the checks the step names; `scripts/check_all.sh` green before moving on (or
  the project's equivalent from `CLAUDE.md`);
- anything learned that is not obvious from the code goes to knowledge in the same change
  (`project-kit:add-knowledge`).

If a step shows that the spec is wrong or incomplete, stop and bring it to the owner: change the
spec first, then the plan, then the code.

## 6. Verify (`verifier`)

Give `verifier` the spec and the changes. It checks each acceptance criterion and fills the
Verification section: pass, fail or not verifiable here, with evidence. A fail goes back to step 5.
Then Status `done`, and tell the owner, in their language: what changed, what was verified, and
exactly what they should test themselves.

Commit on a branch and open a PR as the project's rules say; link the spec in the PR.
