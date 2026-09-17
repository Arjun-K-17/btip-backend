def calculate_liquidity(data: dict) -> dict:
    current_assets = data.get("current_assets", 0)
    current_liabilities = data.get("current_liabilities", 0)
    cash = data.get("cash", 0)

    current_ratio = (
        current_assets / current_liabilities
        if current_liabilities != 0 else None
    )

    return {
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "cash": cash,
        "current_ratio": current_ratio
    }