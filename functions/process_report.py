import pandas as pd

from functions.process_excuses import process_excuses
from functions.utils import cleanup_tables, get_date, load_sql


def process_report(con, report_file, emp_file, duty_file, rest_files):
    report_df = pd.read_excel(
        report_file, header=None, skiprows=1, usecols="B:E,I:J", dtype=str
    )

    emp_df = pd.read_excel(emp_file, header=None, skiprows=1, usecols="A,C", dtype=str)

    report_df["emp_voter_num"] = emp_df[0]
    report_df["target_entry"] = emp_df[2]

    report_columns = [
        "emp_name",
        "date",
        "entry_time",
        "leave_time",
        "excuse",
        "unit",
        "emp_voter_num",
        "target_entry",
    ]

    report_df.columns = report_columns

    if len(report_df) != len(emp_df):
        raise ValueError("عدد الموظفين غير متطابق")

    # normalize date column to ISO format (YYYY-MM-DD)
    # assumes that the day (not month) comes first or last, instead of the american way
    report_df["date"] = pd.to_datetime(report_df["date"], dayfirst=True).dt.strftime('%Y-%m-%d')

    # create report tables
    con.sql(load_sql("sql/schema/report_tables.sql"))

    # load dataframe
    con.register("report_df", report_df)
    con.sql(load_sql("sql/report/load.sql"))

    target_date = get_date(con, "report")

    # label early, late, and absent employees
    con.sql(load_sql("sql/report/label.sql"))

    # extract attendants
    con.sql(load_sql("sql/report/extract_attendant.sql"))

    # process duty and rest files
    process_excuses(con, duty_file, rest_files, target_date)

    # extract full day excuses
    con.sql(load_sql("sql/report/extract_fullday.sql"))

    # create half day excuses
    con.sql(load_sql("sql/report/extract_halfday.sql"))

    # create export tables
    con.sql(load_sql("sql/export/report.sql"))

    # clean tables
    cleanup_tables(con)
