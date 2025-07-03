import pandas as pd

import config.headers as headers


def drop_duty_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unnecessary columns and rows with missing data in required columns.

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: DataFrame with unnecessary columns removed and NA rows filtered
    """

    # Validate that required columns exist in the DataFrame
    missing_cols = set(headers.DROPPEDCOLUMNS.duty_required_columns) - set(df.columns)

    if missing_cols:
        raise ValueError(f"Required columns missing from DataFrame: {', '.join(missing_cols)}")

    # Drop columns and rows as specified
    df.drop(columns=headers.DROPPEDCOLUMNS.duty_dropped_colums, inplace=True)
    df.dropna(subset=headers.DROPPEDCOLUMNS.duty_required_columns, inplace=True)

    return df
