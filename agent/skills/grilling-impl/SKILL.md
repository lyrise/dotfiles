---
name: grilling-impl
description: Grill the user one decision at a time, then delegate approved implementation to an available Claude- or GPT-family subagent. Use when the user wants to refine a plan before implementation, says “grill me, then implement” or “grillingの後に実装,” or explicitly invokes this skill. Use grilling for discussion-only requests.
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

Delegate implementation to one available Claude- or GPT-family subagent.
Give it the brief, working directory, applicable instructions, current worktree
state, and verification commands. Require it to implement and verify the change
without modifying unrelated work.

Review the resulting diff in the main session, run the required checks, and
report any unverified work.
