from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int | None = None
    title: str
    message: str
    severity: str = "medium"
    category: str = "financial"
    is_read: bool = False