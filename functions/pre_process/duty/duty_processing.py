import pandas as pd

from functions.pre_process.duty.drop_cols import drop_duty_cols
from functions.pre_process.duty.hours_fixer import hours_timestamp_fixer
from functions.pre_process.duty.remove_duties import remove_duties

import config.headers as headers


def dtype_fixer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert string columns to appropriate datetime types.

    Args:
        df (pd.DataFrame): DataFrame with string timestamp columns

    Returns:
        pd.DataFrame: DataFrame with properly typed datetime columns
    """

    df['hours_start_timestamp']: pd.Series = pd.to_datetime(df['hours_start_timestamp'])
    df['hours_end_timestamp']   = pd.to_datetime(df['hours_end_timestamp'])
    df['date']                  = pd.to_datetime(df['date'])

    return df


def duty_process(duty_file_path, hour):
    """
    Process duty data from Excel file through multiple cleaning steps.

    Args:
        duty_file_path (str): Path to the Excel duty file
        data (dict): Configuration dictionary containing processing parameters

    Returns:
        pd.DataFrame: Processed duty DataFrame
    """

    # Load data with proper logging
    duty_df = pd.read_excel(duty_file_path, header=None, skiprows=1, dtype='string')
    duty_df.columns = headers.PREPROCESSINGHEADERS.duty_header

    duty_df = (duty_df
               .pipe(drop_duty_cols)
               .pipe(hours_timestamp_fixer)
               .pipe(remove_duties, hour)
               .pipe(dtype_fixer))

    return duty_df
