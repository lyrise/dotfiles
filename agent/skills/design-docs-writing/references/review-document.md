# Review Result Documents

When writing, checking, or transcribing findings from `docs/reviews.md` and `docs/reviews/<slug>.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to review result documents.

These rules protect three things.
Readers do not confuse the scope that was examined with the scope that was not.
Findings do not disappear without being picked up anywhere.
After the fixes are finished, a record remains of when, what, and from what perspectives things were examined.

## Two Kinds of Review

A **diff review** targets changes in a PR, a branch, or the working tree.
The diff determines the scope, so everything outside the diff is unexamined scope.

An **audit review** reads a specific area of existing code straight through, not a diff.
You cut the scope yourself, so unless you write where and by what criterion you cut it, the unexamined scope is undefined.

Declare which one it is in §1.2.
The section structure is common, and only how §2.1 is written differs.

Do not handle both in one document.
If you read beyond the diff, that is two reviews and becomes two documents.

## slug

`<slug>` takes the form `YYYY-MM-DD-<target>`.
`<target>` is a short kebab-case name for the reviewed scope (`2026-08-10-storage-facade`, `2026-08-10-pr-142`).

There are two reasons for putting the date first.
Documents are kept permanently, so their number grows, and being lined up in chronological order is itself an index.
When the same scope is reviewed again later, the file names do not collide.

## Shape of the Parent Document

Do not create a parent that holds only information obtainable from `ls docs/reviews/`.
What `docs/reviews.md` holds is the one thing that can never be learned from the file names: how far each review's findings have been transcribed.

Transcription is a required procedure after publication (§"Transcription"), but there used to be no place that held whether it was done.
Since documents are kept permanently, untranscribed findings do not disappear, but they remain unread by anyone.

Put the following at the top.

1. What this document covers (the review history and transcription status) and what it does not (the content of each review is in the children; the body of findings is at the transcription destinations)
2. How to use it (add a row when publishing, advance the status when transcribing, never delete rows)

In §1.1, write what this document holds and what it does not, and link the family map to `[design.md](./design.md#11-document-responsibilities)`.

Then put the list table.
The four columns are Review, Type, Findings, and Transcription.

| Column | What to write |
| --- | --- |
| Review | A relative link to the child. The displayed text is the `<slug>` |
| Type | `diff` or `audit` |
| Findings | The number of findings in §4 |
| Transcription | `done`, or the IDs of untranscribed findings |

```markdown
| Review | Type | Findings | Transcription |
| --- | --- | --- | --- |
| [2026-08-10-storage-facade](./reviews/2026-08-10-storage-facade.md) | audit | 4 | done |
| [2026-08-22-pr-142](./reviews/2026-08-22-pr-142.md) | diff | 2 | R-2 not transcribed |
```

Stack rows with the newest on top.
Review result documents are not deleted, so the rows of this table are not deleted either.
Keep rows whose transcription is finished.

The Transcription column becomes `done` when the disposition of every finding has been filled in with a transcription destination or a reason not to transcribe.
A finding decided not to be transcribed also counts toward `done` at the time of the decision.

## Shape of Child Documents

```
1. About This Review
   1.1 Document Responsibilities
   1.2 Review Date and Target
2. Scope and Perspectives
   2.1 Examined Scope
   2.2 Unexamined Scope
   2.3 Perspectives
3. Overall Assessment
4. Findings
5. Checked and Found Fine
6. Aftermath
```

All six sections are required.
Number headings in the form `## 1.` `### 1.1`, and do not number `####`.

### 1. About This Review

State in one or two sentences what the review is of.

Write **1.1 Document Responsibilities** as a table.
List here only what this document holds, what it does not, and the documents that are transcription destinations.
Show the family map with a link to `[design.md](../design.md#11-document-responsibilities)`.
Transcription destinations point to `[terms.md](../terms.md)`, `[issues.md](../issues.md)`, `[knowledges.md](../knowledges.md)`, and the relevant design documents.

**1.2 Review Date and Target** is required and contains the following four.

1. The review date
2. The type of review (diff review or audit review)
3. The target commit. For a diff review, write both base and head, and add the PR number if there is one
4. The reviewer. A name for a human, the model name for an agent

The reviewer is written because how a finding is read changes with who looked.
If several looked, write all of them.

### 2. Scope and Perspectives

How **2.1 Examined Scope** is written differs by type of review.

For a diff review, write which of the files changed between base and head were actually read.
If every file in the diff was read, say so in one line.
If some files were not read, move them to §2.2.

For an audit review, write the directories or modules read and the criterion by which the scope was cut there.
Without the criterion, it cannot be told whether an adjacent area was deliberately excluded or overlooked.

**2.2 Unexamined Scope** is required and must not be empty.
Writing "none" or "nothing in particular" is forbidden.
For a diff review, at least everything outside the diff was not examined.

For each item, add why it was not examined:
because it is out of scope, because another review handles it, or because there was not enough time.
Do not hide the last reason.

Without this subsection, the fact of having been reviewed is misread as a guarantee of the whole.
What a review result document must assert most strongly is not what was found, but the scope that was not examined.

In **2.3 Perspectives**, list what was looked for.
Anything not in the perspectives was not looked for and is part of §2.2.

In a review without perspectives, zero findings has no defined meaning.
Looking for nothing also gives zero.

For how to set perspectives, see §"Example: Perspectives".

### 3. Overall Assessment

Write the overall judgment in two to four sentences.

For a diff review, state explicitly in one sentence whether to proceed as is, proceed after fixing, or redecide the design.
For an audit review, state explicitly in one sentence whether the area is usable as it stands.

If there is something serious, point to it by ID and do not repeat the body of the finding.

### 4. Findings

Put a list table at the top.
The five columns are ID, Summary, Kind, Confidence, and Disposition, and the ID is an anchor link to the item.
Below the table, write one paragraph on the relationships between items.
Point out items arising from the same cause and items that are efficient to fix together.

If there are zero findings, do not put a table; write only the one sentence "No findings."
In that case, §2.2 and §5 become the substance of the document.

Write each finding in the following form.

```markdown
<a id="r-1"></a>
### R-1. Short title that conveys the symptom

**Kind: Bug** / **Confidence: High**

**Location**
Links with line numbers, and a code quote if needed.

**What is wrong**
What happens. Do not restate the title.

**Evidence**
Why this can be said. Write what was confirmed separately from what was not.

**Impact**
How far it breaks. If it has not surfaced yet, why.

**Disposition**
The transcription destination document and identifier. If not transcribed, the reason.
```

Write all five labels.
Put the explicit anchor `<a id="r-1"></a>`.
Auto-generated heading anchors are long and break when the title is edited.

IDs start with `R-`, are sequential within one document, and deleted IDs stay as gaps.
§"Identifiers" in the common rules requires items to be referred to by `<slug>`, but findings are confined to one review and are not split into children, so these sequential numbers are outside that rule.

**Kind** is one of the following four, judged by the same boundaries as §"The Document Family and Responsibilities" in the common rules.

- **Bug**: it is known what to fix and how
- **Design question**: what to choose has not yet been decided
- **Terminology**: term definitions, notation, or aliases are inconsistent. The code calls the same thing by two names, `terms.md` and the identifiers in the implementation disagree, or an alias that was supposedly rejected appears in new code
- **Improvement**: not broken, but could be better

The kind determines the transcription destination (§"Transcription").
Do not give one finding two kinds.
If you want to, it is two findings.

**Confidence** has three levels, judged by the following criteria.

- **High**: the code was read and it was confirmed that the path actually behaves that way
- **Medium**: the conditions under which it happens were identified, but whether those conditions hold was not confirmed
- **Low**: suspicious, but whether it holds was not checked

Findings with confidence Low may be written.
Whereas permanent documents do not write unconfirmed things in the body, recording suspicions is the role of review result documents.
However, do not misstate the confidence.
The moment something unconfirmed is written as High, this document lies to its readers.

Evidence and confidence must always agree.
If the evidence says "it seems" or "it should" but the confidence is High, one of them is wrong.

### 5. Checked and Found Fine

Write only things that were suspected, checked, and judged to have no problem.
One to two lines per item: what was suspected, and on what grounds it was ruled out.

Do not write places that were read without suspicion.
The scope in §2.1 already represents them.
Listing places that were skimmed here mixes what was checked with what was merely read, and the section loses its meaning.

Without this section, a review with zero findings cannot be told apart from a review that examined nothing.

### 6. Aftermath

Append what happened after publication as dated bullet points.
At publication, only the heading is placed; this is the only section that may be empty.

```markdown
- 2026-08-12: Filed R-1 as issues/timer-leak.md
- 2026-08-15: R-2 was wrong. `flush` is guaranteed by the caller, and it does not happen on this path
- 2026-08-18: Moved the launchd termination behavior checked in §5 to knowledges/launchd-termination.md
- 2026-08-20: Fixed R-3. issues/stale-cache.md has been deleted
```

Write four kinds of things: transcriptions, moves of external facts, fixes, and reversed judgments.
Do not write implementation progress here.
The implementation plan and git history are authoritative for it.

## Four Modes

**Create**: right after performing the review, set up the shape of the child document (§"Shape of Child Documents"), fill in each section, and add a row to `docs/reviews.md`.
After a day passes, you can no longer remember what was checked and what was not, and §2.2 and confidence can no longer be written.

**Append**: for a published document, add dated entries only to §6 (§"Immutability").
Do not touch §1 to §5.

**Transcribe**: move findings into permanent documents and advance the Transcription column of `docs/reviews.md` (§"Transcription").
This is a required procedure after publication.

**Check**: run §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- The type of review, target commit, review date, and reviewer
- The examined scope, the unexamined scope, and why it was not examined
- The perspectives looked for
- The overall judgment
- Each finding's location, problem, evidence, impact, and disposition
- What was suspected, checked, and judged fine, and the grounds for that judgment
- What happened after publication

The following may additionally be deleted or merged.

- Summaries of the changes (git is the authoritative source)
- "What is wrong" that merely restates the finding's title
- Repeating finding bodies in the overall assessment

## Verification Subagent

Following §"Verification Subagent" in the common rules, replace the scope in which the `verifier` is required with the following.

It is required for creating; if it is unavailable, report without creating the document.
Appending to §6, updating the Transcription column of `docs/reviews.md`, and checks do not require it.
For transcription, the required scope of each reference applies to the changes in the permanent documents receiving the content.

Replace the blocking findings with the following.

- §2.2 is empty, or dismissed with "none"
- Perspectives are not listed
- A finding has no disposition
- Confidence disagrees with the evidence (something unconfirmed is given confidence High)
- Location has no line numbers
- The kind is not one of the four, or the kind and the transcription destination do not correspond
- The identifier of a transcription destination is a link
- A summary of the diff or pasted fix code
- Changes to §1 to §5 of a published document
- There is no row in `docs/reviews.md`, or the number of findings does not match
- Broken headings, anchors, or links

## Immutability

After publication, do not rewrite §1 to §5.

A review result document is a record of judgments at that point in time.
Rewriting it later makes it impossible to tell what was known at the time of the review, and its value as a record disappears.
This is also why, unlike implementation plans, it is not folded.

Only typos and broken links may be fixed; factual statements and judgments are not corrected.
Even when a finding later turns out to be wrong, keep the body in §4 and append to §6 "R-3 was wrong" with the reason.
If it is deleted, the next review repeats why that finding came up.

## Transcription

After publishing, transcribe the findings.
Without transcription, they become findings held only by this document and do not enter the flow of fixes.
Being kept permanently, they do not disappear if left alone, but nobody looks at them.

| Kind | Transcription destination | When transcription may be skipped |
| --- | --- | --- |
| Bug | File it as `docs/issues/<slug>.md`, and add a row to the list table of `issues.md` | When it was fixed within the same review |
| Design question | A deferred item in the design decisions section of the relevant design document (always with a condition for deciding) | Never |
| Terminology | The term list or the term's entry in the terms documents | When it was fixed within the same review |
| Improvement | File it as `docs/issues/<slug>.md` with severity Low | When it was decided not to do it |

Even when not transcribing, do not leave the **Disposition** field empty.
Write "fixed within the same review" or "decided not to do it, because …".
A finding with an empty disposition is one that disappears without anyone picking it up.

Besides findings, there is one more thing to move.
External behavior that appeared in the evidence of §4 and in §5, and that holds outside the context of this review, is moved to `docs/knowledges/<slug>.md` ([External Knowledge](knowledges-document.md)).
This is not a finding, so it has no kind and does not appear in the list table.
Record the move with a date in §6.

When every finding's disposition is filled in and the external facts have been moved, set the Transcription column of `docs/reviews.md` to `done`.
Only this column holds whether transcription is finished.

Write transcriptions according to the destination's reference, and do not paste this document's sentences as is.
This document's sentences were written in the context of a diff or audit, and cannot be read once that context is gone.

**Do not make the Disposition field a link.**
Point by the destination document's name and the identifier within it (the bug's `<slug>`, the title of the design document's deferred item, the term in the terms documents).
Bugs disappear with the fix, deferred items in design documents move to decided once settled, and terms change anchors when renamed, so links always break.
Pointing by identifier means that not finding the target itself conveys that it has been dealt with.

Do not link from the transcription destination back to this document.
With links in both directions, one always goes stale.
To trace the origin, searching `docs/reviews/` for the bug's `<slug>` is enough.

## What Not to Write

Do not write **summaries of the changes**.
git is the authoritative source for what changed, and the diff rewritten in prose is not a review.
Mention the changes only when needed as evidence for a finding.

Do not write **fix code**.
Write how to fix it in one sentence in the disposition in §4; the implementation is held by the remedy in `issues.md` or an implementation plan.

**The reasons for design decisions** are held by design documents.
If a review produces a new design decision, it is a decision rather than a finding; write it in the design document, then point to it from this document as kind Design question.

**Term definitions** are held by `terms.md`.
Do not write the correct definition in a finding of kind Terminology; write only how to fix `terms.md` in the disposition.

Do not write **formatting preferences**.
Formatters and linters are the authoritative source, and only what they do not detect is treated as worth a finding.

Code blocks are allowed only for quotes of existing code showing the location of a finding (with a link with line numbers).

## Source of Evidence

Following §"Distinguishing the Source of Evidence" in the common rules, this document formalizes it in the evidence and confidence of §4.

The correspondence with the three categories is as follows.
Facts confirmed in the code are confidence High, intent read from the code is confidence Medium, and things not confirmed are confidence Low.
The third, which permanent documents do not write, may be written in this document with the confidence stated.

If something was confirmed with reproduction steps or commands, write those commands as evidence.
Whether it was only read or actually run changes the weight of the finding.

## Lifecycle

- Write it right after performing the review, and add a row to `docs/reviews.md`
- Once published, freeze §1 to §5 (§"Immutability")
- Transcribe the findings, and advance the Transcription column of `docs/reviews.md` (§"Transcription")
- When filing, fixing, or correcting a judgment happens, append to §6
- Do not delete it. Do not delete its row in `docs/reviews.md` either

When reviewing the same scope again, do not rewrite this document; create a new document with a new date.
The previous document may be referenced in the perspectives of §2.3 or in §5, and if the scope examined last time is excluded from this time's perspectives, write so in §2.2.

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Is §2.2 not empty? Does it not end with just "none" or "nothing in particular"?
2. Does each item in §2.2 have a reason it was not examined?
3. Are perspectives listed in §2.3?
4. Does every finding have the five labels: location, what is wrong, evidence, impact, and disposition?
5. Does every finding have a disposition, with a transcription destination or a reason not to transcribe? `rg -c '^\*\*(Disposition|扱い)\*\*' docs/reviews/<slug>.md` must match the number of findings
6. Do the rows of the list table correspond one-to-one with the bodies? Is there no ID in only one of them?
7. Is every finding's kind one of the four, and does the destination in the disposition correspond to the table in §"Transcription"?
8. Does confidence agree with the evidence? Do findings with confidence High not contain "seems", "should", or "might" (「思われる」「はず」「かもしれない」 in Japanese)?
9. Does §1.2 have all four: review date, type of review, target commit, and reviewer?
10. Do references to code have line numbers? `rg -nH '\]\((\.\./)+[^)#]*\.[A-Za-z0-9]+\)' docs/reviews/*.md | rg -v '\.md\)'` must be empty (it picks up links to code that lack `#L`, excluding `.md` links between documents)
11. Are identifiers of transcription destinations not links? `rg -n '\*\*(Disposition|扱い)\*\*' -A 2 docs/reviews/<slug>.md` must contain no `](`
12. Are no summaries of changes or fix code pasted? Do code blocks fit within the one exception in §"What Not to Write"?
13. Are places skimmed without suspicion not mixed into §5?
14. Does every line in §6 have a date?
15. If a published document was touched, are the changes limited to appending to §6 and fixing typos? Confirm with `git diff` that there is no diff in §1 to §5
16. Does `docs/reviews.md` have this review's row, and does the Findings column match the count in §4?
17. Do the rows of `docs/reviews.md` correspond one-to-one with `docs/reviews/*.md`? In rows whose Transcription column is `done`, are there no findings with an empty disposition?
18. Are identifiers of transcription destinations the bug's `<slug>`? `rg -n 'I-[0-9]' docs/reviews/` must be empty

## Example: Perspectives

Write the perspectives actually looked for in that review.
The following are examples; do not paste them as is.
Writing perspectives that were not looked for hides in §2.3 what should be written in §2.2.

Perspectives that often apply in diff reviews:

- Do the callers of changed functions satisfy the premises after the change?
- Are there tests for the added branches?
- Are existing invariants (in the topic sections of the relevant design document) not broken?
- Are errors not swallowed?
- Have externally visible contracts (API, configuration, storage formats) not changed?

Perspectives that often apply in audit reviews:

- Do dependencies across layers point in the designed direction?
- Is the same processing not copied in several places?
- Does state not remain half-done on failure paths?
- Are there no places that break under concurrent execution?
- Do the identifiers in `terms.md` and the names in the implementation not disagree?

Narrow the perspectives to three to six.
A review that lists ten has usually not actually examined several of them.

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| `1. About This Review` | `1. このレビューについて` |
| `1.1 Document Responsibilities` | `1.1 文書間の責務分担` |
| `1.2 Review Date and Target` | `1.2 レビュー日と対象` |
| `2. Scope and Perspectives` | `2. 範囲と観点` |
| `2.1 Examined Scope` | `2.1 見た範囲` |
| `2.2 Unexamined Scope` | `2.2 見ていない範囲` |
| `2.3 Perspectives` | `2.3 観点` |
| `3. Overall Assessment` | `3. 総評` |
| `4. Findings` | `4. 指摘` |
| `5. Checked and Found Fine` | `5. 確かめて問題がなかったこと` |
| `6. Aftermath` | `6. その後` |
| Parent columns `Review` / `Type` / `Findings` / `Transcription` | `レビュー` / `型` / `指摘` / `転記` |
| Type `diff` / `audit` | `差分` / `監査` |
| Transcription `done` / `R-2 not transcribed` | `完了` / `R-2 未転記` |
| Findings columns `ID` / `Summary` / `Kind` / `Confidence` / `Disposition` | `ID` / `概要` / `種別` / `確度` / `扱い` |
| Kind `Bug` / `Design question` / `Terminology` / `Improvement` | `不具合` / `設計論点` / `用語` / `改善提案` |
| Confidence `High` / `Medium` / `Low` | `高` / `中` / `低` |
| `**Kind: Bug**` / `**Confidence: High**` | `**種別: 不具合**` / `**確度: 高**` |
| `**Location**` | `**該当箇所**` |
| `**What is wrong**` | `**何が問題か**` |
| `**Evidence**` | `**根拠**` |
| `**Impact**` | `**影響**` |
| `**Disposition**` | `**扱い**` |
| "No findings." | 「指摘なし」 |
