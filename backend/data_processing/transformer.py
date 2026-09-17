import pandas as pd


def transform_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare cleaned data for BTIP analytics.
    """

    df = dataframe.copy()

    # Calculate profit if it is not already available
    if "profit" not in df.columns:
        if "revenue" in df.columns and "expenses" in df.columns:
            df["profit"] = df["revenue"] - df["expenses"]

    # Calculate profit margin
    if "revenue" in df.columns and "profit" in df.columns:
        df["profit_margin"] = 0.0

        revenue_not_zero = df["revenue"] != 0

        df.loc[revenue_not_zero, "profit_margin"] = (
            df.loc[revenue_not_zero, "profit"]
            / df.loc[revenue_not_zero, "revenue"]
        ) * 100

    # Calculate debt-to-equity ratio
    if "debt" in df.columns and "equity" in df.columns:
        df["debt_to_equity"] = 0.0

        equity_not_zero = df["equity"] != 0

        df.loc[equity_not_zero, "debt_to_equity"] = (
            df.loc[equity_not_zero, "debt"]
            / df.loc[equity_not_zero, "equity"]
        )

    return df