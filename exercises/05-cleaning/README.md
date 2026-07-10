# Exercise 05 — Measure before repairing

## Frame

Data cleaning is a set of analytical policies. First make the failures visible.

## Predict

For the small fixture in the tests, predict every reported count before running
pytest.

## Build

Implement `quality_report`. Return integer counts for:

- `rows`;
- `duplicate_customer_ids` (all rows belonging to a duplicated ID);
- `missing_satisfaction`;
- `invalid_tenure` (missing or outside 1–48);
- `invalid_renewed` (missing or not zero/one).

Require the four columns used by the report. Do not modify or silently repair
the input.

## Check

Add a fixture in which one customer ID appears three times and another appears
once. Confirm that `duplicate_customer_ids` is `3`: count **all rows implicated
in a duplicate ID**, including the first occurrence. This is the behavior of
`customers["customer_id"].duplicated(keep=False).sum()`; do not count only
occurrences after the first or only the number of distinct duplicated IDs.

## Explain

Which failures could be repaired mechanically, and which require a conversation
with the data owner?
