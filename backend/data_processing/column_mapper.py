import pandas as pd


COLUMN_ALIASES = {
    "revenue": [
        "revenue",
        "sales",
        "total revenue",
        "total sales",
        "income"
    ],
    "expenses": [
        "expenses",
        "expense",
        "total expenses",
        "operating expenses",
        "costs"
    ],
    "profit": [
        "profit",
        "net profit",
        "net income",
        "earnings"
    ],
    "assets": [
        "assets",
        "total assets"
    ],
    "liabilities": [
        "liabilities",
        "total liabilities"
    ],
    "debt": [
        "debt",
        "total debt",
        "borrowings"
    ],
    "equity": [
        "equity",
        "shareholders equity",
        "owner equity"
    ],
    "cash": [
        "cash",
        "cash balance",
        "cash and equivalents"
    ],
}


def map_columns(dataframe: pd.DataFrame) -> dict:
    """
    Map different dataset column names to BTIP's
    standard financial column names.
    """

    mapping = {}

    normalized_columns = {
        str(column).strip().lower(): column
        for column in dataframe.columns
    }

    for standard_name, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized_columns:
                mapping[normalized_columns[alias]] = standard_name
                break

    return mapping


def apply_column_mapping(
    dataframe: pd.DataFrame,
    mapping: dict
) -> pd.DataFrame:
    """
    Rename dataset columns using the generated mapping.
    """

    return dataframe.rename(columns=mapping)