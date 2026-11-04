# Measurement Record and Comparison Procedure

When writing, revising, checking, or re-measuring `docs/measurements.md` and `docs/measurements/<slug>.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to measurement records and comparison procedures.

This document covers measurements of our own system's behavior under fixed conditions: latency, throughput, memory, bytes, counts, hit rates, and the procedures that compare them before and after a change.
The structure of and design decisions about our own code are held by design documents, bugs by `issues.md`, how external components behave by `knowledge.md`, work in progress by `plans.md`, and review findings by `reviews.md`.

There are three reasons to make this family independent.
A measurement is a snapshot tied to a commit and an environment. Embedded in the prose of a design document, its conditions are lost and its numbers are reread as timeless.
A comparison procedure outlives a piece of work. Written in a plan, it disappears when the plan is folded.
A measured fact can support or refute a design decision, but it is not the decision itself.

## Two Kinds of Child

A **measurement record** holds one measurement or one comparison, the conditions under which it was taken, the numbers, the interpretation, and the limits.
It is dated, and it is kept permanently.

A **comparison procedure** holds how to measure a subject, the acceptance conditions fixed before measuring, the data and environment to use, the steps, and the values a record must save.
It is undated and describes the current way to measure.

A record may exist without a procedure when the measurement is one-off or exploratory.
It states its method inline, fixes the number of runs and the order in the record before measuring, and follows the same record rules.
A procedure may exist before the first record.

## Shape of the Parent Document

Put the following at the top.

1. What this document covers (measurement records and comparison procedures for our own system) and what it does not (design decisions go in the design documents, defects in `issues.md`, external behavior in `knowledge.md`, work in `plans.md`, and review findings in `reviews.md`)
2. How to use it (add a row when a record or a procedure is created; records are never overwritten; a re-measurement is a new dated record; update a procedure in place; do not delete a record because the code changed)

In §1.1, write what this document holds and what it does not, and link the family map to `[design.md](./design.md#11-document-responsibilities)`.

```markdown
## 1. About This Document

### 1.1 Division of Responsibility Between Documents

| Document | What it covers |
| --- | --- |
| This document | List of measurement records and comparison procedures |
| [design.md](./design.md#11-document-responsibilities) | Design decisions, invariants, and their reasons |
| [issues.md](./issues.md) | Confirmed defects and their handling |
| [knowledge.md](./knowledge.md) | How external components actually behave |
| [plans.md](./plans.md) | Work in progress and dependencies |
| [reviews.md](./reviews.md) | Review history and transcription status |
```

## Record List

The three columns are Record, Measured (UTC), and Subject.

| Column | What to write |
| --- | --- |
| Record | A relative link to the child. The displayed text is the identifier `YYYY-MM-DD-<slug>` |
| Measured (UTC) | The measurement date or date range in UTC, such as `2026-08-10` or `2026-08-10 to 11` |
| Subject | One line stating what was measured and the comparison. Do not write the verdict |

```markdown
## 2. Record List

| Record | Measured (UTC) | Subject |
| --- | --- | --- |
| [2026-08-10-storage-throughput](./measurements/2026-08-10-storage-throughput.md) | 2026-08-10 | Listing latency before and after the storage facade split, with the page cache warm |
```

Stack rows with the newest measurement on top.
Records are permanent, so rows are not deleted because the code changed.

Below the table, write one paragraph on the relationships between records.
Point out a before record and its after record, records that re-measure the same subject, and records that share a procedure.

## Comparison Procedures

The two columns are Procedure and Use.

```markdown
## 3. Comparison Procedures

| Procedure | Use |
| --- | --- |
| [storage-protocol](./measurements/storage-protocol.md) | Compares listing latency before and after a change on a fixed fixture, with the daemon restarted for each run |
```

Order procedures alphabetically by `<slug>`.
A procedure is the current way to measure, so update it in place when the code, tools, or data change.
Before using a procedure, check that its commands, paths, versions, and fixtures still match the current code and environment; update it in place before measuring if they do not.
Git history is the history of the procedure.

## Shape of Measurement Records

Write `docs/measurements/YYYY-MM-DD-<slug>.md`.
`<slug>` is kebab-case that conveys the subject (`storage-throughput`, `browse-thumbnails`).
The date is the measurement date in UTC, not the date the document was written.
Putting the date first keeps the records in chronological order and prevents a collision when the same subject is measured again.

```markdown
# Comparing <subject> before and after <change>

**Measured: 2026-08-10 (UTC)** / **Targets: `a1b2c3d` (A), `d4e5f6a` (B)**

One record of [measurements.md](../measurements.md).

## 1. Subject and Conditions

What was measured and why.
When a procedure exists, link it and quote the acceptance condition used.
When there is no procedure, state the method, the conditions, the number of runs, and the order inline, and state the acceptance condition fixed in the record, or that there is none.

Write the conditions that change the numbers.
- Fixture identity and size, and how it was created and verified
- Target commit or build identifier, build profile, toolchain, and measurement tool versions
- OS, hardware, and runtime versions
- Isolation: dedicated port, configuration, and state; read-only data
- State of the OS, process, and persistent caches
- Background work and load from other processes
- The number of runs per condition and the fixed run order (in the procedure, or in the record when there is no procedure), and the order actually used
- The rule for excluding a run, fixed before measuring, and any run excluded under it
- Every failed or excluded run, with its reason and the values it produced

State "not applicable" or "not controlled" rather than omitting a field.

## 2. Results

The values for every run, not only the aggregate.
State the aggregation method (median, mean, minimum, maximum) and the unit.
State the measurement points actually read.
Put the acceptance target and the measured value side by side.
Counts, bytes, hit rates, and UI observations belong here when they are part of the measurement.

Do not round away a difference that matters to the judgment.
Do not paste raw logs; link the sidecar.

## 3. Interpretation

Whether the acceptance condition was met, was not met, or does not exist.
A causal explanation only with its evidence and its confidence; label an inference as an inference.
A relative link to the design decision this measurement supports or refutes.
If no design decision depends on it yet, say so and link the plan if there is one.
What remains unresolved.

## 4. Limits

What was not controlled, what was not measured, what cannot be extrapolated, and environment constraints that affected a run.
```

All four sections are required.
Number headings in the form `## 1.` and do not number `####`.
Do not add §1.1. The one line at the top linking to the parent is enough, following §"Granularity of the Responsibilities Table" in the common rules.

Write the title as the subject and the comparison, not as the verdict.
For an exploratory measurement without a comparison, state what condition was measured.
Write observations in the past tense. The procedure is written in the present tense.

The metadata line is required.
`**Measured: ...**` carries the date in UTC, and `**Targets: ...**` carries an immutable commit or build identifier for each condition.
If the project does not use git, use an equivalent immutable build identifier and say what it is.

## Shape of Comparison Procedures

Write `docs/measurements/<slug>.md`.
The file is undated because it describes the current way to measure.

```markdown
# <Subject> Comparison Procedure

One procedure of [measurements.md](../measurements.md).

## 1. Subject and Acceptance Conditions

What is compared, why, and the acceptance conditions fixed before measuring.
Do not loosen a condition after seeing the values.
Fix the number of runs and the order before measuring, and state them.
Do not change the number of runs or the order after seeing the values.

## 2. Data and Environment

How to create and verify the fixture, and its identity and size.
Build, toolchain, and measurement tool versions.
Dedicated port, configuration, and state; read-only data; a dedicated browser profile when applicable.
Cache and background conditions.

## 3. Procedure

The steps and commands in order.
List the measurement points to read. Their definitions are in the design document responsible for the concern.
Pass secrets through environment variables; never put them in the document or in command arguments.
State exclusions and rerun rules before measuring.
Keep the procedure runnable by someone who was not present.

## 4. Saved Values

What every record produced by this procedure must save: the values for every run, the aggregates, the build, the environment, the acceptance judgment, and the limits.
The schema and location of the sidecar, if one is used.
What must not be saved: credentials, tokens, real paths, and real data names.

## 5. Limits

What this procedure does not measure, does not control, and cannot be extrapolated to.
```

All five sections are required.
Number headings in the form `## 1.` and do not number `####`.
Project-specific comparison sections may follow §5, numbered `## 6.` onward.
Do not add §1.1. The one line at the top linking to the parent is enough.

## Raw Data

A sidecar file may hold the raw values next to the record, with the same base name and a data extension: `YYYY-MM-DD-<slug>.json`, `YYYY-MM-DD-<slug>.csv`.
A sidecar is not a document.
Do not list it in the parent's tables, do not give it a heading, and do not link it as a child.
Link it from the record's §2 Results.

A sidecar is required when the record reports only aggregates.
When the record carries every run's values, a sidecar is optional.
The sidecar must contain the values needed to re-derive the aggregates, the build and environment, and enough schema to read the values without the record.

Do not save credentials, tokens, authorization headers, real paths, or real data names in a sidecar.
Do not overwrite a sidecar when re-measuring; create a new dated sidecar with the new record.

## References from Design Documents

A design document may state the conclusion of a measurement and the rounded number needed for its reason, with a relative link to the record.
It does not copy the conditions, the values of every run, or the limits; the record is authoritative for those.
A record does not restate the design decision; it links the decision.

## Measurement Points

The definition of a measurement point is a design decision.
The span names, log fields, units, and boundaries that the implementation keeps are held by the design document responsible for that concern.
A comparison procedure lists only the names of the measurement points it reads.
A record states the points it actually read.

## Lifecycle

Records:

- Create a new dated record for each measurement. A re-measurement is a new record, not an edit
- Never delete a record because the code changed; it is the before side of later comparisons
- Correct a factual mistake with a note; do not rewrite a value to match a new measurement
- When a record re-measures the same subject, link the earlier record in §1
- Keep a record that failed acceptance, with the failure
- Keep failed and excluded runs in the record or sidecar, with their reasons; do not discard a run because it was abnormal

Procedures:

- Create a procedure before the first measurement when a comparison will be repeated
- Before using a procedure, check it against the current code and environment; update it in place if anything has changed
- Update it in place when the code, tools, or data change
- A record quotes the acceptance condition it used, so a later procedure change does not invalidate old records
- Delete a procedure only when its subject no longer exists; do not keep a history of procedures in this family

Parent:

- Add a row when a record or a procedure is created
- Remove a procedure row only when the procedure is deleted
- Never remove a record row, because records are permanent

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- The measurement date in UTC and the target commit or build
- The conditions: fixture, environment, isolation, cache and background state, the number of runs and run order fixed before measuring, and failed or excluded runs with their reasons
- The values for every run, the aggregates, and the unit
- The measurement points actually read
- The acceptance condition and the judgment
- The causal explanation, its evidence, and its confidence
- The design decision the measurement supports or refutes
- The limits and the unverified scope
- The procedure's steps, commands, saved values, and safety constraints

## Verification Subagent

Following §"Verification Subagent" in the common rules, the `verifier` is required for creating a record or a procedure and for changing values, conditions, or acceptance conditions.
Correcting a typo that does not change the meaning does not require it.
A check does not change the body and does not require it.

Add the following to the blocking findings.

- A record has no `Measured` line, or the date is not in UTC
- The parent's Measured column does not match the record's metadata line
- A record has no `Targets` line, or has no commit or build identifier
- A record lacks any of the four sections or a procedure lacks any of the five, or a required heading is unnumbered or out of order
- Conditions needed to reproduce the measurement are missing
- The record reports only aggregates and does not link a sidecar
- The acceptance condition is not quoted from the procedure when one exists, or differs from it
- A condition was changed after the measurement, or the record does not state that no condition exists
- The number of runs or the run order was changed after measuring, or is not fixed in the procedure or, when there is no procedure, in the record
- A failed or excluded run was discarded without a reason
- The procedure defines the measurement points instead of naming the design document, or the record does not state the points it read
- A re-measurement overwrote or appended to an old record
- A causal claim has no evidence or no confidence label
- The limits are missing
- Credentials, tokens, real paths, or real data names are saved
- The rows of the parent's tables and the child `.md` files do not correspond one-to-one
- A design decision, a bug, an external fact, a review finding, or a term definition is mixed in
- A measurement record is presented as a regression guard
- Procedure commands contain secrets or are not runnable
- The numbers in the record do not match the sidecar

## Three Modes

**Create**: fix the procedure and its acceptance conditions before measuring, or fix the method, conditions, number of runs, and order inline when there is no procedure, then measure, create the dated record, and add rows to the parent.

**Update**: for a record, only correct a factual mistake with a note; for a procedure, update it in place.
A re-measurement is Create, not Update.
Adding a row or fixing a link does not require a body rewrite.

**Check**: run §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

## What Not to Write

**Design decisions** are held by the design documents.
The record says what was observed; the design document says what was chosen and why.
Link the decision instead of restating it.

**Bugs** are held by `issues.md`.
If a measurement reveals a defect, file it in `issues.md` and link it from the record.

**External behavior** is held by `knowledge.md`.
The environment section lists versions; a fact about how an external component behaves goes to `knowledge.md`.

**Review findings** are held by `docs/reviews/<slug>.md`.
A review may cite a measurement record as evidence; the finding and its disposition stay in the review.

**Term definitions** are held by the terms documents.

**General performance advice** is not a measurement.
Write only what this project measured under the conditions it recorded.

**Production data, credentials, and tokens** are never written, even as an example.

**A promise that a number will stay the same** is not a measurement record.
A record is a point in time. To keep a property, use a test or a CI check.

## Safety

- Do not measure against a production instance or with real user data
- Use a dedicated port, configuration, and state, and make the measured data read-only
- Do not save credentials, tokens, authorization headers, real paths, or real data names in records, procedures, or sidecars
- Pass secrets through environment variables, not through command arguments or the document
- If a production process must be stopped, prepare a watchdog and a recovery procedure before stopping it
- Record the environment and the uncontrolled variables; do not claim isolation you did not have

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Does every record have the `**Measured: ...**` and `**Targets: ...**` metadata line, with a UTC date and a commit or build identifier? Does the parent's Measured column match it?
2. Does every record have the four sections, and every procedure the five sections, numbered in the required form and in order?
3. Are the conditions needed to reproduce present, with "not applicable" or "not controlled" where a field does not apply?
4. Are the values for every run present, or is a sidecar linked when only aggregates are shown?
5. Is the acceptance condition quoted from the procedure when one exists, or fixed in the record and stated when there is no procedure?
6. Is the judgment in §"Interpretation", and is the causal explanation labeled as an inference?
7. Does §"Interpretation" link the design decision, or state that none exists yet?
8. Are the limits present?
9. Do the rows of the record table and the procedure table correspond one-to-one with the record and procedure child files, respectively? Are sidecars absent from both tables?
10. Are no sequential-number IDs used? The record identifier is `YYYY-MM-DD-<slug>`
11. Is no earlier measurement record overwritten? For record files, `git diff -- docs/measurements/` must show only corrections with a note and new files. An in-place update of an existing comparison procedure is allowed and is not an overwrite.
12. Are no credentials, tokens, real paths, or real data names present? Search the diff, not only the final text
13. Do references to code in records have line numbers? `rg -nH '\]\((\.\./)+[^)#]*\.[A-Za-z0-9]+\)' docs/measurements/*.md | rg -v '\.md\)'` must be empty (it picks up links to code that lack `#L`, excluding `.md` links between documents)
14. Do the links to sidecars resolve? `rg -o '\]\(\./[^)]+\.(json|csv)\)' docs/measurements/*.md` must list only files that exist
15. Are observations in the past tense and the procedure in the present tense?
16. Is the number of runs fixed in the procedure, or in the record when there is no procedure, before measuring, and is the run order recorded?
17. Are failed and excluded runs kept with their reasons?
18. Does the record state the measurement points actually read, and are their definitions left to the design document?

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| `Measurement Records and Comparison Procedures` | `測定記録と比較手順` |
| `1. About This Document` | `1. 本書について` |
| `1.1 Division of Responsibility Between Documents` | `1.1 文書間の責務分担` |
| `2. Record List` | `2. 記録一覧` |
| `3. Comparison Procedures` | `3. 比較手順` |
| Columns `Record` / `Measured (UTC)` / `Subject` | `記録` / `測定日 (UTC)` / `対象` |
| Columns `Procedure` / `Use` | `手順` / `用途` |
| `**Measured: 2026-08-10 (UTC)**` | `**測定日: 2026-08-10 (UTC)**` |
| `**Targets: ...**` | `**対象コミット/ビルド: ...**` |
| `One record of [measurements.md](../measurements.md).` | `[measurements.md](../measurements.md) の 1 記録。` |
| `One procedure of [measurements.md](../measurements.md).` | `[measurements.md](../measurements.md) の 1 手順。` |
| `## 1. Subject and Conditions` | `## 1. 対象と条件` |
| `## 2. Results` | `## 2. 結果` |
| `## 3. Interpretation` | `## 3. 解釈` |
| `## 4. Limits` | `## 4. 限界` |
| `## 1. Subject and Acceptance Conditions` | `## 1. 対象と受入条件` |
| `## 2. Data and Environment` | `## 2. データと環境` |
| `## 3. Procedure` | `## 3. 手順` |
| `## 4. Saved Values` | `## 4. 保存する値` |
| `## 5. Limits` | `## 5. 限界` |
| `Measurement Record` / `Comparison Procedure` | `測定記録` / `比較手順` |
| `met` / `not met` | `達成` / `未達` |
| `no acceptance condition` | `受入条件なし` |
| `not measured` / `not controlled` | `未測定` / `未制御` |
| `run` (noun) / `per-run values` | `試行` / `全試行値` |
| "not applicable" | 「該当なし」 |
