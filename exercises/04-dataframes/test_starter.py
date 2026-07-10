import pandas as pd
import pytest
from starter import summarise_plans


def test_summary_keeps_counts_rates_and_input() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3"],
            "plan": ["plus", "basic", "basic"],
            "renewed": [1, 1, 0],
        }
    )
    original = customers.copy(deep=True)

    result = summarise_plans(customers)

    assert result.to_dict("records") == [
        {"plan": "basic", "customers": 2, "renewal_rate": 0.5},
        {"plan": "plus", "customers": 1, "renewal_rate": 1.0},
    ]
    pd.testing.assert_frame_equal(customers, original)


@pytest.mark.parametrize(
    "customers",
    [
        pd.DataFrame({"plan": ["basic"], "renewed": [1]}),
        pd.DataFrame({"customer_id": ["C1"], "plan": ["basic"], "renewed": [2]}),
        pd.DataFrame({"customer_id": ["C1"], "plan": ["basic"], "renewed": [None]}),
        pd.DataFrame({"customer_id": [None], "plan": ["basic"], "renewed": [1]}),
        pd.DataFrame(
            {
                "customer_id": ["C1", "C1"],
                "plan": ["basic", "basic"],
                "renewed": [1, 1],
            }
        ),
    ],
)
def test_invalid_tables_fail(customers: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        summarise_plans(customers)
