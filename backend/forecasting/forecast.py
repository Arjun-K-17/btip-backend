def forecast_values(historical_values: list, forecast_periods: int = 3):
    if not historical_values:
        return []

    # If only one historical value exists,
    # use it as the prediction for future periods
    if len(historical_values) == 1:
        return [historical_values[0]] * forecast_periods

    predictions = []

    # Calculate the average change between values
    changes = []

    for i in range(1, len(historical_values)):
        change = historical_values[i] - historical_values[i - 1]
        changes.append(change)

    average_change = sum(changes) / len(changes)

    last_value = historical_values[-1]

    # Generate future predictions
    for _ in range(forecast_periods):
        next_value = last_value + average_change
        predictions.append(round(next_value, 2))
        last_value = next_value

    return predictions