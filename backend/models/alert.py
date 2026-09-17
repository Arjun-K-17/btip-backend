from dataclasses import dataclass
from typing import Optional


@dataclass
class Alert:
    id: Optional[int] = None
    company_id: Optional[int] = None

    title: str = ""
    message: str = ""

    severity: str = "medium"
    category: str = "financial"

    is_read: bool = False