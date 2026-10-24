# Issue List

When writing, revising, or checking `docs/issues.md` and `docs/issues/<slug>.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to the bug list.

This document covers only clear bugs confirmed by reading the code.
Something where what to choose is not yet decided is a design question and goes in the design decisions section of the design document responsible for that concern.
How external things actually behave is held by the knowledge documents ([Knowledge Document](knowledge-document.md)).

## Shape of the Parent Document

Put the following at the top.

1. What this document covers (only clear, confirmed bugs) and what it does not (design questions go in the design decisions section of the relevant design document; external behavior goes in `knowledge.md`)
2. How to use it (add the Issue number once filed; delete the child file when fixed; line numbers drift, so recheck them when fixing)

Do not give the parent an investigation date and target commit.
Items are filed on different days, so no single date can represent the whole family.
Each item holds its own investigation date and target commit (§"Shape of Child Documents").

In §1.1, write what this document holds and what it does not, and link the family map to `[design.md](./design.md#11-document-responsibilities)`.

Then put the list table.
The four columns are Item, Severity, Investigated, and Issue.
The Item column is a relative link to the child, with the symptom stated in one line as the displayed text.

```markdown
| Item | Severity | Investigated | Issue |
| --- | --- | --- | --- |
| [Leaked timers exhaust file descriptors](./issues/timer-leak.md) | High | 2026-08-31 | #12 |
| [Listing after deletion returns stale values](./issues/stale-cache.md) | Medium | 2026-08-20 | - |
```

Below the table, write one paragraph on the relationships between items.
Point out items on the same path and items that are efficient to fix together.

At the end, put a "Not included here" table that lists design gaps handled on the design document side, with links.

## Shape of Child Documents

Write `docs/issues/<slug>.md` in the following form.
`<slug>` is kebab-case that conveys the symptom (`timer-leak`, `stale-cache`).

```markdown
# Short title that conveys the symptom

**Severity: High** (can be triggered externally)

Investigated 2026-08-31 / Target commit `a1b2c3d`

One item of [issues.md](../issues.md).

## Symptom
What is observed. Does it show up in logs, or break silently?

## Location
Links to files with line numbers, and a code quote if needed.

## Cause
Why it is that way.

## Impact
How far it breaks. Dependencies on other items. If it has not surfaced yet, why.

## Remedy
How to fix it. May include proposals to prevent recurrence (detection by tests, types, or macros).
```

Write all five sections.
Do not number the headings.
Children are entered from the parent's list, so following §"Granularity of the Responsibilities Table" in the common rules, they have no §1.1; one line at the top linking to the parent is enough.

The investigation date and target commit are required.
Location points by line number, and is useless unless you know the point in time of the code that was examined.

## Three Modes

**Create**: investigate by reading the code, and create the parent's list table and the first child at the same time.

**Update**: add items, add the number of a filed Issue, delete fixed items.
When rereading an existing child, verify the line numbers in Location and advance the investigation date and target commit.

**Check**: run §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- Each item's investigation date and target commit
- Each item's symptom, location, cause, impact, and remedy
- Severity and manifestation
- Relationships between items
- What is not included here

## Verification Subagent

Following §"Verification Subagent" in the common rules, the `verifier` is required for creating and adding items.
Adding the number of a filed Issue, or only deleting fixed items, does not require it.
A check does not change the body and does not require it.

Add the following to the blocking findings.

- An item lacks any of the five sections
- Severity is not accompanied by manifestation
- Location has no line numbers
- An item has no investigation date or target commit
- Design questions are mixed in as items
- External behavior itself is mixed in as an item
- The rows of the list table and the child files do not correspond one-to-one

## Severity

There are three levels, judged by the following criteria.

- **High**: the feature on that path does not work, data is corrupted, or it can be stopped by external input.
- **Medium**: the result does not change at present but breaks when conditions line up, or it cannot be fixed until a design decision is made.
- **Low**: no actual harm, but it misleads readers, or it is quality debt.

Right after the severity, always add the manifestation in parentheses.
Add nothing for something that is actually broken now.
For something that is not broken, briefly write why it is not broken now ("not yet manifest", "depends on a design question").
Conversely, write it when something can be triggered externally even if its severity is Medium or Low.

Manifestation is orthogonal to severity.
Keep items that are "safe because not wired up" distinguishable from those that are not.

## Lifecycle

- When a bug is confirmed, add a row to the parent's list table and create a child
- When filed, add the number to the Issue column of the list table. Keep the child
- When fixed, delete the child file and remove the row from the list table
- As a rule, whatever remains here is unaddressed

Items transcribed from review result documents are treated the same way.
Do not link to the transcription source.
To trace the origin, searching `docs/reviews/` for the `<slug>` is enough.

Even when the cause is a bug in an external component, if a workaround must go into our own code, create an item in this document.
How the external thing actually behaves also gets an item in `knowledge.md`.
It is normal to appear in both; do not consolidate into one.

## What Not to Write

**Design questions** are held by the design decisions section of the relevant design document.
Do not file something as a bug when what to choose has not been decided.

**External behavior itself** is held by `knowledge.md`.
What this document holds is that our own code is broken, not how the external thing behaves.

**Term definitions** are held by the terms documents.
Even when writing that names are inconsistent as a bug, point to the terms documents for the correct name.

**Review history** is held by `docs/reviews/<slug>.md`.
Do not write who found it and when in this document.

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Does every item have an investigation date and target commit?
2. Does every item have the five sections: symptom, location, cause, impact, and remedy?
3. Do the rows of the list table correspond one-to-one with `docs/issues/*.md`?
4. Is every severity accompanied by manifestation in parentheses?
5. Do references to code in Location have line numbers? `rg -nH '\]\((\.\./)+[^)#]*\.[A-Za-z0-9]+\)' docs/issues/*.md | rg -v '\.md\)'` must be empty (it picks up links to code that lack `#L`, excluding `.md` links between documents)
6. Is there a paragraph on relationships between items below the list table?
7. Is there a "Not included here" table at the end, and do its links to design documents include the heading anchor?
8. Are design questions, external behavior, term definitions, and review history not mixed in?
9. Are no sequential-number IDs left? `rg -n 'I-[0-9]' docs/` must be empty

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| Columns `Item` / `Severity` / `Investigated` / `Issue` | `項目` / `深刻度` / `調査日` / `Issue` |
| Severity `High` / `Medium` / `Low` | `高` / `中` / `低` |
| `**Severity: High**` | `**深刻度: 高**` |
| `Investigated 2026-08-31 / Target commit` | `調査日 2026-08-31 / 対象コミット` |
| `One item of [issues.md](../issues.md).` | `[issues.md](../issues.md) の 1 項目。` |
| `## Symptom` | `## 症状` |
| `## Location` | `## 該当箇所` |
| `## Cause` | `## 原因` |
| `## Impact` | `## 影響` |
| `## Remedy` | `## 対応方針` |
| "Not included here" | 「ここに含めていないもの」 |
| Manifestation "not yet manifest" / "depends on a design question" | 「現時点では未顕在」「設計論点に依存」 |
