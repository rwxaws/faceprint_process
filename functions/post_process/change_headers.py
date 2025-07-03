import pandas as pd


def change_headers(df: pd.DataFrame, arabic_headers: list[str]) -> pd.DataFrame:
    df.columns = arabic_headers
    return df
