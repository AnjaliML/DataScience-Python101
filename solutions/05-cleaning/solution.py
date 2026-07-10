"""Worked solution for Exercise 05."""

import pandas as pd


def quality_report(customers: pd.DataFrame) -> dict[str, int]:
    """Count rows and selected schema failures."""

    required = {
        "customer_id",
        "tenure_months",
        "satisfaction_score",
        "renewed",
    }
    missing = sorted(required - set(customers.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    tenure = pd.to_numeric(customers["tenure_months"], errors="coerce")
    renewed = pd.to_numeric(customers["renewed"], errors="coerce")
    return {
        "rows": int(len(customers)),
        "duplicate_customer_ids": int(
            customers["customer_id"].duplicated(keep=False).sum()
        ),
        "missing_satisfaction": int(customers["satisfaction_score"].isna().sum()),
        "invalid_tenure": int((tenure.isna() | ~tenure.between(1, 48)).sum()),
        "invalid_renewed": int((renewed.isna() | ~renewed.isin([0, 1])).sum()),
    }
