"""Worked solution for Exercise 04."""

import pandas as pd


def summarise_plans(customers: pd.DataFrame) -> pd.DataFrame:
    """Return customer counts and observed renewal rates by plan."""

    required = {"plan", "renewed"}
    if not required <= set(customers.columns):
        raise ValueError(f"required columns: {sorted(required)}")
    if customers[list(required)].isna().any().any():
        raise ValueError("plan and renewed must not be missing")
    if not set(customers["renewed"]) <= {0, 1}:
        raise ValueError("renewed must contain only 0 and 1")

    return (
        customers.groupby("plan", as_index=False, observed=True)
        .agg(customers=("renewed", "size"), renewal_rate=("renewed", "mean"))
        .sort_values("plan")
        .reset_index(drop=True)
    )
