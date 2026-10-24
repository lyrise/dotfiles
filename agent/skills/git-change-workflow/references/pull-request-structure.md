# PR and Commit Structure

Ask for only one decision per PR.
Split by purpose, not by number of files.

## Splitting PRs

Split a change into a separate PR if any of the following applies.

1. Only one part might be sent back
2. The aspects needed for review differ
3. A fix for an existing bug is mixed with a new change

Include several purposes in the same PR only when merging just one of them would break things.
Decide this before implementing and before creating the PR, and if a split is needed, present how to split, the order, and the dependencies and get confirmation before restructuring the history.

Do not fix problems with a different purpose found during the work in the same PR.
If `docs/issues.md` exists, record them according to that document's rules.
If there is nowhere to record them, write why they are not handled and where they were found in the `Background` section of the PR description.

## Structuring Commits

Order commits by dependency, and make each commit build and pass tests on its own.
Put commits that change the verification foundation, such as tests, benchmarks, measurement code, and CI settings, before the changes that use them.
Write the reason for the change in the commit message.
When claiming numbers, also write the measured values for that commit alone.

## Structuring Dependent PRs

Create the PR that others depend on first.
Base a dependent PR on the branch of its dependency, and create it as a draft.

```bash
gh pr create --draft --base feat/dependency --title '...' --body-file pr-body.md
```

When the dependency is merged, change the dependent PR's base back to the default branch.

```bash
gh pr edit <number> --base main
```

Change the base while the PR is still a draft.
If a ready PR needs its base changed, turn it back into a draft first.
In the `Related` section of the PR description, write the direction of the dependency and the reason, and keep it consistent with the actual base.
