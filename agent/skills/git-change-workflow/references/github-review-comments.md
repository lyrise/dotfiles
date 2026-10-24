# GitHub Review Comments

## Writing Review Findings

Write only one problem per finding.
Make the title a short sentence that shows the symptom or the contract being broken; do not restate what the code does.

Write line comments in the following fixed format.

```markdown
**Short title that shows the symptom**

**Problem**
[What this code gets wrong.]

**Evidence**
[Why this can be said, from the code, the specification, or test results. Distinguish what was not verified.]

**Impact**
[Which inputs, users, contracts, or operations break, and how.]

**Required fix**
[The state that must hold. If the implementation need not be pinned down, write only the outcome.]
```

When writing in Japanese, use these labels.

| English | Japanese |
| --- | --- |
| `**Problem**` | `**問題**` |
| `**Evidence**` | `**根拠**` |
| `**Impact**` | `**影響**` |
| `**Required fix**` | `**必要な修正**` |

Do not mix the problem, evidence, and impact, and keep the required fix within what can be derived from the finding.
Do not write out the entire fixed code, and when there are several implementation options, do not force a particular one.

## Placing Comments

Attach the comment to the smallest line or line range among the changed lines that shows the problem.
Right before posting, recount the line numbers against the latest content of the file.
Restacking commits shifts lines, and the comment lands on a neighboring or unrelated line.
Use a range comment only when the problem cannot be shown without several lines together.
For a problem that cannot be attached to a changed line, or one that spans several files, do not attach a line comment to an unrelated line; write it in the overall PR review with links that include line numbers.
Collect multiple locations arising from the same cause at a representative location, and do not repeat the same explanation.

## Annotations by the Author

In the self-review of a draft, consider adding line comments as the author at locations that:

- Do not explain their reason on their own
- Look unnecessary at first glance
- Deliberately depart from the existing style

An annotation is not a review finding, so do not use the fixed format; briefly write only why that implementation was chosen.
An explanation with the same lifetime as an in-code comment belongs in the code, not only on GitHub.
Conversely, library specifications and the results of trying implementations that were not adopted go here, not in the code.

When citing an implementation that was not adopted as evidence, actually apply that implementation, reproduce the failure, and write the observed result.
If it was not reproduced, state explicitly that it is a guess.

## Posting

Present all comment drafts to the user together before posting.
After approval, post multiple comments in a single review API call.
If posting was not requested, stop at drafting the comments.
