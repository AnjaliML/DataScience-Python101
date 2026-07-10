"""Summaries and leakage-safe baseline modelling for the course dataset."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = (
    "tenure_months",
    "monthly_usage_hours",
    "support_tickets",
    "satisfaction_score",
)
CATEGORICAL_FEATURES = ("plan", "signup_channel")
FEATURES = (*NUMERIC_FEATURES, *CATEGORICAL_FEATURES)
POSITIVE_CLASS = "not_renewed"


@dataclass(frozen=True)
class ModelResult:
    """Model, holdout data, and JSON-safe evaluation results."""

    model: Pipeline
    x_test: pd.DataFrame
    y_test: pd.Series
    predictions: np.ndarray
    probabilities: np.ndarray
    metrics: dict[str, float]
    baseline_metrics: dict[str, float]
    confusion: list[list[int]]
    decision_threshold: float
    threshold_rule: str
    cross_validation: dict[str, dict[str, float]]
    subgroup_metrics: list[dict[str, str | float | int]]


def renewal_summary(customers: pd.DataFrame) -> dict[str, Any]:
    """Return a compact, JSON-safe descriptive summary."""

    plan_rates = customers.groupby("plan", observed=True)["renewed"].mean()
    channel_rates = customers.groupby("signup_channel", observed=True)["renewed"].mean()
    return {
        "rows": int(len(customers)),
        "renewal_rate": float(customers["renewed"].mean()),
        "median_tenure_months": float(customers["tenure_months"].median()),
        "missing_satisfaction": int(customers["satisfaction_score"].isna().sum()),
        "renewal_rate_by_plan": {
            str(name): float(value) for name, value in plan_rates.items()
        },
        "renewal_rate_by_signup_channel": {
            str(name): float(value) for name, value in channel_rates.items()
        },
    }


def make_pipeline(random_state: int = 42) -> Pipeline:
    """Create preprocessing and logistic regression as one fitted object."""

    numeric = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", numeric, list(NUMERIC_FEATURES)),
            ("categorical", categorical, list(CATEGORICAL_FEATURES)),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocessing),
            (
                "model",
                LogisticRegression(max_iter=1_000, random_state=random_state),
            ),
        ]
    )


def _classification_metrics(
    truth: pd.Series,
    predictions: Any,
    probabilities: Any,
) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(truth, predictions)),
        "precision": float(precision_score(truth, predictions, zero_division=0)),
        "recall": float(recall_score(truth, predictions, zero_division=0)),
        "f1": float(f1_score(truth, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(truth, probabilities)),
    }


def _training_fold_predictions(
    model: Pipeline,
    x_train: pd.DataFrame,
    y_train_renewal: pd.Series,
    *,
    random_state: int,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """Return out-of-fold non-renewal probabilities using training rows only."""

    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    probabilities = np.empty(len(y_train_renewal), dtype=float)
    validation_folds = []
    for fit_positions, validation_positions in splitter.split(x_train, y_train_renewal):
        fold_model = clone(model)
        fold_model.fit(
            x_train.iloc[fit_positions],
            y_train_renewal.iloc[fit_positions],
        )
        renewal_probability = fold_model.predict_proba(
            x_train.iloc[validation_positions]
        )[:, 1]
        probabilities[validation_positions] = 1.0 - renewal_probability
        validation_folds.append(validation_positions)
    return probabilities, validation_folds


def _choose_threshold(truth: pd.Series, probabilities: np.ndarray) -> float:
    """Choose the F1-maximising threshold from training-fold predictions."""

    candidates = np.linspace(0.20, 0.80, 61)
    scores = [
        f1_score(truth, probabilities >= threshold, zero_division=0)
        for threshold in candidates
    ]
    best_score = max(scores)
    best_candidates = [
        threshold
        for threshold, score in zip(candidates, scores, strict=True)
        if score == best_score
    ]
    return float(min(best_candidates, key=lambda value: abs(value - 0.5)))


def _cross_validation_summary(
    truth: pd.Series,
    probabilities: np.ndarray,
    validation_folds: list[np.ndarray],
    threshold: float,
) -> dict[str, dict[str, float]]:
    """Summarise training-fold variation at the chosen operating threshold."""

    fold_values = {
        name: [] for name in ("accuracy", "precision", "recall", "f1", "roc_auc")
    }
    for positions in validation_folds:
        fold_truth = truth.iloc[positions]
        fold_probabilities = probabilities[positions]
        fold_predictions = (fold_probabilities >= threshold).astype(int)
        metrics = _classification_metrics(
            fold_truth,
            fold_predictions,
            fold_probabilities,
        )
        for name, value in metrics.items():
            fold_values[name].append(value)

    return {
        name: {
            "mean": float(np.mean(values)),
            "std": float(np.std(values, ddof=1)),
        }
        for name, values in fold_values.items()
    }


def _subgroup_error_metrics(
    x_test: pd.DataFrame,
    truth: pd.Series,
    predictions: np.ndarray,
) -> list[dict[str, str | float | int]]:
    """Return transparent holdout error counts for each observed plan."""

    output = []
    for plan in sorted(x_test["plan"].dropna().astype(str).unique()):
        mask = x_test["plan"].astype(str).eq(plan).to_numpy()
        group_truth = truth.to_numpy()[mask]
        group_predictions = predictions[mask]
        _, false_positive, false_negative, true_positive = confusion_matrix(
            group_truth,
            group_predictions,
            labels=[0, 1],
        ).ravel()
        positive_count = true_positive + false_negative
        output.append(
            {
                "plan": plan,
                "rows": int(mask.sum()),
                "recall": (
                    float(true_positive / positive_count) if positive_count else 0.0
                ),
                "false_positives": int(false_positive),
                "false_negatives": int(false_negative),
            }
        )
    return output


def train_and_evaluate(
    customers: pd.DataFrame,
    *,
    test_size: float = 0.25,
    random_state: int = 42,
) -> ModelResult:
    """Fit a dummy baseline and a leakage-safe logistic-regression pipeline."""

    x = customers.loc[:, list(FEATURES)]
    y_renewal = customers["renewed"]
    x_train, x_test, y_train_renewal, y_test_renewal = train_test_split(
        x,
        y_renewal,
        test_size=test_size,
        random_state=random_state,
        stratify=y_renewal,
    )
    y_train = (1 - y_train_renewal).rename("not_renewed")
    y_test = (1 - y_test_renewal).rename("not_renewed")

    baseline = DummyClassifier(strategy="prior", random_state=random_state)
    baseline.fit(x_train, y_train_renewal)
    baseline_predictions = 1 - baseline.predict(x_test)
    baseline_probabilities = 1.0 - baseline.predict_proba(x_test)[:, 1]

    model = make_pipeline(random_state=random_state)
    training_probabilities, validation_folds = _training_fold_predictions(
        model,
        x_train,
        y_train_renewal,
        random_state=random_state,
    )
    decision_threshold = _choose_threshold(y_train, training_probabilities)
    threshold_rule = "maximise F1 on out-of-fold training predictions"
    model.fit(x_train, y_train_renewal)
    probabilities = 1.0 - model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= decision_threshold).astype(int)

    return ModelResult(
        model=model,
        x_test=x_test,
        y_test=y_test,
        predictions=predictions,
        probabilities=probabilities,
        metrics=_classification_metrics(y_test, predictions, probabilities),
        baseline_metrics=_classification_metrics(
            y_test,
            baseline_predictions,
            baseline_probabilities,
        ),
        confusion=confusion_matrix(y_test, predictions, labels=[0, 1])
        .astype(int)
        .tolist(),
        decision_threshold=decision_threshold,
        threshold_rule=threshold_rule,
        cross_validation=_cross_validation_summary(
            y_train,
            training_probabilities,
            validation_folds,
            decision_threshold,
        ),
        subgroup_metrics=_subgroup_error_metrics(x_test, y_test, predictions),
    )
