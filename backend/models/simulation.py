from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Simulation:
    id: Optional[int] = None
    company_id: Optional[int] = None

    name: str = ""
    status: str = "created"

    # User-defined recovery actions
    actions: Dict[str, Any] = field(default_factory=dict)

    # Simulation results
    baseline: Dict[str, Any] = field(default_factory=dict)
    projection: Dict[str, Any] = field(default_factory=dict)
    comparison: Dict[str, Any] = field(default_factory=dict)