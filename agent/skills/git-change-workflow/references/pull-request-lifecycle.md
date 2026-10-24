# PR Lifecycle

## Creating a Draft

Do not work on the default branch, and create PRs as drafts.

```bash
gh pr create --draft --title '...' --body-file pr-body.md
```

After creating the draft, self-review it by going through the diff.
If line comments are needed, read `github-review-comments.md` and get the user's approval before posting.

## Monitoring CI

Right after a push, checks may not be registered yet, so wait for registration before monitoring.

```bash
until ! gh pr checks <number> 2>&1 | grep -q 'no checks reported'; do sleep 10; done
gh pr checks <number> --watch --interval 30
```

In an environment that cannot wait in the foreground, replace this with a monitoring facility that has the same registration and termination conditions.
On failure, check the job URL and the failure log, and report them.

## Marking Ready

Mark a PR ready only on the user's explicit instruction.
Before marking it ready, confirm the following.

1. The description meets the requirements in `pull-request-description.md`
2. If there are numerical claims, they meet the measurement and verification requirements in `measured-claims.md`
3. CI has passed
4. The `verifier` has given `pass` on the independent verification of the artifacts, the self-review is complete, and the necessary line comments have been posted after approval
5. If the dependency has been merged, the base has been changed back to the default branch
6. Out-of-scope problems have been recorded

If any item is not met, do not mark it ready; report the remaining items.
