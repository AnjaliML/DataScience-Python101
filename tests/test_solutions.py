from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_solution(relative_path: str) -> ModuleType:
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_function_solution() -> None:
    solution = load_solution("solutions/02-functions/solution.py")
    assert solution.renewal_rate([1, 0, 1, 1]) == 0.75

    with pytest.raises(ValueError, match="list"):
        solution.renewal_rate((1, 0, 1))


def test_numpy_solution() -> None:
    solution = load_solution("solutions/03-numpy/solution.py")
    result = solution.standardize_columns(np.array([[1, 10], [2, 30], [3, 50]]))
    assert result.shape == (3, 2)
    assert np.isfinite(result).all()
    assert np.allclose(result.mean(axis=0), 0)


def test_numpy_solution_standardises_extreme_finite_values() -> None:
    solution = load_solution("solutions/03-numpy/solution.py")
    matrix = np.array(
        [[1e308, 1], [1e308 - 1e292, 2], [1e308 - 2e292, 3]],
        dtype=float,
    )

    result = solution.standardize_columns(matrix)

    assert np.isfinite(result).all()
    assert np.allclose(result.mean(axis=0), 0, atol=1e-12)
    assert np.allclose(result.std(axis=0), 1, atol=1e-12)


@pytest.mark.parametrize("non_finite", [np.nan, np.inf, -np.inf])
def test_numpy_solution_rejects_non_finite_values(non_finite: float) -> None:
    solution = load_solution("solutions/03-numpy/solution.py")
    matrix = np.array([[1.0, 10.0], [2.0, non_finite], [3.0, 30.0]])

    with pytest.raises(ValueError, match="finite"):
        solution.standardize_columns(matrix)


def test_numpy_solution_rejects_complex_values() -> None:
    solution = load_solution("solutions/03-numpy/solution.py")
    matrix = np.array([[1 + 2j, 10], [2 + 3j, 20], [3 + 4j, 30]])

    with pytest.raises(ValueError, match="real numeric"):
        solution.standardize_columns(matrix)


def test_dataframe_solution() -> None:
    solution = load_solution("solutions/04-dataframes/solution.py")
    frame = pd.DataFrame(
        {
            "customer_id": ["C1", "C2"],
            "plan": ["basic", "basic"],
            "renewed": [0, 1],
        }
    )
    result = solution.summarise_plans(frame)
    assert result.loc[0, "customers"] == 2
    assert result.loc[0, "renewal_rate"] == 0.5


def test_cleaning_solution() -> None:
    solution = load_solution("solutions/05-cleaning/solution.py")
    frame = pd.DataFrame(
        {
            "customer_id": ["C1", "C1"],
            "tenure_months": [3, -1],
            "satisfaction_score": [8, None],
            "renewed": [1, 2],
        }
    )
    report = solution.quality_report(frame)
    assert report["duplicate_customer_ids"] == 2
    assert report["invalid_tenure"] == 1


def test_modeling_solution() -> None:
    solution = load_solution("solutions/06-modeling/solution.py")
    frame = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3", "C4"],
            "usage": [1, 2, 8, 9],
            "renewed": [0, 0, 1, 1],
        }
    )
    features, target = solution.split_features_target(frame)
    model = solution.fit_baseline(features, target)
    assert model.predict(features).shape == (4,)
