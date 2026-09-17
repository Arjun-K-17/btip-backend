from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Company, FinancialData

from forecasting.forecast import forecast_values


router = APIRouter(
    prefix="/forecast",
    tags=["Forecasting"]
)


@router.post("/predict/{company_id}")
def predict_forecast(
    company_id: int,
    forecast_periods: int = 3,
    db: Session = Depends(get_db)
):
    """
    Generate revenue forecasts for a selected company.

    Flow:
        Company
          ↓
        Historical Financial Data
          ↓
        Historical Revenue
          ↓
        Forecasting Model
          ↓
        Future Revenue Predictions
    """

    # =====================================================
    # 1. Validate Forecast Period
    # =====================================================

    if forecast_periods < 1:
        raise HTTPException(
            status_code=400,
            detail="Forecast periods must be at least 1"
        )

    if forecast_periods > 24:
        raise HTTPException(
            status_code=400,
            detail="Forecast periods cannot exceed 24"
        )

    # =====================================================
    # 2. Verify Company
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
    # 3. Get Historical Financial Records
    # =====================================================

    records = (
        db.query(FinancialData)
        .filter(
            FinancialData.company_id == company_id
        )
        .order_by(
            FinancialData.id.asc()
        )
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for this company"
        )

    # =====================================================
    # 4. Extract Historical Revenue
    # =====================================================

    historical_values = [
        float(record.revenue)
        for record in records
        if record.revenue is not None
    ]

    if not historical_values:
        raise HTTPException(
            status_code=404,
            detail="No revenue data available for forecasting"
        )

    # =====================================================
    # 5. Validate Historical Data
    # =====================================================

    if len(historical_values) < 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least two historical revenue records "
                "are required for forecasting"
            )
        )

    # =====================================================
    # 6. Generate Forecast
    # =====================================================

    try:
        predictions = forecast_values(
            historical_values,
            forecast_periods
        )

    except Exception as exc:
        print(
            "Forecasting error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate forecast"
        )

    # =====================================================
    # 7. Validate Forecast Result
    # =====================================================

    if predictions is None:
        raise HTTPException(
            status_code=500,
            detail="Forecasting model returned no predictions"
        )

    # =====================================================
    # 8. Return Forecast
    # =====================================================

    return {
        "message": (
            "Forecast generated successfully"
        ),

        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "company_id": company_id,

        "historical_records": len(
            historical_values
        ),

        "historical_values": historical_values,

        "forecast_periods": forecast_periods,

        "predictions": predictions
    }