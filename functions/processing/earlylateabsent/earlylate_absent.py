import datetime as dt
import pandas as pd


def extract_earlylate_absent(faceprint_df: pd.DataFrame, provided_date: str) -> pd.DataFrame:
    required_date  = dt.datetime.strptime(provided_date, '%Y-%m-%d')

    is_absent    = faceprint_df['is_absent'].notna()
    is_earlylate = faceprint_df['is_early'].notna() | faceprint_df['is_late'].notna()
    is_matched   = faceprint_df['date'] == required_date

    earlylate_absent = faceprint_df[is_matched & (is_absent | is_earlylate)]

    return pd.DataFrame(earlylate_absent)
