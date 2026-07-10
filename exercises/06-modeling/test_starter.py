import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier
from starter import fit_baseline, split_features_target


def test_split_excludes_identifier_and_target() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3", "C4"],
            "usage": [2, 8, 3, 9],
            "plan": ["basic", "plus", "basic", "pro"],
            "renewed": [0, 1, 0, 1],
        }
    )
    original = customers.copy(deep=True)

    features, target = split_features_target(customers)

    assert list(features.columns) == ["usage", "plan"]
    assert target.tolist() == [0, 1, 0, 1]
    pd.testing.assert_frame_equal(customers, original)


def test_baseline_is_fitted() -> None:
    features = pd.DataFrame({"usage": [2, 8, 3, 9]})
    target = pd.Series([0, 1, 0, 1])
    model = fit_baseline(features, target)

    assert isinstance(model, DummyClassifier)
    assert model.strategy == "prior"
    assert model.predict(features).shape == (4,)


@pytest.mark.parametrize(
    "customers",
    [
        pd.DataFrame({"customer_id": ["C1"], "usage": [2]}),
        pd.DataFrame({"customer_id": ["C1"], "renewed": [1]}),
        pd.DataFrame({"customer_id": ["C1", "C2"], "usage": [2, 3], "renewed": [1, 1]}),
    ],
)
def test_invalid_boundaries_fail(customers: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        split_features_target(customers)
