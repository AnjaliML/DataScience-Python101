# 02 — Values, names, and readable expressions

Python lets us turn assumptions into expressions a computer can evaluate. The goal is not to memorize punctuation; it is to know what value an expression should produce, what type that value should have, and why.

## Frame

Suppose one customer-renewal record contains:

```python
customer_id = "C1042"
plan = "plus"
tenure_months = 18
monthly_usage_hours = 24.5
support_tickets = 1
satisfaction_score = None
renewed = 0
has_open_case = False
```

Each line binds a **name** to a **value**. A name gives a useful label to a value so later expressions can describe business rules.

The values use `str` for text, `int` for whole numbers, `float` for fractional numeric values, `bool` for `True` or `False`, and `NoneType` when no value is present here. The raw `renewed` target uses integer `0` or `1`; `has_open_case` is the separate Boolean example.

Types determine which operations make sense. Adding two fees is meaningful. Adding a fee to a customer ID is not.

## Predict

Without running Python, write the value and type produced by each expression:

```python
tenure_months + 6
monthly_usage_hours * 12
monthly_usage_hours / 30
customer_id.lower()
plan == "plus" and monthly_usage_hours > 0
satisfaction_score is None
```

Be precise: `/` produces a `float`, even when the division is exact. A comparison produces a `bool`.

Now predict which line fails and why:

```python
label = customer_id + " renewal record"
bad_total = customer_id + monthly_usage_hours
```

An error is useful evidence that the expression and the values do not agree.

## Build

Use `type` to test your type predictions:

```python
print(type(customer_id))
print(type(tenure_months))
print(type(monthly_usage_hours))
print(type(renewed))
print(type(has_open_case))
print(type(satisfaction_score))
```

Names should reveal meaning and units: `window_days = 30` is more useful than `x = 30`. Prefer `snake_case`, avoid overwriting built-ins such as `list`, and include units where confusion is possible.

Arithmetic operators build numeric expressions:

```python
annualized_usage_hours = monthly_usage_hours * 12
average_daily_usage_hours = monthly_usage_hours / 30
```

Use parentheses to show grouping and intermediate names instead of hiding assumptions in one long expression:

```python
expected_growth_rate = 0.10
expected_added_hours = monthly_usage_hours * expected_growth_rate
forecast_usage_hours = monthly_usage_hours + expected_added_hours
```

Strings hold text. Combine them deliberately:

```python
plan_name = " Plus "
normalized_plan = plan_name.strip().lower()
summary = f"{customer_id}: {normalized_plan} plan, {tenure_months} months"
```

An f-string inserts values without pretending that text and numbers are the same type. `strip()` removes surrounding whitespace; `lower()` returns lowercase text. Strings are immutable: these methods create new strings.

Comparisons answer yes-or-no questions:

```python
is_long_tenure = tenure_months >= 12
has_recent_activity = monthly_usage_hours > 0
tenure_in_expected_range = 1 <= tenure_months <= 48
usage_is_nonnegative = monthly_usage_hours >= 0
```

Combine boolean values with `and`, `or`, and `not`:

```python
eligible_for_predecision_review = (
    has_recent_activity
    and satisfaction_score is None
)
observed_nonrenewal = renewed == 0
```

The parentheses allow one condition per line. The name states what the combined rule means. The observed outcome stays separate from the pre-decision rule so it cannot leak into a decision made before renewal is known.

`None` is not zero, empty text, or `False`; it means absence in this context.
Write `has_satisfaction_score = satisfaction_score is not None`. Use `is None`
or `is not None`, and learn the additional missingness rules of later tabular
objects.

## Check

Convert assumptions into small checks:

```python
assert isinstance(customer_id, str)
assert isinstance(tenure_months, int)
assert 1 <= tenure_months <= 48
assert monthly_usage_hours >= 0
assert support_tickets >= 0
assert isinstance(renewed, int)
assert renewed in {0, 1}
assert isinstance(has_open_case, bool)
```

Predict which check would fail if `monthly_usage_hours = "24.5"`. Then predict
which calculation would repeat text before a later operation fails.

Inspect both values and types when results surprise you:

```python
print(annualized_usage_hours, type(annualized_usage_hours))
print(eligible_for_predecision_review, type(eligible_for_predecision_review))
print(observed_nonrenewal, type(observed_nonrenewal))
```

Floats are useful for exploration but cannot represent every decimal exactly. Use a tolerance for approximate numeric checks:

```python
assert abs((0.1 + 0.2) - 0.3) < 1e-9
```

## Explain

An expression works from the inside out:

1. Python looks up the values bound to names.
2. Operators or functions consume those values.
3. They return a new value with a type.
4. Assignment can bind that result to another name.

Assignment is not mathematical equality. If
`previous_usage = monthly_usage_hours` when the value is `24.5`, then changing
`monthly_usage_hours` leaves `previous_usage` at `24.5`. Names make a sequence
readable; types constrain each step.

Boolean expressions deserve special care because they become filters, labels, and policy rules. Write them so another person can challenge each condition.

## Practice

Create names for a customer with an ID, plan, tenure, monthly usage, ticket
count, missing satisfaction score, and renewal outcome. Before running, predict
the type of every value.

Then write readable expressions for:

1. twelve times the current monthly usage;
2. whether tenure is between 1 and 48 inclusive and usage is non-negative;
3. a one-line text summary using an f-string;
4. whether the record has activity and a missing satisfaction score;
5. average weekly usage using `30 / 7` days per week.

For each result, record the expected value and type first. Add one `assert` that checks a meaningful assumption rather than merely repeating the assignment.

Refactor this expression into named parts and parentheses:

```python
flag = monthly_usage_hours < 5 and support_tickets >= 2 or tenure_months < 3
```

There are at least two plausible policies hiding in it. Explain which grouping you chose and why.

## Keep going

You can now read a short expression as a mechanism: inputs with types, an operation, and an output with a predictable value and type.

Before moving on, check that you can distinguish names, values, and types; predict arithmetic and comparison outputs; build strings without mixing incompatible types; handle `None`; split boolean rules into readable parts; and write checks that expose assumptions.

Next, you will package expressions into small functions and apply them consistently to collections of records.
