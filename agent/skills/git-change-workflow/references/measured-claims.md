# Measured Claims

When claiming numbers such as performance, resource usage, or size, put the results in the `Verification` section of the PR description.

## Measuring

Satisfy all of the following.

- Confirm that the measuring tool measures the target correctly, for example with known inputs
- Measure before and after the change on the same machine, under the same load, with the same data, order, and timing
- Present the comparison as a table by condition, showing the target commits, the number of trials, and the median and variance
- Write executable commands that reproduce the results from the steps in the description
- When accepting the PR depends on the numbers, confirm the same trend with two independent methods
- Make the numbers in the PR description and the commit messages match

## Verifying

Have the `verifier` independently verify, given the diff, the PR description, the measurement results, and the reproduction steps.
If the `verifier` is unavailable and independent verification cannot be done, do not finalize the numerical claims.

The following findings are blocking.

- Any of the comparison conditions, target commits, number of trials, variance, or reproduction commands is missing
- The validity of the measuring tool was not confirmed
- The measurement conditions or timing differ between before and after the change
- Acceptance depends on the numbers but there is no independent corroboration
- The numbers in the PR description and the commit messages differ
