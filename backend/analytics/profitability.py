def calculate_profitability(data: dict) -> dict:
    revenue = data.get("revenue", 0)
    profit = data.get("profit", 0)

    profit_margin = (
        (profit / revenue) * 100
        if revenue != 0 else None
    )

    return {
        "revenue": revenue,
        "profit": profit,
        "profit_margin": profit_margin
    }