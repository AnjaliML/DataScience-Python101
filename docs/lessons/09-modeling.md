# 09 — Supervised learning: start with a baseline

Supervised learning estimates an outcome from examples where that outcome is
already known. The useful question is not “Can we use machine learning?” It is
whether a model improves a declared decision over a simple baseline on data it
did not learn from.

## Frame

Return to the renewal question:

> Using information available before expiry, can we identify subscriptions
> that are less likely to renew?

The target is `renewed`: `1` for renewed and `0` for not renewed. The feature
table is conventionally named `X`, and the target vector is named `y`.

One row must represent the same unit in both objects. Features must be available
at prediction time. A model trained with future payment information would be a
very accurate answer to the wrong question.

## Predict

Before fitting anything, predict:

1. the number of rows in `X` and `y`;
2. which columns are numeric and which are categorical;
3. which class is more common;
4. the accuracy of always predicting that common class;
5. which preprocessing steps must learn values from training data.

That fourth prediction is the baseline against which complexity must earn its place.

## Build

Load the data and convert the target deliberately:

~~~python
import pandas as pd

customers = pd.read_csv("data/customer_renewals.csv")

renewal_map = {
    "true": 1, "false": 0, "yes": 1, "no": 0,
    "1": 1, "0": 0, "1.0": 1, "0.0": 0,
}
renewal_text = customers["renewed"].astype("string").str.strip().str.lower()
y = renewal_text.map(renewal_map)
if y.isna().any():
    raise ValueError("renewed contains missing or unknown values")
y = y.astype("int8")
~~~

Select only columns allowed by the question contract. Identifiers locate rows;
they are not automatically useful features.

~~~python
numeric_features = [
    "tenure_months", "monthly_usage_hours",
    "support_tickets", "satisfaction_score",
]
categorical_features = ["plan", "signup_channel"]
feature_columns = numeric_features + categorical_features
X = customers[feature_columns].copy()

assert len(X) == len(y)
assert X.index.equals(y.index)
~~~

Split before fitting imputers, scalers, encoders, or the model:

~~~python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=101,
)
~~~

`stratify=y` keeps class proportions similar. `random_state` makes this teaching
split repeatable. The test rows now remain untouched until final evaluation.

Fit a deliberately simple baseline on the training rows:

~~~python
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy="prior")
baseline.fit(X_train, y_train)
baseline_accuracy = baseline.score(X_test, y_test)
~~~

Now build one pipeline. Numeric columns receive median imputation and scaling.
Categorical columns receive most-frequent imputation and one-hot encoding.

~~~python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric_steps = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])
categorical_steps = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])

preprocess = ColumnTransformer([
    ("numeric", numeric_steps, numeric_features),
    ("categorical", categorical_steps, categorical_features),
])

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1_000)),
])
model.fit(X_train, y_train)
model_accuracy = model.score(X_test, y_test)
~~~

The pipeline matters: its imputation, scaling, and category vocabulary are
learned from `X_train` inside `fit`. The same learned transformations are then
applied to `X_test`. Fitting preprocessing on the whole table would let the
test set influence training.

Logistic regression estimates a probability and applies a threshold. Here it
performs binary classification. It is fast and inspectable, but it is not proof
of causation or future business value.

## Check

Check boundaries before celebrating a score:

~~~python
from sklearn.metrics import accuracy_score

baseline_predictions = baseline.predict(X_test)
model_predictions = model.predict(X_test)

assert set(model_predictions).issubset({0, 1})
assert set(X_train.index).isdisjoint(X_test.index)
assert len(model_predictions) == len(y_test)
assert baseline_accuracy == accuracy_score(y_test, baseline_predictions)
assert model_accuracy == accuracy_score(y_test, model_predictions)

print({"baseline": baseline_accuracy, "model": model_accuracy})
~~~

Do not require the model to win in a unit test. Test repeatability, valid
outputs, schema, and absence of split overlap instead.

## Explain

Historical rows supply features and known targets. A split reserves rows that
cannot influence fitting. Preprocessing and the classifier learn from training
rows, then held-out predictions are compared with known outcomes and a baseline.

A model score summarizes this mechanism; it does not replace it. Logistic
regression coefficients describe the fitted data representation, not the
effect of changing a customer’s plan, usage, or support experience.

## Practice

1. Predict the majority-class accuracy before printing it.
2. Fit a seeded `DummyClassifier(strategy="stratified")` and explain the seed.
3. Add a future-derived feature, explain why it leaks the target, then remove it.
4. Test an unknown plan in `X_test` and a missing numeric value.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → tests → worked reasoning](../practice/09-modeling.md).
The completion task isolates the target and baseline; transfer builds a split-first pipeline.

## Keep going

You now have a baseline and fitted pipeline, not a finished result. Next, ask
which mistakes matter, how stable the estimate is, and where it may differ.
