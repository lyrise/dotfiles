# External Knowledge

When writing, revising, or checking `docs/knowledges.md` and `docs/knowledges/<slug>.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to external knowledge.

This document covers how dependency libraries, the OS, protocols, external APIs, and runtime environments actually behave.
The structure of and design decisions about our own code are held by design documents, and bugs in our own code by `issues.md`.

There are three reasons to make this family independent.
External behavior is a premise of design decisions, not a design decision itself.
Embedded in the prose of a design document, it cannot be looked up for what to recheck when upgrading a dependency.
Written in a plan, it disappears when the plan is folded.

## Shape of the Parent Document

Put the following at the top.

1. What this document covers (facts confirmed about the outside world) and what it does not (matters of our own code go in design documents and `issues.md`)
2. How to use it (rewrite when the outside changes; do not keep old descriptions; reread `Literature only` items every three months)

In §1.1, write what this document holds and what it does not, and link the family map to `[design.md](./design.md#11-document-responsibilities)`.

Then put the list table.
The four columns are Item, Target, Source, and Last checked.

| Column | What to write |
| --- | --- |
| Item | A relative link to the child. The displayed text states the fact in one line |
| Target | A string that pins down the version or edition (`tokio 1.47.1`, `macOS 15.6`, `Stripe API 2026-04-10`) |
| Source | `Verified` or `Literature only` |
| Last checked | The verification date or reference date |

```markdown
| Item | Target | Source | Last checked |
| --- | --- | --- | --- |
| [LocalSet polls only inside run_until](./knowledges/tokio-localset.md) | tokio 1.47.1 | Verified | 2026-08-31 |
```

The Target column is a machine-readable key for matching against the current dependencies during checks (§"Detecting Staleness").
Do not write values that cannot be resolved, such as `latest` or `current`.

Below the table, write one paragraph on the relationships between items.
Point out items about the same external component, and items where if one does not hold, the other also collapses.

## Shape of Child Documents

Write `docs/knowledges/<slug>.md` in the following form.
`<slug>` is kebab-case that conveys the external component and the fact (`tokio-localset`, `launchd-termination`).

```markdown
# Title stating the fact in one line

**Source: Verified** (tokio 1.47.1 / 2026-08-31)

One item of [knowledges.md](../knowledges.md).

## Fact
What behaves how.
Also write the conditions under which it holds.

## Evidence
If verified, the reproduction steps and the commands run.
If literature only, the reference to the primary source and the reference date.

## Implications
Which parts of this project depend on this fact.
Link with a relative link to the subsection of the design document that depends on it.
```

Write all three sections.
Do not number the headings.
Children are entered from the parent's list, so following §"Granularity of the Responsibilities Table" in the common rules, they have no §1.1; one line at the top linking to the parent is enough.

Write the **Fact** together with the conditions under which it holds.
With a fact that has no conditions, nobody can notice it has become false when the conditions change.
If you write "`LocalSet` polls tasks spawned with `spawn_local` only inside `run_until`", also write what happens when wrapped in `block_on`.

An item whose **Implications** cannot be written is irrelevant to this project.
Do not keep external knowledge nothing depends on, even if it is generally useful.
Keeping it only adds to what must be reverified every time a dependency is upgraded.

## Three Modes

**Create**: write a confirmed fact after fixing its source label and target.
Create the parent's list table and the child at the same time.

**Update**: rewrite when the outside changes.
If reverification gives the same result, advance only the verification date.

**Check**: run §"Detecting Staleness" and §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- The confirmed fact, and the conditions under which it holds
- The source label and target
- The verification date or reference date
- The reproduction steps, or the reference to the primary source
- Which parts of this project depend on this fact

## Verification Subagent

Following §"Verification Subagent" in the common rules, the `verifier` is required for creating and adding items.
Advancing only the verification date after reverification does not require it.
A check does not change the body and does not require it.

Add the following to the blocking findings.

- There is no source label, or it is neither `Verified` nor `Literature only`
- The source is `Verified` but there are no reproduction steps
- The source is `Literature only` but there is no reference to a primary source or no reference date
- The target does not pin down a version or edition
- The conditions under which the fact holds are not written
- Statements about our own code are mixed in
- The rows of the list table and the child files do not correspond one-to-one

## Source Labels

Right after the title, put one of the following.

**Source: Verified** (`<target>` / `<verification date>`)
Confirmed hands-on.
Write the reproduction steps in §"Evidence", and if there is verification code in the repository, point to it with a link with line numbers.

**Source: Literature only** (`<primary source>` / `<reference date>`)
Written in a primary source, but not confirmed yourself.
Write the reference to the primary source and the reference date in §"Evidence".

A primary source is something published by the provider of the component:
official documentation, `man` pages, RFCs, source code, and release notes.
Blog posts and Q&A sites are not primary sources.
Before writing something found there, trace it to a primary source or confirm it yourself.

**Reread the primary source for `Literature only` items every three months from the reference date.**
If the content has not changed, advance only the reference date.
If it has changed, rewrite §"Fact" and §"Evidence".
A fact you have not confirmed gives no natural sign that it has gone stale, so setting a deadline is the only way to detect it.

## Lifecycle

- When external behavior is confirmed, create the parent's list table and the child at the same time
- When the outside changes, rewrite. Do not keep old descriptions
- If reverification gives the same result, advance only the verification date
- Reread `Literature only` items every three months (§"Source Labels")
- When the code that depends on it is gone, delete the item

Do not keep descriptions of past versions.
For "it used to be like this up to 1.47", git history is authoritative.
That the body speaks only of the current dependencies is what makes this family trustworthy.

Things to move into this family arise when folding a plan and after publishing a review.
Each reference defines how to move them ([Implementation Plans](implementation-plan.md), [Review Result Documents](review-document.md)).

## Detecting Staleness

During checks, match the following two pairs and report mismatches as findings.
Do not rewrite the body.
Whoever requested the check decides whether to reverify.

**Target vs. current dependencies.**
Compare the Target column of the list table with the versions actually resolved in `Cargo.lock`, `package-lock.json`, `go.sum`, `Package.resolved`, and the like.
List mismatched items as "reverification not done".
For targets without lock files, such as the OS or external APIs, compare with the supported versions written in `README.md` or the CI configuration.

**Reference date vs. three months.**
List the items with source `Literature only` whose reference date is more than three months ago.

In both cases, the report lines up the item, the value written in Target, and the current value or elapsed days.

## What Not to Write

Do not write **general technical knowledge**.
The external world is the authoritative source for explanations of `TCP` retransmission or `B-tree` complexity.
Write only the specific behavior this project depends on.

Do not write **matters of our own code**.
How it was decided to handle external behavior is a design decision and is held by the design document responsible for that concern.
Even when external behavior is the trigger, if the fix is in our own code, it is a bug and is held by `issues.md`.

**A bug in an external component itself** may be written as a fact.
However, if it requires a workaround in our own code, also create an item in `issues.md`.
It is normal to appear in both; do not consolidate into one.

**Setup and operating procedures** are held by `README.md` and `CONTRIBUTING.md`.
What this document holds is how the external thing behaves, not how to operate it.

**Term definitions** are held by the terms documents.
If this project also uses a term defined externally, put a row in the terms documents' table.

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Does every item have a source label, and is it either `Verified` or `Literature only`?
2. Do `Verified` items have reproduction steps, and do references to verification code in the repository have line numbers?
3. Do `Literature only` items have a reference to a primary source and a reference date? Is the reference a primary source?
4. Does the target pin down a version or edition? Are `latest` and `current` (`最新` and `現行` in Japanese) not mixed in? `rg -n -i '\b(latest|current)\b|最新|現行' docs/knowledges.md docs/knowledges/` must not hit the Target column or a source label
5. Are the conditions under which each fact holds written?
6. Does every item have implications, with a relative link to the subsection of the design document that depends on it?
7. Do the rows of the list table correspond one-to-one with `docs/knowledges/*.md`?
8. Is there a paragraph on relationships between items below the list table?
9. Are no descriptions of past versions left?
10. Are general technical knowledge, matters of our own code, design decisions, operating procedures, and term definitions not mixed in?
11. Did you run the two matchings in §"Detecting Staleness" and report the findings?

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| Columns `Item` / `Target` / `Source` / `Last checked` | `項目` / `検証対象` / `出所` / `最終確認日` |
| Source `Verified` / `Literature only` | `検証済み` / `文献のみ` |
| `**Source: Verified**` / `**Source: Literature only**` | `**出所: 検証済み**` / `**出所: 文献のみ**` |
| `One item of [knowledges.md](../knowledges.md).` | `[knowledges.md](../knowledges.md) の 1 項目。` |
| `## Fact` | `## 事実` |
| `## Evidence` | `## 根拠` |
| `## Implications` | `## 含意` |
| "reverification not done" | 「再検証が未実施」 |
