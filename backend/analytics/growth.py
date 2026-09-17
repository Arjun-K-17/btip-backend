def calculate_growth(current_revenue: float, previous_revenue: float) -> dict:
    if previous_revenue == 0:
        return {
            "current_revenue": current_revenue,
            "previous_revenue": previous_revenue,
            "growth_rate": None
        }

    growth_rate = (
        (current_revenue - previous_revenue)
        / previous_revenue
    ) * 100

    return {
        "current_revenue": current_revenue,
        "previous_revenue": previous_revenue,
        "growth_rate": growth_rate
    }