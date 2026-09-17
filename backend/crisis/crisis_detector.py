from crisis.risk_score import calculate_risk_score
from crisis.trend_rules import detect_trends


def detect_crisis(metrics: dict) -> dict:
    risk_score = calculate_risk_score(metrics)
    warnings = detect_trends(metrics)

    if risk_score >= 70:
        risk_level = "critical"
    elif risk_score >= 40:
        risk_level = "high"
    elif risk_score >= 20:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "crisis_detected": risk_score >= 40,
        "warnings": warnings
    }