# Design Document

When writing, revising, splitting, or checking the design documents whose entry point is `docs/design.md`, follow this document.
For the family's responsibilities, parents and children, identifiers, style, diagrams, information density, handling of evidence, and link conventions, follow the [common rules](../SKILL.md); this document defines only what is specific to design documents.

Design documents do not define terms.
The terms documents ([Terms Document](terms-document.md)) are the authoritative source for term definitions, notation, aliases, and boundaries with adjacent terms, and design documents use that vocabulary as given.

## Shape of the Parent Document

The first three sections and the last two are required, in this order.
The topic sections in between vary by project.

```
1. About This Document
   1.1 Document Responsibilities
   1.2 Tense of This Document
2. What X Is / Out of Scope
   2.1 Out of Scope
3. Overall Structure
   3.1 Component and Directory Map
   3.2 Processing Flow

--- Topic sections (project-dependent; number and headings are free) ---
4. …
N. …

--- End ---
N+1. Design Decisions
   N+1.1 Decided
   N+1.2 Deferred
N+2. Current State and Remaining Work
```

Number headings in the form `## 1.` `### 1.1`.
Do not number `####`.

Do not include a glossary section.
The vocabulary must be in place before reading the topic sections, but what provides it is `terms.md`, not a section of this document.

### 1. About This Document

State in two or three sentences what the document covers and who the intended readers are.
Then put the line "This document assumes the vocabulary of [terms.md](./terms.md). It contains no term definitions."

Write **1.1 Document Responsibilities** as a table.
This section is required, and it is the only place in the family that holds the upper tier of the map.
List what is the authoritative source in which document in this repository, covering the six parents (this document, `terms.md`, `issues.md`, `knowledges.md`, `plans.md`, `reviews.md`), the `docs/design/*.md` children, API definition files, and `README.md`.
Then state explicitly what is not put in this document.

Do not list the children of `terms/`, `issues/`, `knowledges/`, `plans/`, or `reviews/` here.
Each parent's list holds them (§"Granularity of the Responsibilities Table" in the common rules).
If this section changed every time a bug was filed, design diffs and document-management diffs would mix.

Leave only `this document` unlinked, and make every other document name a relative Markdown link to the actual file.
Write `[terms.md](./terms.md)`, `[issues.md](./issues.md)`, and, for the repository root, `[README.md](../README.md)`.

In **1.2 Tense of This Document**, state that the body is written in the present tense as the finished design, and that the implementation status is in the current state and remaining work section.
Always include the line "If you want to know what works now, read section N first."

### 2. What X Is / Out of Scope

State what it does and the intended operation (scale, number of users, exposure).

In **2.1 Out of Scope**, list what was decided not to build.
Then write the mechanisms that are unnecessary because of excluding them.
Tie out-of-scope decisions to the simplicity of the design, as in "Since there are no shared links, there is no permission model."
With this sentence, the cost of a later proposal to widen the scope can be read.

### 3. Overall Structure

Make **3.1** a table mapping directories to components.
On each row, write the path, the package name, and the role.
The displayed text of the path column is the path relative to the repository root, and the link target is the relative path from `docs/design.md` to the actual location.
For example, write `[daemon/entrypoints/daemon](../daemon/entrypoints/daemon)`.
For generated artifacts, state "do not edit by hand" in the table.

Put a diagram of the processing flow in **3.2**.

### Topic Sections

Put one concern per section:
a layer, a feature, or a convention.

In each subsection, write why it has that shape before what it does.
A subsection that writes only the shape duplicates the code and has no value.

Write invariants together with the premises under which they hold.
Write down to the conditions under which the premises break.
For example, if you write "publish atomically with rename", go on to write that this holds only within the same file system, and how it breaks across file systems.

Use the following two guidelines for the granularity of topics.

- A section covers one layer or one feature. Do not make sections that span layers
- Create a "Conventions for …" section only when there are decision criteria that cut across multiple endpoints or operations

### Design Decisions Section

Write **Decided** items one decision per `####` heading, in the following form.

```markdown
#### Summary of the decision, as a noun phrase or a plain statement

**Decision**
What was decided. Write the promise, not the implementation.

**Reason**
Why it was chosen. What was prioritized and what was given up.

**Rejected alternatives**
Alternatives considered and rejected, and why they were rejected.
```

Write **Rejected alternatives** only when alternatives were considered.
For decisions without any, do not include the block.
However, always write an alternative that was once adopted and has left traces in the code or dependencies.
If it is not written, the same alternative will be proposed again later.

Do not write naming decisions here.
`terms.md` holds the rejected names and their reasons ([Terms Document](terms-document.md)).

Write **Deferred** items one item per `####` heading, in the following form.

```markdown
#### The deferred question

**Current state**
How things stand now.

**Why not decide now**
Why it has been possible not to decide.

**Condition for deciding**
What must happen for it to be decided.
```

**Condition for deciding** is required.
An item without it is not deferred but abandoned, and there is no point in writing it.
Write the condition as an observable event ("when access from outside the LAN is actually needed", "when search becomes unusable at production tree sizes").

For a deferred item with several options, list the options numbered and add one sentence on the cost of each.

### Current State and Remaining Work Section

Write the implementation status only in this section.
Do not scatter status notes across the subsections of the body.
Do not put an implementation status summary table at the top either.
When the state is written in two or more places, one of them always goes stale.

Write the **roadmap** as a table.
State explicitly that the order is provisional and that only the dependencies need to be respected.
The table's basic columns are the number, the content, and the dependency it assumes.

Do not write bugs.
At the end of the section, put one line pointing to `[issues.md](./issues.md)`.

### What Not to Write in Design Documents

**Do not copy what has another single authoritative source.**
The terms documents hold term definitions and notation.
`knowledges.md` holds how dependency libraries, the OS, and external APIs actually behave; this document writes only what was chosen on the basis of those facts and links to the `knowledges.md` item.
The API definition file holds exhaustive lists of API paths and status codes.
The code holds byte layouts, serialization field numbers, and encoding details.
`README.md` holds setup steps and dependency packages.

**Do not write what can be looked up mechanically.**
Do not write lists of unimplemented places, lists of `TODO`s, or file lists.
Instead, write one line on how to look them up ("the actual unimplemented places can be found with `rg 'todo!' src`").

The exception is limited to cross-cutting conventions whose whole can be grasped only as a table.
Things that must be seen at a glance as decision criteria, such as "which operations are synchronous and which asynchronous" or "the mapping between error kinds and HTTP status", may be written as a statement of convention rather than a copy.
In that case, state that the individual definitions are in the original documents.

## Shape of Child Documents

There are two differences from the section structure of `design.md`.
Section 2 becomes "Responsibilities and Boundaries", and there is no overall structure section.
Section numbers are closed within the detail document and do not continue those of `docs/design.md`.

```text
1. About This Document
   1.1 Document Responsibilities
   1.2 Tense of This Document
2. Responsibilities and Boundaries

--- Topic sections (concern-dependent) ---
3. …
N. …

--- End ---
N+1. Design Decisions
   N+1.1 Decided
   N+1.2 Deferred
N+2. Current State and Remaining Work
```

`1.1` does not hold the family map; it shows, with relative links, the boundaries with `docs/design.md`, detail documents whose concerns border this one, API definitions, and so on.
Apply the same rules as `docs/design.md` to `1.2`, the topic sections, the design decisions section, and the current state and remaining work section.
Write the pointer to bugs as `[issues.md](../issues.md)`, the relative path from the detail document.

## Splitting

### Deciding to Split

First remove duplication, copies of authoritative sources, and boilerplate without content, following §"Semantic Elements to Preserve" and §"Information Density" in the common rules.
Of the topics that still remain, split out only concerns that have independent responsibilities and boundaries and need not always be read with the other topics.
Do not use line, character, or token counts alone as a reason to split.

For new documents, a single `docs/design.md` is the default.
When checking, report only split candidates and their grounds; do not split without a request to update (§"Parents and Children" in the common rules).

### Placement and Naming

Keep `docs/design.md` as the single entry point to the design documents, and put detail documents in `docs/design/<slug>.md`.
`<slug>` is a stable lowercase kebab-case name for the concern and does not include a section number.
This keeps file names and links unchanged when sections are added or reordered.
Do not split detail documents further into subdirectories.

```text
docs/
├── design.md
├── design/
│   ├── authentication.md
│   ├── storage.md
│   └── task-execution.md
├── terms.md
└── issues.md
```

After splitting out a concern into a detail document, check whether there are several terms with entries confined to that concern, and if so, create `docs/terms/<slug>.md` with the same `<slug>` ([Terms Document](terms-document.md)).
File names are aligned so that someone reading the design and someone looking up a term can name the destination by the same name.

### Responsibilities After Splitting

| Document | What it holds |
| --- | --- |
| `docs/design.md` | Project-wide scope, overall structure, boundaries between concerns, cross-cutting design decisions, overall dependencies |
| `docs/design/<slug>.md` | Responsibilities and boundaries, invariants, design details, design decisions, and current state and remaining work confined to one concern |

Give each fact, decision, and deferred item exactly one authoritative source.
Put cross-cutting content in `docs/design.md` and content confined to one concern in the detail document.

Put term definitions in neither.
`terms.md` is the single authoritative source for vocabulary, and terms confined to a concern show where they belong in the scope column of `terms.md`.

In the topics of `docs/design.md`, keep only a summary that conveys the split concern's purpose, boundaries, and relationship to other concerns, plus a relative link to the detail document.
Do not copy details, invariants, decisions, deferred items, or implementation status.
The overall current state and remaining work section holds only dependencies between concerns and does not restate the implementation status of detail documents.

In §1.1 of `docs/design.md`, list every detail document and what each document tells you.
Each detail document links from its §1.1 to `docs/design.md` with a relative link and states explicitly what it does and does not cover.

### Migrating Existing Documents

1. List the subsections to be moved, design decisions, deferred items, current state and remaining work, and references from within the repository.
2. Decide one destination for each semantic element and build an internal mapping table. Do not leave the mapping table in the deliverable.
3. Move not only the details but also the reasons, invariants, decisions, deferred items, and implementation status confined to that concern.
4. Keep the original topic heading and replace its content with a summary of the purpose, boundaries, and relationship to other concerns, plus a link to the detail document.
5. Update §1.1 of `docs/design.md` and the overall dependencies.
6. Search references in the repository and update links to moved headings to the new file and anchor.

When an existing heading must be deleted or renamed, first check every reference in the repository.
Keep headings that may be referenced from outside as summary headings in `docs/design.md`.

### Verifying the Split

Treat a split as a structural update, not compression.
Measure the character and line counts of the whole document family before and after the split, but allow only increases from adding pointers, responsibilities, and tense notes, and report that increase.
If compression was also requested, measure the reduction of the moved body separately from the increase needed for the split.

Confirm the following with mechanical checks and the `verifier`.

1. The responsibilities, boundaries, invariants and the conditions that break them, decisions, rejected alternatives, deferred items, implementation status, dependencies, and remaining work from before the move have not been lost
2. Each semantic element has one authoritative source, and the body is not duplicated between `docs/design.md` and the detail documents
3. Every detail document is reachable from `docs/design.md`, and each detail document can lead back to the entry point
4. Cross-cutting content and content within a concern are placed according to the division of responsibilities
5. Existing links in the repository, heading anchors, and relative links based on each document are not broken
6. Design documents have no line-number links to code, and implementation status has not leaked outside each document's current state and remaining work section
7. Links from `issues.md` to moved content include the heading in the new detail document
8. Term definitions have not crept into detail documents during the move

## Three Modes

**Create**: read the code, set up the skeleton of `design.md` first (§"Shape of the Parent Document"), and fill in each section.
At the same time, create `docs/terms.md` and define the terms used in the body there.
Do not fill in what could not be confirmed.

**Update**: touch the body when a design decision changes, or when compression or splitting is explicitly requested.
When implementation has merely progressed, do not rewrite the body; fix only the current state and remaining work section and `issues.md`.

**Check**: run the checklist in §"Post-Writing Check" mechanically.
Do not change the body; report only findings, including compression and split candidates, and their grounds.

## Semantic Elements to Preserve

Following §"Information Density" in the common rules, keep the following even when compressing.

- Responsibilities and boundaries
- Invariants, their premises, and the conditions under which they break
- Decisions, reasons, and alternatives actually considered and rejected
- For deferred items: the current state, why not decide now, and the condition for deciding
- Implementation status, dependencies, and remaining work

## Verification Subagent

Following §"Verification Subagent" in the common rules, the `verifier` is required for creating and updating.
Add the following to the blocking findings.

- Term definitions mixed into design documents
- After a split: duplicated authoritative sources, detail documents unreachable from the entry point, or missing responsibilities
- Implementation status leaking outside the current state and remaining work section
- Deferred items without a condition for deciding

## Post-Writing Check

In addition to §"Common Post-Writing Check" in the common rules, confirm the following.

1. Has text about implementation status not leaked outside each design document's current state and remaining work section and `issues.md`? Search for phrases such as "not implemented", "not started", and "not wired" (「未実装」「未着手」「未結線」 in Japanese)
2. Does every deferred item have a "condition for deciding"?
3. Are term definitions not mixed into design documents? Are there no remaining glossary sections or paragraphs defining what a term means?
4. Does section 1 have the line assuming `terms.md`?
5. Does §1.1 of `design.md` list the six parents and `design/*.md`, and not list the children of other families? Does §1.1 of each detail document write only where things are delegated?
6. Has nothing whose authoritative source is another document been copied? Have lists of API paths, field numbers, or `TODO`s not crept in?
7. For each changed subsection, did you internally check where each semantic element from before compression ended up after compression? Do not leave the mapping table in the document
8. Did you measure character and line counts right before and after compression, and do they not increase after compression?
9. If split, are all eight items in §"Verifying the Split" satisfied?

## Example: Topic Sections in a Daemon-Style Repository

In a repository composed of a daemon, an engine, and a generated interface, with the API definition file as the authoritative contract, the topic sections line up as follows.
This is an example and need not be used as is.

```
4. Internal Structure of the daemon
   4.1 Layer structure (write what each layer does not know)
   4.2 Code generation from the API definition
   4.3 Error model and HTTP mapping
5. Storage Layer
   5.1 The facade and the chain of drivers
   5.2 Each driver
   5.3 Atomicity of writes (premises, and the conditions that break them)
6. (Domain-specific features)
7. Authentication and Sessions
   7.1 Initial setup
   7.2 Carrying and storing sessions
8. Conventions for Mutating APIs
   8.1 Namespaces
   8.2 Deciding synchronous vs. asynchronous (table)
   8.3 Conflict policy
   8.4 State transitions of long-running operations
9. Configuration and Persistence
   9.1 Configuration file
   9.2 Where state lives (table with a column for the impact when it is lost)
10. Clients
```

## Japanese Equivalents

When writing in Japanese, use the following headings and labels.

| English | Japanese |
| --- | --- |
| `1. About This Document` | `1. このドキュメントについて` |
| `1.1 Document Responsibilities` | `1.1 文書間の責務分担` |
| `1.2 Tense of This Document` | `1.2 本書の時制について` |
| `2. What X Is / Out of Scope` | `2. 〇〇とは / スコープ外` |
| `2.1 Out of Scope` | `2.1 スコープ外` |
| `2. Responsibilities and Boundaries` (child) | `2. 責務と境界` |
| `3. Overall Structure` | `3. 全体構成` |
| `3.1 Component and Directory Map` | `3.1 コンポーネントとディレクトリ対応表` |
| `3.2 Processing Flow` | `3.2 処理の流れ` |
| `N+1. Design Decisions` | `N+1. 設計判断` |
| `N+1.1 Decided` | `N+1.1 決定済み` |
| `N+1.2 Deferred` | `N+1.2 保留` |
| `N+2. Current State and Remaining Work` | `N+2. 現状と残作業` |
| `**Decision**` | `**決定**` |
| `**Reason**` | `**理由**` |
| `**Rejected alternatives**` | `**却下案**` |
| `**Current state**` | `**現状**` |
| `**Why not decide now**` | `**なぜ今決めないか**` |
| `**Condition for deciding**` | `**決める条件**` |
| `this document` | `本書` |

The fixed lines in section 1 become 「本書は [terms.md](./terms.md) の語彙を前提とする。語の定義は本書にない」 and 「いま何が動くのかを知りたい場合は N 章を先に読む」.
