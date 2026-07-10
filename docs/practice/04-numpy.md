# Practice 04 — Keep shape and axis visible

This journey pairs with [lesson 04](../lessons/04-numpy.md) and
`exercises/03-numpy/`.

## Worked warm-up

For an array with shape `(5, 3)`, rows are five customers and columns are three
features. `values.mean(axis=0)` reduces the row axis and returns one mean per
feature with shape `(3,)`. Naming it `feature_means` preserves that meaning.

## Try

### Completion — implement `standardize_columns`

In `exercises/03-numpy/starter.py`, implement `standardize_columns`. Require a
non-empty two-dimensional **finite, real-valued numeric** array; reject complex
values, `NaN`, positive or negative infinity, and any constant column. Return a
new float array of the same shape and leave the input unchanged. Predict the
shapes of column means, population standard deviations, and output for both
`(3, 2)` and `(2, 3)` inputs. Standardize along `axis=0`.

### Transfer — diagnose alignment in `scratch.py`

Create a `(5, 3)` matrix in `scratch.py`. Try subtracting arrays with shapes
`(3,)`, `(1, 3)`, `(5, 1)`, and `(2,)`. Predict which work, the result shape,
and what values are conceptually repeated. Explain the failure without saying
only “NumPy does not like it.”

## Hint 1

??? tip "Reveal Hint 1"
    `axis=0` collapses rows, so remaining positions correspond to columns.
    NumPy's default `std` uses the population convention required here.

## Hint 2

??? tip "Reveal Hint 2"
    For transfer, compare dimensions from the right. They are compatible when
    equal or when one of them is `1`.

## Tests or rubric

The supplied tests validate the **Completion** task:

```bash
uv run pytest exercises/03-numpy/test_starter.py -q
```

Also add non-square, complex, and non-finite completion cases, then check:

```python
matrix = np.array([[1, 10], [2, 30], [3, 50]], dtype=float)
standardized = standardize_columns(matrix)
assert standardized.shape == matrix.shape
assert standardized.dtype.kind == "f"
assert np.allclose(standardized.mean(axis=0), 0)
assert np.allclose(standardized.std(axis=0), 1)
```

## Worked reasoning

??? success "Reveal worked reasoning"
    Standardisation subtracts one mean per feature and divides by one standard
    deviation per feature. Both parameter arrays have shape `(3,)` for a
    `(5, 3)` matrix and broadcast back across rows. A constant column must fail
    because division by zero would not define a useful standardized feature.
    Complex values, `NaN`, and infinity must fail before means are calculated:
    complex measurements are outside this exercise's real-valued contract, and
    non-finite values would propagate into an output that cannot satisfy the
    promised invariants.

    In transfer, `(3,)` and `(1, 3)` align with feature columns. `(5, 1)`
    assigns one adjustment per customer and repeats across columns. `(2,)`
    fails because its trailing `2` is neither `3` nor `1`.

Next: [lesson 05](../lessons/05-pandas.md) or [practice 05](05-pandas.md).
