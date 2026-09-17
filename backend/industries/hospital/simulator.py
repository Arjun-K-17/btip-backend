def simulate_hospital_recovery(
    metrics: dict,
    actions: dict
) -> dict:
    """
    Apply hospital-specific recovery actions.
    """

    result = metrics.copy()

    # Increase bed occupancy
    occupancy_increase = actions.get("bed_occupancy_increase", 0)

    if "bed_occupancy_rate" in result:
        result["bed_occupancy_rate"] *= (
            1 + occupancy_increase / 100
        )

    # Reduce staff cost
    staff_cost_reduction = actions.get("staff_cost_reduction", 0)

    if "staff_cost" in result:
        result["staff_cost"] *= (
            1 - staff_cost_reduction / 100
        )

    # Reduce treatment cost
    treatment_cost_reduction = actions.get(
        "treatment_cost_reduction", 0
    )

    if "average_treatment_cost" in result:
        result["average_treatment_cost"] *= (
            1 - treatment_cost_reduction / 100
        )

    return result