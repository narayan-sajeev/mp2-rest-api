import logging


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
