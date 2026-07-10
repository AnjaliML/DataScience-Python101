# Practice 06 — Make cleaning a reviewable policy

This journey pairs with [lesson 06](../lessons/06-cleaning.md) and
`exercises/05-cleaning/`.

## Worked warm-up

A quality report measures evidence before repairing it. If one customer ID
appears twice, `duplicated(keep=False)` counts both implicated rows; ordinary
`duplicated()` counts only repeats after the first. The chosen definition must
match the report's documented meaning.

## Try

### Completion — implement `quality_report`

In `exercises/05-cleaning/starter.py`, implement the five documented integer
counts:

- `rows`;
- `duplicate_customer_ids` (all rows implicated in repeated IDs);
- `missing_satisfaction`;
- `invalid_tenure` (missing or outside 1–48);
- `invalid_renewed` (missing or not zero/one).

Require the four used columns, return a dictionary, and do not repair or modify
the input.

### Transfer — defend missingness decisions in `scratch.py`

In `scratch.py`, propose separate policies for missing usage, satisfaction,
and renewal. For each, state whether to reject, exclude for one analysis,
impute, or retain an indicator. Measure the affected row count and name one way
the policy could bias the result. Do not modify the raw CSV.

## Hint 1

??? tip "Reveal Hint 1"
    Completion can construct one Boolean mask per failure and convert each sum
    to `int`. Validate required columns before indexing them.

## Hint 2

??? tip "Reveal Hint 2"
    For transfer, coercion is not a full policy. Compare missingness before and
    after parsing so newly failed conversions cannot disappear into `NaN`.

## Tests or rubric

The supplied tests validate the **Completion** task. The duplicate definition
is fixed: count **all rows implicated** in repeated IDs, equivalent to
`duplicated(keep=False)`, not only repeats after the first.

```bash
uv run pytest exercises/05-cleaning/test_starter.py -q
```

Add a completion case where one ID appears three times. For transfer, require
unchanged raw bytes, recorded affected counts, named allowed missingness, and a
new output path for any cleaned table.

## Worked reasoning

??? success "Reveal worked reasoning"
    `duplicated(keep=False)` exposes every row whose identity is ambiguous.
    Invalid tenure combines missing and out-of-range values because both fail
    this report's declared contract. The function measures failures without
    pretending to know their repair.

    A defensible transfer policy might reject missing renewal, retain missing
    satisfaction plus an indicator, and exclude missing usage only from tasks
    requiring usage while reporting the count. Imputation needs a separate
    justification because it turns unobserved values into modelled ones.

Next: [lesson 07](../lessons/07-visualization.md) or
[practice 07](07-visualization.md).
