from pydantic import BaseModel, Field
from typing import Dict, Any


class SimulationRequest(BaseModel):
    name: str
    company_id: int

    actions: Dict[str, Any] = Field(default_factory=dict)


class SimulationResponse(BaseModel):
    message: str
    simulation_id: int | None = None

    baseline: Dict[str, Any] = Field(default_factory=dict)
    projection: Dict[str, Any] = Field(default_factory=dict)
    comparison: Dict[str, Any] = Field(default_factory=dict)