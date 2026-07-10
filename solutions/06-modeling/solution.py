"""Worked solution for Exercise 06."""

import pandas as pd
from sklearn.dummy import DummyClassifier


def split_features_target(
    customers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return copied features and the binary renewal target."""

    required = {"customer_id", "renewed"}
    missing = sorted(required - set(customers.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if len(customers.columns) <= 2:
        raise ValueError("at least one feature column is required")
    if customers["renewed"].isna().any() or set(customers["renewed"]) != {0, 1}:
        raise ValueError("renewed must contain both binary classes")

    features = customers.drop(columns=["customer_id", "renewed"]).copy()
    target = customers["renewed"].copy()
    return features, target


def fit_baseline(features: pd.DataFrame, target: pd.Series) -> DummyClassifier:
    """Fit and return a prior-probability dummy classifier."""

    model = DummyClassifier(strategy="prior")
    model.fit(features, target)
    return model
