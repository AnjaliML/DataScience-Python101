# 10 — Evaluation: measure the mistakes that matter

A held-out score is useful only when its metric, threshold, and test data match
the decision. Evaluation asks which errors occur, for whom, and how reliably.

## Frame

Suppose the renewal team can contact 100 subscriptions. Missing a likely
non-renewer wastes an opportunity; contacting a likely renewer uses scarce
capacity. Those errors have different costs.

For this lesson, treat **not renewed** as the positive class: it is the event
that triggers attention. Convert the lesson 09 target explicitly:

~~~python
y_train_risk, y_test_risk = 1 - y_train, 1 - y_test
~~~

The model still estimates renewal probability, so risk probability is
`1 - renewal_probability`. Naming the event prevents precision and recall from
silently referring to the opposite class.

## Predict

Predict that lowering the risk threshold flags more rows: recall usually rises,
precision may fall, and false positives increase. Also predict why accuracy can
look high while finding few of the non-renewers the intervention targets.

## Build

Start with probabilities and a declared threshold:

~~~python
import numpy as np
from sklearn import metrics as sk_metrics

renewal_probability = model.predict_proba(X_test)[:, 1]
risk_probability = 1.0 - renewal_probability

def metric_values(truth, predictions, probabilities):
    return {
        "accuracy": float(sk_metrics.accuracy_score(truth, predictions)),
        "precision": float(sk_metrics.precision_score(
            truth, predictions, zero_division=0)),
        "recall": float(sk_metrics.recall_score(
            truth, predictions, zero_division=0)),
        "f1": float(sk_metrics.f1_score(truth, predictions, zero_division=0)),
        "roc_auc": float(sk_metrics.roc_auc_score(truth, probabilities)),
    }

~~~

Each metric answers a different question:

| Metric | Question | Important limitation |
| --- | --- | --- |
| Accuracy | What fraction of all labels were correct? | Can hide failure on a minority class |
| Precision | Of those flagged, how many actually did not renew? | Ignores missed non-renewers |
| Recall | Of all non-renewers, how many were flagged? | Ignores unnecessary contacts |
| F1 | What is the harmonic mean of precision and recall? | Assumes the two deserve equal weight |
| ROC-AUC | How often is a non-renewer ranked above a renewer? | Does not choose an operating threshold |

The confusion matrix preserves all four error counts. Rows are actual classes
and columns predicted classes; label both axes when plotting it.

### Choose thresholds without spending the test set

Use out-of-fold predictions from training data to compare thresholds. Keep the
test set for one final estimate after the choice is fixed.

~~~python
from sklearn.model_selection import StratifiedKFold, cross_val_predict

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=101)
oof_renewal_probability = cross_val_predict(
    model, X_train, y_train, cv=cv, method="predict_proba",
)[:, 1]
oof_risk_probability = 1.0 - oof_renewal_probability

threshold_rows = []
for candidate in (0.30, 0.50, 0.70):
    predicted = (oof_risk_probability >= candidate).astype(int)
    precision = sk_metrics.precision_score(
        y_train_risk, predicted, zero_division=0)
    recall = sk_metrics.recall_score(
        y_train_risk, predicted, zero_division=0)
    threshold_rows.append((candidate, precision, recall, int(predicted.sum())))

eligible = [row for row in threshold_rows if row[2] >= 0.70 and row[3] <= 100]
if not eligible:
    raise ValueError("no threshold meets recall and capacity constraints")
threshold = float(max(eligible, key=lambda row: row[1])[0])
~~~

Choose using a rule stated before looking at the test result—for example, the
highest precision among thresholds that meet a required recall and capacity.

### Estimate variability

Cross-validation exposes how performance changes across training partitions:

~~~python
from sklearn.model_selection import cross_validate

fold_scores = cross_validate(
    model, X_train, y_train_risk, cv=cv,
    scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
)
metric_names = ("accuracy", "precision", "recall", "f1", "roc_auc")
cv_summary = {
    name: {
        "mean": float(fold_scores[f"test_{name}"].mean()),
        "std": float(fold_scores[f"test_{name}"].std(ddof=1)),
    }
    for name in metric_names
}
~~~

`cross_validate` fits the risk target in each fold. Fold standard deviation is
variation across these partitions, not a confidence interval for all customers.

## Check

Audit performance by subgroup and inspect individual errors:

~~~python
import pandas as pd

risk_prediction = (risk_probability >= threshold).astype(int)
baseline_risk_probability = 1.0 - baseline.predict_proba(X_test)[:, 1]
baseline_risk_prediction = 1 - baseline.predict(X_test)
model_metrics = metric_values(y_test_risk, risk_prediction, risk_probability)
baseline_metrics = metric_values(
    y_test_risk, baseline_risk_prediction, baseline_risk_probability)
matrix = sk_metrics.confusion_matrix(y_test_risk, risk_prediction, labels=[0, 1])
audit = X_test[["plan"]].copy()
audit["actual_risk"] = y_test_risk
audit["predicted_risk"] = risk_prediction
audit["risk_probability"] = risk_probability

subgroups = []
for plan, group in audit.groupby("plan", dropna=False):
    actual = group["actual_risk"]
    predicted = group["predicted_risk"]
    subgroups.append({
        "plan": plan,
        "rows": len(group),
        "recall": float(sk_metrics.recall_score(
            actual, predicted, zero_division=0)),
        "false_positives": int(((actual == 0) & (predicted == 1)).sum()),
        "false_negatives": int(((actual == 1) & (predicted == 0)).sum()),
    })
subgroup_metrics = pd.DataFrame(subgroups)
errors = audit.loc[audit["actual_risk"] != audit["predicted_risk"]]

metrics_payload = {
    "positive_class": "not_renewed",
    "threshold": threshold,
    "threshold_rule": "highest precision with recall >= 0.70 and flagged <= 100",
    "baseline": baseline_metrics,
    "logistic_regression": model_metrics,
    "cross_validation": cv_summary,
    "confusion_matrix": matrix.astype(int).tolist(),
    "holdout_rows": int(len(y_test_risk)),
    "subgroups": subgroup_metrics.to_dict(orient="records"),
    "limitations": [
        "synthetic data", "one holdout split", "prediction is not intervention"
    ],
}

assert np.isfinite(risk_probability).all()
assert ((0 <= risk_probability) & (risk_probability <= 1)).all()
assert matrix.sum() == len(y_test_risk)
assert metrics_payload["positive_class"] == "not_renewed"
~~~

## Explain

An honest evaluation exposes every choice in `metrics_payload`. It bounds a
historical estimate; it does not show that contacting someone changes renewal.
