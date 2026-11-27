---
name: create-pr
description: Open or update the pull request for the current branch with a fixed description - what's new, what changed, what to test, acceptance criteria and notes - after merging the base branch in and running the project's checks, linking the spec and copying its acceptance criteria when there is one. Use whenever a PR is to be created or its description refreshed ("open the PR", "create a PR"). Never pushes to the base branch.
---

# create-pr

Opens a PR from the current branch into the project's base branch (normally `main`; `CLAUDE.md`
says if it is another) with the same description format every time. **Never push to the base
branch**: the PR is how work reaches it.

## Steps

1. **Branch check.** `git branch --show-current` must not be the base branch. If it is, stop and
   ask the owner which branch to use. Commit pending work first, only the files you changed.
2. **Bring the base in.** `git fetch origin <base>`, then `git merge --no-edit origin/<base>`: a
   merge, never a rebase or a force-push. Resolve conflicts; regenerate generated files with their
   own tooling.
3. **Prove it.** Run the checks `CLAUDE.md` names for a change (`scripts/check_all.sh` in kit
   projects; otherwise the project's test command, or the suites the change touches). Note which
   ran, their result, and any known flake you re-ran and why: this goes into the description,
   honestly.
4. **Push the branch.** `git push -u origin <branch>`.
5. **Read what the PR contains.** `git log --oneline origin/<base>..HEAD` and
   `git diff --stat origin/<base>...HEAD`, then the diff itself. Describe only what is in that
   diff, not work already merged.
6. **Find the spec.** If the work follows a spec (`docs/specs/NNN-<slug>.md`, named in the
   commits, the branch or the conversation), link it and copy its acceptance criteria, ticked
   where the Verify step passed them.
7. **One PR per branch.** If an open PR exists for the branch, update its body instead of opening
   a second one. A merged or closed PR is never reused.
8. **Open the PR** against the base with a short imperative title and the body below, in the
   language `CLAUDE.md` sets for GitHub text (if it sets none, the owner's language). Give the
   owner the full PR link and offer to watch it.

## Description template

Section titles go in that same language; the order and content stay the same. In English:

```markdown
## What's new
<!-- What the user or developer gets that didn't exist before. 1–4 bullets, plain words. -->

## What changed
<!-- Behaviour that is different now, grouped by area, naming the main files.
     Include what was removed or disabled and what deliberately stayed. -->

## What to test
<!-- Concrete steps the owner can follow: where to go, what to do, what they should see.
     Then the automated checks that ran, with their result. -->
- [ ] ...

**Automated checks:** <what ran and the result; flakes re-run and why>

## Acceptance criteria
<!-- Checkable statements that must all be true to merge; from the spec when there is one. -->
- [ ] ...

## Notes
<!-- Optional: the spec link, risks, follow-ups, open questions, docs or knowledge updated. -->
```

Rules for the body:
- Every "What to test" step is something a person can do; every acceptance criterion is
  something a person or a test can check as true or false. Observable, not "works well".
- Report check results faithfully: a failed or skipped check is stated, never hidden.
- No credentials, tokens, internal hostnames or model identifiers.
- End with the attribution lines the session gives, if any.
