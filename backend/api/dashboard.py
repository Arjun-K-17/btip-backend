from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import (
    Company,
    FinancialData,
    AnalysisResult,
    Recommendation,
    Alert
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =========================================================
# Get All Companies
# =========================================================

@router.get("/companies")
def get_companies(
    db: Session = Depends(get_db)
):
    companies = (
        db.query(Company)
        .order_by(Company.id)
        .all()
    )

    return {
        "count": len(companies),
        "companies": [
            {
                "id": company.id,
                "name": company.name,
                "industry": company.industry,
                "owner_email": company.owner_email
            }
            for company in companies
        ]
    }


# =========================================================
# Get Dashboard Data
# =========================================================

@router.get("/{company_id}")
def get_dashboard(
    company_id: int,
    db: Session = Depends(get_db)
):

    # =====================================================
    # Company
    # =====================================================

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

    # =====================================================
    # Latest Financial Data
    # =====================================================

    financial = (
        db.query(FinancialData)
        .filter(
            FinancialData.company_id == company_id
        )
        .order_by(
            FinancialData.id.desc()
        )
        .first()
    )

    if not financial:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for this company"
        )

    # =====================================================
    # Latest Analysis
    # =====================================================

    analysis = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.company_id == company_id
        )
        .order_by(
            AnalysisResult.id.desc()
        )
        .first()
    )

    # =====================================================
    # Recommendations
    # =====================================================

    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.company_id == company_id
        )
        .order_by(
            Recommendation.id.desc()
        )
        .limit(5)
        .all()
    )

    # =====================================================
    # Alerts
    # =====================================================

    alerts = (
        db.query(Alert)
        .filter(
            Alert.company_id == company_id
        )
        .order_by(
            Alert.id.desc()
        )
        .limit(5)
        .all()
    )

    # =====================================================
    # Financial Metrics
    # =====================================================

    revenue = financial.revenue or 0
    expenses = financial.expenses or 0
    profit = financial.profit or 0
    cash = financial.cash or 0
    debt = financial.debt or 0
    equity = financial.equity or 0

    # =====================================================
    # Calculated Metrics
    # =====================================================

    profit_margin = None

    if revenue != 0:
        profit_margin = (
            profit / revenue
        ) * 100

    current_ratio = None

    if financial.current_liabilities:
        if financial.current_liabilities != 0:
            current_ratio = (
                financial.current_assets or 0
            ) / financial.current_liabilities

    debt_to_equity = None

    if equity != 0:
        debt_to_equity = debt / equity

    net_cash_flow = (
        (financial.operating_cash_flow or 0)
        + (financial.investing_cash_flow or 0)
        + (financial.financing_cash_flow or 0)
    )

    # =====================================================
    # Analysis Values
    # =====================================================

    risk_score = None
    risk_level = "N/A"
    crisis_detected = False

    if analysis:

        risk_score = analysis.risk_score

        risk_level = (
            analysis.risk_level
            if analysis.risk_level
            else "N/A"
        )

        crisis_detected = (
            risk_level.lower()
            not in ["low", "safe", "n/a"]
        )

        # Prefer stored analysis values

        if analysis.profit_margin is not None:
            profit_margin = analysis.profit_margin

        if analysis.current_ratio is not None:
            current_ratio = analysis.current_ratio

        if analysis.debt_to_equity is not None:
            debt_to_equity = analysis.debt_to_equity

        if analysis.net_cash_flow is not None:
            net_cash_flow = analysis.net_cash_flow

    # =====================================================
    # Response
    # =====================================================

    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "financial": {
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "profit_margin": profit_margin,
            "cash": cash,
            "debt": debt,
            "equity": equity,
            "assets": financial.assets or 0,
            "liabilities": financial.liabilities or 0,
            "current_assets": financial.current_assets or 0,
            "current_liabilities": financial.current_liabilities or 0,
            "current_ratio": current_ratio,
            "debt_to_equity": debt_to_equity,
            "operating_cash_flow": (
                financial.operating_cash_flow or 0
            ),
            "investing_cash_flow": (
                financial.investing_cash_flow or 0
            ),
            "financing_cash_flow": (
                financial.financing_cash_flow or 0
            ),
            "net_cash_flow": net_cash_flow
        },

        "risk": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "crisis_detected": crisis_detected
        },

        "recommendations": [
            {
                "id": recommendation.id,
                "title": recommendation.title,
                "description": recommendation.description,
                "priority": recommendation.priority,
                "action": recommendation.action
            }
            for recommendation in recommendations
        ],

        "alerts": [
            {
                "id": alert.id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity,
                "category": alert.category,
                "is_read": alert.is_read
            }
            for alert in alerts
        ]
    }