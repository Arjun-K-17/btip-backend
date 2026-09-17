from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from api.dashboard import get_dashboard
from ai.gemini_service import ask_gemini


router = APIRouter(
    prefix="/chatbot",
    tags=["BTIP AI Assistant"]
)


class ChatRequest(BaseModel):
    company_id: int
    question: str


def build_ai_company_data(dashboard_data):
    """
    Convert the BTIP dashboard response into the flat structure
    expected by the Gemini service.
    """

    company = dashboard_data.get("company", {})
    financial = dashboard_data.get("financial", {})
    risk = dashboard_data.get("risk", {})

    recommendations = dashboard_data.get(
        "recommendations",
        []
    )

    alerts = dashboard_data.get(
        "alerts",
        []
    )

    recommendation_text = []

    for recommendation in recommendations:
        recommendation_text.append(
            {
                "title": recommendation.get("title"),
                "description": recommendation.get("description"),
                "priority": recommendation.get("priority"),
                "action": recommendation.get("action")
            }
        )

    alert_text = []

    for alert in alerts:
        alert_text.append(
            {
                "title": alert.get("title"),
                "message": alert.get("message"),
                "severity": alert.get("severity"),
                "category": alert.get("category")
            }
        )

    return {
        "company_name": company.get(
            "name",
            "Unknown"
        ),

        "industry": company.get(
            "industry",
            "Unknown"
        ),

        "revenue": financial.get(
            "revenue"
        ),

        "expenses": financial.get(
            "expenses"
        ),

        "profit": financial.get(
            "profit"
        ),

        "profit_margin": financial.get(
            "profit_margin"
        ),

        "assets": financial.get(
            "assets"
        ),

        "liabilities": financial.get(
            "liabilities"
        ),

        "debt": financial.get(
            "debt"
        ),

        "equity": financial.get(
            "equity"
        ),

        "cash": financial.get(
            "cash"
        ),

        "current_assets": financial.get(
            "current_assets"
        ),

        "current_liabilities": financial.get(
            "current_liabilities"
        ),

        "current_ratio": financial.get(
            "current_ratio"
        ),

        "debt_to_equity": financial.get(
            "debt_to_equity"
        ),

        "operating_cash_flow": financial.get(
            "operating_cash_flow"
        ),

        "investing_cash_flow": financial.get(
            "investing_cash_flow"
        ),

        "financing_cash_flow": financial.get(
            "financing_cash_flow"
        ),

        "net_cash_flow": financial.get(
            "net_cash_flow"
        ),

        "risk_score": risk.get(
            "risk_score"
        ),

        "risk_level": risk.get(
            "risk_level"
        ),

        "crisis_detected": risk.get(
            "crisis_detected"
        ),

        "recommendations": recommendation_text,

        "alerts": alert_text
    }


@router.post("/ask")
def ask_chatbot(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if len(question) > 4000:
        raise HTTPException(
            status_code=400,
            detail="Question cannot exceed 4000 characters."
        )

    if request.company_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Invalid company ID."
        )

    try:
        dashboard_data = get_dashboard(
            request.company_id,
            db
        )

        company_data = build_ai_company_data(
            dashboard_data
        )

        answer = ask_gemini(
            question,
            company_data
        )

        return {
            "message": (
                "BTIP AI Assistant response generated "
                "successfully."
            ),

            "company": dashboard_data.get(
                "company",
                {}
            ),

            "company_id": request.company_id,

            "question": question,

            "answer": answer
        }

    except HTTPException:
        raise

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

    except Exception as exc:
        print(
            "Chatbot API error:",
            exc
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the chatbot request."
            )
        )