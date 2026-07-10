import pytest
from starter import renewal_rate


def test_known_rate_and_no_mutation() -> None:
    outcomes = [1, 0, 1, 1]
    assert renewal_rate(outcomes) == pytest.approx(0.75)
    assert outcomes == [1, 0, 1, 1]


@pytest.mark.parametrize("outcomes", [[], [0, 2], [1, True], [1, 0.0], (1, 0, 1)])
def test_invalid_outcomes_fail(outcomes: object) -> None:
    with pytest.raises(ValueError):
        renewal_rate(outcomes)  # type: ignore[arg-type]
