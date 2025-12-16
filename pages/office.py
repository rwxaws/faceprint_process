import duckdb as dd
import streamlit as st

from functions.cleanup import clean_duty, clean_report, clean_rest, get_date
from functions.filter import (
    filter_duty,
    filter_restday,
    filter_resttime,
)
from functions.utils import rtl_text
from functions.process_report.extract_excuses import extract_excuses
from functions.process_report.tables import get_excuses, get_no_excuses, get_attendant


def process_files(report_file, emp_file, rest_files, duty_file):
    con = dd.connect(":memory:")

    clean_duty(con, duty_file)
    clean_rest(con, rest_files)

    if clean_report(con, report_file, emp_file) is False:
        rtl_text("عدد الموظفين غير متطابق", component="h2")
        return

    target_date = get_date(con, "report")

    filter_duty(con, target_date)
    filter_resttime(con, target_date)
    filter_restday(con, target_date)

    extract_excuses(con)
    has_excuses = get_excuses(con)
    no_excuse = get_no_excuses(con)
    attendant = get_attendant(con)

    rtl_text("حضور", component="h2")
    st.dataframe(attendant, hide_index=True)

    rtl_text("لديه عذر", component="h2")
    st.dataframe(has_excuses, hide_index=True)

    rtl_text("بدون عذر", component="h2")
    st.dataframe(no_excuse, hide_index=True)


rtl_text("معالجة بصمات الوجه (ذي قار)", component="h1")

rtl_text("ملف بصمة الوجه", component="markdown")
report_file = st.file_uploader('report', type="xlsm",
                                  label_visibility="collapsed")

rtl_text("ارقام الموظفين", component="markdown")
emp_file = st.file_uploader('emp', type="xlsx",
                                  label_visibility="collapsed")

rtl_text("ملفات الاجازات والزمنيات", component="markdown")
rest_files = st.file_uploader('rest', type="xlsx",
                              accept_multiple_files=True,
                              label_visibility="collapsed")

rtl_text("ملف الواجبات", component="markdown")
duty_file = st.file_uploader('duty', type="xlsx", label_visibility="collapsed")

if not all([
    report_file,
    emp_file,
    rest_files,
    duty_file
]):
    st.button("بدء المعالجة", disabled=True)
else:
    if st.button("بدء المعالجة"):
        process_files(report_file, emp_file, rest_files, duty_file)
