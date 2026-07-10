import pandas as pd
import pytest
from starter import summarise_plans


def test_summary_keeps_counts_rates_and_input() -> None:
    customers = pd.DataFrame({"plan": ["plus", "basic", "basic"], "renewed": [1, 1, 0]})
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
        pd.DataFrame({"plan": ["basic"]}),
        pd.DataFrame({"plan": ["basic"], "renewed": [2]}),
        pd.DataFrame({"plan": ["basic"], "renewed": [None]}),
    ],
)
def test_invalid_tables_fail(customers: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        summarise_plans(customers)
