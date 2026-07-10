# Practice 10 — Evaluate the decision rule you will use

This on-site exercise pairs with [lesson 10](../lessons/10-evaluation.md).

## Worked warm-up

A probability model plus a threshold is the prediction rule. If the chosen
threshold is `0.35`, metrics based on the estimator's default `0.50` threshold
describe a different rule. Threshold selection must use training evidence;
the holdout set is spent once on the frozen rule.

## Try

### Completion — audit one threshold

Continue from lesson 10, where each `threshold_rows` tuple is `(threshold,
precision, recall, flagged)`. Replace the six `___` placeholders:

```python
eligible = [
    row for row in threshold_rows
    if row[___] >= 0.70 and row[___] <= 100
]
if not eligible:
    raise ValueError("no threshold meets recall and capacity constraints")

threshold = float(max(eligible, key=lambda row: (row[___], row[___]))[0])
risk_prediction = (risk_probability >= ___).astype(int)
matrix = sk_metrics.confusion_matrix(
    y_test_risk, risk_prediction, labels=[0, 1]
)
holdout_metrics = metric_values(
    y_test_risk, risk_prediction, ___
)
```

Choose the highest-precision threshold that achieves at least 70% training-fold
recall and stays within capacity. Freeze it. Confirm the holdout confusion
matrix, precision, recall, F1, and ROC AUC all describe that rule. Label
non-renewal as the positive class in every artifact.

Then reuse the frozen labels in a plan-level subgroup table with row counts,
recall, false positives, and false negatives. Do not retune the threshold for a
subgroup after seeing its holdout errors.

### Transfer — change the decision cost

Imagine missing a non-renewer becomes twice as costly while review capacity
stays fixed. Write the new threshold rule before recomputing. Compare which
errors move and explain why accuracy alone cannot choose between the rules.

## Hint 1

??? tip "Reveal Hint 1"
    Generate candidate thresholds and metrics entirely from training-fold
    predictions. A capacity rule can be expressed as the number or fraction of
    probabilities at or above each threshold.

## Hint 2

??? tip "Reveal Hint 2"
    After freezing the threshold, compute labels explicitly with
    `(holdout_probability >= threshold).astype(int)`. Pass those labels—not
    `model.predict(...)`—to threshold-dependent metrics.

## Tests or rubric

Check that probability values are finite and within `[0, 1]`, the confusion
matrix sums to holdout size, the positive-class label is repeated in the
report, threshold-dependent metrics use explicit frozen labels, and the
holdout set played no role in threshold selection. Subgroup tables must include
row counts and a warning for small groups.

## Worked reasoning

??? success "Reveal worked reasoning"
    Lowering a threshold usually flags more rows: recall tends to rise while
    precision and capacity pressure may worsen. The exact movement belongs to
    the observed data, so do not promise it in advance. ROC AUC evaluates the
    ranking across thresholds; confusion-matrix metrics evaluate one decision
    rule. Reporting both is useful only when their meanings remain separate.

    When false negatives become more costly, a defensible rule may prioritise
    recall subject to capacity. It is a policy change, not a reason to browse
    the holdout results until a pleasing threshold appears.

    Tuple positions `2`, `3`, `1`, and `0` mean recall, flagged count,
    precision, and threshold. The tuple key breaks equal-precision ties by
    choosing the higher threshold; the explicit `ValueError` is the no-eligible
    policy. The holdout labels use `threshold`, while ROC AUC receives
    `risk_probability`. Passing `model.predict(...)` or hard labels as the
    probability argument would evaluate a different object.

Next: [lesson 11](../lessons/11-reproducibility.md) or
[practice 11](11-reproducibility.md).
