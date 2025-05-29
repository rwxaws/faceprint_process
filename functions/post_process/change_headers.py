import pandas as pd


def change_headers(df, arabic_headers) -> pd.DataFrame:
    df.columns = arabic_headers
    return df
