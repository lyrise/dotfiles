---
name: grilling-impl
description: Grill the user one decision at a time, then delegate approved implementation to a named implementer and independently audit it with a named verifier. Use when the user wants to refine a plan before implementation, says “grill me, then implement” or “grillingの後に実装,” or explicitly invokes this skill. Use grilling for discussion-only requests.
---

# Grilling Impl

Conduct the workflow in the user's language.

## Reach agreement

Read `../grilling/SKILL.md` and follow its interview rules.

Inspect the environment for facts. Ask the user only about decisions, one at a
time, with a recommended answer.

After resolving every material decision, present a concise implementation brief:

- objective;
- accepted decisions;
- scope and non-goals;
- source-of-truth files;
- required verification;

Ask whether the brief represents the shared understanding and implementation
should begin. Do not implement before the user confirms.

## Delegate and verify

Require the named `implementer` and `verifier` agents. If either is unavailable,
do not fall back to another agent. Tell the user to run `agent/setup.py install`
from this dotfiles repository and start a fresh session, then stop.

Give `implementer` the brief, working directory, applicable instructions,
starting worktree state, and verification commands. Require scoped implementation
and verification without modifying unrelated work.

Give the resulting diff and verification evidence to `verifier`. Require strict
read-only review and a `pass` or `changes-required` verdict. Only unmet
requirements, correctness defects, regressions, safety issues, and missing
required verification are blocking.

Consolidate blocking findings from `verifier` and the main session before
returning them to `implementer`. Allow at most two corrective handoffs in total,
and rerun `verifier` after every correction.

After `verifier` passes, review the diff in the main session and rerun the
required checks. If a blocking issue remains and the correction limit is
exhausted, do not fix it in the main session; report the remaining issue and all
unverified work.
