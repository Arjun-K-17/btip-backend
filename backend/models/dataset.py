from dataclasses import dataclass
from typing import Optional


@dataclass
class Dataset:
    id: Optional[int] = None
    filename: str = ""
    file_type: str = ""
    company_id: Optional[int] = None
    status: str = "uploaded"
    rows: int = 0
    columns: int = 0