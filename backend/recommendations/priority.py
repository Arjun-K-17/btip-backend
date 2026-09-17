def sort_recommendations(recommendations: list) -> list:
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    return sorted(
        recommendations,
        key=lambda item: priority_order.get(
            item.get("priority", "low"),
            3
        )
    )