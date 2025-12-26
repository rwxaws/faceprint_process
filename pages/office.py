import duckdb as dd
import streamlit as st

from arabic_names import labels, report_columns
from functions.process_report import process_report
from functions.utils import cleanup_tables, rtl_text


def process_files(report_file, emp_file, rest_files, duty_file):
    con = dd.connect(":memory:")

    try:
        process_report(con, report_file, emp_file, duty_file, rest_files)
    except ValueError as e:
        rtl_text(str(e), component="h2")
        return

    # export dataframes
    attendant_df = (
        con.sql("SELECT * FROM export_report_attendant")
        .df()
        .astype(str)
        .replace(["NaT", "<NA>", "None"], "")
    )

    excused_full_df = (
        con.sql("SELECT * FROM export_report_excused_full")
        .df()
        .astype(str)
        .replace(["NaT", "<NA>", "None"], "")
    )
    excused_half_df = (
        con.sql("SELECT * FROM export_report_excused_half")
        .df()
        .astype(str)
        .replace(["NaT", "<NA>", "None"], "")
    )
    unexcused_df = (
        con.sql("SELECT * FROM export_report_unexcused")
        .df()
        .astype(str)
        .replace(["NaT", "<NA>", "None"], "")
    )

    # set arabic column names
    attendant_df.columns = report_columns["attendant_df"]
    excused_full_df.columns = report_columns["excused_full_df"]
    excused_half_df.columns = report_columns["excused_half_df"]
    unexcused_df.columns = report_columns["unexcused_df"]

    rtl_text(labels["attendant"], component="h2")
    st.dataframe(attendant_df, hide_index=True)

    rtl_text(labels["fullday"], component="h2")
    st.dataframe(excused_full_df, hide_index=True)

    rtl_text(labels["halfday"], component="h2")
    st.dataframe(excused_half_df, hide_index=True)

    rtl_text(labels["unexcused"], component="h2")
    st.dataframe(unexcused_df, hide_index=True)

    cleanup_tables(con)


rtl_text(labels["office"], component="h1")

rtl_text(labels["report_faceprint"], component="markdown")
report_file = st.file_uploader("report", type="xlsm", label_visibility="collapsed")

rtl_text(labels["emp_num"], component="markdown")
emp_file = st.file_uploader("emp", type="xlsx", label_visibility="collapsed")

rtl_text(labels["rest"], component="markdown")
rest_files = st.file_uploader(
    "rest", type="xlsx", accept_multiple_files=True, label_visibility="collapsed"
)

rtl_text(labels["duty"], component="markdown")
duty_file = st.file_uploader("duty", type="xlsx", label_visibility="collapsed")

if not all([report_file, emp_file, rest_files, duty_file]):
    st.button(labels["process_button"], disabled=True)
else:
    if st.button(labels["process_button"]):
        process_files(report_file, emp_file, rest_files, duty_file)
