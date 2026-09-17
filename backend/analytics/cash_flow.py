def calculate_cash_flow(data: dict) -> dict:
    operating_cash_flow = data.get("operating_cash_flow", 0)
    investing_cash_flow = data.get("investing_cash_flow", 0)
    financing_cash_flow = data.get("financing_cash_flow", 0)

    net_cash_flow = (
        operating_cash_flow
        + investing_cash_flow
        + financing_cash_flow
    )

    return {
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "net_cash_flow": net_cash_flow
    }