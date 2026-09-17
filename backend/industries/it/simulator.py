def simulate_it_recovery(
    metrics: dict,
    actions: dict
) -> dict:
    """
    Apply IT-specific recovery actions.
    """

    result = metrics.copy()

    # Increase recurring revenue
    recurring_revenue_increase = actions.get(
        "recurring_revenue_increase", 0
    )

    if "recurring_revenue" in result:
        result["recurring_revenue"] *= (
            1 + recurring_revenue_increase / 100
        )

    # Reduce employee cost
    employee_cost_reduction = actions.get(
        "employee_cost_reduction", 0
    )

    if "employee_cost" in result:
        result["employee_cost"] *= (
            1 - employee_cost_reduction / 100
        )

    # Increase active clients
    client_increase = actions.get(
        "active_clients_increase", 0
    )

    if "active_clients" in result:
        result["active_clients"] *= (
            1 + client_increase / 100
        )

    return result