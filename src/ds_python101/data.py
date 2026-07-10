"""Load and validate the course's tabular customer data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = (
    "customer_id",
    "plan",
    "signup_channel",
    "tenure_months",
    "monthly_usage_hours",
    "support_tickets",
    "satisfaction_score",
    "renewed",
)
VALID_PLANS = frozenset({"basic", "plus", "pro"})
VALID_CHANNELS = frozenset({"organic", "referral", "paid", "partner"})


class DataValidationError(ValueError):
    """Raised when input data violates the declared course schema."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DataValidationError(message)


def validate_customer_data(customers: pd.DataFrame) -> None:
    """Validate schema and domain constraints without changing the table."""

    missing = sorted(set(REQUIRED_COLUMNS) - set(customers.columns))
    _require(not missing, f"missing required columns: {', '.join(missing)}")
    _require(len(customers) > 0, "the dataset contains no rows")
    _require(
        customers["customer_id"].notna().all(),
        "customer_id contains missing values",
    )
    _require(
        customers["customer_id"].map(lambda value: isinstance(value, str)).all(),
        "customer_id must contain strings",
    )
    _require(
        customers["customer_id"].str.strip().ne("").all(),
        "customer_id contains blank values",
    )
    _require(
        customers["customer_id"].is_unique,
        "customer_id must be unique",
    )

    observed_plans = set(customers["plan"].dropna().astype(str))
    unknown_plans = sorted(observed_plans - VALID_PLANS)
    _require(not unknown_plans, f"unknown plan values: {unknown_plans}")
    _require(customers["plan"].notna().all(), "plan contains missing values")

    observed_channels = set(customers["signup_channel"].dropna().astype(str))
    unknown_channels = sorted(observed_channels - VALID_CHANNELS)
    _require(not unknown_channels, f"unknown signup channels: {unknown_channels}")
    _require(
        customers["signup_channel"].notna().all(),
        "signup_channel contains missing values",
    )

    numeric_rules = {
        "tenure_months": (1, 48, False),
        "monthly_usage_hours": (0, 100, False),
        "support_tickets": (0, 30, False),
        "satisfaction_score": (1, 10, True),
    }
    for column, (minimum, maximum, may_be_missing) in numeric_rules.items():
        values = pd.to_numeric(customers[column], errors="coerce")
        if not may_be_missing:
            _require(
                values.notna().all(), f"{column} contains missing or invalid values"
            )
        valid_values = values.dropna()
        _require(
            valid_values.between(minimum, maximum).all(),
            f"{column} must be between {minimum} and {maximum}",
        )

    tenure = pd.to_numeric(customers["tenure_months"], errors="coerce").dropna()
    tickets = pd.to_numeric(customers["support_tickets"], errors="coerce").dropna()
    _require((tenure % 1 == 0).all(), "tenure_months must contain whole numbers")
    _require((tickets % 1 == 0).all(), "support_tickets must contain whole numbers")

    target = pd.to_numeric(customers["renewed"], errors="coerce")
    _require(target.notna().all(), "renewed contains missing or invalid values")
    _require(target.isin([0, 1]).all(), "renewed must contain only 0 and 1")


def load_customer_data(path: str | Path) -> pd.DataFrame:
    """Read a CSV, normalise safe representations, and validate its schema."""

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"data file not found: {source}")

    customers = pd.read_csv(source)
    customers.columns = [str(name).strip() for name in customers.columns]

    for column in ("plan", "signup_channel"):
        if column in customers:
            customers[column] = (
                customers[column].astype("string").str.strip().str.lower()
            )

    for column in (
        "tenure_months",
        "monthly_usage_hours",
        "support_tickets",
        "satisfaction_score",
        "renewed",
    ):
        if column in customers:
            customers[column] = pd.to_numeric(customers[column], errors="coerce")

    validate_customer_data(customers)
    customers["tenure_months"] = customers["tenure_months"].astype("int64")
    customers["support_tickets"] = customers["support_tickets"].astype("int64")
    customers["renewed"] = customers["renewed"].astype("int64")
    return customers.loc[:, list(REQUIRED_COLUMNS)].copy()
