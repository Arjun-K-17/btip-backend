def generate_recommendations(metrics: dict) -> list:
    """
    Generate data-driven business turnaround recommendations
    from financial health indicators.

    Expected metrics:
        profit_margin
        current_ratio
        debt_to_equity
        net_cash_flow

    Returns:
        A list of standardized recommendation dictionaries.
    """

    recommendations = []

    # =====================================================
    # 1. Safely read financial metrics
    # =====================================================

    profit_margin = metrics.get("profit_margin")
    current_ratio = metrics.get("current_ratio")
    debt_to_equity = metrics.get("debt_to_equity")
    net_cash_flow = metrics.get("net_cash_flow")

    # Convert missing / invalid values to zero
    try:
        profit_margin = float(
            profit_margin
            if profit_margin is not None
            else 0
        )
    except (TypeError, ValueError):
        profit_margin = 0

    try:
        current_ratio = float(
            current_ratio
            if current_ratio is not None
            else 0
        )
    except (TypeError, ValueError):
        current_ratio = 0

    try:
        debt_to_equity = float(
            debt_to_equity
            if debt_to_equity is not None
            else 0
        )
    except (TypeError, ValueError):
        debt_to_equity = 0

    try:
        net_cash_flow = float(
            net_cash_flow
            if net_cash_flow is not None
            else 0
        )
    except (TypeError, ValueError):
        net_cash_flow = 0

    # =====================================================
    # 2. Profitability Analysis
    # =====================================================

    if profit_margin < 0:
        recommendations.append({
            "category": "Profitability",
            "title": "Address Negative Profitability",
            "description": (
                "The company is operating with a negative profit margin, "
                "indicating that expenses are exceeding revenue."
            ),
            "action": (
                "Reduce unnecessary operating expenses, review pricing "
                "strategy, improve operational efficiency, and identify "
                "loss-making activities."
            ),
            "priority": "high"
        })

    elif profit_margin < 5:
        recommendations.append({
            "category": "Profitability",
            "title": "Improve Profit Margins",
            "description": (
                "The current profit margin is below 5%, indicating "
                "limited profitability."
            ),
            "action": (
                "Control unnecessary expenses, improve operational "
                "efficiency, review pricing, and focus on higher-margin "
                "products or services."
            ),
            "priority": "high"
        })

    elif profit_margin < 10:
        recommendations.append({
            "category": "Profitability",
            "title": "Strengthen Profitability",
            "description": (
                "Profitability is positive but remains relatively low, "
                "leaving limited protection against financial pressure."
            ),
            "action": (
                "Monitor operating costs, improve process efficiency, "
                "and identify opportunities to increase revenue margins."
            ),
            "priority": "medium"
        })

    # =====================================================
    # 3. Liquidity Analysis
    # =====================================================

    if current_ratio < 1:
        recommendations.append({
            "category": "Liquidity",
            "title": "Improve Liquidity Position",
            "description": (
                "The current ratio is below 1, indicating that current "
                "assets may not be sufficient to cover current liabilities."
            ),
            "action": (
                "Improve working-capital management, strengthen cash "
                "reserves, accelerate receivables, and reduce unnecessary "
                "short-term obligations."
            ),
            "priority": "high"
        })

    elif current_ratio < 1.5:
        recommendations.append({
            "category": "Liquidity",
            "title": "Strengthen Working Capital",
            "description": (
                "The company's liquidity position is positive but "
                "provides limited short-term financial flexibility."
            ),
            "action": (
                "Monitor receivables and payables closely, maintain "
                "adequate cash reserves, and improve working-capital "
                "efficiency."
            ),
            "priority": "medium"
        })

    # =====================================================
    # 4. Debt Management Analysis
    # =====================================================

    if debt_to_equity > 2:
        recommendations.append({
            "category": "Debt Management",
            "title": "Reduce Financial Leverage",
            "description": (
                "The debt-to-equity ratio is above 2, indicating "
                "significant reliance on debt financing."
            ),
            "action": (
                "Prioritize debt reduction, evaluate refinancing "
                "opportunities, restructure expensive loans, and "
                "avoid unnecessary additional borrowing."
            ),
            "priority": "high"
        })

    elif debt_to_equity > 1:
        recommendations.append({
            "category": "Debt Management",
            "title": "Monitor Debt Exposure",
            "description": (
                "The company has a relatively high level of debt "
                "compared with shareholder equity."
            ),
            "action": (
                "Monitor debt servicing requirements, control new "
                "borrowing, and consider gradual debt reduction."
            ),
            "priority": "medium"
        })

    # =====================================================
    # 5. Cash Flow Analysis
    # =====================================================

    if net_cash_flow < 0:
        recommendations.append({
            "category": "Cash Flow",
            "title": "Improve Cash Flow",
            "description": (
                "Net cash flow is negative, indicating that the company "
                "is experiencing a cash outflow."
            ),
            "action": (
                "Improve operating cash generation, accelerate customer "
                "collections, control discretionary spending, and review "
                "major cash outflows."
            ),
            "priority": "high"
        })

    # =====================================================
    # 6. Combined Financial Pressure
    # =====================================================

    financial_pressure = 0

    if profit_margin < 5:
        financial_pressure += 1

    if current_ratio < 1:
        financial_pressure += 1

    if debt_to_equity > 2:
        financial_pressure += 1

    if net_cash_flow < 0:
        financial_pressure += 1

    if financial_pressure >= 3:
        recommendations.append({
            "category": "Turnaround Strategy",
            "title": "Prioritize Immediate Turnaround Actions",
            "description": (
                "Multiple financial indicators show signs of financial "
                "pressure across profitability, liquidity, leverage, "
                "or cash flow."
            ),
            "action": (
                "Develop a structured turnaround plan focused first on "
                "cash preservation, cost control, liquidity improvement, "
                "and debt management."
            ),
            "priority": "high"
        })

    # =====================================================
    # 7. Healthy Financial Position
    # =====================================================

    if not recommendations:
        recommendations.append({
            "category": "Business Performance",
            "title": "Maintain Financial Performance",
            "description": (
                "The available financial indicators do not show major "
                "financial warning conditions."
            ),
            "action": (
                "Maintain the current financial strategy, continue "
                "monitoring key indicators, and identify opportunities "
                "for sustainable growth."
            ),
            "priority": "low"
        })

    return recommendations