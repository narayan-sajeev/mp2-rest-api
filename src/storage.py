import logging

# Set up logger
logger = logging.getLogger(__name__)


class DatasetStorage:
    # Initialize variables
    def __init__(self):
        self._store = {}
        self._counter = 0

    # Store a copy of the data and return a new integer ID
    def save(self, df, filename):
        self._counter += 1
        # Get dataset index
        dataset_id = self._counter
        # Update storage
        self._store[dataset_id] = {
            'filename': filename,
            'df': df.copy()
        }
        # Log update
        logger.debug(f'Stored dataset: id={dataset_id}, rows={len(df)}')

        # Return id
        return dataset_id

    # Return dataset
    def get(self, dataset_id):
        # If id doesn't exist
        if dataset_id not in self._store:
            return None

        # Get df object at that id
        df_object = self._store[dataset_id]

        # Get df and create copy
        df_copy = df_object['df'].copy()

        # Log message
        logger.debug(f'Retrieved dataset copy: id={dataset_id}, rows={len(df_copy)}')

        # Return df
        return df_copy

    # Return dataset metadata
    def get_metadata(self, dataset_id):
        # If id doesn't exist
        if dataset_id not in self._store:
            return None

        # Get df object at that id
        df_object = self._store[dataset_id]

        # Get df
        df = df_object['df']

        # Return metadata
        return {
            'id': dataset_id,
            'filename': df_object['filename'],
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }

    # Update dataset
    def update(self, dataset_id, df):
        # If id doesn't exist
        if dataset_id not in self._store:
            return False

        # Update df, create copy so it doesn't point to same df
        self._store[dataset_id]['df'] = df.copy()

        return True

    # Clear all data
    def clear(self):
        self._store.clear()
        self._counter = 0
