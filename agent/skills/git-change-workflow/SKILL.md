---
name: git-change-workflow
description: Rules for submitting changes through commits, pushes, PRs, and reviews. Use when deciding how to structure commits or write their messages, pushing changes, handling a PR's structure, description, or lifecycle, or writing or posting review findings.
---

# Submitting and Reviewing Changes with Git

Read only the references the request needs, and combine the relevant references when doing several tasks.
The artifact's own structure, evidence, and constraints, and the repository's conventions, take precedence over style preferences.
Build the Japanese parts of PR descriptions, review comments, titles, and commit messages in natural technical Japanese from the first draft.
Before finishing, remove redundancy, unnatural phrasing, and leftovers of the production process from every artifact without changing the meaning.

## Choosing a Reference

| Request | Reference to read |
| --- | --- |
| Decide how to structure commits or write their messages; commit and push without creating a PR | "Structuring Commits" in [PR and Commit Structure](references/pull-request-structure.md) |
| Write or post review findings or line comments | [GitHub Review Comments](references/github-review-comments.md) |
| Decide PR granularity, commit order, or dependencies | [PR and Commit Structure](references/pull-request-structure.md) |
| Write or check a PR description | [PR Description](references/pull-request-description.md) |
| Create, monitor, or mark a PR ready | [PR and Commit Structure](references/pull-request-structure.md), [PR Description](references/pull-request-description.md), [PR Lifecycle](references/pull-request-lifecycle.md) |
| Claim numbers such as performance or resource usage | The above plus [Measured Claims](references/measured-claims.md) |

If the self-review after creating the draft calls for line comments, also read [GitHub Review Comments](references/github-review-comments.md).

## Committing and Pushing

Create a PR only when the request includes it.
Before committing, check the diff and what is staged, and include only the changes the request needs.
Before pushing, check the destination remote and branch and the commits to be sent.

## Verifying the Text

Before returning an artifact as final, committing it, or posting it, have the named strict read-only `verifier` independently verify, all together, the PR description, title, commit messages, and line comments handled in the same operation.
Intermediate drafts and options are out of scope.

Give the `verifier` the final drafts, the diff and facts they rest on, the repository's conventions, the relevant references, and, when numbers are claimed, the measurement results and reproduction steps.
It checks the artifact's structure, logic, placement of evidence, duplication, consistency of facts and numbers, and leftovers of the production process.
English is judged against the repository's conventions and natural technical English, and Japanese against the Japanese headings given in each reference. Style findings in English and findings about leftovers of the production process are blocking; Japanese style findings are not.
The verdict is `pass` or `changes-required`.
With `changes-required`, it points to the location in the artifact, the evidence, and the required fix.

On `changes-required`, fix and verify again.
Fixing and re-verifying is limited to two rounds; if it still does not pass, report the unresolved findings and do not finalize, commit, or post the artifacts.
If the `verifier` is unavailable, also do not finalize, commit, or post the artifacts.
After `pass`, the main agent rechecks the artifacts that will actually be used.

## Common Checks

Read the recent commits and match the language of commit messages to the repository's conventions.

```bash
git log --oneline -20
```

When handling PRs or reviews, also read merged PRs.

```bash
gh pr list --state merged --limit 10
```

Match the language of PR descriptions and line comments to the merged PRs as well.
If the convention cannot be determined, write titles, commit messages, PR descriptions, and line comments in English.
Do not mix languages within one PR description.
When writing in Japanese, use the Japanese headings given in each reference.
