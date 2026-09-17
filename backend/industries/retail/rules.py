RETAIL_RULES = {
    "low_inventory_turnover": {
        "threshold": 2,
        "message": "Inventory turnover is low",
        "action": "Optimize inventory levels and reduce slow-moving stock"
    },
    "low_average_order_value": {
        "threshold": 500,
        "message": "Average order value is low",
        "action": "Use cross-selling, upselling, and product bundles"
    },
    "high_inventory_value": {
        "threshold": 1000000,
        "message": "Inventory value is high",
        "action": "Reduce excess inventory and improve stock planning"
    }
}


def get_retail_rules() -> dict:
    """
    Return retail-specific business rules.
    """

    return RETAIL_RULES.copy()