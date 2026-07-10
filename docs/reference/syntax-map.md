# Python syntax map

Use this page to recall a pattern after you understand its purpose. Before running an expression, predict its value, type, or shape.

## Values and names

```python
customer_id = "C1042"       # str
monthly_usage_hours = 24.5   # float
support_tickets = 1          # int
renewed = 1                  # int: raw target is 0 or 1
satisfaction_score = None    # NoneType
```

Assignment binds a name to a value. Use descriptive `snake_case` names and include units when they matter: `window_days`, not `window`.

```python
annualized_usage_hours = monthly_usage_hours * 12
daily_usage_hours = monthly_usage_hours / 30
usage_is_nonnegative = monthly_usage_hours >= 0
has_no_score = satisfaction_score is None
```

Arithmetic uses `+`, `-`, `*`, `/`, `//`, `%`, and `**`. Comparisons return booleans: `==`, `!=`, `<`, `<=`, `>`, `>=`.

## Strings, f-strings, and hints

```python
plan = " Plus ".strip().lower()
label = f"{customer_id}: {monthly_usage_hours} monthly hours"
```

An f-string formats values as text. Type hints document an intended contract but do not enforce it at runtime:

```python
def annualized_usage(monthly_hours: float) -> float:
    return monthly_hours * 12
```

## Collections

```python
ticket_counts = [0, 2, 1]  # ordered, mutable list
customer = {"customer_id": "C1042", "support_tickets": 1}
ticket_counts[0]              # first item
ticket_counts[-1]             # last item
ticket_counts[:2]             # new list containing the first two items
customer["customer_id"]       # fail with KeyError if absent
customer.get("plan", "unknown")
```

Do not use a default of zero for missing data unless missing and zero have the same meaning.

## Conditions and booleans

```python
if support_tickets >= 3:
    band = "high"
elif support_tickets >= 1:
    band = "medium"
else:
    band = "low"
```

Combine scalar conditions with `and`, `or`, and `not`. Put each non-trivial condition in parentheses or bind it to a descriptive name.

## Loops and comprehensions

```python
total_tickets = 0
for count in ticket_counts:
    total_tickets = total_tickets + count
```

Use a comprehension for one readable transformation or filter:

```python
doubled = [count * 2 for count in ticket_counts]
nonzero_counts = [count for count in ticket_counts if count > 0]
```

Prefer a loop when the body needs multiple steps, checks, or explanation.

## Functions and exceptions

```python
def has_many_tickets(ticket_count: int) -> bool:
    """Return whether a non-negative ticket count is at least three."""
    if ticket_count < 0:
        raise ValueError("ticket_count must be non-negative")
    return ticket_count >= 3

try:
    result = has_many_tickets(-1)
except ValueError as error:
    print(f"Invalid record: {error}")
```

Catch only errors you can handle. Never use an empty `except` to hide unexpected failures.

## Imports and paths

```python
from pathlib import Path
import numpy as np
import pandas as pd

data_path = Path("data") / "customer_renewals.csv"
if not data_path.exists():
    raise FileNotFoundError(data_path)
```

`Path` handles platform-safe path joining. Resolve paths from a known project directory rather than assuming an arbitrary working directory.

## NumPy

```python
features = np.array([[18, 7], [3, 1], [26, 4]])
features.shape                    # (3, 2)
features[:, 1]                    # second column
features[features[:, 1] < 3]      # mask rows
features.mean(axis=0)             # one mean per column
features - features.mean(axis=0)  # broadcast column means across rows
# Check axis meaning, shape, and dtype before calculating.
assert features.ndim == 2
assert features.shape[1] == 2
assert np.isfinite(features).all()
```

## pandas

```python
customers = pd.read_csv(data_path)
customers.head()
customers.shape
customers.dtypes
customers["plan"].value_counts(dropna=False)
active = customers.loc[customers["monthly_usage_hours"] > 0].copy()
summary = (
    active.groupby("plan", as_index=False, dropna=False)
    .agg(customers=("customer_id", "nunique"),
         mean_usage=("monthly_usage_hours", "mean"))
)
```

Use `.loc[rows, columns]` for explicit selection. Name the row grain before grouping, and inspect missing values before dropping them.

## Tests and checks

```python
assert annualized_usage(10.0) == 120.0
assert has_many_tickets(3) is True
assert customers["customer_id"].notna().all()
assert customers["customer_id"].is_unique
assert customers["renewed"].isin([0, 1]).all()
# Compare computed floats or arrays with a tolerance.
assert abs(annualized_usage(0.10) - 1.20) < 1e-9
assert np.allclose(features.mean(axis=0), [47 / 3, 4])
```

A passing assertion confirms only the condition you wrote. Pair every important result with a plain-language claim and a check that could disprove it.
