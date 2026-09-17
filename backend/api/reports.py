from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import (
    Company,
    AnalysisResult,
    FinancialData
)

from crisis.crisis_detector import detect_crisis
from forecasting.forecast import forecast_values

from simulation.baseline import create_baseline
from simulation.scenario_engine import apply_scenario
from simulation.projection import project_scenario
from simulation.comparison import compare_scenarios

from recommendations.recommendation_engine import generate_recommendations
from recommendations.priority import sort_recommendations

from reports.report_generator import generate_report
from reports.pdf_generator import generate_pdf_report


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# =========================================================
# Build Complete Report Data
# =========================================================

def build_report_data(
    analysis_id: int,
    db: Session
):
    # -----------------------------------------------------
    # 1. Get Analysis Result
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 2. Validate Company
    # -----------------------------------------------------

    company = (
        db.query(Company)
        .filter(Company.id == analysis.company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company associated with this analysis was not found"
        )

    company_id = company.id

    # -----------------------------------------------------
    # 3. Get Latest Financial Record
    # -----------------------------------------------------

    latest_record = (
        db.query(FinancialData)
        .filter(
            FinancialData.company_id == company_id
        )
        .order_by(FinancialData.id.desc())
        .first()
    )

    if not latest_record:
        raise HTTPException(
            status_code=404,
            detail="No financial data found for this company"
        )

    # -----------------------------------------------------
    # 4. Prepare Financial Data
    # -----------------------------------------------------

    revenue = latest_record.revenue or 0
    expenses = latest_record.expenses or 0
    profit = latest_record.profit or 0

    cash = latest_record.cash or 0
    debt = latest_record.debt or 0

    current_assets = latest_record.current_assets or 0
    current_liabilities = latest_record.current_liabilities or 0

    equity = latest_record.equity or 0
    assets = latest_record.assets or 0
    liabilities = latest_record.liabilities or 0

    operating_cash_flow = (
        latest_record.operating_cash_flow or 0
    )

    investing_cash_flow = (
        latest_record.investing_cash_flow or 0
    )

    financing_cash_flow = (
        latest_record.financing_cash_flow or 0
    )

    # Calculate net cash flow because FinancialData
    # does not contain a net_cash_flow column.
    net_cash_flow = (
        operating_cash_flow
        + investing_cash_flow
        + financing_cash_flow
    )

    # Use saved analysis metrics when available.
    profit_margin = (
        analysis.profit_margin
        if analysis.profit_margin is not None
        else (
            (profit / revenue) * 100
            if revenue != 0
            else 0
        )
    )

    current_ratio = (
        analysis.current_ratio
        if analysis.current_ratio is not None
        else (
            current_assets / current_liabilities
            if current_liabilities != 0
            else 0
        )
    )

    debt_to_equity = (
        analysis.debt_to_equity
        if analysis.debt_to_equity is not None
        else (
            debt / equity
            if equity != 0
            else 0
        )
    )

    if analysis.net_cash_flow is not None:
        net_cash_flow = analysis.net_cash_flow

    financial = {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "cash": cash,
        "debt": debt,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "equity": equity,
        "assets": assets,
        "liabilities": liabilities,
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "net_cash_flow": net_cash_flow,
        "profit_margin": profit_margin,
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity
    }

    # -----------------------------------------------------
    # 5. Crisis Detection
    # -----------------------------------------------------

    crisis_metrics = {
        "profit_margin": profit_margin,
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "net_cash_flow": net_cash_flow
    }

    try:
        crisis = detect_crisis(crisis_metrics)
    except Exception as exc:
        print("Report crisis detection error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate crisis analysis for report"
        )

    if not isinstance(crisis, dict):
        crisis = {}

    warnings = crisis.get(
        "warnings",
        []
    )

    if warnings is None:
        warnings = []

    # -----------------------------------------------------
    # 6. Get Historical Revenue
    # -----------------------------------------------------

    records = (
        db.query(FinancialData)
        .filter(
            FinancialData.company_id == company_id
        )
        .order_by(FinancialData.id.asc())
        .all()
    )

    historical_values = [
        float(record.revenue)
        for record in records
        if record.revenue is not None
    ]

    # -----------------------------------------------------
    # 7. Revenue Forecast
    # -----------------------------------------------------

    predictions = []

    if len(historical_values) >= 2:
        try:
            predictions = forecast_values(
                historical_values,
                3
            )
        except Exception as exc:
            print("Report forecasting error:", exc)

            raise HTTPException(
                status_code=500,
                detail="Unable to generate revenue forecast for report"
            )

    if predictions is None:
        predictions = []

    forecast = {
        "historical_values": historical_values,
        "predictions": predictions,
        "forecast_periods": len(predictions)
    }

    # -----------------------------------------------------
    # 8. Recovery Simulation
    # -----------------------------------------------------

    baseline_data = {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "cash": cash,
        "debt": debt
    }

    try:
        baseline = create_baseline(
            baseline_data
        )
    except Exception as exc:
        print("Report simulation baseline error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to create simulation baseline for report"
        )

    # These are recovery assumptions, not fixed company data.
    scenario = {
        "revenue_growth": 0.10,
        "expense_reduction": 0.05,
        "debt_reduction": 0.10
    }

    try:
        simulated_data = apply_scenario(
            baseline,
            scenario
        )
    except Exception as exc:
        print("Report simulation scenario error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to apply recovery scenario for report"
        )

    try:
        projection = project_scenario(
            simulated_data
        )
    except Exception as exc:
        print("Report simulation projection error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate recovery projection for report"
        )

    try:
        comparison = compare_scenarios(
            baseline,
            projection
        )
    except Exception as exc:
        print("Report simulation comparison error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to compare recovery scenarios for report"
        )

    simulation = {
        "baseline": baseline,
        "scenario": scenario,
        "projection": projection,
        "comparison": comparison
    }

    # -----------------------------------------------------
    # 9. Generate Recommendations
    # -----------------------------------------------------

    try:
        recommendations = generate_recommendations(
            crisis_metrics
        )
    except Exception as exc:
        print("Report recommendation generation error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate recommendations for report"
        )

    if recommendations is None:
        recommendations = []

    try:
        recommendations = sort_recommendations(
            recommendations
        )
    except Exception as exc:
        print("Report recommendation sorting error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to sort recommendations for report"
        )

    if recommendations is None:
        recommendations = []

    # -----------------------------------------------------
    # 10. Final Report Data
    # -----------------------------------------------------

    report_data = {
        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "company_id": company_id,

        "analysis_id": analysis_id,

        "financial": financial,

        "crisis": {
            "risk_score": crisis.get(
                "risk_score",
                0
            ),

            "risk_level": crisis.get(
                "risk_level",
                "low"
            ),

            "crisis_detected": crisis.get(
                "crisis_detected",
                False
            ),

            "warnings": warnings
        },

        "forecast": forecast,

        "simulation": simulation,

        "recommendations": recommendations
    }

    return report_data


# =========================================================
# JSON Report
# =========================================================

@router.get("/generate/{analysis_id}")
def get_report(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Build complete report data
    # -----------------------------------------------------

    report_data = build_report_data(
        analysis_id,
        db
    )

    # -----------------------------------------------------
    # Generate JSON report
    # -----------------------------------------------------

    try:
        report = generate_report(
            company_id=report_data["company_id"],
            analysis={
                "profit_margin": report_data[
                    "financial"
                ]["profit_margin"],

                "current_ratio": report_data[
                    "financial"
                ]["current_ratio"],

                "debt_to_equity": report_data[
                    "financial"
                ]["debt_to_equity"],

                "net_cash_flow": report_data[
                    "financial"
                ]["net_cash_flow"]
            }
        )
    except Exception as exc:
        print("Report generation error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate report"
        )

    return {
        "message": "Report generated successfully",

        "analysis_id": analysis_id,

        "company": report_data["company"],

        "report": report
    }


# =========================================================
# Download Professional PDF
# =========================================================

@router.get("/download/{analysis_id}")
def download_pdf_report(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Build complete report
    # -----------------------------------------------------

    report_data = build_report_data(
        analysis_id,
        db
    )

    # -----------------------------------------------------
    # Generate PDF
    # -----------------------------------------------------

    try:
        pdf_buffer = generate_pdf_report(
            report_data
        )
    except Exception as exc:
        print("PDF generation error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate PDF report"
        )

    if pdf_buffer is None:
        raise HTTPException(
            status_code=500,
            detail="PDF generator returned no data"
        )

    # -----------------------------------------------------
    # Create professional filename
    # -----------------------------------------------------

    filename = (
        "BTIP_Financial_Turnaround_Report_"
        f"Company_{report_data['company_id']}_"
        f"Analysis_{analysis_id}.pdf"
    )

    # -----------------------------------------------------
    # Return PDF
    # -----------------------------------------------------

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        }
    )