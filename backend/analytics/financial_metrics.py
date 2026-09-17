def calculate_financial_metrics(data: dict) -> dict:
    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    profit = data.get("profit", 0)

    debt = data.get("debt", 0)
    equity = data.get("equity", 0)
    cash = data.get("cash", 0)

    profit_margin = (
        (profit / revenue) * 100
        if revenue != 0 else None
    )

    debt_to_equity = (
        debt / equity
        if equity != 0 else None
    )

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": profit_margin,
        "debt_to_equity": debt_to_equity,
        "cash": cash
    }