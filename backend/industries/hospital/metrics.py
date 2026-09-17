HOSPITAL_METRICS = [
    "revenue",
    "expenses",
    "profit",
    "cash",
    "debt",

    "patient_count",
    "bed_occupancy_rate",
    "average_treatment_cost",
    "staff_cost",
    "bed_count",
]


def get_hospital_metrics() -> list:
    """
    Return metrics specific to the hospital industry.
    """

    return HOSPITAL_METRICS.copy()