from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Company, FinancialData

from analytics.financial_metrics import calculate_financial_metrics
from analytics.profitability import calculate_profitability
from analytics.liquidity import calculate_liquidity
from analytics.leverage import calculate_leverage
from analytics.cash_flow import calculate_cash_flow

from crisis.crisis_detector import detect_crisis


router = APIRouter(
    prefix="/crisis",
    tags=["Crisis Detection"]
)


@router.post("/detect/{company_id}")
def crisis_analysis(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Perform crisis detection for a selected company.

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
    """

    # =====================================================
    # 1. Verify Company
    # =====================================================

    company = (
        db.query(Company)
        .filter(
            Company.id == company_id
        )
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
    # 4. Calculate Financial Analytics
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
    # 5. Combine All Metrics
    # =====================================================

    crisis_metrics = {
        **financial_metrics,
        **profitability,
        **liquidity,
        **leverage,
        **cash_flow
    }

    # =====================================================
    # 6. Detect Crisis
    # =====================================================

    crisis_result = detect_crisis(
        crisis_metrics
    )

    if not isinstance(crisis_result, dict):
        crisis_result = {}

    # =====================================================
    # 7. Return Crisis Analysis
    # =====================================================

    return {
        "message": (
            "Crisis detection completed successfully"
        ),

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
            "current_assets": data[
                "current_assets"
            ],
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

        "crisis_analysis": crisis_result
    }