import pandas as pd
import pytest
from starter import quality_report


def test_counts_failures_without_mutation() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["C1", "C1", "C3", "C4"],
            "tenure_months": [12, -1, None, 8],
            "satisfaction_score": [8.0, None, 7.0, None],
            "renewed": [1, 0, 2, None],
        }
    )
    original = customers.copy(deep=True)

    assert quality_report(customers) == {
        "rows": 4,
        "duplicate_customer_ids": 2,
        "missing_satisfaction": 2,
        "invalid_tenure": 2,
        "invalid_renewed": 2,
    }
    pd.testing.assert_frame_equal(customers, original)


def test_missing_required_column_fails() -> None:
    with pytest.raises(ValueError):
        quality_report(pd.DataFrame({"customer_id": ["C1"]}))
