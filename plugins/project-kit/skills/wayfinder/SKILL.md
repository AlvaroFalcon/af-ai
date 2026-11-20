---
name: wayfinder
description: Plan a chunk of work too big or too foggy for one session as a shared map of decision tickets on GitHub issues (a map issue with sub-issues, shown on a GitHub Project board), then resolve them one per session until the way to the destination - usually a spec - is clear. Use only when the owner explicitly asks for wayfinder or for a map: with a loose idea to chart, or with a map to work through ("work through the map <link>"). Never start a map on your own initiative.
---

# wayfinder

Adapted from Matt Pocock's `wayfinder` skill (MIT, see `THIRD_PARTY.md` at the plugin root).

A loose idea has arrived, too big for one session and wrapped in fog: the way from here to the
**destination** isn't visible yet. Wayfinding finds that way instead of charging at the
destination. It charts the way as a **map** on the repo's GitHub issues, then works its
**decision tickets** (questions whose answer is a decision, not slices of a build) one at a time
until the route is clear.

Naming the destination is the first act of charting, and it fixes the scope. In a project that
uses `project-kit:feature`, the destination is normally **one or more specs** in
`docs/specs/` ready for the Plan phase. It can also be a decision to lock, or a change made in
place.

## Plan, don't do

Each ticket resolves a decision; the map is done when nothing is left to decide. The pull to just
do the work is the signal that you have reached the edge of the map: hand off to `feature`
(Plan → Implement → Verify). The map's **Notes** may override this and carry execution into the
map.

## Refer by name

In everything the owner reads, refer to a map or ticket by its **title**, with the link inside
it: [Choose the save format](link), never a bare `#42`. A wall of numbers is illegible.

## Where the map lives

**GitHub issues are the source of truth; a GitHub Project is the board.**

- The map is one issue with the label `wayfinder:map`. Its tickets are its **sub-issues**
  (create each with the map as parent), each with one `wayfinder:<type>` label. Every map and
  ticket also carries the plain label `wayfinder`, which the board filters on. Those are the only
  labels a map and its tickets carry: they are decisions, not implementation work.
- **Blocking:** a line at the end of the ticket body, `Blocked by: #12, #15`. Use GitHub's native
  issue dependencies as well when the session's tools can set them. A ticket is **unblocked**
  when every ticket it names is closed.
- **Claiming:** assign the ticket to the owner driving the map, **first**, before any work, so
  that other sessions skip it. An open, unassigned ticket is unclaimed.
- **Frontier:** the open, unblocked, unclaimed sub-issues of the map, in sub-issue order.
- **Board:** the owner's GitHub Project shows the tickets as cards. Let GitHub add them: in the
  Project, *Workflows → Auto-add to project* for the repo with the filter `is:issue label:wayfinder`,
  and *Item closed → Done*. Auto-add only picks up issues created or updated after it is turned
  on. Never depend on editing the Project from the session: its API needs permissions that
  sessions usually lack.
- If a `wayfinder:*` label is missing, create it, or ask the owner to, when the project manages its
  labels as code (for example in a labels workflow).
- **No GitHub access:** fall back to one markdown file per map, `docs/maps/<slug>.md`, with the
  same sections and a `## Tickets` list (`- [ ] **Title** (type) - Blocked by: …`). Say so to the
  owner; parallel sessions are not safe there.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed; they
are the open sub-issues.

```markdown
## Destination

<what reaching the end looks like: the spec(s), decision or change. One or two lines.>

## Notes

<domain; agents and skills every session should use; standing preferences for this effort>

## Decisions so far

<!-- one line per closed ticket: enough to judge relevance; the detail lives in the ticket -->
- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- in-scope fog you can't ticket yet; it graduates into tickets as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination, with why; it never graduates -->
```

The map is an **index**, not a store: a decision lives in exactly one place, its ticket. The map
only gists it and links.

### Tickets

The body is the question, sized to one session:

```markdown
## Question

<the decision or investigation this ticket resolves>

Blocked by: #<n>, #<m>
```

The answer is not part of the body: it is the **resolution comment**. Assets made while resolving
a ticket (a prototype, a long research note) are linked from the comment, not pasted in.

## Ticket types

Every ticket is **HITL** (worked with the owner, who speaks for themselves) or **AFK** (the agent
alone). A HITL ticket resolves only through that live exchange: never answer the owner's side.

- **Research** (AFK, `wayfinder:research`): a fact a decision waits on, from the code, the docs,
  a third-party API or the web. Resolved by a subagent with a fresh context: the project's
  `researcher` agent if it has one, otherwise a general-purpose subagent with the question and
  where to look. The findings, with sources, are the resolution comment.
- **Prototype** (HITL, `wayfinder:prototype`): a cheap, rough, concrete thing to react to (an
  outline, a mock-up, a stub, a throwaway scene or script) when "how should it look or behave" is
  the question. Push code prototypes to the session's own branch without opening a PR and link
  the commit; keep them out of the main code paths.
- **Grilling** (HITL, `wayfinder:grilling`, the default): a conversation with the owner. Use
  `project-kit:grilling`.
- **Task** (AFK or HITL, `wayfinder:task`): work that must happen before a decision can be made
  (sign up for a service to judge its API, get access, export data to see its shape). Do it alone
  where you can; otherwise give the owner a precise checklist. The resolution records what was
  done and the facts later tickets need (where credentials are kept, URLs, counts), never a
  secret's value.

## Fog of war

The map is deliberately incomplete. Beyond the live tickets lies the **fog**: decisions you can
tell are coming but can't yet phrase, because they hang on open questions. Resolving a ticket
clears the fog ahead of it.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you
can answer it now. A sharp question becomes a ticket even if blocked; a vague one stays in
**Not yet specified**. Don't pre-slice the fog: one patch may become several tickets, or none.

## Out of scope

The destination fixes the scope; work beyond it is not fog. When a ticket turns out to sit past
the destination, close it as *not planned* and add one line to **Out of scope** (gist, why, link).
It does not go into Decisions so far, which records the route actually walked.

## Invocation

Two modes. Either way, **resolve at most one ticket per session**, except research tickets.

### Chart the map

The owner invokes it with a loose idea.

1. **Is it worth it?** If the project has the `product` agent, ask it about the idea first and
   take its verdict and open questions into the grilling. A "don't build it" ends here.
2. **Name the destination** with `project-kit:grilling`: what this map is finding its way to.
3. **Map the frontier.** Grill again, **breadth-first**: across the whole space rather than deep
   on one thread, to surface the open decisions and the first steps takeable now. If there is no
   fog (the whole journey fits one session), you don't need a map: say so and propose
   `project-kit:feature`.
4. **Create the map** issue (labels `wayfinder` and `wayfinder:map`): Destination and Notes filled in, Decisions so far
   empty, the fog in **Not yet specified**.
5. **Create the tickets you can specify now** as sub-issues of the map. Then, in a **second
   pass**, write the `Blocked by:` lines and any cross-references with the real issue numbers
   (a placeholder `#<n>` would link to an unrelated issue).
6. **Fire the research tickets**: one subagent per research ticket, in parallel, each posting its
   findings as the resolution comment and closing its ticket; then append them to Decisions so
   far.
7. Stop. Give the owner the map's link, the frontier by name, and how to continue: a new session
   with "work through the map <link>". Charting resolves nothing by hand.

### Work through the map

The owner invokes it with a map (link or number) and optionally a ticket. Without one, you pick.

1. Load the **map** body and its open sub-issues (titles, labels, assignees, `Blocked by:`), not
   every ticket body.
2. Choose the ticket: the one named, else the first frontier ticket. **Claim it** (assign it)
   before any work.
3. Resolve it as its `wayfinder:<type>` label says (the body never states the type). Zoom as
   needed: read the full body of a related or closed ticket on demand; use the agents and skills
   the map's **Notes** name.
4. Record the resolution: post the answer as a **resolution comment**, **close** the ticket, and
   append a line to the map's **Decisions so far**.
5. Update the map: create the newly surfaced tickets (create, then wire `Blocked by:`); graduate
   fog that is now specifiable, removing it from **Not yet specified**; rule out of scope what now
   sits beyond the destination; update or close tickets the decision invalidates.
6. Tell the owner, by name, what was decided, what is now on the frontier, and what to open next.

The owner may run unblocked tickets in parallel sessions: expect the issues to change under you,
and re-read a ticket before closing it.

### When the map is done

No open tickets and nothing left in **Not yet specified**: the way is clear. Write the
destination (for example the spec, with `project-kit:feature` from its Spec step, citing the
tickets as its research), add the lasting decisions to the project's knowledge
(`project-kit:add-knowledge`), and close the map with a final comment linking the result.
