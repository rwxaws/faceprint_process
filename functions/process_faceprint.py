import pandas as pd

from functions.process_excuses import process_excuses
from functions.utils import get_date, load_sql


def process_faceprint(con, faceprint_file, duty_file, rest_files):
    faceprint_df = pd.read_csv(faceprint_file, header=0, dtype=str)

    # create tables
    con.sql(load_sql("sql/schema/faceprint_tables.sql"))

    # load from faceprint_df
    con.register("faceprint_df", faceprint_df)
    con.sql(load_sql("sql/faceprint/load.sql"))

    # extract attendant
    con.sql(load_sql("sql/faceprint/extract_attendant.sql"))

    # process duty and rest files
    target_date = get_date(con, "faceprint")
    process_excuses(con, duty_file, rest_files, target_date)

    # create full day tables (rest_day and duty_fullday) and delete from report
    con.sql(load_sql("sql/faceprint/extract_fullday.sql"))
    # create half day tables (rest_time and duty_halfday) and delete from report
    con.sql(load_sql("sql/faceprint/extract_halfday.sql"))

    # create export tables
    con.sql(load_sql("sql/export/faceprint.sql"))
