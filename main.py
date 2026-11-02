import io
import json
import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from data_pipeline import create_cleaning_report, process_data, validate_dataframe
from src import (DatasetInfo, DatasetStorage, HealthResponse, ProcessConfig, ProcessingReport, log_requests,
                 setup_logging)

# Set up logging
setup_logging(verbose=True)

# Create logger
logger = logging.getLogger(__name__)

# Create FastAPI
app = FastAPI(title='Data Processing API', version='1.0.0')
# Creates HTTP middleware function that applies to all HTTP requests and responses
app.middleware("http")(log_requests)

# Create storage object
storage = DatasetStorage()


# Create health route
@app.get('/health', response_model=HealthResponse)
def health_check():
    # Return application status and version
    return {'status': 'ok', 'version': '1.0.0'}


# Create upload route
@app.post('/upload', response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    # Get suffix
    suffix = Path(file.filename or '').suffix.lower()

    # If not CSV
    if suffix != '.csv':
        # Log warning
        logger.warning(f'Unsupported file format: {suffix}')
        # Raise HTTP exception
        raise HTTPException(status_code=400, detail='Only CSV files are accepted.')

    try:
        # Read contents of file
        contents = await file.read()
        # Convert to df
        df = pd.read_csv(io.BytesIO(contents))

    # If errors
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        # Log warning
        logger.warning(f'Error reading CSV file: {e}')
        # Raise HTTP exception
        raise HTTPException(status_code=400, detail='Unsupported or unreadable CSV file.')

    # Get filename
    filename = file.filename

    # Save data and get id
    dataset_id = storage.save(df, filename)

    # Log save
    logger.info(f'Uploaded dataset: id={dataset_id}, filename={filename}, rows={len(df)}')

    # Return metadata
    return storage.get_metadata(dataset_id)


# Create dataset route
@app.get('/datasets/{dataset_id}')
def get_dataset(dataset_id: int, limit: int = Query(default=100, ge=1)):
    # Get df
    df = storage.get(dataset_id)

    # If df is empty
    if df is None:
        # Log warning
        logger.warning(f'Dataset not found: {dataset_id}')
        # Raise HTTP exception
        raise HTTPException(status_code=404, detail='Dataset not found.')

    # Load records as JSON
    records = json.loads(df.head(limit).to_json(orient='records'))

    # Log message
    logger.info(f'Retrieved dataset: id={dataset_id}, returned_rows={len(records)}')

    # Return data
    return {
        'id': dataset_id,
        'data': records,
        # Total rows is total in df, not limited
        'total_rows': len(df)
    }


# Create dataset processing route
@app.post('/datasets/{dataset_id}/process', response_model=ProcessingReport)
def process_dataset(dataset_id: int, config: ProcessConfig):
    # Get df
    df = storage.get(dataset_id)

    # If df is empty
    if df is None:
        # Log warning
        logger.warning(f'Dataset not found: {dataset_id}')
        # Raise HTTP exception
        raise HTTPException(status_code=404, detail='Dataset not found.')

    # Get config settings
    config_settings = config.model_dump()
    # Get validation settings
    validation_settings = config_settings.get('validation')
    # Get numeric columns
    numeric_columns = validation_settings.get('numeric_columns')
    # Get required columns
    required_columns = validation_settings.get('required_columns')

    # Loop through numeric columns
    for col in numeric_columns:
        # If the column not in df columns
        if col not in df.columns:
            # Create message
            msg = f'Numeric column missing: {col}'
            # Log message
            logger.warning(msg)
            # Raise error
            raise HTTPException(status_code=400, detail=msg)

    # Try to validate and proces the df
    try:
        clean_df = validate_dataframe(df, required_columns, numeric_columns)
        # Calculate rows removed
        validation_rows_removed = len(df) - len(clean_df)
        # Copy df
        copy_df = clean_df.copy()
        # Process df
        processed_df = process_data(copy_df, config_settings)
        # Create cleaning report
        cleaning_report = create_cleaning_report(clean_df, processed_df)


    # If error
    except ValueError as error:
        # Log messsage
        logger.warning(f'Error in validation or processing: {error}')
        # Raise error
        raise HTTPException(status_code=400, detail=str(error))

    # Update stored df
    storage.update(dataset_id, processed_df)

    # Get rows before and after
    rows_before, rows_after = cleaning_report['rows_before'], cleaning_report['rows_after']

    # Log message
    logger.info(
        f'Processed dataset: id={dataset_id}, validation_removed={validation_rows_removed}, '
        f'rows_before={rows_before}, rows_after={rows_after}'
    )

    return {
        'id': dataset_id,
        'validation_rows_removed': validation_rows_removed,
        'cleaning_report': cleaning_report
    }
