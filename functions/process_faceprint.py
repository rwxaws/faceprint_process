import pandas as pd

from functions.process_duty_rest import process_duty_rest
from functions.utils import load_sql, get_date


def process_faceprint(con, faceprint_file, duty_file, rest_files, mid_target):
    faceprint_df = pd.read_csv(
        faceprint_file,
        header=0,
        dtype=str
    )

    # create tables
    con.sql(load_sql("sql/faceprint/create_faceprint_tables.sql"))

    # insert into faceprint from faceprint_df
    con.execute(load_sql("sql/faceprint/insert_faceprint_df.sql"), [mid_target])

    # insert into faceprint_attendant and drop from faceprint
    con.sql(load_sql("sql/faceprint/insert_faceprint_attendant.sql"))

    # process duty and rest files
    target_date = get_date(con, "faceprint")
    process_duty_rest(con, duty_file, rest_files, target_date)

    # create full day tables (rest_day and duty_fullday) and delete from report
    con.sql(load_sql("sql/faceprint/fullday_tables.sql"))

    # create half day tables (rest_time and duty_halfday) and delete from report
    con.sql(load_sql("sql/faceprint/halfday_tables.sql"))
    # con.sql(load_sql("sql/faceprint/halfday_missing_tables.sql"))

    # create arabic tables
