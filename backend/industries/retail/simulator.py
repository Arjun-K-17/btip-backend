def simulate_retail_recovery(
    metrics: dict,
    actions: dict
) -> dict:
    """
    Apply retail-specific recovery actions.
    """

    result = metrics.copy()

    # Increase average order value
    aov_increase = actions.get(
        "average_order_value_increase", 0
    )

    if "average_order_value" in result:
        result["average_order_value"] *= (
            1 + aov_increase / 100
        )

    # Improve inventory turnover
    turnover_increase = actions.get(
        "inventory_turnover_increase", 0
    )

    if "inventory_turnover" in result:
        result["inventory_turnover"] *= (
            1 + turnover_increase / 100
        )

    # Reduce inventory value
    inventory_reduction = actions.get(
        "inventory_reduction", 0
    )

    if "inventory_value" in result:
        result["inventory_value"] *= (
            1 - inventory_reduction / 100
        )

    return result