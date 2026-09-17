IT_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "cash",
    "debt",

    "active_clients",
    "recurring_revenue",
    "project_revenue",
    "employee_cost",
    "employee_count",
]


def get_it_metrics() -> list:
    """
    Return metrics specific to the IT industry.
    """

    return IT_METRICS.copy()