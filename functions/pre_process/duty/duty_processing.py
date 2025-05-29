import pandas as pd

from functions.pre_process.duty.drop_cols import drop_duty_cols
from functions.pre_process.duty.hours_fixer import hours_timestamp_fixer
from functions.pre_process.duty.remove_duties import remove_duties


def dtype_fixer(df):
    """
    Convert string columns to appropriate datetime types.
    
    Args:
        df (pd.DataFrame): DataFrame with string timestamp columns
        
    Returns:
        pd.DataFrame: DataFrame with properly typed datetime columns
    """
    df['hours_start_timestamp'] = pd.to_datetime(df['hours_start_timestamp'])
    df['hours_end_timestamp']   = pd.to_datetime(df['hours_end_timestamp'])
    df['date']                  = pd.to_datetime(df['date'])

    return df


def duty_process(duty_file_path, data, hour):
    """
    Process duty data from Excel file through multiple cleaning steps.
    
    Args:
        duty_file_path (str): Path to the Excel duty file
        data (dict): Configuration dictionary containing processing parameters
        
    Returns:
        pd.DataFrame: Processed duty DataFrame
    """
    # Get header configuration
    header = data['pre_process']['duty_header']
    
    # Load data with proper logging
    duty_df = pd.read_excel(duty_file_path, header=None, skiprows=1, dtype='string')
    duty_df.columns = header
    
    # Processing pipeline with proper logging
    duty_df = drop_duty_cols(duty_df)
    duty_df = hours_timestamp_fixer(duty_df)
    duty_df = remove_duties(duty_df, hour)
    duty_df = dtype_fixer(duty_df)

    return duty_df
