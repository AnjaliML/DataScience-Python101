# Exercise 02 — A metric is a contract

## Frame

Implement `renewal_rate`, a small function that summarises binary outcomes.

## Predict

Predict the result for `[1, 0, 1, 1]`. Decide what should happen for an empty
list, a value of `2`, and a Boolean before reading the tests.

## Build

Edit `starter.py`. The function must:

- accept a list of integer zeros and ones;
- return their arithmetic mean as a float;
- reject an empty list;
- reject non-integers, Booleans, and integers other than zero or one;
- leave the input unchanged.

## Check

```bash
uv run pytest -q
```

Add one test that distinguishes your chosen policy from a tempting but invalid
implementation.

## Explain

Why is returning `0.0` for an empty list analytically different from raising an
error?
