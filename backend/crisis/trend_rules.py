def detect_trends(metrics: dict) -> list:
    warnings = []

    revenue_growth = metrics.get("revenue_growth")
    profit_margin = metrics.get("profit_margin")
    debt_to_equity = metrics.get("debt_to_equity")
    current_ratio = metrics.get("current_ratio")
    net_cash_flow = metrics.get("net_cash_flow")

    if revenue_growth is not None and revenue_growth < 0:
        warnings.append("Revenue is declining")

    if profit_margin is not None and profit_margin < 5:
        warnings.append("Profit margin is low")

    if debt_to_equity is not None and debt_to_equity > 2:
        warnings.append("Debt-to-equity ratio is high")

    if current_ratio is not None and current_ratio < 1:
        warnings.append("Liquidity is weak")

    if net_cash_flow is not None and net_cash_flow < 0:
        warnings.append("Cash flow is negative")

    return warnings