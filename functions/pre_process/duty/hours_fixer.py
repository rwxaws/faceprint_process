import datetime as dt

import pandas as pd

from functions.pre_process.duty.military_time import standardize_time


def hours_timestamp_fixer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix timestamp format in the hours_start_timestamp
    and hours_end_timestamp columns.

    Args:
        df (pd.DataFrame): DataFrame containing timestamp columns to fix

    Returns:
        pd.DataFrame: DataFrame with standardized timestamps
    """
    # Validate input
    required_cols = ['date', 'hours_start_timestamp', 'hours_end_timestamp']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

    cleaned_rows = []

    for _, row in df.iterrows():
        try:
            start = row['hours_start_timestamp']
            end = row['hours_end_timestamp']
            date = row['date']

            if pd.notna(date):
                date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()

            if pd.notna(start):
                start = dt.datetime.strptime(start, '%H:%M:%S')
                start = start.replace(year=date.year, month=date.month, day=date.day)
                start = standardize_time(start)
                row['hours_start_timestamp'] = start

            # end is in the format 10:30 arabic_word
            # or 3 arabic_word
            if pd.notna(end):
                end = str(end).split(' ')[0]
                if ':' in end:
                    end = dt.datetime.strptime(end, '%H:%M')
                else:
                    end = dt.datetime.strptime(end, '%H')
                end = end.replace(year=date.year, month=date.month, day=date.day)
                end = standardize_time(end)
                row['hours_end_timestamp'] = end

        except Exception as e:
            # Log the error and either skip the row or use a default value
            print(f"Error processing row: {row}, Error: {e}")
            # Add error handling strategy here

        cleaned_rows.append(row)

    df = pd.DataFrame(cleaned_rows, dtype='string')
    return df
