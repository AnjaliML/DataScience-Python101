# 04 — NumPy arrays: shape before calculation

NumPy stores many values in a compact array and performs one operation across them. Its power comes with a discipline: before calculating, state the array's shape, axis meaning, and data type.

## Frame

Install and import NumPy, then create a small feature matrix:

```python
import numpy as np

# Rows are customers; columns are tenure, usage hours, support tickets.
features = np.array([
    [18, 7, 0],
    [3, 1, 2],
    [26, 4, 1],
    [8, 0, 3],
])
```

Its contract is: axis 0 holds customers; axis 1 holds features; columns 0–2
hold tenure in months, monthly usage hours, and support tickets.

The array's metadata makes part of that structure visible:

```python
print(features.shape)
print(features.ndim)
print(features.dtype)
```

`shape` is `(4, 3)`: four rows by three columns. `ndim` is `2`. All elements share one numeric `dtype`.

## Predict

Before running, write the value, shape, number of dimensions, and data type category expected from each expression:

```python
features[0, 1]
features[0]
features[:, 1]
features[1:3, :2]
features[:, 1] < 3
features[features[:, 1] < 3]
features.mean(axis=0)
features.mean(axis=1)
features.mean(axis=0, keepdims=True)
```

A scalar has no array shape. Selecting one row or column with a single integer produces a one-dimensional array. Slicing keeps the selected axes.

Say what each resulting number means. If you cannot name the aggregation in words, do not trust the calculation yet.

## Build

Select values by position with `array[row, column]`:

```python
first_customer_usage = features[0, 1]
all_usage = features[:, 1]
first_two_customers = features[:2, :]
tenure_and_usage = features[:, :2]
```

Check shape after every structural operation:

```python
assert all_usage.shape == (4,)
assert first_two_customers.shape == (2, 3)
assert tenure_and_usage.shape == (4, 2)
```

A comparison is vectorized: NumPy compares every selected element and returns a boolean array of the same shape.

```python
low_activity_mask = all_usage < 3
print(low_activity_mask)
```

```python
low_activity_customers = features[low_activity_mask]
assert low_activity_customers.shape == (2, 3)
```

Combine masks element by element with `&`, `|`, and `~`. Parenthesize every comparison:

```python
support_tickets = features[:, 2]
priority_mask = (all_usage < 3) & (support_tickets >= 2)
priority_customers = features[priority_mask]
```

Python's `and` and `or` expect one truth value; an array contains many. Use the array operators for masks.

An **axis** names the dimension NumPy reduces over. `axis=0` collapses rows and leaves one value per column; `axis=1` collapses columns and leaves one per row:

```python
feature_means = features.mean(axis=0)
row_means = features.mean(axis=1)
```

The second calculation runs, but averaging months, usage hours, and ticket
counts together has no useful unit. Shape correctness does not guarantee
semantic correctness.

Broadcasting lets compatible shapes interact without manually repeating values. Center every feature by its own mean:

```python
centered = features - feature_means
```

The shapes are `(4, 3)` and `(3,)`. NumPy aligns dimensions from the right and reuses the three means for every row. The result is `(4, 3)`.

Vectorization replaces a Python loop with an array operation while preserving shape:

```python
usage_hours_per_week = all_usage / (30 / 7)
```

Avoid mixing text with numeric features in one array:

```python
mixed = np.array([["C1042", 18], ["C1043", 3]])
print(mixed.dtype)
```

NumPy must choose one common type, so the numbers become text. Numeric arithmetic will no longer behave as intended. Keep identifiers separate from numeric matrices.

Converting a float array to integers truncates the fractional part; it does not perform statistical rounding:

```python
values = np.array([1.2, 1.8, -1.8])
integers = values.astype(int)
```

Predict `integers` before running. Make dtype changes explicit and check whether information is lost.

## Check

Treat array assumptions as executable checks:

```python
assert features.ndim == 2
assert features.shape[1] == 3
assert np.issubdtype(features.dtype, np.integer)
assert np.isfinite(features).all()
assert (features >= 0).all()
assert low_activity_mask.dtype == np.bool_
assert low_activity_mask.shape == (features.shape[0],)
```

Check a reduction against its intended meaning:

```python
assert feature_means.shape == (features.shape[1],)
assert np.allclose(centered.mean(axis=0), 0)
```

Floating-point calculations are approximate, so `np.allclose` is safer than exact equality for computed decimals.

## Explain

Most NumPy operations follow one mechanism: inspect input shapes and dtypes, align compatible axes, apply an elementwise operation or reduction, and return a value with a predictable shape and dtype.

Indexing changes what is selected. Masking selects positions where conditions are true. Reduction removes an axis unless `keepdims=True`. Broadcasting expands an operation conceptually without copying repeated values into a larger input.

Vectorization is not permission to hide meaning. Keep column definitions near an unlabeled matrix, and prefer a table library when named, mixed-type columns matter more than raw numeric operations.

## Practice

Create a `(5, 3)` integer array for tenure, monthly usage hours, and support
tickets. State both axes and predict its metadata. Predict one-row, one-column,
and two-column-slice shapes; mask usage below three and ticket counts of at
least one; compute one mean per feature; center the columns by broadcasting;
and verify their means are approximately zero.

Then deliberately try to subtract an array of shape `(2,)` from your `(5, 3)` matrix. Predict the error before running and explain which trailing dimensions are incompatible.

Finally, add a float column representing satisfaction score. Decide whether to
combine it with the integer matrix, and predict the resulting common dtype.

## Keep going

Before moving on, you should be able to state an expected shape before every indexing, masking, reduction, and broadcasting operation.

You should also be able to explain each axis, mask alignment, why `axis=0` returns one value per column, trailing-dimension broadcasting, the role of vectorization, and how a common dtype can turn numbers into text or discard decimals.

The next step is to work with labeled tables, where columns can carry names and different data types while preserving these same habits of prediction and checking.
