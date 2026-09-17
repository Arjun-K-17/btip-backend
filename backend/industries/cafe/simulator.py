def simulate_cafe_recovery(
    metrics: dict,
    actions: dict
) -> dict:
    """
    Apply café-specific recovery actions.
    """

    result = metrics.copy()

    # Increase average order value
    aov_increase = actions.get("average_order_value_increase", 0)

    if "average_order_value" in result:
        result["average_order_value"] *= (
            1 + aov_increase / 100
        )

    # Reduce food cost
    food_cost_reduction = actions.get("food_cost_reduction", 0)

    if "food_cost" in result:
        result["food_cost"] *= (
            1 - food_cost_reduction / 100
        )

    # Reduce labor cost
    labor_cost_reduction = actions.get("labor_cost_reduction", 0)

    if "labor_cost" in result:
        result["labor_cost"] *= (
            1 - labor_cost_reduction / 100
        )

    return result