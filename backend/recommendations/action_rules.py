def generate_action_rules(metrics: dict) -> list:
    """
    Generate possible recovery actions based on business problems.
    """

    actions = []

    revenue_growth = metrics.get("revenue_growth")
    profit_margin = metrics.get("profit_margin")
    debt_to_equity = metrics.get("debt_to_equity")
    current_ratio = metrics.get("current_ratio")
    net_cash_flow = metrics.get("net_cash_flow")

    if revenue_growth is not None and revenue_growth < 0:
        actions.append({
            "issue": "Revenue is declining",
            "action": "Increase revenue through sales and customer retention strategies"
        })

    if profit_margin is not None and profit_margin < 5:
        actions.append({
            "issue": "Profit margin is low",
            "action": "Reduce operating expenses and improve cost efficiency"
        })

    if debt_to_equity is not None and debt_to_equity > 2:
        actions.append({
            "issue": "Debt-to-equity is high",
            "action": "Reduce debt or restructure existing liabilities"
        })

    if current_ratio is not None and current_ratio < 1:
        actions.append({
            "issue": "Liquidity is weak",
            "action": "Improve cash availability and manage short-term liabilities"
        })

    if net_cash_flow is not None and net_cash_flow < 0:
        actions.append({
            "issue": "Cash flow is negative",
            "action": "Control cash outflows and improve operating cash generation"
        })

    return actions