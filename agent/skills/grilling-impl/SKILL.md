---
name: grilling-impl
description: Grill the user one decision at a time, turn the agreement into a plan document under docs/plans/, then delegate that plan to a named implementer and independently audit it with a named verifier. Use when the user wants to refine a plan before implementation, says “grill me, then implement” or “grillingの後に実装,” or explicitly invokes this skill. Use grilling for discussion-only requests.
---

# Grilling Impl

Conduct the workflow in the user's language.

The workflow has four stages: reach agreement, write the plan, implement and
verify, then close the plan. Do not skip a stage or reorder them.

## Preconditions

Require the named `implementer` and `verifier` agents before writing anything.
Writing the plan document itself requires `verifier`, so an unavailable agent
must surface before the first edit.

If either is unavailable, do not fall back to another agent. Tell the user to run
`agent/setup.py install` from this dotfiles repository and start a fresh session,
then stop.

## 1. Reach agreement

Read `../grilling/SKILL.md` and follow its interview rules.

Inspect the environment for facts. Ask the user only about decisions, one at a
time, with a recommended answer.

Do not move on while a material decision is unresolved. The plan document records
decisions; it is not the place to discover them.

## 2. Write the plan

Read `../implementation-docs-writing/SKILL.md` and follow it to write
`docs/plans/<slug>.md`. That document, not this session's transcript, is the
single source of truth handed to `implementer` and `verifier`.

- Put the accepted decisions in §4.1 前提とする決定 with links only. Reasons live
  in `docs/DESIGN.md`.
- If planning produces a new design decision, write it to `docs/DESIGN.md` first,
  then link to it from the plan.
- If `docs/DESIGN.md` or `docs/ISSUES.md` does not exist, record its absence in
  the §1.1 責務分担 table and keep going. Create `DESIGN.md` only when a new
  design decision needs a home.
- If the work needs more than ten steps, split it into several plan documents and
  implement them one at a time in dependency order.
- Run `verifier` against the plan document as implementation-docs-writing
  requires. Correct and re-verify at most twice.

Then present the plan document path together with its §2 目的・完了条件・非目標
and §5 手順一覧. Ask whether it represents the shared understanding and
implementation should begin. Do not implement before the user confirms.

## 3. Delegate and verify

Give `implementer` the plan document path, working directory, applicable
instructions, starting worktree state, and the §6 受け入れ検証 commands. Require
scoped implementation and verification without modifying unrelated work.

The plan document is the scope boundary. Allow `implementer` to write only the
状態 column of the §5 手順一覧表, since progress belongs in that table alone. If a
premise in the plan turns out to be wrong, require `implementer` to stop and
report instead of rewriting the plan; the main session updates the plan in
implementation-docs-writing's 更新 mode and hands off again.

Give the plan document, the resulting diff, and verification evidence to
`verifier`. Require strict read-only review against §2.1 完了条件 and §6 受け入れ
検証, and a `pass` or `changes-required` verdict. Only unmet requirements,
correctness defects, regressions, safety issues, and missing required
verification are blocking.

Consolidate blocking findings from `verifier` and the main session before
returning them to `implementer`. Allow at most two corrective handoffs in total,
and rerun `verifier` after every correction.

After `verifier` passes, review the diff in the main session and rerun the
required checks. If a blocking issue remains and the correction limit is
exhausted, do not fix it in the main session; report the remaining issue and all
unverified work.

## 4. Close the plan

Only after the implementation passes. Follow implementation-docs-writing's
§ライフサイクル.

List what must outlive the plan: new design decisions go to `docs/DESIGN.md`,
leftover defects and non-goals that will still be needed go to `docs/ISSUES.md`.
Make those moves following `../design-docs-writing/SKILL.md`.

Once the moves have landed, ask the user to confirm deleting
`docs/plans/<slug>.md`, and delete it only after they confirm. Never delete it
before the moves land.

If the user declines, leave the document in place and say that it now disagrees
with the code.
