def compare_scenarios(baseline: dict, projection: dict) -> dict:
    baseline_revenue = baseline.get("revenue", 0)
    projected_revenue = projection.get("revenue", 0)

    baseline_profit = baseline.get("profit", 0)
    projected_profit = projection.get("profit", 0)

    baseline_debt = baseline.get("debt", 0)
    projected_debt = projection.get("debt", 0)

    return {
        "revenue_change": round(
            projected_revenue - baseline_revenue, 2
        ),
        "profit_change": round(
            projected_profit - baseline_profit, 2
        ),
        "debt_change": round(
            projected_debt - baseline_debt, 2
        )
    }