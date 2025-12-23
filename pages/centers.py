import datetime

import duckdb as dd
import streamlit as st

from functions.process_faceprint import process_faceprint
from functions.utils import rtl_text, get_date

def process_files(faceprint_file, rest_files, duty_file, mid_target):
    con = dd.connect(":memory:")

    process_faceprint(con, faceprint_file, duty_file, rest_files, mid_target)



rtl_text("معالجة بصمات الوجه (المكاتب الفرعية)", component="h1")

rtl_text("ملف بصمة الوجه", component="markdown")
faceprint_file = st.file_uploader('faceprint', type="csv",
                                  label_visibility="collapsed")

rtl_text("ملفات الاجازات والزمنيات", component="markdown")
rest_files = st.file_uploader('rest', type="xlsx",
                              accept_multiple_files=True,
                              label_visibility="collapsed")

rtl_text("ملف الواجبات", component="markdown")
duty_file = st.file_uploader('duty', type="xlsx", label_visibility="collapsed")

rtl_text("وقت البصمة الوسطية", component="markdown")
mid_target = str(st.time_input('mid target', label_visibility="collapsed", value=datetime.time(11, 0)))

if not all([
    faceprint_file,
    rest_files,
    duty_file
]):
    st.button("بدء المعالجة", disabled=True)
else:
    if st.button("بدء المعالجة"):
        process_files(faceprint_file, rest_files, duty_file, mid_target)
