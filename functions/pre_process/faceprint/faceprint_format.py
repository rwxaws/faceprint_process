import pandas as pd


def format_faceprint(faceprint_path: str, provided_date: str) -> pd.DataFrame:
    faceprint_df = pd.read_csv(faceprint_path, header=0, dtype='string')

    faceprint_df['date'] = pd.to_datetime(provided_date).date()
    faceprint_df['date'] = pd.to_datetime(faceprint_df['date'], format='%Y-%m-%d')
    faceprint_df['entry_timestamp'] = pd.to_datetime(faceprint_df['entry_timestamp'], format='%d/%m/%Y %H:%M:%S')
    faceprint_df['leave_timestamp'] = pd.to_datetime(faceprint_df['leave_timestamp'], format='%d/%m/%Y %H:%M:%S')

    return faceprint_df
