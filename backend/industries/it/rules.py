IT_RULES = {
    "low_recurring_revenue": {
        "threshold": 30,
        "message": "Recurring revenue is low",
        "action": "Increase subscription and recurring-service revenue"
    },
    "high_employee_cost": {
        "threshold": 40,
        "message": "Employee cost is high",
        "action": "Optimize resource allocation and workforce utilization"
    },
    "low_client_count": {
        "threshold": 10,
        "message": "Active client count is low",
        "action": "Improve client acquisition and retention"
    }
}


def get_it_rules() -> dict:
    """
    Return IT-specific business rules.
    """

    return IT_RULES.copy()