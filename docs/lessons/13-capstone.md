# 13 — Capstone: one question, one reproducible claim

The capstone is a small data-science argument that another person can rebuild,
inspect, and challenge. Its goal is not the highest model score. Its goal is a
visible chain from question and raw rows to evidence and limitations.

## Frame

Use the supplied synthetic `data/customer_renewals.csv` and answer one bounded
question:

> Using information available before renewal, how well does a simple model
> identify customers who will not renew compared with a majority baseline?

The unit is one renewal opportunity. “Not renewed” is the event to flag. The
analysis is predictive, not causal: it cannot establish which action would make
a customer renew.

## Predict

Before running the workflow, write down:

1. the required columns and allowed target values;
2. which fields are known before the decision;
3. likely missingness, range, duplicate, and leakage failures;
4. the majority-class baseline;
5. the direction of the precision–recall tradeoff as the threshold changes;
6. which subgroup may have the least reliable estimate and why.

Save these predictions in the project README. Do not rewrite them after seeing
the result; explain any disagreement instead.

## Build

One command must rebuild the public artifacts from a clean output directory:

~~~bash
uv run ds-python101 --input data/customer_renewals.csv \
  --output-dir build/capstone --seed 101
~~~

The directory must contain exactly these learner-facing outputs:

~~~text
build/capstone/
├── cleaned.csv
├── summary.json
├── renewal-by-plan.png
├── metrics.json
├── confusion-matrix.png
└── manifest.sha256
~~~

### `cleaned.csv`

Preserve the row unit and customer identifier. Normalize text, parse numeric
columns, convert renewal to a documented binary value, retain meaningful
missingness indicators, reject duplicate IDs, and leave the raw CSV unchanged.
Write columns in a stable order.

### `summary.json`

Record source and cleaned row counts, original missingness, plan and target
counts, renewal rate, feature list, target definition, split seed, test
fraction, and every exclusion or repair.

Serialize with sorted keys and no current timestamp so identical inputs and
code produce identical bytes.

### `renewal-by-plan.png`

Build a supporting table first: one row per plan with customer count and
observed renewal rate. Plot a zero-based rate axis, label group sizes, and use
language such as “observed association.” The figure does not show that changing
a customer’s plan would change renewal.

### `metrics.json`

Fit on training rows only. The exact top-level keys are `positive_class`,
`threshold`, `threshold_rule`, `baseline`, `logistic_regression`,
`cross_validation`, `confusion_matrix`, `holdout_rows`, `subgroups`, and
`limitations`. Both model dictionaries contain `accuracy`, `precision`,
`recall`, `f1`, and `roc_auc`. Each cross-validation metric contains `mean` and
`std`. Each subgroup record contains `plan`, `rows`, `recall`,
`false_positives`, and `false_negatives`.

Choose the threshold from training folds, then evaluate it once on the held-out
test set. Do not choose it because the test result looks attractive.

### `confusion-matrix.png`

Label actual and predicted axes, use the same positive-class convention as
`metrics.json`, and show integer counts. The four cells must sum to the number
of held-out rows.

### `manifest.sha256`

List a SHA-256 checksum and relative path for each generated artifact except the
manifest itself. Sort entries by path. Record the raw input checksum separately
in `summary.json` so a reviewer can detect any byte-level change.

## Check

The one command should stop with a non-zero exit status if any required check
fails. At minimum, verify:

~~~python
assert cleaned["customer_id"].notna().all()
assert cleaned["customer_id"].is_unique
assert cleaned["renewed"].isin([0, 1]).all()
assert set(X_train.index).isdisjoint(X_test.index)
assert len(test_predictions) == len(y_test)
assert confusion_matrix_values.sum() == len(y_test)
assert all(0.0 <= value <= 1.0 for value in reported_metrics.values())
~~~

Also check that preprocessing has not been fitted before splitting, all six
artifacts exist and are non-empty, the figures remain readable at final size,
and a second run produces the same checksums.

Include tests for an unknown target label, duplicate customer ID, unseen test
category, missing numeric value, deterministic split, and unchanged raw input.

## Explain

Write the final explanation in this order:

1. **Question:** decision, row unit, prediction time, target, and baseline.
2. **Data:** source, schema, missingness, cleaning policy, and exclusions.
3. **Transformation:** split, preprocessing, model, seed, and threshold rule.
4. **Validation:** tests, baseline comparison, cross-validation, and held-out
   metrics.
5. **Insight:** the strongest supported pattern in plain language.
6. **Limitations:** sampling, measurement, drift, subgroup size, and the gap
   between prediction and intervention.

A useful conclusion can be “the model did not improve enough over the
baseline.” Do not search through features, seeds, thresholds, and metrics until
one result looks impressive and then hide that search.

## Review rubric

| Criterion | 0 — Missing | 1 — Partial | 2 — Convincing |
| --- | --- | --- | --- |
| Question | vague task | target or decision stated | unit, timing, target, baseline, and error cost are explicit |
| Data | unexplained CSV | basic schema | provenance, grain, timing, missingness, and cleaning policy |
| Transformation | tangled notebook state | mostly repeatable | split-first tested pipeline with explicit seed and threshold rule |
| Validation | one preferred score | baseline or holdout | baseline, multiple metrics, CV variation, confusion matrix, and tests |
| Insight | unsupported claim | pattern described | bounded claim tied directly to tables and figures |
| Reproducibility | manual steps | documented commands | clean one-command rebuild, locked environment, stable artifacts, manifest |
| Limitations | absent | generic caveat | concrete coverage, uncertainty, subgroup, drift, and causal limits |

Aim for no zero in any row. Extra models, dashboards, and decorative plots do
not compensate for a missing question or invalid split.

## Practice

Build the capstone in passes:

1. make schema and cleaning tests pass, then write cleaned data and summary;
2. create the plan summary and figure;
3. fit the dummy baseline and logistic pipeline;
4. select a threshold with training folds and evaluate once;
5. add subgroup and error analysis;
6. write the manifest, rebuild from empty, and ask a peer to reproduce it.

## Keep going

The course ends with a workflow, not a final algorithm:

~~~text
question → data → transformation → validation → insight
~~~

Carry that sequence into unfamiliar datasets. Predict before running, preserve
row meaning, reserve independent evidence, compare with a baseline, make errors
visible, and say where the claim must stop.
