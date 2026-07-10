# Exercise 04 — Group without losing the denominator

## Frame

A rate without its group size can be misleading. Build a plan summary that
keeps both.

## Predict

Before coding, write the returned columns, number of rows, sort order, and data
type of `renewal_rate`.

## Build

Implement `summarise_plans`. It must:

- require `plan` and `renewed` columns;
- require binary, non-missing outcomes;
- return one row per observed plan;
- return columns `plan`, `customers`, and `renewal_rate`;
- sort plans alphabetically and reset the index;
- leave the input DataFrame unchanged.

## Check

Run the tests. Add a plan with one customer and make sure both its count and
rate remain visible.

## Explain

Why would selecting only the highest rate be risky when group sizes differ?
