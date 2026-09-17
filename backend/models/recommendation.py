from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Recommendation:
    id: Optional[int] = None
    company_id: Optional[int] = None

    title: str = ""
    description: str = ""
    priority: str = "medium"

    issue: str = ""
    action: str = ""

    expected_impact: Dict[str, Any] = None