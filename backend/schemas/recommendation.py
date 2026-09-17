from pydantic import BaseModel, Field
from typing import Dict, Any


class RecommendationResponse(BaseModel):
    id: int | None = None
    title: str
    description: str
    priority: str = "medium"

    issue: str = ""
    action: str = ""

    expected_impact: Dict[str, Any] = Field(default_factory=dict)