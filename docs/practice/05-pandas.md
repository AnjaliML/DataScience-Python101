# Practice 05 — Preserve row meaning through table operations

This journey pairs with [lesson 05](../lessons/05-pandas.md) and
`exercises/04-dataframes/`.

## Worked warm-up

Before grouping, the unit is one customer record. After grouping by plan, the
unit is one plan. A trustworthy summary names both quantity and unit:

```python
plan_summary = customers.groupby("plan", as_index=False).agg(
    customers=("customer_id", "nunique"),
    renewal_rate=("renewed", "mean"),
)
```

## Try

### Completion — implement `summarise_plans`

In `exercises/04-dataframes/starter.py`, implement the documented plan summary.
Require `customer_id`, `plan`, and `renewed`; reject missing IDs/plans,
non-binary or missing outcomes, and duplicate customer IDs. Return exactly
`plan`, `customers`, and `renewal_rate`, alphabetically sorted with a fresh
index, without changing the input.

### Transfer — change grouping and merge in `scratch.py`

In `scratch.py`, build a signup-channel summary with unique-customer count,
median usage, and renewal rate. Then create a one-row-per-plan lookup with a
readable plan label and merge it onto customers. Declare the relationship,
keep an indicator while checking, and prove every source row has one match.

Deliberately duplicate a lookup key. Explain why multiplying customer rows
would corrupt later rates even though pandas returns a table.

## Hint 1

??? tip "Reveal Hint 1"
    Completion needs named aggregation and `customer_id: nunique` after first
    rejecting duplicate IDs. `as_index=False` keeps plan as a column.

## Hint 2

??? tip "Reveal Hint 2"
    For transfer's many customer rows and one lookup row per plan, use
    `validate="many_to_one"`; reconcile row counts before dropping `_merge`.

## Tests or rubric

The supplied tests validate the **Completion** task:

```bash
uv run pytest exercises/04-dataframes/test_starter.py -q
```

For transfer, check one row per observed channel, counts that reconcile to
unique customers, an enriched row count equal to the source, and `_merge`
always equal to `"both"`.

## Worked reasoning

??? success "Reveal worked reasoning"
    Completion rejects duplicated customer IDs because its contract promises
    one row per customer. It then counts unique IDs explicitly and keeps the
    denominator beside each rate. Alphabetical sorting plus a reset index makes
    output stable and testable.

    In transfer, a many-to-one merge protects the original grain. A duplicated
    lookup key would produce two rows for affected customers, changing both
    denominators and apparent evidence without an obvious syntax error.

Next: [lesson 06](../lessons/06-cleaning.md) or [practice 06](06-cleaning.md).
