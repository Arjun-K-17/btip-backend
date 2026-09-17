CAFE_RULES = {
    "high_food_cost": {
        "threshold": 35,
        "message": "Food cost is high",
        "action": "Review menu pricing, suppliers, and food waste"
    },
    "high_labor_cost": {
        "threshold": 30,
        "message": "Labor cost is high",
        "action": "Optimize staffing and operating schedules"
    },
    "low_average_order_value": {
        "threshold": 200,
        "message": "Average order value is low",
        "action": "Use bundles, upselling, and premium products"
    }
}


def get_cafe_rules() -> dict:
    """
    Return café-specific business rules.
    """

    return CAFE_RULES.copy()