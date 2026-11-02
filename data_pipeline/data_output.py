import logging
from pathlib import Path

# Create logger
logger = logging.getLogger(__name__)

# Create function to save data
def save_data(df, filepath):
    # Define path
    path = Path(filepath)
    # Create location if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    # Save to CSV at path, don't save row indices
    df.to_csv(path, index=False)
    # Calculate row count
    row_count = len(df)
    # Log message
    logger.debug(f'Saved {row_count} rows to {filepath}')

    return filepath