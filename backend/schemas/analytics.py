from pydantic import BaseModel
from typing import Optional


class FinancialMetricsResponse(BaseModel):
    revenue: float = 0.0
    expenses: float = 0.0
    profit: float = 0.0

    debt_to_equity: Optional[float] = None
    profit_margin: Optional[float] = None
    revenue_growth: Optional[float] = None

    current_ratio: Optional[float] = None
    cash: float = 0.0