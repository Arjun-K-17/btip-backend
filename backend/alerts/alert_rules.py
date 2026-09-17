from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import AnalysisResult

from alerts.alert_rules import generate_alerts
from alerts.notifier import format_alerts


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.post("/generate/{analysis_id}")
def get_alerts(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    # Get analysis result from database
    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.id == analysis_id)
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis result not found"
        )

    # Prepare financial metrics
    metrics = {
        "profit_margin": analysis.profit_margin,
        "current_ratio": analysis.current_ratio,
        "debt_to_equity": analysis.debt_to_equity,
        "net_cash_flow": analysis.net_cash_flow,

        # Temporary value until revenue growth is stored
        "revenue_growth": 0
    }

    # Generate alerts
    alerts = generate_alerts(metrics)

    # Format alerts
    formatted_alerts = format_alerts(alerts)

    return {
        "message": "Alerts generated successfully",
        "analysis_id": analysis_id,
        "total_alerts": len(formatted_alerts),
        "alerts": formatted_alerts
    }