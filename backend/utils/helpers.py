def safe_divide(numerator: float, denominator: float):
    """
    Safely divide two numbers.
    Returns None if the denominator is zero.
    """

    if denominator == 0:
        return None

    return numerator / denominator


def percentage_change(
    current: float,
    previous: float
):
    """
    Calculate percentage change between two values.
    """

    if previous == 0:
        return None

    return ((current - previous) / previous) * 100


def clamp(
    value: float,
    minimum: float = 0,
    maximum: float = 100
) -> float:
    """
    Keep a value within a specified range.
    """

    return max(minimum, min(value, maximum))