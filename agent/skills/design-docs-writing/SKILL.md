---
name: design-docs-writing
description: Writing rules for a software project's document family (design.md, design/*.md, terms.md, terms/*.md, issues.md, issues/*.md, knowledge.md, knowledge/*.md, plans.md, plans/*.md, reviews.md, reviews/*.md). Defines the division of roles between parents and children, the division of responsibilities and lifetimes between documents, fixed section structures, the contract for terms and naming, the forms for design decisions, bugs, external knowledge, and findings, observable completion criteria, evidence and confidence, style, diagrams, information compression that preserves meaning and readability, and verification procedures including a strict read-only verifier. Use when writing, updating, splitting, checking, or folding design documents, glossaries, known-bug lists, external knowledge, implementation plans, or review result documents, or when transcribing findings.
---

# Writing Rules for Project Documents

When writing, revising, splitting, checking, or folding documents under `docs/`, follow the rules below.
This document defines only the rules common to the document family and how to choose a reference; each reference holds the section structure and forms specific to its document type.
Read the reference that matches the request, and combine the relevant references when handling several documents.
Before starting, read `../sanitize-artifacts/SKILL.md`. If the documents are written in Japanese, also read `../japanese-tech-writing/SKILL.md`.

The artifact's own structure, evidence, and constraints, and the repository's conventions, take precedence over both skills.
Build Japanese parts according to `japanese-tech-writing` from the first draft.
Before finishing, recheck with the applicable skills, and remove redundancy, unnatural phrasing, and leftovers of the production process without changing the meaning.

These rules protect three things.
First, as implementation progresses, the places where documents must be rewritten stay local.
Second, a later reader (yourself months later, or an AI agent) does not confuse facts, guesses, and open questions.
Third, when a short-lived document disappears, the decisions made there, the vocabulary, and what was confirmed about the outside world are not lost.

## Language

Write in the language of the existing documents under `docs/`.
If there are no existing documents to go by, write in English.
Do not mix languages within one document family.

Each reference defines its fixed headings, labels, column names, and enumerated values in English.
When writing in Japanese, use the Japanese equivalents listed in the "Japanese Equivalents" section at the end of each reference.
Anchors in links follow the actual headings, so with Japanese headings, use anchors such as `#3-全体構成` in place of `#3-overall-structure`.

## Choosing a Reference

| Request | Reference to read |
| --- | --- |
| Write, update, check, or split design documents | [Design Document](references/design-document.md) |
| Define or rename terms, or check the glossary | [Terms Document](references/terms-document.md) |
| Record a bug, or check the known-bug list | [Issue List](references/issue-list.md) |
| Record external behavior, or check external knowledge | [Knowledge Document](references/knowledge-document.md) |
| Write, update, or fold an implementation plan | [Implementation Plan](references/implementation-plan.md) |
| Record or check review results, or transcribe findings | [Review Document](references/review-document.md) |

When starting documents for a new project, create the design document and the terms document at the same time.
The design document holds no term definitions, so without a terms document there is nowhere to put the vocabulary.

## The Document Family and Responsibilities

| Document | What it holds | Lifetime |
| --- | --- | --- |
| `docs/design.md` | The map of the document family, scope, overall structure, boundaries between concerns, cross-cutting design decisions | Same as the project |
| `docs/design/<slug>.md` | Responsibilities and boundaries, invariants, design details, and design decisions confined to one concern | Same as the project |
| `docs/terms.md` | The vocabulary list, boundaries with adjacent terms, definitions of terms not confined to one concern | Same as the project |
| `docs/terms/<slug>.md` | Definitions, notation, avoided aliases, and rejected names of terms confined to one concern | Same as the project |
| `docs/issues.md` | The bug list, relationships between items, investigation dates and target commits | Same as the project |
| `docs/issues/<slug>.md` | One bug's symptom, location, cause, impact, and remedy | Until fixed |
| `docs/knowledge.md` | The list of external knowledge, verification targets, relationships between items | Same as the project |
| `docs/knowledge/<slug>.md` | One fact confirmed about the outside world, and its source | Until the outside changes |
| `docs/plans.md` | The list of work in progress, and the dependencies between pieces of work | Same as the project |
| `docs/plans/<slug>.md` | What this work builds, in what order, and when it is finished | Until the work ends |
| `docs/reviews.md` | The review history, and the transcription status of findings | Permanent |
| `docs/reviews/<slug>.md` | When, what scope, from what perspectives, on what evidence, and what was judged | Permanent |

Decide boundaries with the following five questions.

**Is it the term itself, or the structure described with the term?**
Term definitions, notation, aliases, boundaries with adjacent terms, and the reason a name was chosen belong to the terms documents.
Design documents, the bug list, and plans do not define terms; they use the vocabulary of the terms documents as given.

**Is it about our own code, or about something external?**
How dependency libraries, the OS, protocols, and external APIs actually behave belongs to `knowledge`.
What was chosen on the basis of that behavior is a design decision and belongs to the design document responsible for that concern.
Even when external behavior is the trigger, if the fix is in our own code, it is a bug and goes in `issues.md`.

**Is it known how to fix it?**
Something where it is known what to fix and how is a bug and goes in `issues.md`.
Something where what to choose is not yet decided is a design question and goes in the design decisions section of the design document responsible for that concern.

**Is it the current state, or a past act?**
`issues.md` holds what is broken now, and items disappear with the fix.
`reviews/<slug>.md` holds who looked at what at some point, and does not disappear when things are fixed.
It is normal for the same bug to appear in both; do not delete one and consolidate into the other.

**Does it outlive the work?**
Do not write in a plan anything whose value remains after the work is finished.
When a new design decision is made during planning or review, write it first in the design document that is its authoritative source, and put only the conclusion and a reference in the plan or review result document.
In the reverse order, the reason disappears when the plan is deleted.

Do not keep the bug list as a section of a design document.
Separate it into `issues.md` even when there are few items.
The two have different lifetimes: items in `issues.md` disappear with the fix, but design decisions remain.

## Parents and Children

`docs/<family>.md` is called the parent and `docs/<family>/<slug>.md` a child.

The parent holds the whole-picture material:
what the family covers and does not cover, the list of children, and the relationships between children.
A child holds one unit:
one concern, one group of terms confined to one concern, one bug, one external fact, one piece of work, or one review.

Do not divide items of the same kind between parent and child by length.
Decide uniquely, by each family's rule, where they go; do not push only the items that grew long into children.
Dividing by length leaves readers unsure where an item is, so they always have to look in two places.

When to create children differs by family.

| Family | When to create children |
| --- | --- |
| `issues`, `knowledge` | From the first item. Items are independent of each other and there is no reason to read them together |
| `plans`, `reviews` | Always. One piece of work and one review are one document from the moment they are born |
| `design`, `terms` | When a concern is judged to have independent responsibilities and boundaries and need not always be read with the others. Do not split by line count |

When every family has fully grown, it looks like this.

```text
docs/
├── design.md
├── design/
│   └── storage.md
├── terms.md
├── terms/
│   └── storage.md
├── issues.md
├── issues/
│   └── timer-leak.md
├── knowledge.md
├── knowledge/
│   └── tokio-localset.md
├── plans.md
├── plans/
│   └── storage-facade-split.md
├── reviews.md
└── reviews/
    └── 2026-08-10-storage-facade.md
```

Only `design/` and `terms/` share child file names.
The difference is whether the same concern is read as design or looked up as vocabulary, so the destination should be nameable by the same name.

A new project creates only `docs/design.md` and `docs/terms.md`.
The parents of the other families are created together with a child when the first item arises.
Do not put an empty parent in place ahead of time.

When checking, report only split candidates and their grounds; do not split without a request to update.

### Identifiers

The identifier for an item is the `<slug>` of the child's file name.
Do not use sequential numbers such as `I-1` or `K-1`.
Numbers leave gaps when items disappear, and renumbering shifts every reference.

Even in a family not yet split into children, put an explicit anchor `<a id="<slug>"></a>` on each item.
Then, when splitting, rewriting references is just changing the path from `./issues.md#timer-leak` to `./issues/timer-leak.md`.
Even in review result documents, where rewriting is forbidden, this can be treated as repairing a broken link.

Sequential numbers confined to one document are outside this rule.
`R-1` for findings in a review result document and `S-1` for steps in an implementation plan may stay numbers, because those documents are not split.

## Granularity of the Responsibilities Table

Only documents read on their own hold the division of responsibilities between documents in §1.1.
These are the six parents and `design/*.md`, `plans/*.md`, and `reviews/*.md`.
They may be handed over without going through the parent's list, and need to show by themselves what they are and are not the authoritative source for.

`terms/*.md`, `issues/*.md`, and `knowledge/*.md` do not have §1.1.
They are always entered from the parent's list, so one line at the top with a relative link to the parent is enough.
This avoids copying the responsibilities table every time a single bug is written.

The map has two tiers.
The upper tier is held by §1.1 of `docs/design.md`, which lists what is the authoritative source in which document, covering the six parents, the `docs/design/*.md` children, API definition files, and `README.md`.
The lower tier is held by each parent.
`terms.md` holds the list of all terms; `issues.md`, `knowledge.md`, `plans.md`, and `reviews.md` hold the list of children.

Do not fold the lower tier into the upper tier.
If the top of `docs/design.md` changed every time a bug was filed, design diffs and document-management diffs would mix.

In §1.1 of documents other than `docs/design.md`, write only what this document holds, what it does not, and where the authoritative source is delegated, and show the family map with a link to `docs/design.md`.
This keeps the place to fix when documents increase to one.
Even after 30 entries accumulate in `reviews/`, adding one more document leaves only one place to go stale.

## Document Names

Name documents under `docs/` in lowercase kebab-case.
Documents with established external conventions, such as `README.md`, `LICENSE`, and `CONTRIBUTING.md`, are exceptions and stay uppercase.

## Information Density

When creating and updating, gather the required semantic elements first, then compress.
Do not try to write short from the start; produce a complete intermediate draft, then drop duplication and low-information text.
Do not leave the intermediate draft in the deliverable.

Each reference defines the semantic elements that must survive compression.

The following may be deleted or merged.

- Duplicates of the same fact
- Sentences that merely restate a heading, table, or diagram
- Copies of details that can be obtained mechanically from code or another authoritative source
- Preambles and closings that do not change the interpretation
- Duplicate examples that merely rephrase a rule

Keep references to authoritative sources, design implications that cannot be read from diagrams or tables, and boundary cases that prevent misreading a rule.
When delegating to an authoritative source, keep the relative link and what can be learned at the destination.

Write reasons and causal relationships in prose.
Use tables or bullet lists only where the same form repeats.
Do not shorten by abbreviations, telegraphic style, or strings of nouns.

Do not compress fixed section structures and required items.
Do not leave empty optional headings or boilerplate without content.
As a rule, keep existing headings and anchors.
When merging headings is clearly worthwhile, check and update every reference in the repository.

When asked only to compress, do not correct mismatches with the code or missing information in the same change.
Report mismatches and gaps as findings, separately from the compression diff.

Set no fixed reduction rate.
Stop when nothing more can be safely removed.
Measure the character and line counts right before and after compression, and report the reduction.
Only when a tokenizer suitable for the target model is available, also give the token counts.
The character count after compression must not exceed the count right before compression.

This character-count constraint applies only when compression is explicitly requested.
When an update adds a change in premises, the character count normally grows.

## Distinguishing the Source of Evidence

Write in three categories.

**Facts confirmed in the code** are stated as assertions.

**Intent read from the code** states its source.
Leave the fact that it is a guess in the sentence, as in "this reads as the intent (there is no stated reason in the code)".
Useful inferences need not be discarded, but they must not be written as facts.

**Things not confirmed** are not written in the body of permanent documents.
Move them to the deferred items in the design decisions section, or to `issues.md`.
Writing unverified behavior in the present tense makes the document lie.

There are two exceptions.

Review result documents may write them with the confidence stated, because recording suspicions is itself their role ([Review Document](references/review-document.md)).

External knowledge may write facts based on primary sources with a source label ([Knowledge Document](references/knowledge-document.md)).
Something not confirmed yourself is different from a groundless guess.
Writing it without a label takes it outside this exception.

## Verification Subagent

When creating and updating, confirm before editing that the named `verifier` is available.
If it is not, do not substitute another agent or the main agent alone; report without changing the documents.
Each reference defines the scope in which the `verifier` is required.
A check that does not change the body does not require the `verifier`.

After editing and any required mechanical checks, ask the strict read-only `verifier` for independent verification.
Have the `verifier` read `../sanitize-artifacts/SKILL.md` as well, and also `../japanese-tech-writing/SKILL.md` when the documents are in Japanese.
For verification, give it the target documents, the diff, the semantic elements to preserve, the direct authoritative sources, and the results of the mechanical checks.
If further evidence is needed, have the `verifier` check it itself.

When compressing an existing document, have it compare before and after.
When creating a new one, have it compare the semantic elements extracted from the code and authoritative sources with the finished document.
The verdict is `pass` or `changes-required`.

The following findings are blocking in common, and each reference adds its own.

- Missing or altered semantic elements
- Inconsistencies in facts or responsibility boundaries
- Missing causal relationships or premises needed to understand the text
- Broken headings, anchors, or links
- Missing required structure or required verification
- Identifying items by sequential numbers
- Items of the same family split between parent and child
- An increase in character count after compression, when compression was requested
- Style findings based on `japanese-tech-writing` (for Japanese) or `sanitize-artifacts`

On `changes-required`, the main agent fixes and verifies again.
Fixing and re-verifying is limited to two rounds; if it still does not pass, report the remaining findings and the unverified scope.
Even after `pass`, the main agent checks the diff and reruns the required mechanical checks.

## Notation Specific to Design Documents

When writing in Japanese:

- Put a half-width space before and after half-width alphanumerics (「Rust 製の daemon」)
- Also put a half-width space between a number and its unit (`32 MiB`, `30 分`, `1024 件`)

In any language:

- Write references to sections in the form `§7.3`. A bare number cannot be told apart as a section number or a value

Limit bold to the following three uses.

1. Labels of definition blocks (`**Decision**`, `**Severity: High**`, `**Source: Verified**`)
2. The first definition of a term in the body
3. Only one per section: a premise that leads to a wrong design if overlooked (`**This design has a premise that must hold.**`)

Do not scatter bold for emphasis.
With four or more bold items in one section, none of them stands out anymore.

## Diagrams

Fix the diagram type by purpose.

| Purpose | Notation |
| --- | --- |
| Dependencies, processing flow | mermaid `flowchart` / `graph` |
| Order of interactions between components | mermaid `sequenceDiagram` |
| State transitions | mermaid `stateDiagram-v2` |
| Stacked layers, directory trees | ASCII in a code block |

Do not draw layers and trees in mermaid.
ASCII is easier to read and does not break when lines are added.

**Right before or after a diagram, add one sentence with a design implication that cannot be read from the diagram.**
For example: "Dependencies point in one direction. Only this one edge is a sideways dependency." or "web is served from the same process and the same port as the daemon. This premise is what makes the CSRF countermeasure in §9.5 work."
A diagram without this sentence is decoration and may be removed.

## References and Links

How to refer to code is determined by the document's lifetime.

| Document | References to code | Reason |
| --- | --- | --- |
| `design.md`, `design/*.md`, `terms.md`, `terms/*.md` | By file or directory. Do not write line numbers (`#L42`) | It does not pay for a document about semantics to go stale through line numbers. Point to locations by type or function names |
| `issues.md`, `issues/*.md`, `knowledge.md`, `knowledge/*.md`, `plans.md`, `plans/*.md`, `reviews.md`, `reviews/*.md` | Links with line numbers are required | These are snapshots that state the investigation date, verification date, and target commit, and are expected to go stale |

When a document refers to itself, write only `this document` (`本書` in Japanese).
Do not add the file name or a self-link.
Write all links between documents as relative paths.
From parent to child it is `./issues/timer-leak.md`, from child to parent `../issues.md`, and from child to the repository root `../../README.md`.

When pointing to design documents and terms documents, include the heading anchor.
For example, write `[design.md](./design.md#3-overall-structure)`, `[storage.md](./design/storage.md#2-responsibilities-and-boundaries)`, and `[terms.md](./terms.md#t-session)`.

In the responsibilities table, leave only `this document` unlinked, and make every other document name a relative Markdown link to the actual file.

## Common Post-Writing Check

In addition to each reference's check, confirm the following.
Check items that can be automated with commands.

1. Has the check with `sanitize-artifacts`, and with `japanese-tech-writing` for Japanese documents, been completed?
2. Do section references carry `§`?
3. Does each document refer to itself as `this document` (`本書` in Japanese)? Is the file name or a self-link not added alongside?
4. Are the responsibilities table and links between documents relative links to actual files, and do the link targets exist?
5. Do permanent documents have no links with line numbers, and do references to code in snapshot documents have line numbers?
6. Are guesses not written as assertions? Wherever a reason is given, can you say where in the code its basis is?
7. Are there no remaining duplicates of the same fact, restatements of headings, diagrams, or tables, copies of authoritative sources, or boilerplate without content?
8. Does every diagram have a sentence of implication right before or after it?
9. Have term definitions not leaked outside the terms documents?
10. Does the term list in `terms.md` contain every term, and do only terms with an entry point to the anchor in the parent or child matching their scope?
11. Do the rows of the parent lists in `issues.md`, `knowledge.md`, `plans.md`, and `reviews.md` correspond one-to-one with the child files? Is there no item that exists in only one of them?
12. Are items of the same family not split between parent and child? In families that hold a list of children, are there no items still holding their body in the parent despite having children?
13. Are item identifiers `<slug>`, not sequential numbers? `rg -n '^#+ [A-Z]-[0-9]+\.' docs/` must pick up only findings in `reviews/` and steps in `plans/`
14. Does §1.1 of `docs/design.md` list the parents and `design/*.md`, and not list the children of other families?
15. Where the `verifier` is required, did it give `pass`, and did the main agent then recheck the diff and the required checks?
