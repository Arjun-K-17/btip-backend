CAFE_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "cash",
    "debt",

    "customer_count",
    "average_order_value",
    "food_cost",
    "labor_cost",
    "store_count",
]


def get_cafe_metrics() -> list:
    """
    Return metrics specific to the cafe industry.
    """

    return CAFE_METRICS.copy()