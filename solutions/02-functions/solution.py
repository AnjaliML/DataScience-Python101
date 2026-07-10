"""Worked solution for Exercise 02."""


def renewal_rate(outcomes: list[int]) -> float:
    """Return the fraction of binary integer outcomes equal to one."""

    if type(outcomes) is not list:
        raise ValueError("outcomes must be provided as a list")
    if not outcomes:
        raise ValueError("outcomes must not be empty")
    if any(type(value) is not int or value not in {0, 1} for value in outcomes):
        raise ValueError("outcomes must contain only integer zeros and ones")
    return sum(outcomes) / len(outcomes)
