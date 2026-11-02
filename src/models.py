from pydantic import BaseModel, Field


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


# Create model for validation settings
class ValidationSettings(BaseModel):
    # Given code
    required_columns: list[str] = Field(default_factory=list)
    numeric_columns: list[str] = Field(default_factory=list)


# Create model for missing settings
class MissingSettings(BaseModel):
    # Given code
    enabled: bool = True
    axis: str = 'rows'


# Create model for outlier settings
class OutlierSettings(BaseModel):
    # Define attributes

    # Default is False
    enabled: bool = False
    # Default is empty list using Field
    columns: list[str] = Field(default_factory=list)
    # Default is IQR
    method: str = 'iqr'
    # Default is 1.5
    threshold: float = 1.5


# Create model for processing settings
class ProcessingSettings(BaseModel):
    # Given code
    remove_duplicates: bool = True
    missing: MissingSettings = Field(default_factory=MissingSettings)
    outliers: OutlierSettings = Field(default_factory=OutlierSettings)


# Create model to process configuration
class ProcessConfig(BaseModel):
    # Define attributes

    # Default is empty field of that model
    validation: ValidationSettings = Field(default_factory=ValidationSettings)
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)


# Create model to process report
class ProcessingReport(BaseModel):
    # Define attributes

    id: int
    validation_rows_removed: int
    cleaning_report: dict[str, int]
