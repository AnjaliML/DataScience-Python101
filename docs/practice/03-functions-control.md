# Practice 03 — Build a function from its contract

This journey pairs with [lesson 03](../lessons/03-functions-control.md) and the
repository starter in `exercises/02-functions/`.

## Worked warm-up

For `[1, 0, 1, 1]`, the renewal rate is `3 / 4 = 0.75`. The numerator
counts outcomes equal to one and the denominator is the number of observed
binary outcomes. An empty list has no denominator, so returning `0.0` would
quietly invent a measured zero rate.

## Try

### Completion — implement `renewal_rate`

In `exercises/02-functions/starter.py`, implement the documented function. It
must accept a list containing only integer zeros and ones, return their mean as
a float, reject an empty list, reject Booleans and other values, and leave the
input unchanged. Predict `[1, 0, 1, 1]`, `[]`, `[0, 2]`, and `[1, True]` first.

The input container must be a list. Tuples and other sequence types are outside
the supplied contract and must raise `ValueError`; add an explicit type check
instead of accepting them accidentally.

### Transfer — validate a record in `scratch.py`

Write a new pure function `is_valid_record(record)` in `scratch.py`. It returns
`True` only when `customer_id` is a non-empty string, usage is a non-negative
number but not a Boolean, and tickets is a non-negative integer but not a
Boolean. Choose and document what happens when a key is missing.

## Hint 1

??? tip "Reveal Hint 1"
    Validate the whole input before calculating. `type(value) is int` is one
    direct way to accept integer zeros and ones while rejecting Booleans and
    floats.

## Hint 2

??? tip "Reveal Hint 2"
    For the transfer, `isinstance(value, int)` is insufficient on its own
    because `True` behaves like `1`. Check `not isinstance(value, bool)`.

## Tests or rubric

The supplied tests validate the **Completion** task:

```bash
uv run pytest exercises/02-functions/test_starter.py -q
```

For the transfer, add examples for an empty ID, missing key, negative usage,
fractional tickets, Boolean usage, and Boolean tickets. Confirm that the input
dictionary is unchanged after every call.

For Completion, add `renewal_rate((1, 0, 1))` as a tuple-rejection test as well
as the supplied invalid-value cases.

## Worked reasoning

??? success "Reveal worked reasoning"
    `sum(outcomes) / len(outcomes)` is correct only after validation. Rejecting
    an empty list distinguishes “no observations” from an observed zero rate.
    Rejecting `True`, `0.0`, and `2` keeps the promised binary-integer contract
    instead of relying on Python's convenient coercions.

    The transfer has three independent field claims, so small guard clauses are
    easier to diagnose than one dense expression. Returning `False` suits a
    filter; raising a field-named error may be safer at an ingestion boundary.

Next: [lesson 04](../lessons/04-numpy.md) or [practice 04](04-numpy.md).
