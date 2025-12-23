import pandas as pd

from functions.process_duty_rest import process_duty_rest
from functions.utils import load_sql,get_date


def process_report(con, report_file, emp_file, duty_file, rest_files):
    report_df = pd.read_excel(
        report_file,
        header=None,
        skiprows=1,
        usecols="B:E,I:J",
        dtype=str
    )

    emp_df = pd.read_excel(
        emp_file,
        header=None,
        skiprows=1,
        usecols="A,C",
        dtype=str
    )


    report_df["emp_voter_num"] = emp_df[0]
    report_df["target_entry"]  = emp_df[2]

    report_columns = [
        "emp_name",
        "date",
        "entry_time",
        "leave_time",
        "excuse",
        "unit",
        "emp_voter_num",
        "target_entry"
    ]

    report_df.columns = report_columns

    if len(report_df) != len(emp_df):
        raise ValueError("عدد الموظفين غير متطابق")


    # create report tables
    con.sql(load_sql("sql/report/create_report_tables.sql"))

    # insert from report_df into report table
    con.sql(load_sql("sql/report/insert_report_df.sql"))

    target_date = get_date(con, "report")

    # label early, late, and absent employees
    con.sql(load_sql("sql/report/label_earlylate_absent.sql"))

    # insert attendants into report_attendant and remove them from report
    con.sql(load_sql("sql/report/insert_report_attendant.sql"))

    # process duty and rest files
    process_duty_rest(con, duty_file, rest_files, target_date)

    # create full day tables (rest_day and duty_fullday) and delete from report
    con.sql(load_sql("sql/report/fullday_tables.sql"))

    # create half day tables (rest_time and duty_halfday) and delete from report
    con.sql(load_sql("sql/report/halfday_tables.sql"))
    con.sql(load_sql("sql/report/halfday_missing_tables.sql"))

    # create arabic tables
    con.sql(load_sql("sql/report/create_arabic_tables.sql"))
