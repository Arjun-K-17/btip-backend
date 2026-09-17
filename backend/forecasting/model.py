from sklearn.linear_model import LinearRegression


def create_model() -> LinearRegression:
    """
    Create the Linear Regression model used by BTIP forecasting.
    """
    return LinearRegression()