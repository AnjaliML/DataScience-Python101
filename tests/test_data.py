from pathlib import Path

import pandas as pd
import pytest

from ds_python101.data import DataValidationError, load_customer_data


def test_course_data_matches_declared_contract(customers: pd.DataFrame) -> None:
    assert customers.shape == (240, 8)
    assert customers["customer_id"].is_unique
    assert set(customers["renewed"]) == {0, 1}
    assert customers["satisfaction_score"].isna().sum() == 18


def test_duplicate_identifiers_fail(tmp_path: Path, customers: pd.DataFrame) -> None:
    invalid = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
    path = tmp_path / "duplicate.csv"
    invalid.to_csv(path, index=False)

    with pytest.raises(DataValidationError, match="customer_id must be unique"):
        load_customer_data(path)


def test_unknown_category_fails(tmp_path: Path, customers: pd.DataFrame) -> None:
    invalid = customers.copy()
    invalid.loc[0, "plan"] = "enterprise"
    path = tmp_path / "unknown.csv"
    invalid.to_csv(path, index=False)

    with pytest.raises(DataValidationError, match="unknown plan"):
        load_customer_data(path)


def test_fractional_target_fails(tmp_path: Path, customers: pd.DataFrame) -> None:
    invalid = customers.copy()
    invalid["renewed"] = invalid["renewed"].astype(float)
    invalid.loc[0, "renewed"] = 0.5
    path = tmp_path / "fractional-target.csv"
    invalid.to_csv(path, index=False)

    with pytest.raises(DataValidationError, match="renewed must contain only"):
        load_customer_data(path)


def test_missing_file_fails_with_path(tmp_path: Path) -> None:
    path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError, match="missing.csv"):
        load_customer_data(path)
