import logging
from pathlib import Path

# Create logger
logger = logging.getLogger(__name__)


# Set up logging function
def setup_logging(verbose=False):
    # DEBUG if verbose, otherwise INFO
    level = logging.DEBUG if verbose else logging.INFO

    # Configure logger
    logging.basicConfig(
        level=level,
        # asctime: timestamp
        # levelname-8s: 8 character description of level name
        # name: module name (ex: src.storage)
        # message: actual message to log
        format='%(asctime)s %(levelname)-8s %(name)s — %(message)s',
        datefmt='%H:%M:%S'
    )


# Create function to validate input
def validate_input(filepath):
    # Define path
    path = Path(filepath)

    # Check if it is a file
    if path.is_file():
        # Log message
        logger.info(f'Input file validated: {filepath}')
        return True

    # If not file, log message
    logger.error(f'Input file not found: {filepath}')
    
    return False
