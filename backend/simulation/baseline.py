def create_baseline(financial_data: dict) -> dict:
    return {
        "revenue": financial_data.get("revenue", 0),
        "expenses": financial_data.get("expenses", 0),
        "profit": financial_data.get("profit", 0),
        "cash": financial_data.get("cash", 0),
        "debt": financial_data.get("debt", 0)
    }