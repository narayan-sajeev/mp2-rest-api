import io
import json
import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from src import DatasetInfo, DatasetStorage, HealthResponse, setup_logging

# Set up logging
setup_logging(verbose=True)

# Create logger
logger = logging.getLogger(__name__)

# Create FastAPI
app = FastAPI(title='Data Processing API', version='1.0.0')

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
        # Raise HTTP exceptionf
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

