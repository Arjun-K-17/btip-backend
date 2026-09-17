import pandas as pd


REQUIRED_FINANCIAL_COLUMNS = [
    "revenue",
    "expenses",
    "profit",
    "assets",
    "liabilities",
    "debt",
    "equity",
    "cash",
]


def validate_dataset(dataframe: pd.DataFrame) -> dict:
    """
    Perform basic validation of a financial dataset.
    """

    if dataframe.empty:
        return {
            "valid": False,
            "message": "Dataset is empty",
            "missing_columns": REQUIRED_FINANCIAL_COLUMNS,
        }

    columns = {
        str(column).strip().lower()
        for column in dataframe.columns
    }

    missing_columns = [
        column
        for column in REQUIRED_FINANCIAL_COLUMNS
        if column not in columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "message": "Required financial columns are missing",
            "missing_columns": missing_columns,
        }

    return {
        "valid": True,
        "message": "Dataset passed basic validation",
        "missing_columns": [],
    }