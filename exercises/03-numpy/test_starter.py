import numpy as np
import pytest
from starter import standardize_columns


def test_standardises_columns_without_mutation() -> None:
    matrix = np.array([[1, 10], [2, 30], [3, 50]], dtype=float)
    original = matrix.copy()
    result = standardize_columns(matrix)

    assert result.shape == matrix.shape
    assert np.allclose(result.mean(axis=0), 0)
    assert np.allclose(result.std(axis=0), 1)
    assert np.array_equal(matrix, original)


@pytest.mark.parametrize(
    "matrix",
    [
        np.array([]),
        np.array([1, 2]),
        np.array([[1, 3], [1, 4]]),
        np.array([[1, 2], [np.nan, 3]]),
        np.array([[1, 2], [np.inf, 3]]),
        np.array([[1, 2], [-np.inf, 3]]),
        np.array([[1 + 2j, 2], [3 + 4j, 5]]),
    ],
)
def test_invalid_matrices_fail(matrix: np.ndarray) -> None:
    with pytest.raises(ValueError):
        standardize_columns(matrix)
