MANUFACTURING_RULES = {
    "low_capacity_utilization": {
        "threshold": 60,
        "message": "Capacity utilization is low",
        "action": "Improve production planning and machine utilization"
    },
    "high_unit_production_cost": {
        "threshold": 1000,
        "message": "Unit production cost is high",
        "action": "Optimize production processes and input costs"
    },
    "high_machine_downtime": {
        "threshold": 10,
        "message": "Machine downtime is high",
        "action": "Improve preventive maintenance and equipment reliability"
    }
}


def get_manufacturing_rules() -> dict:
    """
    Return manufacturing-specific business rules.
    """

    return MANUFACTURING_RULES.copy()