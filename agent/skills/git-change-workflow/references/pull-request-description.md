# PR Description

Put the evidence where it is needed for the decision, so that the PR description alone is enough to reconstruct the decision and verification of the change.

## Where Evidence Goes

| Location | What to write |
| --- | --- |
| In-code comments | Implementation intent with the same lifetime as the code. Do not put library specifications or explanations of implementations not adopted here |
| PR line comments | Evidence that is meaningful only for that PR and line |
| PR description | Background, the structure of and decisions behind the change, impact, verification, review points |
| Commit messages | Why that commit goes in, in that order |

Do not write the same evidence in more than one place.

## Sections

Always include `Background`, `Summary`, and `Verification`.
Omit `Changes`, `Impact`, `Review Points`, and `Related` entirely when there is nothing to write.
When included, use the following order and do not rearrange it.

```markdown
## Background

[Write the necessary history, the purpose, non-goals, and open items.]

## Summary

[Write the adopted approach in one to three sentences.]

## Changes

[Write, per concern, only the decisions that cannot be read from the diff. Use h3 if needed.]

## Impact

[Write the affected users, contracts, and operations.]

## Verification

- [x] `[command that was run]`
- [x] [check that cannot be expressed by pass/fail alone]: see below
- [ ] Not verified: [target and reason, or remaining work]

### [Check name]

<details>
<summary>Details</summary>

[Table of conditions, steps, and results]

</details>

## Review Points

- [Location to check and the decision involved]

## Related

- [Dependent PR or Issue, and its relationship to this PR]
```

When writing in Japanese, use these headings.

| English | Japanese |
| --- | --- |
| `## Background` | `## 背景` |
| `## Summary` | `## 概要` |
| `## Changes` | `## 変更内容` |
| `## Impact` | `## 影響範囲` |
| `## Verification` | `## 検証` |
| `## Review Points` | `## レビュー観点` |
| `## Related` | `## 関連` |
| `Not verified` | `未検証` |
| `<summary>Details</summary>` | `<summary>詳細</summary>` |

## Writing Each Section

- `Background`: make the need understandable without opening links, and also write non-goals and open items when they are needed for the decision.
- `Summary`: do not repeat the background; write only the adopted approach in one to three sentences.
- `Changes`: do not write what the diff makes obvious; write, per concern, only the decisions that cannot be read from the diff. Write important rejected alternatives with their reasons, and use h3 only when several concerns need to be separated. Do not make it a file list. Put evidence that a line comment covers there, and omit the section entirely if nothing remains.
  - When contrasting before and after, list only the conclusions, one per line. Do not write the internals of type declarations or intermediate steps of a derivation.
  - Do not write inferences the reader can fill in by comparing the two items side by side; write only the conclusion drawn from them.
  - Write a rejected alternative in one sentence: what was not adopted and why. Move the steps used to check it and the details to `Verification`, or drop them.
- `Impact`: write the impact on users, backward compatibility, APIs, settings, storage formats, CLI arguments, and operations. Even when there is no impact, write the scope checked and the basis. Do not write peripheral facts that merely came up during investigation unless they change the merge decision.
- `Verification`: for what was done, write `- [x]` with the command or reproduction steps and the result; for what was not verified, write `- [ ]` with the target and the reason or remaining work. Put automated tests, manual checks, and measurement results in this section, and make manual checks reproducible steps. Do not vouch for what was not checked.
  - For a check that can be expressed by pass/fail alone, stop at `- [x]` and the command; do not expand a breakdown of what was checked into the body.
  - Put a check that involves a table or long output in an h3 section referenced from the checklist, collapsed with `<details><summary>Details</summary>`. This keeps the checklist scannable while preserving the evidence.
  - Do not mix strengths of verification within one table. Do not put values actually read and facts whose occurrence was merely confirmed in the same column. Recheck rows whose strength does not match before writing them, or drop them.
  - When the behavior before the change is cited as evidence, confirm it by actually running the commit before the change, not from the specification or memory, and put before and after in the same table.
- `Review Points`: make the location and the decision concrete, and write only the points where you actually want a judgment. Do not write checks with obvious answers or routine validity checks. Limit it to three; with four or more, reconsider splitting the PR. If there is nothing to ask, omit the section entirely.
- `Related`: write the number or URL of PRs this depends on, PRs that depend on this, and Issues, with the direction of the dependency or the reason they are related. If none apply, do not include the heading.

When citing external documentation as evidence, attach a URL that goes directly to the relevant part and a short quote if needed.
When citing a CI failure as evidence, attach the job URL and the log that shows the failure.
State guesses as guesses, and write why they were not confirmed.
When you filled in a decision not covered by the instructions or the specification, state the location and the basis explicitly.

## Formatting

- Break the line after each sentence. Mark paragraph breaks with a blank line.
- Insert a blank line where the stage of the argument changes. Do not write the premise, the contrast of facts, and the conclusion as one continuous block.
- For a side note off the main thread, add one line starting with `※` instead of adding a paragraph.
- Refer to PRs and Issues by number only. Do not add a paraphrase of content reachable from the number.
- When supplementing one bullet item with several sentences, use nested `- ` child bullets, not continuation lines that are only indented.

## Do Not Write

Keep only what the reader uses for the decision and reproduction, not what you investigated.

- A per-file list transcribing the diff
- Pasted code that can be read in the GitHub diff
- Explanations of changes that are obvious from the diff
- Intermediate inferences the reader can fill in from the facts presented
- The steps used to check rejected alternatives, or details found there
- Peripheral facts that merely came up during investigation and do not change the merge decision
- Review points that list checks with obvious answers
- Performance or resource usage claims that do not meet the measurement conditions
- Checkboxes that do not show what was run
- Checkboxes that spell out in the body the breakdown of checks that passed
- Comparison tables whose rows do not share the same strength of verification
- Thanks, self-justification, or history not needed for the review decision
