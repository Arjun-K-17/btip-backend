def simulate_manufacturing_recovery(
    metrics: dict,
    actions: dict
) -> dict:
    """
    Apply manufacturing-specific recovery actions.
    """

    result = metrics.copy()

    # Increase capacity utilization
    capacity_increase = actions.get(
        "capacity_utilization_increase", 0
    )

    if "capacity_utilization" in result:
        result["capacity_utilization"] *= (
            1 + capacity_increase / 100
        )

    # Reduce production cost
    production_cost_reduction = actions.get(
        "production_cost_reduction", 0
    )

    if "unit_production_cost" in result:
        result["unit_production_cost"] *= (
            1 - production_cost_reduction / 100
        )

    # Reduce machine downtime
    downtime_reduction = actions.get(
        "machine_downtime_reduction", 0
    )

    if "machine_downtime" in result:
        result["machine_downtime"] *= (
            1 - downtime_reduction / 100
        )

    return result