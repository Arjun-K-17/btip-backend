from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import (
    Company,
    FinancialData,
    Alert
)

from crisis.crisis_detector import detect_crisis


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.post("/generate/{company_id}")
def generate_alerts(
    company_id: int,
    db: Session = Depends(get_db)
):
    # ---------------------------------------------------------
    # 1. Validate company
    # ---------------------------------------------------------
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # ---------------------------------------------------------
    # 2. Get latest financial record
    # ---------------------------------------------------------
    record = (
        db.query(FinancialData)
        .filter(FinancialData.company_id == company_id)
        .order_by(FinancialData.id.desc())
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for this company"
        )

    # ---------------------------------------------------------
    # 3. Prepare financial metrics
    # ---------------------------------------------------------
    revenue = record.revenue or 0
    profit = record.profit or 0
    current_liabilities = record.current_liabilities or 0
    current_assets = record.current_assets or 0
    debt = record.debt or 0
    equity = record.equity or 0

    operating_cash_flow = record.operating_cash_flow or 0
    investing_cash_flow = record.investing_cash_flow or 0
    financing_cash_flow = record.financing_cash_flow or 0

    profit_margin = 0

    if revenue != 0:
        profit_margin = (profit / revenue) * 100

    current_ratio = 0

    if current_liabilities != 0:
        current_ratio = (
            current_assets /
            current_liabilities
        )

    debt_to_equity = 0

    if equity != 0:
        debt_to_equity = (
            debt /
            equity
        )

    net_cash_flow = (
        operating_cash_flow
        + investing_cash_flow
        + financing_cash_flow
    )

    metrics = {
        "profit_margin": profit_margin,
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "net_cash_flow": net_cash_flow
    }

    # ---------------------------------------------------------
    # 4. Detect financial crisis / risks
    # ---------------------------------------------------------
    try:
        crisis_result = detect_crisis(metrics)
    except Exception as exc:
        print("Alert crisis detection error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to detect financial risks"
        )

    if not isinstance(crisis_result, dict):
        crisis_result = {}

    risk_score = crisis_result.get(
        "risk_score",
        0
    )

    risk_level = crisis_result.get(
        "risk_level",
        "low"
    )

    warnings = crisis_result.get(
        "warnings",
        []
    )

    if warnings is None:
        warnings = []

    # ---------------------------------------------------------
    # 5. Create alert objects
    # ---------------------------------------------------------
    alerts = []

    for warning in warnings:
        alerts.append({
            "title": "Financial Risk Detected",
            "message": str(warning),
            "severity": risk_level,
            "category": "financial",
            "is_read": 0
        })

    # ---------------------------------------------------------
    # 6. Save alerts to database
    # ---------------------------------------------------------
    saved_alerts = []

    try:
        for alert_data in alerts:
            db_alert = Alert(
                company_id=company.id,
                title=alert_data["title"],
                message=alert_data["message"],
                severity=alert_data["severity"],
                category=alert_data["category"],
                is_read=alert_data["is_read"]
            )

            db.add(db_alert)
            saved_alerts.append(db_alert)

        db.commit()

        for alert in saved_alerts:
            db.refresh(alert)

    except Exception as exc:
        db.rollback()

        print("Alert database error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to save alerts"
        )

    # ---------------------------------------------------------
    # 7. Return alert information
    # ---------------------------------------------------------
    return {
        "message": "Alerts generated successfully",

        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "company_id": company.id,

        "financial_data": {
            "record_id": record.id,
            "profit_margin": profit_margin,
            "current_ratio": current_ratio,
            "debt_to_equity": debt_to_equity,
            "net_cash_flow": net_cash_flow
        },

        "risk_score": risk_score,

        "risk_level": risk_level,

        "count": len(saved_alerts),

        "alerts": [
            {
                "id": alert.id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity,
                "category": alert.category,
                "is_read": alert.is_read
            }
            for alert in saved_alerts
        ]
    }