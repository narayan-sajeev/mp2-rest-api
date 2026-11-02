import json
import logging
from pathlib import Path

import pandas as pd
import yaml

# Create logger
logger = logging.getLogger(__name__)


# Create function to load CSV
def load_csv(filepath):
    # Read CSV
    df = pd.read_csv(filepath)
    # Log message
    logger.info(f'Loaded CSV file: {filepath} ({len(df)} rows)')

    return df


# Create function to load JSON
def load_json(filepath):
    # Read JSON
    with open(filepath, 'r') as f:
        # Load file
        data = json.load(f)
    # Log message
    logger.info(f'Loaded JSON file: {filepath}')

    return data


# Create function to load YAML
def load_yaml(filepath):
    # Read YAML
    with open(filepath) as f:
        # Load file
        data = yaml.safe_load(f)
    # Log message
    logger.info(f'Loaded YAML file: {filepath}')

    return data


# Create a function to load data
def load_data(filepath):
    # Create path
    path = Path(filepath)
    # Get extension
    ext = path.suffix.lower()

    # If CSV
    if ext == '.csv':
        # Load CSV
        return load_csv(path)
    # If JSON
    elif ext == '.json':
        # Load JSON
        return load_json(path)
    # If YAML
    elif ext == '.yaml':
        # Load YAML
        return load_yaml(path)
    # If None
    else:
        # Define error message
        msg = f'Unsupported file format: {ext}'
        # Log message
        logger.error(msg)
        # Raise error
        raise ValueError(msg)
