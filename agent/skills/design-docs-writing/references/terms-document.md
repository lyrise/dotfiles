# Terms Documents

When writing, revising, or checking `docs/terms.md` and `docs/terms/<slug>.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to terms documents.

The terms documents are the single authoritative source for vocabulary.
Design documents, the bug list, external knowledge, plans, and review result documents do not define terms; they use the vocabulary of this document as given.

The reason for making this authoritative source independent is that vocabulary is consulted more widely than design rationale.
What an agent writing code needs is the mapping between terms, type names, and external forms, not rejected alternatives.
If that lived in a section of a design document, looking up one term would mean reading the whole design document.

Terms documents are permanent and have no investigation date or target commit.

## Shape of the Parent Document

The section structure of `docs/terms.md` is as follows.

```
1. About This Document
   1.1 Document Responsibilities
2. Term List
3. Boundaries Between Adjacent Terms
4. Individual Terms
```

Sections 1 and 2 are required.
Include section 3 only when there are pairs whose boundaries need writing, and section 4 only when there are terms with scope `global` that have an entry; otherwise omit the heading entirely.

Number headings in the form `## 1.` `### 1.1`.
Do not number `####`.

### 1. About This Document

State in one or two sentences that this document is the single authoritative source for vocabulary.

Write **1.1 Document Responsibilities** as a table.
Write here what this document holds (term definitions, notation, aliases, boundaries, reasons for names) and what it does not hold (design rationale, implementation status, bugs, external behavior), and link to where the authoritative source is delegated.
State in one line that the family map is held by `[design.md](./design.md#11-document-responsibilities)`.

### 2. Term List

Put every term in one table.
The six columns are Term, Scope, Identifier, External form, Meaning, and Avoided aliases.

| Column | What to write |
| --- | --- |
| Term | The notation actually used in the documents. Terms with an entry link to it |
| Scope | `global`, or the slug of the concern the term is confined to |
| Identifier | The type or function name in the code. If it varies by layer, write one representative, and show the mapping in the entry |
| External form | API field names, URLs, on-screen text. `-` if none |
| Meaning | A one-line definition |
| Avoided aliases | Synonyms that should not be used. `-` if none |

```markdown
| Term | Scope | Identifier | External form | Meaning | Avoided aliases |
| --- | --- | --- | --- | --- | --- |
| [Session](#t-session) | global | `Session` | `session_id` | One connection of an authenticated user | login state |
| [Snapshot](./terms/storage.md#t-snapshot) | storage | `Snapshot` | `snapshot` | The entire tree at a point in time | backup |
```

The link target in the Term column is an anchor in §4 of this document if the scope is `global`, or an anchor in `docs/terms/<slug>.md` if it is a concern.
Do not link terms that have no entry.

Keep **Meaning** to one line.
A term that cannot be written in one line has usually split into two terms.
If it cannot be split, it is a term that meets condition 2 of §"4. Individual Terms" and gets an entry.

Order rows by scope, and within the same scope alphabetically by identifier.
This lets a reader responsible for one concern read the terms relevant to them in one stretch.

### 3. Boundaries Between Adjacent Terms

Only this section holds the boundaries of term pairs that get misused.
Do not write them in a term's entry.
A boundary is an attribute not of a term but of a pair of terms; writing it in both terms splits the same fact into two places, and one goes stale.

Pairs of terms with different scopes go here too.
Moving the boundary into one side's `docs/terms/<slug>.md` keeps the other side's owner from noticing it.

Write entries one pair per `####` heading, in the following form.

```markdown
<a id="t-session-vs-token"></a>
#### Session and token

**Boundary**
What belongs to which, and what does not.

**What goes wrong if confused**
What actually happens when they are misused.
```

A pair for which **What goes wrong if confused** cannot be written is not confused in the first place.
In that case, do not add an entry; the Meaning and Avoided aliases columns of the table are enough.

Anchors take the form `t-<a>-vs-<b>`.

### 4. Individual Terms

Put here the terms with scope `global` that have an entry.
Entries for terms confined to a concern are in `docs/terms/<slug>.md`, not in this section.

Only terms that meet one of the following three conditions have an entry; for the rest, the table is enough.

1. The type name changes by layer
2. It gets misused with an adjacent term
3. There is a history of choosing the name again

A term that meets condition 2 gets a pair entry in §3, not an entry of its own.
Only conditions 1 and 3 give a term its own entry.

Write entries one term per `####` heading, in the following form.

```markdown
<a id="t-session"></a>
#### Session

**Names by layer**
daemon `Session` / API `session_id` / screen "Logged in"

**Why this name**
Rejected names, and why they were rejected.
```

If only condition 1 applies, include only Names by layer; if only condition 3, only Why this name.
If both apply, include both.

For a term whose type name changes by layer, always write the mapping.
The fact that it has two names itself shows a layer boundary.

Anchors take the form `t-<identifier in kebab-case>`.
Do not number them.
Terms have no order, and `T-7` does not tell you what it points to.

When a term is renamed, change its anchor too.
The old anchor breaking conveys the information that the name no longer exists.

## Shape of Child Documents

A child holds only the entries of terms confined to one concern.

```markdown
# storage terms

Part of [terms.md](../terms.md). Holds the entries of terms confined to this concern.
The list of terms and the boundaries with other terms are in the parent.

<a id="t-snapshot"></a>
## Snapshot

**Names by layer**
daemon `Snapshot` / API `snapshot`

**Why this name**
Rejected names, and why they were rejected.
```

The entry form and the conditions for having an entry are the same as in §"4. Individual Terms".
Only the heading level changes from `####` to `##`.
Children are entered from the parent's list, so following §"Granularity of the Responsibilities Table" in the common rules, they have no §1.1; one line at the top linking to the parent is enough.

Do not copy the term list table into a child.
Do not write boundaries between adjacent terms in a child.

## Splitting

A single `docs/terms.md` is the default.
For a concern that has a `docs/design/<slug>.md`, create `docs/terms/<slug>.md` for that concern when several terms have entries (the three conditions in §"4. Individual Terms").

Make `<slug>` the same concern name as `docs/design/<slug>.md`.
Do not use a term's name as `<slug>`.
Splitting terms into one file each leaves readers unable to identify which file holds the boundary with an adjacent term, and also breaks reading the glossary straight through.

The scope column uniquely determines where the entry goes.

| Value of the scope column | Where the entry goes |
| --- | --- |
| The slug of that concern | `docs/terms/<slug>.md` |
| `global` | §"4. Individual Terms" in `docs/terms.md` |

Boundaries between adjacent terms are held by `docs/terms.md` regardless of scope (§"3. Boundaries Between Adjacent Terms").

Even after splitting, the term list in `docs/terms.md` keeps holding every term.
If the list split, looking up one term would mean opening several files, defeating the point of making this document independent.

## Three Modes

**Create**: create `docs/terms.md` together with `design.md`.
Read the code and the external interfaces, gather the project-specific terms, and then fill in the table.

**Update**: touch it when terms increase, when a term is renamed, or when an alias that should not be used appears.
Do not touch it when implementation has merely progressed.

**Check**: run §"Post-Writing Check" mechanically; do not change the body, and report only findings and their grounds.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- What the term means
- The notation used (identifier in code, external form, names by layer)
- Avoided aliases
- Boundaries with adjacent terms, and what happens if they are confused
- The history of choosing the name again, and the rejected names

## Verification Subagent

Following §"Verification Subagent" in the common rules, replace the scope in which the `verifier` is required with the following.

It is required for creating; if it is unavailable, report without creating the document.
For updates, it is required only when deleting a term, adding or deleting an entry, rewriting a boundary, or creating `docs/terms/<slug>.md`.
Adding a row to the table, or only correcting an identifier or external form, does not require it.
This is an exception so that implementation does not stall midway; verify these together the next time a rewrite that requires it is made.
A check does not change the body and does not require it.

Add the following to the blocking findings.

- A table row lacks any of Term, Scope, Identifier, or Meaning
- A term that does not meet the conditions for an entry has one
- A term that meets the conditions has no entry
- A boundary between adjacent terms is outside `docs/terms.md`
- The boundary of the same pair is written in two places
- A term listed in Avoided aliases also appears in the Term column of another row
- An identifier or external form disagrees with the code
- The value of the scope column and the location of the entry do not correspond

## Lifecycle

- Create `docs/terms.md` together with `design.md`
- When a new term appears in implementation, add a row to the table within that work
- When a detail document for a concern is created and several terms with entries are confined to it, move them to `docs/terms/<slug>.md`
- In work that adds or changes externally visible names, include updating this document in the completion criteria of the steps ([Implementation Plans](implementation-plan.md))
- Move naming decisions made during the work to this document when folding the plan
- When a review produces a finding of kind Terminology, transcribe it to this document ([Review Result Documents](review-document.md))
- When a term is no longer used, delete its table row and entry

Move a term that is no longer used into Avoided aliases only when that name can still appear in the code or external forms.
Keeping a term that appears nowhere as an alias turns the table into a graveyard.

## What Not to Write

Do not write **general technical terms**.
The external world is the authoritative source for explanations of `OAuth`, `gRPC`, and `mutex`.
Write the meaning only when the project gives the term a project-specific meaning.

If this project also uses a term defined externally, put a row in the table and record only the mapping of identifier and external form.
How the mechanism the term refers to actually behaves is held by [External Knowledge](knowledges-document.md).

**Design rationale** is held by design documents.
What this document holds is only the reason for choosing a name, not the reason for choosing the mechanism.
"Why are sessions kept on the server side?" is a design decision; "Why is it called `Session`?" belongs to this document.

Do not write **implementation status**.
Even for a concept not yet implemented, add a row if its name has been decided.

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Does every row of the table have Term, Scope, Identifier, and Meaning? Are empty cells filled with `-`?
2. Does Meaning fit in one line? Has a term that does not fit not split into two terms?
3. Does every term with an entry meet one of the three conditions in §"4. Individual Terms"? Are there no terms that meet them but lack an entry?
4. Do the links in the Term column correspond one-to-one with the entry anchors? Does the linked file correspond to the scope column?
5. Are boundaries between adjacent terms only in §3 of `docs/terms.md`? `**Boundary**` (`**境界**` in Japanese) must not appear in `docs/terms/*.md`
6. Is the boundary of the same pair not written in two places?
7. Does no term listed in Avoided aliases appear in the Term column of another row?
8. Is the scope column `global` or the slug of an existing `docs/design/<slug>.md`?
9. Is the term list table only in `docs/terms.md`? Has it not been copied into children?
10. Do identifiers and external forms match the code? Check each term with `rg`
11. Are general technical terms, design rationale, implementation status, and external behavior not mixed in?

## Japanese Equivalents

When writing in Japanese, use the following headings, labels, column names, and values.

| English | Japanese |
| --- | --- |
| `1. About This Document` | `1. このドキュメントについて` |
| `1.1 Document Responsibilities` | `1.1 文書間の責務分担` |
| `2. Term List` | `2. 用語一覧` |
| `3. Boundaries Between Adjacent Terms` | `3. 隣接語の境界` |
| `4. Individual Terms` | `4. 個別の用語` |
| Columns `Term` / `Scope` / `Identifier` / `External form` / `Meaning` / `Avoided aliases` | `用語` / `スコープ` / `識別子` / `外部表現` / `指すもの` / `使わない別称` |
| Scope value `global` | `全体` |
| `**Boundary**` | `**境界**` |
| `**What goes wrong if confused**` | `**取り違えると何が起きるか**` |
| `**Names by layer**` | `**層ごとの名前**` |
| `**Why this name**` | `**この名前にした理由**` |
| Child title `# <slug> terms` | `# <slug> の用語` |
