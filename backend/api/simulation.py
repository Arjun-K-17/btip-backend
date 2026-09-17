from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Company, FinancialData

from simulation.baseline import create_baseline
from simulation.scenario_engine import apply_scenario
from simulation.projection import project_scenario
from simulation.comparison import compare_scenarios


router = APIRouter(
    prefix="/simulation",
    tags=["Recovery Simulation"]
)


@router.post("/run/{company_id}")
def run_simulation(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Run a business recovery simulation for a selected company.

    Flow:
        Company
          ↓
        Latest Financial Data
          ↓
        Baseline
          ↓
        Recovery Scenario
          ↓
        Simulated Financial Data
          ↓
        Future Projection
          ↓
        Scenario Comparison
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
    # 3. Prepare Current Financial Data
    # =====================================================

    financial_data = {
        "revenue": record.revenue or 0,
        "expenses": record.expenses or 0,
        "profit": record.profit or 0,
        "cash": record.cash or 0,
        "debt": record.debt or 0
    }

    # =====================================================
    # 4. Validate Financial Data
    # =====================================================

    required_values = [
        "revenue",
        "expenses",
        "profit",
        "cash",
        "debt"
    ]

    for field in required_values:
        value = financial_data.get(field)

        if value is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Financial field '{field}' "
                    "is unavailable"
                )
            )

    # =====================================================
    # 5. Create Baseline
    # =====================================================

    try:
        baseline = create_baseline(
            financial_data
        )

    except Exception as exc:
        print(
            "Simulation baseline error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to create simulation baseline"
        )

    # =====================================================
    # 6. Define Recovery Scenario
    # =====================================================

    scenario = {
        "revenue_growth": 0.10,
        "expense_reduction": 0.05,
        "debt_reduction": 0.10
    }

    # =====================================================
    # 7. Apply Recovery Scenario
    # =====================================================

    try:
        simulated_data = apply_scenario(
            baseline,
            scenario
        )

    except Exception as exc:
        print(
            "Simulation scenario error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to apply recovery scenario"
        )

    # =====================================================
    # 8. Project Future Results
    # =====================================================

    try:
        projection = project_scenario(
            simulated_data
        )

    except Exception as exc:
        print(
            "Simulation projection error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to project recovery scenario"
        )

    # =====================================================
    # 9. Compare Baseline and Recovery Scenario
    # =====================================================

    try:
        comparison = compare_scenarios(
            baseline,
            projection
        )

    except Exception as exc:
        print(
            "Simulation comparison error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to compare simulation scenarios"
        )

    # =====================================================
    # 10. Return Complete Simulation
    # =====================================================

    return {
        "message": (
            "Recovery simulation completed successfully"
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
            "revenue": financial_data["revenue"],
            "expenses": financial_data["expenses"],
            "profit": financial_data["profit"],
            "cash": financial_data["cash"],
            "debt": financial_data["debt"]
        },

        "baseline": baseline,

        "scenario": scenario,

        "projection": projection,

        "comparison": comparison
    }