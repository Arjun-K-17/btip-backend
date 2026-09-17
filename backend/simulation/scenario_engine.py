def apply_scenario(baseline: dict, scenario: dict) -> dict:
    revenue = baseline.get("revenue", 0)
    expenses = baseline.get("expenses", 0)
    debt = baseline.get("debt", 0)
    cash = baseline.get("cash", 0)

    # Apply recovery changes
    revenue_growth = scenario.get("revenue_growth", 0)
    expense_reduction = scenario.get("expense_reduction", 0)
    debt_reduction = scenario.get("debt_reduction", 0)

    new_revenue = revenue * (1 + revenue_growth)
    new_expenses = expenses * (1 - expense_reduction)
    new_debt = debt * (1 - debt_reduction)

    # Calculate new profit
    new_profit = new_revenue - new_expenses

    return {
        "revenue": round(new_revenue, 2),
        "expenses": round(new_expenses, 2),
        "profit": round(new_profit, 2),
        "cash": cash,
        "debt": round(new_debt, 2)
    }