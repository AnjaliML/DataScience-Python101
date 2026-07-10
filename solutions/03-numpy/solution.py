"""Worked solution for Exercise 03."""

import numpy as np


def standardize_columns(matrix: np.ndarray) -> np.ndarray:
    """Return column-standardised values with the input shape preserved."""

    values = np.asarray(matrix)
    if values.ndim != 2 or 0 in values.shape:
        raise ValueError("matrix must be a non-empty two-dimensional array")
    is_numeric = np.issubdtype(values.dtype, np.number)
    is_complex = np.issubdtype(values.dtype, np.complexfloating)
    if not is_numeric or is_complex:
        raise ValueError("matrix must contain real numeric values")
    if not np.isfinite(values).all():
        raise ValueError("matrix must contain only finite values")

    standard_deviations = values.std(axis=0)
    if np.any(standard_deviations == 0):
        raise ValueError("every column must vary")
    return (values.astype(float) - values.mean(axis=0)) / standard_deviations
