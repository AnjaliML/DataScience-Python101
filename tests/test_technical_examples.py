from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType

import numpy as np
import pandas as pd
import pytest
from sklearn import metrics as sk_metrics

ROOT = Path(__file__).resolve().parents[1]


def _load_module(relative_path: str) -> ModuleType:
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _python_block(markdown: str, marker: str) -> str:
    blocks = re.findall(r"~~~python\n(.*?)\n~~~", markdown, flags=re.DOTALL)
    return next(block for block in blocks if marker in block)


def _metric_values(truth, predictions, probabilities):
    return {
        "accuracy": float(sk_metrics.accuracy_score(truth, predictions)),
        "precision": float(
            sk_metrics.precision_score(truth, predictions, zero_division=0)
        ),
        "recall": float(sk_metrics.recall_score(truth, predictions, zero_division=0)),
        "f1": float(sk_metrics.f1_score(truth, predictions, zero_division=0)),
        "roc_auc": float(sk_metrics.roc_auc_score(truth, probabilities)),
    }


def test_evaluation_lesson_scores_folds_at_selected_threshold() -> None:
    lesson = (ROOT / "docs/lessons/10-evaluation.md").read_text(encoding="utf-8")
    block = _python_block(lesson, "fold_values")
    namespace = {
        "folds": [
            (np.array([2, 3]), np.array([0, 1])),
            (np.array([0, 1]), np.array([2, 3])),
        ],
        "metric_values": _metric_values,
        "np": np,
        "oof_risk_probability": np.array([0.60, 0.65, 0.20, 0.90]),
        "threshold": 0.70,
        "y_train_risk": pd.Series([0, 1, 0, 1]),
    }

    exec(compile(block, "10-evaluation.md", "exec"), namespace)

    expected = {
        "accuracy": {"mean": 0.75, "std": np.sqrt(0.125)},
        "precision": {"mean": 0.50, "std": np.sqrt(0.5)},
        "recall": {"mean": 0.50, "std": np.sqrt(0.5)},
        "f1": {"mean": 0.50, "std": np.sqrt(0.5)},
        "roc_auc": {"mean": 1.00, "std": 0.0},
    }
    for metric, values in expected.items():
        assert namespace["cv_summary"][metric] == pytest.approx(values)
    assert "fold_predictions = (fold_probabilities >= threshold)" in block
    assert "cross_validate" not in lesson


def test_evaluation_lesson_reuses_declared_folds_for_oof_probabilities() -> None:
    lesson = (ROOT / "docs/lessons/10-evaluation.md").read_text(encoding="utf-8")
    threshold_block = _python_block(lesson, "cross_val_predict")

    assert "folds = list(cv.split(X_train, y_train))" in threshold_block
    assert "cv=folds" in threshold_block
    assert "pooled out-of-fold predictions also selected" in " ".join(lesson.split())
    assert "held-out test set remains the one final estimate" in lesson


def test_dataframe_solution_counts_declared_customer_grain() -> None:
    solution = _load_module("solutions/04-dataframes/solution.py")
    customers = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3"],
            "plan": ["plus", "basic", "basic"],
            "renewed": [1, 1, 0],
        }
    )
    original = customers.copy(deep=True)

    result = solution.summarise_plans(customers)

    assert result.to_dict("records") == [
        {"plan": "basic", "customers": 2, "renewal_rate": 0.5},
        {"plan": "plus", "customers": 1, "renewal_rate": 1.0},
    ]
    pd.testing.assert_frame_equal(customers, original)


@pytest.mark.parametrize(
    "customers",
    [
        pd.DataFrame({"plan": ["basic"], "renewed": [1]}),
        pd.DataFrame(
            {"customer_id": ["C1", "C1"], "plan": ["basic"] * 2, "renewed": [1] * 2}
        ),
        pd.DataFrame({"customer_id": [None], "plan": ["basic"], "renewed": [1]}),
        pd.DataFrame({"customer_id": [" "], "plan": ["basic"], "renewed": [1]}),
    ],
)
def test_dataframe_solution_rejects_undefined_customer_grain(
    customers: pd.DataFrame,
) -> None:
    solution = _load_module("solutions/04-dataframes/solution.py")

    with pytest.raises(ValueError):
        solution.summarise_plans(customers)
