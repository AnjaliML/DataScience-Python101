# Practice 09 — Earn the right to beat a baseline

This journey pairs with [lesson 09](../lessons/09-modeling.md) and
`exercises/06-modeling/`.

## Worked warm-up

A prior-probability dummy model learns only class proportions. It supplies a
simple reference rather than useful individual ranking. A more complex model
must justify its extra failure modes with better evidence on rows that did not
influence fitting.

## Try

### Completion — isolate the answer and fit a baseline

In `exercises/06-modeling/starter.py`, implement
`split_features_target`: require `customer_id` and `renewed`, require both
binary target classes, return copied `X` and `y`, and exclude identifier and
target from features. Implement `fit_baseline` by fitting and returning a
`DummyClassifier(strategy="prior")`. Leave both inputs unchanged.

### Transfer — build a split-first pipeline in `scratch.py`

In `scratch.py`, split once with a fixed seed and stratification, fit the
baseline on training rows, then put numeric and categorical preprocessing
inside one pipeline. Challenge it with an unseen plan and one missing numeric
value. Add a future-derived feature, explain why it leaks, and remove it before
fitting.

## Hint 1

??? tip "Reveal Hint 1"
    For completion, use `.drop(columns=[...]).copy()` for features and copy the
    target too. Validate target values and `nunique() == 2` before returning.

## Hint 2

??? tip "Reveal Hint 2"
    For transfer, pass raw training columns into the pipeline. Imputation,
    scaling, and category discovery must happen inside training `fit`.

## Tests or rubric

The supplied tests validate the **Completion** task:

```bash
uv run pytest exercises/06-modeling/test_starter.py -q
```

For transfer, prove train and test indices are disjoint, predictions match test
length, outputs are in `{0, 1}`, the same seed repeats the split, and inputs are
unchanged. Do not require “model beats baseline” in a unit test.

## Worked reasoning

??? success "Reveal worked reasoning"
    The identifier and target have no legitimate place in `X`; copying makes
    the no-mutation promise explicit. Requiring both target classes prevents a
    misleading one-class training problem. The fitted prior baseline answers
    what class proportions alone can achieve.

    In transfer, splitting before fitting creates an evidence boundary. A
    preprocessing step fitted on the whole table leaks information about test
    distributions. The awkward rows test deployment behavior; the future-
    derived feature tests whether a plausible high score uses available data.

Next: [lesson 10](../lessons/10-evaluation.md) or
[practice 10](10-evaluation.md).
