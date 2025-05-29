import pandas as pd
from typing import List, Dict, Any

def split_days(vacation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Split vacation records into individual days.
    
    Args:
        vacation_df: DataFrame containing vacation records with multi-day vacations
        
    Returns:
        pd.DataFrame: Expanded DataFrame with one row per vacation day
    """
    new_rows: List[Dict[str, Any]] = []

    for _, row in vacation_df.iterrows():
        if pd.notna(row['num_days']):
            try:
                num_vacation_days = int(float(row['num_days']))  # Handle potential float values
                vacation_start_day = pd.to_datetime(row['vacation_from'])

                for i in range(num_vacation_days):
                    new_date = vacation_start_day + pd.Timedelta(days=i)
                    new_row = row.copy()
                    new_row['vacation_from'] = new_date.strftime('%Y-%m-%d')
                    new_row['date'] = new_date.strftime('%Y-%m-%d')  # Update date as well
                    new_rows.append(new_row)
            except (ValueError, TypeError):
                # Handle conversion errors
                new_rows.append(row)
        else:
            new_rows.append(row)

    return pd.DataFrame(new_rows)
