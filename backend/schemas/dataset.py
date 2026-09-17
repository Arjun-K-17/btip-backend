from pydantic import BaseModel


class DatasetResponse(BaseModel):
    message: str
    filename: str
    rows: int
    columns: int
    column_names: list[str]