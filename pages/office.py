import duckdb as dd
import streamlit as st

from functions.process_report import process_report
from functions.utils import rtl_text

def process_files(report_file, emp_file, rest_files, duty_file):
    con = dd.connect(":memory:")

    try:
        process_report(con, report_file, emp_file, duty_file, rest_files)
    except ValueError as e:
        rtl_text(str(e), component="h2")
        return

    attendant_df = con.sql("SELECT * FROM arabic_report_attendant").df().astype(str).replace(['NaT', '<NA>', 'None'], '')
    full_df      = con.sql("SELECT * FROM arabic_report_fullday").df().astype(str).replace(['NaT', '<NA>', 'None'], '')
    half_df      = con.sql("SELECT * FROM arabic_report_halfday").df().astype(str).replace(['NaT', '<NA>', 'None'], '')
    no_excuse_df = con.sql("SELECT * FROM arabic_no_excuse").df().astype(str).replace(['NaT', '<NA>', 'None'], '')


    rtl_text("حضور", component="h2")
    st.dataframe(attendant_df, hide_index=True)

    rtl_text("عذر (يوم كامل)", component="h2")
    st.dataframe(full_df, hide_index=True)

    rtl_text("عذر (زمنية/واجب)", component="h2")
    st.dataframe(half_df, hide_index=True)

    rtl_text("بدون عذر", component="h2")
    st.dataframe(no_excuse_df, hide_index=True)


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
