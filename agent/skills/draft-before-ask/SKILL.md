---
name: draft-before-ask
description: Disclose every open decision behind a change as a numbered draft — a recommendation plus its strongest alternative — before asking anything, then settle only what the user contests and implement. Use when the user wants a change designed and built without being interviewed about decisions they would have accepted anyway.
---

The goal is **full disclosure at the lowest reply cost**. Every decision still open gets put in front of the user as a draft they can accept, reject, or skim past — and answering costs them a number, not an essay.

This is a sibling of `grill`. That workflow asks about every decision and waits. This one answers every decision first, and asks only about the ones the user pushes back on.

Nothing is hidden. There is no class of decision this workflow settles quietly on the user's behalf: the cost of a decision they never saw is far higher than the cost of a line they skim past.

## Phase 1 — enumerate before drafting

Enumerate every open decision behind the change, and do **all** environment exploration up front, before posting a single draft. The user should never be waiting on a tool call.

A decision is open if reversing it would change what gets written. That includes the ones you are confident about — confidence is a reason to recommend, never a reason to omit.

Revise the list as exploration deepens; a deep branch is exactly where a forgotten decision hides. Do not post until the list stops growing.

Recurring process preferences — whether to commit, how to split commits, which checks to run — are not design decisions. They belong in whatever long-lived instruction or memory file this environment already provides. Act on what is recorded there rather than drafting it.

## Phase 2 — post every draft at once

One message, every open decision, **numbered**. The number is how the user replies: "3 and 7" must be a complete and sufficient answer.

Order by **how likely the user is to object**, most contentious first, so an objection arrives as early as possible. Then split their attention across that order.

- **The contentious entries get the full treatment**: the decision in a sentence, your recommendation, **the single strongest alternative in one sentence**, and the reasoning — including the honest cost of the recommendation where there is one. Never omit the alternative here. Without one the user has to construct it themselves before they can judge, which costs more than reading the one you supply.
- **Everything below gets one line**: the decision, and what you chose. No alternative, no reasoning.

Do not draw the line by counting to a fixed number. Draw it where the entries stop being arguable — if you cannot say what a reasonable person would prefer instead, it belongs in the one-line tail. State how many entries are in each tier so the user knows what they are skimming.

The order is a judgement call and you will sometimes get it wrong. That is survivable precisely because the tail is still visible: if the user asks for the alternative behind a one-liner, give it. A misjudged order costs one exchange, not a rewrite.

**Show evidence at the right grain.** If an entry turns on a small, self-contained fact, quote the code or prose inline — a link makes the user leave the conversation to see it. If it turns on something broad — a ten-line design, several interacting types, a dependency web — quote nothing and link instead, because an excerpt would mislead.

Then wait. The drafts are a proposal, not a notification. Do not begin implementing until the user has replied.

## Phase 3 — settle only what was contested

Take the numbers the user pushed back on and work them one at a time, waiting for each answer. Everything they did not mention is settled.

Offer concrete options and a recommendation. When the answer narrows to four or fewer distinct options, use the toolset's picker (`AskUserQuestion` in Claude Code, `request_user_input` in Codex) so answering costs a keystroke. Otherwise ask in prose — never pad, merge, or drop candidates to force a menu, and don't hand-roll one when no picker is available.

**Never graft.** Do not build a question around a decision the user already accepted and append the real question at the end as "related, cheap" or "agreed?". Start at the contested point itself and give one or two sentences of context, no more.

An answer here can invalidate entries further down the list. Re-post those, renumbered, rather than letting a stale draft stand.

## Phase 4 — implement

Implement the settled list. Dependencies govern the order, not contentiousness.

If the user objects to something mid-build, rework what it touched. The branch is the safety net and no other containment machinery is needed, because every decision in the build was on the list they read.

## Phase 5 — hand back a map

Present a **decision-to-diff map**: each numbered decision paired with where it landed — file, anchor, rough size. The user then checks the decisions they cared about instead of reading the whole diff to find them.

**Prefer anchors that cannot drift.** Name the function, type, heading, or test case, and attach the line number as a convenience: "the `--strict` branch in `parse_args` (`src/cli.rs:212`)". If the name and the number ever disagree, the name still lands the user in the right place.

**Resolve every line number after the last edit.** Read them off the new-file side of `git diff` hunk headers — the `+` number in `@@ -old,n +new,m @@` — or grep the finished file for a unique string from the change. Numbers noted while editing are stale: every later insertion above them shifts them, and the shifts accumulate silently across a multi-file build.

Finally, check the map against the list. Every numbered decision from phase 2 should appear, and every entry should point at something that exists in `git diff`. A decision that landed nowhere is either dead or forgotten — say which.
