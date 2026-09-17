RETAIL_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "cash",
    "debt",

    "customer_count",
    "average_order_value",
    "inventory_value",
    "inventory_turnover",
    "store_count",
]


def get_retail_metrics() -> list:
    """
    Return metrics specific to the retail industry.
    """

    return RETAIL_METRICS.copy()