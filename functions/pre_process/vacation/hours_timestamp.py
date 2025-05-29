import pandas as pd
import datetime as dt
from typing import List, Dict, Any

from functions.pre_process.vacation.military_time import standardize_time

def hours_timestamp_fixer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix timestamp formats in the dataframe for hours_start_timestamp and hours_end_timestamp.
    
    Args:
        df: Input dataframe with timestamp columns
        
    Returns:
        pd.DataFrame: Dataframe with fixed timestamp formats
    """
    cleaned_rows: List[Dict[str, Any]] = []
    
    for _, row in df.iterrows():
        try:
            start = row['hours_start_timestamp']
            end = row['hours_end_timestamp']
            date = row['date']

            if pd.notna(date):
                date = pd.to_datetime(date).date()

            if pd.notna(start):
                start = pd.to_datetime(start).time()
                start_dt = dt.datetime.combine(date, start)
                row['hours_start_timestamp'] = standardize_time(start_dt)

            if pd.notna(end):
                # Parse end time from format like "10:30 صباحا" or "3 مساءا"
                end_str = str(end).split(' ')[0]
                try:
                    if ':' in end_str:
                        end_time = dt.datetime.strptime(end_str, '%H:%M').time()
                    else:
                        end_time = dt.datetime.strptime(end_str, '%H').time()
                    
                    end_dt = dt.datetime.combine(date, end_time)
                    row['hours_end_timestamp'] = standardize_time(end_dt)
                except ValueError:
                    # Log or handle invalid time format
                    row['hours_end_timestamp'] = None
            
            cleaned_rows.append(row)
        except Exception as e:
            # Consider logging the error instead of silently continuing
            continue

    return pd.DataFrame(cleaned_rows)
