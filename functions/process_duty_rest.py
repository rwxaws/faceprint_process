import pandas as pd

from functions.utils import load_sql, normalize_time, military_time

def process_duty_rest(con, duty_file, rest_files, target_date):

    # create duty & rest tables
    con.sql(load_sql("sql/duty_rest/create_duty_rest_tables.sql"))

    # insert into rest staging
    for file in rest_files:
        rest_df = pd.read_excel(
            file,
            skiprows=1,
            usecols="A:C,G,I:O,Q:R",
            header=None,
            dtype=str
        )
        con.sql(load_sql("sql/duty_rest/insert_rest_staging.sql"))

    # insert into duty staging
    duty_df = pd.read_excel(
        duty_file,
        skiprows=1,
        usecols="A:C,J:L,N:O",
        header=None,
        dtype=str
    )
    con.sql(load_sql("sql/duty_rest/insert_duty_staging.sql"))

    # fix start & end_hour
    normalize_time(con, "duty_staging", "end_hour")
    military_time(con, "duty_staging", "start_hour")
    military_time(con, "duty_staging", "end_hour")

    # fix start_hour & end_hour
    normalize_time(con, "rest_staging", "end_hour")
    military_time(con, "rest_staging", "start_hour")
    military_time(con, "rest_staging", "end_hour")

    # insert into tables
    con.sql(load_sql("sql/duty_rest/insert_duty_rest_tables.sql"))

    # drop staging tables
    con.sql(load_sql("sql/duty_rest/drop_staging_tables.sql"))

    # filtering (only target date)
    con.execute(load_sql("sql/duty_rest/filter_duty_fullday.sql"), [target_date])
    con.execute(load_sql("sql/duty_rest/filter_rest_day.sql"), [target_date])
    con.execute(load_sql("sql/duty_rest/filter_rest_time.sql"), [target_date])
    con.execute(load_sql("sql/duty_rest/filter_duty_halfday.sql"), [target_date])
