import pandas as pd

from functions.utils import load_sql, military_time, normalize_time


def process_excuses(con, duty_file, rest_files, target_date):
    rest_dfs = [
        pd.read_excel(file, skiprows=1, usecols="A:C,G,I:O,Q:R", header=None, dtype=str)
        for file in rest_files
    ]
    rest_df = pd.concat(rest_dfs, ignore_index=True)

    duty_df = pd.read_excel(
        duty_file, skiprows=1, usecols="A:C,J:L,N:O", header=None, dtype=str
    )

    # create duty & rest tables
    con.sql(load_sql("sql/schema/excuse_tables.sql"))

    # load duty and rest dataframes
    con.register("rest_df", rest_df)
    con.register("duty_df", duty_df)
    con.sql(load_sql("sql/excuse/load.sql"))

    # fix start & end_hour
    normalize_time(con, "raw_duty", "end_hour")
    military_time(con, "raw_duty", "start_hour")
    military_time(con, "raw_duty", "end_hour")

    # fix start_hour & end_hour
    normalize_time(con, "raw_rest", "end_hour")
    military_time(con, "raw_rest", "start_hour")
    military_time(con, "raw_rest", "end_hour")

    # split into half and full excuses
    con.sql(load_sql("sql/excuse/split.sql"))

    # filtering (only target date)
    con.sql(f"SET VARIABLE target_date = '{target_date}'")
    con.sql(load_sql("sql/excuse/filter.sql"))
