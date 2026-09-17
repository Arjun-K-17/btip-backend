MANUFACTURING_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "cash",
    "debt",

    "production_volume",
    "capacity_utilization",
    "unit_production_cost",
    "inventory_value",
    "machine_downtime",
]


def get_manufacturing_metrics() -> list:
    """
    Return metrics specific to the manufacturing industry.
    """

    return MANUFACTURING_METRICS.copy()