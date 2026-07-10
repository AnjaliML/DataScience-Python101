"""Worked solution for Exercise 04."""

import pandas as pd


def summarise_plans(customers: pd.DataFrame) -> pd.DataFrame:
    """Return unique-customer counts and observed renewal rates by plan."""

    required = {"customer_id", "plan", "renewed"}
    if not required <= set(customers.columns):
        raise ValueError(f"required columns: {sorted(required)}")
    if customers[list(required)].isna().any().any():
        raise ValueError("customer_id, plan, and renewed must not be missing")
    if customers["customer_id"].astype("string").str.strip().eq("").any():
        raise ValueError("customer_id must not be blank")
    if not customers["customer_id"].is_unique:
        raise ValueError("customer_id must be unique: expected one row per customer")
    if not set(customers["renewed"]) <= {0, 1}:
        raise ValueError("renewed must contain only 0 and 1")

    return (
        customers.groupby("plan", as_index=False, observed=True)
        .agg(
            customers=("customer_id", "nunique"),
            renewal_rate=("renewed", "mean"),
        )
        .sort_values("plan")
        .reset_index(drop=True)
    )
