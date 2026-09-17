from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    id: Optional[int] = None
    name: str = ""
    industry: str = ""
    country: str = ""
    currency: str = "INR"
    user_id: Optional[int] = None