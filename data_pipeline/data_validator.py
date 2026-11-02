import logging

import pandas as pd

# Create logger
logger = logging.getLogger(__name__)


# Create function to validate dataframe
def validate_dataframe(df, required_columns, numeric_columns):
    # Loop through required columns
    for col in required_columns:
        # If column not in df
        if col not in df.columns:
            # Create message
            msg = f'Required column missing: {col}'
            # Log message
            logger.error(msg)
            # Raise error
            raise ValueError(msg)

    # Calculate rows before
    rows_before = len(df)

    # Copy df before making changes
    clean_df = df.copy()

    # Given code
    for col in numeric_columns:
        invalid_rows = []
        for i, value in clean_df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    logger.warning(f'Invalid value in {col}: {value}')
                    invalid_rows.append(i)

        # Drop invalid rows
        clean_df = clean_df.drop(index=invalid_rows)
        # Convert to numeric values
        clean_df[col] = pd.to_numeric(clean_df[col])

    # Calculate rows after
    rows_after = len(clean_df)
    # Log message
    logger.debug(f'Validation: {rows_before} → {rows_after} rows')

    return clean_df
