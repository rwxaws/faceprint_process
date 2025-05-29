def drop_duty_cols(df, columns_to_drop=None, required_columns=None):
    """
    Remove unnecessary columns and rows with missing data in required columns.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        columns_to_drop (list, optional): List of column names to drop. Defaults to predefined list.
        required_columns (list, optional): List of columns that must contain values. Defaults to ['center_name'].
        inplace (bool, optional): Whether to modify df in place. Defaults to True.
        
    Returns:
        pd.DataFrame: DataFrame with unnecessary columns removed and NA rows filtered
    """
    if columns_to_drop is None:
        columns_to_drop = ['unit', 'gov_center_name', 'subunit', 'position', 'day']
    
    if required_columns is None:
        required_columns = ['center_name']
    
    # Validate that required columns exist in the DataFrame
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Required columns missing from DataFrame: {', '.join(missing_cols)}")
    
    # Drop columns and rows as specified
    df.drop(columns=columns_to_drop, inplace=True)
    df.dropna(subset=required_columns, inplace=True)
    
    return df
