def calculate_leverage(data: dict) -> dict:
    debt = data.get("debt", 0)
    equity = data.get("equity", 0)
    assets = data.get("assets", 0)

    debt_to_equity = (
        debt / equity
        if equity != 0 else None
    )

    debt_ratio = (
        debt / assets
        if assets != 0 else None
    )

    return {
        "debt": debt,
        "equity": equity,
        "assets": assets,
        "debt_to_equity": debt_to_equity,
        "debt_ratio": debt_ratio
    }