from pydantic import BaseModel


# Create model for health response
class HealthResponse(BaseModel):
    # Define attributes
    status: str
    version: str


# Create model for dataset info
class DatasetInfo(BaseModel):
    # Define attributes
    id: int
    filename: str
    rows: int
    columns: int
    column_names: list[str]
