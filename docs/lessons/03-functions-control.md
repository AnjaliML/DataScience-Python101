# 03 — Functions, collections, and control flow

Real analyses repeat the same reasoning across many observations. Small functions let you name that reasoning, test it once, and reuse it without copying expressions.

## Frame

Suppose a renewal team marks a customer as low activity when monthly usage is
below five hours.

We could repeat `usage_hours < 5` everywhere. A function gives the rule a name
and a boundary:

```python
def is_low_activity(usage_hours):
    return usage_hours < 5
```

The input crosses into the function, the expression is evaluated, and the result comes out. Given the same valid input, this **pure function** returns the same result and changes nothing outside itself, making it easy to test and reuse.

## Predict

Before running the code, state the returned value and type for each call:

```python
is_low_activity(0)
is_low_activity(3)
is_low_activity(8)
```

## Build

A useful function begins with a contract: accepted inputs, returned output, and important failure behavior.

```python
def nonrenewal_risk_band(usage_hours, support_tickets):
    """Return a non-renewal risk band from usage and ticket counts.

    Raise ValueError for a negative input.
    """
    if usage_hours < 0 or support_tickets < 0:
        raise ValueError("inputs must be non-negative")
    if usage_hours < 3 and support_tickets >= 2:
        return "high"
    if usage_hours < 8 or support_tickets >= 1:
        return "medium"
    return "low"
```

Read the branches from top to bottom. Python returns from the first matching branch and leaves the function. Order matters: the most specific high-risk condition must be checked before the broader medium-risk condition.

Lists store ordered sequences:

```python
usage_hours = [0.5, 14.2, 5.0, 2.8]
first_value = usage_hours[0]
last_value = usage_hours[-1]
first_two = usage_hours[:2]
```

Predict the type and shape-like length of each result. An index selects one element; a slice returns another list.

Dictionaries map keys to values and are convenient for one small record:

```python
customer = {
    "customer_id": "C1042",
    "monthly_usage_hours": 4.2,
    "support_tickets": 1,
}
```

`customer["monthly_usage_hours"]` returns `4.2`; a missing key raises
`KeyError`. If absence is expected, `customer.get("plan", "unknown")` provides
a deliberate default. Never turn a missing measurement into zero unless they
truly mean the same thing.

A list of dictionaries forms a small collection of records:

```python
customers = [
    {"customer_id": "C1042", "monthly_usage_hours": 4.2, "support_tickets": 1},
    {"customer_id": "C1043", "monthly_usage_hours": 18.0, "support_tickets": 0},
    {"customer_id": "C1044", "monthly_usage_hours": 1.5, "support_tickets": 3},
]
```

A `for` loop applies the same block to each item:

```python
bands = []

for customer in customers:
    band = nonrenewal_risk_band(
        customer["monthly_usage_hours"], customer["support_tickets"]
    )
    bands.append(band)
```

Before running, trace all three iterations. State the value appended each time and the final length of `bands`.

A comprehension can express a simple transform or filter:

```python
low_activity_ids = [
    customer["customer_id"]
    for customer in customers
    if is_low_activity(customer["monthly_usage_hours"])
]
```

Use comprehensions when the transformation remains easy to read. Use a loop when you need several steps, checks, or explanatory names.

Functions can operate on a collection while delegating one-record logic:

```python
def count_low_activity(records):
    """Return the number of records with fewer than five usage hours."""
    return sum(
        is_low_activity(record["monthly_usage_hours"])
        for record in records
    )
```

The local name `count` belongs to each function call. The function reads `records` but does not modify the list or its dictionaries.

## Check

Tests are examples with expected behavior made executable. Predict each outcome before running:

```python
assert is_low_activity(0) is True
assert is_low_activity(5) is False
assert nonrenewal_risk_band(0, 2) == "high"
assert nonrenewal_risk_band(7.9, 0) == "medium"
assert nonrenewal_risk_band(8, 0) == "low"
assert count_low_activity(customers) == 2
assert count_low_activity([]) == 0
```

Test boundaries, not just comfortable examples. For “below five,” values
`4.9` and `5.0` reveal whether the inequality is correct.

Test the stated failure behavior too:

```python
try:
    nonrenewal_risk_band(-1, 0)
except ValueError as error:
    assert str(error) == "inputs must be non-negative"
else:
    raise AssertionError("negative counts should fail")
```

```python
before = customers.copy()
count_low_activity(customers)
assert customers == before
```

## Explain

Control flow determines which statements run: `if` chooses a path, `for` visits items, `return` ends a call with a value, and `raise` ends it with an explicit failure.

Collections and control flow solve different parts of the mechanism. A list holds many items; a loop visits them; a function defines what happens to one item or collection.

Keep functions small enough that their contracts fit in your head. Prefer returning a result over printing it: callers can test, combine, store, or print a returned value, while printed text is harder to reuse.

## Practice

Write a pure function `is_valid_record(record)` that returns `True` only when
`customer_id` is a non-empty string, `monthly_usage_hours` is a non-negative
number, and `support_tickets` is a non-negative integer.

State its contract first. Decide whether missing keys should return `False` or raise an error, and document that choice.

Test one valid record and every failure boundary. Use a loop to collect valid records, rewrite that simple filter as a comprehension, and confirm the original list is unchanged. Predict all output types and lengths first.

Finally, extend `nonrenewal_risk_band` with one new rule. Add a boundary test that would fail if your branch order were wrong.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → tests → worked reasoning](../practice/03-functions-control.md).
The completion task uses the repository starter; transfer work goes in a new file.

## Keep going

You now have a repeatable pattern: define a contract, predict behavior, implement a small function, and challenge it with tests.

Before moving on, explain why branch order changes results, when a loop beats a comprehension, what a function reads or changes, how indexing differs from slicing, why missing is not automatically zero, and which boundary examples test the rule's meaning.

Next, NumPy will apply these ideas to whole rectangular arrays while making shape and data type explicit.
