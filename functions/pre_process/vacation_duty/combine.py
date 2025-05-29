import pandas as pd


def combine_vacation_duty(vacation_df, duty_df):
    common_cols = list(set(vacation_df.columns) & set(duty_df.columns))

    for col in vacation_df.columns:
        if col not in common_cols:
            duty_df[col] = pd.Series(dtype=vacation_df[col].dtype)

    vacation_duty = pd.concat([vacation_df, duty_df], axis=0, ignore_index=True)
    return vacation_duty
