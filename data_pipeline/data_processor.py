import logging

import pandas as pd

# Create logger
logger = logging.getLogger(__name__)


# Create function to remove duplicates
def remove_duplicates(df):
    # Get initial row count
    initial_count = len(df)
    # Drop duplicates
    clean_df = df.drop_duplicates()
    # Log message
    logger.debug(f'remove_duplicates: {initial_count} → {len(clean_df)} rows')

    return clean_df


# Create function to handle missing values
def handle_missing(df, axis='rows'):
    # If dropping rows
    if axis == 'rows':
        # Get initial row count
        initial_count = len(df)
        # Drop missing rows
        clean_df = df.dropna(axis=0)
        # Get final row count
        final_count = len(clean_df)
        # Log message
        logger.debug(f'handle_missing: {initial_count} → {final_count} rows')

        return clean_df

    # If dropping columns
    elif axis == 'columns':
        # Get initial column count
        initial_count = len(df.columns)
        # Drop missing columns
        clean_df = df.dropna(axis=1)
        # Get final column count
        final_count = len(clean_df.columns)
        # Log message
        logger.debug(f'handle_missing: {initial_count} → {final_count} columns')

        return clean_df

    # If neither
    else:
        # Define message
        msg = f'Unsupported axis: {axis}'
        # Log message
        logger.error(msg)
        # Raise error
        raise ValueError(msg)


# Create function to remove outliers
def remove_outliers(df, columns, method, threshold):
    # If method is invalid
    if method not in ['iqr', 'zscore']:
        # Define message
        msg = f'Unsupported outlier method: {method}'
        # Log message
        logger.error(msg)
        # Raise error
        raise ValueError(msg)

    # Loop through provided columns
    for col in columns:
        # If column not in df
        if col not in df.columns:
            # Log message
            logger.warning(f'Column not found: {col}')
            # Move on
            continue

        # If column is not numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Log message
            logger.warning(f'Column not numeric: {col}')
            # Move on
            continue

        # Count rows
        initial_rows = len(df)

        # If method is IQR
        if method == 'iqr':
            # Get Q1 and Q3
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            # Calculate IQR
            iqr = q3 - q1
            # Get lower and upper ranges
            lower, upper = q1 - threshold * iqr, q3 + threshold * iqr

        # If method is z score
        else:
            # Get mean and standard deviation
            mean, std = df[col].mean(), df[col].std()
            # Get lower and upper ranges
            lower, upper = mean - threshold * std, mean + threshold * std

        # Filter data between ranges, copy to avoid changing original variable
        df = df[(df[col] >= lower) & (df[col] <= upper)].copy()
        # Calculate dropped rows
        removed = initial_rows - len(df)
        # Log message
        logger.debug(f'{col}: method={method}, threshold={threshold}, removed={removed}')

    return df


# Create function to process data
def process_data(df, config):
    # Get processing config
    processing = config.get('processing')

    # Check if drop duplicates to be run
    if processing.get('remove_duplicates'):
        # Remove duplicates
        df = remove_duplicates(df)

    # Get missing config
    missing = processing.get('missing')
    # Check if handle missing to be run
    if missing.get('enabled'):
        # Get axis
        axis = missing.get('axis')
        # Handle missing rows
        df = handle_missing(df, axis)

    # Get outliers config
    outliers = processing.get('outliers')
    # Check if remove outliers to be run
    if outliers.get('enabled'):
        # Get columns
        columns = outliers.get('columns')
        # Get method
        method = outliers.get('method')
        # Get threshold
        threshold = outliers.get('threshold')
        # Remove outliers
        df = remove_outliers(df, columns, method, threshold)

    return df


# Create function outputting summary dictionary
def create_cleaning_report(df_before, df_after):
    # Calculate rows before
    rows_before = len(df_before)
    # Calculate rows after
    rows_after = len(df_after)
    # Calculate rows removed
    rows_removed = rows_before - rows_after
    # Calculate columns before
    columns_before = len(df_before.columns)
    # Calculate columns after
    columns_after = len(df_after.columns)
    # Calculate columns removed
    columns_removed = columns_before - columns_after

    return {
        'rows_before': rows_before,
        'rows_after': rows_after,
        'rows_removed': rows_removed,
        'columns_before': columns_before,
        'columns_after': columns_after,
        'columns_removed': columns_removed
    }
