from dataclasses import dataclass
from typing import Optional


@dataclass
class FinancialData:
    id: Optional[int] = None
    dataset_id: Optional[int] = None
    company_id: Optional[int] = None

    period: str = ""

    revenue: float = 0.0
    expenses: float = 0.0
    profit: float = 0.0

    assets: float = 0.0
    liabilities: float = 0.0
    debt: float = 0.0
    equity: float = 0.0

    cash: float = 0.0