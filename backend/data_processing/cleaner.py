import pandas as pd


def clean_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning on the dataset.
    """

    df = dataframe.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean column names
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    # Convert numeric columns where possible
    for column in df.columns:
        converted = pd.to_numeric(df[column], errors="ignore")
        df[column] = converted

    # Fill missing numeric values with 0
    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df