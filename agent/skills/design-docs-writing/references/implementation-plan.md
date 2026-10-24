# Implementation Plan

When writing, revising, checking, or folding `docs/plans.md` and `docs/plans/<slug>.md`, follow this document.
`<slug>` is a short kebab-case name for the work.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to implementation plans.

These rules protect three things.
The implementer (human or AI agent) can get to work by reading this document alone.
Someone other than the implementer can judge whether it is finished.
When the plan disappears, the decisions made there, the vocabulary, and what was confirmed about the outside world are not lost.

In this document, "the design documents" means `docs/design.md` and the `docs/design/*.md` linked from it.
Follow §1.1 of `docs/design.md` to identify the design document responsible for the plan's concern.

When a new design decision is made while drawing up the plan, write it first in the design decisions section of the design document responsible for that concern, and put only the conclusion and a link in the plan.
Cross-cutting decisions have `docs/design.md` as their authoritative source, and decisions confined to one concern have the existing detail document.
If there is no corresponding detail document, `docs/design.md` is the authoritative source.
When a new term is decided, write it in `docs/terms.md`.
Do not split design documents on the back of creating or completing a plan; if a split is needed, handle it separately as an update under the [Design Document](design-document.md) rules.

## Shape of the Parent Document

What `docs/plans.md` holds is the list of work in progress and the dependencies between pieces of work.

The reason the parent holds the dependencies is that the order cannot be read from the children alone.
Dependencies between plans are written only in §4.1 of the later one (§"Granularity of Plans"), so knowing the order of the work running now would mean opening every plan.

Put the following at the top.

1. What this document covers (work in progress and its dependencies) and what it does not (the content of each piece of work is in the children; finished work lives in the code and git history)
2. How to use it (add a row before starting, advance the status, delete the row once folded)

In §1.1, write what this document holds and what it does not, and link the family map to `[design.md](./design.md#11-document-responsibilities)`.

Then put the list table.
The four columns are Plan, Purpose, Status, and Prerequisite.

| Column | What to write |
| --- | --- |
| Plan | A relative link to the child. The displayed text is the `<slug>` |
| Purpose | The purpose in §2 of the child, condensed to one line |
| Status | `not started`, `in progress`, `done` |
| Prerequisite | The `<slug>` of a plan that must be finished first. `-` if none |

```markdown
| Plan | Purpose | Status | Prerequisite |
| --- | --- | --- | --- |
| [storage-facade-split](./plans/storage-facade-split.md) | Listing 1000 items returns within 200 ms | in progress | - |
| [storage-driver-retry](./plans/storage-driver-retry.md) | Writes are not lost on transient failures | not started | storage-facade-split |
```

When a plan is folded, delete its row (§"Folding a Plan").
Do not keep the history of finished work here.
Keeping it leaves a growing number of rows pointing to files that no longer exist, contradicting the principle that the code and git history are authoritative.

When the row of a `<slug>` written in the Prerequisite column disappears, that prerequisite is already satisfied.
Remove it from your own row's Prerequisite column too.

## Shape of Child Documents

```
1. About This Plan
   1.1 Document Responsibilities
   1.2 Creation Date and Target Commit
2. Purpose and Completion Criteria
   2.1 Completion Criteria
   2.2 Non-goals
3. Current State
4. Change Approach
   4.1 Assumed Decisions
   4.2 Scope of Impact
5. Steps
6. Acceptance Verification
7. Risks and Rollback
```

Sections 1 to 6 are required.
Include section 7 only when the plan contains changes that `git revert` does not undo; otherwise omit the heading entirely.
Number headings in the form `## 1.` `### 1.1`, and do not number `####`.

### 1. About This Plan

State in one or two sentences what this work is.

Write **1.1 Document Responsibilities** as a table.
List here only what this document holds, what it does not, and the documents this plan assumes.
Show the family map with a link to `[design.md](../design.md#11-document-responsibilities)`.

Links to design documents include the anchor of the heading the plan assumes.
For example, write `[design.md](../design.md#3-overall-structure)` for the overall structure, and `[storage.md](../design/storage.md#2-responsibilities-and-boundaries)` for the storage boundaries.
For vocabulary, point to `[terms.md](../terms.md)`; for bugs, `[issues.md](../issues.md)`; for external behavior, `[knowledge.md](../knowledge.md)`.

**1.2 Creation Date and Target Commit** is required.
The steps are written assuming the current code, and cannot be read without knowing the point in time.

### 2. Purpose and Completion Criteria

Write the purpose as what changes from the perspective of users or operations, not as a restatement of the implementation.
"Introduce a cache layer" is an implementation; "listing 1000 items returns within 200 ms" is a purpose.

Write **2.1 Completion Criteria** as observable states to be reached, whose truth someone other than the implementer can judge.
Do not write how to check them in this subsection; §6 holds the commands to run and the expected results.
List the criteria numbered, and make them correspond one-to-one with the rows of §6.

The following are restatements of the implementation and cannot be judged, so they are not completion criteria.

- "Implement …"
- "… works"
- "Refactor …"

The work is complete when all of them are met.
For how to rewrite them, see §"Example: Rewriting Completion Criteria".

In **2.2 Non-goals**, list what was decided not to do in this work.
Do not confuse them with the out-of-scope items in `docs/design.md`.
Out of scope is a permanent decision not to build; a non-goal is merely not done in this work.
Move what will be needed in the future to a deferred item in the relevant design document or to `docs/issues/<slug>.md`, and then link to it.
If the plan is deleted while it stays a non-goal, nobody picks it up.

### 3. Current State

Write how the code in the range involved in the change stands now, using only facts confirmed in the code.
Limit the description to what affects the change; do not trace structure that can be read from the code, and point to it with links with line numbers.
Then write in one sentence why the current state is not enough.
Without this sentence, the reader cannot judge whether the steps are needed.

### 4. Change Approach

Write together what shape it will be changed into, before dividing it into steps.
Without the overall picture first, the intent of individual steps cannot be read.

Write **4.1 Assumed Decisions** as a table with two columns: the decision and a link to its authoritative source.
Do not write the reasons, since they are at the link target.
If a decision is not in the design document that is its authoritative source, add it to that document first, then list it in this table.

When plans have been split (§"Granularity of Plans"), the completion of the preceding plan is also an assumption and is listed in this table.
Write "`<preceding slug>` is done" in the decision column and a relative link to that plan in the link column.
When the preceding plan is done and deleted, remove this row too.

In **4.2 Scope of Impact**, write the components touched and what is not touched but is affected.
If there are externally visible changes (API, configuration files, storage formats), state them explicitly and write in one sentence whether compatibility breaks.

If externally visible names are added or changed, include updating `docs/terms.md` in the completion criteria of a step in §5.
A rename takes effect when the code is merged, so waiting until §"Folding a Plan" leaves `terms.md` lying the whole time.
It is a matter of fixing one row of the table, and including it in a step's completion criteria costs almost nothing.

### 5. Steps

Put a list table at the top.
The four columns are No., Content, Depends on, and Status, and the number is an anchor link to the item.
Status is one of `not started`, `in progress`, and `done`.

**Write progress only in this table.**
Do not write status in the body of each step or in any other section.
When it is written in two places, one always goes stale.

Write each step in the following form.

```markdown
<a id="s-1"></a>
### Step 1. Short title that conveys what is done

**Locations to change**
Existing files as links with line numbers. New files as the path and role.

**What to do**
What is changed and how. Do not restate the title.

**Completion criterion**
An observable event that tells this step is finished.
```

Write all three blocks.
Put the explicit anchor `<a id="s-1"></a>`.
Auto-generated heading anchors are long and break when the title is edited.

Order steps by dependency.
For steps that still work when reordered, leave the Depends on column of the list table empty.
A step with the Depends on column filled cannot be started until its dependencies are done.

Numbers are identifiers, not sequential numbers.
§"Identifiers" in the common rules requires items to be referred to by `<slug>`, but steps are confined to one plan and are not split into children, so these numbers are outside that rule.
When an update makes a step unnecessary, delete its row in the list table and its body, and do not close up the following numbers.
Renumbering shifts every `s-N` anchor and every reference in the Depends on column.
When adding a step, take the number after the largest one used, and insert it keeping only the order by dependency.

Make each step a unit after which the build and existing tests pass on their own.
For a step that spans an intermediate state that does not pass, state so explicitly.

### 6. Acceptance Verification

Turn each criterion in §2.1 into a procedure that confirms it is true.

Write it as a table with three columns: the criterion number in §2.1, the command to run, and the expected result.
Every criterion in §2.1 appears in one or more rows.
A criterion for which no corresponding row can be written is a criterion that cannot be judged in the first place; go back to §2.1 and rewrite it.
Do not repeat the wording of the criteria; refer to them by number.

Whereas a step's completion criterion looks at the end of that stage, this section looks at whether the whole work meets the requirements.

Write commands in a form that can be copied and run, and do not leave the expected result column empty.
A command without a result is not verification.

If new tests are added, write in one line what each test protects.
Do not write the test code.

### 7. Risks and Rollback

Changes that cannot be undone are data migrations, changes to published APIs, deletion of data, and changes applied to external services.

For each item, write what happens on failure and the steps to roll back.
For what cannot be rolled back, write that it cannot.
Knowing that something cannot be rolled back is different from assuming it can.

## Granularity of Plans

One plan covers one batch of changes that can be reviewed at once.
If the steps exceed 10, the work is too large; cut it along dependencies and split it.

When splitting, name each `<slug>` by what that plan does, not by a sequential number.
Use `storage-facade-split` and `storage-driver-retry`, not `refactor-storage-1` and `refactor-storage-2`.
With numbers, once one is done and disappears, nobody can tell what the remaining number continues.

Write dependencies between plans in §4.1 of the later one, not in the preceding one.
The preceding plan does not know about things created after it.
Write the same dependency in the Prerequisite column of `docs/plans.md` as well.
A child does not know about what comes after it, but the parent sees every row and can lay out the order.

## Four Modes

**Create**: read the code to confirm the current state, set up the shape of the child document (§"Shape of Child Documents"), fill in each section, and add a row to `docs/plans.md`.
Do not write in the body what could not be confirmed (§"Source of Evidence").
Do not treat it as finished while open questions remain.

**Update**: when a premise breaks during implementation, rewrite the steps before continuing.
Do not silently deviate from the plan.
An implementation that deviated cannot be verified by anyone later.
Advancing the status column of the steps list and the Status column of `docs/plans.md` does not count as rewriting the body and does not require this procedure.

**Check**: run §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

**Complete**: after the acceptance verification passes, move what is worth keeping, then delete the plan and remove its row from `docs/plans.md` (§"Folding a Plan").
Only in this mode is the deliverable the diff of the permanent documents receiving the content, not the plan.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- The purpose, and the criteria for judging it complete
- Non-goals, and why they were excluded from this work
- Facts about the current state that affect whether and how the change can be made
- Assumed decisions, and links to their authoritative sources
- Each step's locations to change, what to do, completion criterion, and dependencies
- The criterion numbers, commands, and expected results of the acceptance verification
- Changes that cannot be rolled back, and how to undo them

The following may additionally be deleted or merged.

- "What to do" that merely restates the step's title
- Descriptions of the current state that trace structure readable from the code
- The deliberation over alternatives not adopted (move it to the rejected alternatives in the design document responsible for that decision)

## Verification Subagent

Following §"Verification Subagent" in the common rules, replace the scope in which the `verifier` is required with the following.

It is required for creating; if it is unavailable, report without creating the plan.
For updates, it is required only when adding or deleting sections, changing completion criteria, adding or deleting steps, or changing the order of dependencies.
Rephrasing, relinking, updating the status column, or only adding or deleting rows of `docs/plans.md` does not require it.
This is an exception so that implementation does not stall midway; verify these together the next time a rewrite that requires it is made.
A check does not change the body and does not require it.
For completion, the required scope of each reference applies to the changes in the permanent documents receiving the content.

Replace the blocking findings with the following.

- Completion criteria are not observable
- The criteria in §2.1 and the rows of §6 do not correspond one-to-one
- A step lacks locations to change or a completion criterion
- The dependency order cannot be executed (a step depends on the result of a preceding step but is ordered before it)
- The description of the current state disagrees with the code
- The reason for a design decision is in the body but not in the design document that is its authoritative source
- The authoritative sources for design decisions, invariants, and deferred items do not match the division of responsibilities of the design documents
- Externally visible names change, but updating the terms documents is not in any step's completion criteria
- Open questions remain
- There is no row in `docs/plans.md`, or its Prerequisite column disagrees with §4.1
- Broken headings, anchors, or links
- An increase in character count after compression, when compression was requested

## What Not to Write

**The reasons for design decisions** are held by the design document responsible for that decision.
**Term definitions and reasons for names** are held by `terms.md`; this document only uses the terms.
**Details of confirmed bugs** are held by `issues.md`; refer to related ones by `<slug>`.
**How external things actually behave** is held by `knowledge.md`.
**Setup steps and dependency packages** are held by `README.md`.

Do not write **finished code**.
Function bodies, implementation pseudocode, and pasted diffs always drift during implementation.
If the plan becomes a draft of the code, the same thing is maintained in two places.

Code blocks are allowed only for the following two.

1. Quotes of existing code showing the current state (with a link with line numbers)
2. Signatures of newly decided types or interfaces (since they are themselves a contract)

## Source of Evidence

Follow §"Distinguishing the Source of Evidence" in the common rules, and in this document observe it especially strictly in the current state section and the completion criteria.
Writing an unconfirmed current state as an assertion makes every step built on it collapse.

When a step needs a premise that has not been confirmed, put the confirmation itself as step 1.
Investigating may be a step, and its completion criterion is written as what was learned.

## Lifecycle

- Write it before starting, and begin implementing after getting agreement
- When a premise breaks during implementation, rewrite the steps before continuing (§"Four Modes")
- Move new design decisions to the design document that is their authoritative source, new terms to `terms.md`, and leftover bugs to `issues.md`, and then link to them
- When the acceptance verification passes, fold the plan according to §"Folding a Plan"

Do not keep finished plans.
For implemented plans, the code and git history are authoritative, and a remaining document always disagrees with the code.

## Folding a Plan

Fold the plan when every acceptance verification in §6 passes and every entry in the status column of the list table is `done`.
Do not fold it if even one is not met.
Ending with something unmet means deciding not to do it; first move it to the non-goals in §2.2 and write why it was excluded.

Folding has three stages: move, confirm, delete.
Do not delete first.
After deleting, nobody can know what failed to be moved.

In **move**, go through the body one section at a time from the top, and move only what outlives the work, according to the following mapping.

| What is in the plan | Destination |
| --- | --- |
| Design decisions made during implementation, and their reasons | Decided items in the design decisions section of the design document responsible for that decision |
| Alternatives considered and rejected | The rejected alternatives of the same decision |
| Questions that could not be settled and were postponed | Deferred items in the design decisions section of the design document responsible for the question (always with a condition for deciding) |
| Invariants learned through implementation, and the conditions that break them | The relevant topic section of the design document responsible for that concern |
| Terms that appeared in implementation and are not yet in the terms documents' table | The term list of the terms documents |
| Naming decisions made during implementation (rejected names and reasons) | The term's entry in the terms documents |
| External behavior confirmed during implementation | File it as `docs/knowledge/<slug>.md`, and add a row to the list table of `knowledge.md` |
| Leftover bugs | File it as `docs/issues/<slug>.md`, and add a row to the list table of `issues.md` |
| Non-goals that will eventually be needed | A deferred item in the relevant design document, or `docs/issues/<slug>.md` |
| Non-goals decided never to be built | Out of scope in `design.md` |
| Acceptance verifications to keep running permanently | Tests or CI configuration. Do not move them into documents |

For the current state, scope of impact, steps, and risks and rollback, the code and git history are authoritative, and there is usually nothing to move.
After confirming there is nothing to move, do nothing.

Write in the destination according to each reference, and do not paste the plan's sentences as is.
The plan's sentences were written in the context of steps, and cannot be read once that context is gone.

In **confirm**, with the plan closed, read only the destinations and see whether the content makes sense.
Moved decisions must not point to step numbers or the `<slug>`.
Filed bugs must satisfy the five sections of §"Shape of Child Documents" in the [Issue List](issue-list.md).
Filed external facts must satisfy the three sections and the source label of §"Shape of Child Documents" in the [Knowledge Document](knowledge-document.md).
Moved terms must satisfy the six columns of the table and the conditions for entries in the [Terms Document](terms-document.md).
No links to the plan may remain anywhere.
Confirm the last one by `rg -n '<slug>' --glob '!docs/plans/**' .` being empty.

In **delete**, delete it with `git rm docs/plans/<slug>.md`, and also remove the row in `docs/plans.md` and any `<slug>` remaining in the Prerequisite column of other rows.
Include this in the same commit as the changes to the destinations.
If the commits are split, content is lost when only one of them is taken in.

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.
The confirmation when folding is defined in §"Folding a Plan".

1. Are §2.1 and each step's completion criterion observable? Are there no remaining criteria ending in "implement", "works", or "handle"?
2. Are the criteria in §2.1 numbered and one-to-one with the rows of §6? Is there no criterion in only one of them?
3. Does every step have the three blocks: locations to change, what to do, and completion criterion?
4. Is progress only in the status column of the list table? `rg -n -i '\b(completed|already done|already implemented|already addressed|already started|the rest is)\b|完了した|完了済み|実装済み|対応済み|着手済み|残りは' docs/plans/*.md` must be empty (it searches only for phrases that describe progress, so as not to pick up section names such as "Completion Criteria")
5. Are no open questions left? Search for "TBD", "to be considered", and "either" (「未定」「検討する」「どちらか」 in Japanese)
6. Are the reasons for design decisions absent from the body, do the places giving reasons link to the authoritative design document that matches the division of responsibilities, and do the design document links in §1.1 and §4.1 include the target file and heading anchor?
7. If §4.2 has additions or changes of externally visible names, is updating `terms.md` in the completion criteria of some step in §5?
8. Are non-goals written, and have those needed in the future been moved to the relevant design document or `issues.md`?
9. Is there a creation date and target commit?
10. Do references to code have line numbers? `rg -nH '\]\((\.\./)+[^)#]*\.[A-Za-z0-9]+\)' docs/plans/*.md | rg -v '\.md\)'` must be empty (it picks up links to code that lack `#L`, excluding `.md` links between documents)
11. Are no function bodies or pseudocode pasted? Do code blocks fit within the two exceptions in §"What Not to Write"?
12. Do the steps not exceed 10? If they do, split according to §"Granularity of Plans"
13. Have step numbers not been renumbered? Do all numbers referenced in the Depends on column and all `s-N` anchors in the body exist?
14. If this is a split plan, is the dependency on the preceding plan in §4.1?
15. Is section 7 missing despite changes that cannot be rolled back? Conversely, is there a section 7 with no changes that cannot be rolled back?
16. Are there no empty cells in the expected result column of §6?
17. Does `docs/plans.md` have this plan's row, and does its Prerequisite column match the preceding plans in §4.1?
18. Do the rows of `docs/plans.md` correspond one-to-one with `docs/plans/*.md`? Are there no remaining rows or prerequisites pointing to deleted plans?

## Example: Rewriting Completion Criteria

The left column restates the implementation and cannot be judged; for the right column, someone other than the implementer can confirm truth or falsity.

| Cannot be judged | Observable completion criterion |
| --- | --- |
| Implement a cache | p95 of listing 1000 items is under 200 ms |
| Fix error handling | `GET /items/{id}` for a nonexistent ID returns 404 and `{"code":"not_found"}` |
| Make the configuration readable | `port = 9000` in `config.toml` is applied at startup, and it listens on 9000 |
| Add tests | The branch for `rename` failure is covered by a test, and all existing tests pass |
| Refactor | `src/storage/facade.rs` does not reference `driver::` directly, and all existing tests pass |

What the right column has in common is that two things are pinned down: the target, and the value or state it must satisfy.
Rewrite any criterion that lacks either.

Do not write the confirmation procedure in the completion criterion itself; put it in the table in §6 with the criterion number and the expected result.
From the top, they correspond to `cargo bench items_list`, `cargo test api::not_found`, `ss -ltn`, `cargo test storage::`, and `rg 'driver::' src/storage/facade.rs`.

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| `1. About This Plan` | `1. この計画について` |
| `1.1 Document Responsibilities` | `1.1 文書間の責務分担` |
| `1.2 Creation Date and Target Commit` | `1.2 作成日と対象コミット` |
| `2. Purpose and Completion Criteria` | `2. 目的と完了条件` |
| `2.1 Completion Criteria` | `2.1 完了条件` |
| `2.2 Non-goals` | `2.2 非目標` |
| `3. Current State` | `3. 現状` |
| `4. Change Approach` | `4. 変更方針` |
| `4.1 Assumed Decisions` | `4.1 前提とする決定` |
| `4.2 Scope of Impact` | `4.2 影響範囲` |
| `5. Steps` | `5. 手順` |
| `6. Acceptance Verification` | `6. 受け入れ検証` |
| `7. Risks and Rollback` | `7. リスクと巻き戻し` |
| Parent columns `Plan` / `Purpose` / `Status` / `Prerequisite` | `計画` / `目的` / `状態` / `先行` |
| Status `not started` / `in progress` / `done` | `未着手` / `進行中` / `完了` |
| Steps table columns `No.` / `Content` / `Depends on` / `Status` | `番号` / `内容` / `依存` / `状態` |
| `### Step 1.` | `### 手順 1.` |
| `**Locations to change**` | `**変更する箇所**` |
| `**What to do**` | `**やること**` |
| `**Completion criterion**` | `**完了条件**` |
| "`<preceding slug>` is done" | 「`<先行の slug>` が完了していること」 |
