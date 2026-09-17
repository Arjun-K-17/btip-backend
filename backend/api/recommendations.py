from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import (
    Company,
    AnalysisResult
)

from recommendations.recommendation_engine import generate_recommendations
from recommendations.priority import sort_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/generate/{analysis_id}")
def get_recommendations(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    # ---------------------------------------------------------
    # 1. Validate analysis result
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # 2. Validate the company associated with the analysis
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # 3. Prepare financial metrics
    # ---------------------------------------------------------
    metrics = {
        "profit_margin": analysis.profit_margin or 0,
        "current_ratio": analysis.current_ratio or 0,
        "debt_to_equity": analysis.debt_to_equity or 0,
        "net_cash_flow": analysis.net_cash_flow or 0
    }

    # ---------------------------------------------------------
    # 4. Generate recommendations
    # ---------------------------------------------------------
    try:
        recommendations = generate_recommendations(metrics)
    except Exception as exc:
        print("Recommendation generation error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate recommendations"
        )

    if recommendations is None:
        recommendations = []

    # ---------------------------------------------------------
    # 5. Sort recommendations by priority
    # ---------------------------------------------------------
    try:
        sorted_recommendations = sort_recommendations(
            recommendations
        )
    except Exception as exc:
        print("Recommendation sorting error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to sort recommendations"
        )

    if sorted_recommendations is None:
        sorted_recommendations = []

    # ---------------------------------------------------------
    # 6. Save recommendations to database
    # ---------------------------------------------------------
    saved_recommendations = []

    try:
        for recommendation in sorted_recommendations:
            # Support dictionary-based recommendation output
            if isinstance(recommendation, dict):
                title = recommendation.get("title", "")
                description = recommendation.get("description", "")
                priority = recommendation.get("priority", "")
                action = recommendation.get("action", "")

            else:
                # Fallback for unexpected recommendation objects
                title = str(recommendation)
                description = ""
                priority = ""
                action = ""

            from database.models import Recommendation

            db_recommendation = Recommendation(
                company_id=company.id,
                title=title,
                description=description,
                priority=priority,
                action=action
            )

            db.add(db_recommendation)
            saved_recommendations.append(db_recommendation)

        db.commit()

        for item in saved_recommendations:
            db.refresh(item)

    except Exception as exc:
        db.rollback()

        print("Recommendation database error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Unable to save recommendations"
        )

    # ---------------------------------------------------------
    # 7. Return recommendations
    # ---------------------------------------------------------
    return {
        "message": "Recommendations generated successfully",

        "analysis_id": analysis_id,

        "company": {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "owner_email": company.owner_email
        },

        "company_id": company.id,

        "metrics": {
            "profit_margin": metrics["profit_margin"],
            "current_ratio": metrics["current_ratio"],
            "debt_to_equity": metrics["debt_to_equity"],
            "net_cash_flow": metrics["net_cash_flow"]
        },

        "recommendation_count": len(saved_recommendations),

        "recommendations": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "priority": item.priority,
                "action": item.action
            }
            for item in saved_recommendations
        ]
    }