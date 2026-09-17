def calculate_risk_score(metrics: dict) -> float:
    score = 0.0

    # Revenue decline
    growth = metrics.get("revenue_growth")
    if growth is not None and growth < 0:
        score += 25

    # Low profitability
    profit_margin = metrics.get("profit_margin")
    if profit_margin is not None and profit_margin < 5:
        score += 20

    # High leverage
    debt_to_equity = metrics.get("debt_to_equity")
    if debt_to_equity is not None and debt_to_equity > 2:
        score += 25

    # Poor liquidity
    current_ratio = metrics.get("current_ratio")
    if current_ratio is not None and current_ratio < 1:
        score += 20

    # Negative cash flow
    net_cash_flow = metrics.get("net_cash_flow")
    if net_cash_flow is not None and net_cash_flow < 0:
        score += 10

    return min(score, 100)