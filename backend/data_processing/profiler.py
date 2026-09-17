import pandas as pd


def profile_dataset(dataframe: pd.DataFrame) -> dict:
    """
    Generate basic information about an uploaded dataset.
    """

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": list(dataframe.columns),
        "data_types": {
            column: str(dtype)
            for column, dtype in dataframe.dtypes.items()
        },
        "missing_values": {
            column: int(value)
            for column, value in dataframe.isnull().sum().items()
        },
        "duplicate_rows": int(dataframe.duplicated().sum()),
    }