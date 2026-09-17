def project_scenario(simulated_data: dict) -> dict:
    revenue = simulated_data.get("revenue", 0)
    expenses = simulated_data.get("expenses", 0)
    profit = simulated_data.get("profit", 0)
    cash = simulated_data.get("cash", 0)
    debt = simulated_data.get("debt", 0)

    # Simple one-period recovery projection
    projected_revenue = revenue * 1.05
    projected_expenses = expenses * 1.02
    projected_profit = projected_revenue - projected_expenses

    return {
        "revenue": round(projected_revenue, 2),
        "expenses": round(projected_expenses, 2),
        "profit": round(projected_profit, 2),
        "cash": cash,
        "debt": debt
    }