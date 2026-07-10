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

    working = values.astype(float)
    if not np.isfinite(working).all():
        raise ValueError("matrix values must fit in finite floating-point storage")

    standardized = np.empty_like(working)
    for column_index in range(working.shape[1]):
        column = working[:, column_index]

        # Same-sign subtraction cannot overflow and preserves tiny differences
        # between very large values. Mixed-sign values are scaled first because
        # their raw range can exceed the largest representable float.
        same_sign = np.all(column >= 0) or np.all(column <= 0)
        if same_sign:
            anchor = column[np.argmin(np.abs(column))]
            offsets = column - anchor
        else:
            magnitude = np.max(np.abs(column))
            scaled = column / magnitude
            anchor = scaled[np.argmin(np.abs(scaled))]
            offsets = scaled - anchor

        offset_scale = np.max(np.abs(offsets))
        if offset_scale == 0:
            raise ValueError("every column must vary")
        bounded = offsets / offset_scale
        centered = bounded - bounded.mean()
        standard_deviation = np.sqrt(np.mean(centered**2))
        if not np.isfinite(standard_deviation) or standard_deviation == 0:
            raise ValueError("every column must have finite, non-zero variation")

        standardized[:, column_index] = centered / standard_deviation

    if not np.isfinite(standardized).all():
        raise ValueError("standardization must produce only finite values")
    return standardized
