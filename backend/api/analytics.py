from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import (
    Company,
    FinancialData,
    AnalysisResult
)

from analytics.financial_metrics import calculate_financial_metrics
from analytics.profitability import calculate_profitability
from analytics.liquidity import calculate_liquidity
from analytics.leverage import calculate_leverage
from analytics.cash_flow import calculate_cash_flow

from crisis.crisis_detector import detect_crisis


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.post("/financial/{company_id}")
def financial_analysis(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Perform complete financial analysis for a selected company.

    Flow:
        Company
          ↓
        Latest Financial Data
          ↓
        Financial Metrics
          ↓
        Profitability
          ↓
        Liquidity
          ↓
        Leverage
          ↓
        Cash Flow
          ↓
        Crisis Detection
          ↓
        Analysis Result
    """

    # =====================================================
    # 1. Verify Company
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
    # 2. Get Latest Financial Record
    # =====================================================

    record = (
        db.query(FinancialData)
        .filter(
            FinancialData.company_id == company_id
        )
        .order_by(
            FinancialData.id.desc()
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for this company"
        )

    # =====================================================
    # 3. Prepare Financial Data
    # =====================================================

    data = {
        "revenue": record.revenue or 0,
        "expenses": record.expenses or 0,
        "profit": record.profit or 0,

        "assets": record.assets or 0,
        "liabilities": record.liabilities or 0,

        "debt": record.debt or 0,
        "equity": record.equity or 0,
        "cash": record.cash or 0,

        "current_assets": (
            record.current_assets or 0
        ),

        "current_liabilities": (
            record.current_liabilities or 0
        ),

        "operating_cash_flow": (
            record.operating_cash_flow or 0
        ),

        "investing_cash_flow": (
            record.investing_cash_flow or 0
        ),

        "financing_cash_flow": (
            record.financing_cash_flow or 0
        )
    }

    # =====================================================
    # 4. Run Financial Analytics
    # =====================================================

    financial_metrics = calculate_financial_metrics(
        data
    )

    profitability = calculate_profitability(
        data
    )

    liquidity = calculate_liquidity(
        data
    )

    leverage = calculate_leverage(
        data
    )

    cash_flow = calculate_cash_flow(
        data
    )

    # =====================================================
    # 5. Combine Metrics for Crisis Detection
    # =====================================================

    crisis_metrics = {
        **financial_metrics,
        **profitability,
        **liquidity,
        **leverage,
        **cash_flow
    }

    # =====================================================
    # 6. Run Crisis and Risk Analysis
    # =====================================================

    crisis_analysis = detect_crisis(
        crisis_metrics
    )

    if not isinstance(crisis_analysis, dict):
        crisis_analysis = {}

    # =====================================================
    # 7. Extract Important Metrics
    # =====================================================

    profit_margin = (
        profitability.get(
            "profit_margin",
            0
        )
        if isinstance(
            profitability,
            dict
        )
        else 0
    )

    current_ratio = (
        liquidity.get(
            "current_ratio",
            0
        )
        if isinstance(
            liquidity,
            dict
        )
        else 0
    )

    debt_to_equity = (
        leverage.get(
            "debt_to_equity",
            0
        )
        if isinstance(
            leverage,
            dict
        )
        else 0
    )

    net_cash_flow = (
        cash_flow.get(
            "net_cash_flow",
            0
        )
        if isinstance(
            cash_flow,
            dict
        )
        else 0
    )

    # =====================================================
    # 8. Extract Risk Information
    # =====================================================

    risk_score = crisis_analysis.get(
        "risk_score",
        0
    )

    risk_level = crisis_analysis.get(
        "risk_level",
        "low"
    )

    # =====================================================
    # 9. Save Analysis Result
    # =====================================================

    analysis_result = AnalysisResult(
        company_id=company_id,

        risk_score=risk_score,

        risk_level=risk_level,

        profit_margin=profit_margin,

        current_ratio=current_ratio,

        debt_to_equity=debt_to_equity,

        net_cash_flow=net_cash_flow
    )

    try:
        db.add(analysis_result)

        db.commit()

        db.refresh(analysis_result)

    except Exception as exc:
        db.rollback()

        print(
            "Analysis database error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to save financial analysis result"
        )

    # =====================================================
    # 10. Return Complete Analysis
    # =====================================================

    return {
        "message": (
            "Financial analysis completed successfully"
        ),

        "analysis_id": analysis_result.id,

        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "company_id": company_id,

        "financial_data": {
            "record_id": record.id,
            "revenue": data["revenue"],
            "expenses": data["expenses"],
            "profit": data["profit"],
            "assets": data["assets"],
            "liabilities": data["liabilities"],
            "debt": data["debt"],
            "equity": data["equity"],
            "cash": data["cash"],
            "current_assets": data["current_assets"],
            "current_liabilities": data[
                "current_liabilities"
            ],
            "operating_cash_flow": data[
                "operating_cash_flow"
            ],
            "investing_cash_flow": data[
                "investing_cash_flow"
            ],
            "financing_cash_flow": data[
                "financing_cash_flow"
            ]
        },

        "financial_metrics": financial_metrics,

        "profitability": profitability,

        "liquidity": liquidity,

        "leverage": leverage,

        "cash_flow": cash_flow,

        "crisis_analysis": crisis_analysis
    }