"""Starter: isolate a target and fit an explicit baseline."""

import pandas as pd
from sklearn.dummy import DummyClassifier


def split_features_target(
    customers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return copied features and the binary renewal target."""

    # TODO: validate the boundary, then exclude the ID and target from X.
    raise NotImplementedError


def fit_baseline(features: pd.DataFrame, target: pd.Series) -> DummyClassifier:
    """Fit and return a prior-probability dummy classifier."""

    # TODO: fit a DummyClassifier(strategy="prior") and return it.
    raise NotImplementedError
