import datetime as dt
import pandas as pd


def extract_attendant(faceprint_df: pd.DataFrame, provided_date: str) -> pd.DataFrame:
    required_date  = dt.datetime.strptime(provided_date, '%Y-%m-%d')

    is_attendant = faceprint_df['is_absent'].isna() & faceprint_df['is_early'].isna() & faceprint_df['is_late'].isna()
    is_matched   = faceprint_df['date'] == required_date
    attendant = pd.DataFrame(faceprint_df[is_attendant & is_matched])

    attendant['date'] = attendant['date'].dt.date
    attendant['entry_timestamp'] = attendant['entry_timestamp'].dt.time
    attendant['leave_timestamp'] = attendant['leave_timestamp'].dt.time

    return pd.DataFrame(attendant)
