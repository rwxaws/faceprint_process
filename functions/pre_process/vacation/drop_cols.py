import pandas as pd


def drop_vacation_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unnecessary columns and rows with missing center_name from vacation dataframe.
    
    Args:
        df: Input DataFrame containing vacation data
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with unnecessary columns removed
    """
    drop_cols = ["unit", "gov_center_name", "subunit", "position", "hours_day_name"]

    # Create a copy to avoid modifying the original dataframe
    result_df = df.copy()
    
    # Drop unwanted columns and rows with missing center_name
    result_df.drop(columns=drop_cols, inplace=True, errors='ignore')
    result_df.dropna(subset=['center_name'], inplace=True)

    return result_df
