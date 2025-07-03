import datetime as dt

import pandas as pd


def remove_duties(df: pd.DataFrame, hour=15):
    """
    Filter the DataFrame to keep only rows with hours_end_timestamp equal to the required time.

    Args:
        df (pd.DataFrame): Input DataFrame with hours_end_timestamp column
        required_time (dt.time, optional): Time to filter on. Defaults to 15:00:00.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows ending at required_time
    """
    # Validate input
    if 'hours_end_timestamp' not in df.columns:
        raise ValueError("DataFrame must contain 'hours_end_timestamp' column")

    required_time = dt.time(hour, 0, 0)
    # Convert timestamps and filter rows
    changed_rows = pd.to_datetime(df['hours_end_timestamp']).dt.time >= required_time
    df = df[changed_rows]
    df.to_csv('duty.csv', index=False)
    return df
