HOSPITAL_RULES = {
    "low_bed_occupancy": {
        "threshold": 60,
        "message": "Bed occupancy is low",
        "action": "Improve patient acquisition and bed utilization"
    },
    "high_staff_cost": {
        "threshold": 35,
        "message": "Staff cost is high",
        "action": "Optimize staffing levels and shift allocation"
    },
    "high_treatment_cost": {
        "threshold": 5000,
        "message": "Average treatment cost is high",
        "action": "Review treatment costs and resource utilization"
    }
}


def get_hospital_rules() -> dict:
    """
    Return hospital-specific business rules.
    """

    return HOSPITAL_RULES.copy()