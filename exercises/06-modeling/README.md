# Exercise 06 — Separate the answer before fitting

## Frame

The first protection against target leakage is a visible feature boundary.

## Predict

For the test fixture, predict the shapes and columns of `X` and `y`. Name two
columns that must not be model features.

## Build

Implement:

- `split_features_target`, which returns a copied feature DataFrame and target
  Series after removing `customer_id` and `renewed` from the feature set;
- `fit_baseline`, which fits and returns a `DummyClassifier(strategy="prior")`.

Require the identifier and target, require a binary target with both classes,
and leave the input unchanged.

## Check

Run the tests. Add a suspicious `renewal_confirmation_sent` column and explain
why a mechanically correct feature split could still leak future information.

## Explain

What question does the dummy classifier answer, and why must every more complex
model beat that reference on unseen rows?
