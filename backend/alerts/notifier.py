def format_alerts(alerts: list) -> list:
    formatted_alerts = []

    for alert in alerts:
        formatted_alerts.append({
            "type": alert.get("type"),
            "message": alert.get("message"),
            "severity": alert.get("severity"),
            "status": "active"
        })

    return formatted_alerts