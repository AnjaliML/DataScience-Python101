# Exercise 03 — Shapes before values

## Frame

Standardise every feature column so columns measured on different scales can be
compared by a model.

## Predict

For a matrix with shape `(4, 3)`, predict the shapes of the column means,
column standard deviations, and returned matrix. Which axis produces them?

## Build

Implement `standardize_columns` in `starter.py`. It must:

- require a two-dimensional, non-empty, real-valued numeric array (complex
  values are not supported);
- require every input value to be finite (reject `NaN`, positive infinity, and
  negative infinity);
- reject any column with zero standard deviation;
- return a new floating-point array of the same shape;
- give every output column mean approximately zero and population standard
  deviation approximately one, with only finite values;
- leave the input unchanged.

## Check

Run the tests, then add a non-square input. A solution that accidentally uses
the wrong axis should fail your new test. Also try `np.nan`, `np.inf`, and
`-np.inf`: each represents an undefined or unbounded measurement and must raise
`ValueError` before standardisation. A complex-valued matrix must also raise
`ValueError` rather than silently losing its imaginary component.

## Explain

Why must scaling parameters later be fitted only on training rows?
