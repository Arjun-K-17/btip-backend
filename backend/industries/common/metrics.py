COMMON_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "assets",
    "liabilities",
    "debt",
    "equity",
    "cash",
]


def get_common_metrics() -> list:
    """
    Return the financial metrics shared across all industries.
    """

    return COMMON_METRICS.copy()