# Practice 02 — Trace values before adding syntax

This is an on-site exercise; no repository starter file is required. Return to
[lesson 02](../lessons/02-python-basics.md) for the worked language examples.

## Worked warm-up

Trace this code one line at a time:

```python
monthly_hours = 8
months = 3
total_hours = monthly_hours * months
needs_review = total_hours < 30
```

The names end with values `8`, `3`, `24`, and `True`; their types are `int`,
`int`, `int`, and `bool`. The comparison consumes `24` and `30` and returns a
new Boolean. It does not change `total_hours`.

## Try

### Completion — fill the trace table

Do not run this yet:

```python
customer_id = "C1042"
usage = 7.5
tickets = 2
annual_usage = usage * 12
high_attention = usage < 8 and tickets >= 2
summary = f"{customer_id}: {annual_usage} hours"
```

Fill a table with one row per name: expression, predicted value, and predicted
type. Then run it and add an observed column.

### Transfer — express a policy clearly

Write a policy that flags a record when either:

- usage is below five **and** there is at least one ticket; or
- tenure is below three months.

Use named intermediate Booleans before combining them. Test values that make
only the first condition true, only the second true, neither true, and both
true. Then set `usage = "7.5"` and predict the first failing operation.

## Hint 1

??? tip "Reveal Hint 1"
    Multiplication returns a float when one operand is a float. An f-string
    returns text even when it contains a formatted number.

## Hint 2

??? tip "Reveal Hint 2"
    Try names such as `low_usage_with_ticket` and `new_customer`. Combine them
    with `or`. Parentheses make the intended grouping reviewable.

## Tests or rubric

```python
assert annual_usage == 90.0
assert isinstance(annual_usage, float)
assert high_attention is True
assert summary == "C1042: 90.0 hours"
```

For the transfer policy, check all four truth combinations. Also explain why
`"7.5" < 5` fails instead of silently converting the text.

## Worked reasoning

??? success "Reveal worked reasoning"
    `usage * 12` produces `90.0` because `usage` is a float. Both parts of
    `usage < 8 and tickets >= 2` are true, so the result is `True`. The f-string
    converts values for display but the original numeric names stay numeric.

    A readable transfer version is:

    ```python
    low_usage_with_ticket = usage < 5 and tickets >= 1
    new_customer = tenure_months < 3
    needs_review = low_usage_with_ticket or new_customer
    ```

    Python rejects comparison between text and an integer because the program
    has not stated a conversion policy. Fix the input boundary; do not scatter
    guesses about conversion through the analysis.

Next: [lesson 03](../lessons/03-functions-control.md) or
[practice 03](03-functions-control.md).
