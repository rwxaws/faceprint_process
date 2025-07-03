import pandas as pd

from functions.pre_process.vacation.drop_cols import drop_vacation_cols
from functions.pre_process.vacation.hours_timestamp import hours_timestamp_fixer
from functions.pre_process.vacation.split_days import split_days

import config.headers


def combine_vacations(file_paths):
    dfs = []

    for file_path in file_paths:
        temp_df = pd.read_excel(file_path, dtype='string', header=None, skiprows=1)
        temp_df.columns = config.headers.PREPROCESSINGHEADERS.vacation_header
        dfs.append(temp_df)

    return pd.concat(dfs, ignore_index=True)


def column_dtype_fixer(df):
    df['hours_start_timestamp'] = pd.to_datetime(df['hours_start_timestamp'])
    df['hours_end_timestamp']   = pd.to_datetime(df['hours_end_timestamp'])
    df['vacation_from']         = pd.to_datetime(df['vacation_from'])
    df['vacation_to']           = pd.to_datetime(df['vacation_to'])
    df['date']                  = pd.to_datetime(df['date'], format='mixed')

    return df


def vacation_process(vacation_file_paths: str) -> pd.DataFrame:
    vacation_df = combine_vacations(vacation_file_paths)

    vacation_df = (vacation_df
                   .pipe(drop_vacation_cols)
                   .pipe(hours_timestamp_fixer)
                   .pipe(split_days)
                   .pipe(column_dtype_fixer)
                   )

    return vacation_df
